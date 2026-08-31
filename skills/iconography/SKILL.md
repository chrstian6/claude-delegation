---
name: iconography
description: >
  Use icons that clarify meaning, from one family, at consistent weight.
agent: builder
priority: low
triggers:
  - icon
  - icons
  - glyph
  - symbol
---

# Purpose

Mixed icon families and cliché metaphors are small signals that accumulate into an interface looking assembled rather than designed.

# When to use

Any interface using icons.

# When not to use

Where a word is clearer. A labelled button usually beats an ambiguous glyph.

# Inputs

The actions needing symbols, and the icon library already installed.

# Process

Pick one family and stay in it. Standardize weight, size, alignment and optical density. Pair with a label wherever the meaning is not universal.

# Decision rules

Never use emoji in UI. Prefer Phosphor, Radix, or project-specific SVG. Avoid rocket, shield, lightning and other cliché metaphors.

# Constraints

Never hand-roll icon paths when a library is installed; never mix two families in one tree.

# Quality checks

Cover the icon with your thumb. Is the control still understandable? If not, it needed a label.

# Common failures

Two families in one view. Icons at whatever size they arrived at. Decorative icons that carry no meaning and no alt.

# Output format

The family, the standard size and weight, and where labels accompany icons.

# Examples

One family at 1.5 stroke, 16px in dense rows and 20px in headers, always beside a label in the nav.

# Related skills

design-taste · accessibility
