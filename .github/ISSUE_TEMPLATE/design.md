---
name: Design
about: Start a Stage-3 design run over one approved feature spec (assign to Copilot)
title: "Design: FEAT-## <feature name>"
labels: design
---

## Feature to design

<!-- Name the single approved feature spec this design run covers. -->
Feature: FEAT-##

## Scope (closed-world)

- Input is the frozen, approved `specs/features/FEAT-##.spec.md` (and its member REQs) only.
- Produce **one `specs/design/DES-##.md`** (+ **one `specs/ux/UX-##.md`** where user-facing).
- New requirements go back through Stage 1 — nothing new is invented here.

## Contract (see .github/copilot-instructions.md — Phase 3)

- [ ] Record all **8 decision axes** with a **grounded rationale**; declarative-first, justify any escalation.
- [ ] Ground every "how" in **Microsoft Learn MCP** and the live environment — never assert an ungrounded capability.
- [ ] Carry every source-REQ NFR over unchanged; security is least-privilege.
- [ ] Fill the **observability** block (events / metrics / traces / alerts / audit).
- [ ] Close every `open_questions` with a recorded human decision (author + date) before Gate A.
- [ ] Run `python scripts/compile_design.py` so COMPILER zones + `spec_hash` are stamped.

## Gates

- **Gate A** — architect approves the DES.
- **Gate B** — customer approves the UX.
