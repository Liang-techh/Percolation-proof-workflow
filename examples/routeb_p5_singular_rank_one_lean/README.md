# T-P5-048 singular rank-one Lyapunov boundary

This portable Lean sidecar formalizes only the source-independent algebra from 红莲魔尊's `T-P5-048` review.

It treats a symmetric 2x2 residual block

`H = [[p,q],[q,s]]`

at the singular rank-one boundary `p*s = q^2`, with `p > 0`.  The finite additive charge exists only when the linear bias is range-compatible, expressed without pseudoinverses as

`p*b5 = q*b4`.

The exported theorems cover:

- the exact rank-one square identity;
- the sharp charge `b4^2/(4*p)` under range compatibility;
- an explicit kernel witness and unboundedness when compatibility fails;
- the exact `V*=1/4` first-exit gate `200*b4^2 < (109-r)*p`;
- the parameter-tube gate `600*g4^2 < (109-r)*p`;
- the adjugate-numerator identity showing continuity with the positive-definite T-P5-044 formula;
- exact collapse of the unreduced determinant gate on the compatible singular boundary.

No theorem here binds `p,q,s,b4,b5,g4,g5` to deployed DH/Float64/controller/solve sources, proves ODE existence/continuation, establishes P8 coverage, changes any parent status, or enters the verified registry.

Run the focused checker from any environment whose `lake` and `lean` are on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_singular_rank_one_lean/verify.sh
```

The verifier reuses the repository-pinned `examples/local_fkg/lake-manifest.json` environment and checks the sidecar's `lean-toolchain` against it.
