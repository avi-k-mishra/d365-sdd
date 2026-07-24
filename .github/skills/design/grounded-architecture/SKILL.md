---
name: grounded-architecture
description: >-
  How to ground every Stage 3 design decision in authoritative sources (Microsoft
  Learn MCP for capability/licensing, and the Dataverse/Copilot Studio/Azure/Bicep
  MCPs for live schema) so no D365-CE capability is asserted without evidence. Use
  whenever a design claims a product can do something.
allowed-tools: [view, edit, create, grep, glob]
---

# grounded-architecture

Reusable **HOW** for the retrieval discipline that makes a design trustworthy:
the architect owns the "how", so **every** capability claim is grounded in an
authoritative source — never invented.

## When to use

- You are authoring any part of `specs/design/DES-##.md` that asserts a product
  capability, connector limit, licensing constraint, or schema fact.
- You are validating whether a proposed approach is actually feasible on the
  Microsoft stack.

## Mechanical process (deterministic)

1. **Ground capability/feasibility in Microsoft Learn (MCP).** Product features,
   connector limits, throttling, licensing, and supported patterns are confirmed
   against Microsoft Learn before you commit to them.
2. **Ground live facts in the environment MCPs** where available — Dataverse
   (tables/columns/roles), Copilot Studio, Azure, Bicep — for real schema and
   security, not assumptions.
3. **Cite inline.** Each grounded decision carries its source so a reviewer can
   verify the "how".
4. **Never assert the ungrounded.** If a capability can't be confirmed, raise an
   open question (`open-question-handling`) or choose a grounded alternative —
   do not proceed on assumption.
5. **Feasibility lives here, not earlier.** Stage 1/2 stay solution-agnostic;
   platform feasibility is decided in Stage 3 with citations.

## Ground rules

- **No ungrounded "how".** A capability claim without a Microsoft Learn / live-
  environment citation is a Stage-3 anti-pattern.
- **Authoritative over memory.** Prefer a fresh MCP lookup to recalled knowledge;
  the platform changes fast.
- **Traceable feasibility.** Grounding citations become the evidence the architect
  reviews at Gate A.

## Anti-patterns

- Asserting a product capability, limit, or license without a citation.
- Relying on stale recalled knowledge instead of a live lookup.
- Deciding feasibility in Stage 1/2 instead of Stage 3.
