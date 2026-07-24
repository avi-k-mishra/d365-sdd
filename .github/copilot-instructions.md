# Repository guidance for the Copilot coding agent

This repo runs **Phase 1 — Requirement Intake** of a Spec-Driven Development (SDD)
pattern for Dynamics 365 CE. Business Analysts submit born-digital documents; you
convert them and draft atomic requirements for human review.

## Intake agent instructions (Phase 1)

When you are assigned an **intake** issue (label `intake`):

1. **Convert, never guess.** For every file under the `intake/<customer>/<date>/`
   path named in the issue, call the MarkItDown MCP tool `convert_to_markdown`
   (e.g. `file://.../intake/contoso/2026-07-09/spec.docx`). Do NOT infer or
   reconstruct document contents from the filename or anything else.

2. **Extract ATOMIC requirements.** One need per requirement. Never bundle
   multiple needs into a single item. Split compound statements.

3. **Write each requirement** to `specs/requirements/REQ-####.md` (zero-padded,
   sequential, no gaps) with YAML front-matter:
   ```yaml
   ---
   id: REQ-0001
   source_file: intake/contoso/2026-07-09/spec.docx
   intake_batch: INTK-0001           # the registry id for this intake (see step 4)
   location: "page 3, section 2.1"   # page / slide / cell
   author: "Jane Doe"                # if available in the doc
   sha256: "<hash of source file>"
   confidence: high                  # high | medium | low
   ---
   ```
   Followed by a clear, testable requirement statement.

4. **Register the intake batch.** Assign the next sequential `INTK-####`
   (`conventions.yml` `intake_batch_format`) by reading `intake/_index.md`, and add
   a row there (`INTK id | folder | intake issue # | date | submitter | REQ range |
   status`). Stamp that same `intake_batch: INTK-####` on **every** REQ produced from
   this intake. This is how each requirement stays traceable to
   the intake that drove it, independent of the sequential REQ/FEAT numbering.
   (Features inherit this trail through their member REQs - they do not store
   their own intake ids.)

5. **Flag, don't fabricate.** If a document is scanned, image-only, empty, or
   garbled, do NOT invent content. Add a note in the PR body listing the file and
   the problem (e.g. `possible_scanned_pdf`). Suggest the opt-in
   `markitdown[az-doc-intel]` fallback for that file.

6. **Preserve provenance.** Every REQ must trace back to a real file + location.
   Never edit the raw documents in `intake/` — they are evidence, not source of truth.

7. **Open a Pull Request** titled `Intake: <customer> <date>` summarizing what was
   extracted and what was flagged. **Do NOT merge** — a human reviews and merges.

## Anti-patterns (never do these)
- Guessing an ambiguous requirement to look complete — flag it instead.
- Bundling multiple needs in one REQ.
- Losing provenance (a REQ with no source file + location).
- Losing the intake trail (a REQ with no `intake_batch`, or a batch missing from `intake/_index.md`).
- Editing or deleting anything under `intake/`.

---

## Feature-spec instructions (Phase 2)

This repo also runs **Phase 2 — Spec Authoring & Refinement**. When you are
assigned a **feature-spec** issue (label `feature-spec`), you elevate the reviewed
`specs/requirements/REQ-####.md` set into a complete, consistent, testable
baseline **and** compile one feature spec per feature. You never touch
`intake/` and never invent facts. Read `conventions.yml` first.

Run the batch in this order — **refine -> group -> compile -> freeze**:

1. **Enrich the front-matter.** For every REQ in scope add the missing fields:
   `title`, `type` (functional|non-functional|integration|data|security|agentic),
   `module`, `priority` (MoSCoW), `status: reviewed`. Keep all existing
   provenance (`source_file`, `intake_batch`, `location`, `author`, `sha256`, `confidence`).

2. **Resolve open questions - do NOT guess.** For each ambiguity, write a
   decision-ready question (2-3 concrete options + build implication) in the
   PR body and in the REQ `## Notes / open questions` section as an unchecked
   box. A question is closed ONLY by a recorded human decision
   (`- [x] ... - decided by <name> <date>`). Leave it open otherwise.

3. **Expand the Gherkin.** Elaborate each thin statement into
   `scenarios:` with `happy`, `negative`, and `boundary` kinds. Before writing
   a criterion, keep it behaviour-focused and traceable to a reviewed REQ
   or a recorded decision, listing those evidence references (REQ ids /
   decisions) under a `grounding:` list. Platform feasibility is NOT decided here - that is Stage 3 Design. A `security` REQ **must** have a negative scenario.

4. **Attach structured NFRs.** Latency/throughput/availability become
   `nfr: [{ metric, target }]` objects drawn from `conventions.yml`
   `nfr_categories` - never free prose.

5. **Consistency & de-dup.** Read the whole backlog at once; merge or link
   duplicates (keep every provenance source); raise conflicts as new open
   questions - never silently resolve.

6. **Group into features/epics.** Write `specs/_index/features.md`
   (Epic -> Feature -> REQ) and complete each REQ `depends_on` into an acyclic
   graph. Set `feature` and `epic` on each REQ.

7. **Compile one feature spec per feature.** For each `FEAT-##`, create
   `specs/features/FEAT-##.spec.md` with the front-matter (`id`, `title`,
   `epic`, `member_reqs`, `status`, and a placeholder `spec_hash`)
   and the `<!-- COMPILER:BEGIN x -->...<!-- COMPILER:END x -->` /
   `<!-- FILL:x -->...<!-- /FILL -->` zone skeleton. Author ONLY the
   FILL zones (intent, scope in/out, grounding notes, open decisions) - follow
   `.github/prompts/spec-authoring.prompt.md`. **Never hand-write the COMPILER
   zones or `spec_hash`** - run `python scripts/compile_specs.py`, which fills
   the traceability / scenarios / NFR / dependency / provenance zones VERBATIM
   from the member REQs and computes `spec_hash`. Re-run it after any REQ change.

8. **Freeze.** When every REQ is complete, evidence-grounded and consistent and every
   feature is compiled (`python scripts/compile_specs.py --check` and
   `python scripts/validate_specs.py` both pass), flip REQs to `status: approved`,
   write `specs/_baseline/reqs-baseline-vN.md` (ids + sha256 + approver + date),
   and open a Pull Request titled `Feature-spec: baseline vN`. **Do NOT merge** -
   customer + architect review at Gate 2.

## Phase 2 anti-patterns (never do these)
- Guessing an open question to look complete - only a recorded decision closes it.
- Asserting platform feasibility - that is Stage 3 Design's call; surface doubts as open questions.
- Free-text NFRs ("should be fast") - use `{ metric, target }`.
- Hand-writing or editing a `COMPILER` zone - those are generated + hash-guarded.
- Silent duplicates/conflicts - reconcile explicitly or raise a question.


---

## Design instructions (Phase 3)

This repo also runs **Phase 3 — Design & Solution Decomposition**. When you are
assigned a **design** issue (label `design`), you turn **one approved feature
spec** `specs/features/FEAT-##.spec.md` into a solution design on the Microsoft
stack. This is where the architect owns the **"how"** — so you **ground every
decision** in the **Microsoft Learn MCP** (and the Dataverse / Copilot Studio /
Azure / Bicep MCPs for live schema), never asserting an ungrounded capability.
You never touch `intake/` or the raw REQs. Read `conventions.yml` first, then
follow `.github/prompts/design-authoring.prompt.md`.

Produce **one `specs/design/DES-##.md`** (+ **one `specs/ux/UX-##.md`** where the
feature is user-facing), using the templates in the prompt file verbatim
(including every `COMPILER` and `FILL` marker):

1. **Record all 10 decision axes with a grounded rationale.** `logic_tier`,
   `data_residency`, `alm_boundary`, `security`, `integration`, `environment`,
   `ux_surface`, `observability`, `batch_processing`, `reporting` (`conventions.yml` `decision_axes`).
   **Declarative-first** (`config` → `low_code` → `pro_code`); any
   `low_code`/`pro_code` choice **must** carry a rationale
   (`escalation_requires_rationale`).

2. **Ground the "how", don't invent it.** Cite Microsoft Learn / the live
   environment for each axis decision. Never assert a capability you have not grounded.

3. **Carry NFRs over unchanged, security least-privilege.** Every source-REQ
   `{ metric, target }` is carried verbatim (the compiler does this); grant the
   minimum roles / field-level security the feature needs.

4. **Fill the observability block** — events, metrics, traces, alerts, audit
   (`observability_required`).

5. **Tag every component AND declare its required payload.** In the `solution`
   FILL zone, list each component as its own granular unit
   `<name> (component_type: <type>)` using the closed vocabulary in
   `conventions.yml` `component_types` (families + design-axis mapping in
   `specs/_schema/component-types.md`). One buildable component per type — never a
   single opaque blob. Declarative-first: prefer a `config_`/`uiux_`/`flow_` type
   over a `code_`/`az_` type, justify any escalation, and if no type fits raise an
   open question (extend the taxonomy first) rather than inventing one.
   Then, **for each component, apply its skill deterministically:**
   (a) look up the component's `component_type` in `conventions.yml`
   `component_type_skills` to find its **skill**; (b) load that skill from
   `.github/skills/<skill>/` (thin `SKILL.md` + the `<component_type>.md` reference)
   and follow its guidance; (c) declare the component's **required payload** as an
   indented `key: value` sub-list beneath the bullet — one line per field in
   `conventions.yml` `component_type_payloads.<type>.required` (the backtick name is
   the `name` field; `satisfies` + type-specific fields are sub-lines), exactly as
   specified by the *Design-item payload contract* in
   `specs/_schema/component-types.md`. Do not invent or omit required fields.

6. **Resolve open questions — do NOT guess.** Record each as `- [ ]` and close
   only with a recorded human decision (`- [x] ... — decided by <name> <date>`).
   **No `- [ ]` may remain** before Gate A/B.

7. **Compile, never hand-write COMPILER zones.** Run
   `python scripts/compile_design.py`, which fills the traceability
   (FEAT←REQ←INTK), NFR carry-over and provenance zones VERBATIM and computes
   `spec_hash`. Re-run after any change.

8. **Open a Pull Request** titled `Design: FEAT-## <name>` once
   `python scripts/compile_design.py --check` and
   `python scripts/validate_design.py` both pass. **Do NOT merge** — the
   architect reviews the DES at **Gate A** and the customer reviews the UX at **Gate B**.

## Phase 3 anti-patterns (never do these)
- Silent pro-code — escalating past config/low-code without a recorded, grounded rationale.
- Ungrounded "how" — asserting product capability without a Microsoft Learn / live-environment citation.
- Over-broad security — granting more than least-privilege.
- Skipping the UX gate — the customer (not the architect) owns the experience sign-off.
- Designing without observability — every DES must declare what it emits.
- Untyped or blob components — a component with no `component_type`, or bundling several
  types into one entry instead of listing one granular unit per type.
- Inventing a `component_type` not in `conventions.yml` — extend the taxonomy first.
- Hand-writing or editing a `COMPILER` zone or `spec_hash` — those are generated + hash-guarded.