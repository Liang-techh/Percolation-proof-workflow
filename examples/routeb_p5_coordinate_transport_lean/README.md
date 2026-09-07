# Route-B P5 coordinate transport Lean sidecar

This portable sidecar formalizes the finite-sum part of `T-P5-022`, consuming
`agent_review_inbox/review-T-P5-022-liuguanyi-20260907T0820.md`.

It proves four interface layers:

1. component source-state / residual-increment / force-coordinate bounds compose
   into `K[a,k] = sum_i sum_j Aabs[a,i] H[i,j] S[j,k]`;
2. row-wise finite Cauchy converts those bounds to
   `sum_a rc[a]^2 <= ell2 * sum_k dz[k]^2`, with
   `ell2 = sum_a sum_k K[a,k]^2`;
3. raw anchor component boxes transported through a finite force map give the
   squared `B2` consumer;
4. exact arithmetic records the Route-B raw-PMI channel scales `1/5` and `1/10`
   and the extra `1/25` / `1/100` undercharge that would result from applying
   those normalizations a second time to an already-generalized residual.

The sidecar deliberately starts after the source/calculus step.  In particular,
`hJac` is a typed component increment bound; proving it from an exact-real
Jacobian interval by a segment/FTOC argument is separate.  A derivative theorem
for an exact-real formula is not silently reused for a lifted Float64 program.
Likewise, the sidecar does not source-bind the coordinate transport `S`, force
map `A`, Jacobian boxes `H`, nominal-anchor boxes, P8 flowpipe coverage, or ODE
continuation.

The algebraic theorem does not require entrywise `S >= 0` after the state
component inequality has already been established.  `transportedK_nonneg` is
kept separately as a checker-facing sanity lemma when `Aabs`, `H`, and `S` are
emitted as nonnegative tables.  This avoids carrying mathematically redundant
hypotheses into the main consumer.

Run from a checkout with the repository's pinned `examples/local_fkg` Lake
environment available:

```bash
bash examples/routeb_p5_coordinate_transport_lean/verify.sh
```

`verify.sh` is marked `CI_PORTABLE=1`, resolves `lake` and `lean` from `PATH`,
checks that the sidecar toolchain matches `examples/local_fkg/lean-toolchain`,
compiles with `-DwarningAsError=true`, requires an axiom report for every public
theorem, and rejects `sorryAx`.

A green compile is only a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.  It does not close P5/P8/M4 and does not enter the theorem registry by compilation alone.
