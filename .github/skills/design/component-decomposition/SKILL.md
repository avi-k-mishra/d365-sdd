---
name: component-decomposition
description: >-
  How to decompose a Stage 3 design into granular, typed components — one
  buildable unit per component_type from the closed vocabulary — and hand each off
  to its build skill with a declared required payload. Use when filling the
  FILL:solution zone of a DES-##.md.
allowed-tools: [view, edit, create, grep, glob]
---

# component-decomposition

Reusable **HOW** for turning design decisions into a list of granular, buildable
components — the bridge from Stage 3 design to the Stage 4 build skills under
`.github/skills/build/`.

## When to use

- You are filling the `FILL:solution` zone of `specs/design/DES-##.md`.
- You need to tag a component with a `component_type` and declare its payload.

## Mechanical process (deterministic)

1. **List one granular unit per type.** Each component is its own bullet
   `<name> (component_type: <type>)` using the closed vocabulary in
   `conventions.yml` `component_types` (families + axis mapping in
   `specs/_schema/component-types.md`). Never a single opaque blob bundling
   several types.
2. **Declarative-first tagging.** Prefer a `config_`/`uiux_`/`flow_` type over a
   `code_`/`az_` type; justify any escalation. If no type fits, raise an open
   question and **extend the taxonomy first** — never invent a type inline.
3. **Apply the component's build skill.** Look up the `component_type` in
   `conventions.yml` `component_type_skills` → the **skill**; load it from
   `.github/skills/build/<skill>/` (thin `SKILL.md` + the `<component_type>.md`
   reference) and follow its guidance.
4. **Declare the required payload.** Beneath each bullet, add an indented
   `key: value` sub-list — one line per field in
   `conventions.yml` `component_type_payloads.<type>.required` (backtick name =
   the `name`; `satisfies` + type-specific fields as sub-lines), per the
   *Design-item payload contract* in `specs/_schema/component-types.md`. Do not
   invent or omit required fields.
5. **No orphans.** Every component carries `satisfies: [REQ-####]` tracing to the
   feature's requirements.

## Ground rules

- **One buildable unit per type.** Granularity is the point — the list feeds
  Stage 4 tasks one-to-one.
- **Closed vocabulary.** Only `component_types` from `conventions.yml`; extend the
  taxonomy (with review) rather than inventing.
- **Skill + payload together.** Every tagged component both loads its build skill
  and declares the exact required payload.

## Anti-patterns

- Untyped or blob components (no `component_type`, or several types in one entry).
- Inventing a `component_type` not in `conventions.yml`.
- Silent escalation to `code_`/`az_` without a rationale.
- Omitting or inventing required payload fields; an orphan with no `satisfies`.
