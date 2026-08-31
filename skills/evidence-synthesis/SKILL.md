---
name: evidence-synthesis
description: >
  Combine findings from several sources into one answer that keeps its disagreements visible.
agent: researcher
priority: normal
triggers:
  - synthesize
  - summarize findings
  - what did we find
  - pull together
---

# Purpose

Synthesis that hides conflict is a lie of omission. Where sources disagree, that disagreement is usually the most useful thing you found.

# When to use

After gathering from more than one source, before recommending anything.

# When not to use

With a single source. Then it is a citation, not a synthesis, and calling it one overstates the evidence.

# Inputs

The findings, each with its source and date.

# Process

Group by claim, not by source. For each claim: who supports it, who contradicts it, and which is more current or more primary. Surface conflicts explicitly rather than picking a winner silently.

# Decision rules

Weight primary over secondary, current over stale, installed over documented. When two credible sources conflict and you cannot resolve it, say so — that is a finding.

# Constraints

Never average two conflicting claims into a middle position that no source supports.

# Quality checks

Can a reader see which parts are agreed and which are contested? If everything reads as settled, you flattened something.

# Common failures

Presenting the majority view as consensus. Dropping the inconvenient source. Losing dates so staleness becomes invisible.

# Output format

Claim-by-claim, each with supporting and contradicting sources and a confidence.

# Examples

Three sources on a query pattern: two agree, the third is two major versions old — reported as agreement plus a stale outlier, not as unanimity.

# Related skills

research-method · comparison · uncertainty-analysis
