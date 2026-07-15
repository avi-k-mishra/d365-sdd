---
name: spec-authoring
description: Fill the reasoning (FILL) zones of a compiled FEAT-##.spec.md
---

# Spec authoring — fill only the FILL zones

You are completing a compiled feature spec `specs/features/FEAT-##.spec.md`.
The deterministic `COMPILER` zones (traceability table, scenarios, NFR table,
dependency graph, provenance) are **already written and hash-guarded by
`spec_hash`** — do **not** touch them. Author **only** the `FILL` zones below,
using the member `REQ-####.md` files and Microsoft Learn grounding as your source.

Fill each zone concisely and factually — no invention beyond what the REQs and
Microsoft Learn support:

- `<!-- FILL:intent -->` — one or two sentences: the user/business outcome this
  feature delivers and why it matters. Trace to the member REQs, don't restate them.
- `<!-- FILL:scope -->` — `In:` what this feature covers · `Out:` explicitly
  excluded items (and which other feature owns them, if any).
- `<!-- FILL:grounding -->` — the Microsoft-stack capability this feature relies
  on, with the Microsoft Learn URL(s) confirming it is realizable.
- `<!-- FILL:open-decisions -->` — design questions deliberately deferred to
  Stage 3 (DES), each traceable to an open question or a grounding gap. If none,
  write `None`.

Rules:
- Never write outside a `FILL` zone. Never alter `spec_hash` or any `COMPILER` zone.
- Ground every capability claim on Microsoft Learn; cite the URL.
- If a member REQ still has an unresolved open question, note it under
  `open-decisions` — do not resolve it yourself.
