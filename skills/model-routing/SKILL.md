---
name: model-routing
description: >
  Pick the cheapest model that can reliably do each SUBTASK, and escalate only on evidence.
agent: orchestrator
priority: high
triggers:
  - model
  - which model
  - haiku
  - sonnet
  - opus
  - escalate
---

# Purpose

A level-5 parent does not put every subtask on the strong model. Extraction inside a hard task is still extraction, and paying strong-model rates for it is waste that compounds across a session.

# When to use

Before each dispatch, and again when a subtask changes character.

# When not to use

As a status signal. Routing to a stronger model because a task feels important is how cost grows without quality moving.

# Inputs

The subtask, its level, and POLICY.md's model map.

# Process

Route on the subtask's own level. `fast` for extraction, classification, formatting, mechanical edits and test runs. `mid` for implementation, debugging, research, repair. `strong` for architecture, ambiguous diagnosis, adversarial review, high-risk judgment.

# Decision rules

Escalate mid→strong when two repairs fail, requirements genuinely conflict, or a decision has no clear default. De-escalate the moment the work turns mechanical.

# Constraints

Model identifiers live in POLICY.md and nowhere else, so a model change is a one-line edit rather than a prompt rewrite.

# Quality checks

Name the specific reason for any use of the strong model. "It is a complex task" is not one; "the architecture has two viable shapes and no clear default" is.

# Common failures

Inheriting the parent's model for every child. Escalating on frustration rather than on a failed attempt. Never de-escalating, so the expensive model finishes the mechanical tail.

# Output format

`<tier> for <subtask> — <one-line reason>.`

# Examples

L5 deploy task: risk analysis on strong, the config diff extraction on fast, the rollback script on mid.

# Related skills

task-classification · escalation · delegation
