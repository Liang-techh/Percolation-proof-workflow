# Verification report

Status: `FOCUSED_COMPILE_PASS_PENDING_ADMISSION`

The focused Lean run now compiles in the pinned Lean/Mathlib environment. The
repair completed the exact rational `OperatorLowerBound` proof, corrected the
factorization rewrite directions and arithmetic normalization, and closed the
anonymous `noncomputable section` separately from the namespace. `verify.sh`
was also made robust to Lean's wrapped multi-line `#print axioms` output.

This is a focused compile receipt only. It is not a verified-registry entry and
does not close any physical Route-B admission obligation.

Target: `RouteBForceAccelNormalization.lean`

Claimed theorem boundary:

- exact real finite-dimensional vectors;
- explicit factorization `eF = M eA`;
- explicit positive operator lower bound;
- force-power-to-acceleration-budget conversion;
- exact rational `diag(1/5, 1/10)` sanity instance;
- negative result showing force-only budget is insufficient without the lower bound.

Not claimed:

- deployed Julia or Float64 binding;
- current P4 `l_F` equals an acceleration residual;
- frozen `M0_BB` equals `I_B`;
- D-row/Gram correspondence;
- continuous-time integral, domain coverage, flowpipe, terminal transfer, or
  physical DH admission.

The authoritative run record is appended by `verify.sh` in a fresh
`output/run-*` directory. Final focused receipt:

- run: `output/run-BbbmCQRa`
- exit code: `0`
- Lean: `4.33.1`
- Mathlib commit: `0df444a360eaa60ab8c11dca51a86af692955474`
- OLean SHA-256: `15ae2631b4c7aa012440701d58ba0234492f648061bea62f73ecc11f3f5bdd57`
- compile log SHA-256: `d6e88c20b6d369239ef7d3d1d637e2fc3b26aa19f0ad6fbd3888f3206fe609a2`
- axiom reports: exactly 3; only `propext`, `Classical.choice`, `Quot.sound`
- forbidden proof escapes: none

The receipt remains conditional exact-real Lean evidence. Registry promotion is
intentionally not performed.
