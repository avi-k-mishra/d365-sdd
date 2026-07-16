---
id: FEAT-02
title: "Tiered SLA & Escalation"
epic: EPIC-01
member_reqs: [REQ-0003, REQ-0004]
spec_hash: "21fa31c369310530339523fef0f25b39599ff2ef57ae373a898c2b08232d9038"
status: approved
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
- Tier-to-priority mapping applied at case creation (via ARC rule action or workflow): Gold→High, Silver→Normal, Bronze→Low, Default→Normal
- SLA KPI definition ("Resolve By" and "First Response By") applied per case priority / tier with the agreed durations (Gold: 1 h / 4 h; Silver: 4 h / 8 h; Bronze: 8 h / next business day)
- SLA KPI failure actions: setting "Is Escalated" flag and notifying the supervisor queue
- SLA KPI pause behaviour when case status is "On Hold"
- Default priority ("Normal") when no tier is defined on the customer record

Out:
- Service tier master data management (Customer/Account tier field ownership is out of scope)
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
All open questions for this feature have been resolved:

- **OQ-003-1** (DECIDED — avinam@microsoft.com, 2026-07-15): Tier-to-priority mapping confirmed as Gold→High, Silver→Normal, Bronze→Low, Default→Normal. The ARC rule action "Set Priority" and SLA KPI applicability filter can now be fully configured.

- **OQ-004-1** (DECIDED — avinam@microsoft.com, 2026-07-15): SLA durations per tier confirmed:
  | Tier | First response | Resolution |
  |------|----------------|-----------|
  | Gold | 1 h | 4 h |
  | Silver | 4 h | 8 h |
  | Bronze | 8 h | Next business day |

No open ambiguities remain in REQ-0003 or REQ-0004 that block Stage 3 design.
<!-- /FILL -->

---

## Traceability

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Type | Priority | Status |
|-----|-------|------|----------|--------|
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | functional | Must | approved |
| REQ-0004 | Automatic Case Escalation on SLA Breach | functional | Must | approved |
<!-- COMPILER:END traceability -->

## Acceptance scenarios

<!-- COMPILER:BEGIN scenarios -->
```gherkin
Feature: Tier-driven case priority assignment

  Scenario: happy — Gold-tier customer case set to High priority
    Given a Case is created for a customer whose service tier is "Gold"
    And the tier-to-priority mapping (Gold→High, Silver→Normal, Bronze→Low) is configured in the system
    When the case is saved
    Then the Case "Priority" field is automatically set to "High"

  Scenario: happy — Silver-tier customer case set to Normal priority
    Given a Case is created for a customer whose service tier is "Silver"
    And the tier-to-priority mapping is configured in the system
    When the case is saved
    Then the Case "Priority" field is automatically set to "Normal"

  Scenario: happy — Bronze-tier customer case set to Low priority
    Given a Case is created for a customer whose service tier is "Bronze"
    And the tier-to-priority mapping is configured in the system
    When the case is saved
    Then the Case "Priority" field is automatically set to "Low"

  Scenario: negative — customer has no tier defined
    Given a Case is created for a customer with no service tier on record
    When the case is saved
    Then the Case "Priority" field defaults to "Normal"
    And no error or blocking validation is raised

  Scenario: boundary — customer tier changes after case creation
    Given a Case exists with priority "High" set from the customer's original "Gold" service tier
    When the customer's service tier is updated to "Silver"
    Then the existing case priority remains "High" (NOT retroactively changed)
    And only Cases created after the tier update reflect the "Silver"→Normal mapping

Feature: Automatic case escalation on SLA breach

  Scenario: happy — Gold-tier case escalated when resolution SLA (4 h) is breached
    Given a Case has priority "High" (Gold tier) and an active SLA KPI with resolution "Failure After" = 4 hours
    And the case is not resolved within 4 hours of creation
    When the SLA KPI timer reaches the 4-hour failure threshold
    Then the "Is Escalated" flag on the case is set to Yes
    And the SLA failure action triggers a notification to the assigned supervisor queue
    And the case status is updated to reflect the escalation

  Scenario: happy — Silver-tier case escalated when resolution SLA (8 h) is breached
    Given a Case has priority "Normal" (Silver tier) and an active SLA KPI with resolution "Failure After" = 8 hours
    And the case is not resolved within 8 hours of creation
    When the SLA KPI timer reaches the 8-hour failure threshold
    Then the "Is Escalated" flag on the case is set to Yes
    And the SLA failure action triggers a notification to the assigned supervisor queue

  Scenario: happy — Bronze-tier case escalated when resolution SLA (next business day) is breached
    Given a Case has priority "Low" (Bronze tier) and an active SLA KPI with resolution "Failure After" = next business day
    And the case is not resolved by the next business day
    When the SLA KPI timer crosses the next-business-day threshold
    Then the "Is Escalated" flag on the case is set to Yes
    And the SLA failure action triggers a notification to the assigned supervisor queue

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
| sla_first_response_gold | First response within 1 hour for Gold (High priority) cases | REQ-0004 |
| sla_resolution_gold | Resolution within 4 hours for Gold (High priority) cases | REQ-0004 |
| sla_first_response_silver | First response within 4 hours for Silver (Normal priority) cases | REQ-0004 |
| sla_resolution_silver | Resolution within 8 hours for Silver (Normal priority) cases | REQ-0004 |
| sla_first_response_bronze | First response within 8 hours for Bronze (Low priority) cases | REQ-0004 |
| sla_resolution_bronze | Resolution by next business day for Bronze (Low priority) cases | REQ-0004 |
| escalation_action_latency | SLA KPI failure action fires within 5 minutes of the failure threshold being crossed | REQ-0004 |
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
