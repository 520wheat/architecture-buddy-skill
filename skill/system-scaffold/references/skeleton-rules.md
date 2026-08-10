# Skeleton Rules

## Semantic-to-code mapping

- Map each confirmed semantic module to the smallest corresponding package, module, or folder in the selected stack.
- Preserve the confirmed boundaries; do not merge unrelated concerns into one scaffold target.
- Emit only the structural code needed to make the module visible and wired.

## Minimal interfaces

- Make interfaces consumer-owned.
- Include only required fields and required entry points.
- Keep empty methods or stubs only where the selected stack requires a concrete symbol to compile.

## Framework registration

- Register only the components required by the confirmed stack.
- Do not add framework glue for unsupported extension points.
- Do not introduce defaults that change the agreed architecture.

## Dependency restrictions

- Depend only on the confirmed stack and its direct runtime necessities.
- Prefer the fewest possible dependencies.
- Keep dependency direction aligned with the architecture handoff.

## Forbidden implementation

- Do not add business behavior.
- Do not add feature logic beyond scaffold wiring.
- Do not synthesize hidden workflows, fallback behavior, or assumed integrations.
- Do not create helper code that changes the design contract.

