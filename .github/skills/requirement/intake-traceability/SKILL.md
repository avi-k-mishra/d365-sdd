---
name: intake-traceability
description: >-
  How to register an intake batch (INTK-####) in the intake registry and stamp it
  on every requirement it produces, so each REQ stays traceable to the intake that
  drove it, for D365-CE SDD Stage 1. Use when opening an intake batch or wiring
  REQ provenance.
allowed-tools: [view, edit, create, grep, glob]
---

# intake-traceability

Reusable **HOW** for the intake-to-requirement audit trail. Every requirement
must trace back to the intake batch that produced it, independent of the
sequential REQ/FEAT numbering.

## When to use

- You are starting a new intake batch (before or while writing its REQs).
- You need to set or verify the `intake_batch` field on a `REQ-####.md`.

## Mechanical process (deterministic)

1. **Assign the next `INTK-####`.** Read `intake/_index.md` and take the next
   sequential id (`conventions.yml` `intake_batch_format`).
2. **Register the batch.** Add a row to `intake/_index.md`:
   `INTK id | folder | intake issue # | date | submitter | REQ range | status`.
3. **Stamp every REQ.** Put that same `intake_batch: INTK-####` in the
   front-matter of **every** `REQ-####.md` produced from this intake.
4. **Fill the REQ range** in the registry row once the batch's REQ ids are known.
5. **Do not propagate to features.** Features derive intake provenance through
   their `member_reqs` → each REQ's `intake_batch`; they never store their own
   intake ids.

## Ground rules

- **REQs are the only intake-id carrier.** Intake traceability lives on REQs;
  everything downstream derives it via membership.
- **Registry is authoritative.** Every batch id used on a REQ must exist as a row
  in `intake/_index.md`; every registry row must have a status.
- **Global-sequential ids.** `INTK-####` (and `REQ-####`) are sequential with no
  gaps.

## Anti-patterns

- A REQ with no `intake_batch`, or a batch that is missing from
  `intake/_index.md`.
- Storing an intake id on a `FEAT` (it inherits through `member_reqs`).
- Reusing or skipping `INTK-####` numbers.
