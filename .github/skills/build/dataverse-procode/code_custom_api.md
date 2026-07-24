# code_custom_api — Custom API

A custom Dataverse message (RPC-style operation) with typed request/response.
Stage-3 reference and Stage-4 `patterns/code_custom_api.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Custom API unique name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture request/response parameters, bound/unbound, plug-in type,
and whether it is a function or action.

## Decision guide

- **Custom API over unmanaged workflow actions.** It's the modern, ALM-friendly way
  to expose a reusable operation with a contract.
- **Define the contract first** — request/response parameters are the public
  interface; version deliberately.
- **Bound vs unbound** to a table; function (GET, no side effects) vs action.
- **Privilege-gate** with a required privilege where the operation is sensitive.

## Anti-patterns

- Using legacy custom workflow activities for new reusable operations.
- Loose/undocumented parameter contracts.
- No privilege check on a sensitive operation.

## Validation checklist

- [ ] `satisfies` declared (+ parameters/binding once authored).
- [ ] Contract + privilege gating stated.

## Stage-4 build mapping

Custom API (+ plug-in implementation) in the solution. Verified by Stage-5 tests
(request → expected response/contract).
