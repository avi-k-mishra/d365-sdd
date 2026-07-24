# Design-stage skills (Stage 3 — Design)

Reusable "how-to" skills the agent (GitHub cloud agent, or VS Code Copilot) loads
while turning one approved `FEAT-##.spec.md` into a `DES-##.md` (and `UX-##.md`)
solution design on the Microsoft stack, grounded via the Microsoft Learn MCP.

Same folder convention as [`../build/`](../build/): one folder per skill =
a `SKILL.md` (frontmatter `name`/`description`/`allowed-tools` + when-to-use +
mechanical process + ground rules + anti-patterns). `name` must equal the folder.

These cover the **design method** (decision axes, grounding, decomposition,
observability, compilation). The per-`component_type` how-to references live in
[`../build/`](../build/) — the `component-decomposition` skill hands each tagged
component off to its build skill.

## Skills

| Skill | Covers |
| --- | --- |
| [`decision-axes`](decision-axes/) | Record all ten architect decision axes with grounded, declarative-first rationale. |
| [`grounded-architecture`](grounded-architecture/) | Ground every capability/feasibility claim in Microsoft Learn / live-environment MCPs. |
| [`component-decomposition`](component-decomposition/) | Tag one granular unit per `component_type`; apply its build skill; declare the required payload. |
| [`observability-design`](observability-design/) | Author the mandatory events/metrics/traces/alerts/audit block. |
| [`design-compilation`](design-compilation/) | Author FILL zones + UX spec, run `compile_design.py`, pass Gate A/B. |

Grounded in the Phase-3 instructions in `.github/copilot-instructions.md` and
`.github/prompts/design-authoring.prompt.md`.
