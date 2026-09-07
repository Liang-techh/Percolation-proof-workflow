# P3 unified four-layer radius input

Status: exact-real typed input adapter candidate, pending independent review.

## Purpose

`NEW_CENTRAL_FD_HULL_UNIFIED_INPUT.lean` is the radius-side seam after the
four-layer force adapter. It does not repeat the Christoffel force map or the
Fin 6 weighted-power inequality. It constructs the single pair expected by
that existing consumer:

```text
R  = R_machineLift + R_centralFD + R_derivativeHull + R_exportCenter
mu = mu_machineLift + mu_centralFD + mu_derivativeHull + mu_exportCenter.
```

## Closed algebra

- `unified_remainder_bound6` proves the pointwise triangle bound for the four
  derivative-first tensor layers.
- `unified_mu_nonneg6` proves nonnegativity of the unified radius from the four
  layerwise nonnegative-radius premises.
- `build_unified_weighted_power_input6` packages the unified `R`, `mu`, the
  exact pointwise bound, and the nonnegative radius into
  `UnifiedWeightedPowerInput6`.

Each layer is counted once; no symmetry, diagonal doubling, or numerical
collapse is introduced.

## Explicit same-domain and velocity/weight boundary

`CommonPremises6` requires one declared `point` and one declared
`commonDomain`, with separate membership fields for machine/lift,
central-FD, derivative-hull, and export-center layers. It also carries an
explicit `velocityPremise` and a nonnegative weight vector. The adapter copies
these premises into the unified consumer input; it does not invent a velocity
box, a weight choice, or a domain inclusion proof.

The resulting record is intended to be destructured by the existing Fin 6
weighted-power consumer using its `remainder`, `radius`, `velocity`, and
`weight` fields. No second force or power theorem is proved here.

## Missing obligations and non-claims

The four pointwise radius hypotheses remain external. This leaf does not bind
any source/export implementation, Float64 or libm rounding, a concrete `mu`,
an interval partition, coverage, flowpipe semantics, source equality, P3/P4/P5
closure, admission, or registry state.

No local Lean/Lake command was run. Independent pinned-environment review must
check imports, elaboration, `#print axioms`, and placeholder absence; any later
compile remains candidate evidence only.

