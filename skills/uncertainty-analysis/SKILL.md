---
name: uncertainty-analysis
description: >
  State what is not known, how much it matters, and what would settle it.
agent: researcher
priority: normal
triggers:
  - uncertain
  - not sure
  - confidence
  - unknown
  - risky assumption
---

# Purpose

Unstated uncertainty gets read as confidence. The reader then makes decisions your evidence does not support, and neither of you notices until it fails.

# When to use

Whenever a conclusion rests on something unverified — which is most conclusions worth writing down.

# When not to use

For claims you actually verified. Hedging verified facts is its own dishonesty and it devalues the hedges that matter.

# Inputs

The conclusion and the assumptions holding it up.

# Process

List each assumption. For each: how confident, what it would take to check, and what breaks if it is wrong. Rank by consequence, not by how uneasy it makes you.

# Decision rules

An assumption that changes the recommendation gets checked before delivering, not flagged after. An assumption that changes nothing can be noted and left.

# Constraints

Never bury a load-bearing uncertainty in a closing caveat.

# Quality checks

If the biggest assumption is wrong, does the recommendation change? If yes, it was not optional to verify.

# Common failures

Uniform hedging that gives the reader no ranking. Confident delivery with a disclaimer at the end. Treating "I did not check" and "it cannot be checked" as the same thing.

# Output format

`ASSUMPTION / CONFIDENCE / IF WRONG / TO VERIFY`, ordered by consequence.

# Examples

"Assumes the WAF still blocks data: URIs — load-bearing, checkable in one request, and the whole upload path depends on it."

# Related skills

research-method · risk-analysis
