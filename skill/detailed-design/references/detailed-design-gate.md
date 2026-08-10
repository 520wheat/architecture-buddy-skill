# Detailed Design Gate

Do not mark the package `design-ready` until all of these are satisfied with evidence.

1. Module coverage exists for every in-scope module.
2. Interfaces are complete enough to implement without inventing missing contracts.
3. Data and state ownership are explicit.
4. Cross-module consistency is checked.
5. Failure semantics are defined.
6. Concurrency behavior is defined where relevant.
7. Security and trust boundaries are explicit.
8. Observability expectations are explicit.
9. Tests and ordering constraints are named.
10. Pending facts have defaults, not just placeholders.
11. Rollback items are listed.

Keyword presence is not quality proof; the gate only passes when the document shows concrete, consistent design evidence.
