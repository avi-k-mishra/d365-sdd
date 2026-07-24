---
name: power-bi-reporting
description: >-
  How to design and build Power BI analytics over Dataverse — semantic datasets
  and reports. Use for any DES component tagged bi_dataset or bi_report.
allowed-tools: [view, edit, create, grep, glob]
---

# power-bi-reporting

Reusable **HOW** for enterprise analytics/reporting on Dataverse data. Applied
both when authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `bi_dataset` | [bi_dataset.md](bi_dataset.md) |
| `bi_report` | [bi_report.md](bi_report.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload against the reference's **Required payload**
   (`_default`: name + satisfies until a specific payload is defined).
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Power BI for analytics, native charts for at-a-glance.** Cross-table trends,
  aggregation, and drill-down belong here; simple in-app visuals stay as
  `uiux_chart`/`uiux_dashboard`.
- **Dataverse connectivity.** Prefer Link to Dataverse / Fabric or the Dataverse
  connector (DirectQuery vs import chosen deliberately); avoid per-report ad-hoc
  queries.
- **One governed semantic model** (`bi_dataset`) shared by reports — don't
  re-model per report.
- **Row-level security** in the dataset mirrors Dataverse access intent; deploy via
  workspaces/deployment pipelines (ALM).
