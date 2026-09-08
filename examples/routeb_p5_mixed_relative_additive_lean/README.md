# T-P5-040 mixed relative-plus-additive Lean sidecar

Owner: 苏梦辰.  Upstream mathematics: 红莲魔尊 `review-T-P5-040-honglianmozun-20260907T1950.md` at commit `06ef9ccc4aa6055a6a3bd7d6f0a5bb9055220f47`.

This sidecar formalizes only the source-independent algebra needed by the T-P5-040 consumer:

- componentwise `|l| <= rho*|u| + b` to residual-power transport;
- the sharp one-channel completion `-t*u^2+b*|u| <= b^2/(4t)` and its division-free form;
- exact reserve numerators `A4,A5` and positive-reserve equivalences;
- the two-channel Pareto mixed residual decay theorem;
- the exact division-free quarter-barrier checker gate and strict first-exit conclusion;
- exact reduction to the T-P5-039 zero-relative additive gate;
- the division-free incremental `dc^2` tube-gate cross inequality.

It does **not** prove that deployed `forceError`, finite differences, controller, matrix solve, or true-DH residuals satisfy the component contracts.  It does not establish Float64-to-real reification, ODE existence/continuation, P8 flowpipe/domain coverage, source provenance/admission, or P5/M4 closure.

The verifier uses `lake`/`lean` from `PATH` and the repository's pinned `examples/local_fkg` Lake environment (`lean-toolchain` plus `lake-manifest.json`).  `CI_PORTABLE=1` registers it with `.github/workflows/lean-agent-sidecars.yml`.

Status after a successful focused compile is only `compiled_candidate`: 待封不觉独立验证 / 待梁智炜最终整合。
