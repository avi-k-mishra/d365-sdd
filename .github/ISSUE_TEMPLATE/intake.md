---
name: Requirement Intake
about: Submit documents for AI requirement extraction (Phase 1)
title: "Intake: <customer> <date>"
labels: intake
---

## Intake batch

**Customer:** <!-- e.g. Contoso -->
**Intake path:** `intake/<customer>/<date>/`
<!-- e.g. intake/contoso/2026-07-09/ -->

**Documents committed:**
<!-- list each filename you added to the intake path -->
-

**Notes for the agent:**
<!-- anything the agent should know: priorities, known ambiguities, out-of-scope items -->

---
### Checklist before assigning to Copilot
- [ ] Documents are committed under the intake path above
- [ ] Files are born-digital Office/PDF (`.docx` / `.xlsx` / `.pptx` / `.pdf`)
- [ ] I will **assign this issue to Copilot** (or comment `@copilot`) to start extraction

> The agent assigns this intake a stable **`INTK-####`** id, records it in
> `intake/_index.md`, and stamps `intake_batch: INTK-####` on every requirement it
> drafts — so the resulting REQs/features stay traceable to this intake. You do not
> need to pick the number.
