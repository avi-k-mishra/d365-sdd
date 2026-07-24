# az_apim — Azure API Management

Gateway that fronts, secures, and governs APIs consumed by / exposed from the
solution. Stage-3 reference and Stage-4 `patterns/az_apim.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | APIM instance / API name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture APIs, products, policies, and backends.

## Decision guide

- **APIM when you need governance** — throttling, auth, transformation, versioning,
  a single façade over multiple backends. Skip it for a single simple call.
- **Policies for cross-cutting concerns** (auth, rate-limit, caching, header
  injection) rather than per-consumer logic.
- **Managed identity to backends**, secrets/named-values from Key Vault.
- **Products + subscriptions** to gate and meter consumers.

## Anti-patterns

- APIM in front of a single trivial API (needless hop/cost).
- Backend keys embedded in policies instead of Key Vault named values.
- Public backends bypassing the gateway.

## Validation checklist

- [ ] `satisfies` declared (+ APIs/policies once authored).
- [ ] Auth/rate-limit policies + Key Vault-backed secrets.

## Stage-4 build mapping

APIM (IaC-deployed) with APIs/policies. Verified by Stage-5 tests (call through the
gateway honors policy + returns expected response).
