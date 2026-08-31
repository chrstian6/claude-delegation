# Policy

Version-controlled. Amended only by a human, or by a human accepting a proposal from
`review_outcomes.py`. Every change is a commit — that commit *is* the versioning and the rollback.

Read at session start. Overrides `ORCHESTRATOR.md` defaults where they conflict.

---

## Model map

Verify these IDs resolve in your harness before relying on them. Referencing tiers by role means a
model upgrade is a one-line change here, not a prompt rewrite.

```yaml
fast:   claude-haiku-4-5
mid:    claude-sonnet-5
strong: claude-opus-5
```

## Routing rules

Format: `WHEN <condition> THEN <action>  # evidence: <n> outcomes, added <date>`

```
WHEN task touches migrations OR deletes data     THEN risk=high, checkpoint, confirm
WHEN 2 repair attempts fail                      THEN escalate to strong for diagnosis only
WHEN subtask is extraction/formatting/reporting  THEN fast, no delegation
WHEN change is single-file and reversible        THEN direct, no subagent
# --- add your own below; each carries its evidence count ---
```

## Project constraints

Facts about THIS codebase that route decisions. Keep short and true.

```yaml
package_manager:  <npm | pnpm | uv | cargo | go>
test_command:     <e.g. npx vitest run>   # REQUIRED — verify.sh cannot run without it
typecheck:        <e.g. npx tsc --noEmit>
lint:             <e.g. npx eslint .>
framework:        <one line: what this is built on>
protected_paths:                          # protect-files.sh reads these
  - .claude/hooks/**
  - .claude/settings.json
no_touch:         [".env", ".env.*", "*.pem", "secrets/"]
```

## Invariants

Things that do not move, in one line each. A reviewer checks against these.

```
- Nothing merges that a single agent both wrote and approved.
- Only the orchestrator runs git.
- <yours>
```
