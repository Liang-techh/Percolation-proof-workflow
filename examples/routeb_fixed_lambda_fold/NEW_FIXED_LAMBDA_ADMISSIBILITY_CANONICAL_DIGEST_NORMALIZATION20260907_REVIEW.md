# Canonical statement digest and normalization review

## Scope and status

This sidecar follows the typed receipt audit and isolates canonical statement
identity.  It distinguishes byte hash, source artifact, exact statement
digest, structured binder/quantifier/order/normalization equality, and ordinary
text similarity.

The file is intentionally `OPEN_UNCOMPILED`: no Lean/Lake command or
comparator was run, and no registry status is asserted.

## Contract supplied

- `CanonicalStatementForm` makes binder, quantifier order, term order,
  normalization, and body separate fields.  `CanonicalStatementEquivalent`
  requires equality of every field.
- `OrdinaryTextSimilar` only compares body text.  The supplied candidate and
  target have identical body text but opposite term-order metadata, and
  `approximate_text_does_not_imply_canonical_equivalence` proves that this
  near-text pair is not canonically equivalent.
- `CanonicalDigestReceiptAdmissionContract` keeps the byte hash bound to the
  source artifact and receipt hash, while separately requiring the exact
  statement digest to equal the target digest produced by the explicit
  `CanonicalDigestOracle`.
- `pending_cannot_admit_canonical_receipt` and
  `rejected_cannot_admit_canonical_receipt` keep missing fields and concrete
  mismatches fail-closed.  `near_text_counterexample_is_rejected` records the
  non-equivalent near-text case as rejected.

## Remaining boundaries

The oracle does not implement a cryptographic digest algorithm, prove byte
hash computation from artifact contents, validate provenance, run the checker,
or establish comparator acceptance.  Receipt completeness is not upgraded to
`VERIFIED` or registry promotion; exact canonical binding remains required.
No state, registry, receipt, or shared script was modified.
