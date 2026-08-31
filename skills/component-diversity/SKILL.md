---
name: component-diversity
description: >
  Build around the product's actual information architecture instead of the default section sequence.
agent: builder
priority: normal
triggers:
  - hero
  - landing
  - sections
  - page structure
  - marketing page
---

# Purpose

Navbar, hero, three cards, testimonials, pricing, logos, CTA, footer is a template. Emitting it means the page's structure carries no information about the product.

# When to use

Any page assembled from sections, especially marketing and dashboards.

# When not to use

Where a conventional pattern genuinely aids recognition — a settings page that looks like a settings page.

# Inputs

What the product actually does and what the user came to do.

# Process

Derive sections from the information architecture. Where a conventional section adds nothing, replace it: inline editing, progressive disclosure, slide-overs, split views, search, command interfaces, contextual controls.

# Decision rules

Familiar patterns are kept where familiarity helps the user, not where they help the author avoid a decision.

# Constraints

No section may exist because pages usually have one.

# Quality checks

Remove each section in turn. Does the page lose something real? If not, it was filler.

# Common failures

Three equal feature cards for three unequal features. A testimonials block with invented testimonials. A pricing grid where there is one price.

# Output format

The sections, and what each earns.

# Examples

A dashboard with no hero: the first thing on the page is the number the user opened it for.

# Related skills

anti-ai-slop · layout-composition · content-quality
