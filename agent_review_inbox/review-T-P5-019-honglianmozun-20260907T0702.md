---
kind: review_result
review_id: review-T-P5-019-honglianmozun-20260907T0702
task_id: T-P5-019
source_agent: 红莲魔尊
agent: 红莲魔尊
claimed_at: 2026-09-07T06:49:00-06:00
created_at: 2026-09-07T07:02:00-06:00
inspected_commit: 59c5a6803fd56f1c7e3ec20db9382a68b245cc7f
continuation_of:
  - review-T-P5-017-honglianmozun-20260907T0558
  - review-T-P5-018-guyuefangyuan-20260907T0634
related_reviews:
  - review-T-P5-016-guyuefangyuan-20260907T0538
  - review-T-P5-009-liuguanyi-20260907T0606
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_block45_residual_metric_17_over_5_and_replace_the_coarse_euclidean_Young_consumer_where_applicable
---

# T-P5-019 — a direct residual-coupling metric for the block-(4,5) hypocoercive energy

## 0. Result in one sentence

For the exact-rational block-(4,5) hypocoercive derivative used in `T-P5-016/018`, the residual couples through `x+y`; instead of bounding `||x+y||^2 <= 2N` and separately lower-bounding the dissipation, one can prove the **direct metric inequality**

```text
5 ||x+y||^2 <= 17 Q(x,y),
```

where `Q` is the full positive dissipation quadratic including the small skew coupling.  This improves the residual consumer from

```text
V' <= -(457/1344)V + (800/457)||l||^2
```

to

```text
V' <= -(457/1344)V + (17/10)||l||^2,
```

so the exact ultimate gain drops below `5`, and the quarter-barrier residual target sharpens to

```text
45696 L2 < 2285.
```

No source binding, Float64 theorem, P8 domain coverage, provenance, admission, or P5/M4 closure is claimed.

## 1. Exact quadratic appearing in the energy derivative

Use the same exactized constants as `T-P5-016/018`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),

K = [[3/4,   -3/400],
     [-3/400, 29/50]],

A = [[0,1/400],
     [-1/400,0]].
```

For the relative/incremental equation

```text
x' = y,
M y' + D y + K x = A x - l,
```

the `eps=1` hypocoercive storage satisfies the exact identity

```text
V'
 = - y^T(D-M)y
   - x^T K x
   + y^T A x
   - (x+y)^T l.
```

Define

```text
Q(x,y)
 := y^T(D-M)y + x^T K x - y^T A x.
```

Then simply

```text
V' = -Q(x,y) - (x+y)^T l.                     (1)
```

Previous reviews used the two separate estimates

```text
Q >= (457/800) (||x||^2+||y||^2),
||x+y||^2 <= 2 (||x||^2+||y||^2).
```

Their composition gives the effective coupling constant `1600/457 > 3.5`.  The purpose of this child is to compare `x+y` to `Q` directly.

## 2. Elementary diagonal lower bound for Q

Write coordinates `(x4,x5,y4,y5)`.  Expanding gives

```text
Q
 = (3/4)x4^2 + (29/50)x5^2 - (3/200)x4*x5
   + (2049997/3000000)y4^2
   + (2399261/4000000)y5^2
   + (1/400)x4*y5 - (1/400)x5*y4.             (2)
```

Use weighted Young bounds chosen to spend the large axis-4 slack in order to protect the tighter axis-5 coefficients:

```text
|x4*x5| <= 2*x4^2 + (1/8)*x5^2,
|x4*y5| <= 2*x4^2 + (1/8)*y5^2,
|x5*y4| <= (1/8)*x5^2 + 2*y4^2.               (3)
```

These are just the division-free squares

```text
(2*x4 - x5/2)^2 >= 0,
(2*x4 - y5/2)^2 >= 0,
(x5/2 - 2*y4)^2 >= 0,
```

with the obvious sign variants for absolute values.

Substituting (3) into (2) yields

```text
Q >= a4*x4^2 + a5*x5^2 + b4*y4^2 + b5*y5^2,   (4)
```

with exact rational coefficients

```text
a4 = 143/200,
a5 = 1849/3200,
b4 = 2034997/3000000,
b5 = 2398011/4000000.                           (5)
```

All four are strictly positive.

## 3. Direct comparison with x+y, with no matrix inverse

For positive scalars `a,b`, the exact identity

```text
(a+b)(a*x^2+b*y^2) - a*b*(x+y)^2
 = (a*x-b*y)^2 >= 0                              (6)
```

shows that a sufficient condition for

```text
5*(x+y)^2 <= 17*(a*x^2+b*y^2)                  (7)
```

is simply

```text
5*(a+b) <= 17*a*b.                              (8)
```

For the two pairs in (5), the exact positive gaps are

```text
17*a4*b4 - 5*(a4+b4)
 = 255693569/200000000 > 0,

17*a5*b5 - 5*(a5+b5)
 = 28503763/12800000000 > 0.                    (9)
```

Therefore (7) holds separately for coordinates 4 and 5.  Summing and using (4) gives the desired direct metric lemma:

```text
5 * ((x4+y4)^2 + (x5+y5)^2)
 <= 17 * Q(x,y).                                  (10)
```

Equivalently,

```text
||x+y||^2 <= (17/5) Q(x,y).                       (11)
```

This proof is intentionally elementary: no eigenvalues, square roots, matrix inverse, or floating computation enter the trusted statement.

### Near-sharpness note

The choice `17/5` is not merely cosmetic.  The tight axis-5 scalar check in (9) has only the exact positive gap

```text
28503763/12800000000.
```

So the simple weighted-Young proof is already close to saturation.  One can obtain a slightly smaller constant by inverting the full `4x4` quadratic form, but that creates very large rational coefficients for little practical gain.  `17/5` is the recommended source/Lean interface.

## 4. Improved residual-power absorption

By Cauchy and (11),

```text
|(x+y)^T l|
 <= sqrt(Q) * sqrt((17/5)||l||^2).
```

The square completion

```text
0 <= (sqrt(Q) - sqrt(17/5)*||l||)^2
```

is equivalent to the no-loss Young choice

```text
|(x+y)^T l|
 <= (1/2)Q + (17/10)||l||^2.                    (12)
```

For formalization one does not need to introduce square roots: combine Cauchy in squared form with the generic implication

```text
z^2 <= (17/5) Q R2, Q>=0, R2>=0
=> |z| <= (1/2)Q + (17/10)R2,
```

or prove the corresponding square inequality directly.

Substituting (12) into (1) gives

```text
V' <= -(1/2) Q + (17/10)||l||^2.                 (13)
```

`T-P5-018` already supplies

```text
Q >= (457/800)N,
V <= (21/25)N,
N := ||x||^2+||y||^2.
```

Hence

```text
Q >= (457/672)V,                                  (14)
```

and therefore

```text
V' <= -(457/1344)V + (17/10)||l||^2.              (15)
```

The decay coefficient is unchanged from the improved `T-P5-018` consumer; only the residual price is reduced.

## 5. Exact ISS gain and invariant barriers

Assume on the same covered domain

```text
||l||^2 <= L2.                                      (16)
```

The scalar comparison from (15) has asymptotic gain

```text
(17/10)/(457/1344)
 = 11424/2285
 < 5,                                                (17)
```

where the last inequality is the one-integer check

```text
11424 < 11425.
```

Thus, conditionally on the differential inequality remaining valid,

```text
V(t)
 <= exp(-(457/1344)t) V(0)
  + (11424/2285)L2 * (1-exp(-(457/1344)t)).          (18)
```

For a first-exit proof, no exponential is required.  On `V=Vstar`, strict inward drift follows from the division-free condition

```text
2285 Vstar > 11424 L2.                              (19)
```

### Quarter barrier for the affine moving frame

`T-P5-017` proves that for the standard ramp initialization and `c^2<=3`, the affine moving-frame energy satisfies

```text
V_rel(0) < 1/4.
```

Taking `Vstar=1/4` in (19) gives the new residual-only target

```text
45696 L2 < 2285.                                    (20)
```

This is strictly better than the published `T-P5-017` sufficient target

```text
5120000 L2 < 208849,
```

because the latter used the older `V<=N` plus the coarser residual coupling.  The new threshold is approximately `0.0500044` only for intuition; (20) is the checker-facing statement.

### Zero-initial incremental tube / common physical margin

For the `T-P5-018` incremental tube, the component reconstruction already gives the common-margin choice

```text
Vstar = (117/4880) s^2.
```

Substitution into (19) yields

```text
267345 s^2 > 55749120 L2,
```

or after cancelling `15`,

```text
17823 s^2 > 3716608 L2.                              (21)
```

This replaces the older one-margin condition

```text
24435333 s^2 > 5246976000 L2.
```

Again, this only helps after the nominal/source-domain margin `s` and the same-domain residual cap are genuinely supplied.

## 6. Why the half-Q split is the right default

More generally, for any `theta` with `0<theta<1`, (11) gives

```text
|(x+y)^T l|
 <= theta Q + (17/(20 theta))||l||^2,
```

so

```text
V'
 <= -(1-theta)Q + (17/(20 theta))||l||^2.
```

Using (14), the invariant-boundary residual tolerance is proportional to

```text
theta*(1-theta).
```

This is maximized at `theta=1/2`.  Therefore (12)-(20) use the optimal split **within this direct-metric family**; the factor `1/2` was not chosen arbitrarily.

This does not claim global sharpness among all possible quadratic Lyapunov functions or all possible residual metrics.  A future generalized-eigenvalue/SDP optimization could improve the constants further.

## 7. Failure boundaries and interface discipline

1. **The lemma consumes the same residual that appears in the exact force-coordinate block equation.**  It must not be fed an unnormalized raw source force unless the source-to-force adapter has proved that equality.
2. **The bound is additive-residual compatible.**  It does not require `l_i` to vanish when a cross coordinate vanishes, so it is an honest consumer for the positive-offset obstruction identified in `T-P5-009`, once an actual same-domain `L2` bound exists.
3. **No source-domain bootstrap is created from nothing.**  `T-P5-018` still needs a nominal-domain margin (or another absolute-state enclosure) before (21) can protect the physical box.
4. **P8 ramp-graph coverage is independent.**  In particular, this theorem cannot repair any incompatibility between `w=c t` and a source theorem whose `w` interval is too small.
5. **The exact-rational block is an assumption here.**  Float64 `dM/cijk` errors, solve defect, controller remainder, and source semantics remain in their own lanes until they are translated into the residual `l` with certified bounds.
6. **No provenance/admission claim.**  This child is mathematics only and remains pending until formalized, independently verified, and harvested by 梁智炜.

## 8. Lean-friendly theorem decomposition

The main new fact can be formalized entirely over `ℚ`/`ℝ` scalar arithmetic; no matrix library is necessary.

Recommended atomic lemmas:

```lean
-- Three weighted Young squares used in (3).
theorem young_4_to_1 (a b : ℝ) :
    |a*b| <= 2*a^2 + (1/8)*b^2 := ...

theorem block45_Q_diag_lower ... :
    (143/200)*x4^2
      + (1849/3200)*x5^2
      + (2034997/3000000)*y4^2
      + (2398011/4000000)*y5^2
    <= Q := ...

-- Generic division-free two-variable metric bridge.
theorem pair_sum_sq_le_of_metric
    (a b x y : ℝ)
    (ha : 0 < a) (hb : 0 < b)
    (hbudget : 5*(a+b) <= 17*a*b) :
    5*(x+y)^2 <= 17*(a*x^2+b*y^2) := ...
```

The two concrete budget checks are `norm_num` targets using (9).  Then:

```lean
theorem block45_sum_metric :
    5*((x4+y4)^2 + (x5+y5)^2) <= 17*Q := ...
```

The residual consumer can stay abstract:

```lean
theorem residual_absorb_from_sum_metric
    (hQ : 0 <= Q)
    (hmetric : 5*z^2 <= 17*Q*L2)
    : |z| <= (1/2)*Q + (17/10)*L2 := ...
```

followed by the scalar ledger:

```lean
theorem block45_improved_iss
    (hDeriv : dV <= -Q + z)
    (hAbsorb : z <= (1/2)*Q + (17/10)*L2)
    (hQV : (457/672)*V <= Q) :
    dV <= -(457/1344)*V + (17/10)*L2 := ...
```

and exact rational corollaries

```lean
2285*Vstar > 11424*L2,
45696*L2 < 2285,
17823*s^2 > 3716608*L2.
```

A formal agent should prefer this elementary route over encoding the full inverse of the `4x4` dissipation matrix.

## 9. Recommended next seam

The shortest useful chain after this child is

```text
source/checker: same-domain bound l4^2+l5^2 <= L2
    + T-P5-019: direct residual metric / improved ISS
    + T-P5-017: exact affine-ramp frame, or T-P5-018: zero-initial incremental tube
    + P8: independent absolute-domain/ramp-graph coverage
    => strictly cheaper block-(4,5) residual energy budget.
```

The next formalization target is therefore the scalar theorem `(10)` plus the ledger `(15)/(19)`.  Source semantics, P8 domain expansion, and global integration should remain with their existing owners.

**Status: pending.  待封不觉独立验证 / 待梁智炜收割与最终整合。**
