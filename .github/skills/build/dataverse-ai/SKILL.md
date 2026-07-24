---
name: dataverse-ai
description: >-
  How to design and build Dataverse-native AI configuration — AI Builder models,
  AIProvider/AI prompt configuration, and other config_ai_* components. Use for any
  DES component tagged config_ai_* (wildcard).
allowed-tools: [view, edit, create, grep, glob]
---

# dataverse-ai

Reusable **HOW** for Dataverse-native AI capabilities (AI Builder / prompts /
Copilot configuration). Applied both when authoring a `DES-##.md` (Stage 3) and
when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
matches:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `config_ai_*` (e.g. `config_ai_prompt_builder`, `config_ai_model_form`) | [config_ai.md](config_ai.md) |

The `config_ai_*` family uses a single wildcard reference file `config_ai.md`
(validator maps `x_*` → `x.md`).

## Mechanical process (deterministic)

1. Confirm the `component_type` matches `config_ai_*`; open [config_ai.md](config_ai.md).
2. Emit / verify the payload against the reference's **Required payload**
   (`_default`: name + satisfies — extend when a specific payload is added to
   `conventions.yml`).
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules

- **Prefer configured AI over custom code.** Use AI Builder / prompt configuration
  before an Azure AI (`az_ai_*`) custom build.
- **Solution-aware.** AI Builder models and prompts are packaged in the solution
  for ALM.
- **Responsible AI.** Human-in-the-loop for consequential outputs; document data
  used and grounding.
- **Ground in Microsoft Learn (MCP)** for current AI Builder / Copilot capabilities
  before committing to a design — this is a fast-moving surface.
