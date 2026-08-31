---
name: task-classification
description: >
  Score a request on the nine difficulty dimensions and assign LEVEL 1-5 before any routing decision. Load at intake, before choosing a model or an agent.
agent: orchestrator
priority: critical
triggers:
  - classify
  - how hard
  - difficulty
  - level
  - scope this
---

# Purpose

Routing without classification is guessing. The level decides the model, the delegation budget and the verification depth, so it is the first decision and every later one inherits it.

# When to use

At intake for any request that is not plainly a question. Again mid-task when requirements expand, failures repeat, or the architecture turns out to be unknown.

# When not to use

A question ("why is X", "does Y exist") is not a task. Answer it. Do not classify, do not queue, do not open a branch.

# Inputs

The request in the user's own words, the files it plausibly touches, and whatever the repository already says about that surface.

# Process

Score 0-3 on each: reasoning · requirements · tools · state · uncertainty · integration · testing · risk · visual complexity. Sum: 0-4 L1, 5-8 L2, 9-14 L3, 15-20 L4, 21-27 L5. Then sanity-check the number against judgment.

# Decision rules

The score is a check on judgment, not a substitute for it. When they disagree, say which you took and why. Risk overrides the sum outright: a one-line change to a payments handler is L5 regardless of how small the diff is.

# Constraints

Never classify to justify a decision already made. Never inflate a level to buy a stronger model, and never deflate one to skip review.

# Quality checks

Can you name the specific evidence for each dimension you scored above 1? If a dimension is high only because the topic sounds important, it is not high.

# Common failures

Scoring the topic rather than the work — "authentication" is not automatically L4. Backfilling a score to match a level already chosen. Never reclassifying downward, so an expensive model stays active for mechanical work.

# Output format

`LEVEL n (score s) — <the dimensions that drove it>. RISK <low|med|high> because <reason>.` One or two lines.

# Examples

"Change the Save label to Update" scores 2 total: L1, direct, no delegation. "Redesign the dashboard to feel premium" scores 17 on visual and requirement complexity: L4, architect then builder then reviewer.

# Related skills

risk-analysis · model-routing · delegation · scheduling
