# integ_connector — Custom Connector

A custom Power Platform connector wrapping an external REST API (OpenAPI + auth +
policies). Stage-3 reference and Stage-4 `patterns/integ_connector.md`.

## Required payload

From `conventions.yml` `component_type_payloads.integ_connector`:

| Field | Meaning |
| --- | --- |
| `name` | Connector display name. |
| `connector_kind` | Custom (this component); records that it is not a standard/certified connector. |
| `api_spec` | The OpenAPI/Swagger definition (host, paths, operations). |
| `auth` | Authentication type (OAuth2 / API key / basic / no-auth) + security definition. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Only when no standard connector exists.** Prefer a certified/standard connector
  + `integ_connection_ref`; build custom for bespoke/internal APIs.
- **Solution-aware custom connector** so it deploys via ALM (host as an environment
  variable for portability).
- **Policies** (set-header, route, data-flow) for cross-cutting concerns rather
  than duplicating logic in every flow.
- **Auth via Key Vault-backed** environment variables/secrets; no baked keys.

## Naming

- Name by the external system (e.g. `Contoso Billing API`).

## Anti-patterns

- Building custom where a standard connector exists.
- Hard-coded host/keys (breaks per-environment deploy).
- Non-solution-aware connector (manual recreate per environment).

## Validation checklist

- [ ] `connector_kind`, `api_spec`, `auth`, `satisfies` declared.
- [ ] Host externalized; auth via secret/Key Vault; solution-aware.

## Stage-4 build mapping

Custom connector in the solution (+ connection reference for consumers). Verified
by Stage-5 tests (operation call returns expected external response).
