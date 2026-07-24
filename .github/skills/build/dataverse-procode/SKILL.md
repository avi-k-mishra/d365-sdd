---
name: dataverse-procode
description: >-
  How to design and build Dataverse pro-code extensions — plug-ins, custom APIs,
  PCF controls, and web resources. Use for any DES component tagged code_plugin,
  code_custom_api, code_pcf, or code_webres_* (wildcard).
allowed-tools: [view, edit, create, grep, glob]
---

# dataverse-procode

Reusable **HOW** for professional-developer extensions on Dataverse. Applied both
when authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `code_plugin` | [code_plugin.md](code_plugin.md) |
| `code_custom_api` | [code_custom_api.md](code_custom_api.md) |
| `code_pcf` | [code_pcf.md](code_pcf.md) |
| `code_webres_*` (e.g. `code_webres_js`, `code_webres_html`) | [code_webres.md](code_webres.md) |

`code_webres_*` uses a single wildcard reference file `code_webres.md`.

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload against the reference's **Required payload**
   (`_default`: name + satisfies until a specific payload is defined).
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Code is the last resort.** Exhaust configuration (business rules, flows, forms)
  before pro-code; justify why the platform can't express it.
- **Plug-in vs flow.** Synchronous/transactional/low-latency → plug-in; async
  orchestration → `flow_cloud`.
- **Registered in the solution**, secrets via environment variables/Key Vault,
  no hard-coded config.
- **Testable + observable.** Unit-testable logic, telemetry to App Insights
  (`azure-infra`), graceful error handling.
