---
name: motion-engineering
description: >
  Implement motion so it stays smooth and interruptible under real input.
agent: builder
priority: normal
triggers:
  - spring
  - damping
  - fps
  - jank
  - performance of animation
  - raf
---

# Purpose

A well-chosen animation implemented badly is worse than none: it janks on the device the designer did not have, and it fights the user's next action.

# When to use

Whenever motion is being built rather than merely decided.

# When not to use

For a simple CSS transition on hover. Reaching for a physics library there is over-engineering.

# Inputs

The interaction, the property that moves, and whether the user can interrupt it.

# Process

Animate transform and opacity only. Drive continuous pointer motion through motion values, not React state — state re-renders the tree on every frame and collapses on mobile. Clean up every effect.

# Decision rules

Springs for drag, gesture, momentum and interruptible interaction. Critically damped for ordinary UI. Bounce only where real physical momentum justifies it.

# Constraints

Never `window.addEventListener('scroll')` for scroll-driven work — use the platform's scroll-driven primitives or an observer.

# Quality checks

Interrupt it mid-flight. Does it continue from where it is, or snap and restart?

# Common failures

State-driven pointer tracking. Animating layout properties. Effects without cleanup. Bounce on a menu, which reads as unserious.

# Output format

The properties animated and how interruption is handled.

# Examples

A draggable widget tracks pointer-down continuously with a spring, preserves velocity on release, and cancels cleanly on escape.

# Related skills

motion · gesture · performance
