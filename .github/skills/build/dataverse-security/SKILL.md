---
name: dataverse-security
description: >-
  How to design and build the Dataverse security and governance model — security
  roles, column (field) security profiles, business units, teams, and auditing.
  Use for any DES component tagged sec_role, sec_field_profile, sec_business_unit,
  sec_team, or config_audit.
allowed-tools: [view, edit, create, grep, glob]
---

# dataverse-security

Reusable **HOW** for least-privilege security and governance. Applied both when
authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `sec_role` | [sec_role.md](sec_role.md) |
| `sec_field_profile` | [sec_field_profile.md](sec_field_profile.md) |
| `sec_business_unit` | [sec_business_unit.md](sec_business_unit.md) |
| `sec_team` | [sec_team.md](sec_team.md) |
| `config_audit` | [config_audit.md](config_audit.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload sub-list against the reference's **Required payload**
   (`conventions.yml` `component_type_payloads`).
3. Apply the reference's **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Least privilege by default.** Grant the narrowest access depth (User < BU <
  Parent:Child BU < Org) that satisfies the requirement; never start from Org.
- **Roles via teams, not per user.** Assign roles to teams (owner/AAD-group) where
  possible for scalable administration.
- **Custom roles, never edit OOB.** Copy an OOB role and adjust; leave system roles
  intact for upgrade safety.
- **Column security is real security.** Sensitive fields use a
  `sec_field_profile` + column security — not form-hide or business-rule visibility.
