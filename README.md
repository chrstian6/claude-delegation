# delegation

A six-role agent organization for Claude Code, packaged so it installs into any project.

The idea it is built on: **roles are separated by what they are allowed to do, not by what they
are asked to do.** A reviewer that holds no `Edit` tool cannot quietly fix what it finds, so a
finding has to be reported. A tester that cannot edit tests cannot make a red suite green by
moving the measurement. Those are toolset facts, not instructions a model can rationalize past.

```
architect    designs and diagnoses          read-only on source
builder      the only role that writes source
tester       runs checks, reports exit codes  cannot edit tests or implementation
reviewer     adversarial review               no write tools at all
repairer     one verified defect, minimal fix capped at 3 attempts
researcher   evidence with sources           cannot execute anything
```

There is no `orchestrator` agent — that is the main thread. None of the six carries the `Agent`
tool, so nesting is bounded by the toolset rather than by a rule, and `guard-delegation.py`
refuses any subagent type outside the six.

## What is in the box

| | |
|---|---|
| `agents/` | the six roles, with `tools:` frontmatter that is the boundary |
| `skills/` | 61 role-scoped skills, loaded per task by the router rather than all at once |
| `bin/route.py` | one call → role, model tier, risk signals, delegation budget, skills |
| `bin/skills.py` | the skill half alone; merges the project's own `.claude/skills/` on top |
| `bin/verify.sh` | the test freeze — `freeze` / `check` / `run` / `release` |
| `bin/tasks.py` | the queue, with a state machine that refuses illegal transitions |
| `bin/log_outcome.py` `metrics.py` `evaluate.py` `review_outcomes.py` | the offline learning loop |
| `bin/checkpoint.sh` `debt.sh` | git checkpoint before risky work; harvest deferred shortcuts |
| `hooks/` | the guards — frozen tests (Edit *and* Bash paths), dangerous commands, protected files, secret scan, orchestrator-only git, delegation contract |
| `CLAUDE.template.md` | **the doctrine** — classification, routing, the delegation contract, the freeze, bounded repair, acceptance. Import this into a project's `CLAUDE.md` |
| `ORCHESTRATOR.md` | the same system for hosts with no hooks (API use, other clients): the lifecycle in full plus worked examples. Run one or the other, never both |
| `POLICY.template.md` | the one file you fill in per project |

## Install

### A. As a plugin — preferred

Nothing lands in the project, and `git pull` updates every project at once.

```
/plugin marketplace add ~/claude-delegation
/plugin install delegation@delegation-marketplace
```

Then, in the project you want it to govern, create `POLICY.md` from `POLICY.template.md` and set
`test_command`. Run `/delegation-doctrine` to load the doctrine, or paste `CLAUDE.template.md`
into the project's own `CLAUDE.md` so it loads every session.

### B. As project files

When you want the system committed to the repo itself, or the host does not load plugins:

```bash
~/claude-delegation/install.sh /path/to/project
~/claude-delegation/install.sh /path/to/project --link   # symlink skills/bin instead of copying
```

It copies agents, skills, bin and hooks into `.claude/`, **merges** the hook wiring into
`settings.json` without clobbering what is there, and creates `POLICY.md` only if absent. It is
idempotent — run it again to update.

Then add one line to the project's `CLAUDE.md`:

```
@.claude/DOCTRINE.md
```

(`install.sh` puts the doctrine at `.claude/DOCTRINE.md` and the hookless build at
`.claude/ORCHESTRATOR.md`. Your project's own `CLAUDE.md` is never touched — the doctrine is
imported into it, so project facts and system doctrine stay separable.)

and export `DELEGATION="$PWD/.claude/bin"` so the doctrine's commands resolve.

## Configure: one file

`POLICY.md` in the project root is the whole per-project surface. It overrides the doctrine.

```yaml
fast:   claude-haiku-4-5      # the model map — a model upgrade is a one-line change here
mid:    claude-sonnet-5
strong: claude-opus-5

test_command:  npx vitest run  # REQUIRED — verify.sh cannot run without it
protected_paths:               # protect-files.sh reads these
  - .claude/hooks/**
```

Nothing else is required. The router, the freeze and the guards work in any language — `verify.sh`
parses pytest, jest, vitest, cargo and go output, and falls back to "unknown" rather than
inventing a number. The file-hash half of the freeze is language-independent.

## Check it works

```bash
bin/route.py "fix the failing auth test" --level 2
#   ROLE repairer (fix, failing) · MODEL mid · BUDGET 1 subagent · SKILLS debugging

bin/verify.sh freeze tests/auth.test.js   # after you have seen it fail
bin/verify.sh check                       # exit 2 if a frozen test moved
bin/tasks.py add "port the settings page" --level 3 --risk med
```

## Two deliberate omissions

**`auto-approve-all.py` ships but is not wired.** Blanket auto-approval for unattended runs is a
per-project risk decision, not a default. The file is in `hooks/`; wire it yourself if you want
it, and only behind the deny rules and guards that make it survivable.

> **Wire it at `"timeout": 60`, not the `10` every other hook here uses.** This one runs the
> other guards *in series* before it may approve anything, with its own `GUARD_TIMEOUT_S = 12`
> per guard — worst case is the Edit family at 4 × 12 = 48s. Give it a 10s outer timeout and the
> host kills it mid-guard; a killed hook emits no JSON, which reads as "defer", so it silently
> stops approving anything while looking installed the whole time. The per-guard entries stay at
> 10 because each of those runs exactly one guard.

**The gate script did not come across.** `gate.sh` in the source repo is npm/vitest-shaped —
tiered typecheck, per-slice, and merge-train checks. Porting it means writing your own tiers for
your own toolchain; `POLICY.md`'s `test_command`, `typecheck` and `lint` keys are where they hook
in.

## Skills

61 skills carry an `agent:` tag naming the role that owns them, and that tag is what makes them
packageable — the router only offers a role the skills declared for it. Project-specific and
third-party skills in the source repo were left behind on exactly that rule.

A project's own `.claude/skills/` is merged on top of the packaged library, and a project skill
with the same name overrides the packaged one rather than appearing twice. Add project skills
there; do not fork the package.

## The rule the guards exist to enforce

Write the test from the requirement, watch it fail, **freeze it**, then implement. An agent that
cannot make the code pass will otherwise make the test pass — by weakening an assertion, skipping
a case, or mocking the unit under test — and the report reads green either way. `verify.sh freeze`
takes that from an invisible move to a blocked tool call, on both the Edit path and the shell path.

A hook that blocks you is information, not an obstacle. Never edit, disable, `chmod -x`, or route
around a guard in the course of doing something else.
