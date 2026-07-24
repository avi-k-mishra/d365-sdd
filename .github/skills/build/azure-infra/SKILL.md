---
name: azure-infra
description: >-
  How to design and build the Azure infrastructure that supports a Dataverse
  solution — API Management, Service Bus, Key Vault, Function Apps, Application
  Insights, Event Grid, and Azure AI. Use for any DES component tagged az_apim,
  az_service_bus, az_key_vault, az_function_app, az_func_scheduled, az_app_insights,
  az_event_grid, or az_ai_* (wildcard).
allowed-tools: [view, edit, create, grep, glob]
---

# azure-infra

Reusable **HOW** for the Azure side of a Dataverse solution. Applied both when
authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `az_apim` | [az_apim.md](az_apim.md) |
| `az_service_bus` | [az_service_bus.md](az_service_bus.md) |
| `az_key_vault` | [az_key_vault.md](az_key_vault.md) |
| `az_function_app` | [az_function_app.md](az_function_app.md) |
| `az_func_scheduled` | [az_func_scheduled.md](az_func_scheduled.md) |
| `az_app_insights` | [az_app_insights.md](az_app_insights.md) |
| `az_event_grid` | [az_event_grid.md](az_event_grid.md) |
| `az_ai_*` | [az_ai.md](az_ai.md) |

`az_ai_*` uses a single wildcard reference file `az_ai.md`.

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload against the reference's **Required payload**
   (`_default`: name + satisfies until a specific payload is defined).
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Managed identity, not keys.** Prefer managed identities + RBAC; secrets live in
  `az_key_vault`, never in code/config.
- **Infrastructure as code.** Bicep/Terraform, parameterized per environment; no
  portal click-ops for real deployments.
- **Least privilege + private networking** where data sensitivity warrants (private
  endpoints, no public exposure by default).
- **Observability by default.** Wire `az_app_insights` telemetry into every
  compute component.
- **Ground in Microsoft Learn (MCP)** for current Azure service capabilities.
