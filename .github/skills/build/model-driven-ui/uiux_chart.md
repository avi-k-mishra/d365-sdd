# uiux_chart — Model-Driven Chart

A visualization bound to a table's data. Stage-3 reference and Stage-4
`patterns/uiux_chart.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_chart`:

| Field | Meaning |
| --- | --- |
| `name` | Chart display name. |
| `table` | The table the chart visualizes. |
| `series` | The measure(s) + aggregation and the category/group-by axis. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Chart follows the view.** Native charts aggregate the current view's rows —
  pair the chart with the intended `uiux_view` filter.
- **Right chart type** for the message (bar/column for comparison, line for trend,
  pie only for small part-to-whole).
- **Aggregation explicit** (count/sum/avg) and category grouping intentional.
- **Complex analytics → Power BI** (`bi_report`), not stacked native charts.

## Naming

- Name by measure + dimension (e.g. `Cases by Priority`).

## Anti-patterns

- Pie charts with many slices.
- Charts divorced from a sensible view filter.
- Forcing multi-dimensional analytics into native charts.

## Validation checklist

- [ ] `series` (measure + category), `satisfies` declared.
- [ ] Paired with an appropriate view; chart type justified.

## Stage-4 build mapping

Chart (savedqueryvisualization) in the solution. Verified by Stage-5 tests
(chart renders expected aggregation for the view).
