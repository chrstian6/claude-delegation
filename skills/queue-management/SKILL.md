---
name: queue-management
description: >
  Own TASKS.md through scripts/tasks.py: turn requests into rows, move states legally, and report the compact non-done view.
agent: orchestrator
priority: high
triggers:
  - queue
  - tasks
  - backlog
  - status
  - what is running
---

# Purpose

The queue survives context compaction; your context window does not. A queue held only in the conversation is one the user has to re-ask for, and on this project they did — twice in one session.

# When to use

Whenever a request arrives that is not a plain continuation of the running task, and whenever a task changes state.

# When not to use

For a single-step continuation of work already running. Adding a row for every sub-step turns the queue into noise and hides the rows that matter.

# Inputs

The request, the currently running task, and TASKS.md.

# Process

`$DELEGATION/tasks.py add "<request>" --level n --risk r`, then move it with `state <id> <state>` as work progresses. `ready` before starting anything, `show` when reporting.

# Decision rules

Every actionable request becomes a row before the first dispatch, not after the work is done. Report status as the non-done view only. Never hand-edit the table — the script enforces the state machine.

# Constraints

A task cannot reach `completed` without `final_validation` or `reviewing`. A task cannot go `running` with an unmet dependency. Both are refusals, not conventions.

# Quality checks

Does the queue reflect what a fresh session would need to continue? If the answer lives only in your context, it is not written down yet.

# Common failures

Batching the writes to the end, which produces a changelog rather than a queue. Marking done at merge rather than at verification. Leaving a `waiting_dependency` row that nothing will ever free.

# Output format

The `show` table, filtered to non-done rows, and nothing else.

# Examples

Five requests in one message become five rows with dependencies inferred from *then*, *after that*, *fix what review found*.

# Related skills

dependency-analysis · scheduling · task-classification
