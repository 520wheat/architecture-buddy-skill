# Architecture Handoff Contract

## Required fields

- architecture file
- ADR paths
- `pre-development`
- `design-ready`
- scope
- confirmed boundaries
- quality targets
- pending facts
- non-goals

## Accepted handoff forms

- File-based handoff: a markdown file in the workspace containing the required fields.
- Message-based handoff: a direct message that names the required fields explicitly.

## Path resolution

- Absolute paths: use as-is.
- Relative paths in file-based handoff: resolve from the handoff file directory.
- Relative paths in message-based handoff: resolve from the active repository/worktree root that contains both the target Skill package and the architecture input.
- If more than one root could satisfy that rule, require the user to select one and mark the handoff `blocked` until the root is explicit.
- If resolution is still ambiguous after selection, treat it as a blocking architecture fact.

## Missing facts

- Missing non-critical fact: mark `draft`, note the gap, and continue if the architecture is still coherent.
- Missing blocking architecture fact: mark `blocked`, stop detailed design, and return to architecture-buddy.

## Blocking architecture facts

Facts are blocking when they change system boundaries, ownership, trust, data flow, or quality targets enough that detailed design would be speculative.

## Non-blocking facts

Facts are non-critical when they refine naming, examples, ordering, or other details that do not change the architecture contract.
