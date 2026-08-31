---
name: debugging
description: >
  Find why something fails, using evidence rather than plausible stories.
agent: repairer
priority: high
triggers:
  - debug
  - not working
  - broken
  - investigate failure
  - trace
  - fix
  - failing
  - bug
  - error
  - crash
---

# Purpose

The expensive mistake is fixing something that was never the cause. It costs the attempt, hides the real defect, and leaves a change nobody can justify.

# When to use

Any failure whose cause is not immediately obvious.

# When not to use

A typo with an unambiguous error. Fix it.

# Inputs

The actual error, a reproduction, and what changed recently.

# Process

Reproduce first — an unreproduced bug cannot be verified fixed. Narrow to the smallest triggering input. Form one hypothesis and test only it. Read the error rather than pattern-matching it.

# Decision rules

Change one thing at a time. Three changes at once means the outcome teaches you nothing about any of them.

# Constraints

Never fix what you cannot reproduce. Never assume the error message is wrong until you have read it carefully.

# Quality checks

Can you explain why it worked before, or why it never did? If neither, you have a correlation.

# Common failures

Fixing the first plausible cause. Adding logging instead of forming a hypothesis. Concluding it is flaky before checking whether it fails in isolation.

# Output format

`SYMPTOM / REPRODUCTION / HYPOTHESIS / TEST / RESULT`, one hypothesis per cycle.

# Examples

An auth test failing only in the full run: reproduced in isolation, it passes — the cause is shared state, not the auth code.

# Related skills

root-cause-analysis · failure-analysis · minimal-fix
