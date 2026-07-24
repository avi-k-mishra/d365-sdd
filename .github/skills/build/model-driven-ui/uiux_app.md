# uiux_app — Model-Driven App

The app shell that bundles tables, forms, views, dashboards, and a site map for a
persona. Stage-3 reference and Stage-4 `patterns/uiux_app.md`.

## Required payload

From `conventions.yml` `component_type_payloads.uiux_app`:

| Field | Meaning |
| --- | --- |
| `name` | App display name. |
| `app_type` | Model-driven (this skill) — recorded for clarity. |
| `tables` | The tables (and their components) included in the app. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **App per persona/journey**, not one app for everyone — scope the components to
  the audience.
- **Include only needed components.** The app designer pulls in forms/views/charts;
  keep it lean so navigation and load stay tight.
- **Pair with a `uiux_sitemap`** — the app's navigation is its site map.
- **Security-role assign the app** so only intended personas see it.

## Naming

- Name by audience/journey (e.g. `Customer Service Hub`).

## Anti-patterns

- One monolithic app spanning unrelated personas.
- Including every table "just in case".
- App not assigned to roles (visible to all).

## Validation checklist

- [ ] `app_type`, `tables`, `satisfies` declared.
- [ ] Persona-scoped; paired with a site map; role-assigned.

## Stage-4 build mapping

Model-driven app (appmodule) in the solution (+ role assignment). Verified by
Stage-5 tests (persona opens app, sees expected tables/navigation).
