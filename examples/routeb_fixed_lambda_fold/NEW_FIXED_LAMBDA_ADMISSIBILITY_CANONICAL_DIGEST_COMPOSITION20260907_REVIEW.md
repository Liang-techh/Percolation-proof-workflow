# Canonical digest composition seam review

## Scope and status

This sidecar adds only the canonical-row encoding and union-digest binding
seam.  It reuses the existing `ExactWitnessDigest`, partition digest fields,
and `selectedRowEncoding`; it does not repeat union cardinality or selected-
box margin lemmas.

No Lean or Lake command was run.  The file is an uncompiled typed interface,
not a kernel-verification receipt, comparator result, or registry admission.

## Contract supplied

- `CanonicalDigestComposition` carries canonical encodings for eta=2.7,
  eta=5.6, and their explicit concatenation, together with the two existing
  partition digest tokens and an externally supplied union digest/oracle.
- `eta27_digest_binding` and `eta56_digest_binding` connect the two tokens to
  their selected-row encodings using the partition's existing binding fields.
- `union_digest_binding_of_consistent_encoding` rewrites the supplied union
  oracle result to the concatenation of the two selected-row encodings.
- `compose_union_digest_binding` packages that result into a reusable typed
  `UnionDigestBinding`.

The interface intentionally does not pretend that
`SHA256(payload27 ++ payload56)` is computable from
`SHA256(payload27)` and `SHA256(payload56)`.  The union token/oracle result is
an external premise, as is the equality between the externally canonicalized
payloads and the selected-row encodings.

## Remaining boundaries

No SHA-256 implementation, hex validation beyond the existing token shape,
CSV/source binding, row-value reconstruction, or receipt verification is
performed here.  The encoding equalities and union oracle equality must be
independently supplied by a future adapter.

This sidecar does not prove sparse-label coverage, one-row-per-box, 577-row
accounting, true-DH interval coverage, residual/PDE/trajectory closure,
formal certificate validity, comparator acceptance, or registry eligibility.
No state, registry, receipt, or shared script was modified.
