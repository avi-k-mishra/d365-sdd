---
id: DES-01
title: "Tiered SLA & Escalation Design"
satisfies: [REQ-0003, REQ-0004]
implements_feature: FEAT-02
spec_hash: "47899e3f5d129cc65a5b5ecc853a834547ea863b6ff25c3aaed6fcdbebf118f0"
status: draft
---

<!-- FILL:decisions -->
### logic_tier
low_code — Use native Customer Service configuration for SLA KPIs, SLA items, queues, and timer controls, and use the platform-authored Power Automate experiences behind automatic record creation/update rules and SLA action flows for the two dynamic behaviors FEAT-02 requires: deriving case priority from the customer tier at create time and executing escalation/notification steps when an SLA KPI becomes non-compliant. Rationale: Microsoft documents both rule authoring and SLA actions through first-party low-code surfaces, so a plug-in or custom API would be an unnecessary escalation beyond the approved scope.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/automatically-create-update-records
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements

### data_residency
dataverse-native — Keep the case, customer tier reference, SLA KPI instance data, queue items, and escalation state inside Dataverse and Customer Service. The approved feature does not require an external store, broker, or analytics sink; Microsoft describes both ARC outputs and SLA tracking as Dataverse-backed records.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/automatically-create-update-records
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements

### alm_boundary
Use one custom-publisher unmanaged solution in Dev for the Case form/view/dashboard updates, SLA KPIs, SLAs, routing rules, and solution-aware flows, then export managed artifacts to Test/UAT/Prod. Queue, user/team, and queue-membership bindings stay environment-specific operational data and must be rebound per target environment because Microsoft documents routing rules as solution-aware while their queue/user/team mappings are not.

Grounding:
- https://learn.microsoft.com/power-platform/alm/solution-concepts-alm
- https://learn.microsoft.com/power-platform/alm/move-from-unmanaged-managed-alm#convert-an-unmanaged-solution-to-managed
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-rules-automatically-route-cases

### security
Least-privilege split:
- configuration rights only for Customer Service Manager / System Customizer / System Administrator when creating or activating SLAs, queues, ARC rules, and routing rules;
- service representatives keep case-handling permissions plus read access to SLA/SLA KPI instance data needed to see timers and breach state;
- supervisor queue membership is limited to supervisors/managers, preferably through a private queue when escalation work visibility should be narrowed.
No external service principal is required because the approved solution stays inside first-party Customer Service and Power Automate capabilities.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements
- https://learn.microsoft.com/dynamics365/customer-service/administer/set-up-queues-manage-activities-cases

### integration
None external — FEAT-02 is implemented with first-party Customer Service + Dataverse + Power Automate only. The design intentionally avoids API Management, Service Bus, Azure Functions, or third-party connectors because the approved requirement set only calls for in-platform case creation logic, queueing, and SLA-driven escalation.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/automatically-create-update-records
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla

### environment
Author in a dedicated development environment, validate the managed import in Test/UAT before production, and never test the managed package in the same environment that contains the originating unmanaged solution. This follows Microsoft ALM guidance for Power Platform solutions and supports the Gate A/B review path without polluting downstream environments with unmanaged layers.

Grounding:
- https://learn.microsoft.com/power-platform/alm/solution-concepts-alm
- https://learn.microsoft.com/power-platform/alm/move-from-unmanaged-managed-alm#convert-an-unmanaged-solution-to-managed

### ux_surface
Use the existing Customer Service model-driven experience: the Case main form shows Priority plus the SLA timer controls, service representatives work from case and queue views, and supervisors monitor escalation queues/dashboards. Stay with out-of-box Unified Interface controls; do not introduce PCF or custom pages because Microsoft already provides responsive navigation, grid/form accessibility, and dashboard support for this feature.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements
- https://learn.microsoft.com/power-apps/user/unified-interface
- https://learn.microsoft.com/power-apps/user/screen-reader

### observability
Use platform-visible operational evidence instead of custom telemetry: SLA KPI instance state/time fields, queue items, flow run history for SLA actions, Dataverse audit history for case changes, and dashboard/view counts for escalated work. This satisfies the feature's need to prove priority assignment, pause/resume behavior, and breach escalation without introducing external monitoring infrastructure.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
- https://learn.microsoft.com/power-platform/admin/manage-dataverse-auditing#use-the-audit-history-in-a-model-driven-app
<!-- /FILL -->

<!-- FILL:solution -->
- **components:**
  - Automatic record creation/update rule item (or equivalent case-create flow in the approved creation path) that stamps Case Priority from the reviewed customer tier mapping.
  - Enhanced SLA with two KPI tracks on Case: `First Response By` and `Resolve By`, with Applicable When conditions aligned to the approved priority/tier combinations.
  - SLA item actions in Power Automate for warning/non-compliance handling, including setting the Case `Is Escalated` field and notifying the supervisor queue.
  - Basic queue(s) for supervisor escalation handling plus, if needed, a routing ruleset that routes escalated cases to the supervisor queue.
  - Case main form timer control plus queue/case views and dashboards for service representatives and supervisors.
- **data_model:**
  - Reuse the existing customer service tier column referenced by REQ-0003 on the customer record that FEAT-02 cases are created against; implementation binds the actual Dataverse schema name in the target environment.
  - Case table fields used by this feature: Priority, status/on-hold state, SLA timer/KPI lookup fields required by the SLA configuration, and `Is Escalated`.
  - Queue and queue-item records carry supervisor escalation work; SLA KPI Instance records carry warning/failure timing evidence.
- **security[]:**
  - Admin/config roles: Customer Service Manager or equivalent for SLA, queue, and routing configuration; System Customizer/System Administrator only where schema/form changes are needed.
  - Runtime roles: service representatives can read timers/escalation indicators and work their assigned cases; supervisor queue members can view and act on escalated queue items.
  - Queue visibility: prefer a private supervisor queue when escalations should be operationally restricted; keep underlying case access under normal Dataverse role governance because queue privacy alone does not secure the record.
- **integration[]:**
  - None external.
  - First-party Power Automate flows generated from ARC/SLA configuration remain inside the Microsoft platform boundary.
- **test_strategy[]:**
  - Convert REQ-0003 scenarios into case-create tests for Gold/Silver/Bronze/default customers and verify Priority on the saved Case record.
  - Convert REQ-0004 scenarios into SLA tests that verify warning/failure timing, `On Hold` pause behavior, and the boundary case where success occurs exactly at the threshold.
  - For the escalation latency NFR, measure the delta between SLA KPI failure time and the `Is Escalated`/queue-notification outcome recorded by the flow and queue item state.
  - Use queue and dashboard views plus audit history to confirm the design emits the same operational evidence that Stage 5 assertions will inspect.
<!-- /FILL -->

<!-- FILL:observability -->
- **events:**
  - `CasePriorityDerived` when the create-time rule stamps Priority from customer tier.
  - `SLAWarningReached` when a KPI reaches warning time.
  - `CaseEscalatedToSupervisorQueue` when the non-compliance action sets `Is Escalated` and posts work/notification to the supervisor path.
- **metrics:**
  - Carry over and monitor the REQ-0004 timing targets: `sla_first_response_gold`, `sla_resolution_gold`, `sla_first_response_silver`, `sla_resolution_silver`, `sla_first_response_bronze`, `sla_resolution_bronze`, and `escalation_action_latency`.
  - Operational counts: active escalated cases, breached cases by tier, paused SLA KPI instances, queue backlog for the supervisor queue.
- **traces:**
  - Correlate the Case record, SLA KPI Instance record, queue item, and Power Automate run history by case identifier and created/modified timestamps.
  - Preserve the exact approved tier/priority and SLA item names in flow/action naming so support teams can trace a breach back to the configured rule.
- **alerts:**
  - Use SLA warning/non-compliance email/notification actions for immediate supervisor awareness.
  - Review queue backlog and breached-case dashboard views against the `escalation_action_latency` target; any case that breaches the KPI but does not show `Is Escalated`/queue evidence within 5 minutes is an operational alert condition.
- **audit:**
  - Enable Dataverse auditing on the case fields that show Priority, escalation state, status/on-hold transitions, and assignment/owner changes relevant to the escalation path.
  - Retain SLA KPI Instance history and flow run history as the supportable record of when warning/failure transitions occurred.
<!-- /FILL -->

<!-- FILL:open-questions -->
- [x] OQ-DES-01-1 (DECIDED — avinam@microsoft.com, 2026-07-15): The approved tier-to-priority mapping is fixed as Gold→High, Silver→Normal, Bronze→Low, Default→Normal, so the design does not introduce alternate mapping tables or customer-specific overrides.
- [x] OQ-DES-01-2 (DECIDED — avinam@microsoft.com, 2026-07-15): The approved SLA durations are fixed as Gold 1h/4h, Silver 4h/8h, Bronze 8h/next business day, so the design only configures those KPI thresholds.
<!-- /FILL -->

---

## Traceability (FEAT ← REQ ← INTK)

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Intake Batch | Feature |
|-----|-------|--------------|--------|
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | INTK-0001 | FEAT-02 |
| REQ-0004 | Automatic Case Escalation on SLA Breach | INTK-0001 | FEAT-02 |
<!-- COMPILER:END traceability -->

## NFR carry-over

<!-- COMPILER:BEGIN nfr -->
| Metric | Target | Source REQ |
|--------|--------|------------|
| sla_first_response_gold | First response within 1 hour for Gold (High priority) cases | REQ-0004 |
| sla_resolution_gold | Resolution within 4 hours for Gold (High priority) cases | REQ-0004 |
| sla_first_response_silver | First response within 4 hours for Silver (Normal priority) cases | REQ-0004 |
| sla_resolution_silver | Resolution within 8 hours for Silver (Normal priority) cases | REQ-0004 |
| sla_first_response_bronze | First response within 8 hours for Bronze (Low priority) cases | REQ-0004 |
| sla_resolution_bronze | Resolution by next business day for Bronze (Low priority) cases | REQ-0004 |
| escalation_action_latency | SLA KPI failure action fires within 5 minutes of the failure threshold being crossed | REQ-0004 |
<!-- COMPILER:END nfr -->

## Provenance

<!-- COMPILER:BEGIN provenance -->
| Design | Feature | Member REQs |
|--------|---------|-------------|
| DES-01 | FEAT-02 | REQ-0003, REQ-0004 |
<!-- COMPILER:END provenance -->
