---
name: spec-compilation
description: >-
  How to compile one feature spec per feature in D365-CE SDD Stage 2 — authoring
  only the FILL zones, running scripts/compile_specs.py to generate the
  hash-guarded COMPILER zones, and freezing an approved baseline. Use when
  creating/updating a FEAT-##.spec.md or freezing a baseline.
allowed-tools: [view, edit, create, grep, glob]
---

# spec-compilation

Reusable **HOW** for the hybrid spec generator: a deterministic compiler writes
the traceability/scenario/NFR/dependency/provenance zones VERBATIM from the
member REQs, and you author only the reasoning (FILL) zones. Follow
`.github/prompts/spec-authoring.prompt.md`.

## When to use

- You are compiling or updating `specs/features/FEAT-##.spec.md`.
- You are freezing an approved requirements baseline for a Gate 2 review.

## Mechanical process (deterministic)

1. **Create the spec skeleton.** For each `FEAT-##`, write
   `specs/features/FEAT-##.spec.md` with front-matter (`id`, `title`, `epic`,
   `member_reqs`, `status`, placeholder `spec_hash`) and the
   `<!-- COMPILER:BEGIN x -->…<!-- COMPILER:END x -->` /
   `<!-- FILL:x -->…<!-- /FILL -->` zone markers.
2. **Author ONLY the FILL zones** — `intent`, `scope` (In/Out), `grounding`
   (member REQ ids + recorded decisions), `open-decisions` (deferred to Stage 3,
   or `None`). Trace to the REQs; never restate or invent.
3. **Never hand-write COMPILER zones or `spec_hash`.** Run
   `python scripts/compile_specs.py`; it fills the traceability / scenarios / NFR
   / dependency / provenance zones verbatim from member REQs and computes the
   hash. Re-run after **any** REQ change.
4. **Verify.** `python scripts/compile_specs.py --check` and
   `python scripts/validate_specs.py` must both pass.
5. **Freeze the baseline.** When every REQ is complete/consistent and every
   feature compiles, flip REQs to `status: approved`, write
   `specs/_baseline/reqs-baseline-vN.md` (ids + sha256 + approver + date), and
   open a PR `Feature-spec: baseline vN`. **Do not merge** — Gate 2 review.

## Ground rules

- **FILL zones are yours; COMPILER zones are the compiler's.** Editing a COMPILER
  zone or `spec_hash` by hand is a hash-guard failure.
- **Idempotent round-trip.** Re-running the compiler after a REQ edit must be the
  only way COMPILER content changes.
- **Human merges gates.** The agent opens the baseline PR; the customer +
  architect merge at Gate 2.

## Anti-patterns

- Hand-writing or editing a `COMPILER` zone or `spec_hash`.
- Writing outside a `FILL` zone.
- Freezing a baseline while an open question remains unresolved.
- Approving REQs without a passing compile + validate.
