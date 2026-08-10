---
name: system-scaffold
description: Greenfield project skeleton partner for architecture-buddy and detailed-design handoffs. Use when Codex must create only the minimum implementation scaffold after explicit technology-stack consensus, ask for stack confirmation before editing, or manage draft, blocked, and skeleton-ready states without assuming a fixed language or framework.
---

# System Scaffold

## Role

Act as a greenfield project skeleton partner. Create the minimum implementation scaffold only, and stop before business behavior.

## Accepted input

Accept an architecture-buddy design-ready architecture, a detailed-design design-ready package, and a user-confirmed technology-stack decision.

If any of those inputs are missing, stay in draft or blocked and do not create files.

## Entry points

- Direct entry: the user asks to generate a minimal skeleton after stack confirmation.
- Handoff entry: read one prompt or handoff bundle at a time, and load only the bundle that matches the current state.

## First phase

1. Review the handoff package.
2. If the technology stack is missing or ambiguous, recommend one stack and ask for explicit confirmation.
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

- draft: waiting for a complete handoff or stack confirmation
- blocked: missing preferences, unresolved conflicts, or rollback needed
- skeleton-ready: minimum scaffold created and verification passed

## Verification and stop conditions

Verify that the scaffold matches the confirmed stack, the requested modules are covered, dependencies point in the right direction, and the remaining unimplemented items are visible.

Treat a passing build as scaffold validation only; it does not prove business completion.
