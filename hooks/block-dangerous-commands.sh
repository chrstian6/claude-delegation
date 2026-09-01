#!/usr/bin/env bash
# Blocks dangerous shell commands: push to protected branches, force push,
# destructive operations. PreToolUse hook for Bash operations.
# Exit 2 = block. Exit 0 = allow.
#
# Configurable via env:
#   CLAUDE_PROTECTED_BRANCHES  comma list (default: derived from git + main,master)

set -uo pipefail

emit_deny() {
  # Emit a JSON deny decision and exit 2.
  local reason="${1//\"/\\\"}"
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$reason"
  exit 2
}

if ! command -v jq >/dev/null 2>&1; then
  emit_deny "jq is required for command protection hooks but is not installed."
fi

INPUT=$(cat)
COMMAND=$(printf '%s' "$INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null || true)
[ -z "$COMMAND" ] && exit 0

# JOIN BACKSLASH LINE-CONTINUATIONS BEFORE ANY MATCHING. `git push \<newline>
# --force origin main` is one logical command written across two physical lines,
# and the shell will run it as one. Every pattern below is written against the
# logical command, so matching them against the raw physical lines lets an
# ordinary line-wrapped invocation slip past — force-push to anything, with no
# rule able to see it. Joining here fixes it once, for every rule, instead of
# teaching 26 patterns about continuations.
COMMAND=${COMMAND//\\$'\n'/ }

# ── Protected branch list ────────────────────────────────────────────────
DEFAULT_BRANCHES="main,master"
if GIT_DEFAULT=$(git config --get init.defaultBranch 2>/dev/null) && [ -n "$GIT_DEFAULT" ]; then
  DEFAULT_BRANCHES="$DEFAULT_BRANCHES,$GIT_DEFAULT"
fi
PROTECTED_BRANCHES="${CLAUDE_PROTECTED_BRANCHES:-$DEFAULT_BRANCHES}"
# Build a regex alternation: main|master|develop|...
BR_REGEX=$(printf '%s' "$PROTECTED_BRANCHES" | tr ',' '\n' | awk 'NF{printf "%s%s",sep,$0; sep="|"}')

# bash's own ERE engine, not `printf | grep` — that was two process spawns
# per call across 19 calls, and on Windows process spawn is expensive enough
# that this one guard measured 2.97-9.61s (15 runs, median 4.96) while the
# other four guards are ~0.3s each. auto-approve-all.py runs every guard
# before it may approve anything, with a per-guard timeout; at that speed it
# was timing out on a guard that had actually PASSED, so the hook deferred
# intermittently and .claude/tests/auto-approve-matrix.py was flaky.
# Measured: 19 calls, 3796ms via grep -> 122ms via [[ =~ ]].
#
# THAT SPEEDUP IS SINGLE-LINE ONLY — do not quote it as the general case. Once
# per-line iteration was restored below (it had to be: the whole-string form was
# a bypass), the cost became O(lines x rules) in pure bash, and on multi-line
# input this is now SLOWER than the grep it replaced. Best-of-3, this machine:
#
#   lines      grep    [[ =~ ]] whole-string    HEAD (per-line)
#       1      50ms                     26ms              30ms
#     200      52ms                     27ms              95ms
#    2000      63ms                     39ms             677ms
#   10000     177ms                    110ms            3327ms
#
# Crossover is ~150 lines. Heredocs writing a file and generated scripts hit
# that easily, and Windows — where this guard already measured 2.97-9.61s and
# where GUARD_TIMEOUT_S sits at 12 — is the platform with no headroom. Hoisting
# the split into a one-time array recovers about a third (2000 lines:
# 677 -> 454ms) and does not remove the linear term. Correctness first; if this
# ever times out in practice, fix it by hoisting, never by returning to
# whole-string matching.
#
# The patterns are unchanged: [[ =~ ]] takes the same POSIX ERE, including
# [[:space:]] classes. `$1` MUST stay unquoted on the right-hand side —
# quoting it makes bash match it as a literal string, which would silently
# stop every one of these checks from ever firing.
#
# ITERATE PER LINE. Not a style choice — removing the loop reopens a proven
# bypass. `grep -qE` matches per LINE, so `^` and `$` anchor at every newline.
# `[[ =~ ]]` matches the WHOLE STRING, so `^` anchors only at the very start.
# The regexes are byte-identical and the semantics are not, which is why "the
# patterns are unchanged" above was true and irrelevant. Every rule anchored
# with `(^|[;&|()]+...)` or a trailing `$` silently stopped applying to any
# line after the first:
#
#   git push --force origin main            -> denied  (one line, ^ matches)
#   cd /repo <newline> git push --force ...  -> ALLOWED before this fix
#
# Caught in review, then reproduced end to end: a two-line Bash call
# force-pushing to main was auto-approved with no prompt shown. Only the push
# family diverged (4 of 80 probed variants) because `\n` falls inside
# [[:space:]] for every other rule — which is exactly what made it invisible.
#
# WHOLE-STRING FIRST, THEN PER LINE. The whole-string pass is not redundant: a
# backslash line-continuation splits one logical command across two physical
# lines, so `git push \<newline>  --force origin main` is invisible to every
# per-line pattern while the whole-string pass still sees it. Per-line alone
# would have been a straight downgrade from the discarded version on exactly
# that shape.
_match_lines() {                  # _match_lines <ere>; reads $COMMAND
  local line
  [[ $COMMAND =~ $1 ]] && return 0
  while IFS= read -r line; do
    [[ $line =~ $1 ]] && return 0
  done <<< "$COMMAND"
  return 1
}
contains_cmd() { _match_lines "$1"; }
# A deny pattern with a suppressor must see BOTH on the same line. Riding two
# separate whole-input calls let a suppressor on one line disarm a deny on
# another: `npm publish --dry-run` followed by a real `npm publish` was allowed,
# which is the precise thing that rule exists to stop.
contains_cmd_unless() {           # contains_cmd_unless <ere> <suppressor-ere>
  local line
  while IFS= read -r line; do
    [[ $line =~ $1 ]] && ! [[ $line =~ $2 ]] && return 0
  done <<< "$COMMAND"
  return 1
}
# nocasematch is bash's equivalent of grep -i. Saved and restored rather than
# left on: it is a shell-wide option and would change the behaviour of every
# later [[ ]] and case statement in this script.
contains_icmd() {
  local restore rc
  restore=$(shopt -p nocasematch)
  shopt -s nocasematch
  _match_lines "$1"; rc=$?
  eval "$restore"
  return $rc
}

# ── Git push protections ────────────────────────────────────────────────
# `^[[:space:]]*` — WITHOUT it a single leading space or tab disables every push
# rule below, because they all live inside this gate and the alternation had no
# whitespace-after-^ branch. An indented `git push --force origin main`, which is
# what any command inside an `if`/`for`/heredoc looks like, sailed through.
if contains_cmd '(^[[:space:]]*|[;&|()]+[[:space:]]*)git[[:space:]]+push'; then
  # Explicit refspec to a protected branch (origin main, :main, HEAD:main, remote branch)
  if contains_cmd "git[[:space:]]+push[[:space:]]+[^[:space:]]+[[:space:]]+([^[:space:]]*:)?($BR_REGEX)(\$|[[:space:]])"; then
    MATCHED_BRANCH=$(printf '%s' "$COMMAND" | grep -oE "($BR_REGEX)(\$|[[:space:]])" | head -1 | tr -d '[:space:]')
    emit_deny "Blocked: push to protected branch '${MATCHED_BRANCH:-main}'. Use a feature branch and open a PR."
  fi
  if contains_cmd "git[[:space:]]+push.*:($BR_REGEX)(\$|[[:space:]])"; then
    MATCHED_BRANCH=$(printf '%s' "$COMMAND" | grep -oE ":($BR_REGEX)(\$|[[:space:]])" | head -1 | tr -d ': [:space:]')
    emit_deny "Blocked: push to protected branch '${MATCHED_BRANCH:-main}' via refspec. Use a feature branch and open a PR."
  fi
  # Bare `git push` while on protected branch
  if contains_cmd 'git[[:space:]]+push[[:space:]]*($|[;&|])'; then
    CURRENT=$(git branch --show-current 2>/dev/null || true)
    if [ -n "$CURRENT" ] && printf '%s' ",$PROTECTED_BRANCHES," | grep -q ",$CURRENT,"; then
      emit_deny "Blocked: you are on '$CURRENT' (a protected branch). Switch to a feature branch."
    fi
  fi
  # Force push (but allow --force-with-lease)
  # Same-line suppressor: a --force-with-lease on ANOTHER line must not disarm a
  # real --force on this one.
  if contains_cmd_unless 'git[[:space:]]+push([[:space:]]+[^[:space:]]+)*[[:space:]]+(-[a-zA-Z]*f[a-zA-Z]*|--force)([[:space:]=]|$)' \
     '\-\-force-with-lease'; then
    emit_deny "Blocked: force push is not allowed. Use --force-with-lease if you must overwrite remote."
  fi
fi

# ── Branch / remote-ref deletion ────────────────────────────────────────
# -D is force-delete (discards unmerged commits); -d is the safe merged-only
# delete that CLAUDE.md's "delete branches after merge" step relies on.
if contains_cmd 'git[[:space:]]+branch([[:space:]]+[^[:space:]]+)*[[:space:]]+(-D|--delete[[:space:]]+--force|-[a-zA-Z]*D[a-zA-Z]*)([[:space:]]|$)'; then
  emit_deny "Blocked: 'git branch -D' force-deletes a branch with unmerged commits. Use -d, or delete manually if intended."
fi
if contains_cmd 'git[[:space:]]+push([[:space:]]+[^[:space:]]+)*[[:space:]]+(--delete|-d)([[:space:]]|$)'; then
  emit_deny "Blocked: 'git push --delete' removes a remote branch. Delete it via the GitHub UI or manually if intended."
fi
if contains_cmd 'git[[:space:]]+push[[:space:]]+[^[:space:]]+[[:space:]]+:[^[:space:]]+'; then
  emit_deny "Blocked: refspec ':branch' deletes a remote branch. Delete it manually if intended."
fi

# ── Destructive filesystem operations ───────────────────────────────────
# rm -rf targeting root, home, $HOME, $VAR (any unresolved expansion), or parent traversal.
# We normalise quotes before matching so "my folder", '$HOME/trash', etc. Are all inspected.
CMD_NOQUOTE=$(printf '%s' "$COMMAND" | tr -d "'\"")
if printf '%s' "$CMD_NOQUOTE" | grep -qE 'rm[[:space:]]+(-[a-zA-Z]*[[:space:]]+)*-?[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*[[:space:]]+(/([[:space:]]|\*|$)|~|\$HOME|\$[A-Za-z_][A-Za-z0-9_]*|\.\./\.\.)' ; then
  emit_deny "Blocked: recursive force-delete on /, ~, \$HOME, an unresolved \$VAR, or .../.. Path. Specify a concrete safe target."
fi
# rm -rf /usr, /etc, /var, /bin, etc.
if printf '%s' "$CMD_NOQUOTE" | grep -qE 'rm[[:space:]]+(-[a-zA-Z]+[[:space:]]+)*-?[a-zA-Z]*r[a-zA-Z]*f[a-zA-Z]*[[:space:]]+/(usr|etc|var|bin|sbin|lib|opt|root|boot)([[:space:]/]|$)'; then
  emit_deny "Blocked: recursive delete targeting a system directory."
fi

# ── Dangerous database operations ───────────────────────────────────────
# DROP TABLE|DATABASE|SCHEMA
if contains_icmd 'DROP[[:space:]]+(TABLE|DATABASE|SCHEMA)[[:space:]]+'; then
  emit_deny "Blocked: DROP TABLE/DATABASE/SCHEMA detected. Run manually if intended."
fi
# DELETE FROM without a WHERE on the SAME statement.
# Split on ';' so multi-statement inputs are analysed per-statement.
if printf '%s\n' "$COMMAND" | awk '
  BEGIN { IGNORECASE=1; RS=";" }
  /DELETE[[:space:]]+FROM[[:space:]]+[A-Za-z_][A-Za-z0-9_.]*/ {
    if ($0 !~ /WHERE/) { print "BAD"; exit }
  }
' | grep -q BAD; then
  emit_deny "Blocked: DELETE FROM without a WHERE clause. Add a WHERE or run manually."
fi
if contains_icmd 'TRUNCATE[[:space:]]+TABLE'; then
  emit_deny "Blocked: TRUNCATE TABLE detected. Run manually if intended."
fi

# ── Dangerous system commands ───────────────────────────────────────────
# chmod: any world-writable/universal mode (0?777 or a+rwx)
if contains_cmd 'chmod([[:space:]]+-[a-zA-Z]+)*[[:space:]]+0?777([[:space:]]|$)' \
  || contains_cmd 'chmod([[:space:]]+-[a-zA-Z]+)*[[:space:]]+a\+rwx([[:space:]]|$)'; then
  emit_deny "Blocked: chmod 777 / a+rwx grants everyone full access. Use restrictive perms."
fi

# curl/wget piped to a shell
if contains_cmd '(curl|wget)[[:space:]].*\|[[:space:]]*(sudo[[:space:]]+)?(bash|sh|zsh|ksh|fish|dash|csh)([[:space:]]|$)'; then
  emit_deny "Blocked: piping downloaded content directly to a shell is dangerous."
fi

# Disk / partition. Note: only REDIRECTIONS to /dev/ are destructive. `2>/dev/null` is not.
# Pattern matches: `>[ ]*/dev/<something>` but NOT `2>/dev/null` or `&>/dev/null` style for fd-null.
# Strategy: match `>` optionally with whitespace, followed by /dev/<name>, EXCLUDING /dev/null and /dev/stderr/stdout.
if printf '%s' "$COMMAND" | grep -qE '(^|[^0-9&])>[[:space:]]*/dev/[a-zA-Z][a-zA-Z0-9]*' \
   && ! printf '%s' "$COMMAND" | grep -qE '>[[:space:]]*/dev/(null|stdout|stderr|tty|zero|random|urandom)([[:space:]]|$)' ; then
  emit_deny "Blocked: redirection into a raw device file can destroy data."
fi
if contains_cmd '(^|[;&|[:space:]])(mkfs|mkfs\.[a-z0-9]+)([[:space:]]|$)' \
  || contains_cmd '(^|[;&|[:space:]])dd[[:space:]]+[^|]*(if|of)=/dev/[a-zA-Z]' ; then
  emit_deny "Blocked: mkfs/dd against a device node. Irreversible data loss."
fi

# ── Destructive git ─────────────────────────────────────────────────────
if contains_cmd 'git[[:space:]]+reset[[:space:]]+--hard'; then
  emit_deny "Blocked: git reset --hard discards uncommitted changes permanently."
fi
if contains_cmd 'git[[:space:]]+clean[[:space:]]+-[a-zA-Z]*f'; then
  emit_deny "Blocked: git clean -f permanently deletes untracked files."
fi

# ── Accidental package publishing ───────────────────────────────────────
# Allow --dry-run variants (npm publish --dry-run is safe and common in CI).
publish_patterns=(
  '(npm|yarn|pnpm|bun)[[:space:]]+publish'
  'cargo[[:space:]]+publish'
  'gem[[:space:]]+push'
  'twine[[:space:]]+upload'
)
for pat in "${publish_patterns[@]}"; do
  if contains_cmd_unless "$pat" '(^|[[:space:]])(--dry-run|-n)([[:space:]=]|$)'; then
    emit_deny "Blocked: publishing packages should run in CI or manually, not via Claude."
  fi
done

exit 0
