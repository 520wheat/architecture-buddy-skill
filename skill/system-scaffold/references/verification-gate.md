# Verification Gate

## Required checks

- stack compliance against the user-confirmed language/runtime, framework, dependency manager, and startup entrypoint
- module coverage for every confirmed module boundary
- dependency direction against the architecture and design handoff
- compile or build success for the selected stack
- reachable test entry points where the stack supports them
- visible unimplemented-item list for any missing business behavior

## skeleton-ready conditions

Mark the scaffold `skeleton-ready` only when all required checks pass and the remaining work is explicitly visible.

## Rollback and warnings

- If the stack is inconsistent with the handoff, rollback and return to blocked.
- If a build passes, treat that as scaffold validation only.
- A passing build does not prove business completion.
