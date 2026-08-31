---
name: frontend-engineering
description: >
  Implement UI inside the framework already present, using its idioms rather than importing new ones.
agent: builder
priority: high
triggers:
  - component
  - react
  - ui code
  - frontend
  - page
  - form
  - state
  - dashboard
  - filter
  - filtering
  - table
  - list
  - modal
---

# Purpose

Most frontend defects here are not visual. They are a component fighting the framework: state where the server already had it, a client island around a whole page, a dependency nobody verified.

# When to use

Any change to a component, page, form or layout.

# When not to use

For pure visual direction with no code — that belongs to design-taste and the reviewer.

# Inputs

The route, the components it mounts, the data it receives, and package.json.

# Process

Read the surrounding components first and match them. Prefer server components; isolate interactivity into leaf client islands. Prefer local state. Verify every import against the installed version before writing it.

# Decision rules

Do not add a state-management library because one is available. Do not introduce a second pattern for something already solved two files over.

# Constraints

This repo is Next 16 app-router with Tailwind v4, which inlines `--font-sans` into the utility at build time — redefining that variable inside a scope does nothing.

# Quality checks

Does this file look like its neighbours? A reviewer should not be able to tell which file was AI-written by its structure.

# Common failures

Making everything a client component. Hallucinating a package. Fragile flexbox percentage math where grid expresses the structure.

# Output format

Files changed with line counts, plus the gate:edit result.

# Examples

Adding a filter row: server component fetches, one client island owns the open/closed state, no new dependency.

# Related skills

component-architecture · responsive-design · frontend-testing
