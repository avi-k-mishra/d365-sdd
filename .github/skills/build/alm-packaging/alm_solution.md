# alm_solution — Dataverse Solution

The container that packages all components for ALM transport. Stage-3 reference
and Stage-4 `patterns/alm_solution.md`.

## Required payload

From `conventions.yml` `component_type_payloads.alm_solution`:

| Field | Meaning |
| --- | --- |
| `name` | Solution unique/display name. |
| `publisher` | The owning `alm_publisher` (prefix source). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **One logical solution per app family**; split only for genuine independent
  lifecycle (segmentation) needs.
- **Unmanaged authoring, managed delivery.** Dev holds unmanaged; downstream gets
  managed.
- **Avoid default solution** for real components — always a named custom solution.
- **Dependencies explicit.** If it references another solution's components, that
  dependency is part of the design.

## Naming

- Stable unique name (no spaces), human-readable display name.

## Anti-patterns

- Building in the Default/Common Data Services Default solution.
- Over-segmentation creating dependency tangles.
- Managed imported into the dev/authoring environment.

## Validation checklist

- [ ] `publisher`, `satisfies` declared.
- [ ] Managed-downstream / unmanaged-dev intent clear.

## Stage-4 build mapping

Solution (unpacked to source control; exported managed for delivery). Verified by
Stage-5 tests (managed solution imports cleanly in a target environment).
