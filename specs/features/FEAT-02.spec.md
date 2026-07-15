---
id: FEAT-02
title: "Tiered SLA & Escalation"
epic: EPIC-01
member_reqs: [REQ-0003, REQ-0004]
spec_hash: "12928460caf0e42eeedc8c42555b75f8b6d7052a0d5793b8ae0061ec8f74df93"
status: reviewed
---

<!-- FILL:intent -->
This feature ensures that each case receives a priority reflecting the customer's
contracted service tier and that the system automatically escalates the case to a
supervisor queue when the configured SLA resolution time is breached. It closes the
gap between case creation (FEAT-01) and accountable SLA enforcement, protecting
service commitments and enabling proactive management (REQ-0003, REQ-0004).
<!-- /FILL -->

<!-- FILL:scope -->
In:
- Tier-to-priority mapping applied at case creation (via ARC rule action or workflow)
- SLA KPI definition (e.g. "Resolve By") applied per case priority / tier
- SLA KPI failure actions: setting "Is Escalated" flag and notifying the supervisor queue
- SLA KPI pause behaviour when case status is "On Hold"
- Default priority ("Normal") when no tier is defined on the customer record

Out:
- Service tier master data management (Customer/Account tier field ownership is out of scope)
- Definition of tier names and SLA durations — these are open questions (OQ-003-1, OQ-004-1)
  that must be resolved by the customer before Stage 3 design can proceed
- Routing cases to specific agents after escalation (separate routing configuration)
- Email case creation (owned by FEAT-01)
<!-- /FILL -->

<!-- FILL:grounding -->
Dynamics 365 Customer Service enhanced SLAs support KPI-level failure actions, including
setting the "Is Escalated" field on a Case and triggering notifications, using the
built-in SLA item failure action workflow. SLA KPIs can be scoped per case priority,
enabling tier-differentiated SLA targets. The platform also supports pause-and-resume
behaviour via SLA KPI pause conditions.

- https://learn.microsoft.com/dynamics365/customer-service/administer/define-service-level-agreements
- https://learn.microsoft.com/dynamics365/customer-service/administer/create-enhanced-sla
<!-- /FILL -->

<!-- FILL:open-decisions -->
The following open questions must be resolved by the customer before Stage 3 design:

- **OQ-003-1** (from REQ-0003): Customer service tier names and their mapping to Dynamics 365
  case priority values are undefined. Three options proposed (Gold/Silver/Bronze → High/Normal/Low,
  or a four-tier model, or customer-defined labels). Without this decision, the ARC rule
  action "Set Priority" and the SLA KPI applicability filter cannot be authored.

- **OQ-004-1** (from REQ-0004): SLA durations per tier (first response and resolution time)
  are undefined, contingent on OQ-003-1. Without this decision, "Failure After" values in the
  SLA items and the supervisor queue assignment for escalation notifications cannot be configured.
<!-- /FILL -->

---

## Traceability

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Type | Priority | Status |
|-----|-------|------|----------|--------|
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | functional | Must | reviewed |
| REQ-0004 | Automatic Case Escalation on SLA Breach | functional | Must | reviewed |
<!-- COMPILER:END traceability -->

## Acceptance scenarios

<!-- COMPILER:BEGIN scenarios -->
```gherkin
Feature: Tier-driven case priority assignment

  Scenario: happy — case priority set automatically from customer tier
    Given a Case is created for a customer with a defined service tier
    And the tier-to-priority mapping has been configured in the system
    When the case is saved
    Then the Case "Priority" field is automatically set to the value mapped from the customer's tier

  Scenario: negative — customer has no tier defined
    Given a Case is created for a customer with no service tier on record
    When the case is saved
    Then the Case "Priority" field defaults to "Normal"
    And no error or blocking validation is raised

  Scenario: boundary — customer tier changes after case creation
    Given a Case exists with a priority set from the customer's original service tier
    When the customer's service tier is updated to a different value
    Then the existing case priority is NOT retroactively changed
    And only Cases created after the tier update reflect the new tier mapping

Feature: Automatic case escalation on SLA breach

  Scenario: happy — case escalated when SLA failure time is reached
    Given a Case has an active SLA KPI with a configured failure time
    And the case is not resolved before the failure time elapses
    When the SLA KPI timer reaches the failure threshold
    Then the "Is Escalated" flag on the case is set to Yes
    And the SLA failure action triggers a notification to the assigned supervisor queue
    And the case status is updated to reflect the escalation

  Scenario: negative — SLA KPI paused while case is on hold
    Given a Case has an active SLA KPI
    And the case status is changed to "On Hold"
    When the SLA KPI pause condition is triggered
    Then the SLA timer is paused and elapsed time stops increasing
    And the escalation deadline is recalculated when the case status is returned to active

  Scenario: boundary — case resolved at exactly the SLA failure boundary
    Given a Case has an active SLA KPI
    And the case is resolved at the exact moment the failure time is reached
    When the SLA KPI evaluates success criteria
    Then the success criteria are considered met
    And no escalation action is triggered
    And the KPI instance is marked as succeeded
```
<!-- COMPILER:END scenarios -->

## NFR table

<!-- COMPILER:BEGIN nfr -->
| Metric | Target | Source REQ |
|--------|--------|------------|
| agent_response | SLA KPI failure action fires within 5 minutes of the failure threshold being crossed | REQ-0004 |
<!-- COMPILER:END nfr -->

## Dependency graph

<!-- COMPILER:BEGIN deps -->
REQ-0003 → REQ-0001
REQ-0004 → REQ-0001, REQ-0003
<!-- COMPILER:END deps -->

## Provenance

<!-- COMPILER:BEGIN provenance -->
| REQ | Source File | SHA-256 | Location |
|-----|-------------|---------|----------|
| REQ-0003 | intake/test/2026-07-09/case-management-spec.docx | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | section 2.2 SLA |
| REQ-0004 | intake/test/2026-07-09/case-management-spec.docx | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | section 2.2 SLA |
<!-- COMPILER:END provenance -->
