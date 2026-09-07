# Fixed-lambda uniform feasibility review

## Scope and status

This sidecar adds the finite sparse-union feasibility layer after the two-eta
union and selected-box parent lemmas.  It does not repeat digest composition,
union cardinality, selected-box witness uniqueness, or the coefficient bridge.

No Lean or Lake command was run.  The file is an uncompiled typed interface,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `marginAt` defines the candidate margin for one scalar λ over one typed cell.
  `marginAt_fixed_lambda_eq_declared` identifies it with the existing declared
  margin when the parameter record has exact `lambda=2`.
- `uniformCandidateFeasible` quantifies the strict lower bound, strict upper
  bound, and positive candidate margin over every element of the tagged sparse
  union.
- `union_positive_margins_of_uniform_strict_upper` converts both partition
  strict-upper premises into positivity for every selected union row.
- `UniformLambdaFeasibilityWitness` records one shared scalar parameter and an
  explicit finite-union nonemptiness premise.
- `fixed_two_uniform_feasibility_of_positive_margins` proves the pointwise to
  uniform implication: all selected declared margins positive imply a global
  feasible witness at the fixed `lambda=2`; the imported parameter record also
  carries `theta=1`.
- `fixed_two_uniform_feasibility_of_uniform_strict_upper` supplies the same
  result from the two partition-level strict-upper premises.

The proof uses the existing positive-denominator and strict-margin bridge.  It
does not derive any row premise from a digest or receipt.

## Remaining boundaries

The theorem consumes the finite union, its nonemptiness, positive denominator,
ratio/margin equalities, and declared row positivity or strict-upper premises.
It does not prove that the union is complete, that 577 rows cover the true-DH
domain, or that the candidate extends to missing cells or a continuous PDE.

No source/CSV binding, SHA/digest verification, interval coverage, residual or
trajectory closure, Lean compilation, comparator acceptance, or registry
promotion is implied.  The result is a declared finite feasibility interface
only; no state, registry, receipt, or shared script was modified.
