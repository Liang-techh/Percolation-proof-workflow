# P4.fixed_lambda_uniform_declared_row_fold review

## Scope and status

This sidecar is intentionally source-independent. It defines a finite witness
record, a `Finset.all` conjunction fold, and a sparse box-label image. It does
not parse or import the 577-row CSV, does not bind a source evaluator, and does
not assert true-DH coverage. The file was not passed to Lean/Lake on this
machine, so there is no kernel-verified or compiled claim.

The only artifact facts used for orientation are the existing
`examples/routeb_fixed_lambda_fold/check_fold.py` contract and its
`RECEIPT.json`: the declared slices are eta=2.7 with 256 rows and eta=5.6 with
321 rows, for 577 rows total; the receipt says
`PASS_EXACT_DECLARED_FINITE_FOLD_ONLY`, while source binding, true-DH coverage,
Lean compilation, comparator acceptance, registry eligibility, and formal
certificate permission are all false. Those facts are not imported as Lean
theorems here.

## Concrete Lean declarations

In `NEW_FixedLambdaUniformDeclaredFold20260907.lean`:

- `FixedLambdaWitness` contains only `boxLabel : Nat`, `lambdaUpper : ℝ`, and
  `candidateMargin : ℝ`.
- `rowStrict` is exactly `2 < lambdaUpper ∧ 0 < candidateMargin`.
- `rowStrictBool`, `rowStrictFold`, and
  `rowStrictFold_eq_true_iff` provide the finite row-level conjunction.
- `fixedLambdaAdmissible` and `fixedLambdaAdmissible_iff` record the fixed
  lower-side fact `1 < 2` together with the strict row contract.
- `DeclaredPartition` contains an arbitrary finite `Finset Nat` of selected
  row indices, a row accessor, eta, and `oneRowPerBox` (box-label injectivity
  on the selected rows).
- `uniformStrictFold`, `uniformStrictFold_eq_true_iff`, and
  `uniform_strict_fold_of_each_row` prove that every selected row satisfying
  the strict upper-bound and positive-margin premises yields a true finite
  fold conjunction across all declared partitions.
- `boxLabels`, `mem_boxLabels_iff`, and `sparse_box_label_witness` expose label
  membership through `Finset.image` without assuming labels are consecutive.
- `card_rows_eq_card_sparse_boxLabels` gives row/label cardinality under
  `oneRowPerBox`; `sparse_labels_need_no_dense_ordinal` states the requested
  abstract sparse-label witness lemma without a dense ordinal.
- `UniformDeclaredWitness` packages the finite contract, and
  `UniformDeclaredWitness.fold_passes` closes its Boolean fold from the row
  premises.

## Boundaries still open

### Source boundary

There is no theorem that `lambdaUpper`, `candidateMargin`, `boxLabel`, eta,
or the row accessor equals a value computed by the Route-B source evaluator.
The decimal text, quantization rule, tolerance relation, ledger path, and
receipt digest remain external evidence. A future CSV connection may only be
an explicitly marked, uncompiled adapter until it has a pinned Lean compile
receipt and an independently checked source bridge.

### Coverage boundary

The fold quantifies only over the supplied finite `Finset`s. It proves no
partition completeness, no interval coverage, no true-DH validity, no missing
cell exclusion, and no extension from declared labels to a dense box domain.
`oneRowPerBox` is uniqueness/accounting, not coverage. In particular, the
fact that the diagnostic receipt reports 577 selected rows does not discharge
any of these premises.

### Comparator and admission boundary

No Lean compiler receipt, zero-`sorry`/allowed-axiom report, statement
comparator receipt, or exact comparator output is supplied. Therefore this
sidecar is not `LEAN_VERIFIED`, not comparator-accepted, not registry-eligible,
and not a formal certificate. It does not modify state, registry, receipt
files, or shared scripts. The decomposition script's pending obligations for
the pinned Lean receipt, axiom report, and statement comparator remain open.

## Admission checklist for a later adapter

1. Bind the finite accessor and labels to authoritative source evidence while
   preserving textual decimal provenance.
2. Separately prove the declared row predicates and one-row-per-box facts.
3. Supply a genuine source/true-DH/coverage theorem if a stronger Route-B
   claim is intended; the fold theorem alone cannot provide it.
4. Compile in the pinned Lean/Mathlib environment, audit axioms and `sorry`s,
   and run the exact standalone comparator contract.
5. Keep the candidate pending until the project admission workflow explicitly
   promotes it; a finite fold does not directly register a verified theorem.
