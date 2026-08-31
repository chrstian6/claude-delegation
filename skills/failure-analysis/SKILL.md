---
name: failure-analysis
description: >
  Turn a failure into evidence someone can act on without re-running it.
agent: tester
priority: high
triggers:
  - why did it fail
  - failure
  - error output
  - stack trace
  - what broke
---

# Purpose

"It failed" is not a finding. The error, the exit code and the conditions are what let the next step be a diagnosis instead of a guess.

# When to use

Whenever a check fails.

# When not to use

When the failure is a typo in the command you just typed. Fix it and rerun.

# Inputs

The command, its exit code, and its complete output.

# Process

Capture the command verbatim, the exit code, and the error as printed. Note which tests failed and whether they fail in isolation. Distinguish a failure from an error from a timeout.

# Decision rules

Classify: requirement, implementation, dependency, configuration, environment, test, data, permission, unknown. The class decides who fixes it.

# Constraints

Never paraphrase an error. Never report a verdict read out of a log tail — grep for FAIL, because failure lines print before the summary.

# Quality checks

Could someone reproduce this from your report alone? If not, something is missing.

# Common failures

Summarizing instead of quoting. Missing that a test only fails under concurrency. Reporting the last error when the first one caused it.

# Output format

`COMMAND / EXIT / COUNTS / FAILURES (verbatim) / ISOLATION (does it fail alone?)`.

# Examples

Five timeouts in one run, all passing in isolation: reported as a concurrency flake, not five bugs.

# Related skills

regression-testing · evidence-reporting · root-cause-analysis
