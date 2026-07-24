# config_business_rule — Business Rule

Declarative, server- or client-side rule that sets values, shows errors, or
toggles field state. Stage-3 reference and Stage-4 `patterns/config_business_rule.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_business_rule`:

| Field | Meaning |
| --- | --- |
| `name` | Business rule display name. |
| `table` | The table the rule is defined on. |
| `condition` | The if-condition(s) that trigger the rule. |
| `action` | The then/else actions (set value, set requirement, show error, show/hide, lock). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Scope = Entity** for logic that must hold across all forms, the API, and bulk
  ops; scope to a single form only for pure UI convenience.
- **Business rule before JavaScript.** Prefer a business rule to a web resource for
  show/hide, set-value, set-required, validation — no code, upgrade-safe.
- **Keep it simple.** If the logic needs loops, external calls, or many branches,
  escalate to a real-time flow or plugin (record the rationale) — don't chain a
  dozen business rules.

## Naming

- Name by intent (e.g. `Require Reason on Escalation`).

## Anti-patterns

- JavaScript for what a business rule does natively.
- Form-scoped rule for logic that must hold server-side (bypassed by API/import).
- Business-rule sprawl emulating procedural code.

## Validation checklist

- [ ] `table`, `condition`, `action`, `satisfies` declared.
- [ ] Scope (Entity vs form) chosen deliberately.

## Stage-4 build mapping

Business Rule (a process on the table) in the solution. Verified by Stage-5 tests
(condition → action, incl. server-side path where Entity-scoped).
