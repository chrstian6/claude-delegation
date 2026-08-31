---
description: Freeze test files after RED, so implementation cannot edit them
argument-hint: "<test file paths>"
---
The test must already be RED. Record the failure message first, then:

```bash
"${CLAUDE_PLUGIN_ROOT}/bin/verify.sh" freeze $ARGUMENTS
```

The frozen paths are now FORBIDDEN to every writing role. Implement source only, then
`verify.sh run` for GREEN plus the tamper and count-drop check.
