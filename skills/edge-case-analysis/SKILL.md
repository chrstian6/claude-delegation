---
name: edge-case-analysis
description: >
  Find the inputs and sequences that break something which works on the happy path.
agent: tester
priority: normal
triggers:
  - edge case
  - boundary
  - what if
  - corner case
  - null
---

# Purpose

The happy path is what was built and what was checked. Everything expensive lives just outside it.

# When to use

Any logic with branches, boundaries, external input or asynchrony.

# When not to use

Straight-line code with no branches and no input.

# Inputs

The behaviour and the shape of its inputs.

# Process

Work the boundaries: empty, one, many, maximum. Then absent, null, wrong type, duplicate. Then sequence: out of order, repeated, interrupted, concurrent.

# Decision rules

Prioritize by consequence. An edge case that loses data outranks one that renders oddly.

# Constraints

An edge case you cannot construct is a hypothesis; say so rather than asserting the behaviour.

# Quality checks

Have you tried zero, one and many? Most boundary bugs are at zero and one.

# Common failures

Listing exotic cases while missing the empty list. Testing rejection but never the double-submit.

# Output format

The cases tried, what each did, and which remain untested.

# Examples

A pagination fix is tried at zero rows, exactly one page, and one row past the boundary.

# Related skills

test-strategy · failure-analysis
