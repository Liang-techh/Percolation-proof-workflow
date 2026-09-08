# T-P5-056 radical eta-Lipschitz Lean sidecar

Formalization owner: **苏梦辰**.

Mathematical input: `agent_review_inbox/review-T-P5-056-honglianmozun-20260908T0100.md` by 红莲魔尊.

This sidecar isolates the source-independent polynomial core of the review's radical-free squared certificate. Instead of binding `Real.sqrt` directly to deployed source code, it exposes a small root packet:

- nonnegative root values `r,s` with exact square identities `r^2=A`, `s^2=B`;
- an exact rational lower squared margin `m <= r^2,s^2`;
- an exact reciprocal-difference relation `r*s*h=s-r`;
- numerator/root and bias decomposition relations;
- exact squared two-point variation/amplitude bounds.

From these premises it proves:

1. `root_product_margin`;
2. `sqrt_two_point_sq_from_roots`;
3. `inverse_root_charge_from_relation`;
4. `numerator_over_root_charge`;
5. `bias_inverse_root_charge`;
6. exact denominator-free weighted Young identity/bound;
7. `normalized_radical_sq_from_atomic_charges`;
8. end-to-end `normalized_radical_sq_from_root_packet`.

The final consumer is exactly the checker-friendly shape

`4*theta*m^3*|Delta u|^2 <= (1+theta)*(4*theta*m^2*DG^2 + MG^2*DA^2)*|Delta eta|^2`,

represented over `ℝ` with squares rather than absolute-value squares.

## Boundary

This sidecar does **not** prove that the deployed source evaluator supplies the root packet, radicand positive margin, derivative/two-point constants, or amplitude constants. It does not prove MVT/FTC, Float64/libm semantics, source-parser equivalence, physical coverage, P8 ODE continuation, admission, or registry status. T-P5-057 factor cancellation is separately owned by 柳冠一 and is not duplicated here.

A focused compile/axiom PASS is only a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.

## Verification

Run from the repository checkout with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 examples/routeb_p5_radical_eta_lipschitz_lean/verify.sh
```

The verifier uses the repository-local pinned `examples/local_fkg/lake-manifest.json` and checks the Lean 4.32 toolchain before compiling with `-DwarningAsError=true` and auditing all exported theorem axiom reports for `sorryAx`.
