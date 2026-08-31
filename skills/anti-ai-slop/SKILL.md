---
name: anti-ai-slop
description: >
  Detect and remove the patterns that make an interface look statistically generated, without swapping one cliché for another.
agent: builder
priority: high
triggers:
  - generic
  - ai slop
  - looks like every
  - template
  - cliché
  - distinctive
---

# Purpose

The failure is not ugliness. It is an interface that is plausible, competent and indistinguishable from a thousand others — which is exactly what a model produces when it defaults.

# When to use

Any surface the user will see, and mandatorily on anything described as premium, distinctive, or a redesign.

# When not to use

Where convention genuinely helps the user. A login form that looks like a login form is not slop; it is legible.

# Inputs

The built surface, and the product it belongs to.

# Process

Run the three tests. STRUCTURE: strip brand and copy — does the composition still feel like this product? DECORATION: strip effects — does hierarchy survive? AI-SIMILARITY: would another model produce nearly this from the same prompt? Then fix and re-run.

# Decision rules

Avoid by default: Inter/Roboto everywhere, purple-blue AI gradients, neon glow, generic glassmorphism, centered hero with a giant meaningless headline, three identical feature cards, three identical pricing towers, card-on-card, rounded-everything, pill-everything, floating blobs, generic SaaS illustrations, rocket and shield icons, emoji UI, Lorem Ipsum, John Doe, Acme, fake-perfect statistics, dead href="#", modal for everything, sidebar by default.

# Constraints

Do not replace a cliché with a different cliché. Specificity comes from the product, not from a fresher trend.

# Quality checks

If a meaningful problem is found: FIX, then review again. Reporting it is not the job.

# Common failures

Treating the ban list as the whole skill, so the result avoids all thirty patterns and is still generic. Adding novelty that costs usability.

# Output format

The three test results, what was changed, and what was deliberately kept.

# Examples

A dashboard fails STRUCTURE because stripped of copy it is four equal cards; fixed by making the primary metric structurally dominant rather than typographically louder.

# Related skills

design-taste · component-diversity · content-quality
