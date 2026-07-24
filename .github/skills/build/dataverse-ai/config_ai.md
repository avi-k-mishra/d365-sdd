# config_ai_* — Dataverse AI Configuration (wildcard)

Wildcard reference for the `config_ai_*` component family (AI Builder models,
prompt/Copilot configuration). Stage-3 reference and Stage-4
`patterns/config_ai_<subtype>.md`.

> Phase-B skill. Fill in a specific payload when the concrete `config_ai_<subtype>`
> is added to `conventions.yml`; until then the `_default` payload applies.

## Required payload

`conventions.yml` `component_type_payloads` — `_default` (no explicit entry yet):

| Field | Meaning |
| --- | --- |
| `name` | AI component display name. |
| `satisfies` | `[REQ-####]`. |

When authoring a concrete subtype, add its real fields (e.g. model type, entities,
prompt template, grounding source) both here and in `conventions.yml`.

## Decision guide

- **Configured before custom.** AI Builder / prompt configuration beats a bespoke
  Azure AI build for standard extraction/classification/generation.
- **Solution-aware** so the model/prompt travels through ALM.
- **Grounding + Responsible AI** documented; human review for consequential output.
- **Check Microsoft Learn (MCP)** for the current capability set before finalizing.

## Anti-patterns

- Custom Azure AI where AI Builder would suffice.
- Ungrounded generative output on consequential decisions.
- Non-solution-aware AI artifacts (manual per-environment recreate).

## Validation checklist

- [ ] `satisfies` declared (+ subtype-specific payload once defined).
- [ ] Grounding + Responsible AI note present.

## Stage-4 build mapping

AI Builder model / prompt configuration in the solution. Verified by Stage-5 tests
(model/prompt produces expected output on sample input).
