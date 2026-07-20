---
id: FEAT-03
title: "Automated Case Escalation & Supervisor Notifications"
epic: EPIC-01
member_reqs: [REQ-0005, REQ-0006, REQ-0007, REQ-0008]
spec_hash: "c0ab09ecd8d7d04d27f6f58a8910a5e206499b8fdff4dca7c7b13f6cd3759d8c"
status: approved
---

<!-- FILL:intent -->
This feature defines proactive case escalation before SLA breach, supervisor
notification on escalation, operational visibility of active escalations, and
access control for escalation-only internal notes. It extends the established
SLA baseline with escalation operations while preserving role-based security
boundaries for escalation content (REQ-0005, REQ-0006, REQ-0007, REQ-0008).
<!-- /FILL -->

<!-- FILL:scope -->
In:
- Escalating open cases before SLA breach using the agreed threshold once decided (REQ-0005)
- Notifying assigned supervisors via email and Teams with required case context when escalation occurs (REQ-0006)
- Listing active escalated cases in urgency order on a supervisor-facing dashboard (REQ-0007)
- Restricting escalation notes and supervisor commentary visibility to Supervisor/Manager roles only (REQ-0008)
- Enforcing dependence on the existing SLA definitions that provide breach-time inputs for escalation logic (REQ-0005..REQ-0008 dependency on REQ-0004)

Out:
- Selection of a concrete escalation threshold while OQ-005-1 remains undecided
- Platform implementation design choices for notification transport, dashboard implementation, or access-control mechanism
- Any changes to existing SLA definitions captured by prior approved requirements
<!-- /FILL -->

<!-- FILL:grounding -->
Grounded only on reviewed requirement evidence and recorded decisions in this repository:
- REQ-0005, REQ-0006, REQ-0007, REQ-0008 (source: intake/test/2026-07-20/case-escalation-spec.md)
- Dependency on existing SLA definitions via REQ-0004
- No external product-feasibility or implementation guidance is used at this stage
<!-- /FILL -->

<!-- FILL:open-decisions -->
- [ ] **OQ-005-1** (REQ-0005): escalation trigger threshold remains undecided.
  - **Option A**: 80% of total SLA time elapsed
  - **Option B**: fixed 30 minutes before SLA breach
  - **Build implication**: Option A requires percentage-based thresholding; Option B requires absolute-time thresholding.

Dependency note:
- REQ-0008 assumes Supervisor and Manager security roles exist as a prerequisite; if missing, those roles must be defined before implementation.
<!-- /FILL -->

---

## Traceability

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Type | Priority | Status |
|-----|-------|------|----------|--------|
| REQ-0005 | Automatic Case Escalation Before SLA Breach | functional | Must | approved |
| REQ-0006 | Supervisor Notification on Case Escalation | integration | Must | approved |
| REQ-0007 | Supervisor Dashboard for Active Escalations | functional | Must | approved |
| REQ-0008 | Role-Based Access Control for Escalation Notes | security | Must | approved |
<!-- COMPILER:END traceability -->

## Acceptance scenarios

<!-- COMPILER:BEGIN scenarios -->
```gherkin
Feature: Automatic pre-breach case escalation

  Scenario: happy — open case is escalated when it approaches the SLA resolution deadline
    Given an open case has an active SLA resolution KPI
    And the case has not yet been escalated
    And the case is approaching the SLA resolution deadline (at the agreed escalation threshold — see open question OQ-005-1)
    When the system evaluates the SLA warning threshold
    Then the case is automatically reassigned to the supervisor queue for its team
    And the "Escalated" flag on the case is set to true
    And no agent action was required to trigger the escalation

  Scenario: negative — case already marked Escalated is not escalated again
    Given a case that already has the "Escalated" flag set to true
    When the system re-evaluates the SLA warning threshold for that case
    Then no duplicate escalation action is triggered
    And the case queue and Escalated flag remain unchanged

  Scenario: boundary — case resolved before the escalation threshold is reached
    Given an open case has an active SLA resolution KPI
    And the case has not yet reached the escalation threshold
    When the case is resolved by an agent
    Then no escalation action is triggered
    And the case remains in its original assigned queue with Escalated flag false

Feature: Supervisor notification on case escalation

  Scenario: happy — supervisor receives both email and Teams notification upon escalation
    Given a case has just been escalated (Escalated flag set to true)
    And the case's team has an assigned supervisor
    When the escalation notification action fires
    Then the assigned team supervisor receives an email containing the case number, customer name, and remaining time to breach
    And the assigned team supervisor receives a Microsoft Teams message containing the case number, customer name, and remaining time to breach
    And both notifications are delivered within 1 minute of the escalation event

  Scenario: negative — no notification is sent when no supervisor is assigned to the team
    Given a case has been escalated
    And no supervisor is configured for the case's team
    When the notification action fires
    Then no email or Teams message is sent
    And the system records that no supervisor was found for notification

  Scenario: boundary — notification contains exactly the three required fields and nothing more sensitive
    Given a case has been escalated
    When the notification message is generated
    Then the notification includes the case number
    And the notification includes the customer name
    And the notification includes the remaining time to SLA breach
    And the notification does not include any internal escalation notes or supervisor commentary

Feature: Escalated cases dashboard

  Scenario: happy — dashboard displays all escalated cases ordered by urgency
    Given multiple open cases with the "Escalated" flag set, each with a different remaining time to SLA breach
    When a supervisor opens the escalations dashboard
    Then all currently escalated cases are listed on the dashboard
    And the cases are sorted with the case having the shortest remaining time to breach at the top
    And each row shows sufficient information to identify and act on the case

  Scenario: negative — dashboard shows an empty state when no cases are currently escalated
    Given no open cases have the "Escalated" flag set to true
    When a supervisor opens the escalations dashboard
    Then the dashboard displays an empty list
    And a message or indicator communicates that there are no currently escalated cases

  Scenario: boundary — a resolved escalated case is removed from the dashboard
    Given a case is shown on the escalations dashboard with the "Escalated" flag set
    When the case is resolved by a supervisor or agent
    Then the case is no longer listed on the escalations dashboard
    And the remaining cases retain their sort order by remaining time to breach

Feature: Escalation notes access control

  Scenario: happy — user with Supervisor role can read escalation internal notes
    Given a case has escalation internal notes and supervisor commentary recorded
    And the current user has the Supervisor security role
    When the user views the case record
    Then the escalation internal notes and supervisor commentary are visible to the user

  Scenario: happy — user with Manager role can read escalation internal notes
    Given a case has escalation internal notes and supervisor commentary recorded
    And the current user has the Manager security role
    When the user views the case record
    Then the escalation internal notes and supervisor commentary are visible to the user

  Scenario: negative — front-line agent cannot read escalation internal notes
    Given a case has escalation internal notes and supervisor commentary recorded
    And the current user has only the front-line Agent security role (not Supervisor or Manager)
    When the user views the case record
    Then the escalation internal notes and supervisor commentary are NOT visible in the UI
    And no escalation note content is returned via any API or export accessible to an agent-role user

  Scenario: negative — customer cannot read escalation internal notes via the portal
    Given a case has escalation internal notes and supervisor commentary recorded
    And the requestor is the case's customer accessing the case via the customer self-service portal
    When the customer views their case
    Then no escalation internal notes or supervisor commentary are visible on the portal
    And no escalation note content is exposed through any portal API response

  Scenario: boundary — user holding both Agent and Supervisor roles is granted access
    Given a case has escalation internal notes recorded
    And the current user holds both the Agent role and the Supervisor role
    When the user views the case record
    Then the escalation internal notes are visible (the Supervisor role grants access)
```
<!-- COMPILER:END scenarios -->

## NFR table

<!-- COMPILER:BEGIN nfr -->
| Metric | Target | Source REQ |
|--------|--------|------------|
| agent_response | Escalation notifications are delivered to the assigned supervisor within 60 seconds of the escalation event. | REQ-0006 |
<!-- COMPILER:END nfr -->

## Dependency graph

<!-- COMPILER:BEGIN deps -->
REQ-0005 → REQ-0004
REQ-0006 → REQ-0004, REQ-0005
REQ-0007 → REQ-0004, REQ-0005
REQ-0008 → REQ-0004, REQ-0005
<!-- COMPILER:END deps -->

## Provenance

<!-- COMPILER:BEGIN provenance -->
| REQ | Source File | SHA-256 | Location |
|-----|-------------|---------|----------|
| REQ-0005 | intake/test/2026-07-20/case-escalation-spec.md | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | section 2.1 Automatic escalation before SLA breach |
| REQ-0006 | intake/test/2026-07-20/case-escalation-spec.md | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | section 2.2 Supervisor notification |
| REQ-0007 | intake/test/2026-07-20/case-escalation-spec.md | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | section 2.3 Escalations dashboard |
| REQ-0008 | intake/test/2026-07-20/case-escalation-spec.md | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | section 3 Security & Access |
<!-- COMPILER:END provenance -->
