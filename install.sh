#!/usr/bin/env bash
# Install the delegation org into a project WITHOUT using the plugin system.
#
# The plugin route (README, option A) is preferred: it updates with a git pull and
# touches nothing in the project. Use this when you want the files committed to the
# project itself, or when the host does not load plugins.
#
#   ~/claude-delegation/install.sh [target-project]   # default: $PWD
#   ~/claude-delegation/install.sh . --link           # symlink instead of copy
#
# Idempotent. Never overwrites POLICY.md or CLAUDE.md — it prints what to add instead.
set -euo pipefail

PKG="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$PWD}"
MODE="copy"
[[ "${2:-}" == "--link" ]] && MODE="link"

[[ -d "$TARGET" ]] || { echo "no such directory: $TARGET" >&2; exit 1; }
TARGET="$(cd "$TARGET" && pwd)"
[[ "$TARGET" != "$PKG" ]] || { echo "refusing to install the package into itself" >&2; exit 1; }

C="$TARGET/.claude"
# NOT skills/ or bin/ — those are place()'s targets, and in --link mode
# `ln -sfn src dst` against an EXISTING real directory creates the link INSIDE
# it (dst/skills -> src) instead of as it. bin/ was never pre-created and so
# always worked; skills/ was, so a --link install silently resolved ZERO skills
# and bin/skills.py reported none, with no error anywhere.
mkdir -p "$C"/{agents,hooks,state}

# place <src-dir> <dst-dir>
#
# Copies the package's entries INTO dst, overwriting same-named ones and leaving
# everything else alone. It deliberately does NOT `rm -rf "$dst"` first.
#
# It used to. `place "$PKG/skills" "$C/skills"` then deleted every skill the
# project had authored — on one real target that was 15 skills, including the
# two that carried its database stack, none of which this package ships. The
# README described this step as "copies agents, skills, bin and hooks" and never
# mentioned a delete, and `bin/skills.py` is documented as merging "the
# project's own .claude/skills/ on top" — which the copy route then made
# impossible. An installer silently deleting the user's own work is the worst
# failure this package can have, so the destructive form is gone rather than
# guarded.
#
# Stale plugin-owned entries are not pruned. That is the deliberate trade: an
# orphan costs nothing, a deleted project skill is unrecoverable if uncommitted.
place() {
  local src="$1" dst="$2"
  if [[ "$MODE" == "link" ]]; then
    ln -sfn "$src" "$dst"
  else
    mkdir -p "$dst"
    cp -R "$src"/. "$dst"/
  fi
}

# Agents: the plugin uses <name>.md; a project .claude/agents/ reads the same shape.
for f in "$PKG"/agents/*.md; do
  cp "$f" "$C/agents/$(basename "$f")"
done

place "$PKG/skills" "$C/skills"
place "$PKG/bin"    "$C/bin"
cp "$PKG"/hooks/*.py "$PKG"/hooks/*.sh "$C/hooks/"
chmod +x "$C"/hooks/* "$C"/bin/* 2>/dev/null || true

# Same rule as POLICY.md below: never clobber a file the project may have edited.
# DOCTRINE.md is what the README tells a project to @-include into its own
# CLAUDE.md, so it is exactly the kind of file someone tunes — and re-running an
# "idempotent" installer silently reverting those edits is the same class of bug
# as the destructive place() this script used to have.
for doc in "CLAUDE.template.md:DOCTRINE.md" "ORCHESTRATOR.md:ORCHESTRATOR.md"; do
  src="${doc%%:*}"; dst="${doc##*:}"
  if [[ -f "$C/$dst" ]] && ! cmp -s "$PKG/$src" "$C/$dst"; then
    cp "$PKG/$src" "$C/$dst.new"
    echo "$dst: yours differs — package copy written to $dst.new, yours left alone"
  else
    cp "$PKG/$src" "$C/$dst"
  fi
done

# --- settings.json: merge hooks in, never clobber what is already there ---
python3 - "$C" <<'PY'
import json, pathlib, sys

claude = pathlib.Path(sys.argv[1])
settings = claude / "settings.json"
existing = json.loads(settings.read_text()) if settings.is_file() else {}

D = "$CLAUDE_PROJECT_DIR/.claude"
def h(cmd, msg, timeout=10):
    return {"type": "command", "command": f"{D}/{cmd}", "timeout": timeout, "statusMessage": msg}

wanted = {
    "PreToolUse": [
        {"matcher": "Task|Agent",
         "hooks": [h("hooks/guard-delegation.py", "Checking the delegation contract...")]},
        {"matcher": "Edit|Write|MultiEdit|NotebookEdit",
         "hooks": [h("hooks/guard-frozen-tests.sh", "Checking the test freeze..."),
                   h("hooks/protect-files.sh", "Checking file protections..."),
                   h("hooks/warn-large-files.sh", "Checking for build artifacts..."),
                   h("hooks/scan-secrets.sh", "Scanning for secrets...")]},
        {"matcher": "Bash",
         "hooks": [h("hooks/guard-frozen-tests-bash.py", "Checking the test freeze (shell)..."),
                   h("hooks/block-dangerous-commands.sh", "Checking command safety..."),
                   h("hooks/orchestrator-only-git.sh", "Checking git ownership...")]},
    ],
    "SessionStart": [
        {"matcher": "startup|resume|clear",
         "hooks": [h("hooks/session-start.sh", "Loading project context...")]},
    ],
}

hooks = existing.setdefault("hooks", {})
added = 0
for event, groups in wanted.items():
    cur = hooks.setdefault(event, [])
    have = {json.dumps(g, sort_keys=True) for g in cur}
    for g in groups:
        if json.dumps(g, sort_keys=True) not in have:
            cur.append(g)
            added += 1

existing.setdefault("$schema", "https://json.schemastore.org/claude-code-settings.json")
settings.write_text(json.dumps(existing, indent=2) + "\n")
print(f"settings.json: {added} hook group(s) added, existing entries preserved")
PY

# --- POLICY.md: create only if absent. Never overwrite a real one. ---
if [[ -f "$TARGET/POLICY.md" ]]; then
  echo "POLICY.md: already present, left alone"
else
  cp "$PKG/POLICY.template.md" "$TARGET/POLICY.md"
  echo "POLICY.md: created from template — FILL IN test_command before using verify.sh"
fi

cat <<EOF

installed into $TARGET

  .claude/agents/     6 roles
  .claude/skills/     $(ls "$PKG/skills" | wc -l | tr -d ' ') skills
  .claude/bin/        router, freeze/verify, queue, metrics
  .claude/hooks/      guards (wired into .claude/settings.json)
  POLICY.md           project config — set test_command

One line left, in the project's CLAUDE.md:

  @.claude/DOCTRINE.md

Then set DELEGATION so the doctrine's commands resolve:

  export DELEGATION="\$PWD/.claude/bin"

Check it:  .claude/bin/route.py "fix the failing auth test" --level 2
EOF
