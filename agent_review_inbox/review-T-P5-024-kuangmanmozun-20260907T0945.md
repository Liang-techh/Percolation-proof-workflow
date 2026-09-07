---
kind: review_result
review_id: review-T-P5-024-kuangmanmozun-20260907T0945
task_id: T-P5-024
source_agent: 狂蛮魔尊
agent: 狂蛮魔尊
claimed_at: 2026-09-07T09:37:00-06:00
created_at: 2026-09-07T09:45:00-06:00
inspected_commit: d271bb25b9f0a784b4ad831592204f181af9b7be
continuation_of:
  - review-T-P5-020-guyuefangyuan-20260907T0743
  - review-T-P5-023-liuguanyi-20260907T0916
related_reviews:
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P5-019-honglianmozun-20260907T0702
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_joint_UN_over_Q_squared_certificate_and_use_144_ell2_le_25_mu_squared_instead_of_multiplying_the_separate_N_and_x_plus_y_bounds
---

# T-P5-024 — joint `N × ||x+y||²` dissipation inequality and sharper centered small gain

## 0. Result in one sentence

`T-P5-020` bounds the centered residual coupling by multiplying two independently valid estimates,

```text
N <= (800/457) Q,
||x+y||^2 <= (17/5) Q,
```

which gives

```text
||x+y||^2 N <= (2720/457) Q^2.
```

For the **actual exact block-(4,5) quadratic `Q`**, those two worst cases cannot occur simultaneously.  A direct joint quadratic argument proves the strictly better, clean rational inequality

```text
25 ||x+y||^2 N <= 144 Q^2.                            (J)
```

Hence a centered gain `||r_c||² <= ell2 N` is absorbed whenever

```text
144 ell2 <= 25 mu^2,   0 <= mu < 1,                  (SG)
```

replacing the previous `2720 ell2 <= 457 mu²`.  The admissible `ell2` increases by the exact factor `4250/4113 ≈ 1.033309`, about 3.33%, with no change to the storage, source contract, or anchor-bias ledger.

This is a source-independent inequality child only.  It does not certify the `T-P5-023` cell chain, any Julia/Float64 Jacobian, P8 coverage, ODE continuation, provenance, P5/P8/M4 closure, or registry admission.

---

## 1. Exact quadratic reused from T-P5-019

Use coordinates

```text
z = (x4,x5,y4,y5),
N = x4^2+x5^2+y4^2+y5^2,
U = (x4+y4)^2 + (x5+y5)^2.
```

The exact dissipation quadratic is

```text
Q
 = (3/4)x4^2 + (29/50)x5^2 - (3/200)x4*x5
   + (2049997/3000000)y4^2
   + (2399261/4000000)y5^2
   + (1/400)x4*y5 - (1/400)x5*y4.                    (1)
```

`T-P5-019` already proves `Q>0` for nonzero `z` and the convenient direct metric `5U <= 17Q`.  `T-P5-018` separately proves `457 N <= 800 Q`.  The old centered-gain constant simply multiplies those two inequalities:

```text
U N <= (17/5)(800/457) Q^2
     = (2720/457) Q^2.                               (2)
```

The present child keeps `U` and `N` coupled before comparing to `Q`.

---

## 2. A weighted AM-GM reduction

For `U,N >= 0`, choose the rational weight

```text
alpha = 7/10.
```

Then the exact square

```text
((7/10)U - (10/7)N)^2 >= 0
```

gives

```text
4 U N
 <= ((7/10)U + (10/7)N)^2.                          (3)
```

So it is enough to prove a **single quadratic-form comparison**

```text
(7/10) U + (10/7) N <= (24/5) Q.                    (4)
```

Indeed, since both sides of (4) are nonnegative,

```text
4UN
 <= ((7/10)U + (10/7)N)^2
 <= (24/5)^2 Q^2
 = (576/25) Q^2,
```

which is exactly

```text
25 U N <= 144 Q^2.                                   (5)
```

Thus the whole improvement reduces to the positive definiteness of one rational `4x4` form.

---

## 3. Exact positive-definite certificate for the joint form

Let

```text
R(z)
 := (24/5)Q(z) - (7/10)U(z) - (10/7)N(z).            (6)
```

In the coordinate order `(x4,x5,y4,y5)`, the symmetric matrix of `R` is

```text
[ 103/70       -9/250      -7/10          3/500        ]
[ -9/250       1147/1750   -3/500        -7/10         ]
[ -7/10        -3/500      5037479/4375000   0         ]
[  3/500       -7/10        0          13134481/17500000].  (7)
```

Its four leading principal minors are exactly

```text
Delta1 = 103/70,

Delta2 = 737389/765625,

Delta3 = 10550522799949/13398437500000,

Delta4 = 302371148712671469/234472656250000000000.     (8)
```

Every numerator and denominator in (8) is strictly positive.  By Sylvester's criterion, the matrix in (7) is positive definite.  Therefore

```text
R(z) >= 0                                             (9)
```

for every real `z`, with strict inequality for `z != 0`.  This proves (4), hence the joint inequality (5).

This certificate is intentionally rational.  It needs no numerical eigenvalue, square root, matrix inverse, sampled state, or source semantics.

---

## 4. Sharper centered residual absorption

Assume the same centered residual premise as `T-P5-020/T-P5-023`:

```text
||r_c||^2 <= ell2 N,
ell2 >= 0.                                             (10)
```

Cauchy gives

```text
|(x+y)^T r_c|^2
 <= U ||r_c||^2
 <= ell2 U N.                                          (11)
```

Using (5),

```text
|(x+y)^T r_c|^2
 <= (144/25) ell2 Q^2.                                (12)
```

Therefore, if a rational checker parameter `mu` satisfies

```text
0 <= mu < 1,
144 ell2 <= 25 mu^2,                                  (13)
```

then

```text
|(x+y)^T r_c| <= mu Q.                                (14)
```

The square-to-absolute-value step is safe because `mu>=0` and `Q>=0`.

Substituting into the existing incremental Lyapunov identity

```text
V' = -Q - (x+y)^T(r_c+b)
```

changes **none** of the later logic:

- if `b=0`, `V' <= -(1-mu)Q`;
- with an anchor bias, the `T-P5-020` first-exit/ISS barrier is reused unchanged after replacing only the centered-gain premise by (13).

So this child is a drop-in strengthening of the current centered branch.

---

## 5. Exact improvement over the old checker condition

Old condition from `T-P5-020`:

```text
2720 ell2 <= 457 mu^2,
```

i.e.

```text
ell2 <= (457/2720) mu^2.                              (15)
```

New condition:

```text
ell2 <= (25/144) mu^2.                                (16)
```

The gain ratio is exactly

```text
(25/144) / (457/2720)
 = 4250/4113
 > 1.                                                  (17)
```

and the absolute coefficient improvement is

```text
25/144 - 457/2720
 = 137/24480.                                          (18)
```

For the convenient `mu=1/2` specialization, the old checker asks for

```text
10880 ell2 <= 457,                                     (19)
```

whereas the new joint theorem only asks for

```text
576 ell2 <= 25.                                        (20)
```

The physical meaning is important: a state direction that nearly saturates the `N/Q` coercivity bound is not the same direction that nearly saturates the `U/Q` residual-coupling bound, so multiplying the two separate constants pays for an impossible simultaneous extremum.

---

## 6. A rational counterexample rules out the tempting `23/4` constant

The clean upper constant `144/25 = 5.76` is not wildly loose.  A very simple rational state already disproves the tempting stronger claim

```text
U N <= (23/4) Q^2.                                    (21)
```

Take

```text
x4 = 0,
x5 = 15,
y4 = 0,
y5 = 14.                                               (22)
```

Then

```text
N = 421,
U = 841,
Q = 248063789/1000000.                                 (23)
```

Direct exact arithmetic gives

```text
4 U N - 23 Q^2
 = 924201500160017 / 1000000000000
 > 0.                                                   (24)
```

Hence the universal constant must be strictly larger than `23/4 = 5.75`, while (5) proves it is at most `144/25 = 5.76`.  Thus the present fully rational certificate brackets the sharp constant inside an interval of width only `1/100`, without solving a quartic optimization problem or importing an eigenvalue oracle.

This witness is also a useful regression guard: any future attempt to advertise a centered joint constant `<=23/4` for the same `Q,U,N` is false.

---

## 7. Interaction with T-P5-023 piecewise-cell transport

`T-P5-023` produces a source/path certificate of the form

```text
||r_c||^2 <= ell2_path N,                              (25)
```

where `ell2_path` comes from the transported component matrix `K_path`.  No change to the cell/path theorem is needed.  The improved consumer is simply

```text
144 ell2_path <= 25 mu^2                               (26)
```

instead of

```text
2720 ell2_path <= 457 mu^2.                            (27)
```

This separation should be preserved:

```text
cell-chain / Jacobian / coordinate transport
    -> ell2_path,

joint block45 dissipation geometry (this child)
    -> 144 ell2_path <= 25 mu^2,

P5 first-exit / anchor ledger
    -> existing T-P5-020 consumer.
```

No source-side checker needs to know the 4x4 Sylvester certificate; it can remain a reusable exact-real theorem.

---

## 8. Minimal formalization target

A formalization agent can keep the theorem decomposition small.

### `block45_joint_residual_metric`

Inputs: real `x4 x5 y4 y5`; define `Q`, `N`, `U` exactly as above.

Conclusion:

```text
25 * U * N <= 144 * Q^2.
```

Recommended proof route:

1. establish the matrix/SOS quadratic inequality (4);
2. establish `(alpha*U-alpha^-1*N)^2 >= 0` with `alpha=7/10`;
3. combine with `ring`/`nlinarith`.

The matrix positivity itself can be encoded either via the exact four-minor Sylvester certificate in (8), or by deriving an explicit rational LDL/SOS decomposition.  The theorem statement should not mention eigenvalues.

### `centered_small_gain_joint`

Premises:

```text
0 <= ell2,
0 <= mu,
0 <= Q,
rcSq <= ell2 * N,
coupling^2 <= U * rcSq,
144 * ell2 <= 25 * mu^2.
```

Conclusion:

```text
|coupling| <= mu * Q.
```

No source binding or path geometry belongs in this theorem.

---

## 9. Remaining boundary

This result improves only the **consumer constant**.  It does not discharge the hard physical premises:

1. `T-P5-023` still needs a certified connecting cell chain/path for actual-vs-nominal comparisons;
2. the local exact-real/Float64 residual increment or Jacobian bounds still need source binding;
3. distal coordinates still need typed variation bounds or a separate transverse/additive route;
4. the nominal-anchor bias `b` is still paid separately;
5. P8 same-domain coverage and ODE existence/continuation remain open.

Do not use the better constant to hide a missing source/path premise.

---

## 10. Admission boundary

`pending` mathematical child only.  No provenance/receipt/admission re-audit was performed, no prior sidecar was independently revalidated, and no P5/P8/M4 or registry state is changed.

Recommended next step: formalize (J) as a small exact-rational sidecar, then let `T-P5-023` feed its `ell2_path` directly into the stronger checker condition `(SG)`.

待封不觉独立验证 / 待梁智炜收割与最终整合。
