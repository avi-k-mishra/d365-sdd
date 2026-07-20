# Requirements Baseline v2

| Field | Value |
|-------|-------|
| Baseline version | v2 |
| Date | 2026-07-20 |
| Approver | pending Gate 2 review |
| Status | pending Gate 2 review |

## Requirements in scope

| ID | Title | SHA-256 (source doc) | Status |
|----|-------|----------------------|--------|
| REQ-0005 | Automatic Case Escalation Before SLA Breach | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | approved |
| REQ-0006 | Supervisor Notification on Case Escalation | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | approved |
| REQ-0007 | Supervisor Dashboard for Active Escalations | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | approved |
| REQ-0008 | Role-Based Access Control for Escalation Notes | 6436859ab6d7ef3bbd30b017c1ffbb0dbe635eff78d0a5a8ec4a725a48970dcf | approved |

## Feature specs compiled

| Feature | Title | Spec hash | Status |
|---------|-------|-----------|--------|
| FEAT-03 | Automated Case Escalation & Supervisor Notifications | c0ab09ecd8d7d04d27f6f58a8910a5e206499b8fdff4dca7c7b13f6cd3759d8c | approved |

## Decisions recorded

- **OQ-005-1** (REQ-0005): escalation trigger threshold is still open and remains a carry-forward decision for Stage 3:
  - Option A: 80% of SLA elapsed
  - Option B: fixed 30 minutes before SLA breach
- **REQ-0008 prerequisite**: Supervisor and Manager security roles must exist before implementation.

## Note

This baseline is grounded in the reviewed REQ evidence only. It preserves the unresolved OQ-005-1 and keeps this batch dependent on the established SLA definitions from earlier approved requirements.

**Do NOT merge this PR without human review and Gate 2 sign-off.**
