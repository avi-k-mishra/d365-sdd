# bi_dataset — Power BI Semantic Model (Dataset)

The governed data model (tables, relationships, measures, RLS) that reports build
on. Stage-3 reference and Stage-4 `patterns/bi_dataset.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Semantic model name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture source tables, storage mode, key measures, and RLS roles.

## Decision guide

- **One shared model, many reports.** Build a reusable semantic model; don't
  re-model per report.
- **Import vs DirectQuery vs Direct Lake.** Choose per freshness/volume; Direct
  Lake / Link to Fabric for large near-real-time Dataverse data.
- **Row-level security** mirrors Dataverse access intent — model RLS roles
  explicitly.
- **Star schema + measures in DAX**; avoid heavy per-visual calculated columns.

## Anti-patterns

- Per-report duplicated models (governance drift).
- DirectQuery on huge tables causing slow visuals (wrong storage mode).
- No RLS where data is access-sensitive.

## Validation checklist

- [ ] `satisfies` declared (+ sources/storage/RLS once authored).
- [ ] Shared model + storage mode + RLS stated.

## Stage-4 build mapping

Power BI semantic model in a workspace (deployment pipeline). Verified by Stage-5
tests (measures compute correctly; RLS restricts as designed).
