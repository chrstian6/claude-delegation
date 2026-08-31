---
name: requirements-analysis
description: >
  Turn a request into checkable requirements, and separate the non-negotiable ones from the rest.
agent: architect
priority: high
triggers:
  - requirements
  - what exactly
  - clarify
  - spec
  - acceptance criteria
---

# Purpose

Most failed work satisfied a requirement nobody had written down and violated one nobody had noticed. Making them explicit is what makes success measurable.

# When to use

Before planning anything at level 3 or above, and any time a request could reasonably mean two different things.

# When not to use

For a one-step request whose success is obvious. Formalizing it is ceremony.

# Inputs

The request in the user's words, and whatever the repository already implies.

# Process

Extract each requirement as a sentence that can be checked. Mark which are mandatory. Name the constraints. Name what is explicitly out of scope. Then list the ambiguities that would change the work.

# Decision rules

Minor ambiguity is resolved with a stated assumption. Ambiguity that changes safety, scope, architecture, cost or the expected result is not guessed — it is asked.

# Constraints

Never invent a requirement. Never silently narrow one because it looks hard. If you drop something, say you dropped it.

# Quality checks

Can each requirement be checked by a command, a file, or an observation? If it can only be judged, say so explicitly.

# Common failures

Turning a wish into three requirements the user never asked for. Missing the implicit requirement that existing behaviour keeps working.

# Output format

Numbered requirements, mandatory ones marked, constraints, out-of-scope, open questions.

# Examples

"Make the dashboard faster" — the checkable version names a metric, a route and a threshold, or admits it has none and says what it would take.

# Related skills

architecture-analysis · tradeoff-analysis · acceptance
