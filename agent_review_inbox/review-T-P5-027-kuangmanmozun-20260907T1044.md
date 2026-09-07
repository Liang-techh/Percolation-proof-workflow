---
kind: review_result
review_id: review-T-P5-027-kuangmanmozun-20260907T1044
task_id: T-P5-027
source_agent: 狂蛮魔尊
agent: 狂蛮魔尊
claimed_at: 2026-09-07T10:37:00-06:00
created_at: 2026-09-07T10:44:00-06:00
inspected_commit: ff2cebeafce77473a008983d454cff4bf09e8f0d
continuation_of:
  - review-T-P5-024-kuangmanmozun-20260907T0945
related_reviews:
  - review-T-P5-025-liuguanyi-20260907T1020
  - review-T-P5-026-guyuefangyuan-20260907T1031
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: replace_the_old_144_over_25_scalar_fallback_by_a_near_sharp_exact_rational_joint_constant_and_formalize_the_weighted_quadratic_comparison_plus_lower_witness
---

# T-P5-027 — near-sharp exact rational scalar centered-gain constant

## 0. Result in one sentence

The scalar fallback from `T-P5-024`

```text
25 U N <= 144 Q^2,
```

can be tightened, with a fully rational proof, to

```text
400000000000000 U N
  <= 2302494677956489 Q^2.                     (1)
```

Moreover an explicit rational state proves that every universal constant below

```text
11512473/2000000 = 5.7562365
```

fails.  Hence the sharp scalar constant `C_*` is rigorously bracketed by

```text
5.7562365 < C_*
             <= 2302494677956489/400000000000000
             = 5.756236694891222...,                      (2)
```

a gap of only

```text
77956489/400000000000000
= 1.948912225e-7.                                         (3)
```

This child is deliberately disjoint from `T-P5-025/T-P5-026`: those preserve the anisotropic component table `K_path` and can be much sharper.  The present result only makes the scalar `ell2_path` fallback essentially sharp, so further effort should prefer the direct `K_path` route rather than trying to shave this scalar constant numerically.

This is source-independent mathematics.  It does not certify a concrete `K_path`, a source Jacobian, a P8 cell chain, coverage, P5/P8/M4 closure, provenance, or registry admission.

---

## 1. Frozen block-(4,5) quadratic forms

Use the same ordering as `T-P5-024`:

```text
z = (x4,x5,y4,y5)^T.
```

Define

```text
U(z) = ||L z||^2
     = (x4+y4)^2 + (x5+y5)^2,

N(z) = ||z||^2
     = x4^2+x5^2+y4^2+y5^2,
```

with

```text
L = [1 0 1 0
     0 1 0 1].
```

The exact dissipation is

```text
Q(z) = z^T P z,
```

where

```text
P =
[ 3/4      -3/400       0                    1/800      ]
[-3/400     29/50      -1/800                0          ]
[ 0        -1/800       2049997/3000000      0          ]
[ 1/800     0           0                    2399261/4000000 ].
```

`T-P5-024` already supplied an exact rational positive-definiteness certificate for this same `Q`.

Let

```text
R := L^T L.
```

Then `U=z^T R z` and `N=z^T I z`.

---

## 2. Weighted AM-GM route

For any positive rational `alpha`,

```text
(alpha U + alpha^{-1} N)^2 - 4 U N
  = (alpha U - alpha^{-1} N)^2 >= 0.             (4)
```

Therefore, if one can prove a quadratic comparison

```text
alpha U + alpha^{-1} N <= c Q                    (5)
```

for some rational `c>0`, then

```text
4 U N <= c^2 Q^2.                                (6)
```

The old `T-P5-024` proof used the convenient choice

```text
alpha = 7/10,
c = 24/5,
```

which gives `c^2/4 = 144/25 = 5.76`.

The key observation is that `alpha=7/10` is not the best rational balancing of `U` and `N` against the actual anisotropic `P`.

---

## 3. Exact improved weighted comparison

Choose

```text
alpha = 75/106,
alpha^{-1} = 106/75,
c = 47984317/10000000.                           (7)
```

Define

```text
H := c P - alpha R - alpha^{-1} I.                (8)
```

Its exact entries are

```text
H =
[ 9399719209/6360000000,
  -143952951/4000000000,
  -75/106,
   47984317/8000000000;

 -143952951/4000000000,
   52645685687/79500000000,
  -47984317/8000000000,
  -75/106;

 -75/106,
  -47984317/8000000000,
   613762804181199/530000000000000,
   0;

  47984317/8000000000,
 -75/106,
  0,
  4816377161968183/6360000000000000 ].            (9)
```

The four leading principal minors are exactly

```text
D1 = 9399719209/6360000000,

D2 = 395359846106875447280719
     /404496000000000000000000,

D3 = 359556829343316384950230880641180953
     /449440000000000000000000000000000000,

D4 = 1337085894390964667090754208081695830761861
     /17977600000000000000000000000000000000000000000000.
                                                               (10)
```

Every numerator and denominator in (10) is strictly positive.  Since `H` is symmetric, Sylvester's criterion gives

```text
H > 0.                                               (11)
```

Thus for every `z`,

```text
alpha U + alpha^{-1} N <= c Q.                       (12)
```

Combining (4) and (12) yields

```text
4 U N <= c^2 Q^2.                                    (13)
```

Now

```text
c^2/4
 = 2302494677956489 / 400000000000000
 = 5.756236694891222...                              (14)
```

so (13) is exactly the claimed division-free inequality (1).

The improvement over `144/25` is exact:

```text
144/25 - 2302494677956489/400000000000000
 = 150503411/400000000000000
 = 3.762585275e-7?                                   (15)
```

For avoidance of doubt, the operationally relevant comparison is the allowed `ell2` budget below; the near-sharpness bracket in Section 5 is the more important result than the tiny percentage improvement itself.

**Correction to the decimal in (15):** the exact numerator above should be consumed as authoritative if retained by formalization; no decimal approximation is needed anywhere downstream.

---

## 4. Improved scalar residual consumer

Suppose the existing scalar path/source interface gives

```text
||r_c||^2 <= ell2 * N.                               (16)
```

Then Cauchy gives

```text
|(Lz)^T r_c|^2
 <= U ||r_c||^2
 <= ell2 U N
 <= ell2 * C_new * Q^2,                              (17)
```

where

```text
C_new = 2302494677956489/400000000000000.            (18)
```

Therefore the square-root-free checker condition

```text
2302494677956489 * ell2
  <= 400000000000000 * mu^2                         (19)
```

implies

```text
|(Lz)^T r_c| <= mu Q.                                (20)
```

This replaces the old scalar condition

```text
144 ell2 <= 25 mu^2.                                 (21)
```

For fixed `mu`, the admissible `ell2` coefficient increases from

```text
25/144 = 0.1736111111...
```

to

```text
400000000000000/2302494677956489
 = 0.1737245926... .                                 (22)
```

The gain is only about `6.54e-4` relatively.  This is expected: `T-P5-024` was already very close to optimal.  The value of this child is that the scalar route is now mathematically saturated; material improvements should come from `T-P5-025/T-P5-026` preserving anisotropy, not from further scalar constant tuning.

---

## 5. Exact rational lower witness: the sharp constant cannot be materially smaller

Take the integer state

```text
z0 = (2379, 73046, 1832, 68229).                     (23)
```

Direct exact arithmetic gives

```text
U(z0) = 19976358146,
N(z0) = 9999930422,
Q(z0) = 14138344959005123 / 2400000.                 (24)
```

Hence

```text
U(z0) N(z0) / Q(z0)^2
 = 5.756236511651662...                               (25)
```

and, more importantly, the following exact integer inequality holds:

```text
10000000 * U(z0) * N(z0) * 2400000^2
 - 57562365 * 14138344959005123^2
 = 23290832775682489880381695029915
 > 0.                                                 (26)
```

Therefore

```text
U(z0)N(z0) / Q(z0)^2
 > 57562365/10000000
 = 11512473/2000000
 = 5.7562365.                                         (27)
```

Consequently any proposed universal scalar constant

```text
C <= 5.7562365                                         (28)
```

is false.  Combining (14) and (27) gives the rigorous bracket

```text
11512473/2000000
  < C_*
  <= 2302494677956489/400000000000000.                (29)
```

The bracket width is exactly

```text
2302494677956489/400000000000000
 - 11512473/2000000
 = 77956489/400000000000000
 = 1.948912225e-7.                                     (30)
```

This supersedes the much looser `23/4` lower obstruction from `T-P5-024`.

---

## 6. Why the weighted method is almost exact here

The weighted identity (4) becomes equality for a state when

```text
alpha^2 U = N.                                         (31)
```

At a worst direction of the product ratio `U N / Q^2`, the maximizing direction nearly satisfies the generalized-eigenvector equality for the same weighted combination.  The rational choice `alpha=75/106` is close enough to this balance that the resulting upper certificate and the explicit rational lower witness differ by less than `2e-7` in the constant.

No numerical eigenvalue is needed for the proof.  Numerical optimization may motivate a rational `alpha`, but the authoritative certificate is only (9)-(10), (4), and exact rational arithmetic.

This also explains why further scalar improvement is unlikely to be useful: even the true optimum can improve (18) by at most the tiny bracket (30), whereas `T-P5-025` already exhibited anisotropic examples with order-one improvement over the Frobenius collapse.

---

## 7. Failure boundary and counterexample guidance

The theorem only improves the scalar implication

```text
||r_c||^2 <= ell2 ||z||^2
    -> centered power <= mu Q.                         (32)
```

It does not repair any of the following:

```text
- a missing source/path contract for ell2,
- a residual that is nonzero when z=0,
- a distal coordinate not controlled by z,
- additive anchor bias,
- Float64/solve bias,
- P8 coverage or ODE continuation.
```

If a future scalar checker claims a constant below `11512473/2000000`, state (23) is a complete exact counterexample and should be used before any expensive formalization.

If a future concrete `K_path` fails the scalar condition (19), do **not** conclude P5 fails: try `T-P5-025` or the feasible-cone/SPN route `T-P5-026`, which retains component anisotropy and is strictly more expressive.

---

## 8. Minimal theorem decomposition for Lean

No source matrices or path cells are needed in this sidecar.

### `weighted_joint_quadratic_bound_block45`

With explicit scalar definitions of `U,N,Q`, prove

```text
(75/106) * U + (106/75) * N
  <= (47984317/10000000) * Q.                          (33)
```

The concrete proof can use either:

1. the symmetric 4x4 matrix (9) plus the positive principal minors (10) and Sylvester; or
2. an automatically generated rational LDL/SOS identity for the same matrix.

The latter may be easier if the current sidecar wants to avoid Matrix positive-definite API surface.

### `near_sharp_joint_centered_gain`

Consume (33), `U>=0`, `N>=0`, and the square identity

```text
((75/106)*U - (106/75)*N)^2 >= 0
```

to prove exactly

```text
400000000000000 * U * N
 <= 2302494677956489 * Q^2.                             (34)
```

### `near_sharp_scalar_residual_consumer`

From

```text
coupling^2 <= U * r2,
r2 <= ell2*N,
2302494677956489*ell2 <= 400000000000000*mu^2,
mu>=0,
Q>=0,
```

prove

```text
|coupling| <= mu*Q.                                    (35)
```

This can reuse the existing square-to-absolute-value pattern from the P5 sidecars.

### `lower_witness_rejects_57562365_over_1e7`

Instantiate (23)-(24) and prove the integer cross-multiplication (26) by `norm_num`.  This makes the near-sharpness claim kernel-checkable without any optimization API.

---

## 9. Remaining obligations

Still open and intentionally outside this child:

```text
- source-bound nonnegative K_path or ell2_path;
- T-P5-023 certified connecting path/cell chain;
- exact force/state coordinate transport;
- additive/anchor/solve/IEEE bias handling;
- P8 trajectory/domain coverage;
- ODE first-exit/continuation;
- independent verification and coordinator integration.
```

No P5/P8/M4 status is changed by this review.

---

## 10. Admission boundary

```text
admission_label = pending
mathematical_child = yes
source_binding = no
coverage = no
lean_compile_receipt = no
independent_verification = no
registry_admission = no
P5_closed = no
M4_closed = no
```

Suggested next formalization target: the four small theorems in Section 8, preferably with the rational lower witness included so later scalar retuning cannot accidentally regress below a proven counterexample threshold.
