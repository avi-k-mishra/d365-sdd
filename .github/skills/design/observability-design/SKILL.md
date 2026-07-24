---
name: observability-design
description: >-
  How to author the mandatory observability block of a D365-CE SDD Stage 3
  DES-##.md — the events, metrics, traces, alerts, and audit the solution emits.
  Use when filling the observability decision axis / block of a design.
allowed-tools: [view, edit, create, grep, glob]
---

# observability-design

Reusable **HOW** for making every design observable by construction. A DES with
no observability block **fails** (`conventions.yml` `observability_required`) —
you cannot operate what you cannot see.

## When to use

- You are filling the `observability` axis / block of `specs/design/DES-##.md`.
- A component performs work whose success, latency, or failure must be visible.

## Mechanical process (deterministic)

1. **Declare what the solution emits** across five facets:
   - **Events** — meaningful business/technical events raised.
   - **Metrics** — counters/latencies tied to the source-REQ NFRs
     (`{ metric, target }`), so SLAs are measurable.
   - **Traces** — correlation across Dataverse → Azure hops (operation ids).
   - **Alerts** — the conditions (failure rate, latency, availability) that page
     someone, tied to the observability requirement.
   - **Audit** — what compliance requires logging (see the build
     `config_audit` component where Dataverse auditing applies).
2. **Tie metrics to carried-over NFRs.** Each NFR target should have a metric
   that proves it.
3. **Route telemetry to a sink.** Where Azure compute exists, wire
   Application Insights (see the build `az_app_insights` component); name the
   sink, don't leave it implicit.
4. **No PII/secrets in telemetry.** Never log sensitive data into events/traces.

## Ground rules

- **Observability is mandatory, not optional.** Every DES declares events,
  metrics, traces, alerts, and audit.
- **Measurable SLAs.** Every NFR target has a metric that verifies it.
- **Actionable alerts.** Alerts map to real failure/latency/availability
  conditions, not noise nobody watches.

## Anti-patterns

- A DES with no observability block (hard validation failure).
- NFR targets with no metric proving them.
- Logging secrets or PII into telemetry.
- Alerts defined but tied to nothing actionable.
