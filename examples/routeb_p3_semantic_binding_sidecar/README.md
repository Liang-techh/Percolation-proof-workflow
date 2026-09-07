# Route-B P3 semantic-binding sidecar

This directory is a minimal sidecar for `T-P3-006`.

Scope:

- provenance hashes are kept as provenance only;
- manifest/snapshot agreement is an explicit, separate premise;
- exact true-DH semantics are an explicit, separate premise;
- interval enclosure is an explicit, separate premise.

Non-goals:

- no claim that a SHA-256 match implies semantic equality;
- no claim that the theorem proves any real `Float64` equality;
- no modification of `StateStore`, registry data, or existing source files;
- no attempt to promote this sidecar into a full Route-B proof.

The Lean file is intentionally minimal. It only packages the four separated
premises into a single interface theorem so the boundary stays visible.

If Lean is unavailable in the current environment, the verify step records that
as a blocked compile rather than weakening the interface.
