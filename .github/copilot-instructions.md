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
   location: "page 3, section 2.1"   # page / slide / cell
   author: "Jane Doe"                # if available in the doc
   sha256: "<hash of source file>"
   confidence: high                  # high | medium | low
   ---
   ```
   Followed by a clear, testable requirement statement.

4. **Flag, don't fabricate.** If a document is scanned, image-only, empty, or
   garbled, do NOT invent content. Add a note in the PR body listing the file and
   the problem (e.g. `possible_scanned_pdf`). Suggest the opt-in
   `markitdown[az-doc-intel]` fallback for that file.

5. **Preserve provenance.** Every REQ must trace back to a real file + location.
   Never edit the raw documents in `intake/` — they are evidence, not source of truth.

6. **Open a Pull Request** titled `Intake: <customer> <date>` summarizing what was
   extracted and what was flagged. **Do NOT merge** — a human reviews and merges.

## Anti-patterns (never do these)
- Guessing an ambiguous requirement to look complete — flag it instead.
- Bundling multiple needs in one REQ.
- Losing provenance (a REQ with no source file + location).
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
   provenance (`source_file`, `location`, `author`, `sha256`, `confidence`).

2. **Resolve open questions - do NOT guess.** For each ambiguity, write a
   decision-ready question (2-3 concrete options + build implication) in the
   PR body and in the REQ `## Notes / open questions` section as an unchecked
   box. A question is closed ONLY by a recorded human decision
   (`- [x] ... - decided by <name> <date>`). Leave it open otherwise.

3. **Expand the Gherkin (grounded).** Elaborate each thin statement into
   `scenarios:` with `happy`, `negative`, and `boundary` kinds. Before writing
   a criterion, confirm the capability with the **Microsoft Learn MCP**
   (`microsoft_docs_search` / `microsoft_docs_fetch`) and cite the Learn URL
   under a `grounding:` list. A `security` REQ **must** have a negative scenario.

4. **Attach structured NFRs.** Latency/throughput/availability become
   `nfr: [{ metric, target }]` objects drawn from `conventions.yml`
   `nfr_categories` - never free prose.

5. **Consistency & de-dup.** Read the whole backlog at once; merge or link
   duplicates (keep every provenance source); raise conflicts as new open
   questions - never silently resolve.

6. **Group into features/epics.** Write `specs/_index/features.md`
   (Epic -> Feature -> REQ) and complete each REQ `depends_on` into an acyclic
   graph. Set `feature` and `epic` on each REQ.

7. **Compile one feature spec per feature.** For each `FEAT-##`, write
   `specs/features/FEAT-##.spec.md`. Copy the traceability table, acceptance
   scenarios (VERBATIM from the member REQs), NFR table, dependency graph and
   provenance into `<!-- COMPILER:BEGIN x -->...<!-- COMPILER:END x -->` zones,
   and compute `spec_hash` (sha256 over the compiler zones) into the
   front-matter. Author ONLY the `<!-- FILL:x -->...<!-- /FILL -->` zones
   (intent, scope in/out, grounding notes, open decisions) - follow
   `.github/prompts/spec-authoring.prompt.md`. Never hand-write compiler zones.

8. **Freeze.** When every REQ is complete, grounded and consistent and every
   feature is compiled, flip REQs to `status: approved`, write
   `specs/_baseline/reqs-baseline-vN.md` (ids + sha256 + approver + date), and
   open a Pull Request titled `Feature-spec: baseline vN`. **Do NOT merge** - customer
   + architect review at Gate 2.

## Phase 2 anti-patterns (never do these)
- Guessing an open question to look complete - only a recorded decision closes it.
- Inventing a capability - ground every non-trivial criterion on Microsoft Learn.
- Free-text NFRs ("should be fast") - use `{ metric, target }`.
- Hand-writing or editing a `COMPILER` zone - those are generated + hash-guarded.
- Silent duplicates/conflicts - reconcile explicitly or raise a question.
