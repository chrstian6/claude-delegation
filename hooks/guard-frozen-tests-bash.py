#!/usr/bin/env python3
"""PreToolUse hook on Bash. Closes the matcher gap in guard-frozen-tests.sh.

That hook runs on Edit|Write|MultiEdit|NotebookEdit, so it never sees a shell
edit. Its own header says so:

    KNOWN GAP: this hook only sees the tools in its matcher. A shell edit
    (sed -i, >, git checkout --) via Bash bypasses it entirely. Cover that in
    your Bash guard, or accept that the freeze is enforced for agent edits and
    detected after the fact, by verify.sh run, for shell edits.

This is that Bash guard. Detected-after-the-fact is not good enough for the one
move the freeze exists to stop, and the gap is not theoretical: `sed -i ''` was
used on a frozen test in this repo on 2026-08-30 while the Edit-side hook was
installed and armed. It did not fire, because it never ran.

Conservative by construction: a frozen path must appear in the command AND the
command must contain a mutating construct. Reading a frozen test (cat, grep,
diff, git show) stays allowed — implementers legitimately need to read the
definition of success they are building against.

Exit 0 = allow. Exit 2 = block, stderr returns to Claude as the reason.
"""
import json
import os
import re
import shlex
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOCK = os.path.join(ROOT, ".claude", "state", "test-lock.txt")

# Constructs that can modify a file named on the same command line.
MUTATORS = (
    # Flags bundle: `perl -pi -e` and `sed -Ei` carry the in-place flag inside a
    # cluster, so a pattern demanding a bare ` -i` misses both. The matrix caught
    # perl; sed -Ei was the same hole one character away.
    r"\bsed\b[^|;]*\s-[A-Za-z]*i\b",
    r"\bperl\b[^|;]*\s-[A-Za-z]*i\b",
    r"\bawk\b[^|;]*>",               # awk ... > file
    r">>?",                          # any redirect, incl. truncation
    r"\btee\b",
    r"\bgit\s+checkout\s+--",        # discard working-tree changes
    r"\bgit\s+restore\b",
    r"\bgit\s+stash\b",
    r"\bmv\b", r"\bcp\b", r"\brm\b",
    r"\btruncate\b", r"\bpatch\b", r"\bapply\b",
    r"\bdd\b",
    r">\s*\|",                       # clobber redirect
)
MUTATOR_RE = re.compile("|".join(MUTATORS))


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def frozen_paths():
    out = []
    try:
        with open(LOCK) as fh:
            for line in fh:
                parts = line.split(None, 1)
                if len(parts) == 2:
                    out.append(parts[1].strip())
    except OSError:
        return []
    return out


def main() -> None:
    # No active freeze: nothing to protect. The only fail-open path, and correct
    # — there is nothing to compare against.
    if not os.path.isfile(LOCK):
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        # A freeze IS active and the request cannot be read. Fail closed: a
        # guard that cannot understand the call cannot know whether to allow it.
        block("BLOCKED: hook payload is not parseable JSON while a test freeze "
              "is active. Failing closed.")

    if not isinstance(payload, dict) or payload.get("tool_name") != "Bash":
        sys.exit(0)
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command:
        sys.exit(0)

    if not MUTATOR_RE.search(command):
        sys.exit(0)                      # reading a frozen test is fine

    # Tokenize so a bare substring in an unrelated word cannot trip the match.
    try:
        tokens = set(shlex.split(command))
    except ValueError:
        tokens = set(command.split())
    tokens |= set(command.split())

    for locked in frozen_paths():
        base = os.path.basename(locked)
        hit = any(t == locked or t.endswith("/" + base) or t == base
                  or os.path.basename(t) == base for t in tokens)
        if hit or base in command:
            block(
                f"BLOCKED: this command would modify the frozen test {locked}.\n\n"
                f"  {command.strip()[:200]}\n\n"
                "The Edit-side hook does not see shell edits, which is exactly why\n"
                "this one exists. Editing the test now would change the measurement\n"
                "instead of the thing being measured, and a green result afterward\n"
                "would prove nothing.\n\n"
                "Fix the source so the existing test passes. If the test is\n"
                "genuinely wrong, say so and why, then run:\n"
                "  verify.sh release\n"
                "change it as its own visible step, and re-freeze.\n\n"
                "Reading it (cat, grep, diff, git show) is allowed and always was."
            )

    sys.exit(0)


if __name__ == "__main__":
    main()
