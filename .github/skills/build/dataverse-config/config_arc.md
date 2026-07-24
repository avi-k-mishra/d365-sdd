# config_arc — Automatic Record Creation & Update rule

Declarative rule that converts an incoming activity (email, social, custom) into a
record such as a Case. Stage-3 reference and Stage-4 `patterns/config_arc.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_arc`:

| Field | Meaning |
| --- | --- |
| `name` | Rule display name. |
| `source` | The source channel / activity type (queue, email, custom activity). |
| `target` | The record created/updated (e.g. Case) and how fields are mapped. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **ARC over custom flow** for channel-to-record conversion — it is the supported
  Customer Service mechanism (dedupe against existing records, condition steps,
  create/update actions).
- **Deduplicate first.** Configure the "find existing record" condition so replies
  update the existing Case instead of spawning duplicates.
- **Channel scope.** One rule per source queue/channel; keep mapping explicit.
- **Escalate only when needed.** Push custom transformation to a child flow only if
  ARC conditions cannot express it (record the escalation rationale).

## Naming

- Name by source→target (e.g. `Support Inbox → Case`).

## Anti-patterns

- A cloud flow reinventing ARC.
- No dedupe step → duplicate Cases on email threads.
- One rule spanning many unrelated channels.

## Validation checklist

- [ ] `source`, `target`, `satisfies` declared.
- [ ] Dedupe / find-existing condition stated.

## Stage-4 build mapping

Automatic Record Creation and Update Rule + its rule items in the solution.
Verified by Stage-5 tests (inbound activity → expected record).
