# integ_connection_ref — Connection Reference

An ALM-portable pointer that decouples a flow/app from a concrete connection.
Stage-3 reference and Stage-4 `patterns/integ_connection_ref.md`.

## Required payload

From `conventions.yml` `component_type_payloads.integ_connection_ref`:

| Field | Meaning |
| --- | --- |
| `name` | Connection reference display name. |
| `connector` | The connector it targets (standard/certified, or a custom `integ_connector`). |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Every connector consumer uses one.** Flows and canvas apps bind to the
  connection reference, never to a raw connection — this is what makes managed
  deployment work.
- **One reference per connector per solution** — reused across all flows that use
  that connector.
- **Connection bound per environment.** The reference is set to an actual
  connection at/after import (via the deployment settings file), not in the design.
- **Standard connectors need only this** (no `integ_connector`).

## Naming

- Name by connector + purpose (e.g. `Office 365 Outlook — Notifications`).

## Anti-patterns

- Flows binding directly to connections (breaks ALM).
- Duplicate references for the same connector.
- Expecting the design to hard-set the target connection.

## Validation checklist

- [ ] `connector`, `satisfies` declared.
- [ ] Consumers bind to the reference; connection set via settings file.

## Stage-4 build mapping

Connection reference in the solution (bound per environment via settings file).
Verified by Stage-5 tests (consuming flow runs against the environment connection).
