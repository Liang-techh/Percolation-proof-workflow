# Fixed-lambda downward monotonicity review

## Scope and status

This sidecar adds the generic monotonicity leaf after the finite sparse-union
feasibility interface.  It does not repeat the existing fixed-2 feasibility,
union cardinality, digest, selected-box, or coefficient-bridge results.

No Lean or Lake command was run.  The file is an uncompiled typed interface,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `row_margin_monotone_downward` uses `cellGamma > 0` to show that decreasing a
  shared λ cannot decrease `externalGamma - λ*cellGamma`.
- `UniformCandidateWitness` permits an arbitrary finite-union candidate
  `lambda₀`, retaining explicit union nonemptiness and feasibility premises.
- `uniform_candidate_feasible_downward` proves that every
  `1 < lambda ≤ lambda₀` remains strictly below every selected row's
  `lambdaUpper` and has positive candidate margin.
- `reduce_feasible_candidate_to_exact_two` packages the special case
  `2 ≤ lambda₀` as the existing exact `lambda=2, theta=1` witness.

The result is pointwise over the supplied tagged sparse union; no minimum
margin computation is needed because the same inequalities are preserved row
by row.

## Remaining boundaries

The proof consumes, rather than establishes, finite-union membership,
nonemptiness, positive denominators, strict upper bounds, and the candidate
margin formula.  It does not bind these fields to the CSV/source evaluator or
to a canonical digest.

Downward feasibility does not imply true-DH interval coverage, dense box
labels, missing-cell exclusion, residual/PDE/trajectory closure, formal
certificate validity, comparator acceptance, or registry eligibility.  No
state, registry, receipt, or shared script was modified.
