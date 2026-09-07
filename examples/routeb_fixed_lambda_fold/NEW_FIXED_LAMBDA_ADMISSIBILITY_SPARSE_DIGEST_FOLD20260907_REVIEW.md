# Fixed-lambda sparse digest fold review

## Scope and status

`NEW_FIXED_LAMBDA_ADMISSIBILITY_SPARSE_DIGEST_FOLD20260907.lean` adds the
sparse-label fold layer on top of the existing fixed-lambda consumer and
coefficient bridge.  It does not repeat `coefficient_identity` or redefine
the parameter/margin structures.

No Lean or Lake command was run.  This is an uncompiled typed interface, not a
kernel-verification receipt, comparator result, or registry admission.

## What is typed

- `SparseDeclaredPartition` keeps an arbitrary `Finset Nat` of selected row
  indices, a row accessor, a box-label accessor, and an explicit
  `oneRowPerBox` injectivity premise.
- `boxLabels`, `mem_boxLabels_iff`, and
  `card_rows_eq_card_sparse_boxLabels` expose sparse global labels without
  assuming `range rows.card`, consecutive labels, or dense coverage.
- `ExactWitnessDigest` is a length-64 digest token.  The partition carries an
  explicit `digestOracle` and `digest_binding` over
  `rows.toList.map rowEncoding`, so the digest input is tied to the selected
  row membership and canonical order.  This is an external binding premise;
  no SHA-256 computation is claimed.
- `strictUpperRows_iff_positiveMarginRows` lifts the imported fixed-λ margin
  bridge over the exact selected `Finset`.
- `Declared577SparseFold` records the two declared slices as separate sparse
  partitions with row-count premises `256` and `321`; the supplied premises
  imply the accounting identity `577` only.
- `selected_box_has_positive_margin` makes the requested membership-to-margin
  connection explicit: a selected box label has a selected row with positive
  fixed-λ margin whenever the row-level strict-upper premise is supplied.

## External premises and non-claims

The digest token, oracle, row encodings, row counts, scalar fields, and
one-row-per-box facts are not sourced or checked against the CSV here.  The
sidecar does not prove that the 577 rows are complete, that labels cover the
true-DH domain, or that the two eta slices exhaust the Route-B partition.

It also does not establish source evaluator binding, interval soundness,
residual/PDE/trajectory closure, Lean compilation, comparator acceptance, or
registry promotion.  `Finset` membership and the `577` accounting theorem
remain declared-artifact interfaces only.  Any future source/digest adapter
must preserve the canonical row encoding and independently supply the digest
and coverage evidence before admission can advance.

No state file, registry, receipt, or shared script was modified.
