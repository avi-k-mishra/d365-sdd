# config_dup_detection — Duplicate Detection Rule

Declarative rule that warns on (or blocks) duplicate records. Stage-3 reference
and Stage-4 `patterns/config_dup_detection.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_dup_detection`:

| Field | Meaning |
| --- | --- |
| `name` | Duplicate detection rule display name. |
| `table` | The base (and matching) table. |
| `match_criteria` | The columns + match codes (exact / same-first-N-chars) that define a duplicate. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Detection warns, keys enforce.** Duplicate detection is advisory (create/update,
  import, bulk). If uniqueness must be **guaranteed**, use a `schema_key` alternate
  key instead (or in addition).
- **Match codes** must fit within the length limit; choose case/whitespace options
  deliberately.
- **Publish to activate**, and confirm the jobs (create/update/import) it runs under.
- **Cross-table** rules only when the duplicate concept legitimately spans tables.

## Naming

- Name by table + basis (e.g. `Account — Name + City`).

## Anti-patterns

- Relying on detection where a hard alternate key is required.
- Match criteria so loose everything flags, or so tight nothing does.
- Forgetting to publish/activate the rule.

## Validation checklist

- [ ] `table`, `match_criteria`, `satisfies` declared.
- [ ] Warn-vs-enforce decision stated (key added if enforcement needed).

## Stage-4 build mapping

Duplicate Detection Rule (published) in the environment. Verified by Stage-5 tests
(duplicate input → expected warning/behaviour).
