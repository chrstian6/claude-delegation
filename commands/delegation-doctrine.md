---
description: Load the orchestrator doctrine — roles, routing, contracts, the freeze
---
Read and follow `${CLAUDE_PLUGIN_ROOT}/CLAUDE.template.md` for the remainder of this session. It is the operating manual for this agent organization: priorities, classification, role/skill/tool/model
separation, the delegation gate and contract, the test freeze, bounded repair, and acceptance.

Then read `POLICY.md` in the project root — it overrides the doctrine's defaults, and carries the
model map and this project's test command.

On a host with no PreToolUse hooks (API use, another client), read
`${CLAUDE_PLUGIN_ROOT}/ORCHESTRATOR.md` **instead** — it carries the full lifecycle and the
worked examples, and says the parts the guards would otherwise enforce. Run one or the other,
never both.
