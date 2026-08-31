#!/usr/bin/env python3
"""One call that answers: role, model, delegation, skills. Nobody names an agent.

The user says what they want. They should not have to know that "fix the failing
auth test" is a repairer and "compare two databases" is a researcher, any more
than they should have to pick a model.

    route.py "fix the failing authentication tests"
    route.py "add status filtering to the dashboard" --level 3
    route.py "drop the legacy leads column" --json

Inference is deliberately inspectable — every decision prints the signal that
produced it, so it can be argued with. A router whose reasoning is opaque gets
obeyed when it is wrong.

What this does NOT do: classify difficulty for you. Level and risk are judgment
(CLAUDE.md §3), and a keyword list that pretended otherwise would be exactly the
fake precision the master prompt warns about. Pass --level to get the delegation
budget; without it you get the routing and a reminder to classify.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skills.py")

# Ordered: the first role whose signals match wins, so a review of a UI change
# routes to reviewer rather than builder. Order encodes intent, not frequency.
ROLES = [
    ("reviewer", ["review", "audit", "critique", "check the diff", "look over",
                  "vulnerability", "security review", "is it safe", "adversarial"]),
    ("tester", ["run the tests", "test coverage", "regression", "does it pass",
                "write tests", "add tests", "verify the suite"]),
    ("repairer", ["fix", "bug", "broken", "failing", "crash", "error", "regression in",
                  "debug", "not working", "stopped working"]),
    ("researcher", ["compare", "research", "investigate", "evaluate options",
                    "which should", "find out", "look into", "survey", "versus"]),
    ("architect", ["architecture", "design decision", "data model", "schema",
                   "root cause", "why does", "plan the", "tradeoff", "approach for"]),
    ("builder", ["add", "build", "implement", "create", "redesign", "restyle",
                 "component", "page", "ui", "dashboard", "form", "endpoint",
                 "refactor", "port", "migrate the", "migration", "column",
                 "drop the", "remove the", "rename", "schema change"]),
]

# §18 delegation budget by level.
BUDGET = {"1": 0, "2": 1, "3": 2, "4": 4, "5": None}

# Roles whose default model differs from the implementation default.
MODEL = {"reviewer": "strong", "architect": "strong",
         "tester": "fast", "researcher": "mid",
         "builder": "mid", "repairer": "mid"}

# Risk signals are ACTIONS, not topics. The first version listed "auth", so
# "fix the failing authentication tests" — a test repair touching nothing —
# came back HIGH. A flag that fires on the subject matter rather than on what
# the task DOES is a flag people learn to click past, which is worse than not
# having it.
HIGH_RISK = [
    r"\bdrop\b", r"\bdelete\b", r"\btruncate\b", r"\bdeploy\b",
    r"\bmigrat(e|ion)\b", r"\brevoke\b", r"\brotate\b", r"\bpurge\b",
    r"\bto production\b", r"\bin production\b",
    r"\bcredential", r"\bsecret", r"\bapi key", r"\bprivate key",
    r"\bcharge\b", r"\brefund\b", r"\bpayout\b",
    r"\bchange (the )?(auth|authorization|permission)", r"\bgrant\b",
]

# A question is not a task. §3: answer it, do not route it.
QUESTION = re.compile(r"^\s*(what|why|how|when|where|which|who|does|do|is|are|can|should)\b",
                      re.I)


def infer_role(task):
    t = task.lower()
    hits = []
    for role, signals in ROLES:
        matched = [s for s in signals if s in t]
        if matched:
            hits.append((role, matched))
    return hits


def risk_flags(task):
    t = task.lower()
    return [re.search(p, t).group(0) for p in HIGH_RISK if re.search(p, t)]


def routed_skills(task, role):
    cmd = [sys.executable, SKILLS, task, "--json"]
    if role:
        cmd += ["--role", role]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    try:
        return json.loads(out.stdout or "[]")
    except json.JSONDecodeError:
        return []


def main():
    ap = argparse.ArgumentParser(description="Route a task: role, model, skills")
    ap.add_argument("task")
    ap.add_argument("--level", choices=["1", "2", "3", "4", "5"])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    # Question-shaped AND no role signal. Keying only on the leading word made
    # "what is the root cause of the slow query" a lookup, when it is exactly
    # the diagnosis the architect exists for. Letting the role signals decide
    # also means this stays correct as those lists grow.
    if QUESTION.match(args.task) and not infer_role(args.task):
        if args.json:
            print(json.dumps({"role": None, "reason": "question, not a task",
                              "skills": [], "risk_flags": risk_flags(args.task)}, indent=2))
        else:
            print("ROLE      none — this is a question, not a task")
            print("          §3: answer it. No classification, no queue row, no branch.")
        return

    hits = infer_role(args.task)
    role = hits[0][0] if hits else None
    flags = risk_flags(args.task)
    skills = routed_skills(args.task, role)
    budget = BUDGET.get(args.level) if args.level else None

    if args.json:
        print(json.dumps({
            "role": role,
            "role_signals": hits[0][1] if hits else [],
            "alternatives": [h[0] for h in hits[1:]],
            "model": MODEL.get(role) if role else None,
            "level": args.level,
            "delegation_budget": budget,
            "risk_flags": flags,
            "skills": [s["name"] for s in skills],
            "skill_words": sum(s["words"] for s in skills),
        }, indent=2))
        return

    if not role:
        if flags:
            # High-risk work with no matching specialist is orchestrator work
            # WITH approval — not "just do it". Saying "probably a one-step
            # change" here would be the most dangerous wrong answer available.
            print("ROLE      none — no specialist covers this, and it is high risk")
            print("          The orchestrator owns it directly, under §3 controls.")
            print("          There is deliberately no deployer role: deployment is")
            print("          authorized, not delegated.")
        else:
            print("ROLE      none inferred — handle it directly")
            print("          No signal matched. That usually means it is a question or a")
            print("          one-step change, and §6 says do it yourself.")
    else:
        print(f"ROLE      {role}   ({', '.join(hits[0][1])})")
        if len(hits) > 1:
            print(f"          also matched: {', '.join(h[0] for h in hits[1:])}"
                  f" — override with --role if the first is wrong")
        print(f"MODEL     {MODEL[role]}")

    if flags:
        print(f"RISK      HIGH signals: {', '.join(flags)}")
        print("          §3: checkpoint, state what is irreversible, and get")
        print("          confirmation BEFORE executing. Not after.")

    if args.level:
        b = BUDGET[args.level]
        print(f"BUDGET    level {args.level} -> " +
              ("only what is justified" if b is None else f"{b} subagent(s)"))
        if b == 0:
            print("          Do it directly. A subagent here costs more than it returns.")
    else:
        print("LEVEL     unset — classify before routing (§3). Pass --level for the budget.")

    if skills:
        print(f"SKILLS    {', '.join(s['name'] for s in skills)}"
              f"   (~{sum(s['words'] for s in skills)} words)")
    else:
        print("SKILLS    none matched — proceed without one, or say so if the work")
        print("          is clearly specialized. That is a trigger gap, not licence.")


if __name__ == "__main__":
    main()
