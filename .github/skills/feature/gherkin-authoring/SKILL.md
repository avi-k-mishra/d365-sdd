---
name: gherkin-authoring
description: >-
  How to expand thin requirement statements into behaviour-focused Gherkin
  scenarios (happy, negative, boundary) grounded in reviewed REQs and recorded
  decisions for D365-CE SDD Stage 2. Use when writing acceptance criteria /
  scenarios for a REQ.
allowed-tools: [view, edit, create, grep, glob]
---

# gherkin-authoring

Reusable **HOW** for elaborating each reviewed requirement into testable
`scenarios:` — the behavioural contract a feature will later be verified against.

## When to use

- You are expanding a REQ's thin statement into acceptance scenarios in Stage 2.
- A `security`-type REQ needs its mandatory negative scenario.

## Mechanical process (deterministic)

1. **Expand into `scenarios:`** with the sanctioned kinds `happy`, `negative`,
   and `boundary` (`conventions.yml` `scenario_kinds`).
2. **Keep every criterion behaviour-focused** — observable Given/When/Then
   outcomes, not implementation or platform mechanics.
3. **Ground each scenario.** List the evidence it rests on (reviewed `REQ` ids /
   recorded decisions) under a `grounding:` list before finalising. No scenario
   without grounding.
4. **Security REQs require a negative scenario.** A `type: security` REQ **must**
   have at least one `negative` scenario (`security_requires_negative`) or Stage-2
   validation fails.
5. **Defer feasibility.** Do not encode whether D365 *can* satisfy a scenario —
   platform feasibility is Stage 3 Design; surface doubts as open questions.

## Ground rules

- **Behaviour, not build.** Scenarios describe what the user/system observes, not
  how it is implemented.
- **Traceable.** Every scenario cites its `grounding:` (REQ ids / decisions).
- **Cover the edges.** Prefer at least one `negative` and one `boundary` per
  meaningful requirement, not only `happy`.
- **Solution-agnostic.** No Dataverse/Azure specifics — that arrives in Design.

## Anti-patterns

- A `security` REQ with no `negative` scenario.
- Scenarios with no `grounding:` reference.
- Implementation-flavoured steps ("insert row into table X").
- Only happy-path coverage.
