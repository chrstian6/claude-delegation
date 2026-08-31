#!/usr/bin/env python3
"""System metrics from state/outcomes.jsonl. Master prompt §90.

Reports only what was actually logged. Every number here traces to a row that a
task-close wrote; nothing is estimated, and a metric with no data says so rather
than showing a confident zero.

    ./metrics.py
    ./metrics.py --since 2026-08-01
"""
import argparse, collections, json, os, sys

ROOT = os.path.abspath(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())  # the project, not this package
LOG = os.path.join(ROOT, ".claude", "state", "outcomes.jsonl")


def pct(n, d):
    return "n/a" if not d else f"{n / d:.0%}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="ISO date, inclusive")
    args = ap.parse_args()

    if not os.path.exists(LOG) or os.path.getsize(LOG) == 0:
        print("No outcomes logged yet.")
        print("Metrics are computed from real task closes, not estimated —")
        print("so there is nothing to report until tasks start closing.")
        return
    rows = [json.loads(l) for l in open(LOG) if l.strip()]
    if args.since:
        rows = [r for r in rows if r.get("ts", "") >= args.since]
    n = len(rows)
    if not n:
        print("No outcomes in that window."); return

    passed = sum(r["result"] == "pass" for r in rows)
    repairs = sum(r.get("repairs", 0) for r in rows)
    repaired = sum(1 for r in rows if r.get("repairs", 0) > 0)
    delegated = sum(1 for r in rows if r.get("route") in ("specialist", "parallel"))
    escalated = sum(1 for r in rows if r.get("escalated"))
    reclassified = sum(1 for r in rows if r.get("reclassified"))
    unverified = sum(1 for r in rows if r.get("verified", "none") == "none")

    print(f"{n} outcome(s)\n")
    print(f"  task success rate       {pct(passed, n)}   ({passed}/{n})")
    print(f"  repair rate             {pct(repaired, n)}   {repairs} attempts total")
    print(f"  delegation rate         {pct(delegated, n)}")
    print(f"  model escalation rate   {pct(escalated, n)}")
    print(f"  reclassification rate   {pct(reclassified, n)}")
    print(f"  UNVERIFIED rate         {pct(unverified, n)}   <- watch this one")

    if unverified and unverified / n > 0.3:
        print("\n  More than a third of tasks closed unverified. That usually means")
        print("  the inner-loop test command is too slow to run, not that people")
        print("  stopped caring. Narrow the command before lowering the bar.")

    def group(key, label):
        b = collections.defaultdict(lambda: [0, 0])
        for r in rows:
            k = r.get(key) or "?"
            b[k][0] += 1
            b[k][1] += r["result"] == "pass"
        if b:
            print(f"\n  by {label}:")
            for k, (tot, ok) in sorted(b.items()):
                print(f"    {str(k):<24} {tot:>3} task(s)  {pct(ok, tot)} pass")

    group("level", "difficulty")
    group("risk", "risk")
    group("model", "model")
    group("route", "route")

    skills = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        for s in r.get("skills", []):
            skills[s][0] += 1
            skills[s][1] += r["result"] == "pass"
    if skills:
        print("\n  skill activation (§41):")
        for s, (tot, ok) in sorted(skills.items(), key=lambda x: -x[1][0]):
            print(f"    {s:<24} {tot:>3} activation(s)  {pct(ok, tot)} pass")


if __name__ == "__main__":
    main()
