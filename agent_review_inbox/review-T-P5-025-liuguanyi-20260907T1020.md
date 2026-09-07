---
kind: review_result
review_id: review-T-P5-025-liuguanyi-20260907T1020
task_id: T-P5-025
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T10:04:00-06:00
created_at: 2026-09-07T10:20:00-06:00
inspected_commit: c9c60150ff3128c38ff0a28d0838b7e5f43ad2e6
continuation_of:
  - review-T-P5-023-liuguanyi-20260907T0916
  - review-T-P5-024-kuangmanmozun-20260907T0945
related_reviews:
  - review-T-P5-022-liuguanyi-20260907T0820
  - review-T-P5-020-guyuefangyuan-20260907T0743
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: preserve_K_path_as_a_typed_component_matrix_and_add_a_direct_finite_orthant_quadratic_certificate_consumer_before_collapsing_to_ell2_path
---

# T-P5-025 — direct orthant certificate from transported component bounds to P5 small gain

## 0. Result in one sentence

`T-P5-023` currently collapses the transported component matrix `K_path` to the scalar

```text
ell2_path = sum_{a,k} K_path[a,k]^2,
```

before the P5 consumer sees it.  `T-P5-024` then substantially improves the geometry of the scalar consumer.  There is nevertheless one more source-to-math loss that can be removed: **the full nonnegative component matrix `K_path` can be consumed directly by the exact block-(4,5) dissipation quadratic through finitely many rational orthant quadratic-form checks.**

The resulting bridge needs no square root, spectral norm, global Euclidean residual gain, or multiplication of independently optimized constants.  It is a strict extension of the current `ell2_path` route: the scalar route remains a fallback, while anisotropic source/Jacobian information can pass through without being destroyed.

This is source-independent interface mathematics only.  It does not certify any concrete `K_path`, Julia/Float64 Jacobian, P8 cell chain, ODE continuation, provenance, P5/P8/M4 closure, or registry admission.

---

## 1. Exact block-(4,5) objects

Use

```text
z = (x4,x5,y4,y5)^T in R^4,
L z = (x4+y4, x5+y5)^T in R^2,
```

with

```text
L = [1 0 1 0
     0 1 0 1].
```

Write the exact dissipation from `T-P5-024` as

```text
Q(z) = z^T P z,
```

where

```text
P =
[ 3/4      -3/400       0          1/800      ]
[-3/400     29/50      -1/800      0          ]
[ 0        -1/800       2049997/3000000  0    ]
[ 1/800     0           0          2399261/4000000 ].
```

`T-P5-024` already provides a rational positive-definiteness certificate for the same `Q`.

Let the centered generalized-force residual be

```text
r = (r4,r5)^T.
```

Suppose `T-P5-023` or a source checker preserves the full nonnegative component table

```text
K in R_{>=0}^{2 x 4}
```

and proves

```text
|r_a| <= sum_k K[a,k] |z_k|,        a=1,2.             (1)
```

This is strictly more information than the scalar consequence

```text
||r||^2 <= ||K||_F^2 ||z||^2.                           (2)
```

The present child consumes (1) directly.

---

## 2. First bridge: component envelope to direct power envelope

The P5 centered coupling is

```text
C(z,r) := (Lz)^T r.
```

From (1), only triangle inequality is needed:

```text
|C(z,r)|
 <= sum_a |(Lz)_a| |r_a|
 <= sum_a sum_k |(Lz)_a| K[a,k] |z_k|
 = |Lz|^T K |z|.                                      (3)
```

This is already better typed than the scalar route because the source ordering, force-channel ordering, and state-coordinate direction remain visible in `K`.

No Cauchy inequality has yet been applied.

---

## 3. Finite orthant reduction

For a sign vector

```text
sigma in {+1,-1}^4,
tau   in {+1,-1}^2,
```

write `D_sigma`, `D_tau` for the corresponding diagonal sign matrices.

For every concrete `z`, choose signs so that

```text
|z|  = D_sigma z,
|Lz| = D_tau Lz.                                      (4)
```

(When a component is zero, either sign is allowed.)

Then the right side of (3) becomes exactly

```text
|Lz|^T K |z|
 = z^T L^T D_tau K D_sigma z.                         (5)
```

Only the symmetric part contributes to a scalar quadratic form.  Define

```text
B_{sigma,tau}
 := sym(L^T D_tau K D_sigma)
  = (L^T D_tau K D_sigma
     + D_sigma K^T D_tau L)/2.                        (6)
```

Hence

```text
|Lz|^T K |z| = z^T B_{sigma,tau} z.                  (7)
```

Therefore a completely finite exact-rational certificate is enough.

### Direct orthant small-gain theorem

Assume `mu >= 0`, (1), and for every sign pair `(sigma,tau)`

```text
mu P - B_{sigma,tau}  is positive semidefinite.        (8)
```

Then for every `z` and every residual satisfying (1),

```text
|(Lz)^T r| <= mu Q(z).                                (9)
```

### Proof

Choose `(sigma,tau)` from (4).  By (3), (7), and (8),

```text
|(Lz)^T r|
 <= |Lz|^T K |z|
 = z^T B_{sigma,tau} z
 <= mu z^T P z
 = mu Q(z).
```

That is the entire proof.

There is no square-to-absolute-value step and no need to form `ell2_path`.

---

## 4. The certificate is finite and rational

For block-(4,5), there are at most

```text
2^4 * 2^2 = 64
```

sign pairs.  Global sign reversal sends

```text
(sigma,tau) -> (-sigma,-tau)
```

and leaves

```text
D_tau K D_sigma
```

unchanged, so at most **32 distinct matrices** actually need checking.

If `K`, `mu`, and `P` are rational, every matrix in (8) is rational.  A checker can therefore emit, for each distinct sign pair, an exact rational LDL/SOS certificate or any other exact PSD witness accepted by the formalization layer.  No numerical eigenvalue or square root is required.

For a strict checker margin, it is even simpler to require every matrix in (8) to be positive definite and provide positive rational LDL pivots.  The mathematical theorem itself only needs semidefiniteness.

This is a natural interface for `T-P5-023`: its path transport already computes a concrete nonnegative `K_path`.  The checker should preserve that table as a first-class artifact and compute `ell2_path` only as a fallback scalar projection.

---

## 5. Why this can be strictly sharper than T-P5-024

`T-P5-024` starts from the scalar implication

```text
||r||^2 <= ell2 ||z||^2
```

and proves the excellent joint geometry

```text
25 ||Lz||^2 ||z||^2 <= 144 Q(z)^2.
```

With `ell2 = ||K||_F^2`, its checker condition is

```text
144 ||K||_F^2 <= 25 mu^2.                             (10)
```

Condition (10) is a valid universal fallback for the component table `K`, but it forgets *where* the gain sits.  The direct orthant test (8) keeps that anisotropy.

A simple exact rational example proves that the improvement can be material.

Take a source envelope with only one active entry:

```text
K[1,1] = kappa >= 0,
all other K[a,k] = 0.                                  (11)
```

Thus

```text
|r4| <= kappa |x4|,
r5 = 0.                                                (12)
```

The coupling obeys

```text
|(Lz)^T r|
 <= kappa |x4+y4| |x4|.                               (13)
```

I now prove the exact rational block inequality

```text
|x4(x4+y4)| <= (49/30) Q(z).                          (14)
```

Let `A` be the symmetric matrix of `x4(x4+y4)`:

```text
A =
[1  0  1/2  0
 0  0   0   0
 1/2 0  0   0
 0  0   0   0].
```

Then (14) follows if both

```text
(49/30)P - A > 0,
(49/30)P + A > 0.                                     (15)
```

The leading principal minors of `(49/30)P - A` are exactly

```text
9/40,
3407999/16000000,
1255633011647/1440000000000000,
1321698458648580481847/1555200000000000000000000,
```

and those of `(49/30)P + A` are

```text
89/40,
101167997/48000000,
9139258405266941/4320000000000000,
3223330686008501679625847/1555200000000000000000000.
```

Every numerator and denominator is strictly positive.  Sylvester's criterion proves both matrices positive definite, hence (14).

Therefore (12) implies the direct small-gain certificate

```text
|(Lz)^T r| <= (49/30) kappa Q(z).                     (16)
```

By contrast, the scalar `T-P5-024` fallback has `ell2=kappa^2`, so it asks for

```text
mu >= (12/5) kappa.                                   (17)
```

The direct rational certificate only asks for

```text
mu >= (49/30) kappa.                                  (18)
```

For a fixed admissible `mu`, this toy anisotropic envelope permits an exact factor

```text
(12/5)/(49/30) = 72/49 > 1                            (19)
```

more `kappa` than the Frobenius-scalar route.  This is not a claim about the deployed `K_path`; it is a constructive proof that preserving the table can matter substantially and that the new interface is not merely cosmetic.

---

## 6. Relation to T-P5-023 cell/path transport

The source-facing chain should now be

```text
cell-chain / local Jacobian / coordinate transport
    -> nonnegative K_path[a,k]
    -> direct orthant rational matrices (8)
    -> |(x+y)^T r_c| <= mu Q
    -> existing T-P5-020 first-exit / anchor-bias consumer.
```

The existing scalar chain remains available:

```text
K_path
    -> ell2_path = sum K_path[a,k]^2
    -> T-P5-024: 144 ell2_path <= 25 mu^2
    -> |(x+y)^T r_c| <= mu Q.
```

The source checker can try the direct orthant certificate first and fall back to `ell2_path` if desired.  No physical hypothesis changes.

Importantly, the same one-time force-coordinate rule from T-P5-022/T-P5-023 still applies: `K_path` must already be in the actual generalized-force coordinates consumed by `r_c`.  Raw PMI force must be normalized upstream exactly once; a `DHPowerBinding.forceError` table must not be multiplied by `I_B` again.

---

## 7. Distal-coordinate obstruction remains visible

This stronger consumer does **not** repair a missing state contract.

If a source coordinate can vary while

```text
z=(x4,x5,y4,y5)=0,
```

and that variation changes the residual, then no finite `K in R^{2x4}` satisfying (1) exists.  The correct repair is still one of:

1. prove a transport relation from that coordinate to the four P5 coordinates;
2. enlarge `z` and the Lyapunov/dissipation metric;
3. route the effect into a separate additive/transverse budget.

The orthant certificate should never be used to hide a missing `T-P5-023` path/state premise.

---

## 8. Minimal theorem decomposition for Lean

The formalization need not enumerate source cells or Jacobians.

### `component_envelope_power_bound`

For fixed finite vectors/matrices, prove

```text
(forall a, |r_a| <= sum_k K[a,k] |z_k|)
  -> |dot (L z) r| <= dot |L z| (K |z|).
```

Only finite sums and triangle inequality are needed.

### `orthant_quadratic_small_gain`

Inputs: `P,L,K,mu`, nonnegative `K`, a residual satisfying the component envelope, and a hypothesis that every sign pair satisfies the quadratic comparison corresponding to (8).

Conclusion:

```text
|dot (L z) r| <= mu * (z^T P z).
```

A convenient theorem statement may accept sign selectors `sigma,tau` with entries `±1` and the identities `|z|=D_sigma z`, `|Lz|=D_tau Lz`; a block45 corollary can discharge existence componentwise by `by_cases 0 <= ...`.

### `block45_one_axis_direct_certificate`

Formalize the exact rational regression example (14):

```text
abs (x4*(x4+y4)) <= (49/30) * qDissipation x4 x5 y4 y5.
```

An LDL/SOS decomposition is preferable to importing a matrix eigenvalue API.

These theorems are disjoint from the already-claimed `T-P5-024` sidecar.

---

## 9. Remaining boundary

Still open after this child:

1. source/P8 must produce an actual certified `K_path` on the same first-exit domain;
2. cell/path connectivity and local exact-real/Float64 increment/Jacobian bounds remain source obligations;
3. anchor bias `b` remains separate;
4. distal coordinates require a typed variation relation or another budget lane;
5. ODE existence/continuation and P8 flowpipe coverage remain open.

No audit, provenance, receipt, admission, or parent-state mutation is justified by this theorem.

Current label: `pending` mathematical/interface child only.  待封不觉独立验证 / 待梁智炜收割与最终整合。
