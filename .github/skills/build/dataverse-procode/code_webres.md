# code_webres_* — Web Resource (wildcard)

Wildcard reference for the `code_webres_*` family (JavaScript, HTML, CSS, image,
and other web resources). Stage-3 reference and Stage-4
`patterns/code_webres_<subtype>.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Web resource name (with publisher prefix + logical path). |
| `satisfies` | `[REQ-####]`. |

When authoring a concrete subtype (`code_webres_js`, `code_webres_html`, …), add
its real fields (type, attached form/event, dependencies).

## Decision guide

- **Business rules before JavaScript.** Use declarative form logic first; JS web
  resources only for what rules can't do.
- **Use the client API (Xrm)**, no unsupported DOM manipulation; register on form
  events, not global overrides.
- **Libraries + dependencies** declared as dependent web resources; keep bundles
  small.
- **HTML/iframe web resources** are sandboxed — avoid them for security-sensitive
  UI; prefer PCF for rich controls.

## Anti-patterns

- JavaScript where a business rule works.
- Unsupported DOM/global overrides.
- Treating client-side JS validation/hide as security.

## Validation checklist

- [ ] `satisfies` declared (+ subtype/event/dependencies once authored).
- [ ] Justified over business rules; uses supported client API.

## Stage-4 build mapping

Web resource in the solution (+ form/event registration). Verified by Stage-5
tests (event → expected client behaviour).
