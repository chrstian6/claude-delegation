---
name: accessibility-review
description: >
  Verify the interface is usable without a mouse, without full vision, and without motion — by trying it.
agent: reviewer
priority: high
triggers:
  - accessibility review
  - a11y review
  - keyboard test
  - screen reader check
---

# Purpose

Accessibility claims are usually inherited from a component library and never checked at the composition level, which is where they break.

# When to use

Any interactive surface, before acceptance.

# When not to use

Non-interactive static output.

# Inputs

The running surface, and its measured contrast table.

# Process

Walk the primary flow on the keyboard alone. Check focus is visible at every stop and the order is logical. Check labels reach the accessible name. Check the reduced-motion arm. Read the measured ratios.

# Decision rules

Measured, never estimated. WCAG AA: 4.5:1 body, 3:1 large text and UI components.

# Constraints

Never rely on colour alone for state. Touch targets need both min height and min width.

# Quality checks

Could you complete the task with the keyboard, and always know where you were?

# Common failures

Trusting the library. Checking contrast on the resting state only. Reduced motion that removes feedback as well as movement.

# Output format

The flow walked, what failed, and the measured pairs.

# Examples

Focus ring invisible on the image card because `ring-inset` paints under an opaque child — WCAG 2.4.7.

# Related skills

accessibility · design-review
