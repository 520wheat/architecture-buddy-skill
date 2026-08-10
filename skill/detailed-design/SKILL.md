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
- If DD6 or DD7 reaches `design-ready`, ask exactly `是否继续生成项目骨架代码？` before any scaffold handoff.
- Agreement to continue transfers the architecture path, detailed-design output path, confirmed boundaries, contracts, data and state rules, failure rules, non-goals, and user preferences to `system-scaffold`.
- User refusal ends detailed design normally without invoking `system-scaffold`.
- If later scaffold work exposes an architecture-boundary or quality-attribute conflict, rollback to `architecture-buddy`; if it exposes a detailed-design ambiguity, return to `detailed-design`.
- No scaffold file may be written before `system-scaffold` completes technology-stack confirmation.

## Deterministic helper

- `scripts/init-design.py --output DIR --name NAME [--force]` initializes `detailed-design-overview.md`, `modules/`, and `architecture-feedback.md`.
- The helper is path-safe for spaces and Unicode, refuses overwrite by default, and only overwrites when `--force` is supplied explicitly.
- `scripts/validate-input.py ARCHITECTURE.md --adr ADR.md [--adr ADR-2.md ...]` validates one architecture input plus repeatable ADR paths; `--adr` is required, rejects non-`pre-development`, non-`design-ready`, missing boundary evidence, unreadable ADRs, incomplete handoff fields, and pending facts without default / reason / trigger / rollback / reopen fields.
- `scripts/validate-deliverable.py OUTPUT_DIR` validates one detailed-design output directory; it requires `detailed-design-overview.md`, at least one module document, cross-module contract evidence, independent rollback sections, and pending-fact closure, and rejects `blocked`.
- Exit code `0` means the structure is acceptable; any non-zero exit means initialization or validation failed.
- Validation helpers only check structural evidence and input contract completeness; they do not judge architecture quality.

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

## Handoff after design-ready

When the design gate passes, detailed-design still owns the final user confirmation. Ask exactly `是否继续生成项目骨架代码？` and explain that a yes hands the architecture artifact path, detailed-design output path, confirmed boundaries, contracts, data and state rules, failure rules, non-goals, and user preferences to `system-scaffold`.

- If the user says no, end the detailed-design run normally with the package left at `design-ready`.
- If the user says yes, transfer only the confirmed handoff bundle and let `system-scaffold` enforce stack confirmation before any file creation.
- If scaffold planning reveals an architecture or quality-target conflict, return to `architecture-buddy`.
- If scaffold planning reveals only detailed-design ambiguity, return to `detailed-design`.
