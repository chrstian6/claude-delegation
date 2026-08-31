#!/usr/bin/env bash
# Harvest deferred shortcuts into a ledger, so "later" doesn't become "never".
# Markers are left by skills/lazy: // ponytail: <what was skipped and when to revisit>
set -uo pipefail
cd "$(git rev-parse --show-toplevel 2>/dev/null || echo .)"
hits=$(grep -rn --exclude-dir={.git,node_modules,dist,build,.venv} -E '(ponytail|TODO-lazy):' . 2>/dev/null)
[[ -z "$hits" ]] && { echo "No deferred shortcuts. Either genuinely clean, or nobody is marking them."; exit 0; }
echo "$hits" | sed 's/^\.\///'
echo
echo "$(echo "$hits" | wc -l) deferred shortcut(s). Each should name what was skipped and what triggers doing it properly."
