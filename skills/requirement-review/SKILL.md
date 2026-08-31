---
name: requirement-review
description: >
  Check the work against what was actually asked, including what was quietly dropped.
agent: reviewer
priority: normal
triggers:
  - did it meet
  - requirements met
  - scope
  - as asked
---

# Purpose

Work that satisfies its own restatement of the task is the most common way a request goes unmet without anyone noticing.

# When to use

Any delegated result, and before accepting a task.

# When not to use

Where there were no stated requirements — then the gap is upstream, and that is the finding.

# Inputs

The original request in the user's words, and the delivered artifact.

# Process

Map each requirement to evidence. Note requirements met partially, met differently, or silently dropped. Note anything delivered that nobody asked for.

# Decision rules

Scope creep is a finding too. Unrequested work is unreviewed work.

# Constraints

Compare against the user's words, not the worker's restatement of them.

# Quality checks

Can you point at evidence for every mandatory requirement? Anything without it is unverified, not done.

# Common failures

Accepting a restatement as the requirement. Missing an implicit requirement that existing behaviour survives.

# Output format

Requirement by requirement: met / partial / dropped / extra, each with evidence.

# Examples

"Add filtering" delivered filtering plus a refactor of the table component — the refactor is unrequested and unreviewed.

# Related skills

code-review · acceptance
