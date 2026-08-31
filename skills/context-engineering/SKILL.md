---
name: context-engineering
description: >
  Give each worker the minimum useful context and get compact artifacts back. Load when packaging a dispatch or when returned context starts dominating cost.
agent: orchestrator
priority: high
triggers:
  - context
  - token
  - prompt size
  - too much context
  - package
---

# Purpose

Returned context is the dominant cost in a delegated architecture. A worker that pastes files back spends more than it saved by being a worker at all.

# When to use

Every dispatch, and whenever a session starts feeling slow or a worker returns a wall of text.

# When not to use

For a single tool call you can make yourself. Packaging costs more than the call.

# Inputs

The subtask, the files it truly needs, and the results it must return.

# Process

Include: objective, requirements, constraints, the specific file paths, relevant prior results, the skills the router named. Exclude: unrelated conversation, duplicate instructions, whole files, logs nobody will read.

# Decision rules

Paths, not contents. Results, not transcripts. Cap returns at roughly 1500 tokens and say so in the contract.

# Constraints

Never paste a whole file into a contract when a path and a line range will do. Never forward one worker's full conversation to the next.

# Quality checks

If you removed half this context, would the worker still succeed? If yes, remove it.

# Common failures

Sending the conversation as context. Asking for a summary and getting a re-derivation. Forgetting that the artifact is the interface between workers.

# Output format

The contract's CONTEXT block: paths and the minimum facts.

# Examples

Instead of the 4k-word design law, the contract names the two token files and the one component the change touches.

# Related skills

delegation · skill-routing
