# az_app_insights — Application Insights

Telemetry and monitoring backbone for the solution's compute and integrations.
Stage-3 reference and Stage-4 `patterns/az_app_insights.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Application Insights resource name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture what emits telemetry, sampling, and alert rules.

## Decision guide

- **Observability is default, not optional.** Every Function App / custom connector
  / integration emits traces, requests, dependencies, and exceptions here.
- **Correlate end-to-end** with operation IDs across Dataverse → Azure hops.
- **Alerts on the observability requirement** (failure rate, latency, availability)
  — tie to the design's `observability` axis.
- **Workspace-based** Application Insights; sensible sampling to control cost.

## Anti-patterns

- Compute components with no telemetry (black-box failures).
- Logging secrets/PII into telemetry.
- No alerts (monitoring nobody watches).

## Validation checklist

- [ ] `satisfies` declared (+ emitters/alerts once authored).
- [ ] Correlation + alerting tied to the observability requirement.

## Stage-4 build mapping

Application Insights (IaC) + instrumentation + alerts. Verified by Stage-5 tests
(operation produces expected telemetry; alert fires on fault injection).
