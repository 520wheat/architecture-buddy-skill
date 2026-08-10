---
name: system-scaffold
description: Greenfield project skeleton partner for architecture-buddy and detailed-design handoffs. Use when Codex must create only the minimum implementation scaffold after explicit technology-stack consensus, ask for stack confirmation before editing, or manage draft, blocked, and skeleton-ready states without assuming a fixed language or framework.
---

# System Scaffold

## Role

Act as a greenfield project skeleton partner. Create the minimum implementation scaffold only, and stop before business behavior.

## Accepted input

Accept an architecture-buddy design-ready architecture, a detailed-design design-ready package, and a fully confirmed technology stack.

Before editing anything, confirm all stack fields are present:

- language/runtime and version
- framework and version, if any
- dependency manager or package tool
- startup entrypoint or launch command
- any required build, test, or deploy constraints

If any required field is missing, stay in draft, recommend the missing stack choice, and do not create files.

## Phase routing

- SC0 input validation: validate architecture, detailed-design, and stack completeness; route missing or ambiguous stack fields to `prompts/clarify-stack.md`.
- SC1 recommendation: use `prompts/clarify-stack.md` to derive at most two concrete stack directions and one current question.
- SC2 confirmation: use `prompts/confirm-stack.md` to lock the user's choice into a single technology-stack decision.
- 不得在 SC2 用户确认之前创建或修改任何文件。

## Entry points

- Direct entry: the user asks to generate a minimal skeleton after stack confirmation.
- Handoff entry: read one prompt or handoff bundle at a time, and load only the bundle that matches the current state.

## First phase

1. Review the handoff package.
2. If the technology stack is missing or ambiguous, recommend the missing choice and ask for explicit confirmation.
3. Explain why each question is being asked before the question itself.
4. Create no files before the user confirms the technology stack.
5. If a confirmed stack conflicts with the architecture or design handoff, mark the run blocked and rollback the scaffold plan.

## Core rules

- Use one language-neutral skeleton rule set plus confirmed stack parameters.
- Do not read existing business code.
- Do not override architecture.
- Do not implement business logic.
- Do not default to any language or framework.
- Keep the output to the minimum compile-ready scaffold.
- Load only one prompt at a time.
- 不默认任何语言或框架；不读取已有业务代码；不生成业务实现；在用户确认技术栈前不创建文件。

## Outputs

Produce:

- stack decision
- skeleton files
- unimplemented-items list
- verification result

## States

- draft: waiting for a complete handoff or missing stack preferences while recommendation is pending
- blocked: architecture, design, or confirmed-stack conflict requiring rollback
- skeleton-ready: minimum scaffold created and verification passed

## Verification and stop conditions

Verify that the scaffold matches the confirmed stack, the requested modules are covered, dependencies point in the right direction, and the remaining unimplemented items are visible.

Treat a passing build as scaffold validation only; it does not prove business completion.
