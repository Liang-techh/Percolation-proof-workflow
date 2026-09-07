# Pinned Lean kernel receipt fail-closed review

## Scope and status

This sidecar isolates the pinned-kernel receipt prerequisite for the promotion
workflow.  It does not run Lean/Lake and does not write `VERIFIED` or registry
status.

## Contract supplied

- `PinnedKernelReceiptAuditRecord` keeps project commit, toolchain identity,
  theorem identity, artifact digest, exit code, and zero-count audit fields
  (`sorry`, `admit`, and nonstandard axioms) independent and optionally
  present.
- `PinnedKernelReceiptComplete` requires exact expected project/toolchain/
  theorem/artifact identities, exit code `0`, and all three audit counts equal
  to zero.
- `PinnedKernelReceiptPending` represents missing receipt fields.  
  `PinnedKernelReceiptRejected` represents present-but-mismatched identities,
  digest, exit code, or nonzero audit counts.
- `pending_kernel_receipt_blocks_promotion` and
  `rejected_kernel_receipt_blocks_promotion` prove that either state prevents
  construction of the receipt promotion gate.

## Remaining boundaries

The sidecar does not establish that Lean/Lake actually ran, validate the
artifact digest algorithm or bytes, authenticate the pinned environment,
derive zero counts from an authoritative axiom report, or assert comparator
acceptance.  The receipt gate itself is not `VERIFIED` and does not promote a
registry entry.  No state, registry, receipt, or shared script was modified.
