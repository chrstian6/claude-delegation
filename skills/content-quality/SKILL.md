---
name: content-quality
description: >
  Write interface copy that is specific to this product and never fabricated.
agent: builder
priority: high
triggers:
  - copy
  - text
  - wording
  - labels
  - microcopy
  - content
---

# Purpose

Generic copy is the fastest way to make a real product look like a demo, and fabricated copy is a lie shipped at scale.

# When to use

Every label, empty state, error message, heading and button in a user-facing surface.

# When not to use

Internal debug output. Clarity still helps, but the standard is different.

# Inputs

The product's real vocabulary, and the actual data the screen shows.

# Process

Name real things: a jeweler, a lead, a design, a project stage. Say what the control does. Write the error as what happened and what to do next.

# Decision rules

Avoid: Elevate, Seamless, Unleash, Next-gen, Game-changing, Revolutionary, Delve, Unlock your potential, Supercharge, Empower your workflow. Prefer specific nouns, specific verbs, concrete outcomes, plain language.

# Constraints

Never fabricate a statistic, testimonial, customer, or result. Never use Lorem Ipsum, John Doe or Acme. Placeholder data must be plausibly real and clearly not a claim.

# Quality checks

Read every visible string aloud. Does any of it sound like it was written to fill a space? Would any of it be a lie if a customer read it?

# Common failures

Marketing voice inside product UI. An empty state that says "No data". An error that says "Something went wrong" when the system knows exactly what went wrong.

# Output format

The strings, with anything invented marked as placeholder.

# Examples

"No leads in Payao this cycle" beats "No data available" — it names the filter that produced the emptiness.

# Related skills

design-taste · anti-ai-slop · interaction-states
