# Route-B fixed-lambda two-row admissibility review

## Result and status

`NEW_FIXED_LAMBDA_ADMISSIBILITY20260907.lean` supplies the smallest typed
consumer for the fixed parameter bottleneck.  It is deliberately finite and
source-independent: two rows are represented by `Fin 2`, and each row carries
typed scalar data plus explicit denominator, ratio, and margin equalities.

No Lean or Lake command was run on this machine.  Consequently this sidecar
has no kernel-verified, compiled, zero-`sorry`, comparator-accepted, or
registry-eligible status.  The theorem shapes below are a formalization target
and a reviewable contract, not a verification receipt.

## Contract supplied

- `FixedLambdaParameters` carries one fixed `lambda` and one fixed `theta`,
  with explicit equalities `lambda = 2`, `theta = 1`, and
  `lambda = 1 + 1/theta`.
- `CellMarginData` makes `cellGamma > 0`,
  `lambdaUpper = externalGamma / cellGamma`, and
  `candidateMargin = externalGamma - 2 * cellGamma` explicit fields.
- `rowAdmissible` is the strict interval/margin consumer:
  `1 < lambda`, `lambda < lambdaUpper`, and `0 < candidateMargin`.
- `positive_margin_of_strict_upper` is the exact scalar implication using the
  positive denominator.  It is algebra, not a claim that any ledger row
  satisfies the premises.
- `TwoRowFixedLambdaWitness` uses `Fin 2` and binds both
  `affinePMILambda` and `schurLambda` to the same `params.lambda`.
  `admissible_of_strict_rows` consumes the two supplied obligations
  `lambdaUpper > 2` and `candidateMargin > 0` for every row.

The existing `check_fold.py`/`RECEIPT.json` may provide declared-artifact
orientation for a future adapter, but neither is imported or converted into a
Lean theorem here.  In particular, exact textual rational reconstruction and
the reported two eta partitions remain external evidence.

## Explicit non-claims

This sidecar does not prove that `externalGamma`, `cellGamma`, `lambdaUpper`,
or `candidateMargin` came from the Route-B source evaluator.  It does not prove
that the declared rows are all cells, that intervals cover the true-DH domain,
that missing boxes are impossible, or that any trajectory/PDE statement
follows.  `Fin 2` is only the interface arity.

It also does not reconcile the per-cell combined-Schur ledger with an
aggregate port ledger, prove residual absorption, establish a complete PMI,
or authorize a formal certificate.  A state-dependent lambda is excluded by
the equality-bound parameter slots, but no physical theorem is thereby
closed.

## Required next admission evidence

1. Bind each `CellMarginData` field to authoritative source bytes and preserve
   the decimal/quantization provenance.
2. Independently establish the row premises and the intended row-to-cell
   coverage relation; do not infer coverage from `Fin 2` or a row count.
3. Compile in the pinned Lean/Mathlib environment and inspect the resulting
   axiom and `sorry` report.
4. Run the exact statement/comparator contract, retaining the candidate as
   pending until the project admission workflow explicitly promotes it.

The current artifact therefore remains a typed, declared-ledger-level
formalization target only.
