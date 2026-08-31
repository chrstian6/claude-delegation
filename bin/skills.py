#!/usr/bin/env python3
"""Skill router. Answers "which skills does THIS task need" from skill frontmatter.

The rule this enforces is CLAUDE.md §5: do not stuff every skill into every agent.
A skill loaded for a task that did not need it is context every later step pays
for, and the design library is the expensive case — 12k words that has no
business being present while renaming a variable.

    skills.py "add a draggable widget to the dashboard" --role builder
    skills.py "compare postgres and dynamo" --role researcher
    skills.py "why does the auth test fail" --json

Scoring is deliberately dumb and inspectable: explicit `triggers:` dominate,
`agent:` narrows, description overlap breaks ties. A model can read the output
and disagree with it; that is better than an opaque ranking it cannot audit.

Frontmatter this reads (all optional except name):

    name: skill-name
    description: >
      what it does and when to use it
    agent: builder | researcher | architect | tester | reviewer | repairer | orchestrator | any
    priority: low | normal | high | critical
    triggers:
      - dashboard
      - drag
"""
import argparse
import json
import os
import pathlib
import re
import sys
from typing import Dict, List, Optional, Set, Tuple

# Skill sources, in precedence order. The packaged library ships with this tool;
# a project's own .claude/skills/ is merged on top, so a project can add or
# override a skill without forking the package.
ROOT = pathlib.Path(__file__).resolve().parent.parent
PROJECT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()


def _skill_dirs():
    seen, out = set(), []
    for cand in (
        os.environ.get("DELEGATION_SKILLS"),
        os.environ.get("CLAUDE_PLUGIN_ROOT", "") and
        os.path.join(os.environ["CLAUDE_PLUGIN_ROOT"], "skills"),
        ROOT / "skills",
        PROJECT / ".claude" / "skills",
    ):
        if not cand:
            continue
        d = pathlib.Path(cand)
        if d.is_dir() and str(d) not in seen:
            seen.add(str(d))
            out.append(d)
    return out

# CLAUDE.md §5. A conflict is resolved by the higher band, never by merging two
# skills that contradict each other.
PRIORITY_RANK = {"critical": 3, "high": 2, "normal": 1, "low": 0}

# Returning everything is the failure this script exists to prevent.
DEFAULT_LIMIT = 6

# Skills a role ALWAYS loads, trigger or not. These are postures rather than
# techniques: they apply to every piece of that role's work, so making them
# depend on wording would mean the one task phrased unusually is the one that
# goes without them.
#
#   lazy         stop over-building. The ladder applies to every implementation,
#                and "make the sidebar collapsible" needs it as much as
#                "refactor the sidebar" does.
#   design-taste every visual decision is made rather than defaulted. Owner
#                ruling 2026-08-30.
#
# Before this, both arrived only when a trigger happened to match, and on a task
# with no strong trigger they arrived via the weak-score fallback — present by
# luck, not by rule.
MANDATORY = {
    "builder": ["lazy", "design-taste"],
}


STOPWORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "is",
    "it", "this", "that", "be", "are", "was", "into", "from", "at", "by", "as",
    "we", "i", "my", "our", "then",
    # "add", "make", "build", "use" are NOT stopwords: they are the verbs that
    # signal implementation work, and dropping them made `lazy` — priority
    # critical, the default posture for building — silently fail to fire.
}


def parse_frontmatter(path):
    # No PEP 604 unions: system python here is 3.9, same as the hooks.
    text = path.read_text(errors="replace")
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block, body = text[3:end], text[end + 4:]

    meta = {"triggers": [], "body_words": len(body.split())}
    key = None
    for raw in block.splitlines():
        if not raw.strip():
            continue
        item = re.match(r"\s+-\s+(.*)$", raw)
        if item and key == "triggers":
            meta["triggers"].append(item.group(1).strip().strip("\"'").lower())
            continue
        m = re.match(r"([A-Za-z_]+):\s*(.*)$", raw)
        if not m:
            if key and key in ("description",):        # folded block scalar
                meta[key] = (meta.get(key, "") + " " + raw.strip()).strip()
            continue
        key, value = m.group(1).lower(), m.group(2).strip()
        if value in (">", "|", ">-", "|-"):
            meta[key] = ""
        elif key != "triggers":
            meta[key] = value.strip("\"'")
    return meta


def load_all():
    # A later source wins on name collision, so a project-local skill overrides
    # the packaged one of the same name rather than appearing twice.
    by_name = {}
    for base in _skill_dirs():
        for d in sorted(base.iterdir()):
            f = d / "SKILL.md"
            if not f.is_file():
                continue
            meta = parse_frontmatter(f)
            if not meta:
                continue
            meta.setdefault("name", d.name)
            meta["path"] = str(f)
            by_name[meta["name"]] = meta
    return list(by_name.values())


def tokens(text):
    return {w for w in re.findall(r"[a-z0-9]+", text.lower())
            if len(w) > 2 and w not in STOPWORDS}


def score(skill, task, role):
    task_l = task.lower()
    task_t = tokens(task)
    pts, why = 0, []

    # One task WORD may satisfy at most one trigger. Prefix matching means the
    # token "auth" satisfies both an "auth" trigger and an "authorization" one,
    # and counting both scored +20 from a single word — enough for a reviewer
    # skill to beat the wrong-role penalty and land in a builder dispatch.
    spent = set()
    for trig in skill.get("triggers", []):
        if " " in trig:
            if trig in task_l and trig not in spent:
                spent.add(trig)
                pts += 10
                why.append(f"trigger:{trig}")
            continue
        matched = next((t for t in task_t
                        if t not in spent and (t.startswith(trig) or trig.startswith(t))), None)
        if matched:
            spent.add(matched)
            pts += 10
            why.append(f"trigger:{trig}")

    agent = (skill.get("agent") or "any").lower()
    if role:
        if agent == role:
            pts += 4
            why.append(f"role:{role}")
        elif agent != "any":
            # Orchestrator skills are NOT exempt: when a worker role is named,
            # queue-management and task-classification are somebody else's job.
            # Exempting them let "status" pull the orchestrator library into a
            # builder task about a status filter.
            pts -= 12
            why.append(f"other-role:{agent}")

    overlap = task_t & tokens(skill.get("description", ""))
    if overlap:
        pts += min(len(overlap), 4)
        why.append("desc:" + ",".join(sorted(overlap)[:4]))

    pts += PRIORITY_RANK.get((skill.get("priority") or "normal").lower(), 1)
    return pts, why


def main():
    ap = argparse.ArgumentParser(description="Which skills does this task need?")
    ap.add_argument("task", help="the task description, in the user's own words")
    ap.add_argument("--role", help="researcher|architect|builder|tester|reviewer|repairer")
    ap.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    ap.add_argument("--all", action="store_true", help="list every skill and its score")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    skills = load_all()
    if not skills:
        print("No skills found under .claude/skills/", file=sys.stderr)
        sys.exit(1)

    ranked = []
    for s in skills:
        pts, why = score(s, args.task, args.role)
        ranked.append((pts, s, why))
    ranked.sort(key=lambda r: (-r[0], r[1]["name"]))

    # A trigger hit is a real signal; priority alone is not. Without this floor
    # every task returns the same six highest-priority skills.
    # Weak-score fallback tightened from 6 to 9: at 6 a task with no real
    # trigger collected four role-and-priority matches and returned a plausible
    # bundle, which reads like a decision and is not one.
    hits = [r for r in ranked if r[0] >= 10] or [r for r in ranked if r[0] >= 9]
    chosen = (ranked if args.all else hits)[: (len(ranked) if args.all else args.limit)]

    if not args.all and args.role:
        by_name = {s["name"]: (p, s, w) for p, s, w in ranked}
        for name in reversed(MANDATORY.get(args.role, [])):
            if name in by_name and not any(s["name"] == name for _, s, _ in chosen):
                p_, s_, w_ = by_name[name]
                chosen.insert(0, (p_, s_, w_ + [f"MANDATORY:{args.role}"]))
            elif name in by_name:
                chosen = [(p_, s_, (w_ + [f"MANDATORY:{args.role}"]) if s_["name"] == name else w_)
                          for p_, s_, w_ in chosen]

    if args.json:
        print(json.dumps([{"name": s["name"], "score": p, "why": w, "path": s["path"],
                           "priority": s.get("priority", "normal"),
                           "words": s["body_words"]} for p, s, w in chosen], indent=2))
        return

    if not chosen:
        print("No skill matched this task.")
        print("Proceed without one, or say so if the work is clearly specialized —")
        print("that is a gap in the triggers, not permission to improvise.")
        return

    budget = sum(s["body_words"] for _, s, _ in chosen)
    print(f"{len(chosen)} skill(s), ~{budget} words of context:\n")
    for pts, s, why in chosen:
        pr = s.get("priority", "normal")
        print(f"  {s['name']:<28} {pts:>3}  [{pr}]  {s['body_words']:>5}w  {s['path']}")
        print(f"  {'':<28}      {' '.join(why)}")
    print("\nLoad these and nothing else.")


if __name__ == "__main__":
    main()
