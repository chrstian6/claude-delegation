#!/usr/bin/env python3
"""Analyze accumulated outcomes and propose policy changes.

This is the learning loop. It runs offline, against real logged evidence, and it
*proposes* — it never edits POLICY.md. A human applies the change as a commit,
which is what makes it versioned and revertible.

The threshold matters: a pattern needs MIN_EVIDENCE independent observations
before it is proposed at all. One bad task is noise, and promoting noise into a
permanent rule is how these systems accumulate superstition.

Usage:
  python scripts/review_outcomes.py
  python scripts/review_outcomes.py --min-evidence 5 --since 2026-01-01
"""

import argparse
import collections
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()  # the project, not this package
LOG = ROOT / ".claude" / "state" / "outcomes.jsonl"

MIN_EVIDENCE = 3          # observations before a pattern is proposable
FAIL_RATE_TRIGGER = 0.34  # a bucket failing more than a third of the time
LOW_VALUE_TRIGGER = 0.9   # delegation that never beats direct


def load(since=None):
    if not LOG.exists():
        return []
    rows = []
    for line in LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if since and r.get("ts", "") < since:
            continue
        rows.append(r)
    return rows


def rate(rows, pred):
    if not rows:
        return 0.0
    return sum(1 for r in rows if pred(r)) / len(rows)


def analyze(rows, min_evidence):
    findings = []
    ok = lambda r: r["result"] == "pass"

    # 1. Difficulty x route buckets that fail disproportionately.
    buckets = collections.defaultdict(list)
    for r in rows:
        buckets[(r["level"], r["route"])].append(r)
    for (level, route), rs in sorted(buckets.items()):
        if len(rs) < min_evidence:
            continue
        fr = 1 - rate(rs, ok)
        if fr > FAIL_RATE_TRIGGER:
            findings.append({
                "kind": "routing",
                "evidence": len(rs),
                "observation": f"level {level} via '{route}' fails {fr:.0%} of the time",
                "proposal": f"WHEN level={level} THEN prefer a different route than '{route}'",
                "caution": "check the notes first — this may be one recurring project issue, "
                           "not a routing problem",
            })

    # 2. Misclassification: levels that keep getting revised upward.
    # The lower bands, where under-classification actually happens. 1-5 per the
    # master prompt; this read ("S", "M") and silently matched nothing.
    for level in ("1", "2", "3"):
        rs = [r for r in rows if r["level"] == level]
        if len(rs) < min_evidence:
            continue
        rc = rate(rs, lambda r: r.get("reclassified"))
        if rc > 0.4:
            findings.append({
                "kind": "classification",
                "evidence": len(rs),
                "observation": f"{rc:.0%} of level-{level} tasks were reclassified upward",
                "proposal": f"tighten the level-{level} entry criteria in ORCHESTRATOR.md",
                "caution": "under-classifying wastes a cycle; over-classifying wastes tokens "
                           "on every task",
            })

    # 3. Delegation that does not earn its cost.
    direct = [r for r in rows if r["route"] == "direct"]
    deleg = [r for r in rows if r["route"] in ("specialist", "parallel")]
    if len(direct) >= min_evidence and len(deleg) >= min_evidence:
        d_ok, g_ok = rate(direct, ok), rate(deleg, ok)
        if g_ok <= d_ok * LOW_VALUE_TRIGGER:
            findings.append({
                "kind": "delegation",
                "evidence": len(deleg),
                "observation": f"delegated pass rate {g_ok:.0%} vs direct {d_ok:.0%}",
                "proposal": "raise the delegation bar — require parallelism or independent "
                            "verification, not just difficulty",
                "caution": "delegated tasks may simply be harder; compare within the same level "
                           "before acting",
            })

    # 4. Escalation that does not help.
    esc = [r for r in rows if r.get("escalated")]
    if len(esc) >= min_evidence:
        e_ok = rate(esc, ok)
        if e_ok < 0.5:
            findings.append({
                "kind": "escalation",
                "evidence": len(esc),
                "observation": f"escalated tasks still pass only {e_ok:.0%} of the time",
                "proposal": "escalation is not the right lever here — the failures are likely "
                            "missing context, not missing reasoning capacity",
                "caution": "a stronger model cannot supply facts it was never given",
            })

    # 5. Verification gaps — the quiet one that matters most.
    if len(rows) >= min_evidence:
        unver = rate(rows, lambda r: r.get("verified") == "none")
        if unver > 0.3:
            findings.append({
                "kind": "verification",
                "evidence": len(rows),
                "observation": f"{unver:.0%} of tasks completed with no verification at all",
                "proposal": "establish a runnable test command in POLICY.md, or make the "
                            "unverified state explicit in every handoff",
                "caution": "this is the failure mode that produces confident wrong results",
            })

    # 6. Skills that never appear in passing work.
    skill_rows = collections.defaultdict(list)
    for r in rows:
        for s in r.get("skills", []):
            skill_rows[s].append(r)
    for skill, rs in sorted(skill_rows.items()):
        if len(rs) < min_evidence:
            continue
        s_ok = rate(rs, ok)
        if s_ok < 0.5:
            findings.append({
                "kind": "skill",
                "evidence": len(rs),
                "observation": f"'{skill}' loaded in {len(rs)} tasks, {s_ok:.0%} passed",
                "proposal": f"review skills/{skill}/SKILL.md — it may be triggering on the "
                            f"wrong tasks or missing guidance",
                "caution": "correlation only; the skill may be loaded precisely on hard tasks",
            })

    return findings


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--min-evidence", type=int, default=MIN_EVIDENCE)
    p.add_argument("--since", default=None, help="ISO date lower bound")
    a = p.parse_args()

    rows = load(a.since)
    if not rows:
        print("No outcomes logged yet. Nothing to learn from — that is the correct state\n"
              "for a new system, not a problem to fix.")
        return 0

    passed = sum(1 for r in rows if r["result"] == "pass")
    repairs = sum(r.get("repairs", 0) for r in rows)

    print(f"\n{len(rows)} outcomes  |  {passed}/{len(rows)} passed  |  "
          f"{repairs} repair attempts  |  threshold: {a.min_evidence} observations\n")

    findings = analyze(rows, a.min_evidence)
    if not findings:
        print("No pattern met the evidence threshold.\n"
              "This is a normal and healthy result. Do not lower the threshold to\n"
              "manufacture a finding — a rule built on two data points is superstition\n"
              "that will outlive the situation that produced it.")
        return 0

    print(f"{len(findings)} proposal(s). None applied. Review, then edit POLICY.md as a commit.\n")
    for i, f in enumerate(findings, 1):
        print(f"[{i}] {f['kind'].upper()}  (evidence: {f['evidence']})")
        print(f"    observed:  {f['observation']}")
        print(f"    proposal:  {f['proposal']}")
        print(f"    caution:   {f['caution']}\n")

    print("Before applying any of these, read the `note` fields of the underlying records.\n"
          "A statistical pattern with no mechanism behind it is a coincidence.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
