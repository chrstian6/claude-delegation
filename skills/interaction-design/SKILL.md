---
name: interaction-design
description: >
  Design what the interface does in response to the user, including everything that is not the happy path.
agent: builder
priority: high
triggers:
  - interaction
  - behavior
  - click
  - hover
  - drag
  - flow
  - affordance
---

# Purpose

The happy path is the smallest part of an interface's behaviour and the only part that gets built by default.

# When to use

Any component with state, and any multi-step flow.

# When not to use

Static content with no interaction.

# Inputs

The flow, its states, and what can fail inside it.

# Process

Map the states before writing them: default, hover, focus, active, disabled, loading, success, error, empty, selected, expanded, collapsed, offline, permission denied, validation failure. Then build the ones that can occur here.

# Decision rules

Respond on pointer-down, not on release. Keep interactions interruptible. Never lock input while something is in flight if the user might reasonably want out.

# Constraints

Avoid `window.alert()` as a primary pattern. An empty state is a designed screen, not a blank div.

# Quality checks

Walk the flow and try to break it: double-click the submit, go back mid-flow, lose the network. Does it behave, or does it hang?

# Common failures

Building only the success case. A loading state that does not match the shape of what is loading. Disabled controls with no explanation.

# Output format

The state list with what each does, and which cannot occur here and why.

# Examples

A filter that shows a skeleton of the same row height, an empty state naming the filter that produced it, and an error state offering a retry.

# Related skills

interaction-states · motion · gesture
