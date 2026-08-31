---
name: frontend-testing
description: >
  Test UI behaviour rather than UI structure, so the test survives a redesign.
agent: builder
priority: normal
triggers:
  - test the ui
  - component test
  - frontend test
  - rtl
---

# Purpose

A test asserting class names breaks on every restyle and catches no bug. A test asserting behaviour survives the redesign and catches the regression.

# When to use

After building any component with logic, state or a data dependency.

# When not to use

For a purely presentational component with no branches. There is nothing to assert that is not a snapshot of the markup.

# Inputs

The component, its states, and what a user does with it.

# Process

Assert what the user sees and can do: the empty state renders, the error shows the message, the disabled control cannot be clicked. Avoid asserting internal structure.

# Decision rules

A `toContain` on a class string is almost never valid — Tailwind families are prefix-nested, so deleting the feature passes. Anchor the boundaries or assert behaviour instead.

# Constraints

jsdom's getComputedStyle returns plausible garbage; do not measure layout there. `gate:edit` is typecheck only and runs no lint.

# Quality checks

Break the implementation deliberately. Does the test go red? If not, it is decoration.

# Common failures

Snapshot tests that get blessed on every change. Asserting class names. Mocking the component under test so the real path never runs.

# Output format

The tests added and what each would catch.

# Examples

A filter test asserts that selecting a status changes the visible rows — not that the button has a particular class.

# Related skills

test-strategy · edge-case-analysis
