# config_audit — Audit Configuration

Governance component that enables and scopes Dataverse auditing. Stage-3 reference
and Stage-4 `patterns/config_audit.md`.

## Required payload

From `conventions.yml` `component_type_payloads.config_audit`:

| Field | Meaning |
| --- | --- |
| `name` | Audit configuration label. |
| `scope` | What is audited — environment on/off, which tables, which columns, and read-audit if required. |
| `satisfies` | `[REQ-####]`. |

## Decision guide

- **Three levels must all be on.** Org-level auditing, table-level auditing, and
  (optionally) column-level auditing are independent switches — enabling one
  without the others captures nothing.
- **Audit only what compliance requires.** Auditing every table/column bloats logs
  and storage; scope to the regulated data.
- **Read auditing** is expensive and separate — enable only when access logging is
  mandated (e.g. sensitive data access).
- **Retention** is governed at the environment/tenant level — reference the policy,
  don't assume infinite retention.

## Naming

- Name by the compliance driver (e.g. `GDPR — Contact PII Audit`).

## Anti-patterns

- Turning on org-level auditing but forgetting table/column flags (no data captured).
- Auditing everything (cost, noise).
- Using audit history as an application data store.

## Validation checklist

- [ ] `scope` (org + tables + columns / read) and `satisfies` declared.
- [ ] Driven by a stated compliance requirement.

## Stage-4 build mapping

Environment + table + column audit settings. Verified by Stage-5 tests
(audited change produces an audit record; non-scoped change does not).
