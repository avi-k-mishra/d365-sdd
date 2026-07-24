# sec_team — Team

A group (owner / AAD security-group / AAD Office-group) used to assign roles and
own records. Stage-3 reference and Stage-4 `patterns/sec_team.md`.

## Required payload

From `conventions.yml` `component_type_payloads.sec_team`:

| Field | Meaning |
| --- | --- |
| `name` | Team name. |
| `business_unit` | The BU that owns the team. |
| `roles` | Security roles assigned to the team. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Prefer AAD-group teams** for membership that mirrors Entra ID groups — members
  and role inheritance are automatic.
- **Owner teams** when records must be team-owned (not user-owned).
- **Access teams** (record-level sharing) are a different mechanism — use when
  sharing is per-record and dynamic, not for broad role assignment.
- **Assign roles to the team**, then add users to the team — the scalable
  alternative to per-user role assignment.

## Naming

- Name by function + BU where ambiguous (e.g. `Support Agents — EU`).

## Anti-patterns

- Per-user role assignment where a team would scale better.
- Confusing owner teams with access teams.
- Team in the wrong BU (owner/role scope surprises).

## Validation checklist

- [ ] `business_unit`, `roles`, `satisfies` declared.
- [ ] Team type (owner / AAD-group / access) implied by the design.

## Stage-4 build mapping

Team (+ role assignment) in the environment. Verified by Stage-5 tests
(team member inherits expected access).
