---
name: gesture
description: >
  Build direct-manipulation interactions that follow the user continuously.
agent: builder
priority: normal
triggers:
  - drag
  - swipe
  - pinch
  - gesture
  - pointer
  - touch
---

# Purpose

A gesture that only reacts when it ends is not a gesture, it is a button with extra steps. The continuity is the entire affordance.

# When to use

Drag, swipe, pinch, pull, resize, reorder — anything the user moves with a finger or pointer.

# When not to use

A click. Adding gesture machinery to a button is complexity with no return.

# Inputs

The element, what it moves relative to, and what cancels the interaction.

# Process

Respond on pointer-down. Track continuously. Respect the grab offset so the element does not jump. Use pointer capture. Track velocity where momentum matters. Support cancellation and interruption.

# Decision rules

The element follows the pointer during the gesture, not after it. If it snaps into place only on release, the implementation is faking it.

# Constraints

Never fake a gesture with a final-state-only handler. Never lock the pointer without a way out.

# Quality checks

Start a drag, then press escape. Does it cancel cleanly and return? Start one and reverse direction — does it follow?

# Common failures

Ignoring the grab offset, so the element jumps to the cursor. No cancellation path. Momentum that overshoots into an invalid position.

# Output format

The gesture, its cancellation path, and how velocity is handled.

# Examples

Reordering widgets: the card follows the pointer from the grab point, neighbours reflow live, escape returns it to origin.

# Related skills

motion-engineering · interaction-design
