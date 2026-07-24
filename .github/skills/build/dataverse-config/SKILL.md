---
name: dataverse-config
description: >-
  How to design and build declarative Dynamics 365 business configuration —
  SLAs, automatic record creation rules, business process flows, business rules,
  routing and assignment rules, queues, and duplicate detection. Use for any DES
  component tagged config_sla, config_arc, config_bpf, config_business_rule,
  config_routing_rule, config_queue, config_assignment_rule, or config_dup_detection.
allowed-tools: [view, edit, create, grep, glob]
---

# dataverse-config

Reusable **HOW** for declarative business configuration — the no-code, no-flow
settings that shape how records behave. Applied both when authoring a `DES-##.md`
(Stage 3) and when building the artifact (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `config_sla` | [config_sla.md](config_sla.md) |
| `config_arc` | [config_arc.md](config_arc.md) |
| `config_bpf` | [config_bpf.md](config_bpf.md) |
| `config_business_rule` | [config_business_rule.md](config_business_rule.md) |
| `config_routing_rule` | [config_routing_rule.md](config_routing_rule.md) |
| `config_queue` | [config_queue.md](config_queue.md) |
| `config_assignment_rule` | [config_assignment_rule.md](config_assignment_rule.md) |
| `config_dup_detection` | [config_dup_detection.md](config_dup_detection.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the component's payload sub-list against the reference's
   **Required payload** (fields from `conventions.yml` `component_type_payloads`).
3. Apply the reference's **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]` is present and traces to a real requirement.

## Ground rules (all types)

- **Config beats code.** These types exist so behaviour is declared, not coded.
  Never escalate to `flow_`/`code_` what a business rule, SLA, or routing rule can
  express (`conventions.yml` `logic_tiers`).
- **Server-side over client-side.** Prefer server-evaluated logic (business rules
  scoped to Entity, real-time workflows) so rules hold across all clients and APIs.
- **Reuse OOB.** Extend the OOB Service/Sales configuration before inventing new
  mechanisms; state what is existing vs new.
