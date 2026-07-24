# Feature-stage skills (Stage 2 — Spec refinement)

Reusable "how-to" skills the agent (GitHub cloud agent, or VS Code Copilot) loads
while elevating the reviewed atomic `REQ-####.md` set into a testable baseline and
compiling one `FEAT-##.spec.md` per feature.

Same folder convention as [`../build/`](../build/): one folder per skill =
a `SKILL.md` (frontmatter `name`/`description`/`allowed-tools` + when-to-use +
mechanical process + ground rules + anti-patterns). `name` must equal the folder.

## Skills

| Skill | Covers |
| --- | --- |
| [`requirement-refinement`](requirement-refinement/) | Enrich REQ front-matter, attach structured NFRs, de-dup/reconcile across the backlog. |
| [`open-question-handling`](open-question-handling/) | Raise decision-ready questions; close only on a recorded human decision (Stage 2 & 3). |
| [`gherkin-authoring`](gherkin-authoring/) | Expand REQs into happy/negative/boundary scenarios with grounding; security needs a negative. |
| [`feature-grouping`](feature-grouping/) | Group REQs into Epic→Feature; build the acyclic `depends_on` graph; write `features.md`. |
| [`spec-compilation`](spec-compilation/) | Author FILL zones, run `compile_specs.py` for hash-guarded COMPILER zones, freeze the baseline. |

Grounded in the Phase-2 instructions in `.github/copilot-instructions.md` and
`.github/prompts/spec-authoring.prompt.md`.
