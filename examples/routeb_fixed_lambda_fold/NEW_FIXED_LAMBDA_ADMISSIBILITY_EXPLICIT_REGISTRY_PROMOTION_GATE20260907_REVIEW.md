# Explicit registry promotion gate review

## Scope and status

This sidecar is the boundary after final admission.  It keeps final admission,
pinned Lean kernel receipt, comparator receipt, source/provenance identity, and
independent promotion authorization as separate evidence objects.

It is `OPEN_UNCOMPILED`: no Lean/Lake command or comparator was run.  The
contract does not construct `VERIFIED` or perform registry promotion.

## Contract supplied

- `PinnedLeanKernelReceipt` requires a nonempty pinned Lean/Lake/theorem
  identity, receipt digest, and exit code `0`.
- `ComparatorReceiptReference` separately requires a nonempty receipt id,
  expected artifact hash and statement digest, exit code `0`, and the exact
  standalone output `Your solution is okay!`.
- `ProvenanceSourceIdentity` separately binds source root, artifact id,
  provenance id, and expected byte hash.
- `IndependentPromotionAuthorization` is an independent explicit decision;
  it is not inferred from final admission or either receipt.
- `RegistryPromotionPending` records missing components.  
  `RegistryPromotionRejected` records present-but-invalid kernel receipt,
  comparator receipt, source identity, or authorization.  The two impossibility
  theorems prove that either state blocks construction of the promotion
  contract.

## Remaining boundaries

The sidecar does not run Lean, validate a real kernel receipt, execute the
comparator, verify artifact bytes or provenance externally, mark the candidate
`VERIFIED`, or mutate a registry.  All five evidence classes and the explicit
authorization remain required and independently auditable.  No state,
registry, receipt, or shared script was modified.
