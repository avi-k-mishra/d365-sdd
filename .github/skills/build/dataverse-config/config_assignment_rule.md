# config_assignment_rule — Assignment Rule

Declarative logic that sets the owner of a work item (who works it), typically
after routing places it in a queue. Stage-3 reference and Stage-4
`patterns/config_assignment_rule.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_assignment_rule`:

| Field | Meaning |
| --- | --- |
| `name` | Assignment rule display name. |
| `queue` | The queue whose items are assigned. |
| `logic` | The distribution logic (round-robin, capacity/skills, most-available, condition-based). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Assignment ≠ routing.** Routing selects the queue; assignment selects the
  owner. Keep the two components distinct.
- **Prefer OOB distribution** (unified routing assignment methods: round-robin,
  capacity, skills) over a custom flow that picks owners.
- **Fallback owner.** Define what happens when no agent matches (leave in queue /
  assign to team) — never silently drop.
- **Capacity/skills** require the corresponding agent profiles configured.

## Naming

- Name by queue + method (e.g. `Escalation Queue — Round Robin`).

## Anti-patterns

- Owner-picking logic buried in a cloud flow instead of an assignment rule.
- No fallback when no agent qualifies.
- Mixing routing criteria into assignment.

## Validation checklist

- [ ] `queue`, `logic`, `satisfies` declared.
- [ ] Fallback behaviour stated.

## Stage-4 build mapping

Unified-routing assignment configuration (or classic assignment) in the
environment. Verified by Stage-5 tests (queue item → expected owner).
