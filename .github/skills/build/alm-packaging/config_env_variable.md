# config_env_variable — Environment Variable

Externalizes environment-specific configuration so one managed solution runs
everywhere. Stage-3 reference and Stage-4 `patterns/config_env_variable.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_env_variable`:

| Field | Meaning |
| --- | --- |
| `name` | Environment variable schema/display name. |
| `data_type` | String / Number / Boolean / JSON / Data source / Secret. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Anything environment-specific becomes a variable** — URLs, IDs, toggles,
  thresholds — never hard-coded in flows/plug-ins.
- **Default vs current value.** Ship a default in the solution; set the current
  value per environment via the deployment settings file.
- **Secrets → Key Vault-backed** secret variables, not plain strings.
- **Consumers reference it** (flows, plug-ins, canvas) — the variable is the single
  source.

## Naming

- Prefixed, purpose-based (e.g. `contoso_ServiceApiBaseUrl`).

## Anti-patterns

- Hard-coded environment values in logic.
- Secrets stored as plain-string variables.
- Setting current values manually post-import instead of via settings file.

## Validation checklist

- [ ] `data_type`, `satisfies` declared.
- [ ] Default provided; current value delivered via settings file (secret → Key Vault).

## Stage-4 build mapping

Environment Variable (definition + value) in the solution / settings file.
Verified by Stage-5 tests (consumer reads the environment-correct value).
