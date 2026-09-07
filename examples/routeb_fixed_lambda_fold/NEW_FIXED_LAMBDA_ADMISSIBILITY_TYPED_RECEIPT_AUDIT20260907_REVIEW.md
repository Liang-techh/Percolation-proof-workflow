# Typed comparator receipt audit review

## Scope and status

This sidecar defines the smallest typed audit seam after the exact statement
boundary.  It distinguishes byte hash, source artifact, exact statement
digest, checker exit/output, pending, rejected, and admission.

No Lean or Lake command was run.  This is an uncompiled proof attempt, not a
comparator receipt, comparator-accepted result, `VERIFIED` claim, or registry
promotion.

## Contract supplied

- `ByteHash`, `SourceArtifact`, and `ExactStatementDigest` are distinct types;
  the source artifact carries separate provenance and byte-hash fields.
- `StatementTargetEvidence.equivalent` requires the existing exact statement
  boundary, while `missing` and `mismatch` remain distinguishable.
- `ReceiptAuditComplete` requires source artifact identity/provenance, source
  byte hash and receipt byte hash equal to the expected hash, exact statement
  digest equality, statement binding, checker exit `0`, and exact output
  `Your solution is okay!`.
- `ReceiptAuditPending` covers missing fields, including missing provenance or
  source byte hash.  `ReceiptAuditRejected` covers concrete mismatches in
  artifact identity/provenance/hash, statement digest/binding, exit code, or
  output.
- `pending_is_fail_closed` and `rejected_is_fail_closed` show that neither
  state can inhabit the admission contract.  The contract separately retains
  `complete`, `pending_absent`, and `rejected_absent` gates.

## Remaining boundaries

The sidecar does not compute or validate a specific hash algorithm, bind the
hash to artifact bytes, validate a provenance chain, run the checker, assert
comparator acceptance, mark the candidate `VERIFIED`, or promote a registry
entry.  Receipt completeness remains conditional typed evidence only; missing
authoritative fields are pending and mismatches are rejected.  No state,
registry, receipt, or shared script was modified.
