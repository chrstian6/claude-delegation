---
name: typography-system
description: >
  Choose and apply type so hierarchy comes from the system rather than from size alone.
agent: builder
priority: normal
triggers:
  - font
  - typeface
  - type scale
  - tracking
  - leading
  - text size
---

# Purpose

Type is where an interface most quickly reveals whether anyone made a decision. One family, one weight and three sizes is the default look of generated UI.

# When to use

Any surface where text carries the hierarchy, which is most of them.

# When not to use

When the project has a settled type system. Then apply it; inventing a second is the defect.

# Inputs

The hierarchy the surface needs, the existing tokens, and the data being displayed.

# Process

Assign roles before sizes: what is the page's one heading, what is supporting, what is data. Then choose family, weight, size, tracking, leading and measure per role.

# Decision rules

Tighten tracking as size grows; a single tracking value at every size is a tell. Use tabular figures for data. Serif only where the language genuinely benefits.

# Constraints

Emphasis inside a headline uses italic or bold of the same family — injecting a second family for one word is amateur.

# Quality checks

Cover the smallest and largest text on the page. Does the scale still read as one system?

# Common failures

Choosing a typeface by reputation. Letting default tracking ride at display sizes. Body measure so wide it is hard to track lines.

# Output format

The roles, their settings, and why the family suits them.

# Examples

A dashboard uses one sans for everything and a mono only for meter IDs and figures, where alignment actually matters.

# Related skills

design-taste · color-system · layout-composition
