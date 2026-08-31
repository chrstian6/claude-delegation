---
name: risk-analysis
description: >
  Classify consequences independently of difficulty, and decide what must happen before execution. Load whenever an action touches production, data, credentials, money or anything irreversible.
agent: orchestrator
priority: critical
triggers:
  - risk
  - dangerous
  - irreversible
  - production
  - destructive
  - migration
  - credentials
---

# Purpose

Difficulty asks how hard. Risk asks what happens if it goes wrong. They are independent, and risk wins — it decides whether the work needs a checkpoint, a confirmation and an independent review.

# When to use

Before executing anything that writes outside the working tree: migrations, deploys, deletions, credential handling, anything touching customer data or money.

# When not to use

Read-only work, local reversible edits, and anything a `git checkout` undoes. Applying HIGH controls to those is theatre and it teaches people to route around the controls that matter.

# Inputs

The concrete actions the task will take, not the task's description. "Update the billing page" is low risk; the migration it needs is not.

# Process

Name each action. For each: is it reversible, and by what exactly? Who is affected if it is wrong? Does it need authorization this session does not have? Then take the highest band any single action reaches.

# Decision rules

LOW reversible and local. MED shared state, integrations, user data, CI. HIGH production, credentials, migrations, deletions, money, authorization changes. HIGH requires a checkpoint, an explicit statement of what is irreversible, and user confirmation before execution.

# Constraints

Never self-authorize a destructive action. Never downgrade a risk band because the change is small — size and consequence are unrelated.

# Quality checks

Can you state, in one sentence, exactly how to undo this? If not, it is HIGH and it needs confirmation.

# Common failures

Classifying the task instead of its actions. Treating a small diff as low risk. Assuming a migration is safe because the local gate is green — merging the PR lands the SQL and does not change the database.

# Output format

`RISK <band> — irreversible: <what>. Undo: <how, or NONE>. Requires: <checkpoint | confirmation | review>.`

# Examples

"Drop the legacy leads column" — HIGH: irreversible data loss, undo is a restore from backup, requires checkpoint plus explicit confirmation plus ship:migration verification.

# Related skills

task-classification · escalation · acceptance
