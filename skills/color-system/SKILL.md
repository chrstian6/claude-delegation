---
name: color-system
description: >
  Build a palette that stays coherent across states and themes, and prove its contrast.
agent: builder
priority: normal
triggers:
  - color
  - palette
  - accent
  - dark mode
  - theme
  - contrast ratio
---

# Purpose

Colour is where accessibility fails silently and where a design most easily becomes noisy. Both are prevented by restraint plus measurement.

# When to use

Any new surface, any theme work, any new semantic state.

# When not to use

Where the palette exists and applies cleanly. Do not introduce a variant for one component.

# Inputs

The existing tokens, the surfaces they sit on, and the states that need signalling.

# Process

Controlled neutrals, one considered accent, desaturated semantics, one grey temperature. Design dark mode deliberately rather than inverting.

# Decision rules

Spend the accent in one place per view. A translucent token's alpha is a function of its ground, so any background change silently retunes every alpha over it.

# Constraints

Measure with `scripts/verify/contrast.mjs` and add a standing row per new pair. Measure the worst case — the pressed state over the darkest surface — not the resting one.

# Quality checks

Is every pair in the table, including hover and active? A ratio you did not measure is a ratio you do not have.

# Common failures

AI-purple gradients by default. Mixing warm and cool neutrals. Dark mode derived by inversion, so hierarchy inverts with it.

# Output format

The tokens added and the measured contrast rows.

# Examples

One accent on the overdue state; everything else carries in neutrals, so the one coloured thing means something.

# Related skills

design-taste · accessibility
