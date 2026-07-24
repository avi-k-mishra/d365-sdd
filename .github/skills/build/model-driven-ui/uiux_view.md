# uiux_view — Model-Driven View

A saved query defining rows + columns for a table grid. Stage-3 reference and
Stage-4 `patterns/uiux_view.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_view`:

| Field | Meaning |
| --- | --- |
| `name` | View display name. |
| `table` | The table the view queries. |
| `filter` | Row filter criteria (FetchXML condition). |
| `columns` | Displayed columns, order, width, sort. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Public vs personal vs system.** Design components are public/system views;
  don't rely on user personal views for shared behaviour.
- **Filter server-side.** Push criteria into the view's FetchXML, not client script.
- **Sort + column widths** matter for usability — specify a default sort.
- **Related columns via link-entity** for cross-table display, but watch performance.

## Naming

- Name by audience + filter (e.g. `Active Cases — My Team`).

## Anti-patterns

- Overly wide views (dozens of columns) that hurt load and readability.
- Client-side filtering of unfiltered views.
- Relying on personal views for a shared requirement.

## Validation checklist

- [ ] `filter`, `columns`, `satisfies` declared.
- [ ] Default sort specified; server-side filter.

## Stage-4 build mapping

Saved query (public/system view) in the solution. Verified by Stage-5 tests
(view returns expected rows/columns).
