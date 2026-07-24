---
name: dataverse-table
description: >-
  How to design and build the Dataverse data model for a D365-CE solution:
  tables, columns, relationships, choices (option sets), and alternate keys.
  Use for any DES component tagged schema_table, schema_column,
  schema_relationship, schema_choice, or schema_key.
allowed-tools: [view, edit, create, grep, glob]
---

# dataverse-table

Reusable **HOW** for the Dataverse data model. Applied twice against the same
canonical reference files: when **authoring** a `DES-##.md` (Stage 3) and when
**building** the artifact (Stage 4). This skill never restates a specific
design — it is the expertise layered on top of whatever the DES declares.

## When to use

Load this skill for every DES `solution.components` bullet whose
`component_type` is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `schema_table` | [schema_table.md](schema_table.md) |
| `schema_column` | [schema_column.md](schema_column.md) |
| `schema_relationship` | [schema_relationship.md](schema_relationship.md) |
| `schema_choice` | [schema_choice.md](schema_choice.md) |
| `schema_key` | [schema_key.md](schema_key.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and find its row above.
2. Open the matching reference file and read its **Required payload** and
   **Decision guide** sections.
3. Emit / verify the component's `data_model` entry so it declares **every**
   required field for that type — the required-field list is the single source
   of truth in `conventions.yml` `component_type_payloads` (do not invent
   fields; do not omit required ones).
4. Apply the reference file's **Naming**, **Decision guide**, and
   **Anti-patterns** before finalising.
5. Confirm each component carries `satisfies: [REQ-####]` — no orphan components.

## Ground rules (all types)

- **Config-first.** A data-model component is the declarative baseline; never
  push logic into pro-code that a column default, business rule, or rollup can
  express (`conventions.yml` `logic_tiers` = config → low_code → pro_code).
- **Publisher prefix.** Every new table/column/choice/relationship uses the
  solution publisher prefix (see the target solution's publisher, e.g. `cr_`);
  never author in the `default` publisher.
- **Traceability.** Every component maps to at least one `REQ-####` via
  `satisfies`. Reuse existing OOB tables/columns before creating new ones and
  say so ("existing" / "OOB").
- **Enforcement.** `validate_design.py` checks the `component_type` tag (shipped)
  and the required payload per type (Step validate-payload). This skill is the
  guidance; the validator is the backstop.
