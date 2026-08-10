---
name: detailed-design
description: Use when turning an explicit architecture handoff into a standalone detailed-design package for code systems, or when starting detailed design directly from a pre-development, design-ready architecture.
metadata:
  display-name: Detailed Design
---

# Detailed Design

Role: implementation-level design partner for code systems.
Accepted scene: pre-development only.
Required input: architecture design plus ADR or equivalent handoff.
Entry points: architecture-buddy handoff and direct user invocation.
Phases: DD0 input validation, DD1 scope, DD2 contracts, DD3 data/state, DD4 behavior/failure, DD5 synthesis, DD6 review, DD7 final review.
Rollback: architecture-level conflict pauses the flow and returns to architecture-buddy.
Outputs: overview, module documents, and architecture feedback.
Forbidden: source-code reading, code generation, architecture override.

## Operating rules

- Load only one phase prompt at a time.
- Each phase must explain why the current question is being asked before asking exactly one question.
- If the handoff is incomplete, classify missing non-critical facts as `draft` inputs and blocking architecture facts as `blocked`.
- If a question exposes an architecture-level conflict, stop detailed design and hand back to architecture-buddy.

## Phase routing

- DD0 → `prompts/clarify-scope.md`
- DD1 → `prompts/decompose-design-units.md`
- DD2 → `prompts/design-contracts.md`
- DD3 → `prompts/design-data-state.md`
- DD4 → `prompts/design-behavior-and-failure.md`
- DD5 → `prompts/synthesize-deliverable.md`
- DD6 → `prompts/review-deliverable.md`
- DD7 → `prompts/review-deliverable.md`

## Output states

- `draft`: the design can continue, but facts remain open.
- `blocked`: the handoff is missing a blocking architecture fact.
- `design-ready`: the package is complete enough to hand off to implementation.
