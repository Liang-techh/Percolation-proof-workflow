# P3 explicit finite cap-max budget seam

Status: exact-real finite-sum candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_CAPMAX.lean` compresses a nonuniform six-entry cap vector
to an explicit scalar `capMax`. It intentionally uses a witness contract rather
than an unverified finite-set maximum API:

```text
qCap[i] <= capMax for every i
qCap[iWitness] = capMax for some iWitness : Fin 6.
```

`capMax_nonneg6` derives scalar cap nonnegativity from the witness and
componentwise cap nonnegativity.

## Budget result

For nonnegative load coefficients,

```text
sum_i load[i] * qCap[i]
  <= capMax * sum_i load[i].
```

The core theorem is `loadCapBudget6_le_maxCapBudget6`; the transitivity theorem
`capMax_budget_transit6` consumes an already established nonuniform consumer
bound and transfers it to the scalar cap-max budget.

No component-to-cap derivation, scalar-cap monotonicity theorem, common context,
force map, or radius monotonicity is repeated.

## Boundary

The cap vector, maximum witness, load vector, and upstream consumer bound are
all explicit premises. No concrete source, velocity box, numerical value,
rounding evidence, coverage, admission, or registry state is selected or
inferred.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

