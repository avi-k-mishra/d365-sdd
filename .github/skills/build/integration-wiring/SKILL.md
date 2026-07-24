---
name: integration-wiring
description: >-
  How to design and build Power Platform integration wiring — custom connectors
  and connection references that let flows and apps talk to external systems. Use
  for any DES component tagged integ_connector or integ_connection_ref.
allowed-tools: [view, edit, create, grep, glob]
---

# integration-wiring

Reusable **HOW** for connecting Dataverse/Power Platform to external services.
Applied both when authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `integ_connector` | [integ_connector.md](integ_connector.md) |
| `integ_connection_ref` | [integ_connection_ref.md](integ_connection_ref.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload sub-list against the reference's **Required payload**.
3. Apply the reference's **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Custom connector = new API surface.** Only build an `integ_connector` when no
  standard/certified connector exists; otherwise just add a connection reference.
- **Connection references for ALM.** Flows/apps bind to `integ_connection_ref`, not
  to a connection directly — so managed solutions deploy without rewiring.
- **Auth is explicit.** OAuth2 / API-key / managed identity is declared, secrets in
  Key Vault (see `azure-infra`), never inline.
- **Gateway for on-prem.** On-premises targets go through the on-prem data gateway.
