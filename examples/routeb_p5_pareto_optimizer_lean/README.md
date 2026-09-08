# T-P5-039 exact Pareto optimizer Lean sidecar

Formalization-only sidecar for `review-T-P5-039-guyuefangyuan-20260907T1931`.

It proves the exact concave quadratic form of the T-P5-038 quarter-barrier gate,
endpoint/vertex maximization, the rational piecewise optimizer, an exact
necessary-and-sufficient existence test, a branchwise fail-fast obstruction,
source-facing `E5` thresholds, and the exact rational regression witness where
both endpoint certificates fail while the interior optimizer succeeds.

This sidecar is deliberately source-independent. It does **not** prove valid
same-domain `E4/E5` caps, deployed source identity, Float64/FD/controller/solve
semantics, ODE continuation, P8 coverage, P5/M4 closure, or registry admission.
The T-P5-038 first-exit consumer is not duplicated here.

`verify.sh` uses the repository's pinned `examples/local_fkg` Lake environment,
requires `lake` and `lean` on `PATH`, checks the exact Lean toolchain, runs with
`-DwarningAsError=true`, scans all exported theorem axiom reports, and rejects
`sorryAx`.

Status after a focused compile remains only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.
