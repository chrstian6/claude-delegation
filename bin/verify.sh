#!/usr/bin/env bash
# Test provenance. Makes "the tests passed" checkable instead of assertable.
#
# The problem this solves: an agent under pressure to produce a green result can
# edit the test, skip it, or delete it. Freezing the test files before
# implementation turns that from an invisible move into a detected one.
#
#   verify.sh freeze tests/auth_test.py      # after RED, before implementing
#   verify.sh check                          # did any test file move?
#   verify.sh run                            # check + run suite + compare counts
#   verify.sh release                        # clear the lock (task done)
#
# Test command comes from POLICY.md (test_command:) or the TEST_CMD env var.

set -uo pipefail

# The freeze belongs to the PROJECT being worked on, not to this package —
# otherwise two projects share one lock file and each releases the other's.
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
LOCK="$ROOT/.claude/state/test-lock.txt"
META="$ROOT/.claude/state/test-lock.meta"

hash_file() {
  if command -v sha256sum >/dev/null 2>&1; then sha256sum "$1" | cut -d' ' -f1
  else shasum -a 256 "$1" | cut -d' ' -f1; fi
}

test_cmd() {
  if [[ -n "${TEST_CMD:-}" ]]; then echo "$TEST_CMD"; return; fi
  sed -n 's/^ *test_command: *//p' "$ROOT/POLICY.md" "$ROOT/.claude/POLICY.md" 2>/dev/null \
    | sed 's/ *#.*$//' | grep -v '^$' | head -1
}

# Count test results out of common runner output. Best-effort by design: when it
# cannot parse, it reports "unknown" rather than inventing a number. The hash
# check does not depend on this and works for every language.
parse_counts() {
  local out="$1" passed="" failed="" total=""

  # pytest / jest / rust:  "41 passed", "3 failed", "41 passed; 3 failed"
  passed=$(grep -oE '[0-9]+ passed' <<<"$out" | tail -1 | grep -oE '[0-9]+')
  failed=$(grep -oE '[0-9]+ failed' <<<"$out" | tail -1 | grep -oE '[0-9]+')
  total=$(grep -oE '[0-9]+ total' <<<"$out" | tail -1 | grep -oE '[0-9]+')

  # vitest:  "Tests  41 passed | 3 failed (44)"
  [[ -z "$total" ]] && total=$(grep -oE 'Tests?[^(]*\(([0-9]+)\)' <<<"$out" | grep -oE '[0-9]+' | tail -1)

  # rspec:  "44 examples, 3 failures"
  if [[ -z "$passed" ]] && grep -qE '[0-9]+ examples?' <<<"$out"; then
    total=$(grep -oE '[0-9]+ examples?' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    failed=$(grep -oE '[0-9]+ failures?' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    passed=$(( ${total:-0} - ${failed:-0} ))
  fi

  # junit/maven:  "Tests run: 44, Failures: 3, Errors: 0"
  if [[ -z "$passed" ]] && grep -qE 'Tests run:' <<<"$out"; then
    total=$(grep -oE 'Tests run: *[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    local fl er
    fl=$(grep -oE 'Failures: *[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    er=$(grep -oE 'Errors: *[0-9]+'   <<<"$out" | tail -1 | grep -oE '[0-9]+')
    failed=$(( ${fl:-0} + ${er:-0} ))
    passed=$(( ${total:-0} - failed ))
  fi

  # dotnet:  "Failed: 3, Passed: 41, Skipped: 0, Total: 44"
  if [[ -z "$passed" ]] && grep -qE 'Passed: *[0-9]+' <<<"$out"; then
    passed=$(grep -oE 'Passed: *[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    failed=$(grep -oE 'Failed: *[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    total=$(grep -oE  'Total: *[0-9]+'  <<<"$out" | tail -1 | grep -oE '[0-9]+')
  fi

  # phpunit:  "OK (44 tests, 88 assertions)"  /  "Tests: 44, Assertions: 88, Failures: 3."
  if [[ -z "$passed" ]] && grep -qE 'Tests: *[0-9]+|OK \([0-9]+ tests' <<<"$out"; then
    total=$(grep -oE '(Tests: *|OK \()[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    failed=$(grep -oE 'Failures: *[0-9]+' <<<"$out" | tail -1 | grep -oE '[0-9]+')
    failed=${failed:-0}; passed=$(( ${total:-0} - failed ))
  fi

  # go test: reports per-package, not per-test. Count FAIL/ok lines instead.
  if [[ -z "$passed" ]] && grep -qE '^(ok|FAIL|---)' <<<"$out"; then
    failed=$(grep -cE '^--- FAIL|^FAIL' <<<"$out")
    passed=$(grep -cE '^ok |^--- PASS' <<<"$out")
    total=$(( passed + failed ))
    [[ $total -eq 0 ]] && { passed=""; failed=""; total=""; }
  fi

  # Nothing matched — say so rather than reporting a confident zero.
  if [[ -z "$passed" && -z "$failed" && -z "$total" ]]; then
    echo "unknown unknown unknown"; return
  fi
  passed=${passed:-0}; failed=${failed:-0}
  [[ -z "$total" ]] && total=$((passed + failed))
  echo "$passed $failed $total"
}

case "${1:-help}" in

freeze)
  shift
  [[ $# -gt 0 ]] || { echo "usage: verify.sh freeze <test-file>..." >&2; exit 1; }
  mkdir -p "$ROOT/.claude/state"; : > "$LOCK"
  for f in "$@"; do
    [[ -f "$f" ]] || { echo "not a file: $f" >&2; exit 1; }
    echo "$(hash_file "$f")  $f" >> "$LOCK"
  done

  cmd="$(test_cmd)"
  baseline="unknown"
  if [[ -n "$cmd" ]]; then
    out="$(eval "$cmd" 2>&1)"; read -r p f t <<<"$(parse_counts "$out")"
    baseline="$t"
    if [[ "$f" == "0" && "$t" != "0" && "$t" != "unknown" ]]; then
      echo
      echo "  WARNING: nothing is failing at freeze time."
      echo "  A new test that passes before the implementation exists is not"
      echo "  testing anything. Confirm you observed RED before continuing."
      echo
    fi
    if [[ "$t" == "unknown" ]]; then
      echo
      echo "  NOTE: could not parse test counts from this runner."
      echo "  The file-hash check still works; the count-drop check is disabled."
      echo "  Read the RED output yourself before continuing."
      echo
    fi
  fi
  {
    echo "total_at_freeze=$baseline"
    echo "cmd_at_freeze=$cmd"
  } > "$META"
  echo "frozen $# test file(s); total tests at freeze: $baseline"
  echo "these paths are now FORBIDDEN to the implementer until 'verify.sh release'"
  ;;

check)
  [[ -f "$LOCK" ]] || { echo "no active freeze"; exit 0; }
  bad=0
  while read -r want path; do
    [[ -n "$path" ]] || continue
    if [[ ! -f "$path" ]]; then
      echo "DELETED:  $path"; bad=1; continue
    fi
    got="$(hash_file "$path")"
    if [[ "$got" != "$want" ]]; then echo "MODIFIED: $path"; bad=1; fi
  done < "$LOCK"
  if [[ $bad -eq 0 ]]; then echo "OK: all frozen test files unchanged"; exit 0; fi
  echo
  echo "A frozen test changed during implementation. This invalidates the run:"
  echo "the measurement moved, so a green result proves nothing."
  echo "Either restore the file, or state openly why the test was wrong and re-freeze."
  exit 2
  ;;

run)
  "$0" check || exit 2
  cmd="$(test_cmd)"
  if [[ -z "$cmd" ]]; then
    echo "No test command. Set test_command: in POLICY.md or TEST_CMD env." >&2
    echo "Do not report this task as verified." >&2
    exit 3
  fi
  echo "\$ $cmd"
  out="$(eval "$cmd" 2>&1)"; code=$?
  echo "$out"
  read -r p f t <<<"$(parse_counts "$out")"
  echo
  echo "exit=$code  passed=$p  failed=$f  total=$t"

  base="unknown"; basecmd=""
  if [[ -f "$META" ]]; then
    base="$(sed -n 's/^total_at_freeze=//p' "$META")"
    basecmd="$(sed -n 's/^cmd_at_freeze=//p' "$META")"
  fi

  if [[ -n "$basecmd" && "$basecmd" != "$cmd" ]]; then
    echo
    echo "  NOTE: count-drop check skipped — this run used a different command"
    echo "        than the freeze, so the totals are not comparable."
    echo "        freeze: $basecmd"
    echo "        run:    $cmd"
    echo "        The file-hash check ran and is authoritative."
  elif [[ "$base" =~ ^[0-9]+$ && "$t" =~ ^[0-9]+$ && "$t" -lt "$base" ]]; then
    echo
    echo "  TEST COUNT DROPPED: $base -> $t"
    echo "  Tests were removed or skipped during implementation. Restore them."
    exit 2
  fi
  [[ $code -eq 0 ]] && echo "VERIFIED" || echo "NOT VERIFIED — failures above are the result. Report them."
  exit $code
  ;;

release)
  rm -f "$LOCK" "$META"; echo "freeze released"
  ;;

*)
  echo "usage: verify.sh {freeze <files>|check|run|release}"
  ;;
esac
