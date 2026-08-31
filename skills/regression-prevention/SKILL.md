---
name: regression-prevention
description: >
  Leave behind the check that would have caught this.
agent: repairer
priority: high
triggers:
  - prevent regression
  - add a test for
  - make sure it stays
  - guard against
---

# Purpose

A fix without a test is a fix that will be undone by the next person who does not know why the line is there.

# When to use

After every repair of a real defect.

# When not to use

For a fix to code with no runnable test path — then say so, and say what testing it would require.

# Inputs

The defect, the fix, and the test that failed to catch it.

# Process

Write a test that fails before the fix and passes after. Verify both directions — a test that passes before the fix caught nothing.

# Decision rules

The test asserts the behaviour, not the implementation. Otherwise the next refactor deletes the protection along with the shape.

# Constraints

If a defect escaped the suite, that is a coverage gap: name it, even when you cannot close it.

# Quality checks

Did you run the test against the unfixed code? If not, you do not know it catches anything.

# Common failures

Writing the test after the fix and never checking it fails without it. Asserting the fix's shape rather than the behaviour.

# Output format

The test, plus evidence it fails on the old code and passes on the new.

# Examples

The guard's test is run against the pre-fix state, goes red, then green — both shown.

# Related skills

minimal-fix · test-strategy · verification
