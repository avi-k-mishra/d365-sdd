# schema_choice — Dataverse choice (option set)

Canonical how-to for a Dataverse **choice / option set**. Stage-3 reference and
Stage-4 `patterns/schema_choice.md`.

## Required payload

From `conventions.yml` `component_type_payloads.schema_choice`:

| Field | Meaning |
| --- | --- |
| `name` | Choice display name with publisher prefix. |
| `options` | The labels and their integer values. |
| `satisfies` | `[REQ-####]` the choice traces to. |

State whether it is a **global** (reusable) or **local** (single-column) choice,
and whether it is single- or multi-select.

## Decision guide

- **Global vs local.** Use a **global** choice when the same value set is used by
  more than one column/table (define once, reuse). Use local only for a truly
  one-off list.
- **Choice vs Lookup vs Boolean.** Choice = small, fixed, stable list managed by
  makers. If the list grows/changes at runtime or needs its own attributes →
  Lookup to a table. If exactly two mutually exclusive states → Boolean column,
  not a choice.
- **Stable integer values.** Assign explicit, meaningful, **immutable** integer
  values (respect the publisher option-value prefix). Never renumber existing
  options — integrations and rollups depend on the value, not the label.
- **Multi-select** only when a row genuinely holds several values at once;
  otherwise single.

## Naming

- Choice schema name `<prefix>_<concept>`; option labels concise and
  business-facing; avoid embedding the value in the label.

## Anti-patterns

- Choice for an open/growing list that should be a Lookup table.
- Two-option choice where a Boolean is correct.
- Reusing/renumbering existing option integer values (breaks data + integrations).
- Duplicating a global choice locally per column.

## Validation checklist

- [ ] `options` (label + stable integer value) and `satisfies` declared.
- [ ] Global-vs-local and single-vs-multi decided.
- [ ] Not a case that should be Boolean or Lookup instead.

## Stage-4 build mapping

Choice → (global) option set metadata or a local choice on its column. Verified
by Stage-5 tests.
