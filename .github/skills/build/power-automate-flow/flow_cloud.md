# flow_cloud — Power Automate Cloud Flow

Solution-aware cloud flow automating a Dataverse process. Stage-3 reference and
Stage-4 `patterns/flow_cloud.md`.

## Required payload

From `conventions.yml` `component_type_payloads.flow_cloud`:

| Field | Meaning |
| --- | --- |
| `name` | Flow display name. |
| `trigger` | What starts the flow (Dataverse row create/update/delete + filter, scheduled, manual, or other connector). |
| `actions` | The ordered steps / branches the flow performs. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Trigger precision.** Use Dataverse trigger filters (columns + filter
  expression) so the flow runs only when it must — not on every write.
- **Flow vs plug-in.** Async orchestration/approvals/connectors → flow;
  synchronous/transactional/sub-second → `code_plugin`.
- **Error handling.** Configure run-after (on failure/timeout), retry policy, and a
  terminate/notify path. No silent failures.
- **Idempotency.** Design actions to tolerate duplicate trigger firings.
- **Connection references** for every connector (ALM portability), no inline auth.

## Naming

- Verb-first, scenario-based (e.g. `Notify Owner On Escalation`).

## Anti-patterns

- Unfiltered trigger firing on every row change.
- No failure branch / retry.
- Business logic that must be synchronous placed in a flow.
- Inline connections instead of connection references.

## Validation checklist

- [ ] `trigger`, `actions`, `satisfies` declared.
- [ ] Trigger filter, error handling, and flow-vs-plugin choice stated.
- [ ] Uses connection references.

## Stage-4 build mapping

Solution-aware cloud flow (+ connection references). Verified by Stage-5 tests
(trigger condition → expected actions/outcome).
