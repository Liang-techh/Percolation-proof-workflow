# T-P5-025 finite-orthant `K_path` Lean sidecar

Agent/source_agent: **苏梦辰**.

This sidecar formalizes only the source-independent mathematical seam from 柳冠一 `review-T-P5-025-liuguanyi-20260907T1020.md`, after 梁智炜's precise retarget to the finite-orthant / directional support-function checker.

## Formalized boundary

`Gain24` keeps the transported `2 x 4` component table in explicit generalized-force-channel/state-coordinate order. `component_envelope_power_bound` proves that channelwise bounds imply the direct support envelope `|Lz|^T K |z|` without first collapsing `K` to a Frobenius scalar. Boolean sign selectors then represent every concrete absolute-value orthant exactly. `OrthantSmallGainCertificate` is a finite `2^4 * 2^2 = 64` directional-quadratic checker contract, and `orthant_quadratic_small_gain` consumes it to prove the centered P5 power bound. `orthant_support_global_reversal` proves the simultaneous sign reversal symmetry, leaving at most 32 distinct forms for an exact rational checker.

The theorem deliberately does **not** claim that a concrete deployed `K_path` exists or satisfies the certificate. `Gain24.Nonnegative` is kept as an explicit source/checker interface rather than smuggled into the algebraic proof.

## Out of scope / still open

No global Lipschitz constant, controller rebuild, source/Jacobian/Float64 reification, cell/path connectivity, distal-coordinate repair, anchor-bias budget, ODE continuation, P8 flowpipe coverage, provenance/receipt/admission, registry mutation, or P5/M4 parent closure is proved here. The `K_path` table must already be in the actual generalized-force coordinates consumed by `ForceResidual45`; normalization may not be applied twice.

## Focused verification

The sidecar uses the repository-pinned Lean 4.32 / `examples/local_fkg/lake-manifest.json` environment. `verify.sh` finds `lake` and `lean` from `PATH`, rejects `sorry`/`admit`, compiles with `-DwarningAsError=true`, checks the exported `#print axioms` reports, and is registered for `.github/workflows/lean-agent-sidecars.yml` with `CI_PORTABLE=1`.

Run from the repository root after the pinned environment is available:

```bash
bash examples/routeb_p5_finite_orthant_kpath_lean/verify.sh
```

Status is only `compiled_candidate` after a real focused CI pass. Even then: **待封不觉独立验证 / 待梁智炜最终整合**.
