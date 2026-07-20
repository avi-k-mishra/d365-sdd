---
name: Feature Spec
about: Elevate reviewed requirements into an approved, compiled baseline (Phase 2)
title: "Feature-spec: baseline v<N>"
labels: feature-spec
---

## Feature-spec batch

**Baseline version:** v<!-- e.g. 1 -->
**Requirements in scope:**
<!-- list the REQ ids to refine, e.g. REQ-0001 .. REQ-0004 -->
-

**Known ambiguities / decisions the customer still owes:**
<!-- e.g. what are the service tiers and their priorities? (REQ-0003) -->
-

**Notes for the agent:**
<!-- anything else: priorities, must-haves, out-of-scope -->

---
### What the agent will do (see `.github/copilot-instructions.md` Phase 2)
1. Enrich front-matter (title, type, module, priority, status)
2. Raise open questions — **not** guess them
3. Expand Gherkin (happy / negative / boundary), grounded only in the recorded REQ evidence
4. Attach structured NFRs `{metric, target}`
5. De-dup & reconcile the whole backlog
6. Group into features/epics + acyclic `depends_on` (`specs/_index/features.md`)
7. Compile one `specs/features/FEAT-##.spec.md` per feature (COMPILER + FILL, `spec_hash`)
8. Open a **Feature-spec: baseline vN** PR — **not** merge (Gate 2 = human sign-off)

> Stage 2 stays solution-agnostic: the agent grounds only in the recorded REQ evidence and decisions. Product-capability and platform-feasibility grounding (Microsoft Learn MCP) happens in Stage 3 (Design), not here.

### Checklist before assigning to Copilot
- [ ] The requirements above are merged on `main` at `status: reviewed`
- [ ] I will **assign this issue to Copilot** (or comment `@copilot`) to start refinement
