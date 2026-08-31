---
name: adversarial-review
description: >
  Attempt to disprove the result rather than confirm it.
agent: reviewer
priority: critical
triggers:
  - adversarial
  - try to break
  - disprove
  - challenge
  - stress the claim
---

# Purpose

Confirmation is the default posture and it approves broken work. The only reliable correction is to start from the assumption that the result is wrong.

# When to use

Any high-risk or high-consequence work, and any result that seems obviously fine.

# When not to use

Trivial reversible changes where the review would cost more than the defect.

# Inputs

The claim, the evidence for it, and the assumptions underneath it.

# Process

Ask what would have to be true for this to be wrong, then look for exactly that. Attack the strongest claim, not the weakest. Re-run the evidence yourself.

# Decision rules

The tests passing and the tests being able to fail are different claims. Check the second.

# Constraints

The freeze cannot catch an assertion that was weak before it was frozen — that judgment is yours, and it is the main reason this role exists.

# Quality checks

Did you find nothing because there is nothing, or because you were looking for confirmation?

# Common failures

Reviewing what the author documented. Accepting a green suite without asking what it covers. Manufacturing a nitpick to look diligent.

# Output format

What you attacked, what survived, what did not, and what remains unverified.

# Examples

A green test suite where the new test asserts a truth that held before the feature existed — passes, proves nothing.

# Related skills

code-review · test-quality-review · security-review
