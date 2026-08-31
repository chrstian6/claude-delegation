#!/usr/bin/env python3
"""Append one task outcome to state/outcomes.jsonl.

This is the entire persistence surface for the learning loop. It is deliberately
append-only: nothing here mutates policy. Policy changes go through
review_outcomes.py, a human, and a git commit.

Usage:
  python scripts/log_outcome.py --task 042 --level M --risk low \\
      --route specialist --model claude-sonnet-5 --repairs 1 \\
      --result pass --note "tailwind v4 syntax broke the first attempt"
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()  # the project, not this package
LOG = ROOT / ".claude" / "state" / "outcomes.jsonl"


def git_sha() -> str:
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT, capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except Exception:
        return ""


def main() -> int:
    p = argparse.ArgumentParser(description="Append a task outcome record.")
    p.add_argument("--task", required=True, help="Task id from TASKS.md")
    # 1-5, not S/M/L: the master prompt classifies on five levels and CLAUDE.md
    # instructs `--level 1-5`. The script shipped accepting only S/M/L, so every
    # task-close raised argparse error 2 and the learning loop recorded nothing.
    p.add_argument("--level", required=True, choices=["1", "2", "3", "4", "5"])
    p.add_argument("--risk", required=True, choices=["low", "med", "high"])
    p.add_argument("--route", required=True,
                   choices=["direct", "script", "skill", "specialist", "parallel"])
    p.add_argument("--model", required=True, help="Model id that did the main work")
    p.add_argument("--result", required=True, choices=["pass", "partial", "fail"])
    p.add_argument("--repairs", type=int, default=0, help="Repair attempts used")
    p.add_argument("--escalated", action="store_true", help="Model tier was escalated")
    p.add_argument("--reclassified", action="store_true", help="Difficulty was revised")
    p.add_argument("--skills", default="", help="Comma-separated skills loaded")
    p.add_argument("--tokens", type=int, default=0, help="Approx total tokens, if known")
    p.add_argument("--verified", default="none",
                   choices=["tests", "manual", "review", "none"],
                   help="How the result was actually verified")
    p.add_argument("--note", default="", help="One sentence: what actually mattered")

    a = p.parse_args()

    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "task": a.task,
        "level": a.level,
        "risk": a.risk,
        "route": a.route,
        "model": a.model,
        "skills": [s.strip() for s in a.skills.split(",") if s.strip()],
        "repairs": a.repairs,
        "escalated": a.escalated,
        "reclassified": a.reclassified,
        "verified": a.verified,
        "tokens": a.tokens,
        "result": a.result,
        "note": a.note.strip(),
        "policy_sha": git_sha(),
    }

    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"logged {a.task}: {a.result} ({a.level}/{a.risk}, {a.route}, {a.repairs} repairs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
