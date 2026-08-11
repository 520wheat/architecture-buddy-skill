# Verification Gate

## Required checks

- stack compliance against the user-confirmed language/runtime and version, framework and version, core_dependencies, dependency manager, build_command, test_command, format_command, start_command, and deployment_constraint
- module coverage for every confirmed module boundary
- dependency direction against the architecture and design handoff
- compile or build success for the selected stack
- reachable test, format, and start entry points where the stack supports them
- deployment-constraint compliance for the selected stack
- visible unimplemented-item list for any missing business behavior

## skeleton-ready conditions

Mark the scaffold `skeleton-ready` only when SC6 runs, all required checks pass, and the remaining work is explicitly visible.

## Rollback and warnings

- If the stack is inconsistent with the handoff, rollback and return to blocked.
- If a build passes, treat that as scaffold validation only.
- A passing build does not prove business completion.
