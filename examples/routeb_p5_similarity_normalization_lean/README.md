# T-P5-079 similarity normalization Lean sidecar

Agent/source_agent: **苏梦辰**.

This portable sidecar formalizes the first source-independent theorem decomposition requested by 柳冠一's `T-P5-079-SIMILARITY-NORMALIZATION` mathematics. It intentionally uses a 2×2 real symmetric metric and diagonal affine state scaling as the minimal kernel-checkable specialization. It does not bind a deployed normalization chart, source SCC/Jacobian, Float64/FD/controller/solve semantics, physical coverage, P8/ODE continuation, admission, registry mutation, or parent closure.

Kernel-facing leaves:

- `quadraticForm_congruence`: `W_z = Sᵀ W_x S` at quadratic-form level for diagonal `S`, with a general symmetric 2×2 weight including the cross entry.
- `bilinear_congruence`: bilinear companion used by the strong-monotonicity packet.
- `strongMonotone_similarity_iff`: exact pointwise transport of the same `mu` under covariant state/residual differences.
- `sqLipschitz_similarity_iff`: exact pointwise transport of the same `Lambda`.
- `corrector_step_similarity`: affine damped-corrector conjugacy with the same scalar step `h`.
- `jacobian_sym_congruence`: quadratic-form version of `A_z = Sᵀ A_x S`, consuming only the multiplication-only action intertwining `J_x S v = S J_z v`.
- `jacobian_gram_congruence`: quadratic-form version of `H_z = Sᵀ H_x S`, with the same source-facing intertwining.
- three exact rational regressions for the `J_x=[[1,1],[-1,1]]`, `S=diag(3,1)` example: freezing the metric at `I` gives `-4/3` in direction `(1,1)`, while the transported metric `diag(9,1)` preserves both the symmetric and Gram constants exactly at value `2`.

This sidecar deliberately does **not** claim the global domain-level `iff` for arbitrary invertible matrices. The current theorem set is the exact local 2×2 diagonal chart needed to expose the typed interfaces without importing Matrix inverse, differentiability, or set-image APIs into the first receipt. A later child may generalize the same algebra once a concrete source chart requires it.

Run from this directory or through `.github/workflows/lean-agent-sidecars.yml`:

```bash
CI_PORTABLE=1 bash verify.sh
```

`verify.sh` resolves `lake` and `lean` from `PATH`, reuses the repository's pinned `examples/local_fkg` Lake environment and manifest, requires the same `lean-toolchain`, scans for `sorry`/`admit`, compiles with warnings as errors, and checks all exported theorem axiom reports for `sorryAx`.

Passing this sidecar means only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.
