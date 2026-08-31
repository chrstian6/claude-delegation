---
name: minimal-fix
description: >
  Change only what the diagnosis justifies.
agent: repairer
priority: high
triggers:
  - smallest fix
  - minimal change
  - just fix
  - targeted
---

# Purpose

A fix that also refactors is two changes in one commit, and when something breaks nobody can tell which half did it.

# When to use

Every repair.

# When not to use

When the diagnosis genuinely requires a structural change — then say so, and treat it as its own task with its own review.

# Inputs

The diagnosis, and the code around the fix.

# Process

Write the smallest change that addresses the cause. Note adjacent problems in the report instead of fixing them. Preserve working behaviour exactly.

# Decision rules

Unrelated improvements go in the report, not the diff. "While I was in there" is how a repair becomes unreviewable.

# Constraints

Never reformat a file you are repairing. The diff must show the fix, not the formatter.

# Quality checks

Could a reviewer see the fix in the diff without hunting? If not, it is too large.

# Common failures

Refactoring while fixing. Adding defensive code nobody asked for. Renaming things in passing.

# Output format

The diff, and the adjacent issues you deliberately left alone.

# Examples

A one-line guard, plus a note that the same function has an unrelated naming inconsistency worth a separate task.

# Related skills

root-cause-repair · regression-prevention
