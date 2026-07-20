# Intake Registry

Every intake batch gets a stable **`INTK-####`** id, assigned by the intake agent
(Phase 1) when it processes an intake issue. This id makes every downstream artifact
traceable to the intake that drove it, independent of the (sequential) REQ/FEAT ids:

- each `specs/requirements/REQ-####.md` carries `intake_batch: INTK-####` back to a row below;
- each `specs/features/FEAT-##.spec.md` aggregates them in `intake_batches`.

Ids are zero-padded and sequential (`conventions.yml` `intake_batch_format`). A friendly
id (not the folder path) is used so that multiple intakes on the same day — or from
different submitters — never collide.

| INTK | Folder | Intake issue | Date | Submitter | REQ range | Status |
|------|--------|--------------|------|-----------|-----------|--------|
| INTK-0001 | intake/test/2026-07-09/ | — | 2026-07-09 | Service Delivery team | REQ-0001..REQ-0004 | extracted |
| INTK-0002 | intake/test/2026-07-20/ | #12 | 2026-07-20 | Service Delivery team | REQ-0005..REQ-0008 | extracted |
