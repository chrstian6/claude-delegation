---
name: component-architecture
description: >
  Decide what is a component, what is a prop, and what should stay inline.
agent: builder
priority: normal
triggers:
  - component structure
  - props
  - reuse
  - extract
  - split component
---

# Purpose

Premature componentization is the most common form of over-engineering in a UI codebase, and the resulting indirection is paid by every reader afterwards.

# When to use

When a surface grows past what one file should hold, or when a pattern genuinely repeats.

# When not to use

For a second occurrence. Three similar lines beat a helper used once, and two usages are not yet a pattern.

# Inputs

The surface, its repetitions, and where state actually lives.

# Process

Split on responsibility, not on length. Keep state as low as it can go. Isolate interactivity into leaf client islands so the rest stays server-rendered.

# Decision rules

An abstraction needs a third use or a real boundary. Otherwise inline it and move on.

# Constraints

Follow the existing component conventions; a second pattern for the same job is worse than the first pattern being imperfect.

# Quality checks

Would a new reader find the logic where they expect it? Does any component take more props than it has real variants?

# Common failures

A component per section, whether or not the sections differ. Prop drilling through three layers instead of moving the state. A wrapper that only forwards.

# Output format

The component boundaries and why each exists.

# Examples

A filter bar stays one file until the third filter type appears, at which point the shared shape is real rather than anticipated.

# Related skills

frontend-engineering · layout-composition
