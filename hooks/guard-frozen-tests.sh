#!/usr/bin/env bash
# Claude Code PreToolUse hook. Blocks writes to frozen test files.
#
# The freeze is only a rule until something enforces it. This turns "don't edit
# the test" from an instruction the model may rationalize past into a tool call
# that is refused.
#
# Wire it up in .claude/settings.json:
#   { "hooks": { "PreToolUse": [ {
#       "matcher": "Edit|Write|MultiEdit|NotebookEdit",
#       "hooks": [ { "type": "command",
#                    "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/guard-frozen-tests.sh" } ]
#   } ] } }
#
# Exit 0 = allow. Exit 2 = block, and stderr goes back to Claude as the reason.
#
# PARSING: the payload is JSON, and JSON escapes non-ASCII — a path containing
# "cafe\u0301" arrives escaped. Regex-scraping the raw text compares the literal
# escape against the real filename and silently fails open. It also cannot tell a
# real file_path from one appearing inside a `content` string. So: parse it as
# JSON, and fail CLOSED if that is not possible.
#
# KNOWN GAP: this hook only sees the tools in its matcher. A shell edit
# (sed -i, >, git checkout --) via Bash bypasses it entirely. Cover that in your
# Bash guard, or accept that the freeze is enforced for agent edits and detected
# after the fact, by verify.sh run, for shell edits.

set -uo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
LOCK="$ROOT/.claude/state/test-lock.txt"

# No active freeze: nothing to protect. The only fail-open path, and correct —
# there is nothing to compare against.
[[ -f "$LOCK" ]] || exit 0

payload="$(cat)"

read -r -d '' EXTRACT <<'PY'
import json, sys
try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(3)
ti = d.get("tool_input") or {}
out = []
for k in ("file_path", "notebook_path", "path"):
    v = ti.get(k)
    if isinstance(v, str):
        out.append(v)
for e in (ti.get("edits") or []):
    if isinstance(e, dict) and isinstance(e.get("file_path"), str):
        out.append(e["file_path"])
print("\n".join(out))
PY

if ! command -v python3 >/dev/null 2>&1; then
  echo "BLOCKED: python3 not on PATH; cannot parse payload while a freeze is active." >&2
  exit 2
fi

paths="$(printf '%s' "$payload" | python3 -c "$EXTRACT")"
rc=$?

if [[ $rc -ne 0 ]]; then
  cat >&2 <<'EOF'
BLOCKED: could not parse the tool payload while a test freeze is active.

Failing closed on purpose. A guard that cannot read the request cannot know
whether it targets a frozen test, and allowing it would make the freeze
unenforceable exactly when it matters.

Run verify.sh release if the freeze is stale.
EOF
  exit 2
fi

[[ -n "$paths" ]] || exit 0

canon() {
  local p="$1"
  [[ "$p" = /* ]] || p="$ROOT/$p"
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$p" 2>/dev/null || echo "$p"
}

while IFS= read -r target; do
  [[ -n "$target" ]] || continue
  ctarget="$(canon "$target")"
  while read -r _hash locked; do
    [[ -n "$locked" ]] || continue
    if [[ "$ctarget" == "$(canon "$locked")" ]]; then
      cat >&2 <<EOF
BLOCKED: $target is a frozen test file.

It was locked with verify.sh freeze after you observed it fail. Editing the test
now would change the measurement instead of the thing being measured — a green
result afterward would prove nothing.

Fix the source code so the existing test passes.

If the test itself is genuinely wrong (it encodes a misread requirement), stop,
say so explicitly and why, then run:
  verify.sh release
change the test as its own visible step, and re-freeze.
EOF
      exit 2
    fi
  done < "$LOCK"
done <<< "$paths"

exit 0
