---
name: design-compilation
description: >-
  How to compile a Stage 3 design in D365-CE SDD — authoring only the FILL zones of
  DES-##.md (and UX-##.md where user-facing), running scripts/compile_design.py for
  the hash-guarded COMPILER zones, and passing Gate A/B. Use when creating a
  DES-##/UX-## or preparing a design PR.
allowed-tools: [view, edit, create, grep, glob]
---

# design-compilation

Reusable **HOW** for the hybrid design generator: the deterministic compiler
writes the traceability (FEAT←REQ←INTK), NFR carry-over, and provenance zones
VERBATIM and computes `spec_hash`; you author only the reasoning (FILL) zones.
Follow `.github/prompts/design-authoring.prompt.md` templates verbatim.

## When to use

- You are creating or updating `specs/design/DES-##.md` (and `specs/ux/UX-##.md`
  where the feature is user-facing).
- You are preparing the design PR for Gate A/B review.

## Mechanical process (deterministic)

1. **Use the templates verbatim** — every `COMPILER` and `FILL` marker from the
   prompt file. `DES-##` / `UX-##` are zero-padded, sequential
   (`des_id_format` / `ux_id_format`); `satisfies` **must equal** the feature's
   `member_reqs`.
2. **Author ONLY the FILL zones** — decisions (10 axes; see `decision-axes`),
   security, observability (see `observability-design`), and the typed component
   list (see `component-decomposition`). Leave COMPILER bodies empty.
3. **Author the UX spec** where the feature is user-facing — `specs/ux/UX-##.md`
   captures the experience the **customer** signs off at Gate B (not the
   architect).
4. **Close every open question** with a recorded human decision
   (`open-question-handling`); **no `- [ ]` may remain** before Gate A/B.
5. **Compile, never hand-write COMPILER zones.** Run
   `python scripts/compile_design.py` (fills traceability / NFR carry-over /
   provenance + `spec_hash`); re-run after any change.
6. **Verify + open PR.** `python scripts/compile_design.py --check` and
   `python scripts/validate_design.py` must pass; open a PR
   `Design: FEAT-## <name>`. **Do not merge** — architect reviews DES at **Gate
   A**, customer reviews UX at **Gate B**.

## Ground rules

- **FILL is yours; COMPILER is the compiler's.** Never hand-write a COMPILER zone
  or `spec_hash` (hash-guarded).
- **Two gates, two owners.** Architect owns DES (Gate A); customer owns UX
  (Gate B) — never skip the UX gate.
- **Green before PR.** Compile-check + validate pass before the PR opens.

## Anti-patterns

- Hand-writing or editing a `COMPILER` zone or `spec_hash`.
- Writing outside a `FILL` zone.
- Leaving an unresolved `- [ ]` before a gate.
- Skipping the UX (Gate B) sign-off for a user-facing feature.
- `satisfies` not matching the feature's `member_reqs`.
