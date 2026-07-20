---
name: design-authoring
description: Author a Stage-3 DES-##.md (and UX-##.md) from one approved feature spec — fill only the FILL zones
---

# Design authoring — fill only the FILL zones

You are producing the Stage-3 design for **one approved feature spec**
`specs/features/FEAT-##.spec.md` (and its member `REQ-####.md` files). Create
`specs/design/DES-##.md` and — where the feature is user-facing —
`specs/ux/UX-##.md`, using the templates below **verbatim** (including every
`COMPILER` and `FILL` marker).

The deterministic `COMPILER` zones (traceability chain FEAT←REQ←INTK, NFR
carry-over, provenance) are filled and hash-guarded by
`scripts/compile_design.py` — leave their bodies empty; **do not** hand-write
them. Author **only** the `FILL` zones. When done, run
`python scripts/compile_design.py` so the COMPILER zones and `spec_hash` are
stamped, then `python scripts/validate_design.py`.

## Grounding (Stage 3 = the architect owns the "how")

- **Ground every decision** in **Microsoft Learn MCP** (product capability,
  connector limits, licensing/feasibility) and, where an environment is
  available, the **Dataverse / Copilot Studio / Azure / Bicep MCP** (real schema,
  roles). Never assert a capability you have not grounded.
- **Declarative-first:** prefer `config` → `low_code` → `pro_code`. Any
  `low_code`/`pro_code` choice **must** carry a rationale.
- **Least-privilege** security. **Carry every source-REQ NFR over unchanged.**
- Close every open question with a **recorded human decision** (author + date);
  none may remain unresolved (`- [ ]`) before Gate A/B.

## Naming

`DES-##` / `UX-##` are zero-padded and sequential (see `conventions.yml`
`des_id_format` / `ux_id_format`). `satisfies` must equal the feature's
`member_reqs`. Table/prefix names come from `conventions.yml` — the pattern is
entity-agnostic.

---

## DES-##.md template

```markdown
---
id: DES-##
title: "<design name>"
satisfies: [REQ-####, REQ-####]
implements_feature: FEAT-##
spec_hash: "0000000000000000000000000000000000000000000000000000000000000000"
status: draft
---

<!-- FILL:decisions -->
Record all ten axes; give a grounded rationale (cite Microsoft Learn) for every
non-trivial or escalated choice.

### logic_tier
<config | low_code | pro_code> — decision + rationale (declarative-first; a
low_code/pro_code choice REQUIRES a rationale).

### data_residency
Dataverse-native vs external (connector / API Management) — decision + rationale.

### alm_boundary
Unmanaged solution + publisher prefix; managed downstream — decision + rationale.

### security
Roles / field-level security / business units / least-privilege service principals.

### integration
Connectors / API Management / Service Bus / Functions / Event Grid — or none.

### environment
Dev / Test / UAT / Prod + source environment.

### ux_surface
App type, forms, views/dashboards, PCF vs OOB, navigation, accessibility (detail in UX-##).

### observability
Which telemetry events / metrics / traces / alerts / audit this design emits (detail below).

### batch_processing
How the design handles bulk/high-volume or scheduled work — none, OOB bulk operations, async/background flows, or a dedicated batch mechanism. Declarative-first; justify any escalation.

### reporting
How reporting/analytics needs are met — none, OOB views/dashboards/charts, Power BI, or a dedicated analytics store. Reference the source REQs; declarative-first.
<!-- /FILL -->

<!-- FILL:solution -->
- **components:** the concrete D365/Power Platform components realising this design.
- **data_model:** tables/columns/relationships (placeholder names per conventions.yml).
- **security[]:** the specific roles / FLS grants.
- **integration[]:** the concrete integration points, if any.
- **test_strategy[]:** how the carried-over Gherkin scenarios become Stage-5 tests
  (measured on the same metric each component emits).
<!-- /FILL -->

<!-- FILL:observability -->
- **events:** e.g. `CaseEscalated`
- **metrics:** e.g. SLA-breach count (feeds the Stage-7 alert and any dashboard REQ)
- **traces:** correlation ids across components
- **alerts:** threshold-based alerts tied to the NFR targets
- **audit:** what is audited and where
<!-- /FILL -->

<!-- FILL:open-questions -->
List each open design question as `- [ ]` and, once decided, `- [x]` with
(DECIDED — author, date). Must contain no `- [ ]` before Gate A. If none, write `None.`
<!-- /FILL -->

---

## Traceability (FEAT ← REQ ← INTK)

<!-- COMPILER:BEGIN traceability -->

<!-- COMPILER:END traceability -->

## NFR carry-over

<!-- COMPILER:BEGIN nfr -->

<!-- COMPILER:END nfr -->

## Provenance

<!-- COMPILER:BEGIN provenance -->

<!-- COMPILER:END provenance -->
```

---

## UX-##.md template (only where the feature is user-facing)

```markdown
---
id: UX-##
title: "<experience name>"
satisfies: [REQ-####, REQ-####]
implements_design: DES-##
spec_hash: "0000000000000000000000000000000000000000000000000000000000000000"
status: draft
---

<!-- FILL:surfaces -->
The app + surfaces: `app{type, app_module}`, forms / quick_create / views /
dashboards with layout. For a Copilot Studio surface, this is the **conversation
design** (greeting, disambiguation, anonymous-user refusal, fallback).
<!-- /FILL -->

<!-- FILL:client-logic -->
Client logic — **business-rule first**, then low-code, then PCF/script (with a
rationale for any escalation).
<!-- /FILL -->

<!-- FILL:components -->
OOB vs PCF components, each with a justification.
<!-- /FILL -->

<!-- FILL:navigation-accessibility -->
Navigation / information architecture and accessibility commitments
(keyboard, contrast, screen-reader labels).
<!-- /FILL -->

<!-- FILL:open-questions -->
Open experience questions as `- [ ]` / decided `- [x]`. No `- [ ]` before Gate B.
If none, write `None.`
<!-- /FILL -->

---

## Traceability (DES ← REQ ← INTK)

<!-- COMPILER:BEGIN traceability -->

<!-- COMPILER:END traceability -->

## Provenance

<!-- COMPILER:BEGIN provenance -->

<!-- COMPILER:END provenance -->
```

## Rules

- Never write outside a `FILL` zone. Never hand-edit a `COMPILER` zone or `spec_hash`.
- `satisfies` must equal the source feature's `member_reqs` (DES) / design's `satisfies` (UX).
- Ground every "how" in Microsoft Learn / the live environment; declarative-first; least-privilege.
- Resolve every open question with a recorded human decision before the gate.
- Always finish by running `compile_design.py` then `validate_design.py`.
