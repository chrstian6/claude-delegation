---
name: research-method
description: >
  Structure an investigation so its conclusion can be checked by someone who was not there.
agent: researcher
priority: high
triggers:
  - research
  - investigate
  - find out
  - look into
  - survey
---

# Purpose

Research that cannot be retraced is an opinion with citations. The method is what makes the conclusion inspectable.

# When to use

Any question whose answer is not already in the working set — external comparisons, unfamiliar libraries, how a subsystem behaves.

# When not to use

When one grep answers it. Say so; over-delegating a lookup is a cost the whole system pays.

# Inputs

The question in precise form, and what would count as a satisfying answer.

# Process

Search wide before reading deep: glob for shape, grep for the symbol, read only what survives. For external questions, prefer primary sources over summaries of them. Record what you searched, not just what you found.

# Decision rules

Separate what you saw from what you infer. A file existing is a fact; what it does at runtime is a hypothesis until something runs it.

# Constraints

Never assert a dependency capability from memory — grep the installed package. Never present an empty or off-topic search as if it returned data.

# Quality checks

Could another person retrace this from your notes and reach the same conclusion? If the searches are not listed, no.

# Common failures

Reading the first plausible result and stopping. Reporting absence without saying what was searched. Citing a summary as a primary source.

# Output format

`ANSWER / EVIDENCE (file:line or URL + date) / SEARCHED / NOT FOUND / UNSURE`.

# Examples

"Does this repo have rate limiting?" — searched three patterns across two directories, found it in one middleware, named the file and line.

# Related skills

source-verification · evidence-synthesis · comparison
