---
name: code-review
description: >
  Read a diff for correctness against its requirements, trying to find what is wrong.
agent: reviewer
priority: high
triggers:
  - review the code
  - correctness review
  - check the diff
  - code review
---

# Purpose

The writer has already convinced themselves. The reviewer's value is entirely in not sharing that context.

# When to use

Every diff that changes behaviour.

# When not to use

Formatting-only changes with no logic.

# Inputs

The diff, the requirements it claims to satisfy, and the evidence offered.

# Process

Check the requirements are met, then the logic, then the edge cases, then the error paths. Re-run the claimed evidence yourself before accepting it.

# Decision rules

A claim you did not reproduce is not verified. Trust `verify.sh check` over any summary.

# Constraints

You cannot write. Report findings; do not absorb them by fixing them quietly.

# Quality checks

For each finding: file, line, what is wrong, why it matters, severity. A finding without a consequence is a preference.

# Common failures

Reviewing style while missing a logic error. Approving because the tests are green without asking whether they would have gone red.

# Output format

`VERDICT / CHECKED (commands + exit codes) / FINDINGS / UNABLE`.

# Examples

A guard added in one caller: the finding is that three other callers route through the same function unguarded.

# Related skills

requirement-review · adversarial-review · test-quality-review
