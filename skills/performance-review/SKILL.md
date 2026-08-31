---
name: performance-review
description: >
  Find the cost this change adds, before it reaches the hot path.
agent: reviewer
priority: normal
triggers:
  - performance review
  - slow query
  - n+1
  - render performance
---

# Purpose

Performance regressions are cheap to prevent in review and expensive to find in production, because they degrade rather than break.

# When to use

Diffs touching queries, loops over data, render paths, or anything on a request path.

# When not to use

One-off scripts and build-time code.

# Inputs

The diff, and where the code runs.

# Process

Look for N+1s, unbounded scans, a new predicate with no index, work in a render, and anything synchronous on a request path.

# Decision rules

Rank by how it scales, not by how it looks. A loop over three items is fine; the same loop over an unbounded result set is not.

# Constraints

A performance claim needs a measurement or a complexity argument, not an impression.

# Quality checks

For each finding, what happens at 10x the current data volume?

# Common failures

Micro-optimizing a render while an N+1 sits above it. Calling code slow without a number or an argument.

# Output format

Findings with the cost, the scaling behaviour, and the fix.

# Examples

A list fetches its author per row — one query becomes N, unbounded by page size.

# Related skills

performance · code-review
