---
name: skill-routing
description: >
  Select the skills a task actually needs via scripts/skills.py, and refuse to load the rest.
agent: orchestrator
priority: high
triggers:
  - which skill
  - skills
  - load
  - activate
---

# Purpose

Skills are not free. The design library alone is thousands of words, and loading it to rename a variable is context every later step pays for.

# When to use

Before dispatching any specialist, and before doing specialized work directly.

# When not to use

For trivial mechanical work. If the task is one obvious step, the skill lookup costs more than it returns.

# Inputs

The task in the user's words, and the role that will do it.

# Process

`$DELEGATION/skills.py "<task>" --role <role>`. Read what it returned and why. Load those; load nothing else.

# Decision rules

Priority resolves conflict: safety > mandatory constraint > role skill > domain skill > project skill > optional polish. Higher band wins; never merge two skills that contradict.

# Constraints

Do not activate a skill because its name sounds related. If the router returned nothing and the work is clearly specialized, say so — that is a gap in the triggers, not licence to improvise.

# Quality checks

Would a reviewer agree every loaded skill was needed? Would they spot one that was obviously missing?

# Common failures

Loading the whole role library by habit. Ignoring the router when it disagrees with a hunch, without saying so.

# Output format

The router's output verbatim, plus one line if you overrode it.

# Examples

"Compare postgres and dynamo" returns `research` alone — no design skills, which is the case that catches a router matching on vibes.

# Related skills

context-engineering · delegation
