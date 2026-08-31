---
name: evidence-reporting
description: >
  Report results as machine-checkable output, never as a composed summary.
agent: tester
priority: critical
triggers:
  - evidence
  - prove it
  - show the output
  - did it pass
---

# Purpose

A summary looks identical whether or not the run happened. That is precisely why it cannot be evidence.

# When to use

Every time a result is reported to the orchestrator or the user.

# When not to use

Never skipped. Depth varies; the requirement does not.

# Inputs

The commands run and their real output.

# Process

Report the command, its exit code, and the counts as the runner printed them. Quote failures verbatim. Say explicitly what was not run.

# Decision rules

Evidence is a command with an exit code, a diff stat, a named test with a state, or a file that exists. "It should work", "it compiles", "looks correct" are not evidence.

# Constraints

Never report a run you did not execute — not as a prediction, not as a formatting convenience. If a check could not run, that is the result.

# Quality checks

Is every claim traceable to output you actually saw? Any that is not must be marked unverified.

# Common failures

Composing a plausible summary. Reporting the intent of a command. Claiming coverage from a run that errored at startup.

# Output format

Raw output plus one line naming which criterion each result satisfies.

# Examples

`npx vitest run — exit 1, 8416 passed, 1 failed: lib/auth.test.ts "rejects expired token"`.

# Related skills

failure-analysis · acceptance
