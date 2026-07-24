# uiux_dashboard — Model-Driven Dashboard

An at-a-glance surface composing charts, lists, and iframes/web resources. Stage-3
reference and Stage-4 `patterns/uiux_dashboard.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_dashboard`:

| Field | Meaning |
| --- | --- |
| `name` | Dashboard display name. |
| `components` | The tiles — charts, list/stream views, web resources — and their layout. |
| `roles` | Which security roles the dashboard is enabled for. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Interactive vs classic.** Use interactive dashboards for stream/tile
  drill-down scenarios (service); classic for simple chart/list composition.
- **Reuse existing views/charts** as tiles rather than re-defining queries.
- **Role-enable** the dashboard so each persona sees the relevant one by default.
- **Power BI embedding** → prefer a `bi_report` component for heavy analytics, not
  a dozen native charts.

## Naming

- Name by persona/purpose (e.g. `Supervisor Overview`).

## Anti-patterns

- Cramming analytics that belong in Power BI into native charts.
- No role enablement (everyone sees everything).
- Duplicating queries instead of reusing views/charts.

## Validation checklist

- [ ] `components`, `roles`, `satisfies` declared.
- [ ] Reuses existing views/charts; role-enabled.

## Stage-4 build mapping

Dashboard in the solution (+ role enablement). Verified by Stage-5 tests
(role sees expected dashboard/tiles).
