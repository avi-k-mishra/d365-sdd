# az_event_grid — Azure Event Grid

Lightweight, push-based event distribution between publishers and handlers.
Stage-3 reference and Stage-4 `patterns/az_event_grid.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Topic / system-topic / subscription name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture the event source, event types, subscriptions, and handlers.

## Decision guide

- **Event Grid vs Service Bus.** Event Grid for reactive, fan-out, near-real-time
  notification of discrete events; Service Bus for reliable, ordered, transactional
  messaging/commands.
- **Filter at the subscription** (event type / subject) so handlers get only what
  they need.
- **Dead-letter + retry policy** configured; handlers idempotent.
- **Managed identity** for delivery where supported; validate webhook endpoints.

## Anti-patterns

- Event Grid for guaranteed-ordered transactional workflows (use Service Bus).
- Unfiltered subscriptions waking handlers on every event.
- No dead-letter / non-idempotent handlers.

## Validation checklist

- [ ] `satisfies` declared (+ sources/subscriptions once authored).
- [ ] Filtering + dead-letter + idempotency stated.

## Stage-4 build mapping

Event Grid topic/subscriptions (IaC). Verified by Stage-5 tests (event published →
filtered handler invoked / dead-lettered as designed).
