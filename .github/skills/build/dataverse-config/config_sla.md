# config_sla — Service Level Agreement

Declarative SLA (enhanced SLA) with KPIs, warning and failure actions. Stage-3
reference and Stage-4 `patterns/config_sla.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_sla`:

| Field | Meaning |
| --- | --- |
| `name` | SLA display name. |
| `applies_to` | The table the SLA governs (e.g. Case) + the entitlement/condition scope. |
| `kpi` | The KPI(s) tracked (e.g. First Response By, Resolve By) with target durations. |
| `satisfies` | `[REQ-####]`. |

State warning-time and failure-time actions and the applicable-when / success
conditions.

## Decision guide

- **Enhanced SLA, not standard.** Use enhanced SLAs (support pause/resume, warning
  actions, success/failure actions) for anything beyond a single timer.
- **Business hours + holidays.** Attach a Customer Service Schedule so KPIs respect
  working calendars; never compute breach in a flow.
- **Warning vs failure.** Model proactive escalation as a **warning** action at a
  fraction of the KPI (e.g. 80%), and the breach as the **failure** action.
- **Pause conditions.** Define pause statuses (e.g. Waiting on Customer) so KPIs are
  fair and auditable.

## Naming

- Name by tier + KPI (e.g. `Gold — Resolve By`).

## Anti-patterns

- Re-implementing SLA timing in a cloud flow or plugin.
- Ignoring business hours (KPIs breach overnight/weekends).
- One giant SLA instead of per-tier SLA items.

## Validation checklist

- [ ] `applies_to`, `kpi`, `satisfies` declared.
- [ ] Warning + failure actions and pause conditions stated.
- [ ] Business-hours schedule referenced.

## Stage-4 build mapping

SLA + SLA KPI + SLA Item records in the solution; warning/failure actions wire to
their flows/updates. Verified by Stage-5 tests on the KPI metric.
