---
description: Route a task — role, model, risk, skills — before doing anything
argument-hint: "<the task, in the user's own words>"
---
Run the router and act on what it returns:

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/route.py" "$ARGUMENTS"
```

Read the signal behind each decision. If you disagree with the routing, say which call you took
and why — the router does not classify difficulty, that is your judgment (ORCHESTRATOR.md §3).
