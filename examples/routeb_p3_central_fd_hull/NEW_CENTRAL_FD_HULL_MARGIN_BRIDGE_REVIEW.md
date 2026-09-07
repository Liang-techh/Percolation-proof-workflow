# P3 strict scalar-budget margin bridge

Status: exact-real order bridge candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_MARGIN_BRIDGE.lean` consumes two upstream facts:

```text
nonuniformBudget <= scalarCapBudget
scalarCapBudget < downstreamMargin.
```

It proves the strict conclusion `nonuniformBudget < downstreamMargin` by exact
order transitivity. The capMax-specialized version writes the scalar budget as
`capMax * totalLoad` using the shape-compatible `CapMaxWitness6`.

## Boundary

The nonuniform-to-scalar comparison and strict margin inequality are explicit
premises. This leaf does not compute a cap load, prove capMax minimality or
attainment equality, derive a downstream margin, or select any source,
velocity, numerical constant, rounding evidence, coverage, admission, or
registry state.

No force, component-to-cap, common-context, or weighted-power theorem is
repeated. No local Lean/Lake command was run. Independent pinned-environment
review must check imports, elaboration, `#print axioms`, and placeholder
absence; later compilation remains candidate evidence only.

