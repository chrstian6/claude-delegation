---
name: responsive-design
description: >
  Make a layout work at every width it will actually be used at, and verify rather than assume.
agent: builder
priority: high
triggers:
  - mobile
  - responsive
  - breakpoint
  - small screen
  - tablet
---

# Purpose

Responsive bugs are invisible from the machine that built them. They are found by users on the width nobody opened.

# When to use

Any layout change, and any component that will appear on a phone.

# When not to use

Fixed-width contexts like a print stylesheet or an emailed report.

# Inputs

The component, its container's real width budget, and the breakpoints the project uses.

# Process

Design the narrow case first. Declare the collapse for every multi-column layout in the same file. Then check the widths in between, where most breakage lives.

# Decision rules

A viewport breakpoint is not a container width. A `lg:` rule inside a 400px panel fires on a 1440px screen and squeezes the content. Never copy a breakpoint between two surfaces with different width budgets.

# Constraints

Prefer grid over flexbox percentage math. Use `min-height: 100dvh`, never `h-screen`, for viewport-filling sections.

# Quality checks

Have you looked at it between the breakpoints? The failure is usually at 900px, not at 375.

# Common failures

Testing only at the design breakpoints. Assuming Tailwind handles it. A button label whose no-wrap width sets a grid track wider than the viewport.

# Output format

The widths checked and what happened at each.

# Examples

A toolbar with three fixed controls crushed the title to 2px at 320px; fixed on the row with wrap and a min width, desktop unchanged.

# Related skills

layout-composition · interaction-states · accessibility
