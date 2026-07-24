# config_bpf — Business Process Flow

Guided, stage-based process across one or more tables. Stage-3 reference and
Stage-4 `patterns/config_bpf.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_bpf`:

| Field | Meaning |
| --- | --- |
| `name` | Process flow display name. |
| `table` | The primary table (and any additional tables the flow spans). |
| `stages` | Ordered stages, each with its steps (fields) and any stage-gating. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **BPF for user-guided progression**, not for automation — pair with business
  rules / flows for the automated side effects.
- **Stage-gating** via required steps; use branching only when the path genuinely
  diverges on a data condition.
- **Cross-table flows** only when the process truly moves between tables (e.g.
  Lead → Opportunity); otherwise keep it single-table.
- **Security:** BPF availability follows the security role; assign deliberately.

## Naming

- Name by the business process (e.g. `Case Resolution Process`).

## Anti-patterns

- Using a BPF to enforce data rules that belong in a business rule.
- Excessive stages/branches that mirror UI clutter.
- Making every field a required step.

## Validation checklist

- [ ] `table`, `stages`, `satisfies` declared.
- [ ] Stage order + required steps stated; branching justified.

## Stage-4 build mapping

Business Process Flow definition (a special process/table) in the solution.
Verified by Stage-5 tests (stage transitions + required-step enforcement).
