# config_routing_rule — Routing Rule Set

Declarative Customer Service routing that directs cases to the right queue/team.
Stage-3 reference and Stage-4 `patterns/config_routing_rule.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_routing_rule`:

| Field | Meaning |
| --- | --- |
| `name` | Routing rule set display name. |
| `queue` | The destination queue(s)/team the rule routes to. |
| `criteria` | The ordered rule-item conditions that select the destination. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Rule item order matters** — the first matching item wins; order most-specific
  first, with a catch-all last.
- **Basic vs unified routing.** Use classic routing rule sets for simple
  queue assignment; note when unified routing (intelligent/skills-based) is the
  better fit and raise it if the design needs it.
- **Routing sets destination, not ownership.** Pair with an assignment rule for
  who actually works the item.
- **One active set.** Only one routing rule set is active per table — consolidate.

## Naming

- Name by scope (e.g. `Case Routing — Priority`).

## Anti-patterns

- Overlapping/ambiguous rule items with no clear precedence.
- Encoding assignment (owner) logic into routing.
- Multiple competing active sets.

## Validation checklist

- [ ] `queue`, `criteria`, `satisfies` declared.
- [ ] Rule-item order + catch-all stated.

## Stage-4 build mapping

Routing Rule Set + rule items in the solution (activated post-import). Verified by
Stage-5 tests (case attributes → expected queue).
