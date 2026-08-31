---
name: accessibility
description: >
  Make the interface usable without a mouse, without full vision, and without motion.
agent: builder
priority: critical
triggers:
  - accessible
  - a11y
  - keyboard
  - screen reader
  - contrast
  - focus
---

# Purpose

Accessibility is a floor, not a feature. It is also the cheapest thing to get right while building and the most expensive to retrofit.

# When to use

Every interactive surface. Always.

# When not to use

Never skipped. Depth scales with surface, but the floor does not move.

# Inputs

The component, its interaction model, and the measured contrast of every pair it introduces.

# Process

Semantic HTML first — most of this is free if the element is right. Then keyboard order, visible focus, labels, and the reduced-motion arm. Measure contrast; never estimate it.

# Decision rules

WCAG AA: body text 4.5:1, large text and UI components 3:1. Never rely on colour alone for state. Touch targets need both a min height and a min width — a floor on one is half a target.

# Constraints

Run `node scripts/verify/contrast.mjs --scope <scope>` and add a standing row for any new pair. A ratio in a comment goes stale; a row in the table does not.

# Quality checks

Can you complete the primary flow with the keyboard alone, and see where you are at every step?

# Common failures

Div soup with click handlers. A focus ring hidden behind an opaque child. Reduced-motion that removes the feedback along with the movement. Colour as the only status signal.

# Output format

The measured contrast rows plus the keyboard path you actually walked.

# Examples

A status pill gets an icon and a label, not just a colour, and its ring is measured over the darkest surface it can sit on.

# Related skills

interaction-states · motion · design-taste
