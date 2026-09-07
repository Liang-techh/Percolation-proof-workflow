# P3 capMax minimality and witness equivalence

Status: exact-real order-algebra candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_CAPMAX_MINIMALITY.lean` consumes the explicit
upper-bound/attainment witness shape used by the preceding capMax sidecar. It
does not recompute a maximum and does not touch any budget or force expression.

## Results

- `capMax_le_candidate6`: every scalar candidate upper-bounding all six cap
  entries satisfies `capMax <= candidate`.
- `candidate_equals_capMax6`: a candidate is equal to `capMax` when it both
  upper-bounds every entry and is attained by one entry.
- `capMax_unique_of_same_caps6`: two upper+attainment witnesses for the same
  cap vector have identical scalar maxima.
- `attainment_values_equivalent6`: two attainment indices yield the same cap
  value. The theorem intentionally does not claim the indices themselves are
  unique.
- `upper_attainment_equiv_capMax6`: upper-bound plus attainment is equivalent
  to equality with the witness capMax.

## Boundary

Only finite witness/order algebra is covered. No load budget, scalar-cap
monotonicity, component-to-cap estimate, common context, force map, source
binding, numerical value, rounding evidence, coverage, admission, or registry
state is selected or inferred.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

