---
name: intake-conversion
description: >-
  How to convert born-digital intake documents into Markdown evidence for D365-CE
  SDD Stage 1 (Requirement Intake) using the MarkItDown MCP — preserving
  provenance and flagging unusable files. Use when processing an `intake` issue,
  reading anything under `intake/<customer>/<date>/`, or before drafting any REQ.
allowed-tools: [view, edit, create, grep, glob]
---

# intake-conversion

Reusable **HOW** for turning raw intake artifacts into trustworthy Markdown that
atomic requirements can be drafted from. This is the first move of every
Stage-1 intake batch — you never draft a `REQ` from a file you have not
converted.

## When to use

- You are assigned an issue labelled `intake`.
- You need to read any born-digital document under `intake/<customer>/<date>/`
  (docx, pptx, xlsx, pdf, …).

## Mechanical process (deterministic)

1. **Convert, never guess.** For every file named in the issue, call the
   MarkItDown MCP tool `convert_to_markdown` with the `file://…` path. Do **not**
   infer or reconstruct contents from the filename, folder, or issue text.
2. **Capture provenance per file** — source path, and where each fact sits
   (page / slide / cell / section) — because every downstream `REQ` must cite it.
3. **Compute the source `sha256`** of each converted file; it is stamped on the
   REQs so evidence is tamper-evident.
4. **Flag, don't fabricate.** If a file is scanned, image-only, empty, or
   garbled, do not invent content: note the file + problem (e.g.
   `possible_scanned_pdf`) in the PR body and suggest the opt-in
   `markitdown[az-doc-intel]` fallback for that file only.
5. **Preserve the raw evidence.** Never edit, move, or delete anything under
   `intake/` — those files are evidence, not source of truth.

## Ground rules

- **MCP-first extraction.** The converted Markdown is the only sanctioned basis
  for requirements; anything not present in it is not a fact.
- **One provenance chain.** Every downstream artifact traces file → location →
  sha256 back to here.
- **Fail loud, not silent.** A file that cannot be converted is surfaced, not
  guessed around.

## Anti-patterns

- Reconstructing a document's contents from its filename or surrounding context.
- Editing or deleting raw files under `intake/`.
- Silently skipping an unconvertible file instead of flagging it.
