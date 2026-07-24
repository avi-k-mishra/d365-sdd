---
name: decision-axes
description: >-
  How to record all ten architect decision axes with grounded, declarative-first
  rationale in a D365-CE SDD Stage 3 DES-##.md. Use when authoring the
  FILL:decisions zone of a design (logic_tier, data_residency, alm_boundary,
  security, integration, environment, ux_surface, observability, batch_processing,
  reporting).
allowed-tools: [view, edit, create, grep, glob]
---

# decision-axes

Reusable **HOW** for the architect's ten decision axes — the encoded judgment
that turns an approved feature spec into a solution shape on the Microsoft stack.

## When to use

- You are filling the `FILL:decisions` zone of `specs/design/DES-##.md`.
- You need to choose a logic tier or justify an escalation past config.

## The ten axes

`logic_tier`, `data_residency`, `alm_boundary`, `security`, `integration`,
`environment`, `ux_surface`, `observability`, `batch_processing`, `reporting`
(`conventions.yml` `decision_axes`).

## Mechanical process (deterministic)

1. **Record all ten axes** — none omitted. (Legacy designs in
   `conventions.yml` `legacy_designs` may hold to `decision_axes_baseline`; new
   designs record the full ten.)
2. **Declarative-first for `logic_tier`.** Choose in order
   `config → low_code → pro_code` (`logic_tiers`). Any `low_code`/`pro_code`
   choice **must** carry a recorded rationale (`escalation_requires_rationale`)
   — a silent escalation fails.
3. **Ground every non-trivial choice.** Cite Microsoft Learn (capability,
   connector limits, licensing) or the live environment — see the
   `grounded-architecture` skill. Never assert an ungrounded capability.
4. **Least-privilege on `security`.** Grant the minimum roles / field-level
   security the feature needs; carry each source-REQ NFR over unchanged.
5. **Defer nothing silently.** Any axis that can't be decided becomes an open
   question (`open-question-handling`), not an assumption.

## Ground rules

- **Config beats code.** Reach for `low_code`/`pro_code` only with a grounded
  reason; the default is declarative.
- **Grounded rationale, not opinion.** Every escalated or non-trivial axis cites
  a source.
- **Complete.** All ten axes appear; missing axes fail validation for
  non-legacy designs.

## Anti-patterns

- Silent pro-code — escalating without a recorded, grounded rationale.
- Omitting an axis on a non-legacy design.
- Over-broad security beyond least-privilege.
- Ungrounded capability claims.
