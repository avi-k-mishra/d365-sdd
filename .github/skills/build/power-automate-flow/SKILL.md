---
name: power-automate-flow
description: >-
  How to design and build Power Automate cloud flows for Dataverse automation —
  triggers, actions, error handling, and connection references. Use for any DES
  component tagged flow_cloud.
allowed-tools: [view, edit, create, grep, glob]
---

# power-automate-flow

Reusable **HOW** for declarative process automation with Power Automate cloud
flows. Applied both when authoring a `DES-##.md` (Stage 3) and when building it
(Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `flow_cloud` | [flow_cloud.md](flow_cloud.md) |

## Mechanical process (deterministic)

1. Confirm `component_type: flow_cloud`, open [flow_cloud.md](flow_cloud.md).
2. Emit / verify the payload against the reference's **Required payload**.
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules

- **Flow vs plug-in.** Use a cloud flow for orchestration, approvals, and
  connector integration; use a `code_plugin` for synchronous, transactional, or
  low-latency logic. State the choice explicitly.
- **Bind to connection references**, never inline credentials — pair with
  `integ_connection_ref` components for ALM portability.
- **Idempotency + error handling** are mandatory: configure run-after / retry /
  terminate scopes; assume the trigger may fire more than once.
- **Solution-aware flows only** (created inside the solution) so they deploy via ALM.
