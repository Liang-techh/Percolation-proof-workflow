# Comparator receipt admission review

## Scope and status

This sidecar follows the exact statement-boundary contract and defines only a
fail-closed receipt-admission interface.  It does not run the comparator and
does not assert comparator acceptance, `VERIFIED`, or registry promotion.

No Lean or Lake command was run.  This is an uncompiled typed contract, not a
kernel-verification receipt or an authoritative admission result.

## Contract supplied

- `ComparatorReceiptRecord` keeps the exact statement-target equivalence,
  checker exit code, exact standalone success output, artifact hash, and
  provenance as separate fields.
- `ComparatorReceiptComplete` requires every field: an explicit
  `ExactStatementBoundaryContract`, exit code `0`, exact output
  `Your solution is okay!`, and nonempty hash/provenance values.
- `ComparatorReceiptAdmissionContract` is constructible only from complete
  receipt evidence.  `MissingComparatorReceiptField` plus
  `missing_receipt_field_is_fail_closed` proves that absence of any one field
  leaves admission uninhabited rather than silently accepted.
- `ExplicitRegistryPromotionGate` is separate from receipt admission and
  requires an explicit authorization proof.  Receipt completeness does not
  populate or imply this gate.

## Remaining boundaries

Nonempty hash/provenance fields do not yet validate a specific digest
algorithm, artifact bytes, source binding, or provenance chain.  The sidecar
does not execute the comparator, verify its output, claim comparator
acceptance, mark the candidate `VERIFIED`, or promote the registry.  Missing
authoritative evidence remains pending/fail-closed.  No state, registry,
receipt, or shared script was modified.
