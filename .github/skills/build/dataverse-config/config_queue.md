# config_queue — Queue

A queue for holding and distributing work items (cases, activities). Stage-3
reference and Stage-4 `patterns/config_queue.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_queue`:

| Field | Meaning |
| --- | --- |
| `name` | Queue display name. |
| `queue_type` | `private` (members only) or `public` (org-visible). |
| `satisfies` | `[REQ-####]`. |

State queue membership (which teams/roles) and any auto-record-creation binding.

## Decision guide

- **Private for scoped work** (e.g. a supervisor escalation queue) — only members
  see items; public for broadly shared work.
- **Membership via team**, not individuals, so access is role-managed.
- **Queue vs owner.** Items in a queue still have an owner; routing moves the queue
  item, assignment sets the owner.
- **Mailbox binding** only if the queue ingests email (ARC/incoming mail).

## Naming

- Name by function (e.g. `Supervisor Escalations`).

## Anti-patterns

- Public queue for sensitive/escalated work.
- Per-user membership instead of team-based.
- A queue with no defined worker/assignment path.

## Validation checklist

- [ ] `queue_type`, `satisfies` declared; membership stated.

## Stage-4 build mapping

Queue record + membership in the solution/environment. Verified by Stage-5 tests
(visibility + item routing).
