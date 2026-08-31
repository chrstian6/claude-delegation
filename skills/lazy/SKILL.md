---
name: lazy
description: Stop the agent from over-building. Apply the solution ladder before writing any code, prefer deletion and reuse over addition, and mark deferred shortcuts so they can be harvested later. Load this for every implementation, refactor, or "add a feature" task — it is the default posture for building, not a special mode.
agent: builder
priority: critical
triggers:
  - implement
  - build
  - feature
  - refactor
  - add
  - rewrite
  - simplify
  - cleanup
  - redesign
  - create
  - port
# Exempt from the §15 body format by design: CLAUDE.md names this skill as the
# default posture for all implementation, and its existing structure is the
# ladder itself. Adding empty §15 headings would be format for its own sake.
---

# Lazy

Adapted from [ponytail](https://github.com/DietrichGebert/ponytail) (MIT, DietrichGebert). The
ladder and the never-cut list are theirs; the precedence rules, orchestration ladder, and debt
harvesting are this system's integration.

Lazy means efficient, not careless. The best code is the code never written — it has no bugs, no
CVEs, no maintenance cost, and nobody has to read it in two years.

The failure mode this prevents: asked for a date picker, the agent installs a library, writes a
wrapper component, adds a stylesheet, and opens a discussion about timezones. The correct answer
was `<input type="date">`.

## Lazy about the solution, never about the reading

Run the ladder *after* understanding the problem, not instead of understanding it. Read the code
the change touches. Trace the actual flow. Then be lazy about what you write.

Skipping the reading to reach a smaller diff faster is not laziness, it is guessing, and it
produces a one-line change that is confidently wrong.

## The ladder

Before writing any code, stop at the first rung that holds:

```
1. Does this need to exist at all?      → no:  don't build it
2. Already in this codebase?            → yes: reuse it, don't rewrite it
3. Standard library does it?            → yes: use it
4. Native platform feature covers it?   → yes: use it
5. Installed dependency solves it?      → yes: use it
6. Can it be one line?                  → yes: one line
7. Only then                            → the minimum that works
```

Stop at the first rung that holds. Do not climb past a rung that answers the question because a
higher rung would be more interesting.

Rung 2 is the one agents skip most. Search the codebase before writing anything — a helper that
already exists is worth more than a better helper that doesn't.

## Rules

- No abstractions nobody asked for. A second use case is when you generalize, not the first.
- No new dependency if an installed one or the platform covers it.
- No boilerplate nobody asked for — no config layer, no factory, no interface with one impl.
- Deletion over addition. Boring over clever. Fewest files possible.
- Question complexity once: "do you actually need X, or does Y cover it?"

## Never lazy about

The ladder does not touch these. Cutting them is not minimalism, it is a defect:

- **Validation at trust boundaries** — anything crossing from user, network, or file into your code
- **Error handling that prevents data loss** — writes, deletes, migrations, transactions
- **Security** — authz, injection, secrets, session handling
- **Accessibility** — semantics, keyboard, labels, contrast
- **Anything explicitly requested** — see below

This list exists because "write minimal code" without it measurably drops safety guards. It is
the difference between lazy and negligent.

## The explicit-request guard

Rung 1 is aimed at work *you* invented, not work the user asked for.

You may question a requirement **once**, briefly, with a concrete alternative: "a native
`<input type="date">` covers this — want that instead of a component?" Then accept the answer.

If the user restates it, build it. Not slowly, not grudgingly, not with a smaller version that
technically compiles. Using the ladder to argue down an explicit request is scope refusal, and it
is a worse failure than over-building — the user loses the thing they came for.

## Deferred shortcuts

When you deliberately take the simple path where a fuller one exists, leave a marker:

```js
// ponytail: single retry, no backoff — add if this endpoint gets flaky
```

Format: `ponytail:` followed by what you skipped and what would trigger doing it properly.

This is not an apology comment. It is a ledger entry. `scripts/debt.sh` harvests every marker in
the repo into a list, so deferred work stays visible instead of quietly becoming permanent.

Do not mark ordinary simple code. A marker means "a fuller version exists and I chose not to build
it yet." Marking everything makes the ledger useless.

## Intensity

Set in `POLICY.md` as `lazy_mode`. Default `full`.

| Mode | Behavior |
|---|---|
| `lite` | Ladder rungs 1–2 only. Reuse and YAGNI; leaves architecture alone. Use on unfamiliar or legacy code. |
| `full` | The whole ladder. The default. |
| `ultra` | Full ladder, plus actively propose deletions of adjacent code the change makes redundant. Proposals only — never delete unasked. |
| `off` | Skill inactive. For spikes, prototypes, and teaching examples where verbosity is the point. |

`ultra` proposing deletions never becomes `ultra` performing them. Deletion is a user decision.

## Precedence

The ladder governs **whether and how much to build**. It does not override:

- **`ORCHESTRATOR.md` safety and authorization** — always higher
- **Explicit user requirements** — see the guard above
- **`skills/frontend-design`** on *how a built thing looks and behaves*. Division of labor: the
  ladder picks the native `<input type="date">` over a 400-line component; frontend-design decides
  how it is styled, labeled, and what its error state does. A styled native element is the
  intended outcome of both. When native genuinely does not cover the requirement — a range with
  blackout dates, say — rung 4 does not hold and you fall through. Do not use the ladder to ship a
  worse interface than was asked for.
- **`skills/testing`** — a test you skipped is not a deferred shortcut, it is unverified work

Where the ladder conflicts with `skills/architecture`, the ladder usually wins: both prefer boring
and fewer moving parts. If architecture genuinely needs a structure the ladder resists, that is a
signal the decision is real — make it explicitly rather than by default.

## Before returning

- Which rung did I stop at, and does a lower one actually hold?
- Did I add an abstraction, dependency, config option, or file nobody asked for?
- Does something in this codebase already do this?
- Did I cut anything on the never-lazy list?
- Did I build less than was explicitly asked for?
- Is every `ponytail:` marker a real deferral, not decoration?

If the diff is large, say why in one sentence. A large diff can be correct — it just should not be
accidental.
