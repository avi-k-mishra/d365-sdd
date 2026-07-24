# code_pcf — PowerApps Component Framework (PCF) Control

A custom code control for model-driven/canvas UI. Stage-3 reference and Stage-4
`patterns/code_pcf.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | PCF control name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture bound column/dataset, input/output properties, and
target (field vs dataset control).

## Decision guide

- **PCF only when platform UX can't express it.** Exhaust forms/views/business
  rules first; PCF for genuinely custom interaction/visualization.
- **Field vs dataset control** chosen to match the binding.
- **Solution-aware + versioned.** Ship in the solution; bump the version on change.
- **Accessible + performant.** Follow WCAG, avoid heavy bundles, no direct
  unmonitored external calls.

## Anti-patterns

- Rebuilding standard controls as PCF.
- Inaccessible/heavyweight controls.
- Non-solution-aware control (manual per-environment import).

## Validation checklist

- [ ] `satisfies` declared (+ binding/properties once authored).
- [ ] Justified over configuration; accessibility considered.

## Stage-4 build mapping

PCF control in the solution, bound to a column/dataset. Verified by Stage-5 tests
(control renders/behaves as specified).
