---
name: comparison
description: >
  Evaluate options against criteria that were fixed before the options were examined.
agent: researcher
priority: high
triggers:
  - compare
  - versus
  - which is better
  - evaluate options
  - choose between
---

# Purpose

Criteria chosen after the fact are a rationalization of a preference. Fixing them first is what makes a comparison a comparison.

# When to use

Any "which should we use" question: libraries, databases, architectures, vendors.

# When not to use

When the decision is already made and only justification is wanted. Say that plainly instead of dressing it up.

# Inputs

The options, and the constraints that actually apply to this project.

# Process

Derive criteria from the project's real constraints. Score each option on each. Note what you could not evaluate. Recommend, and name the strongest argument against your own recommendation.

# Decision rules

Weight criteria by what this project actually needs, not by what is generally impressive. An option that wins on a criterion nobody here cares about has not won.

# Constraints

Never compare on features that no criterion asked about. Never omit an option's cost because it is unpleasant.

# Quality checks

Would the recommendation change if you removed the criterion you weighted highest? If not, most of the comparison was decoration.

# Common failures

Criteria that appear only where they favour the preferred option. Feature-matrix theatre. Ignoring operational cost.

# Output format

Criteria table, per-option assessment, the recommendation, the strongest counterargument, and what remains untested.

# Examples

Postgres vs Dynamo for a multi-tenant app where tenant isolation is enforced in application code — the criterion that decides it is not throughput.

# Related skills

evidence-synthesis · tradeoff-analysis
