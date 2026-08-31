---
name: interaction-states
description: >
  Build every state a component can actually be in, not just the one where everything worked.
agent: builder
priority: high
triggers:
  - states
  - empty state
  - loading
  - error state
  - disabled
  - hover
---

# Purpose

The happy path is what gets built by default and the smallest part of what users encounter. Missing states are found by users, in production.

# When to use

Any component with data, input or asynchrony.

# When not to use

Static presentational markup with no states to be in.

# Inputs

The component and everything that can happen to it.

# Process

Walk the list: default, hover, focus, active, disabled, loading, success, error, empty, selected, expanded, collapsed, offline, permission denied, validation failure. Build those that can occur; say why the rest cannot.

# Decision rules

Forms need label, input, helper text where useful, inline validation, error, loading, disabled and success. An empty state is a designed screen that says what would fill it.

# Constraints

A loading state matches the shape of what is loading. A skeleton that does not mirror the real component is a second layout to maintain and it will drift.

# Quality checks

Try to reach each state deliberately. Any you cannot reach is either impossible — say so — or unbuilt.

# Common failures

Spinners where a skeleton belongs. "No data" as an empty state. Disabled controls with no reason given. Errors that discard what the user typed.

# Output format

Each state, whether it was built, and why any was skipped.

# Examples

A filter's empty state names the filter that emptied it and offers to clear it.

# Related skills

interaction-design · accessibility · content-quality
