# schema_column — Dataverse column (attribute)

Canonical how-to for a Dataverse **column**. Stage-3 reference and Stage-4
`patterns/schema_column.md`.

## Required payload

From `conventions.yml` `component_type_payloads.schema_column`:

| Field | Meaning |
| --- | --- |
| `name` | Column display name (schema name carries publisher prefix). |
| `data_type` | Text, Multiline, Whole Number, Decimal, Currency, Boolean, DateTime, Lookup, Choice, File/Image, etc. |
| `required_level` | `none` (optional), `recommended`, or `required` (business required). |
| `satisfies` | `[REQ-####]` the column traces to. |

Declare the parent table, and — where the type demands it — the default value,
format, max length/precision, and any column-security flag.

## Decision guide

- **Pick the narrowest correct type.** Boolean for yes/no (not a 2-option
  choice); Whole Number for counts; Currency (not Decimal) for money; DateTime
  with the right behaviour (User Local vs Date Only vs Time-Zone Independent).
- **Choice vs Lookup.** A fixed, small, stable value list → `schema_choice`
  (choice column). A reference to rows in another table → Lookup (backed by a
  `schema_relationship`). Never model a growing list as a hard-coded choice.
- **Calculated / Rollup before code.** If the value is derived, use a calculated
  or rollup column rather than a plugin/flow. Record the escalation reason if you
  must go pro-code.
- **Column security.** For sensitive fields, enable column security and pair the
  column with a `sec_field_profile` component (do not rely on form-hide).
- **Required level.** Use `required` sparingly — only when the row is invalid
  without it; over-requiring breaks imports and integrations.

## Naming

- Schema name `<prefix>_<column>`; display name concise, no type suffixes.
- Booleans read as a state (`Escalated`), not a question.

## Anti-patterns

- Text column storing a number/date/boolean.
- Two-option `schema_choice` where a Boolean is correct.
- Hard-coded choice for an open/growing list (should be a Lookup).
- Business-required on optional-in-practice data (blocks imports).
- Form-level hide used as a substitute for column security.

## Validation checklist

- [ ] `data_type`, `required_level`, `satisfies` declared; parent table named.
- [ ] Choice-vs-Lookup decision correct for the value set.
- [ ] Sensitive columns reference a `sec_field_profile`.

## Stage-4 build mapping

Column → attribute metadata on the parent table; column-security-enabled columns
also wire to their FieldSecurityProfile. Verified by Stage-5 tests.
