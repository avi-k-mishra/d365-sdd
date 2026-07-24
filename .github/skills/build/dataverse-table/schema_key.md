# schema_key — Dataverse alternate key

Canonical how-to for a Dataverse **alternate key**. Stage-3 reference and
Stage-4 `patterns/schema_key.md`.

## Required payload

From `conventions.yml` `component_type_payloads.schema_key`:

| Field | Meaning |
| --- | --- |
| `name` | Alternate key display name with publisher prefix. |
| `table` | The table the key is defined on. |
| `key_columns` | The column(s) forming the unique key. |
| `satisfies` | `[REQ-####]` the key traces to. |

## Decision guide

- **When you need one.** Add an alternate key whenever rows are created/updated
  from an external system by a business identifier (Upsert), or when a natural
  business uniqueness rule must be enforced (e.g. one config row per region).
- **Key columns.** Use stable, immutable business identifiers (codes/numbers).
  Do **not** key on free-text names or on values that change over time.
- **Simple vs composite.** Use the minimum set of columns that is truly unique;
  a composite key only when no single column is unique. Supported column types
  only (Text, Whole Number, DateTime, Lookup, Choice) — not Multiline/Currency.
- **Integration contract.** The alternate key is the Upsert handle for
  integrations; keep it aligned with the source system's key and never renumber.

## Naming

- Key schema name `<prefix>_<table>_<purpose>_key` (e.g. `cr_region_code_key`).

## Anti-patterns

- Keying on a display name / mutable text (breaks on rename).
- A composite key where one column already guarantees uniqueness.
- Adding a key on an unsupported column type.
- Relying on duplicate-detection rules where a hard alternate key is required
  (dup detection warns; a key enforces).

## Validation checklist

- [ ] `table`, `key_columns`, `satisfies` declared.
- [ ] Key columns are stable, unique, and of a supported type.
- [ ] Simple vs composite justified.

## Stage-4 build mapping

Key → alternate-key metadata on the table (async index build). Verified by
Stage-5 tests (Upsert by key succeeds; duplicate insert is rejected).
