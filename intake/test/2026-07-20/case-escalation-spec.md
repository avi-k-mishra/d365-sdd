# Automated Case Escalation & Supervisor Notifications

**Customer:** Contoso Support Operations
**Prepared by:** Service Delivery team
This document specifies a new capability for the Dynamics 365 Customer Service application. It builds on the existing case management and SLA capabilities.

## 1. Background & Goal
Support supervisors currently discover SLA breaches only after they happen. The business wants cases that are approaching their SLA deadline to be escalated automatically to a supervisor before the breach occurs, so a supervisor can intervene in time.

## 2. Functional Requirements

### 2.1 Automatic escalation before SLA breach
When an open case is approaching its SLA resolution deadline, the system must automatically escalate the case: reassign it to the supervisor queue for its team and set an "Escalated" flag. The escalation must happen automatically without an agent taking any action.

> OPEN ITEM: The business has not yet agreed on how close to the deadline the escalation should trigger. Some supervisors suggested at 80% of the SLA time elapsed; others suggested a fixed 30 minutes before breach. This threshold needs to be decided.

### 2.2 Supervisor notification
When a case is escalated, the assigned team supervisor must be notified via email and via a Microsoft Teams message. The notification must include the case number, customer name, and remaining time to breach.

Performance expectation: the notification should reach the supervisor quickly - within about one minute of the escalation.

### 2.3 Escalations dashboard
Supervisors need a dashboard view listing all currently escalated cases, sorted by the shortest remaining time to breach first, so the most urgent cases are at the top.

## 3. Security & Access
Escalation internal notes and the supervisor commentary on an escalated case must be visible only to users in the Supervisor and Manager roles. Front-line agents and customers must never be able to read these internal escalation notes.

## 4. Dependencies
This capability depends on the existing SLA definitions already captured for case management (the SLA resolution deadline is the input to the escalation timing).
