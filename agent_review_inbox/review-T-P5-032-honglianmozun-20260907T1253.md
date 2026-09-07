---
kind: review_result
review_id: review-T-P5-032-honglianmozun-20260907T1253
task_id: T-P5-032
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-07T12:46:00-06:00
created_at: 2026-09-07T12:53:00-06:00
inspected_commit: fadcea91671504eeeb73ea6f70a6435c9d1c58b3
inspected_paths:
  - agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md
  - agent_review_inbox/review-T-P5-030-honglianmozun-20260907T1205.md
  - agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md
continuation_of:
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-030-honglianmozun-20260907T1205
related_reviews:
  - review-T-P5-017-honglianmozun-20260907T0558
  - review-T-P5-031-guyuefangyuan-20260907T1224
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_nine_square_Q_minus_eight_ninths_V_identity_then_replace_the_coarse_Q_to_V_constant_in_single_trajectory_and_incremental_energy_consumers
---

# T-P5-032 — exact nine-square proof upgrades the block-(4,5) dissipation to `Q >= (8/9) V`

## 0. Result in one sentence

The `eps=1` block-(4,5) hypocoercive storage already used by `T-P5-017/019/030` has substantially more direct coercivity than the old route through the common Euclidean norm.  For the same exact rational matrices and the same dissipation quadratic `Q`, there is an explicit nine-square identity proving

```text
Q(x,y) >= (8/9) V(x,y).                                  (0.1)
```

This is source-independent algebra.  Combining (0.1) with the already-derived direct residual metric

```text
5 ||x+y||^2 <= 17 Q                                      (0.2)
```

improves the reusable energy ledger from

```text
V' <= -(457/1344) V + (17/10)||l||^2
```

to

```text
V' <= -(4/9) V + (17/10)||l||^2.                         (0.3)
```

The decay coefficient is larger by the exact factor

```text
(4/9)/(457/1344) = 1792/1371 > 1,                        (0.4)
```

so every residual/tube budget that uses the same `(17/10)||l||^2` consumer gains about 30.7% without changing the source contract.

In particular:

```text
one-trajectory V*=1/4 barrier:      153 L2 < 10,          (0.5)
T-P5-030 K=1/12 incremental tube:   153 mu + 1836 nu < 40. (0.6)
```

The latter replaces `11424 mu + 137088 nu < 2285` and is strictly weaker by the same factor `1792/1371` after normalizing both to `mu+12 nu`.

No source gain table, Float64/solve theorem, ODE first-exit theorem, P8 coverage, provenance/admission, or P5/M4 closure is supplied here.

---

## 1. Exact storage and dissipation already in the accepted mathematical lane

Use the exact matrices from `T-P5-019`:

```text
M = diag(350003/3000000, 200739/4000000),
D = diag(4/5, 13/20),

K = [[3/4,    -3/400],
     [-3/400, 29/50]],

A = [[0, 1/400],
     [-1/400, 0]].                                       (1.1)
```

For the moving-frame / relative equation

```text
x' = y,
M y' + D y + K x = A x - l,                              (1.2)
```

the `eps=1` storage is

```text
V(x,y)
 := (1/2) y^T M y
  + (1/2) x^T K x
  + x^T M y
  + (1/2) x^T D x,                                       (1.3)
```

and the exact derivative identity is

```text
V' = -Q(x,y) - (x+y)^T l,                                (1.4)
```

with

```text
Q(x,y)
 := y^T(D-M)y + x^T K x - y^T A x.                      (1.5)
```

`T-P5-019` previously lower-bounded `Q` and upper-bounded `V` separately through

```text
N = ||x||^2+||y||^2,
Q >= (457/800)N,
V <= (21/25)N,
```

which yields only

```text
Q >= (457/672)V.                                         (1.6)
```

The loss in (1.6) is not intrinsic.  `Q` and `V` share several cross terms, so comparing both through `N` throws away useful correlation.

---

## 2. Exact nine-square identity for `Q-(8/9)V`

Write

```text
x=(x4,x5),
y=(y4,y5).
```

Direct exact-rational expansion gives the following identity:

```text
Q - (8/9)V
=
  (51869/13500000) x4^2
+ (16837/3000000)  x5^2
+ (15616199/27000000) y4^2
+ (6647479/12000000)  y5^2

+ (1/240)              (x4-x5)^2
+ (350003/6750000)     (x4-y4)^2
+ (1/800)              (x4+y5)^2
+ (1/800)              (x5-y4)^2
+ (66913/3000000)      (x5-y5)^2.                        (2.1)
```

Every coefficient in (2.1) is strictly positive.  Therefore

```text
Q - (8/9)V >= 0,                                         (2.2)
```

which is exactly (0.1).

This identity is stronger and cleaner than an eigenvalue computation: it contains only rational constants and nine scalar squares.  A future Lean proof can be `ring_nf` plus nonnegativity of squares and `norm_num` on the coefficients.  No matrix inverse, square root, characteristic polynomial, numerical eigensolver, or source premise is required.

### How (2.1) was found

In the coordinate order

```text
z=(x4,x5,y4,y5),
```

the symmetric matrix of `Q-(8/9)V` is

```text
H =
[[ 11/180,          -1/240,          -350003/6750000,  1/800],
 [ -1/240,           1/30,           -1/800,           -66913/3000000],
 [ -350003/6750000, -1/800,           17049961/27000000, 0],
 [ 1/800,           -66913/3000000,   0,                6930131/12000000 ]]. (2.3)
```

Subtracting the absolute off-diagonal weights from each diagonal leaves the four positive margins

```text
m4x = 51869/13500000,
m5x = 16837/3000000,
m4y = 15616199/27000000,
m5y = 6647479/12000000.                                  (2.4)
```

Re-adding each edge as `(zi-zj)^2` for a negative edge and `(zi+zj)^2` for a positive edge yields exactly (2.1).  Thus (2.1) is simply an explicit diagonally-dominant SOS decomposition, not a sampled PSD observation.

---

## 3. Improved residual-coupled Lyapunov inequality

`T-P5-019` already proved the direct coupling metric

```text
5 ||x+y||^2 <= 17 Q.                                     (3.1)
```

Using the same half-Young consumer as that review gives

```text
|(x+y)^T l|
 <= (1/2)Q + (17/10)||l||^2.                             (3.2)
```

Substitute (3.2) into the exact derivative (1.4):

```text
V'
 <= -(1/2)Q + (17/10)||l||^2.                            (3.3)
```

Now use the new direct coercivity (0.1):

```text
(1/2)Q >= (4/9)V.                                        (3.4)
```

Hence

```text
V' <= -(4/9)V + (17/10)||l||^2.                          (3.5)
```

This changes only the `Q -> V` comparison.  The residual coupling constant `17/10`, force coordinates, moving frame, and source-facing definition of `l` remain exactly the same.

The corresponding constant-residual ultimate coefficient is

```text
(17/10)/(4/9) = 153/40 = 3.825,                          (3.6)
```

instead of the previous value just below `5`.

---

## 4. Stronger one-trajectory finite-energy barrier

Suppose on the relevant first-exit domain

```text
||l||^2 <= L2.                                           (4.1)
```

At a generic energy barrier `V=Vstar`, (3.5) is strictly inward whenever

```text
(17/10)L2 < (4/9)Vstar.                                  (4.2)
```

Clearing denominators gives the compact division-free gate

```text
153 L2 < 40 Vstar.                                       (4.3)
```

For the existing convenient choice

```text
Vstar = 1/4,                                              (4.4)
```

this becomes

```text
153 L2 < 10.                                              (4.5)
```

The old `T-P5-019` quarter-barrier condition was

```text
45696 L2 < 2285.                                         (4.6)
```

The permitted `L2` threshold improves by exactly

```text
(10/153) / (2285/45696)
 = 1792/1371
 = 1 + 421/1371.                                         (4.7)
```

So the source-side residual-square budget is enlarged by about 30.7% without any new source assumption.

---

## 5. Stronger T-P5-030 incremental ramp-parameter tube

Now reuse the incremental residual envelope from `T-P5-030`:

```text
||Dl||^2 <= mu*Vd + nu*dc^2,
mu >= 0,
nu >= 0.                                                  (5.1)
```

The new derivative bound is

```text
Vd'
 <= -(4/9)Vd + (17/10)(mu*Vd+nu*dc^2)

 = -[(4/9)-(17/10)mu] Vd
   + (17/10)nu dc^2.                                     (5.2)
```

For a generic candidate tube

```text
Vd = Kc * dc^2,
Kc > 0,                                                   (5.3)
```

the boundary derivative is strictly negative whenever

```text
[(4/9)-(17/10)mu] Kc > (17/10)nu.                        (5.4)
```

Clearing denominators gives the clean rational theorem target

```text
(40 - 153*mu) * Kc > 153*nu.                             (5.5)
```

Together with the initial condition

```text
C0 < Kc,
C0 = 474733828336525417 / 5726342542105201000,            (5.6)
```

(5.5) is the exact first-exit arithmetic seam for any chosen rational tube coefficient `Kc`.

### Existing `Kc=1/12` specialization

`T-P5-030` already proved `C0<1/12`, so keep its same tube size:

```text
Kc = 1/12.                                                (5.7)
```

Then (5.5) becomes

```text
40 - 153*mu > 1836*nu,                                   (5.8)
```

i.e.

```text
153*mu + 1836*nu < 40.                                   (5.9)
```

Equivalently,

```text
mu + 12*nu < 40/153.                                     (5.10)
```

The previous T-P5-030 gate is

```text
mu + 12*nu < 2285/11424.                                 (5.11)
```

and

```text
(40/153)/(2285/11424) = 1792/1371 > 1.                  (5.12)
```

Thus the same `1/12` parameter tube accepts about 30.7% more incremental residual budget.

---

## 6. Direct downstream upgrade for T-P5-031

`T-P5-031` is a disjoint source-to-math bridge.  It produces

```text
mu = U+p,
nu = W+q,                                                 (6.1)
```

from nonnegative physical incremental gains, with the cross-term absorption premise

```text
p*q >= U*W.                                               (6.2)
```

Nothing in that construction needs to change.  Only its final energy consumer can be strengthened by substituting (6.1) into (5.9):

```text
153*(U+p) + 1836*(W+q) < 40.                             (6.3)
```

So the recommended pipeline becomes

```text
physical incremental gain table
 -> T-P5-031 square-only U/W/p/q bridge
 -> mu=U+p, nu=W+q
 -> T-P5-032 gate 153 mu + 1836 nu < 40
 -> T-P5-030 Vd<dc^2/12 first-exit consumer.              (6.4)
```

This does not compete with the already claimed T-P5-031 source-gain or Lean work; it only replaces the downstream dissipation constant.

### Optional exact pre-search obstruction for the new gate

If a source checker wants to test whether any real nonnegative slack pair can satisfy both (6.2) and (6.3), define

```text
R8 := 40 - 153*U - 1836*W.                               (6.5)
```

The weighted linear slack cost is

```text
153*p + 1836*q.                                           (6.6)
```

Under `p*q >= U*W`, its infimum is

```text
2*sqrt(153*1836*U*W).
```

Therefore the strict feasibility diagnostic is exactly

```text
R8 > 0,
R8^2 > 1123632 * U*W,                                    (6.7)
```

because

```text
4*153*1836 = 1123632.                                    (6.8)
```

As in T-P5-031, a trusted checker need not formalize the square root: it can emit rational `p,q` and verify (6.2)-(6.3) directly.  Equation (6.7) is only a search-space obstruction/diagnostic.

---

## 7. Failure boundary and what is not improved

The new coercivity does **not** repair any of the following:

- an absolute residual cap cannot by itself prove a parameter-cell diameter shrinking like `dc^2`;
- T-P5-030 still needs an incremental residual theorem of the form (5.1), or the stronger T-P5-031 physical gain contract;
- ODE existence/continuation and first-exit logic remain separate;
- the P8 absolute `w=c*t` source-domain obstruction remains separate;
- Float64/solve/controller incremental semantics remain source-side obligations;
- this is not a registry/admission result and does not close P5/P8/M4.

What changes is only the amount of already-correct residual budget that the exact block-(4,5) energy can absorb.

---

## 8. Recommended Lean theorem decomposition

The main new theorem can be exceptionally small.

```text
block45_Q_minus_eight_ninths_V_sos
```

Statement: with the exact rational scalar definitions of `V` and `Q`, prove equality (2.1).

Expected proof shape:

```text
ring_nf
```

or an explicit `ring` after unfolding constants.

Then:

```text
block45_Q_ge_eight_ninths_V
```

Input: the same four real coordinates.
Output:

```text
(8/9)*V <= Q.
```

Proof: rewrite by the SOS identity and discharge nine nonnegative square terms with `positivity`/`nlinarith`.

Downstream scalar children:

```text
block45_residual_decay_8_9
```

Input:

```text
Vdot <= -(1/2)*Q + (17/10)*L2,
(8/9)*V <= Q.
```

Output:

```text
Vdot <= -(4/9)*V + (17/10)*L2.
```

```text
quarter_barrier_8_9
```

Input `153*L2 < 10` and `V=1/4`; output strict inward derivative.

```text
parameter_tube_boundary_8_9
```

Input

```text
L2 <= mu*V + nu*dc2,
(40-153*mu)*Kc > 153*nu,
V = Kc*dc2,
dc2 > 0,
```

plus the derivative ledger; output `Vdot<0`.

```text
parameter_tube_one_twelfth_8_9
```

Specialize `Kc=1/12` to the single checker gate

```text
153*mu + 1836*nu < 40.
```

All of these are source-independent rational algebra.  They should remain separate from the source gain table, P8 coverage, and any final admission receipt.

---

## 9. Evidence / exact arithmetic checks

The trusted content of this review is the explicit identity (2.1).  Expanding its right-hand side reproduces the matrix (2.3) coefficient-for-coefficient.  The four leftover margins are exactly the rational values in (2.4), all positive.

The downstream arithmetic was also reduced exactly:

```text
(1/2)*(8/9) = 4/9,
(17/10)/(4/9) = 153/40,
153*(1/12) = 51/4,
1836 = 153*12,
4*153*1836 = 1123632,
(40/153)/(2285/11424) = 1792/1371.
```

No floating inequality is needed for any theorem statement.  Decimal percentages in the prose are explanatory only.

## 10. Admission boundary

Status: `pending mathematical child`.

This review proves a new exact-rational energy inequality on the already-defined block-(4,5) mathematical model.  It does not authenticate the deployed source, create an incremental residual envelope, prove ODE/flowpipe coverage, validate a Lean build, alter the authoritative workflow state, or justify registry admission.
