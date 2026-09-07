# Fixed-lambda selected-box parent lemma review

## Scope and status

This sidecar adds the missing parent-level finite logic on top of the sparse
digest fold.  It does not repeat the coefficient identity or redefine the
fixed-lambda, cell, partition, or digest structures.

No Lean or Lake command was run.  The declarations are an uncompiled proof
skeleton/interface, with no kernel, comparator, or registry status.

## New seam closed

- `SelectedBoxRow` packages a selected row witnessing a box-label membership.
- `selectedBoxRow_unique` uses `oneRowPerBox` to prove that two witnesses for
  the same sparse global label have the same row index.
- `selectedBoxMargin` is therefore a well-defined selected-box margin up to
  the supplied membership proof; `candidate_margin_independent_of_selected_row`
  records the exact witness-independence lemma.
- `selectedBoxMargin_positive` combines sparse label membership, the uniform
  strict upper premise, the positive denominator in `CellMarginData`, and the
  imported fixed-λ margin bridge to conclude a positive box-level margin.
- `uniform_selected_box_margins_positive` lifts this result to both declared
  eta partitions, and
  `uniform_admissibility_implies_uniform_selected_box_margins_positive`
  connects the existing uniform `lambda=2` admissibility proposition to that
  parent result.

The digest binding is deliberately only projected by
`parent_margin_result_does_not_change_digest_binding`.  It remains an
external canonical-row/digest premise and is not used to prove positivity.

## Remaining boundaries

The proof consumes, but does not establish, each row's `cellGamma > 0`,
`lambdaUpper = externalGamma / cellGamma`, `candidateMargin` equation,
strict upper condition, and one-row-per-box fact.  It does not bind those
fields to CSV/source bytes or verify the SHA-256 value.

The finite result quantifies only over labels in the supplied sparse
`Finset.image`.  It does not prove dense labels, complete 577-row coverage,
true-DH interval coverage, missing-cell exclusion, residual/PDE/trajectory
closure, or parent-node theorem closure.  The `256 + 321` accounting remains
declared-ledger bookkeeping only.

No state, registry, receipt, or shared script was modified, and no formal
certificate admission is implied.
