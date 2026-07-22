---
id: DES-02
title: "Automated Case Escalation & Supervisor Notifications Design"
satisfies: [REQ-0005, REQ-0006, REQ-0007, REQ-0008]
implements_feature: FEAT-03
spec_hash: "c42807963d3240215e0cc70cc379eaa6c1df36a2162ce422e9f5fbd28a013cfd"
status: draft
---

<!-- FILL:decisions -->
Record all ten axes; give a grounded rationale (cite Microsoft Learn) for every
non-trivial or escalated choice.

### logic_tier
low_code — SLA item "Nearing Non-compliance" (warning) actions in the enhanced SLA (built by FEAT-02) natively invoke Power Automate cloud flows. The escalation trigger flow sets Case_Escalated=true and re-assigns the case to the supervisor queue; the supervisor notification flow sends email via the Office 365 Outlook connector and a Teams message via the Teams connector. All three behaviors (flag-setting, queue re-assignment, dual notification) are achievable through documented low-code surfaces without a Dataverse plugin or custom API.

Rationale: Microsoft Learn documents that SLA item warning/failure actions call a Power Automate flow via a first-party mechanism in enhanced SLAs; the Teams and Office 365 Outlook connectors are published first-party connectors available in Power Automate without escalating to pro-code. No pro-code component is required.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
- https://learn.microsoft.com/connectors/teams/
- https://learn.microsoft.com/connectors/office365/

### data_residency
Dataverse-native — all state (Case_Escalated flag, Case_EscalationNotes column, SLA KPI Instance records, queue items, supervisor lookup) lives in Dataverse. Notification delivery uses first-party Microsoft 365 connectors (Teams, Outlook) within the Power Platform boundary. No external data store, message broker, or analytics sink is required for the approved feature scope.

Grounding:
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
- https://learn.microsoft.com/power-platform/admin/field-level-security

### alm_boundary
Custom publisher solution (unmanaged in Dev, exported as managed to Test/UAT/Prod). The solution wraps: schema components (Case_Escalated column, Case_EscalationNotes column), security components (EscalationNotes FieldSecurityProfile, Supervisor and Manager security roles), config components (SLA escalation warning item, supervisor escalation queue), flow components (escalation trigger flow, notification flow), UX components (Case main form update, active escalations view, supervisor escalations dashboard, escalation section business rule), and ALM components (connection references for Teams and Outlook connectors). Queue membership and user/team/supervisor bindings are operational data that must be rebound per environment after managed import, as documented by Microsoft ALM guidance.

Grounding:
- https://learn.microsoft.com/power-platform/alm/solution-concepts-alm
- https://learn.microsoft.com/power-platform/alm/move-from-unmanaged-managed-alm#convert-an-unmanaged-solution-to-managed

### security
Least-privilege across three layers:

- **Column-level security**: Case_EscalationNotes is a column-security-enabled column. The EscalationNotes FieldSecurityProfile grants Create/Read/Update only to the Supervisor and Manager security roles. The Agent role has no access to this profile; the column is not surfaced on portal forms and not returned via portal Web API to portal users without the profile (REQ-0008).
- **Queue access**: the supervisor escalation queue is configured as a private queue, visible and accessible only to members assigned the Supervisor or Manager role, preventing front-line agents from seeing or working escalated queue items (REQ-0005).
- **Flow service identity**: the escalation and notification flows run under a dedicated service account with minimum Dataverse permissions (Read Case, Write Case_Escalated, Create Queue Item, Read SLA KPI Instance). The Teams and Outlook connectors use solution-aware connection references bound to environment-appropriate Microsoft 365 service accounts.
- **Config roles**: Customer Service Manager or System Administrator for SLA item, queue, and field-security-profile configuration; System Customizer for schema and form changes.

Grounding:
- https://learn.microsoft.com/power-platform/admin/field-level-security
- https://learn.microsoft.com/dynamics365/customer-service/administer/set-up-queues-manage-activities-cases
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla

### integration
Internal Microsoft 365 only — no external third-party integration. The supervisor notification flow uses:
- **Microsoft Teams connector** (first-party Power Automate connector) to post a direct message or channel message to the assigned supervisor.
- **Office 365 Outlook connector** (first-party Power Automate connector) to send the notification email to the assigned supervisor.

Both connectors operate within the Microsoft 365 / Power Platform boundary. No Azure API Management, Azure Service Bus, Azure Functions, or third-party service is required or introduced.

Grounding:
- https://learn.microsoft.com/connectors/teams/
- https://learn.microsoft.com/connectors/office365/

### environment
Dev (author unmanaged) → Test (import managed) → UAT (import managed) → Prod (import managed). Connection references for the Teams and Outlook connectors are rebound to environment-appropriate service account credentials in each environment after managed import. Queue membership and supervisor user/team bindings are operational data and must be configured per environment. Never test the managed package in the same environment as the originating unmanaged solution, per Microsoft ALM guidance.

Grounding:
- https://learn.microsoft.com/power-platform/alm/solution-concepts-alm
- https://learn.microsoft.com/power-platform/alm/move-from-unmanaged-managed-alm#convert-an-unmanaged-solution-to-managed

### ux_surface
Model-driven Customer Service app; Copilot Service admin center used only for SLA/queue configuration. Key surfaces:
- **Case main form**: a new Escalation section shows the Case_Escalated indicator (Boolean, read-only) and the Case_EscalationNotes field (hidden for Agent role via FieldSecurityProfile). A business rule shows the section only when Escalated=true, keeping the form clean for non-escalated cases.
- **Active escalations view**: model-driven system view on Case (Escalated=true, Status=Active), sorted ascending by remaining SLA breach time; columns: Case Number, Customer, Priority, Remaining Time to Breach (REQ-0007).
- **Supervisor escalations dashboard**: model-driven system dashboard embedding the active escalations view and a chart for urgency distribution; accessible to Supervisor/Manager roles (REQ-0007).

No PCF component or custom page is introduced; standard OOB Unified Interface controls fully satisfy the approved feature scope. Detail in UX-02.

Grounding:
- https://learn.microsoft.com/power-apps/maker/model-driven-apps/create-edit-dashboards
- https://learn.microsoft.com/power-apps/user/unified-interface
- https://learn.microsoft.com/dynamics365/customer-service/administer/set-up-queues-manage-activities-cases

### observability
Key telemetry emitted by this design:
- **Events**: `CaseEscalated` (escalation trigger flow sets flag + queue), `SupervisorNotificationSent` (email + Teams dispatched), `SupervisorNotificationSkipped` (no supervisor configured for team).
- **Metrics**: `escalation_notification_latency` (seconds from `CaseEscalated` to `SupervisorNotificationSent`, target ≤60s per REQ-0006 NFR), `active_escalated_cases_count`, `notification_failure_count`.
- **Traces**: case ID correlated across SLA KPI Instance record, escalation flow run, queue item, and notification flow run.
- **Alerts**: flow run failure rate > 0 for either flow; `escalation_notification_latency` > 60s.
- **Audit**: Dataverse audit on Case_Escalated and Case_EscalationNotes columns; queue item creation and owner-change audit.

Detail in the observability zone below.

Grounding:
- https://learn.microsoft.com/power-platform/admin/manage-dataverse-auditing
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla

### batch_processing
None — escalation is entirely event-driven. The SLA KPI "Nearing Non-compliance" warning fires the escalation flow for each individual case as its threshold is reached. No scheduled flow, batch job, or high-volume bulk-processing mechanism is required by the approved requirement set.

### reporting
OOB model-driven dashboard and views only — the supervisor escalations dashboard and active escalations view (both OOB config-level, no Power BI) fully satisfy REQ-0007's requirement for a real-time operational list sorted by urgency. No external Power BI dataset or report is introduced because the approved requirements call only for an operational visibility surface, not an analytical reporting store.

Grounding:
- https://learn.microsoft.com/power-apps/maker/model-driven-apps/create-edit-dashboards
<!-- /FILL -->

<!-- FILL:solution -->
- **components:**
  - `Case_Escalated column` (component_type: schema_column) — Boolean column on the Case table; stores the escalation state set by the escalation trigger flow; default false; read-only to front-line agents (REQ-0005).
  - `Case_EscalationNotes column` (component_type: schema_column) — Multi-line text column on the Case table; stores escalation internal notes and supervisor commentary; column-security-enabled via EscalationNotes FieldSecurityProfile (REQ-0008).
  - `EscalationNotes FieldSecurityProfile` (component_type: sec_field_profile) — Dataverse column security profile for Case_EscalationNotes; grants Create/Read/Update to Supervisor and Manager roles only; denies access to Agent role and portal users (REQ-0008).
  - `Supervisor security role` (component_type: sec_role) — Least-privilege Dynamics 365 security role for team supervisors; grants Case read/write, supervisor queue access, EscalationNotes FieldSecurityProfile, and dashboard access; created as part of this solution if not pre-existing (REQ-0008 prerequisite).
  - `Manager security role` (component_type: sec_role) — Least-privilege Dynamics 365 security role for managers; same EscalationNotes field-profile access as Supervisor; created as part of this solution if not pre-existing (REQ-0008 prerequisite).
  - `SLA escalation warning item` (component_type: config_sla) — Extends the enhanced SLA (from FEAT-02/DES-01) with a "Nearing Non-compliance" warning-time action on the resolution KPI; warning time configured at 80% of the SLA resolution KPI failure duration per OQ-005-1 (Option A); action invokes the escalation trigger flow (REQ-0005).
  - `Supervisor escalation queue` (component_type: config_queue) — Dedicated private queue for escalated cases; accessible only to members with Supervisor or Manager role; used as re-assignment target by the escalation trigger flow (REQ-0005).
  - `Escalation trigger flow` (component_type: flow_cloud) — Cloud flow invoked by the SLA warning action; reads Case_Escalated for idempotency (skips if already true); when false: sets Case_Escalated=true, moves case to supervisor queue, records `CaseEscalated` event timestamp; uses Dataverse connector; chains to supervisor notification flow (REQ-0005).
  - `Supervisor notification flow` (component_type: flow_cloud) — Cloud flow invoked by the escalation trigger flow; resolves the assigned supervisor for the case's team; if found: sends email via Office 365 Outlook connector and Teams message via Teams connector, both containing case number, customer name, and remaining SLA breach time; if not found: records `SupervisorNotificationSkipped`; target delivery ≤60s (REQ-0006 NFR).
  - `Case main form — Escalation section` (component_type: uiux_form) — Adds an Escalation section to the existing Case main form containing the Case_Escalated indicator (read-only Boolean) and Case_EscalationNotes field (hidden by FieldSecurityProfile for non-Supervisor/Manager users); visibility controlled by the escalation section business rule (REQ-0007, REQ-0008).
  - `Active escalations view` (component_type: uiux_view) — Model-driven system view on Case; filter: Case_Escalated=true AND Status=Active; sort: remaining SLA breach time ascending; columns: Case Number, Customer, Priority, Remaining Time to Breach (REQ-0007).
  - `Supervisor escalations dashboard` (component_type: uiux_dashboard) — Model-driven system dashboard embedding the active escalations view and a chart for escalation urgency distribution; accessible to Supervisor and Manager roles in the Customer Service app (REQ-0007).
  - `Escalation section visibility business rule` (component_type: config_business_rule) — Server-side business rule on Case; shows the Escalation section on the Case main form only when Case_Escalated=true, keeping the form uncluttered for non-escalated cases without JavaScript.
  - `Teams connection reference` (component_type: integ_connection_ref) — Solution-aware connection reference for the Microsoft Teams connector used by the notification flow; rebound per deployment environment.
  - `Outlook connection reference` (component_type: integ_connection_ref) — Solution-aware connection reference for the Office 365 Outlook connector used by the notification flow; rebound per deployment environment.
  - `FEAT-03 ALM solution` (component_type: alm_solution) — Custom publisher unmanaged solution wrapping all the above components; exported as managed for Test/UAT/Prod promotion; publisher prefix aligns with existing convention from FEAT-02 solution.

- **data_model:**
  - Case table (existing): add `cr_escalated` (Boolean, default false — Case_Escalated), add `cr_escalation_notes` (multi-line text, column-security-enabled — Case_EscalationNotes).
  - SLA KPI Instance table (Dataverse-managed): provides the failure time and warning-time trigger; the 80% threshold is expressed as a fixed warn duration per SLA item (warn duration = 80% of each KPI's failure time, e.g., Gold 4h resolve → warn at 3h12m, Silver 8h → warn at 6h24m).
  - Queue / Queue Item (existing): supervisor escalation queue is created; queue items are generated when the escalation trigger flow re-assigns case ownership to the supervisor queue.

- **security[]:**
  - EscalationNotes FieldSecurityProfile: Read/Create/Update → Supervisor role; Read/Create/Update → Manager role. No access → Agent role; no access → portal user.
  - Supervisor security role: Case (Read/Write for owned and team cases), SLA KPI Instance (Read), Queue Item (Read/Create), EscalationNotes FieldSecurityProfile, dashboard access.
  - Manager security role: equivalent to Supervisor with potential additional reporting scope.
  - Escalation/notification flow service account: Case (Read + Write cr_escalated only), Queue Item (Create), SLA KPI Instance (Read); Teams and Outlook connection references bound to environment-appropriate M365 service accounts.
  - Config admin: Customer Service Manager or System Administrator for SLA/queue/profile configuration; System Customizer for schema/form changes.

- **integration[]:**
  - Office 365 Outlook connector (Power Automate first-party): sends email notification to supervisor.
  - Microsoft Teams connector (Power Automate first-party): sends Teams direct message or channel notification to supervisor.
  - Both connectors stay within the Microsoft 365 / Power Platform boundary; no external gateway or API Management layer is introduced.

- **test_strategy[]:**
  - REQ-0005 scenarios: test SLA warning event triggers escalation trigger flow; verify Case_Escalated=true and case queue = supervisor escalation queue on the saved Case record; verify no duplicate escalation when the flow is re-triggered for an already-escalated case; verify no escalation for a case resolved before the threshold.
  - REQ-0006 scenarios: test notification flow dispatches both email and Teams message within 60 seconds of CaseEscalated timestamp; verify message content includes case number, customer name, and remaining time to breach, and nothing more sensitive; test flow skips notification and records SupervisorNotificationSkipped when no supervisor is configured.
  - REQ-0007 scenarios: verify active escalations view shows only escalated open cases sorted ascending by remaining breach time; verify empty-state view when no escalated cases; verify a resolved escalated case is removed from the view.
  - REQ-0008 scenarios: verify EscalationNotes field is visible and readable for users with Supervisor and Manager roles; verify field is invisible and not returned via API for Agent role; verify field is not exposed through portal API responses for the case customer.
<!-- /FILL -->

<!-- FILL:observability -->
- **events:**
  - `CaseEscalated` — emitted by the escalation trigger flow when Case_Escalated is set to true and the case is moved to the supervisor queue. Payload: case ID, team ID, escalation timestamp, SLA KPI Instance ID. Recorded as a flow run history entry and optionally as a Dataverse activity or custom event record.
  - `SupervisorNotificationSent` — emitted by the notification flow when both email and Teams message are successfully dispatched. Payload: case ID, supervisor user ID, notification timestamp, delivery channels (email, Teams).
  - `SupervisorNotificationSkipped` — emitted by the notification flow when no supervisor is found for the case's team. Payload: case ID, team ID, skipped timestamp. Recorded in flow run history and optionally as a warning log entry on the Case record.

- **metrics:**
  - `escalation_notification_latency` — seconds between `CaseEscalated` timestamp and `SupervisorNotificationSent` timestamp for each case; target ≤60s per REQ-0006 NFR. Measured from Power Automate flow run start/end timestamps and Case record timestamps.
  - `active_escalated_cases_count` — count of Case records with Case_Escalated=true and Status=Active; monitored via the supervisor escalations dashboard view and Dataverse query.
  - `notification_failure_count` — count of `SupervisorNotificationSkipped` events plus flow run failures for the notification flow; operational health indicator for supervisor coverage gaps.

- **traces:**
  - Correlate: Case record ID ↔ SLA KPI Instance record (via KPI instance lookup on Case) ↔ escalation trigger flow run ID ↔ queue item created by the flow ↔ notification flow run ID, using the Case ID as the primary correlation key across all Power Automate run history entries and Dataverse records.
  - Flow runs include the Case ID in run metadata so traces can be reconstructed from Power Automate monitoring or the Dataverse audit log.

- **alerts:**
  - Escalation trigger flow run failure rate > 0: operational alert requiring immediate investigation; a failure means a case may not have been escalated despite reaching the SLA warning threshold.
  - Notification flow run failure rate > 0: operational alert indicating a supervisor may not have been notified.
  - `escalation_notification_latency` > 60s for any case: NFR breach for REQ-0006; alert supervisor or platform administrator.
  - Active escalated case backlog growth without corresponding queue activity over a configurable observation window: escalation queue health degradation indicator.

- **audit:**
  - Enable Dataverse auditing on `cr_escalated` and `cr_escalation_notes` columns on the Case table: records who changed the escalation state and who read or modified escalation notes, providing the audit trail required by REQ-0008.
  - Enable audit on Case record owner changes (queue re-assignment) and queue item creation for the supervisor escalation queue.
  - Retain Power Automate flow run history for both escalation and notification flows as the execution trace for each escalation and notification event (supports Stage 5 verification of the REQ-0006 60-second NFR).
<!-- /FILL -->

<!-- FILL:open-questions -->
- [x] **OQ-005-1** (DECIDED — avi-k-mishra@github, 2026-07-22): Escalation trigger threshold is **Option A — 80% of the SLA resolution KPI time elapsed**, configured as a fixed warn duration on each SLA item. For the three SLA tiers defined in FEAT-02/DES-01: Gold (4h resolve) → warn at 3h12m; Silver (8h resolve) → warn at 6h24m; Bronze (next business day, ~8h) → warn at approximately 6h24m of business hours. Rationale: proportional warning time scales correctly across all three SLA tiers, providing adequate supervisor response windows. A fixed 30-minute warning (Option B) is operationally insufficient for a 1-hour SLA tier or other short SLA durations that may be added in future. The warn duration is set via the "Warn and Fail Duration" fields on each enhanced SLA item.
  - Grounding: https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla

- [x] **OQ-DES-02-1** (DECIDED — avi-k-mishra@github, 2026-07-22): The Supervisor and Manager security roles are created as components of this solution (as new roles) if they do not exist in the target environment. They are included as explicit `sec_role` components in the FEAT-03 ALM solution so they will be created/updated on managed import. Administrators must assign users to these roles per environment as operational setup after deployment. No Dynamics 365 system roles are modified; only new custom roles are added.
<!-- /FILL -->

---

## Traceability (FEAT ← REQ ← INTK)

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Intake Batch | Feature |
|-----|-------|--------------|--------|
| REQ-0005 | Automatic Case Escalation Before SLA Breach | INTK-0002 | FEAT-03 |
| REQ-0006 | Supervisor Notification on Case Escalation | INTK-0002 | FEAT-03 |
| REQ-0007 | Supervisor Dashboard for Active Escalations | INTK-0002 | FEAT-03 |
| REQ-0008 | Role-Based Access Control for Escalation Notes | INTK-0002 | FEAT-03 |
<!-- COMPILER:END traceability -->

## NFR carry-over

<!-- COMPILER:BEGIN nfr -->
| Metric | Target | Source REQ |
|--------|--------|------------|
| agent_response | Escalation notifications are delivered to the assigned supervisor within 60 seconds of the escalation event. | REQ-0006 |
<!-- COMPILER:END nfr -->

## Provenance

<!-- COMPILER:BEGIN provenance -->
| Design | Feature | Member REQs |
|--------|---------|-------------|
| DES-02 | FEAT-03 | REQ-0005, REQ-0006, REQ-0007, REQ-0008 |
<!-- COMPILER:END provenance -->
