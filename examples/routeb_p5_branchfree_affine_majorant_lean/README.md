# T-P5 branch-free affine majorant Lean sidecar

Formalization owner: **苏梦辰**. Mathematical input: 柳冠一, `T-P5-BRANCHFREE-AFFINE-MAJORANT`.

This sidecar isolates the source-independent algebra behind the fixed positive budget `kappa` for the two-channel affine energy term

```text
Q(x,y) = p*x^2 + sigma*x*y + s*y^2,
d(x,y) = b4*x + b5*y.
```

The trusted forward interface is division-free. For `kappa > 0`, it consumes exactly the two correlated polynomial gates

```text
b4^2 + b5^2 <= 4*kappa*(p+s),
s*b4^2 - sigma*b4*b5 + p*b5^2 <= kappa*(4*p*s-sigma^2),
```

and proves `-Q(x,y)-d(x,y) <= kappa` for every real `x,y`. The proof is matrix-free: a scaled `2x2` trace/determinant quadratic lemma plus the exact completion identity from the mathematical review.

The sidecar also exposes a source-family adapter that keeps `p,s,sigma,b4,b5` on the same key/domain, a strict-reserve consumer, and the exact near-singular family `p=t^2,s=1,sigma=0,b4=2t,b5=0,kappa=1` where the joint determinant remainder remains zero even though independently intervalizing determinant and numerator can fail.

Not proved here: source/Float64 interval enclosure of the two remainders, true-DH/controller/FD/solve semantics, ODE/first-exit/flowpipe coverage, registry admission, or final P5/M4 closure. The mathematically optional converse (`global affine bound -> both gates`) is intentionally left outside this minimal forward consumer unless a downstream checker needs exact iff classification; T-P5-051 remains the sharp branch classifier.

Run with the repository-pinned local-FKG Lake environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_branchfree_affine_majorant_lean/verify.sh
```

A successful compile remains a `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.
