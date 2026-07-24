# bi_report — Power BI Report

A report (pages/visuals) built on a `bi_dataset`, optionally embedded in a
model-driven app. Stage-3 reference and Stage-4 `patterns/bi_report.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Report name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture the source `bi_dataset`, pages/visuals, audience, and
embedding surface.

## Decision guide

- **Report binds to the shared dataset** (`bi_dataset`), never its own private
  model — one source of truth.
- **Audience-scoped pages**; rely on the dataset's RLS for data security, not visual
  hiding.
- **Embed thoughtfully.** Power BI embedded in a model-driven dashboard/form for
  in-context analytics; standalone in a workspace/app otherwise.
- **Performance.** Reasonable visual counts per page; push aggregation into
  measures.

## Anti-patterns

- Report with its own embedded model instead of the shared dataset.
- Treating visual-level filters as security (use dataset RLS).
- Overloaded pages harming performance.

## Validation checklist

- [ ] `satisfies` declared (+ dataset/pages/audience once authored).
- [ ] Bound to a shared dataset; RLS-based security; embedding surface stated.

## Stage-4 build mapping

Power BI report in a workspace (deployment pipeline) + optional app embedding.
Verified by Stage-5 tests (report renders expected data per audience/RLS).
