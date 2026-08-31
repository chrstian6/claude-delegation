---
name: root-cause-repair
description: >
  Fix where all callers pass through, not where the symptom was reported.
agent: repairer
priority: high
triggers:
  - real fix
  - proper fix
  - fix it properly
  - underlying cause
---

# Purpose

A fix at the report site leaves every sibling caller broken and guarantees the same bug returns from a different direction.

# When to use

Any fix to shared code, and any bug that has recurred.

# When not to use

A defect genuinely local to one call site with no shared surface.

# Inputs

The diagnosed cause and every caller of the code involved.

# Process

Grep every caller before editing. Decide where the guard belongs so all paths are covered. Prefer one change in the shared function to a change in each caller.

# Decision rules

One guard in a shared function is a smaller diff and a stronger fix than a guard in every caller. The lazy fix and the root-cause fix are usually the same edit.

# Constraints

Do not expand the fix into a redesign. Root cause means the right location, not a larger scope.

# Quality checks

Did you check every caller, or only the one in the report? Name them.

# Common failures

Patching the reported path. Fixing the symptom because the root cause is in code you did not want to touch.

# Output format

The cause, the location chosen and why, and the callers verified.

# Examples

A null crash on one page: the guard goes in the shared loader, and the four other callers are named as covered.

# Related skills

root-cause-analysis · minimal-fix · regression-prevention
