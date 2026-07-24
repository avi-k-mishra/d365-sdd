---
name: requirement-refinement
description: >-
  How to elevate the reviewed atomic REQ set into a complete, consistent, testable
  baseline for D365-CE SDD Stage 2 — enriching front-matter, attaching structured
  NFRs, and de-duplicating across the whole backlog. Use when refining REQs on a
  `feature-spec` issue.
allowed-tools: [view, edit, create, grep, glob]
---

# requirement-refinement

Reusable **HOW** for the "refine" step of Stage 2. You take the human-reviewed
`specs/requirements/REQ-####.md` set and make it complete, consistent, and
testable — without ever touching `intake/` or inventing facts. Read
`conventions.yml` first.

## When to use

- You are assigned a `feature-spec` issue and are enriching or reconciling REQs.
- You need to attach NFRs or resolve duplicates/conflicts across the backlog.

## Mechanical process (deterministic)

1. **Enrich the front-matter.** For every in-scope REQ add the missing fields:
   `title`, `type` (`conventions.yml` `requirement_types`), `module`
   (`modules`), `priority` (MoSCoW `priorities`), `status: reviewed`. Preserve
   **all** existing provenance (`source_file`, `intake_batch`, `location`,
   `author`, `sha256`, `confidence`).
2. **Attach structured NFRs.** Turn latency/throughput/availability needs into
   `nfr: [{ metric, target }]` objects drawn from `conventions.yml`
   `nfr_categories` — never free prose like "should be fast".
3. **Read the whole backlog at once** before editing, so consistency is global.
4. **De-duplicate.** Merge or link duplicates, **keeping every provenance
   source**. Never drop a source when merging.
5. **Surface conflicts.** Where two REQs disagree, raise a new open question
   (see the `open-question-handling` skill) — never silently pick a winner.

## Ground rules

- **Preserve provenance forever.** Refinement adds fields; it never removes a
  `source_file`/`intake_batch`/`sha256`.
- **Structured NFRs only.** Every non-functional target is a `{ metric, target }`
  from the sanctioned categories.
- **No platform feasibility.** Whether D365 *can* do it is a Stage-3 call; keep
  refinement solution-agnostic and evidence-grounded.
- **Forward-only status.** Move REQs along `conventions.yml` `status_flow`
  (`draft → reviewed → approved …`); never regress.

## Anti-patterns

- Free-text NFRs ("fast", "scalable") instead of `{ metric, target }`.
- Dropping a provenance source when merging duplicates.
- Silently resolving a conflict instead of raising an open question.
- Asserting that the platform can/can't do something.
