---
name: copilot-studio-agent
description: >-
  How to design and build Copilot Studio agents (topics, actions, knowledge,
  triggers) that integrate with Dataverse. Use for any DES component tagged
  mcs_<agentname>_* (wildcard).
allowed-tools: [view, edit, create, grep, glob]
---

# copilot-studio-agent

Reusable **HOW** for Microsoft Copilot Studio agents. Applied both when authoring
a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
matches:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `mcs_<agentname>_*` (e.g. `mcs_supportbot_topic`, `mcs_supportbot_action`) | [mcs.md](mcs.md) |

The `mcs_*` family uses a single wildcard reference file `mcs.md`. The
`<agentname>` segment identifies the owning agent; the trailing segment is the
component kind (topic / action / knowledge / trigger).

## Mechanical process (deterministic)

1. Confirm the `component_type` matches `mcs_*`; open [mcs.md](mcs.md).
2. Emit / verify the payload against the reference's **Required payload**
   (`_default`: name + satisfies until a specific payload is defined).
3. Apply its **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules

- **Generative + topics together.** Use generative orchestration with
  knowledge grounding; add explicit topics for deterministic/critical flows.
- **Actions call Dataverse/flows/connectors** via connection references
  (`integration-wiring`) — no inline secrets.
- **Solution-aware agent** for ALM; environment variables for per-environment config.
- **Responsible AI + auth.** Authenticated channels for data access; human handoff
  and content moderation configured.
- **Ground in Microsoft Learn (MCP)** — Copilot Studio changes rapidly.
