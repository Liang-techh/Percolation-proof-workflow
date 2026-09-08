# T-P5-054 correlated matrix perturbation Lean sidecar

Agent: **苏梦辰**  
Mathematical source: 柳冠一, `review-T-P5-054-correlated-matrix-perturbation-liuguanyi-20260908T0013.md`.

This isolated sidecar formalizes the source-independent 2x2 perturbation layer between nominal exact/Bernstein packets and the existing branch-free affine-energy mathematics.  It deliberately represents a symmetric 2x2 packet by three real scalars instead of using matrix inverse/eigenvalue APIs.

The Lean file proves:

- exact branch-free packet trace and determinant identities, including `det(G)=4*kappa*Rdet`;
- exact correlated determinant update `det2_add_exact`;
- a sound independent-entry-radius determinant/trace fallback;
- exact source-variable to matrix-error entry identities and rational absolute-error radii;
- a matrix-free trace/determinant PSD consumer and affine-energy consumer;
- preferred nominal-reserve + correlated-correction composition and fallback nominal-reserve + entry-radius composition;
- the rank-one regression `G(t)=[[1,t],[t,t^2]]`, where the correlated determinant correction is exactly zero but independent radii charge `2*eps^2`.

The direct correlated `Cdet`/full-`Rdet` lane is therefore part of the theorem interface and must not be silently replaced by independently intervalized determinant factors near singularity.

## Focused verification

```bash
bash examples/routeb_p5_correlated_matrix_perturbation_lean/verify.sh
```

`verify.sh` obtains `lake` and `lean` from `PATH`, checks the sidecar toolchain against the repository-pinned `examples/local_fkg/lean-toolchain` and `lake-manifest.json`, runs Lean with `-DwarningAsError=true`, requires a `#print axioms` report for every exported theorem, and rejects `sorryAx`.

The file is marked `CI_PORTABLE=1`, so `.github/workflows/lean-agent-sidecars.yml` executes it in the pinned Lean 4.32 / local-FKG environment.

## Explicit non-claims

This sidecar does **not** prove a concrete deployed nominal/error split, trigonometric/Taylor/rational enclosure, Float64 or outward-rounding semantics, same-domain physical cell coverage, authoritative `kappa`, ODE continuation/flowpipe coverage, P5/M4 closure, or registry/admission status.

A successful compile is only a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**。
