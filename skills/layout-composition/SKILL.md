---
name: layout-composition
description: >
  Compose a page so its structure carries the hierarchy, not its decoration.
agent: builder
priority: normal
triggers:
  - layout
  - grid
  - spacing
  - composition
  - alignment
  - structure the page
---

# Purpose

Centred-everything with equal cards is the default composition of generated UI, and it flattens importance into a grid.

# When to use

Any new page or significant restructure.

# When not to use

Small components inside an existing layout.

# Inputs

The content, its relative importance, and the container's real width budget.

# Process

Establish what dominates. Use asymmetry, offsets, mixed proportions and negative space to make that structural rather than typographic. Use CSS Grid for real relationships.

# Decision rules

Every unusual structural choice must improve focus, hierarchy, flow, story or rhythm. If it improves none, it is novelty.

# Constraints

Avoid fragile flexbox percentage math. Pair `grid-rows` with `grid-cols-[minmax(0,1fr)]` — rows alone create one implicit auto column that overflows. Prefer `min-height: 100dvh`.

# Quality checks

Squint at it. Does the eye land on the most important thing first, without colour or weight doing the work?

# Common failures

Cards as the default container. Equal columns for unequal content. Centering because it is safe.

# Output format

The grid, what dominates, and why.

# Examples

A stat strip becomes one panel divided by hairlines rather than four equal cards, so the numbers read as a set.

# Related skills

design-taste · responsive-design · anti-card
