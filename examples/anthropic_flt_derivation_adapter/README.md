# D1 PointDerivations adapter handoff

This directory contains a metadata-only handoff for the highest-value
non-number-theoretic derivation candidate found in the Anthropic FLT snapshot.
It does not copy the upstream proof body and it is not a Lean receipt.

The target is the linear post-composition API around
`Algebra.PointDerivations.map`, `map_comp`, `map_id`, and `map_apply_coe`.
The handoff preserves the exact upstream commit and Git blob identity and keeps
the Route-B boundary explicit: a physical derivative, evaluation-Leibniz law,
continuity, residual semantics, and flowpipe obligations remain separate.

The JSON packet is pending until a Lean agent compiles it against a pinned
environment and returns declaration-level axioms plus a statement comparator
receipt. A successful adapter receipt would still not promote a Route-B theorem.

`D1_SOURCE_PROVENANCE_RECEIPT_20260908.json` records the local source-only
commit/blob/declaration check. It is deliberately not a Lean or kernel receipt.
