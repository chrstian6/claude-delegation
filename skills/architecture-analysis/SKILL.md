---
name: architecture-analysis
description: >
  Choose a structure and record why, including what it costs and what you rejected.
agent: architect
priority: high
triggers:
  - architecture
  - structure
  - design the
  - data model
  - schema
  - how should we build
---

# Purpose

Architecture is the set of decisions that are expensive to reverse. Making them implicitly means making them badly and discovering it later.

# When to use

Multi-file features, new subsystems, data-model changes, anything where two credible shapes exist.

# When not to use

When the structure is already set and the task is to work within it. Then follow the existing pattern; inventing a second one is the actual defect.

# Inputs

The requirements, the existing structure, and the constraints that are genuinely fixed.

# Process

Read how the codebase already solves adjacent problems. Propose the smallest structure that satisfies the requirements. Name the alternative you rejected and why. Identify the seams where it will be extended.

# Decision rules

Prefer the existing pattern unless there is a stated reason. Consistency is worth more than a marginally better shape nobody else will follow.

# Constraints

Every claim is labelled fact, assumption, hypothesis or verified. An unlabelled claim in a plan is how a guess gets executed faithfully by three workers.

# Quality checks

Could someone implement this without asking you a question? If not, it is a direction, not a design.

# Common failures

Designing for imagined future requirements. Introducing a second way to do something already solved. Presenting a preference as a constraint.

# Output format

`DECISION / RATIONALE / REJECTED (and why) / CLAIMS (labelled) / SLICES / RISKS`.

# Examples

Adding an entity: the design names the table, the scoped access path, the seam for the next feature, and the assumption about volume it rests on.

# Related skills

requirements-analysis · tradeoff-analysis · component-architecture
