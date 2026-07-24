# sec_field_profile — Field (Column) Security Profile

Grants access to column-security-enabled columns. Stage-3 reference and Stage-4
`patterns/sec_field_profile.md`.

## Required payload

From `conventions.yml` `component_type_payloads.sec_field_profile`:

| Field | Meaning |
| --- | --- |
| `name` | Field security profile display name. |
| `protected_columns` | The column-security-enabled columns this profile governs. |
| `grantee_roles` | The roles/teams/users granted Read/Create/Update on those columns. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Enable column security on the column first** (the `schema_column` component),
  then grant via this profile — the two are a pair.
- **Grant per operation.** Read, Create, and Update are separate grants; grant only
  what the grantee needs (often Read-only for most, Update for a few).
- **Deny is the default.** Anyone not granted (incl. otherwise-privileged users)
  cannot see the column value — verify no one is unintentionally locked out.
- **Grant to roles/teams, not individuals** for maintainability.

## Naming

- Name by the protected data (e.g. `Escalation Notes`).

## Anti-patterns

- Using form-hide / business-rule visibility as "security" (bypassed via API/export).
- Over-granting Update where Read suffices.
- Per-user grants instead of role/team grants.

## Validation checklist

- [ ] `protected_columns`, `grantee_roles`, `satisfies` declared.
- [ ] Paired with a column-security-enabled `schema_column`.

## Stage-4 build mapping

Field Security Profile + field permissions in the solution. Verified by Stage-5
tests (granted vs denied identities read/write the protected column correctly).
