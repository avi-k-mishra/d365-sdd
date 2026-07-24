# schema_relationship — Dataverse relationship

Canonical how-to for a Dataverse **table relationship**. Stage-3 reference and
Stage-4 `patterns/schema_relationship.md`.

## Required payload

From `conventions.yml` `component_type_payloads.schema_relationship`:

| Field | Meaning |
| --- | --- |
| `name` | Relationship (schema) name with publisher prefix. |
| `relationship_type` | `one_to_many` (1:N), `many_to_one` (N:1), or `many_to_many` (N:N). |
| `related_table` | The other table in the relationship. |
| `satisfies` | `[REQ-####]` the relationship traces to. |

State the **primary (one)** and **related (many)** tables explicitly, and the
cascade behaviour.

## Decision guide

- **1:N vs N:N.** Use 1:N when a child belongs to exactly one parent (adds a
  Lookup on the child). Use native N:N only for a pure link with no attributes;
  if the link needs its own fields/dates/status, model a manual intersect
  **table** (two 1:N) instead — a `schema_table` component.
- **Cascade behaviour.** Choose deliberately per action (Assign, Share, Delete,
  Reparent): `Cascade`, `Cascade Active`, `Cascade User-Owned`, `Restrict`,
  `Remove Link`. Default new custom parents to `Restrict` delete unless the child
  is meaningless without the parent.
- **Required vs optional Lookup.** A required Lookup enforces the parent at
  create time; make it optional if rows can exist before assignment.
- **Reuse existing relationships** (e.g. Account↔Contact) before adding new ones.

## Naming

- Schema name `<prefix>_<primary>_<related>`; clear role for self-referential
  relationships (e.g. `parent`/`child`).

## Anti-patterns

- Native N:N when the link needs attributes → data becomes unqueryable/untidy.
- `Cascade` delete on a shared reference parent (accidental mass deletes).
- Duplicate relationship where an OOB one already exists.
- Circular required Lookups that make records uncreatable.

## Validation checklist

- [ ] `relationship_type`, `related_table`, `satisfies` declared.
- [ ] Primary/related sides and cascade behaviour stated.
- [ ] N:N-with-attributes correctly modelled as an intersect table instead.

## Stage-4 build mapping

Relationship → relationship metadata (and the Lookup column it creates on the
many side). Verified by Stage-5 tests.
