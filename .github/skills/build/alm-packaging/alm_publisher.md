# alm_publisher — Solution Publisher

Defines the customization prefix and option-value base for a solution family.
Stage-3 reference and Stage-4 `patterns/alm_publisher.md`.

## Required payload

From `conventions.yml` `component_type_payloads.alm_publisher`:

| Field | Meaning |
| --- | --- |
| `name` | Publisher display/unique name. |
| `prefix` | Customization prefix (e.g. `contoso`) applied to schema names. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **One publisher across the family.** All related solutions share the same
  publisher/prefix so schema names are consistent and re-parenting is avoided.
- **Choose the prefix once, early** — changing it later renames every component.
- **Set the option-value prefix** deliberately (avoids choice-value collisions
  across publishers).
- **Never use the default publisher** (`new_`/`cr###_`) for real work.

## Naming

- Short, org-branded prefix (3–8 chars), lowercase.

## Anti-patterns

- Default publisher / random prefix.
- Multiple publishers within one solution family.
- Changing prefix after components exist.

## Validation checklist

- [ ] `prefix`, `satisfies` declared.
- [ ] Prefix consistent across the solution family.

## Stage-4 build mapping

Publisher (created before the solution). Verified by Stage-5 tests (components
carry the expected prefix).
