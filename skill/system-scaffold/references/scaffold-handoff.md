# Scaffold Handoff

Use this handoff only when the architecture and design are already design-ready.

## Required inputs

- architecture path or message block
- detailed-design path or message block
- `design-ready` state for both artifacts
- confirmed modules, contracts, data shapes, state transitions, and failure rules
- scope and non-goals
- user technology preferences, fully confirmed as:
  - language/runtime and version
  - framework and version, if any
  - dependency manager or package tool
  - startup entrypoint or launch command
  - any build, test, or deploy constraints
- known build, test, and deploy constraints

Do not edit any file until every required stack field above is explicitly confirmed.

## Decision rules

- If a preference is missing, recommend the missing stack choice and ask for explicit confirmation.
- If the architecture conflicts with the confirmed stack, modules, contracts, or state rules, mark the run blocked and rollback the scaffold plan.
- If the handoff is complete and the stack is confirmed, proceed to skeleton generation.

## Handoff checklist

Confirm all of the following before generation:

1. The architecture artifact is design-ready.
2. The detailed-design artifact is design-ready.
3. The stack choice is explicit and user-confirmed.
4. The module boundaries are fixed.
5. The contracts and state rules are fixed.
6. The known constraints are recorded.
