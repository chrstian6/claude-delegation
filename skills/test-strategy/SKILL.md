---
name: test-strategy
description: >
  Decide what is worth testing for this change, and what a pass would actually prove.
agent: tester
priority: high
triggers:
  - what to test
  - test plan
  - coverage
  - which tests
---

# Purpose

Tests are not free and coverage is not the goal. The goal is that a wrong implementation goes red.

# When to use

Before writing tests for any non-trivial change.

# When not to use

For a change with no behaviour — a comment, a rename with no call-site effect.

# Inputs

The change, its requirements, and the existing suite.

# Process

For each requirement, name the observation that would prove it. Prefer one test that fails for the right reason over five that fail together for the same one.

# Decision rules

Test behaviour, not structure. A test that must change whenever the implementation is refactored is testing the implementation.

# Constraints

Write the test before the implementation, watch it fail, then freeze it. A test written afterwards describes whatever the code happens to do.

# Quality checks

For each test: what wrong implementation does this catch? If you cannot name one, delete it.

# Common failures

Testing the framework. Asserting on hand-rendered SQL. Five tests for one behaviour and none for the edge that breaks.

# Output format

The tests planned, each with the failure it catches.

# Examples

A filter change gets one test per filter semantic and one for the combination, not one per UI element.

# Related skills

edge-case-analysis · frontend-testing · regression-testing
