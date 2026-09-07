# Verified registry entry invariant review

## Scope and status

This sidecar defines a constructor invariant only; it does not create a
registry entry or assert that any candidate is `VERIFIED`.  It remains
`OPEN_UNCOMPILED` and no Lean/Lake/comparator command was run.

## Contract supplied

- `ExplicitVerifiedEvidenceBundle` requires final admission, pinned kernel
  admission, comparator receipt, source/provenance identity, independent
  promotion authorization, zero-audit kernel evidence, and artifact/statement
  digest equalities.
- `VerifiedRegistryEntryInvariant` has only one evidence-bearing field, so an
  entry cannot be constructed from a compiled candidate or an
  `evidence_complete` flag alone.
- `RegistryAdmissionInput` separates `compiledOnly`, `pending`, `rejected`,
  and `explicit` inputs.  The admission function maps the first three to
  `none`; only the explicit evidence bundle maps to `some entry`.
- The three corresponding theorems give concrete pending/rejected/
  compiled-only counterexamples to automatic entry construction.

## Remaining boundaries

The sidecar does not mutate a registry, run a comparator, run Lean/Lake,
validate external provenance or digest computation, or establish a real
`VERIFIED` status.  The invariant is a typed admission boundary, not an
authoritative registry record.  No state, registry, receipt, or shared script
was modified.
