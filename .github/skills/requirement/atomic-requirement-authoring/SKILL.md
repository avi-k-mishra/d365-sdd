---
name: atomic-requirement-authoring
description: >-
  How to extract atomic, testable requirements from converted intake evidence and
  write them as `specs/requirements/REQ-####.md` files with full provenance
  front-matter for D365-CE SDD Stage 1. Use when drafting or splitting
  requirements from an intake document.
allowed-tools: [view, edit, create, grep, glob]
---

# atomic-requirement-authoring

Reusable **HOW** for turning converted intake Markdown (see the
`intake-conversion` skill) into a set of **atomic** `REQ-####.md` files that a
human can review. One need per requirement — never a bundle.

## When to use

- After converting an intake batch, when you are writing the requirement files.
- Whenever a statement in the evidence expresses more than one need and must be
  split.

## Mechanical process (deterministic)

1. **Extract atomic needs.** One requirement = one need. Split every compound
   statement ("the system must do X and Y") into separate REQs.
2. **Number sequentially.** Assign the next `REQ-####` (`conventions.yml`
   `req_id_format`, zero-padded, **no gaps**) after the current maximum.
3. **Write `specs/requirements/REQ-####.md`** with the Stage-1 front-matter:
   `id`, `source_file`, `intake_batch` (from the `intake-traceability` skill),
   `location`, `author` (if in the doc), `sha256`, `confidence`
   (`high | medium | low`). Follow with a clear, **testable** requirement
   statement.
4. **Ground every REQ in evidence.** The statement must be supported by the
   converted Markdown at the cited `location` — no capability, number, or actor
   that is not in the source.
5. **Flag ambiguity, don't resolve it.** If the evidence is unclear, lower
   `confidence` and note the ambiguity; Stage 2 formalizes it as an open
   question. Do not guess to look complete.

## Ground rules

- **Atomicity over brevity.** Prefer more, smaller REQs to one bundled REQ.
- **Testable phrasing.** Write each requirement so a reviewer can imagine a pass/
  fail check; avoid vague verbs ("support", "handle") without an object.
- **Provenance is mandatory.** Every REQ carries `source_file` + `location` +
  `sha256`; a REQ with no traceable source is invalid.
- **No solutioning.** Stage 1 captures the *need*, not the D365 how — that is
  Stage 3 Design.

## Anti-patterns

- Bundling multiple needs into one REQ.
- Inventing detail (numbers, actors, rules) not present in the evidence.
- Gaps or reordering in the `REQ-####` sequence.
- Asserting a solution or platform capability inside a requirement.
