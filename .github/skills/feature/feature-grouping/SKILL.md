---
name: feature-grouping
description: >-
  How to group reviewed requirements into epics and features and build the acyclic
  dependency graph for D365-CE SDD Stage 2 — writing specs/_index/features.md and
  setting feature/epic/depends_on on each REQ. Use when organising the backlog
  into features.
allowed-tools: [view, edit, create, grep, glob]
---

# feature-grouping

Reusable **HOW** for turning a flat, refined REQ backlog into a structured
Epic → Feature → REQ hierarchy with a clean dependency graph — the unit that
Stage 3 designs against (one `FEAT-##` ↔ one `DES-##`).

## When to use

- The REQs are refined and you are organising them into features/epics.
- You need to set or verify `feature`, `epic`, or `depends_on` on REQs.

## Mechanical process (deterministic)

1. **Group by cohesive capability.** Cluster REQs that deliver one feature; group
   related features under an epic. A feature is the unit of design.
2. **Write `specs/_index/features.md`** as the Epic → Feature → REQ map
   (`FEAT-%02d`, `EPIC-%02d` per `conventions.yml`).
3. **Set membership on each REQ.** Stamp `feature` and `epic` on every in-scope
   REQ so membership is discoverable from both directions.
4. **Complete `depends_on` into an acyclic graph.** Record real dependencies
   between REQs; ensure there are **no cycles**.
5. **No orphans.** Every reviewed REQ belongs to exactly one feature; every
   feature to an epic.

## Ground rules

- **Feature = unit of design.** Group so each `FEAT-##` maps 1:1 to a future
  `DES-##`; avoid features too large to design as one solution.
- **Acyclic dependencies.** `depends_on` must form a DAG — a cycle is a
  validation failure.
- **Bidirectional membership.** The index and the REQ front-matter agree on
  feature/epic assignment.
- **Derived intake trail.** Features carry no `intake_batch`; provenance derives
  through `member_reqs`.

## Anti-patterns

- Orphan REQs (no feature) or orphan features (no epic).
- Dependency cycles in `depends_on`.
- A feature so broad it can't be designed as a single `DES-##`.
- Index and REQ front-matter disagreeing on membership.
