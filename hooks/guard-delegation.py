#!/usr/bin/env python3
"""PreToolUse hook on Task/Agent. Makes the delegation boundary a refusal.

WHY THIS EXISTS

Agent OS moved delegation limits from `permissions.deny` — engine enforced,
monotonic, not arguable — into the contract's FORBIDDEN block, which is
prompt-level. That is the same gap the test freeze had before
guard-frozen-tests.sh: a rule the model can rationalize past under pressure,
with nothing refusing the call.

WHAT WAS ACTUALLY LOST, measured on 2026-08-30 rather than assumed:

  git by a subagent    still blocked. orchestrator-only-git.sh fires INSIDE
                       subagents (it keys on agent_id) and denies every write
                       verb. Verified against the hook.
  deploy, force-push,  still blocked by engine permissions.deny rules
  destructive infra    (vercel deploy*, git push --force*, terraform destroy*,
                       prisma migrate reset*). Verified through auto-approve.
  catch-all dispatch   LOST. Agent(general-purpose) / Agent(claude) were the
                       only thing stopping a dispatch to a type that carries
                       every tool INCLUDING Agent — unbounded nesting, and a
                       subagent holding permissions no contract granted it.

So this restores that one boundary and adds the cheapest mechanical check on
contract discipline: a dispatch with no FORBIDDEN block never had limits.

WHY PYTHON AND NOT SED

The first version parsed the payload with sed. Claude Code sends JSON, and JSON
escapes non-ASCII: an en-dash spelling arrives as `general\\u2013purpose`, so a
regex sees the literal escape and the fold never happens. The matrix caught it.
Parse the payload as JSON; do not pattern-match over serialized JSON.

Exit 0 = allow. Exit 2 = block, stderr goes back to Claude as the reason.
"""
import json
import re
import sys
import unicodedata

# Types that carry `*` tools, Agent included. Matching shapes rather than the
# two known names, because the next built-in to ship with that toolset will have
# a different name and the same problem.
CATCH_ALL = {"generalpurpose", "general", "claude", "agent", "default", "assistant"}

# The project's dispatchable tiers, defined by PERMISSION rather than job title.
# This is what makes the contract's `ALLOWED:` block mechanical: the tier's
# `tools:` frontmatter is enforced by the engine, where prose is not.
#
#   researcher  Read Grep Glob WebSearch WebFetch   gathers evidence, runs nothing
#   architect   Read Grep Glob Bash                 designs and diagnoses, writes no source
#   builder     Read Edit Write Bash Grep Glob      the only role that writes source
#   tester      Read Grep Glob Bash                 runs checks, cannot edit
#   reviewer    Read Grep Glob Bash                 cannot write: creator != reviewer
#   repairer    Read Edit Write Bash Grep Glob      minimal corrective change
#
# None carries Agent, so nesting is bounded by the toolset rather than by a rule
# someone has to remember. Explore and Plan are host built-ins with no write tools.
ALLOWED_TYPES = {"researcher", "architect", "builder", "tester", "reviewer",
                 "repairer", "explore", "plan"}

# Under this, a prompt is a question, not a delegation of work.
CONTRACT_MIN_CHARS = 200


def norm(value: str) -> str:
    """The engine's subagent-name fold: NFKC, lowercase, strip separators."""
    folded = unicodedata.normalize("NFKC", value).lower()
    return re.sub(r"[\s‐-―−\-_]+", "", folded)


def block(reason: str) -> None:
    print(reason, file=sys.stderr)
    sys.exit(2)


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)                      # unparseable: not this hook's call
    if not isinstance(payload, dict):
        sys.exit(0)

    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        sys.exit(0)

    subagent = tool_input.get("subagent_type")

    # NAME A ROLE. Every check below inspects subagent_type only when it is a
    # non-empty string, so a missing, null or blank one sailed past all of them
    # and this guard exited 0 — approving a dispatch whose role nothing could
    # see. The engine resolves an absent subagent_type to a catch-all carrying
    # every tool including Agent, which is the precise thing CATCH_ALL below
    # exists to refuse; omitting the field was a way to ask for it that this
    # guard did not read as asking.
    #
    # Downstream this was worse than it looks. auto-approve-all.py's fail-closed
    # only covers a tool a deny rule actually names: with `Agent(general-purpose)`
    # in permissions.deny and no `Task(...)` rule, `Agent` with no role deferred
    # while `Task` with no role was AUTO-APPROVED. Fixing it here rather than
    # there closes both, and closes it for the engine's own path too — the guard
    # is the boundary, not the approval hook.
    if subagent is None or not isinstance(subagent, str) or not subagent.strip():
        block(
            "BLOCKED: this dispatch names no subagent_type.\n\n"
            "An absent role resolves to a catch-all carrying every tool,\n"
            "including Agent itself — no role boundary at all, and no contract\n"
            "limits anything the engine will enforce.\n\n"
            "Name the tier whose toolset already denies what your contract\n"
            "forbids:\n\n"
            "  researcher  gathers evidence; runs nothing\n"
            "  architect   designs and diagnoses; writes no source\n"
            "  builder     the only role that writes source\n"
            "  tester      runs checks; cannot edit\n"
            "  reviewer    cannot write, so creator != reviewer\n"
            "  repairer    minimal corrective change"
        )

    if isinstance(subagent, str) and norm(subagent) in CATCH_ALL:
        block(
            f"BLOCKED: '{subagent}' is a catch-all subagent type.\n\n"
            "It carries every tool including Agent, so it can spawn further\n"
            "subagents and holds permissions no delegation contract granted it.\n"
            "That is the boundary the Agent(general-purpose) deny rule enforced.\n\n"
            "Dispatch a scoped subagent and put the limits in the contract:\n\n"
            "  ALLOWED:   <the tools this task needs, and only those>\n"
            "  FORBIDDEN: <frozen test paths; deploy, migrate, push, install, delete>\n\n"
            "If a catch-all is genuinely required, say so and why before\n"
            "dispatching, so it is a judgment call in the open rather than a\n"
            "default nobody noticed."
        )

    if isinstance(subagent, str) and subagent and norm(subagent) not in ALLOWED_TYPES:
        block(
            f"BLOCKED: '{subagent}' is not a dispatchable tier in this project.\n\n"
            "Tiers are defined by permission, not by job title, because the\n"
            "`tools:` frontmatter is the only part of a contract's ALLOWED block\n"
            "the engine actually enforces:\n\n"
            "  researcher  gathers evidence; runs nothing\n"
            "  architect   designs and diagnoses; writes no source\n"
            "  builder     the only role that writes source\n"
            "  tester      runs checks; cannot edit\n"
            "  reviewer    cannot write, so creator != reviewer\n"
            "  repairer    minimal corrective change\n\n"
            "Pick the tier whose toolset already denies what your contract\n"
            "forbids. If this task genuinely needs a capability none of them has,\n"
            "that is a new tier with its own AGENT.md and its own review — not a\n"
            "one-off dispatch to something broader."
        )

    prompt = tool_input.get("prompt")
    if isinstance(prompt, str) and len(prompt) > CONTRACT_MIN_CHARS \
            and "forbidden" not in prompt.lower():
        block(
            "BLOCKED: this delegation contract has no FORBIDDEN block.\n\n"
            "CLAUDE.md's contract requires one. Without it the subagent's limits\n"
            "exist only in your intent and the engine has nothing to enforce.\n"
            "Add at minimum:\n\n"
            "  FORBIDDEN: <frozen test paths>; deploy, migrate, push, install,\n"
            "             delete; anything outside the files this task names\n\n"
            f"Prompts under {CONTRACT_MIN_CHARS} characters are exempt — those are\n"
            "queries, not delegations of work."
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
