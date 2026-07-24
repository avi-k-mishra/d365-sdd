# uiux_form — Model-Driven Form

A form surface for creating/editing a table's records. Stage-3 reference and
Stage-4 `patterns/uiux_form.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_form`:

| Field | Meaning |
| --- | --- |
| `name` | Form display name. |
| `table` | The table the form belongs to. |
| `form_type` | Main / Quick Create / Quick View / Card. |
| `sections` | Tabs/sections and the columns they contain. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Right form type.** Main for full edit; Quick Create for fast inline capture;
  Quick View to show related-record data read-only; Card for grids/timelines.
- **Role-specific main forms** + form order rather than script-driven show/hide.
- **Business rules** for cross-field logic/visibility (declarative) before JS.
- **Sensitive columns** rely on column security (`sec_field_profile`), not layout.

## Naming

- Name by persona/purpose when multiple (e.g. `Case — Agent`, `Case — Supervisor`).

## Anti-patterns

- One mega-form for all roles with script-hidden fields.
- Form-hide treated as security.
- JavaScript where a business rule suffices.

## Validation checklist

- [ ] `table`, `form_type`, `sections`, `satisfies` declared.
- [ ] Role tailoring + declarative logic preferred.

## Stage-4 build mapping

Form in the solution (+ form order/role assignment). Verified by Stage-5 tests
(role sees expected form/fields).
