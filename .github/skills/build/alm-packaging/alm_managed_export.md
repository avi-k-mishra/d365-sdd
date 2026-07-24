# alm_managed_export — Managed Solution Export

The build step that produces a managed solution artifact for downstream
environments. Stage-3 reference and Stage-4 `patterns/alm_managed_export.md`.

## Required payload

From `conventions.yml` `component_type_payloads.alm_managed_export`:

| Field | Meaning |
| --- | --- |
| `name` | Export/artifact label. |
| `source_solution` | The unmanaged `alm_solution` being exported managed. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Managed everywhere but dev.** Test/UAT/prod receive managed; only the dev
  environment holds unmanaged.
- **Pipeline-produced, versioned.** Export via automated build (Power Platform CLI /
  Build Tools), stamp a version, store the artifact — no manual portal exports.
- **Upgrade vs update vs stage-and-upgrade.** Choose the import mode; stage-and-
  upgrade for controlled cutovers with deletes.
- **Include a settings file** for environment variables + connection references so
  imports are unattended.

## Naming

- Artifact named `<solution>_<version>_managed`.

## Anti-patterns

- Manual portal exports (no version, not reproducible).
- Importing unmanaged into shared/prod environments.
- Export without a deployment settings file (breaks unattended import).

## Validation checklist

- [ ] `source_solution`, `satisfies` declared.
- [ ] Versioned, pipeline-produced, settings-file-backed.

## Stage-4 build mapping

Managed `.zip` produced by the ALM pipeline. Verified by Stage-5 tests (artifact
imports/upgrades cleanly downstream).
