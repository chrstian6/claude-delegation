#!/usr/bin/env python3
"""The queue, mechanically. Implements the master prompt's §11-16.

TASKS.md is the source of truth for what is queued, running, blocked and done —
it survives context compaction, which a context window does not. Left as prose,
"every actionable request becomes a row" is an instruction that gets skipped
exactly when the session is busiest, which is when the queue matters most.

    tasks.py add "add authentication" --level 3 --risk med
    tasks.py add "then write the auth tests"      # dependency inferred
    tasks.py state 002 running
    tasks.py ready        # what may start now, and what may run in parallel
    tasks.py show         # the non-done view, per §59
    tasks.py check        # cycles, unknown deps, illegal states

What this enforces that prose could not: the state machine (§12), so a task
cannot jump from QUEUED to COMPLETED without passing through verification;
dependency readiness (§14-15); and failure isolation (§16), where a failed task
blocks only its dependents.
"""
import argparse
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()  # the project, not this package
TASKS = ROOT / ".claude" / "TASKS.md"

# §12. The linear spine, then the off-ramps.
SPINE = ["QUEUED", "CLASSIFYING", "PLANNED", "READY", "RUNNING", "SELF_EVALUATING",
         "TESTING", "REPAIRING", "REVIEWING", "FINAL_VALIDATION", "COMPLETED"]
OFF_RAMP = ["WAITING_DEPENDENCY", "WAITING_APPROVAL", "BLOCKED", "PAUSED",
            "FAILED", "PARTIAL", "ESCALATED", "CANCELLED"]
STATES = SPINE + OFF_RAMP
TERMINAL = {"COMPLETED", "CANCELLED"}

# §14. The user's own words become dependencies.
DEP_CUES = ("then ", "after that", "once this", "once that", "using what you",
            "using the previous", "fix what", "test that", "review that",
            "continue from", "and then")

LEVELS = ["1", "2", "3", "4", "5"]
RISKS = ["low", "med", "high"]


def allowed(cur, nxt):
    """A transition is legal if it advances the spine, or steps off it and back.

    Deliberately permissive about *where* on the spine you re-enter — a repair
    can send a task back to TESTING — but never lets a task reach COMPLETED
    without passing through FINAL_VALIDATION. That is the one edge worth
    enforcing: it is the difference between done and reported-done.
    """
    if nxt not in STATES:
        return False, f"'{nxt}' is not a state in §12"
    if cur == nxt:
        return True, ""
    if nxt == "COMPLETED" and cur not in ("FINAL_VALIDATION", "REVIEWING"):
        return False, ("COMPLETED only from FINAL_VALIDATION or REVIEWING — "
                       "a task cannot skip verification to reach done")
    if cur in TERMINAL and nxt not in ("QUEUED",):
        return False, f"{cur} is terminal; re-open as QUEUED if the work returns"
    return True, ""


def parse():
    """Split TASKS.md into head / rows / tail.

    Phase-tracked rather than inferred from whether rows exist yet: the first
    version put everything after an EMPTY table into `head`, so the first added
    row was written below the "## Rules" section and the next parse could not
    see it. Every subsequent add then re-issued id 001.
    """
    rows, head, tail = [], [], []
    phase = "before"
    if not TASKS.is_file():
        # The skeleton MUST carry the header and separator: parse() only enters
        # the table phase after the separator row, so a bare "# Tasks" heading
        # would make every later parse see zero rows and re-issue id 001.
        return rows, ["# Tasks\n", "\n",
                      "| id | task | level | risk | deps | state | notes |\n",
                      "|---|---|---|---|---|---|---|\n"], []
    for ln in TASKS.read_text().splitlines(keepends=True):
        if phase == "before":
            head.append(ln)
            if re.match(r"^\|[\s\-:|]+\|$", ln):
                phase = "table"                # the separator row ends the header
            continue
        if phase == "table":
            if ln.startswith("|"):
                c = [x.strip() for x in ln.strip().strip("|").split("|")]
                if len(c) >= 7:
                    rows.append(dict(id=c[0], task=c[1], level=c[2], risk=c[3],
                                     deps=[d for d in re.split(r"[,\s]+", c[4]) if d
                                           and d not in ("—", "-")],
                                     state=c[5].upper(), notes=c[6]))
                continue
            phase = "after"
        tail.append(ln)
    return rows, head, tail


def write(rows, head, tail):
    body = "".join(head)
    for r in rows:
        deps = ",".join(r["deps"]) if r["deps"] else "—"
        body += (f"| {r['id']} | {r['task']} | {r['level']} | {r['risk']} | "
                 f"{deps} | {r['state'].lower()} | {r['notes']} |\n")
    TASKS.write_text(body + "".join(tail))


def by_id(rows, tid):
    for r in rows:
        if r["id"] == tid:
            return r
    return None


def blocked_by(rows, r):
    """Unmet dependencies. §16: a FAILED dep blocks, it does not cascade-fail."""
    out = []
    for d in r["deps"]:
        dep = by_id(rows, d)
        if dep is None:
            out.append((d, "unknown"))
        elif dep["state"] != "COMPLETED":
            out.append((d, dep["state"].lower()))
    return out


def cmd_add(args):
    rows, head, tail = parse()
    nid = f"{max([int(r['id']) for r in rows] + [0]) + 1:03d}"
    deps = list(args.deps or [])
    text = args.request
    if not deps and rows and any(c in text.lower() for c in DEP_CUES):
        prev = rows[-1]["id"]
        deps = [prev]
        print(f"dependency inferred from the wording -> depends on {prev}")
        print("  say --deps to override; an inferred dependency is a guess, not a fact")
    state = "WAITING_DEPENDENCY" if deps else "QUEUED"
    rows.append(dict(id=nid, task=text, level=args.level or "?", risk=args.risk or "?",
                     deps=deps, state=state, notes=args.note or "—"))
    write(rows, head, tail)
    print(f"{nid}  {state.lower():18} {text}")
    if not args.level:
        print("  level unset: classify it before routing (§5)")


def cmd_state(args):
    rows, head, tail = parse()
    r = by_id(rows, args.id)
    if not r:
        sys.exit(f"no such task: {args.id}")
    nxt = args.state.upper()
    ok, why = allowed(r["state"], nxt)
    if not ok:
        sys.exit(f"refused: {r['id']} {r['state']} -> {nxt}\n  {why}")
    if nxt in ("RUNNING", "READY"):
        unmet = blocked_by(rows, r)
        if unmet:
            sys.exit("refused: dependencies unmet -> " +
                     ", ".join(f"{d}({s})" for d, s in unmet))
    r["state"] = nxt
    write(rows, head, tail)
    print(f"{r['id']}  -> {nxt.lower()}")
    freed = [x["id"] for x in rows
             if x["state"] == "WAITING_DEPENDENCY" and not blocked_by(rows, x)]
    if nxt == "COMPLETED" and freed:
        print("now ready: " + ", ".join(freed))


def cmd_ready(args):
    rows, _, _ = parse()
    ready = [r for r in rows
             if r["state"] in ("QUEUED", "READY", "WAITING_DEPENDENCY")
             and not blocked_by(rows, r)]
    if not ready:
        print("nothing ready")
        return
    print("READY:")
    for r in ready:
        print(f"  {r['id']}  L{r['level']}/{r['risk']:<4} {r['task'][:60]}")
    if len(ready) > 1:
        print("\n§15: run these in parallel ONLY if they touch different files and")
        print("neither mutates shared state. Same files, DB, migrations or deploy")
        print("run one at a time.")


def cmd_show(args):
    rows, _, _ = parse()
    live = [r for r in rows if r["state"] not in TERMINAL]
    if not live:
        print("queue empty")
        return
    for r in live:
        dep = ""
        unmet = blocked_by(rows, r)
        if unmet:
            dep = "  <- " + ",".join(f"{d}({s})" for d, s in unmet)
        print(f"{r['id']}  {r['state'].lower():18} L{r['level']}/{r['risk']:<4} "
              f"{r['task'][:58]}{dep}")


def cmd_check(args):
    rows, _, _ = parse()
    bad = 0
    ids = {r["id"] for r in rows}
    for r in rows:
        if r["state"] not in STATES:
            print(f"FAIL {r['id']}: '{r['state'].lower()}' is not a §12 state"); bad += 1
        if r["level"] not in LEVELS + ["?"]:
            print(f"FAIL {r['id']}: level '{r['level']}' is not 1-5"); bad += 1
        if r["risk"] not in RISKS + ["?"]:
            print(f"FAIL {r['id']}: risk '{r['risk']}' is not low/med/high"); bad += 1
        for d in r["deps"]:
            if d not in ids:
                print(f"FAIL {r['id']}: depends on unknown task {d}"); bad += 1
        if r["state"] == "COMPLETED" and blocked_by(rows, r):
            print(f"FAIL {r['id']}: COMPLETED with unmet dependencies"); bad += 1

    # Cycles: a queue that cannot drain is worse than one that is merely wrong.
    seen, stack = set(), set()

    def walk(node, path):
        nonlocal bad
        if node in stack:
            print(f"FAIL cycle: {' -> '.join(path + [node])}"); bad += 1
            return
        if node in seen:
            return
        seen.add(node); stack.add(node)
        r = by_id(rows, node)
        for d in (r["deps"] if r else []):
            if d in ids:
                walk(d, path + [node])
        stack.discard(node)

    for r in rows:
        walk(r["id"], [])

    print(f"\n{len(rows)} task(s), {bad} problem(s)")
    sys.exit(1 if bad else 0)


def main():
    ap = argparse.ArgumentParser(description="TASKS.md queue, per the master prompt §11-16")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add"); a.add_argument("request")
    a.add_argument("--level", choices=LEVELS); a.add_argument("--risk", choices=RISKS)
    a.add_argument("--deps", nargs="*"); a.add_argument("--note")
    a.set_defaults(fn=cmd_add)
    s = sub.add_parser("state"); s.add_argument("id"); s.add_argument("state")
    s.set_defaults(fn=cmd_state)
    for name, fn in (("ready", cmd_ready), ("show", cmd_show), ("check", cmd_check)):
        sub.add_parser(name).set_defaults(fn=fn)
    args = ap.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
