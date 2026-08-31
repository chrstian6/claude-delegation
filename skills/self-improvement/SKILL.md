---
name: self-improvement
description: >
  Turn task outcomes into validated policy changes, and refuse to call reflection learning.
agent: orchestrator
priority: normal
triggers:
  - learn
  - improve
  - policy
  - routing rule
  - lesson
---

# Purpose

Self-correction fixes this task. Self-improvement changes the next one. Only the second requires evidence, and only the second is worth the word.

# When to use

At task close, always. When proposing a policy change, which is rarer.

# When not to use

Mid-session policy edits. Nothing changes POLICY.md while work is running; that is how an unvalidated hunch becomes permanent.

# Inputs

The outcome of the task just finished, and the accumulated rows in state/outcomes.jsonl.

# Process

Log the close with `scripts/log_outcome.py`. Periodically run `scripts/review_outcomes.py`, which proposes above an evidence threshold and never applies. A human commits the change; that commit is the version and the rollback.

# Decision rules

Only VALIDATED (repeated evidence plus a successful intervention) or ESTABLISHED (validated across independent tasks) changes persistent policy. A single observation is a hypothesis.

# Constraints

Learning may strengthen safety, authorization, privacy and least privilege. It may never weaken them — that needs explicit human authorization every time.

# Quality checks

Did future behaviour actually change, and can you point at the commit? If not, nothing was learned; something was merely noticed.

# Common failures

Announcing a lesson at task end that goes nowhere. Promoting a rule from one bad experience. Letting stale rules accumulate — a rule nobody has tested since it was written is indistinguishable from noise.

# Output format

One `log_outcome.py` line per task. Policy proposals only from `review_outcomes.py`.

# Examples

Three tasks in a row fail at level 2 via direct routing: that is a pattern with an evidence count, and a candidate `WHEN` rule for POLICY.md.

# Related skills

acceptance · metrics
