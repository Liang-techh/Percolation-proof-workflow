# P3 quantitative strict-gap lower bound

Status: bounded exact-real quantitative candidate, pending independent review.

## Scope

`NEW_CENTRAL_FD_HULL_QUANTITATIVE_GAP.lean` defines the selected component
gap

```text
gap[j] = load[j] * (qCap[j] - q[j]).
```

Under pointwise `load >= 0` and `q <= qCap`, it proves:

```text
weightedLoad(load,qCap) - weightedLoad(load,q)
  >= gap[j].
```

The proof uses an explicit Fin6 erase decomposition and requires all remaining
component gaps to be nonnegative. `weighted_gap_lower_bound_strict_witness6`
retains a positive selected gap as a quantitative witness, without reproving
the strict-order theorem.

## Boundary

This leaf does not repeat non-strict or strict order, obstruction tracking,
load-witness construction, capMax, scalar budget, force, source semantics,
coverage, admission, registry state, or Lean compilation. The component order
and nonnegative load conditions remain explicit premises.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; later
compilation remains candidate evidence only.

