# sec_role — Security Role

Least-privilege Dataverse security role. Stage-3 reference and Stage-4
`patterns/sec_role.md`.

## Required payload

From `conventions.yml` `component_type_payloads.sec_role`:

| Field | Meaning |
| --- | --- |
| `name` | Role display name. |
| `privileges` | Per-table privileges (Create/Read/Write/Delete/Append/AppendTo/Assign/Share) each at an access level (User/BU/Parent:Child/Org), plus miscellaneous privileges. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Copy, don't edit OOB.** Base a custom role on the closest OOB role; never
  modify system roles.
- **Minimum depth.** Choose the lowest access level per privilege that works
  (User → BU → Parent:Child → Org). Escalate a single privilege, not the whole role.
- **Additive model.** Users get the union of their roles — design small composable
  roles rather than one mega-role.
- **Don't forget app + custom privileges.** Model-driven app access, custom table
  privileges, and miscellaneous privileges (e.g. bulk delete) are explicit.

## Naming

- Name by persona (e.g. `Supervisor`, `Escalation Manager`).

## Anti-patterns

- Org-level access "to be safe".
- Editing OOB roles (breaks upgrades).
- One monolithic role instead of composable roles.
- Granting Delete where Deactivate/Write suffices.

## Validation checklist

- [ ] `privileges` (table + level) and `satisfies` declared.
- [ ] Least-privilege depth justified; based on a copied OOB role.

## Stage-4 build mapping

Security Role in the solution (role privileges bound to the target BU on import).
Verified by Stage-5 tests (persona can/can't perform the guarded actions).
