---
name: dependency-analysis
description: >
  Turn the user's own sequencing words into explicit task dependencies, without inventing ones they did not mean.
agent: orchestrator
priority: high
triggers:
  - depends
  - then
  - after that
  - order
  - blocked
---

# Purpose

Users express order naturally — *then*, *after that*, *using what you built*, *fix what review found*. Those phrases are data. Losing them means running work whose input does not exist yet.

# When to use

At intake, whenever more than one request arrives, or a request references earlier work.

# When not to use

When the ordering is genuinely ambiguous and the guess would change execution. Then ask, or mark the task as needing clarification. An invented dependency stalls a queue as effectively as a missed one.

# Inputs

The requests in their original wording and the existing rows.

# Process

Scan for the cue phrases. Link to the specific row the phrase points at, not merely to the previous one. State the inference so it can be corrected.

# Decision rules

An inferred dependency is a guess and is reported as one. "Review the dashboard" after "build the dashboard" depends on the build; "add auth" after it usually does not.

# Constraints

Never create a cycle. Never depend on a task that does not exist. `tasks.py check` refuses both.

# Quality checks

Could these two rows run at the same time without one breaking the other? If yes, they are independent no matter what order they were typed in.

# Common failures

Chaining everything to the previous row because it was typed last. Missing that a review depends on the artifact rather than on the task that produced it.

# Output format

`TASK-00n depends_on TASK-00m — inferred from "<the phrase>"`.

# Examples

"Build the dashboard. Add authentication. Then write the tests." — the tests depend on auth; auth does not depend on the dashboard unless it touches the same files.

# Related skills

queue-management · scheduling
