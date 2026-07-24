# az_service_bus — Azure Service Bus

Reliable asynchronous messaging (queues/topics) between Dataverse and external
systems. Stage-3 reference and Stage-4 `patterns/az_service_bus.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Namespace / queue / topic name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture queues vs topics/subscriptions, sessions, and
dead-lettering.

## Decision guide

- **Service Bus for decoupled, reliable, ordered async** integration; Event Grid
  for lightweight event distribution — choose per pattern.
- **Dataverse → Service Bus** via the plug-in service endpoint (data export) for
  reliable outbound eventing.
- **Topics + subscriptions** for fan-out; queues for point-to-point.
- **Dead-letter + retry** designed in; sessions when ordering matters.
- **Managed identity + RBAC**, no shared-access keys where avoidable.

## Anti-patterns

- Polling instead of messaging for near-real-time integration.
- No dead-letter handling (silent message loss).
- SAS keys where managed identity works.

## Validation checklist

- [ ] `satisfies` declared (+ queue/topic topology once authored).
- [ ] Dead-letter/retry + identity model stated.

## Stage-4 build mapping

Service Bus namespace/entities (IaC). Verified by Stage-5 tests (message published
→ consumed / dead-lettered as designed).
