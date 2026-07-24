---
name: open-question-handling
description: >-
  How to raise, record, and close open questions in D365-CE SDD specs so
  ambiguity is never silently guessed away — a question closes only on a recorded
  human decision. Use whenever a REQ, feature spec, or design has an ambiguity or
  a decision to gate (Stage 2 and Stage 3).
allowed-tools: [view, edit, create, grep, glob]
---

# open-question-handling

Reusable **HOW** for the decision-gating discipline that runs through both Stage 2
(spec) and Stage 3 (design). Ambiguity is made explicit and is resolved **only**
by a recorded human decision — never by the agent guessing to look complete.

## When to use

- A requirement, feature spec, or design contains an ambiguity or a choice with
  build implications.
- You need to check whether a spec/design is clear of blocking questions before a
  gate (baseline freeze, Gate A/B).

## Mechanical process (deterministic)

1. **Write a decision-ready question.** State the ambiguity + **2–3 concrete
   options**, each with its **build implication**. A vague "needs clarification"
   is not acceptable.
2. **Record it in two places** where applicable: the PR body (for reviewers) and
   the artifact's `## Notes / open questions` (or design open-questions) section
   as an unchecked box `- [ ]`.
3. **Close only with a recorded decision.** A question is closed **exclusively**
   by a human decision written as `- [x] … — decided by <name> <date>`. Leave it
   `- [ ]` otherwise.
4. **Never guess to close.** If no decision exists, the question stays open and
   the artifact does not advance past its gate.
5. **Gate check.** No `- [ ]` may remain before a Stage-2 baseline freeze or a
   Stage-3 Gate A/B.

## Ground rules

- **Only a human decision closes a question.** The agent proposes options; it
  never records the decision on the human's behalf.
- **Decision-ready or not at all.** Every open question carries concrete options
  and their consequences so a reviewer can decide fast.
- **Traceable closure.** A closed question names the decider and date, becoming
  citable grounding for downstream work.

## Anti-patterns

- Marking a question `- [x]` without a recorded decider + date.
- Filing a vague question with no options or build implications.
- Advancing to a gate with unresolved `- [ ]` items.
- Resolving an ambiguity silently inside the spec text.
