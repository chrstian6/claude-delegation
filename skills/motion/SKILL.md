---
name: motion
description: >
  Decide whether something should move, then make the movement mean something.
agent: builder
priority: normal
triggers:
  - animate
  - animation
  - transition
  - motion
  - easing
---

# Purpose

Motion is the easiest thing to add and the hardest to justify. Unjustified motion is the most reliable signal that an interface was decorated rather than designed.

# When to use

Before adding any animation, and when reviewing one that already exists.

# When not to use

Frequently-used UI where the only argument is that it looks impressive. That cost is paid on every interaction, forever.

# Inputs

The state change, and what the user needs to understand about it.

# Process

Answer, in order: should this animate, why, what does the movement communicate, can it be interrupted, what property moves, what easing, how long, and what happens under reduced motion.

# Decision rules

Valid purposes: feedback, spatial continuity, state indication, orientation, explanation, preventing an abrupt change. "It looks cool" is not one.

# Constraints

Animate transform and opacity. Avoid animating top, left, width and height. Keep expensive grain and noise on a fixed, pointer-events-none layer, never on scrolling content.

# Quality checks

Turn it off. Is the interface worse? If not, it was decoration.

# Common failures

Animating everything so nothing reads as significant. Reduced-motion arms that delete the feedback along with the movement. A reveal keyframe with fill:both leaving elements invisible when animation is off.

# Output format

Each animation with its purpose, duration, easing and reduced-motion behaviour.

# Examples

A drawer slides from the edge it belongs to — spatial continuity. A row highlight does not animate, because the change is already legible.

# Related skills

motion-engineering · gesture · accessibility
