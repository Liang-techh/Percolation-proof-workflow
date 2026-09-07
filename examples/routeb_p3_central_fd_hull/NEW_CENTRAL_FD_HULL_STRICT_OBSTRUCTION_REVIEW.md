# P3 strict cap-load obstruction leaf

Status: bounded exact-real obstruction candidate, pending independent review.

## Results

`NEW_CENTRAL_FD_HULL_STRICT_OBSTRUCTION.lean` records two failure modes for a
strict weighted cap-load conclusion:

- `no_strict_without_cap_gap6`: if every component cap is equal, the weighted
  loads are equal and strictness is impossible;
- `explicit_zero_support_counterexample6`: on `Fin 6`, a strict gap at one
  coordinate can coexist with exact equality when that coordinate has zero
  load (the construction uses zero load everywhere and a one-coordinate cap
  gap);
- `no_strict_from_pointwise_term_equality6`: any pointwise equality of weighted
  terms blocks a strict sum inequality.

These facts explain why the strict order leaf must retain a positive selected
load premise together with a strict selected cap gap. They do not weaken or
replace the existing strict theorem.

## Boundary

This is obstruction tracking only. It does not compute a load witness, radius,
capMax, scalar budget, force map, physical/source semantics, coverage,
admission, registry state, or Lean compilation claim.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

