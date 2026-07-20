# Feature & Epic Index — Baseline v2

## EPIC-01: Automated Case Management

Goal: Enable Dynamics 365 Customer Service to automatically create, classify, and
escalate cases from inbound email with minimal manual intervention.

### FEAT-01: Case Creation from Email
Scope: Automatic case creation via ARC rules on inbound email; customer auto-population
from sender email match.

| REQ | Title | Type | Priority |
|-----|-------|------|----------|
| REQ-0001 | Agent-Initiated Case Creation from Incoming Email | functional | Must |
| REQ-0002 | Auto-Population of Customer from Sender Email Address Match | functional | Must |

Dependency graph: REQ-0002 → REQ-0001

---

### FEAT-02: Tiered SLA & Escalation
Scope: Tier-driven case priority assignment; SLA KPI configuration; automatic escalation
on SLA breach.

| REQ | Title | Type | Priority |
|-----|-------|------|----------|
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | functional | Must |
| REQ-0004 | Automatic Case Escalation on SLA Breach | functional | Must |

Dependency graph: REQ-0003 → REQ-0001; REQ-0004 → REQ-0001, REQ-0003

---

### FEAT-03: Automated Case Escalation & Supervisor Notifications
Scope: Pre-breach escalation triggering, supervisor notifications, escalation dashboard,
and role-based access control for escalation notes.

| REQ | Title | Type | Priority |
|-----|-------|------|----------|
| REQ-0005 | Automatic Case Escalation Before SLA Breach | functional | Must |
| REQ-0006 | Supervisor Notification on Case Escalation | integration | Must |
| REQ-0007 | Supervisor Dashboard for Active Escalations | functional | Must |
| REQ-0008 | Role-Based Access Control for Escalation Notes | security | Must |

Dependency graph: REQ-0005 → REQ-0004; REQ-0006 → REQ-0004, REQ-0005; REQ-0007 → REQ-0004, REQ-0005; REQ-0008 → REQ-0004, REQ-0005

---

## Open questions blocking Stage 3
- **OQ-005-1** (REQ-0005) is still open: escalation trigger threshold remains undecided between:
  - Option A: 80% of SLA elapsed
  - Option B: fixed 30 minutes before SLA breach
  Build implication: the SLA warning configuration differs between percentage-based and absolute-time thresholding.
