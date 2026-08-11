---
name: system-scaffold
description: Use when Codex must scaffold a new greenfield project from pre-development, design-ready architecture and detailed-design handoffs with explicit stack confirmation before any file creation.
---

# System Scaffold

## Role

Act as a greenfield project skeleton partner. Create the minimum implementation scaffold only, and stop before business behavior.

## Accepted input

Accept a pre-development, design-ready architecture handoff and a design-ready detailed-design package, plus optional user preference notes.

Stack completeness is checked in SC0; complete technology-stack confirmation is not required to enter the skill.
Complete stack confirmation is the SC2 gate and must be finished before SC4 generation starts.

Before editing anything, confirm all stack fields are present:

- language/runtime and version
- framework and version, if any
- core_dependencies
- dependency manager or package tool
- build_command
- test_command
- format_command
- start_command
- deployment constraints

If any required field is missing, stay in draft, recommend the missing stack choice, and do not create files.

## Phase routing

- SC0 input validation: validate greenfield scope, pre-development/design-ready handoffs, and stack completeness; route missing or ambiguous stack fields to `prompts/clarify-stack.md`. If the request is for an existing project, source-code reading, or refactoring, mark blocked immediately and do not read code or write files.
- SC1 recommendation: use `prompts/clarify-stack.md` to derive at most two concrete stack directions and one current question.
- SC2 confirmation: use `prompts/confirm-stack.md` to lock the user's choice into a single technology-stack decision.
- SC3 design mapping: use `prompts/map-design-to-skeleton.md` to map each design unit to the smallest code target, preserve module boundaries, and stop on contradictions.
- SC4 skeleton generation: use `prompts/generate-skeleton.md` with `templates/skeleton-manifest.md` to emit only the minimum stack syntax scaffold and list every generated file before writing.
- SC5 unimplemented-item recording: use `prompts/record-unimplemented.md` with `templates/unimplemented-items.md` to record every empty method and `not implemented` path.
- SC6 verification: use `prompts/verify-skeleton.md` after SC5 and allow `skeleton-ready` only when SC6 passes.
- 不得在 SC2 用户确认之前创建或修改任何文件。

## Entry points

- Direct entry: the user asks to generate a minimal greenfield skeleton after stack confirmation.
- Handoff entry: read one prompt or handoff bundle at a time, and load only the bundle that matches the current state.
- Phase flow: SC0 → SC1 → SC2 → SC3 → SC4 → SC5 → SC6, with SC6 as the only path to `skeleton-ready`.

## First phase

1. Review the handoff package.
2. If the request is for an existing project, source-code reading, or refactoring, mark blocked immediately and do not read code or write files.
3. If the technology stack is missing or ambiguous, recommend the missing choice and ask for explicit confirmation.
4. Explain why each question is being asked before the question itself.
5. Create no files before the user confirms the technology stack.
6. If a confirmed stack conflicts with the architecture or design handoff, mark the run blocked and rollback the scaffold plan.

## Core rules

- Use one language-neutral skeleton rule set plus confirmed stack parameters.
- Do not introduce per-language adapter packages or duplicate stack-specific rule sets.
- Do not read existing business code.
- Do not override architecture.
- Do not implement business logic.
- Do not default to any language or framework.
- Keep the output to the minimum compile-ready scaffold.
- Load only one prompt at a time.
- greenfield only: if the request targets an existing project or a refactor, block immediately and do not inspect code or write files.
- 不默认任何语言或框架；不读取已有业务代码；不生成业务实现；在用户确认技术栈前不创建文件。

## Outputs

Produce:

- stack decision
- skeleton manifest
- skeleton files
- unimplemented-items list
- SC6 verification result

## States

- draft: waiting for a complete handoff or missing stack preferences while recommendation is pending
- blocked: architecture, design, or confirmed-stack conflict requiring rollback
- skeleton-ready: minimum scaffold created and SC6 verification passed

## Verification and stop conditions

Verify that the scaffold matches the confirmed stack, the requested modules are covered, dependencies point in the right direction, and the remaining unimplemented items are visible.

Treat a passing build as scaffold validation only; it does not prove business completion.
