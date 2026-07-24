# Requirement-stage skills (Stage 1 — Intake)

Reusable "how-to" skills the agent (GitHub cloud agent, or VS Code Copilot) loads
while drafting atomic `REQ-####.md` files from born-digital intake documents.

Same folder convention as [`../build/`](../build/): one folder per skill =
a `SKILL.md` (frontmatter `name`/`description`/`allowed-tools` + when-to-use +
mechanical process + ground rules + anti-patterns). `name` must equal the folder.

## Skills

| Skill | Covers |
| --- | --- |
| [`intake-conversion`](intake-conversion/) | Convert born-digital docs via the MarkItDown MCP; preserve provenance; flag scanned/garbled files. |
| [`atomic-requirement-authoring`](atomic-requirement-authoring/) | Extract one-need-per-REQ atomic, testable requirements with provenance front-matter. |
| [`intake-traceability`](intake-traceability/) | Assign/register `INTK-####` in the intake registry and stamp it on every REQ. |

Grounded in the Phase-1 instructions in `.github/copilot-instructions.md`.
