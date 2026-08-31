---
name: escalation
description: >
  Change the right component when something fails, rather than retrying the same thing harder.
agent: orchestrator
priority: high
triggers:
  - escalate
  - stuck
  - failed again
  - not working
  - give up
---

# Purpose

Blind retry is the most expensive failure mode available: it costs a full attempt and teaches nothing. Something specific was wrong, and naming it is the whole job.

# When to use

After a failed attempt, and mandatorily at the repair cap of three attempts or two strategy changes.

# When not to use

On the first failure of a mechanical task with an obvious cause. Fix it and move on.

# Inputs

The actual error, what was attempted, and what has already been ruled out.

# Process

Identify which component failed: model, role, skill, context, tool, assumption, contract, or strategy. Change that one. Retrying with the same context changes nothing.

# Decision rules

Escalate in the smallest scope that fixes it. A hard diagnosis goes to the strong model; the implementation that follows does not have to.

# Constraints

At the cap: stop. Report what failed, what was tried, what was ruled out, and what you now believe. Never quietly widen scope to route around a problem.

# Quality checks

Can you name which component you are changing and why? "Try again with Opus" is not an escalation, it is a hope.

# Common failures

Replacing the entire workflow with the strong model. Escalating without a hypothesis. Continuing past the cap because the fix feels close — attempt three is exactly where the forbidden shortcuts start looking reasonable.

# Output format

`ESCALATE <component>: <what was wrong> → <what changes>.`

# Examples

Two repairs fail on an auth test: the diagnosis moves to the strong model, the fix stays on mid.

# Related skills

model-routing · debugging · acceptance
