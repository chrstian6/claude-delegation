---
name: tradeoff-analysis
description: >
  Make the cost of a choice explicit, including the cost of not choosing it.
agent: architect
priority: normal
triggers:
  - tradeoff
  - pros and cons
  - worth it
  - cost of
  - should we
---

# Purpose

Every option has a price. Listing benefits without prices is advocacy, and it produces decisions that surprise people later.

# When to use

Whenever two viable options exist and the choice is not obviously forced.

# When not to use

When one option is plainly correct. Manufacturing a tradeoff to look rigorous wastes the reader's attention.

# Inputs

The options, the constraints, and what the project actually optimizes for.

# Process

For each option: what it buys, what it costs, what it forecloses, and what it would take to reverse. Then say which you would pick and under what condition you would change your mind.

# Decision rules

Reversibility is a first-class criterion. A slightly worse decision that can be undone often beats a better one that cannot.

# Constraints

Never present a tradeoff without a recommendation. "Both have merits" hands the work back to the reader.

# Quality checks

Have you named a cost for the option you prefer? If not, you wrote an argument, not an analysis.

# Common failures

Listing only the costs of the option you dislike. Ignoring operational and maintenance cost. Treating token cost as free.

# Output format

Per option: buys, costs, forecloses, reversibility. Then the recommendation and its trigger for revision.

# Examples

Two auth approaches: one is faster to build and harder to undo; the recommendation goes to the reversible one and names the volume at which that flips.

# Related skills

architecture-analysis · comparison · risk-analysis
