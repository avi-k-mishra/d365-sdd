# az_function_app — Azure Function App

Serverless compute hosting custom code (HTTP APIs, event handlers) for the
solution. Stage-3 reference and Stage-4 `patterns/az_function_app.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Function App name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture triggers/functions, hosting plan, and bindings.

## Decision guide

- **Function App vs plug-in/flow.** Heavy/long-running/external compute → Function
  App; in-transaction Dataverse logic → `code_plugin`; simple orchestration →
  `flow_cloud`.
- **Trigger type** (HTTP / Service Bus / Event Grid / timer — timer belongs to
  `az_func_scheduled`) matches the integration pattern.
- **Managed identity to Dataverse/Key Vault/Service Bus**; secrets from Key Vault.
- **Plan choice** (Consumption/Premium) driven by cold-start, VNet, and scale needs.

## Anti-patterns

- Function App doing what a plug-in/flow should (or vice-versa).
- Connection strings/keys in app settings instead of Key Vault references.
- No telemetry to App Insights.

## Validation checklist

- [ ] `satisfies` declared (+ triggers/plan once authored).
- [ ] Identity + Key Vault + App Insights wired.

## Stage-4 build mapping

Function App (IaC) + deployed functions. Verified by Stage-5 tests (trigger →
expected function output/side effect).
