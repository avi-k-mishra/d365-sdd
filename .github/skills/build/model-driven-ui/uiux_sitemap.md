# uiux_sitemap — Site Map (App Navigation)

The navigation structure of a model-driven app. Stage-3 reference and Stage-4
`patterns/uiux_sitemap.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_sitemap`:

| Field | Meaning |
| --- | --- |
| `name` | Site map name. |
| `app` | The model-driven app the site map belongs to. |
| `areas` | Areas → groups → subareas (tables, dashboards, web resources, URLs). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **One site map per app.** The site map is owned by its `uiux_app`; design them
  together.
- **Group by task, not by schema.** Areas/groups reflect how users work, not table
  alphabetization.
- **Show only what the persona needs** — fewer, well-named subareas beat exhaustive
  navigation.
- **Privilege-trim.** Subareas hidden when the user lacks the table privilege; rely
  on security, don't duplicate site maps to "hide" things.

## Naming

- Areas/groups named by workflow (e.g. `Service`, `Knowledge`).

## Anti-patterns

- Navigation that mirrors the schema rather than the workflow.
- Overstuffed site map exposing every table.
- Cloning site maps to simulate security instead of using privileges.

## Validation checklist

- [ ] `app`, `areas`, `satisfies` declared.
- [ ] Task-oriented grouping; relies on privilege trimming.

## Stage-4 build mapping

App site map (appmodule sitemap) in the solution. Verified by Stage-5 tests
(navigation shows expected areas for the persona).
