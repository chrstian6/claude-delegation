---
name: acceptance
description: >
  Decide whether work is actually complete, against evidence rather than confidence.
agent: orchestrator
priority: critical
triggers:
  - done
  - accept
  - complete
  - finished
  - ship it
---

# Purpose

Output produced and task completed are different states. The gap between them is where fabricated verdicts live, and confidence is exactly the signal that cannot tell them apart.

# When to use

Before reporting any non-trivial task complete, and before merging anything.

# When not to use

For a trivial answer with no artifact. There is nothing to accept.

# Inputs

The success criteria, the evidence produced, and the list of what remains unverified.

# Process

Check each criterion against a command, an exit code, a diff stat or a file that exists. Anything with no evidence is unverified, and unverified is reported, not assumed.

# Decision rules

Accept only when every required criterion has evidence, no blocking issue remains, required tests pass, and the actions taken were authorized. Confidence never substitutes for a failed check.

# Constraints

Before delivering, ask: did I do the whole thing or the easy part? Did I skip something tedious? Did I leave work I could have finished? If a required gap remains, close it — reporting a gap you could have closed is not completion.

# Quality checks

For each criterion, name the evidence. If the answer is a description rather than an output, it is not evidence.

# Common failures

Accepting "implemented" as a result. Treating a green typecheck as a verified feature. Declaring done at merge rather than at verification.

# Output format

Criterion by criterion: `<criterion> — <the command and its exit code>` or `UNVERIFIED — <what checking would take>`.

# Examples

A builder returns "done, it works": rejected, with the specific evidence required — the command, its output, and which criterion each satisfies.

# Related skills

risk-analysis · evidence-reporting · adversarial-review
