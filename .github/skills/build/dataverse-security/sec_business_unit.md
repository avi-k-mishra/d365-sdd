# sec_business_unit — Business Unit

An organizational boundary that scopes ownership and BU-level access. Stage-3
reference and Stage-4 `patterns/sec_business_unit.md`.

## Required payload

From `conventions.yml` `component_type_payloads.sec_business_unit`:

| Field | Meaning |
| --- | --- |
| `name` | Business unit name. |
| `parent` | Parent business unit (root BU if top-level). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **BUs are for data isolation, not org charts.** Add a BU only when access must be
  partitioned; don't mirror every department.
- **Hierarchy drives Parent:Child depth.** The tree shape is what makes
  Parent:Child access meaningful — design it deliberately.
- **Modern (matrix) BU access** via owning-BU on records + `sec_team` can avoid deep
  trees; consider before proliferating BUs.
- **Moving records/users between BUs** reassigns roles — plan for it.

## Naming

- Name by the real boundary (region/legal entity), not by a role.

## Anti-patterns

- One BU per department when no isolation is needed.
- Deep BU trees where a team-based model would do.
- Treating BUs as security roles.

## Validation checklist

- [ ] `parent`, `satisfies` declared.
- [ ] Isolation need justified (not merely org-chart mirroring).

## Stage-4 build mapping

Business Unit in the environment (BUs are environment data; solution-aware
deployment scripts create/verify). Verified by Stage-5 tests (BU-scoped access).
