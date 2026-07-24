# az_key_vault — Azure Key Vault

Central store for secrets, keys, and certificates used by the solution. Stage-3
reference and Stage-4 `patterns/az_key_vault.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Key Vault name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture the secrets/keys stored and the identities granted access.

## Decision guide

- **All secrets live here.** Connection strings, API keys, certificates —
  referenced by Function Apps, APIM, plug-ins (via env vars), never inlined.
- **RBAC access model** + managed identities for consumers; least privilege
  (get/list only).
- **Dataverse secret environment variables** are Key Vault-backed — this is the
  bridge to Power Platform.
- **Rotation + soft-delete/purge protection** enabled.

## Anti-patterns

- Secrets in app settings/config/source instead of Key Vault.
- Broad access policies granting more than get/list.
- Purge protection disabled on a production vault.

## Validation checklist

- [ ] `satisfies` declared (+ secrets/identities once authored).
- [ ] RBAC + managed identity + purge protection stated.

## Stage-4 build mapping

Key Vault (IaC) + access assignments. Verified by Stage-5 tests (authorized
identity reads a secret; unauthorized is denied).
