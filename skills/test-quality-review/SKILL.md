---
name: test-quality-review
description: >
  Judge whether the tests would go red if the implementation were wrong.
agent: reviewer
priority: high
triggers:
  - would the test catch
  - test quality
  - weak test
  - mutation
---

# Purpose

A passing suite is evidence only if it can fail. Tests that cannot fail are the most dangerous artifact in a repository, because they are counted as coverage.

# When to use

Any diff that adds or changes tests, and any repair claiming a fix is verified.

# When not to use

Where no tests were claimed. The finding is then simply that.

# Inputs

The tests, and the implementation they cover.

# Process

Mentally mutate: delete the guard, invert the condition, return the wrong shape. For each, would a test go red? Then check coverage of the change specifically, not the file.

# Decision rules

A `toContain` on a class string is almost never valid — prefix-nested families mean deleting the feature passes. A presence check is not an assertion.

# Constraints

`toMatchObject` with an empty leaf matches any object. A test that never makes its mock reject leaves the whole error class untested.

# Quality checks

Name the mutation each test catches. If a test catches none, it is decoration.

# Common failures

Counting tests. Accepting snapshots. Missing that the assertion was weakened in the same commit as the code it guarded.

# Output format

Per test: what it catches, or that it catches nothing.

# Examples

Three new tests, all asserting the component renders — none would fail if the filter logic inverted.

# Related skills

adversarial-review · test-strategy
