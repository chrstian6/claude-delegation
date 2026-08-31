---
name: regression-testing
description: >
  Prove that what worked before still works after the change.
agent: tester
priority: high
triggers:
  - regression
  - did i break
  - still works
  - broke something
---

# Purpose

Most damage from a fix is not in the thing fixed. It is in the neighbour that shared the function and nobody re-ran.

# When to use

After any repair, and after any change to shared code.

# When not to use

After a change to an isolated new file nothing imports yet.

# Inputs

The change, and what depends on the code it touched.

# Process

Identify the blast radius by grepping callers, not by intuition. Run the tests that cover them. Report what you ran, not what you believe is covered.

# Decision rules

The scope of the regression check follows the blast radius of the change, not the size of the diff.

# Constraints

Never report a suite you did not run. If it will not start, the startup error is the result.

# Quality checks

Did you actually run the callers' tests, or only the one for the file you edited?

# Common failures

Running only the new test. Assuming untouched files are unaffected when the change was in shared code. Reading a summary tail instead of an exit code.

# Output format

The commands run, their exit codes, and the counts as printed.

# Examples

A guard added in a shared loader: the regression check runs every caller's tests, not just the reporting one.

# Related skills

test-strategy · failure-analysis
