---
id: FEAT-01
title: "Case Creation from Email"
epic: EPIC-01
member_reqs: [REQ-0001, REQ-0002]
spec_hash: "97b0e5a862e9ee70ac5314ae49761d3147f82e388fff113791fb94fd2549ca42"
status: reviewed
---

<!-- FILL:intent -->
This feature enables the Dynamics 365 Customer Service system to automatically
create a case from an inbound email and identify the sending customer, reducing
manual data-entry effort for service agents and ensuring every email generates a
traceable case record. It delivers the foundational case-creation capability on
which all downstream triage, routing, and SLA tracking depends (REQ-0001, REQ-0002).
<!-- /FILL -->

<!-- FILL:scope -->
In:
- Automatic Record Creation (ARC) rule configuration to convert inbound emails to cases
- Auto-population of the Case "Customer" field from sender email address matching Contact/Account records
- Linking the originating email activity to the case timeline
- Handling of unknown senders (no case created if "Create contact for unknown sender" is disabled)

Out:
- Case priority assignment (owned by FEAT-02)
- SLA configuration and escalation (owned by FEAT-02)
- Routing of cases to specific queues beyond the ARC rule's monitored queue
- Manual case creation via the Case form (supported by D365 out of the box; not in scope for automation)
<!-- /FILL -->

<!-- FILL:grounding -->
The Automatic Record Creation and Update Rules feature in Dynamics 365 Customer
Service supports converting inbound email activities to case records, with
configurable conditions and actions including customer lookup from sender email.
The "Customer" field resolution (Contact vs Account precedence) is a documented
platform behaviour.

- https://learn.microsoft.com/dynamics365/customer-service/administer/automatically-create-update-records
- https://learn.microsoft.com/troubleshoot/dynamics-365/customer-service/email/incoming-email-not-converted-case
<!-- /FILL -->

<!-- FILL:open-decisions -->
None. All scenarios for this feature are fully grounded on Microsoft Learn. No
open ambiguities remain in REQ-0001 or REQ-0002 that block Stage 3 design.
<!-- /FILL -->

---

## Traceability

<!-- COMPILER:BEGIN traceability -->
| REQ | Title | Type | Priority | Status |
|-----|-------|------|----------|--------|
| REQ-0001 | Agent-Initiated Case Creation from Incoming Email | functional | Must | reviewed |
| REQ-0002 | Auto-Population of Customer from Sender Email Address Match | functional | Must | reviewed |
<!-- COMPILER:END traceability -->

## Acceptance scenarios

<!-- COMPILER:BEGIN scenarios -->
```gherkin
Feature: Agent-initiated case creation from email

  Scenario: happy — ARC rule creates case from inbound email
    Given an email arrives in the monitored support queue
    And an active Automatic Record Creation rule is configured for that queue with activity type "Email"
    When the ARC rule evaluates the inbound email
    Then a new Case record is created in Dynamics 365 Customer Service
    And the originating email activity is linked to the case timeline

  Scenario: negative — email from unknown sender with contact creation disabled
    Given an email arrives from an address not matching any Contact or Account
    And the "Create contact for unknown sender" option is disabled on the ARC rule
    When the ARC rule evaluates the email
    Then no Case is created
    And the email activity remains in the queue without a linked case

  Scenario: boundary — email with empty body
    Given an email arrives with a non-empty subject line but an empty body
    And an active ARC rule is configured for that queue
    When the ARC rule evaluates the email
    Then a Case is created using the subject as the case title
    And the case description field is left empty

Feature: Auto-population of customer from sender email

  Scenario: happy — sender email matches a known Contact
    Given an email arrives in the monitored support queue
    And the sender address matches the primary email of an existing Contact record
    When the ARC rule creates a new Case
    Then the "Customer" field on the case is auto-populated with that Contact
    And no manual customer lookup by the agent is required

  Scenario: negative — sender email matches no Contact or Account
    Given an email arrives from an address not matching any Contact or Account
    And the "Create contact for unknown sender" option is disabled on the ARC rule
    When the ARC rule creates a Case (if conditions allow)
    Then the "Customer" field on the case remains empty
    And the agent must manually set the customer

  Scenario: boundary — sender email address is associated with both a Contact and an Account
    Given an email arrives from an address linked to both a Contact and an Account record
    When the ARC rule creates a new Case
    Then the "Customer" field is resolved to the Account record
    And the Contact remains visible on the case timeline via the linked email activity
```
<!-- COMPILER:END scenarios -->

## NFR table

<!-- COMPILER:BEGIN nfr -->
| Metric | Target | Source REQ |
|--------|--------|------------|
| (none) | — | — |
<!-- COMPILER:END nfr -->

## Dependency graph

<!-- COMPILER:BEGIN deps -->
REQ-0002 → REQ-0001
<!-- COMPILER:END deps -->

## Provenance

<!-- COMPILER:BEGIN provenance -->
| REQ | Source File | SHA-256 | Location |
|-----|-------------|---------|----------|
| REQ-0001 | intake/test/2026-07-09/case-management-spec.docx | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | section 2.1 Case Creation |
| REQ-0002 | intake/test/2026-07-09/case-management-spec.docx | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | section 2.1 Case Creation |
<!-- COMPILER:END provenance -->
