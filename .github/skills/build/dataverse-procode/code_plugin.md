# code_plugin — Dataverse Plug-in

Server-side .NET code registered on a Dataverse message/event. Stage-3 reference
and Stage-4 `patterns/code_plugin.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Plug-in (type) name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture message, table, pipeline stage (pre/post), sync/async, and
filtering attributes.

## Decision guide

- **Plug-in vs flow.** Synchronous/transactional/validation/low-latency → plug-in;
  async orchestration/connectors → `flow_cloud`.
- **Right stage.** Pre-validation/pre-operation for changing input or blocking;
  post-operation for reacting. Filtering attributes to avoid needless firing.
- **Stateless + fast.** Sync plug-ins have a 2-minute limit; keep them lean, no
  long external calls in-transaction.
- **Config via environment variables / secure config**, secrets in Key Vault.

## Anti-patterns

- Business logic in a plug-in that configuration could do.
- Long/external synchronous calls blocking the transaction.
- Unfiltered registration firing on every update.
- Hard-coded configuration/secrets.

## Validation checklist

- [ ] `satisfies` declared (+ message/table/stage/mode once authored).
- [ ] Plug-in-vs-flow choice justified; filtering attributes set.

## Stage-4 build mapping

Registered plug-in assembly + step in the solution. Verified by Stage-5 tests
(triggering message → expected side effect).
