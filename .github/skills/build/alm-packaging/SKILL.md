---
name: alm-packaging
description: >-
  How to design and build the ALM packaging model for a Dataverse solution —
  solutions, publishers, managed exports, and environment variables. Use for any
  DES component tagged alm_solution, alm_publisher, alm_managed_export, or
  config_env_variable.
allowed-tools: [view, edit, create, grep, glob]
---

# alm-packaging

Reusable **HOW** for application lifecycle management packaging. Applied both when
authoring a `DES-##.md` (Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `alm_solution` | [alm_solution.md](alm_solution.md) |
| `alm_publisher` | [alm_publisher.md](alm_publisher.md) |
| `alm_managed_export` | [alm_managed_export.md](alm_managed_export.md) |
| `config_env_variable` | [config_env_variable.md](config_env_variable.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload sub-list against the reference's **Required payload**.
3. Apply the reference's **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Unmanaged in dev, managed downstream.** Author unmanaged in the dev
  environment; ship managed to test/prod via `alm_managed_export`.
- **One custom publisher + prefix** across the solution family for consistent
  schema names.
- **Environment-specific config → environment variables**, never hard-coded — so
  the same managed solution runs in every environment.
- **Source control is the source of truth.** Solutions unpack to the repo; the
  environment is a build output.
