# az_func_scheduled — Scheduled Azure Function (Timer Trigger)

A timer-triggered function running recurring background work. Stage-3 reference and
Stage-4 `patterns/az_func_scheduled.md`.

> Phase-B skill. `_default` payload until a specific payload is added to
> `conventions.yml`.

## Required payload

`_default`:

| Field | Meaning |
| --- | --- |
| `name` | Scheduled function name. |
| `satisfies` | `[REQ-####]`. |

When authoring, capture the CRON schedule and the batch operation performed.

## Decision guide

- **Scheduled function vs Power Automate scheduled flow.** Heavy/bulk/compute-bound
  recurring work → timer function; light connector-based recurrence → scheduled
  `flow_cloud`.
- **CRON explicit + timezone-aware**; align with `batch_processing` requirements.
- **Idempotent + resumable.** Assume overlap/retry; checkpoint progress for large
  batches.
- **Managed identity + Key Vault**; telemetry to App Insights (duration, counts,
  failures).

## Anti-patterns

- Long bulk jobs in a Power Automate flow (timeouts) instead of a function.
- Non-idempotent runs that double-process on overlap.
- Silent failures with no telemetry/alert.

## Validation checklist

- [ ] `satisfies` declared (+ schedule/batch once authored).
- [ ] Idempotency + telemetry + schedule stated.

## Stage-4 build mapping

Timer-triggered function (IaC + code). Verified by Stage-5 tests (scheduled run →
expected batch outcome; overlap-safe).
