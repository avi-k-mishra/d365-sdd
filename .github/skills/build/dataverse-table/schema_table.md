# schema_table — Dataverse table

Canonical how-to for a Dataverse **table** (entity). This file is both the
Stage-3 authoring reference and the Stage-4 `patterns/schema_table.md` build
pattern.

## Required payload

From `conventions.yml` `component_type_payloads.schema_table`:

| Field | Meaning |
| --- | --- |
| `name` | Logical display name (with publisher prefix on the schema name). |
| `ownership` | `user_team` (owned) or `organization`. |
| `primary_name` | The primary name column label/logical name. |
| `columns` | The initial column set (each detailed as a `schema_column`). |
| `satisfies` | `[REQ-####]` the table traces to. |

Always also state whether the table is **new** or an **existing/OOB** table
being extended (extend before you create).

## Decision guide

- **New table vs extend OOB.** Prefer extending an OOB table (Case, Account,
  Contact, …) when the concept already exists. Create a new table only for a
  genuinely new business entity. Record the choice.
- **Ownership.** Use `user_team` when row-level security / assignment / queues
  matter (most transactional data). Use `organization` for reference/config data
  shared org-wide with no per-row access needs.
- **Activity vs standard.** Make it an activity table only if it represents a
  time-stamped interaction that belongs on the timeline; otherwise standard.
- **Primary name.** Pick a human-meaningful primary column; if the natural key
  is a code/number, still provide a readable primary name and add a
  `schema_key` for the code.
- **Auditing.** Enable table auditing when any column is compliance-relevant
  (pairs with a `config_audit` component).

## Naming

- Schema name = `<prefix>_<entity>` (singular, e.g. `cr_escalation`).
- Display name singular, plural set correctly.
- Do not encode type/module into the name; the `component_type` already does.

## Anti-patterns

- Creating a new table for something an OOB table already models.
- `organization` ownership on transactional data that needs assignment/queues.
- A "misc"/EAV catch-all table with generic `attribute`/`value` columns.
- Authoring in the `default` publisher (unmanaged sprawl).
- Table with no alternate key when it is integrated/imported (add `schema_key`).

## Validation checklist

- [ ] `ownership`, `primary_name`, `columns`, `satisfies` all declared.
- [ ] New-vs-existing decision stated.
- [ ] Publisher prefix applied.
- [ ] Each column listed also appears as a `schema_column` component.

## Stage-4 build mapping

Table → solution component (metadata) authored via Dataverse (maker portal /
`pac solution` / Web API). Verified by solution-checker + Stage-5 tests that the
`satisfies` acceptance criteria pass.
