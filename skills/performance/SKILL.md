---
name: performance
description: >
  Make it fast enough for the machine it runs on, based on measurement rather than instinct.
agent: builder
priority: normal
triggers:
  - slow
  - performance
  - optimize
  - lag
  - bundle
  - render
---

# Purpose

Performance intuition is unreliable and performance work is easy to spend forever on. Measurement decides both what to fix and when to stop.

# When to use

When something is observably slow, or when adding work to a hot path.

# When not to use

Speculatively. Optimizing code nobody has measured is how simple code becomes unreadable for no gain.

# Inputs

The observed slowness, where it happens, and on what.

# Process

Measure first and name the number. Find the dominant cost — usually a query pattern, unbounded work, or render churn. Fix that one. Measure again and report both numbers.

# Decision rules

Fix the dominant cost, then stop. The second-largest cost is rarely worth what removing it does to the code.

# Constraints

Lazy-load anything heavy that is not above the fold. Never animate layout properties. Watch for N+1s and for a new predicate with no index.

# Quality checks

Do you have a before and an after number? Without both, you have a refactor with a performance-sounding commit message.

# Common failures

Optimizing the part that was easy to measure. Micro-optimizing render while an N+1 dominates. Claiming an improvement with no baseline.

# Output format

The measurement before, the change, and the measurement after.

# Examples

A list re-rendering on every keystroke: the fix is where the state lives, not memoizing every row.

# Related skills

motion-engineering · frontend-testing
