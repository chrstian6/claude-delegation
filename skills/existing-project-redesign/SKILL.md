---
name: existing-project-redesign
description: >
  Change how an existing surface looks without breaking what it does.
agent: builder
priority: high
triggers:
  - redesign
  - restyle
  - refresh
  - modernize
  - update the look
---

# Purpose

A redesign that also rewrites the logic is two changes wearing one commit, and when it breaks nobody can tell which half did it.

# When to use

Any restyle of a surface that already works.

# When not to use

Greenfield. There is nothing to preserve, so the constraint does not apply.

# Inputs

The current surface, its framework, its styling system, its state, and its actual behaviour.

# Process

SCAN the framework, dependencies, components and current visual language. DIAGNOSE what specifically is wrong. Make the TARGETED change. TEST that behaviour is unchanged.

# Decision rules

Preserve working business logic. Do not migrate technology for aesthetic reasons. Land the token change first — it re-skins every screen and is the cheapest reviewable increment.

# Constraints

Never drop a token the previous block declared without checking what reads it — several are undefined at :root on purpose, and an undefined var() paints nothing and throws no error.

# Quality checks

Does every flow that worked before still work? Did you check, or assume?

# Common failures

Rewriting from scratch because the existing code is imperfect. Changing behaviour while changing appearance. Removing a token that something invisible depended on.

# Output format

What changed visually, what was deliberately preserved, and the evidence behaviour is intact.

# Examples

A portal restyle lands as a token block first; component edits follow only where the tokens could not reach.

# Related skills

design-taste · anti-ai-slop · component-architecture
