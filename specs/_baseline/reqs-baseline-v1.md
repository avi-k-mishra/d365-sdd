# Requirements Baseline v1

| Field | Value |
|-------|-------|
| Baseline version | v1 |
| Date | 2026-07-15 |
| Approver | *awaiting human Gate 2 review* |
| Status | reviewed — pending approval |

## Requirements in scope

| ID | Title | SHA-256 (source doc) | Status |
|----|-------|----------------------|--------|
| REQ-0001 | Agent-Initiated Case Creation from Incoming Email | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | reviewed |
| REQ-0002 | Auto-Population of Customer from Sender Email Address Match | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | reviewed |
| REQ-0003 | Case Priority Assignment Based on Customer Service Tier | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | reviewed |
| REQ-0004 | Automatic Case Escalation on SLA Breach | 02285f737d34c0e5fa46ecd3c2977d625eac0320da5445903196e4fb26ce97b4 | reviewed |

## Feature specs compiled

| Feature | Title | Spec hash | Status |
|---------|-------|-----------|--------|
| FEAT-01 | Case Creation from Email | 97b0e5a862e9ee70ac5314ae49761d3147f82e388fff113791fb94fd2549ca42 | reviewed |
| FEAT-02 | Tiered SLA & Escalation | 12928460caf0e42eeedc8c42555b75f8b6d7052a0d5793b8ae0061ec8f74df93 | reviewed |

## Open questions blocking Gate 2 approval

The following customer decisions are required before this baseline can be approved
and Stage 3 (Design) can begin:

- **OQ-003-1** (REQ-0003): Customer service tier names and their Dynamics 365 case
  priority mappings are undefined. Proposed options: A) Gold→High, Silver→Normal,
  Bronze→Low; B) four-tier model; C) customer-defined labels.
- **OQ-004-1** (REQ-0004): SLA duration per tier (first-response and resolution time)
  is undefined. Contingent on OQ-003-1.

## Note

REQ-0001 and REQ-0002 are fully grounded and have no open questions.
REQ-0003 and REQ-0004 are structurally complete but contain open questions
(OQ-003-1, OQ-004-1) that must be resolved by the customer before the baseline
can be formally approved at Gate 2.

**Do NOT merge this PR without human review and Gate 2 sign-off.**
