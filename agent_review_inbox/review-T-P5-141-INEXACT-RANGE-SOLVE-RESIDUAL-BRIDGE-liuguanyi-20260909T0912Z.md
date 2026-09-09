---
kind: review_result
review_id: review-T-P5-141-inexact-range-solve-residual-bridge-liuguanyi-20260909T0912Z
task_id: T-P5-141-INEXACT-RANGE-SOLVE-RESIDUAL-BRIDGE
reviewer: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-09T09:12:00Z
claim_commit: cda1f465e1fc7efb3ad543e613a5ed55ffd2da77
inspected_commit: 6d4275c964d8f3481f87e8546d7bec8b020651c0
upstream_reviews:
  - path: agent_review_inbox/review-T-P5-137-ELLIPSOIDAL-KNOT-RESET-MULTIPLIER-honglianmozun-20260909T0811Z.md
    commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
  - path: agent_review_inbox/review-T-P5-139-RANGE-SOLVE-SCHUR-RESET-kuangmanmozun-20260909T0834Z.md
    commit: f0198916eb5fe1783cbeb9055031c9d9bd0dc954
  - path: agent_review_inbox/review-T-P5-140-MULTIPLIER-SECANT-OPTIMIZATION-honglianmozun-20260909T0908Z.md
    commit: 6d4275c964d8f3481f87e8546d7bec8b020651c0
status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: accept approximate shifted-curvature solves only through the signed residual identity b=K y+r and a residual dual-metric certificate sigma K-r r^T>=0; consume the corrected scalar floor before reusing T-P5-137, and use the corrected secant identity when comparing multipliers
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
commands: none; exact finite-dimensional quadratic-form algebra only
exit_code: n/a
---

# T-P5-141 — inexact range-solve residual bridge

## 0. Narrow seam

T-P5-139 reduces the fixed-multiplier reset LMI to an exact range solve

`K y = b`

plus one scalar floor gate. T-P5-140 then compares exact solves at different multipliers. Its fail-closed boundary explicitly states that an approximate solve cannot be substituted for an exact solve: solve residual terms enter the completion and the multiplier secant.

This child closes exactly that mathematical/interface seam. It does not redo the exact range-solve theorem or multiplier optimization. It answers:

> If a producer supplies an approximate vector `y` and a signed residual `r=b-Ky`, what exact additional packet is sufficient to recover the same augmented PSD/reset conclusion without pretending `r=0`?

The answer is a residual dual-metric certificate in the same shifted-curvature metric `K`.

No actual deployed source binding, Float64-to-real semantics, controller/FD/solve execution equivalence, P8 coverage, Lean/kernel receipt, provenance/admission audit, registry promotion, or parent closure is claimed.

---

## 1. Exact residual completion identity

Let `K` be symmetric, let `b,y,r,x` be finite-dimensional real vectors, and let `e,t` be real scalars. Define the signed solve residual by

**(1.1)** `r := b - K y`, equivalently `b = K y + r`.

Set

**(1.2)** `u := 2x - t y`.

Then the following identity is exact:

**Theorem A — residual completion**

**(1.3)**

`4 [ x^T K x - t b^T x + e t^2 ]`

` = u^T K u - 2 t r^T u`

`   + t^2 [ 4e - b^T y - r^T y ]`.

### Proof

Expanding the first term gives

`u^T K u`

` = 4 x^T K x - 4t y^T K x + t^2 y^T K y`

` = 4 x^T K x - 4t (b-r)^T x + t^2 y^T K y`.

Also

`-2t r^T u = -4t r^T x + 2t^2 r^T y`.

Therefore the cross terms in `r^T x` cancel, while

`y^T K y = y^T(b-r)=b^T y-r^T y`.

The remaining `t^2` coefficient is exactly `4e`. This proves (1.3).

This identity is the correct replacement for the T-P5-139 exact completion when a producer gives an inexact solve. The residual must remain signed until after the full expression is formed.

---

## 2. Division-free residual dual-cap theorem

Assume now that `K` is positive semidefinite. Let `sigma>=0` satisfy the exact matrix inequality

**(2.1)** `sigma K - r r^T >= 0`.

This is the natural dual-metric residual packet. It is strictly stronger and better typed than a coordinatewise or Euclidean residual norm when the consumer is the `K`-quadratic form.

### Lemma B1 — residual block is PSD

Under `K>=0`, `sigma>=0`, and (2.1), for every `u,t`,

**(2.2)** `u^T K u - 2t r^T u + sigma t^2 >= 0`.

One root-free proof is the rank-one Schur identity already used upstream: the block

`[[K,-r],[-r^T,sigma]]`

has rank-one condition `sigma K-r r^T>=0`. Equivalently, for `sigma>0`,

` sigma [u^T K u - 2t r^T u + sigma t^2]`

` = u^T(sigma K-r r^T)u + (r^T u-sigma t)^2 >=0`.

At `sigma=0`, (2.1) forces `r=0`, so the expression reduces to `u^T K u>=0`.

### Theorem B — inexact solve to augmented PSD

If

1. `K>=0`;
2. `r=b-Ky`;
3. `sigma>=0`;
4. `sigma K-r r^T>=0`;
5. the corrected scalar gate

**(2.3)** `4e - b^T y - r^T y - sigma >= 0`,

then for every `x,t`,

**(2.4)** `x^T K x - t b^T x + e t^2 >=0`.

Equivalently,

**(2.5)** `[[K,-b/2],[-b^T/2,e]] >=0`.

### Proof

Insert `sigma t^2-sigma t^2` into (1.3):

`4Q = [u^T K u-2t r^T u+sigma t^2]`

`     + t^2[4e-b^T y-r^T y-sigma]`.

The first bracket is nonnegative by Lemma B1 and the second by (2.3). Hence `Q>=0`.

No inverse, pseudoinverse, square root, eigenvalue, determinant, or floating-point residual heuristic appears in the theorem statement.

---

## 3. Direct ellipsoidal reset specialization

For the T-P5-137/139 packet define

`K_tau := H + tau G`,

`e := E - C - tau R`.

Suppose the producer supplies only an approximate candidate `y` and the exact signed residual identity

**(3.1)** `r = b - K_tau y`.

Then the following is sufficient:

**Theorem C — inexact range-solve ellipsoidal reset gate**

Assume

- `tau>=0`;
- `K_tau>=0`;
- `sigma>=0`;
- `sigma K_tau-r r^T>=0`;
- and

**(3.2)**

`4(E-C-tau R) >= b^T y + r^T y + sigma`.

Then the T-P5-137 multiplier block is PSD, hence for every physical state satisfying

`x^T G x<=R`,

**(3.3)** `W_+(x) <= kappa W_-(x) + E`.

For a downstream knot headroom `J`, replace `E` by `J`:

**(3.4)**

`4(J-C-tau R) >= b^T y + r^T y + sigma`.

This is the smallest useful interface change: an approximate solve does not invalidate the reset architecture, but it must carry a same-metric residual certificate and pay the corresponding scalar correction.

---

## 4. Exact correction solve and sharp meaning of `sigma`

The preceding theorem is only a sufficient statement for a supplied `sigma`. In finite dimensions the residual cap has a sharper interpretation.

Assume `K>=0` is symmetric and there exists `z` with

**(4.1)** `K z = r`.

Then

`y_* := y+z`

is an exact solve because

`K y_* = K y+r = b`.

The exact T-P5-139 scalar is

`q_K(b)=b^T y_*`.

A direct expansion gives the correction identity

**Theorem D — exact dual-energy update**

**(4.2)**

`q_K(b) = b^T y + r^T y + r^T z`.

Indeed,

`b^T z = (K y+r)^T z = y^T K z+r^T z = r^T y+r^T z`.

Also

**(4.3)** `r^T z = z^T K z >=0`.

Thus the approximate scalar `b^T y` is not the correct floor. The missing correction consists of the signed cross term `r^T y` plus the residual energy `r^T z`.

### Intrinsic residual energy

If `K z=r` and `K z'=r`, then `r^T z=r^T z'` by the same nullspace argument as T-P5-139. Define

**(4.4)** `q_K(r):=r^T z`.

Then the sharp correction is

**(4.5)** `q_K(b)=b^T y+r^T y+q_K(r)`.

Moreover

**(4.6)** `q_K(r) K-r r^T>=0`.

This follows from semidefinite Cauchy:

`(r^T x)^2=(z^T K x)^2 <= (z^T K z)(x^T K x)`.

Conversely, any supplied `sigma` satisfying (2.1) obeys

**(4.7)** `q_K(r)<=sigma`.

To see this, evaluate (2.1) at `z`:

`0 <= sigma z^T K z-(r^T z)^2`

`   = q_K(r)(sigma-q_K(r))`.

Since `q_K(r)>=0`, the inequality gives (4.7).

Therefore Theorem C is exactly the sharp T-P5-139 floor when `sigma=q_K(r)`, and is conservative by precisely `sigma-q_K(r)` otherwise.

---

## 5. The residual cap also certifies singular range compatibility

There is a useful interface consequence that is easy to miss.

Suppose `K>=0` is symmetric and finite-dimensional and (2.1) holds. For every `v in ker K`,

`0 <= v^T(sigma K-r r^T)v = -(r^T v)^2`.

Hence

**(5.1)** `r^T v=0` for every `v in ker K`.

Thus

**(5.2)** `r in (ker K)^perp = range(K)`.

So the residual dual-cap is not merely a size bound. At a singular multiplier it also proves that the inexact residual has no forbidden nullspace component and therefore can be corrected by some exact `z`.

This recovers the T-P5-139 singular obstruction fail-closed:

> if the residual has any nonzero component along `ker K`, no finite `sigma` can satisfy `sigma K-r r^T>=0`, and the approximate solve cannot be repaired into an exact range solve at that multiplier.

---

## 6. Exact residual-corrected multiplier secant

T-P5-140 compares two exact range solves. For approximate solves the exact signed correction is as follows.

Let

`K_i := H + tau_i G`,

`r_i := b-K_i y_i`,

and let

`d := tau_2-tau_1`.

Then, with no PSD or smallness assumption,

**Theorem E — inexact two-multiplier secant identity**

**(6.1)**

`b^T y_1-b^T y_2`

` = d y_1^T G y_2 + r_2^T y_1-r_1^T y_2`.

### Proof

Using `b=K_2 y_2+r_2` and `K_2=K_1+dG`,

`b^T y_1`

` = y_1^T K_2 y_2+r_2^T y_1`

` = y_1^T K_1 y_2+d y_1^T G y_2+r_2^T y_1`

` = (b-r_1)^T y_2+d y_1^T G y_2+r_2^T y_1`,

which is (6.1).

Therefore a producer must not reuse the T-P5-140 exact secant

`q_1-q_2=d c_12`

with approximate solves. The omitted signed correction is exactly

**(6.2)** `r_2^T y_1-r_1^T y_2`.

Only after forming this signed quantity should an enclosure be taken. Separate absolute-value bounds can destroy cancellation and can also give the wrong sign for whether the multiplier floor improves.

### Conservative corrected floors

If each candidate carries a residual cap `sigma_i` and one defines the certified scalar floor

**(6.3)**

`4(Ehat_i-C-tau_i R)`

` := b^T y_i+r_i^T y_i+sigma_i`,

then pure algebra gives

**(6.4)**

`4(Ehat_2-Ehat_1)`

` = d(4R-y_1^T G y_2)`

`   + (r_1+r_2)^T (y_2-y_1)`

`   + (sigma_2-sigma_1)`.

This is an identity for the chosen conservative floors. It does **not** imply sharp multiplier optimality unless the `sigma_i` are the intrinsic residual energies or exact correction solves are supplied. It is nevertheless the correct source/checker comparison formula for two approximate producer solves.

If exact correction solves `K_i z_i=r_i` are available, use `y_i^*=y_i+z_i`; then T-P5-140 applies unchanged to `y_i^*`, with cross metric

`(y_1+z_1)^T G (y_2+z_2)`.

---

## 7. Two exact rational regressions

### 7.1 Naively dropping the residual undercertifies the floor

Take one dimension:

`K=1`, `b=1`, `y=0`.

Then

`r=1`.

A false use of the exact-solve T-P5-139 gate would read `b*y=0` and could accept `e=0`.
But the augmented matrix

`[[1,-1/2],[-1/2,0]]`

is indefinite.

The present packet gives the sharp residual cap

`sigma=1`, because `sigma K-r^2=0`.

The corrected gate is

`4e >= b*y+r*y+sigma = 1`,

so `e>=1/4`, exactly the true Schur floor.

### 7.2 Singular nullspace residual is a hard obstruction

Take

`K=diag(0,1)`, `b=(1,0)`, `y=(0,0)`.

Then

`r=(1,0)`.

For every finite `sigma`,

`sigma K-r r^T = diag(-1,sigma)`,

which is not PSD. Hence no residual packet exists and no correction solve `Kz=r` exists. This correctly reproduces the fixed-multiplier range obstruction rather than hiding it behind a small Euclidean residual claim.

---

## 8. Optional metric-transport corollary

A source may already bound the residual in another PSD metric `S`. The safe adapter is itself a matrix-order bridge.

If

**(8.1)** `sigma S-r r^T>=0`,

and

**(8.2)** `lambda K-S>=0` with `lambda>=0`,

then

**(8.3)** `(sigma lambda) K-r r^T>=0`.

Indeed,

`(sigma lambda)K-r r^T`

` = sigma(lambda K-S)+(sigma S-r r^T)>=0`.

Thus a foreign residual metric can be consumed only after a same-key PSD comparison to `K`. Euclidean `||r||` or another Schur metric must not be silently treated as a `K`-dual cap.

---

## 9. Minimal theorem/interface packet

For an approximate fixed-multiplier producer the minimal source-to-math packet is now:

1. same reset/cell/reference key for `G,H,b,C,R,tau`;
2. exact definition `K=H+tau G` and PSD witness `K>=0`;
3. approximate candidate vector `y`;
4. **signed** residual identity `r=b-Ky`;
5. rational `sigma>=0`;
6. exact PSD witness `sigma K-r r^T>=0`;
7. scalar floor/headroom gate
   `4(E-C-tau R)>=b^T y+r^T y+sigma`;
8. only if multipliers are compared, retain the signed cross-residual terms from (6.1) or use exact correction solves before invoking T-P5-140.

This is preferable to a generic solver tolerance field. A scalar tolerance without its metric, sign convention, and same-source identity cannot justify the reset LMI.

---

## 10. Suggested Lean split

A future source-independent sidecar can be small:

- `inexact_rangeSolve_completion_identity` — theorem (1.3), ring algebra;
- `residual_dualCap_block_nonnegative` — `K>=0`, `sigma>=0`, `sigma K-r r^T>=0` imply (2.2);
- `inexact_rangeSolve_augmented_psd` — Theorem B;
- `inexact_rangeSolve_ellipsoid_reset` — Theorem C composed with T-P5-137;
- `residual_exact_correction_identity` — Theorem D under `Kz=r`;
- `residual_dualCap_range_compatible` — finite-dimensional nullspace/range bridge;
- `inexact_rangeSolve_secant` — Theorem E;
- `residual_metric_transport` — Section 8.

The trusted statements need only real/rational arithmetic, symmetry, PSD quadratic forms, and finite-dimensional range/ker orthogonality for the optional existence theorem. No matrix inverse API is required.

---

## 11. Fail-closed boundaries

1. `r` must be the signed residual of the same `K,b,y`; a solver's reported norm alone is not the identity `r=b-Ky`.
2. A Float64 residual vector is not automatically an exact-real residual. Parser, operation, rounding, and coefficient/source semantics remain separate.
3. `sigma K-r r^T>=0` is metric-specific. A residual bound in Euclidean or another physical metric needs the explicit transport of Section 8.
4. The cross term `r^T y` is signed. Replacing it automatically by `|r| |y|` is safe only after proving a chosen norm bridge and generally loses cancellation.
5. At singular `K`, a residual nullspace component is fatal for this fixed multiplier; no finite `sigma` repairs it.
6. A conservative `sigma` certifies a conservative floor. T-P5-140 global multiplier optimality applies only to exact solves or to exact correction solves, not to arbitrary conservative `Ehat_i`.
7. This theorem does not prove the actual producer's `y/r/sigma`, same-cell coverage, controller/reference identity, FD/DH semantics, P8 flowpipe, Lean/kernel receipt, independent verification, admission, registry eligibility, or P5/M4 closure.

---

## 12. Result

The approximate-solve boundary left explicit by T-P5-140 is mathematically closed at the interface level:

**`r=b-Ky`, `sigma K-r r^T>=0`, and `4e>=b^T y+r^T y+sigma` are sufficient to recover the exact augmented PSD/reset conclusion.**

The residual cap additionally certifies range compatibility at singular `K`; its sharp value is the residual `K`-energy `q_K(r)`, and with that sharp value the corrected floor is exactly the T-P5-139 floor. For multiplier comparisons, the exact residual-corrected secant is (6.1), so solve residuals can no longer be silently dropped from T-P5-140.

Current status remains `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending`.