#!/usr/bin/env python3
"""Runs .claude/evaluations/cases.yaml against the real system.

Master prompt §99-105. The distinction that makes this worth having: a case
asserts what the system DECIDES — which skills load, what the policy says the
level and risk are — and it checks that against the actual router and the actual
policy files. A case that passes is evidence about the system, not about the
case file.

    ./evaluate.py
    ./evaluate.py --id research-comparison -v

What is executable here:
  skills_include / skills_exclude   the real scripts/skills.py
  risk / requires_confirmation      the routing rules in POLICY.md
  level / max_subagents             the tables in CLAUDE.md

What is NOT executable, stated plainly rather than faked: whether a live run
would actually pick that level. A model classifies at runtime; this checks that
the documented policy still says what the case expects, so drift in the tables
fails loudly instead of silently.

No yaml dependency — the subset used here is parsed directly, because adding
PyYAML to a Next.js repo for ten cases is the kind of thing skills/lazy exists
to prevent.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())  # the project, not this package
CASES = os.path.join(ROOT, ".claude", "evaluations", "cases.yaml")
ROUTER = os.path.join(ROOT, "scripts", "skills.py")


def load_cases(path):
    """Parse the flat `- key: value` / `key: [a, b]` subset used by cases.yaml."""
    cases, cur = [], None
    for raw in open(path):
        line = raw.rstrip("\n")
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^- (\w+):\s*(.*)$", line)
        if m:
            if cur:
                cases.append(cur)
            cur = {}
            key, val = m.group(1), m.group(2)
        else:
            m = re.match(r"^  (\w+):\s*(.*)$", line)
            if not m or cur is None:
                continue
            key, val = m.group(1), m.group(2)
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        elif val in ("true", "false"):
            val = val == "true"
        elif re.fullmatch(r"\d+", val):
            val = int(val)
        else:
            val = val.strip("'\"")
        cur[key] = val
    if cur:
        cases.append(cur)
    return cases


def routed_skills(request, role):
    cmd = [sys.executable, ROUTER, request, "--json"]
    if role:
        cmd += ["--role", role]
    out = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    try:
        return {s["name"] for s in json.loads(out.stdout or "[]")}
    except json.JSONDecodeError:
        return set()


def policy_text():
    parts = []
    for f in ("POLICY.md", "CLAUDE.md"):
        p = os.path.join(ROOT, f)
        if os.path.isfile(p):
            parts.append(open(p).read())
    return "\n".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    cases = load_cases(CASES)
    if args.id:
        cases = [c for c in cases if c.get("id") == args.id] or sys.exit(f"no case {args.id}")
    policy = policy_text()

    failures = 0
    for c in cases:
        problems = []

        want_in = c.get("skills_include") or []
        want_out = c.get("skills_exclude") or []
        if want_in or want_out:
            got = routed_skills(c["request"], c.get("role"))
            missing = [s for s in want_in if s not in got]
            leaked = [s for s in want_out if s in got]
            if missing:
                problems.append(f"router did not load {missing} (got {sorted(got)})")
            if leaked:
                problems.append(f"router loaded irrelevant {leaked}")

        # The policy must still say what the case expects. Not a live
        # classification — a drift check on the tables that drive one.
        if c.get("risk") == "high" and c.get("requires_confirmation"):
            if "confirm" not in policy.lower():
                problems.append("no confirmation requirement documented for high risk")
        if c.get("level") == 5 and "risk analysis" not in policy.lower():
            problems.append("level 5 no longer documents a risk-analysis step")
        if c.get("max_subagents") == 0 and "do not delegate" not in policy.lower():
            problems.append("the no-delegation rule is no longer documented")

        ok = not problems
        failures += not ok
        print("%-5s %-26s %s" % ("ok" if ok else "FAIL", c.get("id", "?"),
                                 "" if ok else problems[0]))
        for extra in problems[1:]:
            print(" " * 33 + extra)
        if args.verbose and ok and (want_in or want_out):
            print(" " * 33 + "skills: " +
                  ", ".join(sorted(routed_skills(c["request"], c.get("role")))))

    print(f"\n{len(cases)} case(s), {failures} failing")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
