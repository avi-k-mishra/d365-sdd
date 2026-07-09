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
