---
name: anti-card
description: >
  Use a card only when elevation, boundary or layering does real work.
agent: builder
priority: normal
triggers:
  - card
  - panel
  - container
  - box
  - grouping
---

# Purpose

Cards are the default container of generated UI. Everything becomes a box, and when everything is a box nothing has hierarchy.

# When to use

Before creating any card, panel or bordered container.

# When not to use

Where a boundary genuinely separates surfaces — a modal over a page, a floating control over content.

# Inputs

The content being grouped and why it belongs together.

# Process

Ask three questions: does elevation communicate hierarchy, does the boundary clarify grouping, does the surface create meaningful layering. If none, use spacing, dividers, a background change, typographic grouping or alignment.

# Decision rules

Dense interfaces need less boxing, not more. Nothing inside a card should draw a second border or radius.

# Constraints

Nested radius is arithmetic: inner equals outer minus the padding. An inner radius larger than its parent is the tell.

# Quality checks

Remove the borders. Is the grouping still legible from spacing and type alone? If yes, the border was decoration.

# Common failures

Card-on-card. A card per item because a list needed structure. Shadows plus borders both turned up.

# Output format

Which groupings are cards, and what the others use instead.

# Examples

A table of routes uses hairline row dividers inside one panel, not a card per route.

# Related skills

layout-composition · design-taste
