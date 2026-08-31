---
name: verification
description: >
  Prove the fix worked and that nothing else broke.
agent: repairer
priority: critical
triggers:
  - verify the fix
  - did it work
  - confirm fixed
  - retest
---

# Purpose

The repair loop's last step is the one most often skipped, because by then the fix feels obvious. That feeling is not evidence.

# When to use

After every repair, without exception.

# When not to use

Never skipped. The depth scales with risk; the requirement does not.

# Inputs

The original failing command, and the blast radius of the change.

# Process

Re-run the exact command that failed. Then run the regression check across the callers you touched. Report both, with exit codes.

# Decision rules

The original failure is the primary evidence. A different command passing is not the same claim.

# Constraints

Never report a run you did not execute. If the suite will not start, that is the result. `--verified none` is legitimate; a fabricated pass is not.

# Quality checks

Do you have the before and after output of the same command? Anything else is a different claim.

# Common failures

Running a narrower command than the one that failed. Declaring victory on a typecheck. Skipping the regression check because the fix was small.

# Output format

`BEFORE (command + output) / AFTER (same command + output) / REGRESSION (what else ran)`.

# Examples

The failing test named in the report is re-run verbatim, then the four callers' tests, all with exit codes.

# Related skills

regression-prevention · evidence-reporting
