---
name: root-cause-analysis
description: >
  Find the cause a fix must address, not the symptom that was reported.
agent: architect
priority: high
triggers:
  - root cause
  - why did
  - diagnose
  - what caused
  - keeps happening
---

# Purpose

A report names a symptom. Fixing the symptom leaves every sibling caller broken and guarantees the bug returns wearing different clothes.

# When to use

Before any non-trivial fix, and always when a bug has recurred.

# When not to use

For a typo or a single obvious mistake with no shared surface.

# Inputs

The failure evidence: the actual error, the reproduction, and what changed recently.

# Process

Reproduce it. Narrow to the smallest input that triggers it. Then grep every caller of the function you intend to change — the fix usually belongs where they all pass through.

# Decision rules

One guard in a shared function is a smaller diff than a guard in every caller, and it does not leave the siblings broken. The lazy fix and the root-cause fix are usually the same edit.

# Constraints

Do not fix what you cannot reproduce. An unreproduced fix is a guess with a commit message.

# Quality checks

Can you explain why it worked before, or why it never did? If neither, you have found a correlation.

# Common failures

Stopping at the first plausible cause. Patching the path the ticket named. Changing three things at once and learning nothing from the result.

# Output format

`SYMPTOM / REPRODUCTION / CAUSE (with evidence) / BLAST RADIUS (every caller) / FIX LOCATION`.

# Examples

A null crash on one page traces to a shared loader that has always returned undefined on empty — four other callers had the same latent bug.

# Related skills

debugging · minimal-fix · failure-analysis
