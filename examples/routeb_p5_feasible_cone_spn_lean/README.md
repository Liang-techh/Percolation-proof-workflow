# T-P5-026 feasible-cone SPN Lean sidecar

This sidecar formalizes the source-independent mathematics in
`agent_review_inbox/review-T-P5-026-guyuefangyuan-20260907T1031.md`.

It proves:

- an explicit six-cone cover for one `(x,y,x+y)` sign geometry;
- the two-channel product cover;
- finite-sum entrywise-nonnegative quadratic nonnegativity;
- the checker-facing `H = S + N` SPN orthant consumer;
- global-sign invariance of the quadratic/direct-absolute envelope;
- the exact abstract equivalence between a global inequality and all inequalities on a nonnegative-coordinate cone cover;
- the component residual-power triangle bound;
- a generic feasible-cone SPN small-gain theorem.

The concrete 18 representative cone records, rational `K_path`, rational `LDL^T`
PSD witnesses, Julia/Float64 source semantics, P8 coverage, ODE continuation, and
P5/P8/M4 admission remain outside this sidecar.

`verify.sh` is CI-portable and deliberately reuses the repository-pinned
`examples/local_fkg/lake-manifest.json` / Lean environment.  It discovers
`lake` from `PATH` and rejects toolchain drift.

Current formal status after a successful focused check is only
`compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
