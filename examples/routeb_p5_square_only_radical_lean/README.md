# T-P5-058 square-only radical cancellation Lean sidecar

Agent: **苏梦辰**

This portable sidecar formalizes the source-independent square-only lane from `review-T-P5-058-guyuefangyuan-20260908T0120.md` and its companion log. It does not perform source discovery, provenance/admission, Float64/libm reasoning, or P8 trajectory coverage.

## Kernel boundary

`P5SquareOnlyRadical.lean` exposes a deliberately narrow interface:

- `normalized_square_eq_ratio` removes the square root after squaring.
- `normalized_square_factor_cancel` cancels a strictly positive common factor from the radicand/numerator-square packet.
- `balanced_square_extension_no_parity` records that the balanced square consumer needs no parity/fixed-sign hypothesis.
- `common_factor_square_cancel` is the denominator-free source-packet version.
- `cancelled_square_pointwise_bound` and `balanced_square_pointwise_bound` are division-free pointwise energy bounds.
- `balanced_square_difference_identity`, `cancelled_square_difference_identity`, and `square_difference_abs_bound` expose the two-point algebra needed by exact rational variation consumers without hiding a source Lipschitz theorem.
- `cancelled_square_zero_at_factor_zero` records the over-cancelled root endpoint.
- the three `balanced_odd_*` regressions prove the semantic boundary: pointwise squares are constant in the exact `sign(t)` model while the centered signed jump remains `4`.
- `RadicalConsumerKind` / `squareOnlyAdmissible` keeps `PointwiseSquare` distinct from `CenteredSignedDifference` in the formal interface.

The sidecar intentionally leaves the actual factor identities `A=h^(2m)S`, `G=h^(m+k)J`, the same-key source binding, executable rewrite at `h=0`, and P5/P8 integration outside the kernel leaf.

## Verification

Run from the repository checkout with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 examples/routeb_p5_square_only_radical_lean/verify.sh
```

The verifier checks the sidecar `lean-toolchain` against `examples/local_fkg/lean-toolchain`, uses the pinned `examples/local_fkg/lake-manifest.json`, compiles with `-DwarningAsError=true`, checks `#print axioms` coverage for every exported theorem, and rejects `sorryAx`.

Passing focused compilation is only a **compiled_candidate**. It remains **待封不觉独立验证 / 待梁智炜最终整合**.
