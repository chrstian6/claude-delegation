---
name: security-review
description: >
  Find the ways this change could be abused, ranked by consequence.
agent: reviewer
priority: critical
triggers:
  - security
  - vulnerability
  - injection
  - exploit
  - authorization
---

# Purpose

Security defects are invisible to every other lens, and they are the ones where being late is most expensive.

# When to use

Any diff touching auth, input handling, queries, file paths, tokens, uploads, or authorization.

# When not to use

A pure styling change with no data path.

# Inputs

The diff, the trust boundaries it crosses, and who can reach it.

# Process

Walk the categories: injection (SQL string-building, command, XSS via innerHTML, template, path traversal), authentication, authorization, data exposure, SSRF, deserialization, dependencies, crypto, input validation, upload safety.

# Decision rules

IDOR first: any lookup on a user-supplied id with no ownership check. It is the most common real finding and the easiest to miss.

# Constraints

On this project: every jeweler-scoped read goes through the scoped DB layer — Neon has no RLS, so `scopedDb` is the only isolation there is — every `/admin/*` has its `requireAdmin`, and image bytes are raw base64 in their own field, never a `data:` URI.

# Quality checks

For each finding: the attack vector, and a proof-of-concept payload if one exists. A vulnerability without a vector is a worry.

# Common failures

Reviewing the code that changed while missing the boundary it crossed. Assuming an internal endpoint is unreachable.

# Output format

Severity-ranked findings, each with vector, impact and fix.

# Examples

A new endpoint takes a lead id from the client and never checks the vendor — IDOR, high, with the payload.

# Related skills

code-review · adversarial-review
