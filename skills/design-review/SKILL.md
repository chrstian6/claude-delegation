---
name: design-review
description: >
  Judge whether an interface was designed or defaulted, and say what specifically to change.
agent: reviewer
priority: normal
triggers:
  - design review
  - looks
  - visual review
  - ui review
  - hierarchy
---

# Purpose

Design feedback that cannot be acted on is noise. Every finding names the element and the change.

# When to use

Any user-facing surface, especially one described as premium or redesigned.

# When not to use

Internal tooling where function is the only requirement.

# Inputs

The built surface, its purpose, and the design decisions claimed for it.

# Process

Run the three differentiation tests — structure, decoration, AI-similarity. Then check hierarchy, type, spacing, colour discipline, and whether states exist.

# Decision rules

Direction is the designer's call; whether the direction was executed is yours. Do not relitigate a chosen palette — review whether it was applied coherently.

# Constraints

Contrast is measured, never eyeballed. A ratio you did not measure is not a finding.

# Quality checks

Is every finding actionable? "Feels generic" is not; "four equal cards flatten the primary metric" is.

# Common failures

Taste assertions with no reason. Reviewing the direction instead of the execution. Missing that the mobile composition was never checked.

# Output format

Findings with element, problem, and the concrete change.

# Examples

"The stat row reads as four peers; the collected figure is the one users open this page for and should dominate structurally."

# Related skills

anti-ai-slop · accessibility-review · adversarial-review
