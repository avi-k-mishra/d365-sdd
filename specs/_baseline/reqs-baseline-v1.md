# Requirements Baseline v1

| Field | Value |
|-------|-------|
| Baseline version | v1 |
| Date | 2026-07-15 |
| Approver | avinam@microsoft.com, 2026-07-15 |
| Status | approved |

## Requirements in scope

| ID | Title | SHA-256 (source doc) | Status |
|----|-------|----------------------|--------|
| REQ-0001 | Agent-Initiated Case Creation from Incoming Email | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | approved |
| REQ-0002 | Auto-Population of Customer from Sender Email Address Match | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | approved |
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | approved |
| REQ-0004 | Automatic Case Escalation on SLA Breach | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | approved |

## Feature specs compiled

| Feature | Title | Spec hash | Status |
|---------|-------|-----------|--------|
| FEAT-01 | Case Creation from Email | 61786ac57296e463d0f10f0c9bddd3b28e41d9a8d9f9d0a33f701ac11869c16f | approved |
| FEAT-02 | Tiered SLA & Escalation | 60140d8bce06910b5b376ac71d128299badf6c15a3c664f0fc39f00fd628dcb6 | approved |

## Decisions recorded

All open questions have been resolved prior to Gate 2 approval:

- **OQ-003-1** (REQ-0003): Tier-to-priority mapping — Gold→High, Silver→Normal, Bronze→Low, Default→Normal. Decided by avinam@microsoft.com, 2026-07-15.
- **OQ-004-1** (REQ-0004): SLA durations per tier — Gold: 1 h first response / 4 h resolution; Silver: 4 h / 8 h; Bronze: 8 h / next business day. Decided by avinam@microsoft.com, 2026-07-15.

## Note

All four requirements are fully grounded on Microsoft Learn, acceptance scenarios include concrete tier values and SLA durations, and all NFRs are expressed as structured `{ metric, target }` objects.

**Do NOT merge this PR without human review and Gate 2 sign-off.**
