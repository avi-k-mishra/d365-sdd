# Component-type taxonomy (Phase 3 design → granular components)

A `specs/design/DES-##.md` must not collapse into one opaque blob. In the design's
`FILL:solution` zone, **every** entry of the `components` list is tagged with one
**`component_type`** so the design reads as a set of granular, independently-buildable
units — one buildable component per type. This keeps each design element small enough
to understand and (downstream, in Stage 4) to build and test on its own.

The closed vocabulary lives in `conventions.yml` under `component_types`; this file
is the human-readable reference and the **family → design-axis** mapping. Extend both
as the pattern evolves.

## Format

`<family>_<type>` (lowercase, snake_case). Some ids are parameterised:

| Parameterised id | Meaning | Examples |
|---|---|---|
| `config_ai_<type>_<type>` | Dataverse-stored AI-agent config | `config_ai_orderstatus_topic` |
| `mcs_<agentname>_<type>` | Copilot Studio agent artefact | `mcs_orderstatus_topic`, `mcs_orderstatus_action`, `mcs_orderstatus_knowledge` |
| `az_ai_<type>_<type>` | Azure AI component | `az_ai_foundry_agent`, `az_ai_openai_deployment` |
| `code_webres_<type>` | web-resource kind | `code_webres_js`, `code_webres_html`, `code_webres_css` |

## Families and types

| Family | Types | Authoring MCP |
|---|---|---|
| **`schema_`** | `schema_table`, `schema_column`, `schema_relationship`, `schema_choice`, `schema_key` | Dataverse |
| **`config_`** | `config_sla`, `config_arc`, `config_bpf`, `config_business_rule`, `config_routing_rule`, `config_queue`, `config_assignment_rule`, `config_dup_detection`, `config_env_variable`, `config_audit`, `config_ai_<type>_<type>` | Dataverse / pac |
| **`uiux_`** | `uiux_form`, `uiux_view`, `uiux_dashboard`, `uiux_chart`, `uiux_sitemap`, `uiux_app` | pac |
| **`flow_`** | `flow_cloud` | pac |
| **`code_`** | `code_plugin`, `code_custom_api`, `code_pcf`, `code_webres_<type>` | pac / Azure |
| **`mcs_`** | `mcs_<agentname>_<type>` (topic, action, knowledge, …) | Copilot Studio |
| **`sec_`** | `sec_role`, `sec_field_profile`, `sec_business_unit`, `sec_team` | Dataverse / pac |
| **`az_`** | `az_apim`, `az_service_bus`, `az_key_vault`, `az_function_app`, `az_func_scheduled`, `az_app_insights`, `az_event_grid`, `az_ai_<type>_<type>` | Azure / Bicep |
| **`bi_`** | `bi_dataset`, `bi_report` | Power BI |
| **`alm_`** | `alm_solution`, `alm_publisher`, `alm_managed_export` | pac |
| **`integ_`** | `integ_connector`, `integ_connection_ref` | pac / Azure |

## Design-axis coverage

Every design axis (`conventions.yml` `decision_axes`) is realised by at least one
component family, so a fully-decomposed design leaves no axis un-buildable. The only
exception is `environment`, which is a cross-cutting Stage-6 (CI/CD ALM) concern, not
a per-component build artefact.

| Design axis | Realising component families |
|---|---|
| `logic_tier` | `config_` → `flow_` → `code_` (declarative-first ladder) |
| `data_residency` | `schema_` (Dataverse-native), `az_` / `integ_` (external) |
| `alm_boundary` | `alm_` |
| `security` | `sec_` |
| `integration` | `integ_`, `az_` |
| `environment` | *cross-cutting → Stage 6 CI/CD (no component family)* |
| `ux_surface` | `uiux_`, `code_pcf`, `code_webres_` |
| `observability` | `config_audit`, `az_app_insights` |
| `batch_processing` | `flow_cloud`, `az_func_scheduled`, `code_plugin`, `az_service_bus` |
| `reporting` | `uiux_dashboard`, `uiux_chart`, `bi_` |

## Skill library (map + required payload)

Each `component_type` is served by one **skill** — a reusable "how-to" for building
that kind of component, applied both when authoring a DES (Stage 3) and building it
(Stage 4). The skill grouping is a **domain grouping layered over the type prefix**,
so some `config_*` types are re-homed by concern (`config_audit` →
`dataverse-security`, `config_env_variable` → `alm-packaging`, `config_ai_*` →
`dataverse-ai`).

- **Map + rollout phases:** `conventions.yml` `component_type_skills` (skill → covered
  types) and `skill_phases` (A = active, B = deferred). All 47 types are mapped exactly
  once. A skill lives at `.github/skills/<skill>/` = a thin `SKILL.md` router + one
  `<component_type>.md` deep reference per covered type; that reference file **is** the
  Stage-4 `patterns/<component_type>.md` (one canonical asset, both stages).
- **Required payload:** `conventions.yml` `component_type_payloads` lists the minimum
  fields each design item must declare in its `data_model` entry (falling back to
  `_default: [name, satisfies]`). This is the single source of truth read by the prompt
  files (guidance) and by `validate_design.py` (enforcement, Step validate-payload).
- **Custom connectors:** `integ_connector` = a **custom** connector you author (OpenAPI
  + auth + policies); standard/certified connectors need only an `integ_connection_ref`.

## Rules

- Tag **every** component in `FILL:solution` with exactly one `component_type` from
  the closed vocabulary (or a valid parameterised form). `validate_design.py`
  enforces this per component bullet — an untagged primary bullet in the
  `components:` list fails the gate (legacy designs are exempt).
- **Declarative-first:** prefer a `config_` / `uiux_` / `flow_` type over a `code_` /
  `az_` type; any escalation to a pro-code type must carry the same grounded rationale
  the `logic_tier` axis records.
- Choose the **most specific** type that fits; if none fits, do not invent a type
  silently — raise it as an open question so the taxonomy can be extended in
  `conventions.yml` first.
