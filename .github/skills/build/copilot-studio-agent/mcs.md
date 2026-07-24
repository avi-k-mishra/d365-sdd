# mcs_* — Copilot Studio Agent Component (wildcard)

Wildcard reference for the `mcs_<agentname>_*` family (topics, actions, knowledge
sources, triggers of a Copilot Studio agent). Stage-3 reference and Stage-4
`patterns/mcs_<subtype>.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Component name (e.g. `mcs_supportbot_topic_reset_password`). |
| `satisfies` | `[REQ-####]`. |

When authoring, capture the agent name, component kind (topic / action /
knowledge / trigger), and kind-specific fields (trigger phrases, action inputs/
outputs, knowledge source).

## Decision guide

- **Topic vs generative.** Explicit topics for deterministic/compliance flows;
  generative answers + knowledge for open Q&A. Combine deliberately.
- **Actions** wrap flows/connectors/Custom APIs — bind via connection references.
- **Knowledge grounding** scoped to approved sources; cite and constrain.
- **Auth + Responsible AI.** Authenticated access for Dataverse data; moderation +
  human handoff configured.
- **Solution-aware** for ALM; per-environment config via environment variables.

## Anti-patterns

- Generative-only where a compliance flow needs a deterministic topic.
- Inline secrets in actions instead of connection references.
- Ungrounded/unscoped knowledge answers.

## Validation checklist

- [ ] `satisfies` declared (+ agent/kind-specific payload once authored).
- [ ] Auth, grounding, and topic-vs-generative choice stated.

## Stage-4 build mapping

Copilot Studio agent component in the solution. Verified by Stage-5 tests
(utterance → expected topic/action/answer).
