---
name: source-verification
description: >
  Establish whether a claim's source actually supports it, and how current it is.
agent: researcher
priority: high
triggers:
  - verify
  - source
  - is it true
  - citation
  - confirm
---

# Purpose

A confident answer built on a stale changelog is worse than no answer, because it survives review. Version and date are part of the claim.

# When to use

Before relying on any external claim: an API shape, a pricing figure, a deprecation, a capability.

# When not to use

For claims about this repository — those are settled by reading it, which is stronger than any external source.

# Inputs

The claim, and the source offered for it.

# Process

Find the primary source. Check its date and the version it describes. Check it says what the claim says, not merely something adjacent. State the retrieval date.

# Decision rules

A blog post about a library is not the library. A README on the web is not the installed version. When they disagree, the installed package wins.

# Constraints

Never cite a source you did not open. Never carry a version claim without the version.

# Quality checks

Does the source, read directly, support the specific sentence you are writing? Not the general area — the sentence.

# Common failures

Citing search-result snippets. Treating a summary as primary. Omitting the date on anything that changes.

# Output format

`CLAIM / SOURCE (url or path) / RETRIEVED (date) / VERSION / SUPPORTS: yes|partly|no`.

# Examples

"Tailwind v4 inlines the font variable" — verified against the installed package, not against a v3-era article.

# Related skills

research-method · uncertainty-analysis
