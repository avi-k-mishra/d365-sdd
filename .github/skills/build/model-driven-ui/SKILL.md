---
name: model-driven-ui
description: >-
  How to design and build model-driven app UI/UX for Dataverse — forms, views,
  dashboards, charts, sitemaps, and the apps themselves. Use for any DES component
  tagged uiux_form, uiux_view, uiux_dashboard, uiux_chart, uiux_sitemap, or uiux_app.
allowed-tools: [view, edit, create, grep, glob]
---

# model-driven-ui

Reusable **HOW** for model-driven UX. Applied both when authoring a `DES-##.md`
(Stage 3) and when building it (Stage 4).

## When to use

Load this skill for every DES `solution.components` bullet whose `component_type`
is one of:

| component_type | Reference (== Stage-4 `patterns/<type>.md`) |
| --- | --- |
| `uiux_form` | [uiux_form.md](uiux_form.md) |
| `uiux_view` | [uiux_view.md](uiux_view.md) |
| `uiux_dashboard` | [uiux_dashboard.md](uiux_dashboard.md) |
| `uiux_chart` | [uiux_chart.md](uiux_chart.md) |
| `uiux_sitemap` | [uiux_sitemap.md](uiux_sitemap.md) |
| `uiux_app` | [uiux_app.md](uiux_app.md) |

## Mechanical process (deterministic)

1. Read the component's `component_type` and open the matching reference file.
2. Emit / verify the payload sub-list against the reference's **Required payload**.
3. Apply the reference's **Decision guide** and **Anti-patterns**.
4. Confirm `satisfies: [REQ-####]`.

## Ground rules (all types)

- **Configuration over code.** Achieve UX with forms/views/business rules first;
  reach for `code_pcf`/`code_webres` only when platform UX cannot express it.
- **Role-tailored, not one-size.** Use multiple forms/views by security role rather
  than hiding fields with script.
- **Accessibility + performance.** Reasonable column counts, no giant single form
  tab, keyboard/screen-reader friendly.
- **Security is server-side.** Never treat form-hide as security — see
  `dataverse-security` (`sec_field_profile`).
