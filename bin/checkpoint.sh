#!/usr/bin/env bash
# Checkpoint before risky work. This is what "rollback" actually means in a
# coding system — a commit you can return to, not a conceptual policy version.
#
#   ./checkpoint.sh create "before auth migration"
#   ./checkpoint.sh list
#   ./checkpoint.sh restore agent/2026-08-30-1432
#
# Run create before any high-risk task. It costs a second and it is the
# difference between an undo and an incident.

set -euo pipefail

cmd="${1:-help}"

case "$cmd" in
  create)
    msg="${2:-checkpoint}"
    tag="agent/$(date +%Y-%m-%d-%H%M)"
    if [[ -n "$(git status --porcelain)" ]]; then
      git stash push -u -m "checkpoint: $msg" >/dev/null
      git stash apply >/dev/null
      echo "uncommitted work stashed as a safety copy"
    fi
    git tag -f "$tag" -m "$msg" >/dev/null
    echo "checkpoint: $tag  ($msg)"
    echo "restore with: ./checkpoint.sh restore $tag"
    ;;

  list)
    git tag -l 'agent/*' --sort=-creatordate --format='%(refname:short)  %(creatordate:short)  %(contents:subject)'
    ;;

  restore)
    tag="${2:?usage: checkpoint.sh restore <tag>}"
    echo "This resets the working tree to $tag. Uncommitted changes will be lost."
    read -r -p "Type the tag again to confirm: " confirm
    [[ "$confirm" == "$tag" ]] || { echo "aborted"; exit 1; }
    git reset --hard "$tag"
    echo "restored to $tag"
    ;;

  diff)
    tag="${2:?usage: checkpoint.sh diff <tag>}"
    git diff --stat "$tag"..HEAD
    ;;

  *)
    echo "usage: checkpoint.sh {create <msg>|list|restore <tag>|diff <tag>}"
    exit 1
    ;;
esac
