# az_ai_* — Azure AI Service (wildcard)

Wildcard reference for the `az_ai_*` family (Azure OpenAI, AI Search, Document
Intelligence, Language, and other Azure AI services). Stage-3 reference and
Stage-4 `patterns/az_ai_<subtype>.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Azure AI resource / deployment name. |
| `satisfies` | `[REQ-####]`. |

When authoring a concrete subtype (`az_ai_openai`, `az_ai_search`, …), add its real
fields (model/deployment, index, capacity, grounding data).

## Decision guide

- **AI Builder before Azure AI.** Use Dataverse-native `config_ai_*` for standard
  needs; reach for Azure AI when you need custom models, RAG over large corpora, or
  capabilities AI Builder lacks.
- **RAG pattern.** Pair Azure OpenAI with AI Search for grounded retrieval; keep the
  ground-truth data governed.
- **Managed identity + private networking**; keys in Key Vault; content filtering on.
- **Responsible AI.** Human-in-the-loop for consequential output; log prompts/
  responses to App Insights (no PII leakage).

## Anti-patterns

- Custom Azure AI where AI Builder suffices.
- Ungrounded generation on consequential decisions.
- Public endpoints / keys in config instead of MI + Key Vault.

## Validation checklist

- [ ] `satisfies` declared (+ subtype/model/index once authored).
- [ ] Grounding, identity, and Responsible AI stated.

## Stage-4 build mapping

Azure AI resource + deployment (IaC). Verified by Stage-5 tests (prompt/input →
expected grounded output).
