---
name: scheduling
description: >
  Decide what may run at once and what must be serialized. Load when two or more tasks are ready.
agent: orchestrator
priority: normal
triggers:
  - parallel
  - at the same time
  - concurrently
  - serialize
  - order of work
---

# Purpose

Parallelism is the cheapest speedup available and the easiest way to corrupt a working tree. The dividing line is whether two pieces of work touch the same mutable state.

# When to use

Whenever `tasks.py ready` returns more than one row.

# When not to use

For a single ready task, or when both ready tasks obviously touch the same files.

# Inputs

The ready rows and the files each will change.

# Process

For each pair: do they write the same files, the same database, the same migration, the same deploy? If none, run them together. If any, order them and say why.

# Decision rules

Parallel is safe for research, read-only analysis, independent tests and inspection. Serialize same-file edits, database mutations, migrations, deploys and destructive actions.

# Constraints

On this project, heavyweight test runs and builds are serialized by a lock regardless — five concurrent runs reproduce a documented flake where different files time out and all pass in isolation.

# Quality checks

Can you name the files each branch will touch? If not, you cannot claim they are independent.

# Common failures

Parallelizing two tasks that both edit the same component. Assuming separate agents means separate state — they share a working tree unless you gave them worktrees.

# Output format

`PARALLEL: 002, 004 — disjoint files. SERIAL: 003 after 002 — both touch lib/auth.`

# Examples

A UI review and an auth implementation run together. Two migrations never do.

# Related skills

queue-management · dependency-analysis
