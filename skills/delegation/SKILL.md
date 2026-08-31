---
name: delegation
description: >
  Decide whether to spawn a subagent at all, and which role. Load before every dispatch. Answers the question the delegation gate asks: does this pay for itself?
agent: orchestrator
priority: high
triggers:
  - delegate
  - subagent
  - specialist
  - parallel
  - who should
---

# Purpose

Delegation is context management, not difficulty avoidance. A subagent costs tokens, latency and a handoff where information is lost. It earns that back only in specific conditions.

# When to use

When there is bulk you do not want to carry, when independence matters (verification, review), or when two pieces of work can genuinely run at once.

# When not to use

Because a task is hard. Hard work you understand is work you should do. If you could not check the result, you are not ready to delegate it.

# Inputs

The subtask, its files, and an honest estimate of what carrying it yourself would cost in context.

# Process

Answer four questions: can I do this reliably right now; does a separate context window help; does independence matter; can it run in parallel. Delegate only on a yes to one of the last three.

# Decision rules

Budget by level: L1 zero, L2 zero to one, L3 one to two, L4 two to four, L5 only what is justified. Exceeding the budget means reclassifying, not quietly adding another agent. Prefer direct → script → skill → one specialist → parallel.

# Constraints

A deterministic script beats an LLM for anything repeatable. Never delegate a test run — that is `fast` work the orchestrator does directly.

# Quality checks

For each subagent you are about to spawn: what does it know that you do not, or what does it carry that you do not want to? If the answer is neither, do it yourself.

# Common failures

Delegating to look thorough. Spawning three agents where one would do. Passing a whole conversation as context. Delegating the judgment and keeping the mechanical part.

# Output format

`DELEGATE <role> because <which of the four>. Budget: n of m.` Or `DIRECT — <why delegation does not pay>.`

# Examples

"Rename usr to user in one file" — direct, no subagent. "Review this diff for authorization flaws" — reviewer, because independence is the whole point.

# Related skills

queue-management · context-engineering · model-routing
