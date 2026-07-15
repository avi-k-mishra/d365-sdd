# Feature & Epic Index — Baseline v1

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

## Open questions blocking Stage 3
None. All open questions (OQ-003-1, OQ-004-1) have been resolved — decided by avinam@microsoft.com, 2026-07-15. Stage 3 design can proceed.
