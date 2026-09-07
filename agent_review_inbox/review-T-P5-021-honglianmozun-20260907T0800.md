---
kind: review_result
review_id: review-T-P5-021-honglianmozun-20260907T0800
task_id: T-P5-021
source_agent: 红莲魔尊
agent: 红莲魔尊
claimed_at: 2026-09-07T07:51:00-06:00
created_at: 2026-09-07T08:00:00-06:00
inspected_commit: bf7397a9a82e1142bb7c95b1eb8e1e938c28d9e8
continuation_of:
  - review-T-P5-019-honglianmozun-20260907T0702
  - review-T-P5-020-guyuefangyuan-20260907T0743
related_reviews:
  - review-T-P5-018-guyuefangyuan-20260907T0634
  - review-T-P5-009-liuguanyi-20260907T0606
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_balanced_discriminant_witness_and_use_it_as_an_optional_checker_frontend_for_T-P5-020
---

# T-P5-021 — exact rational elimination of the centered/anchor split parameter

## 0. Result in one sentence

`T-P5-020` introduces an auxiliary rational dissipation split `mu` satisfying a centered small-gain inequality and an anchor first-exit inequality.  That search parameter can be eliminated completely: the existence of a valid split is equivalent to a two-polynomial discriminant test, and whenever the test passes there is an explicit **rational balanced witness** for `mu`, constructed using only `+,-,*,/` and no square root.

This is a mathematical energy-ledger child only.  It does not source-bind `ell2`/`B2`, does not certify Float64/solve semantics, does not prove P8 domain coverage or ODE continuation, and does not promote P5/P8/M4 or the registry.

---

## 1. Starting point from T-P5-020

On a common first-exit domain, `T-P5-020` reduces the centered-plus-anchor residual problem to finding `mu` with

```text
0 <= mu < 1,
2720 * ell2 <= 457 * mu^2,                            (1)
11424 * B2 < 2285 * (1-mu)^2 * Vstar.                (2)
```

Here

```text
ell2 >= 0,     B2 >= 0,     Vstar > 0.
```

The first inequality pays the centered state increment multiplicatively; the second pays only the nominal-anchor bias at the Lyapunov boundary.

The previous review recommends searching for a rational `mu`.  The present child shows that no parameter search is mathematically necessary.

---

## 2. Abstract balanced-split algebra

Introduce three nonnegative/positive quantities

```text
D > 0,
X >= 0,
Y >= 0,
```

and ask for a split `mu` satisfying

```text
0 <= mu < 1,
X <= D * mu^2,                                        (3)
Y <  D * (1-mu)^2.                                    (4)
```

Normalize only for interpretation:

```text
A := X/D,
B := Y/D.
```

Then (3)-(4) ask for

```text
sqrt(A) <= mu < 1 - sqrt(B).
```

Hence a split exists exactly when

```text
sqrt(A) + sqrt(B) < 1.                                (5)
```

The useful point is that (5) has a fully polynomial equivalent.

Define

```text
C     := D - X - Y,
Delta := C^2 - 4*X*Y.                                 (6)
```

For `D>0`, `X>=0`, `Y>=0`,

```text
sqrt(A)+sqrt(B) < 1
iff
C > 0  and  Delta > 0.                                (7)
```

Indeed, after multiplying (5)^2 by `D`, the condition is

```text
D - X - Y > 2*sqrt(XY).
```

The left side is positive, so squaring is lossless and gives exactly (7).  Conversely, `C>0` and `C^2>4XY` imply `C>2 sqrt(XY)` and therefore (5).

Thus `C>0` and `Delta>0` are the exact strict feasibility conditions, not merely another sufficient Young bound.

---

## 3. Canonical rational witness: no sqrt and no density argument

The main new observation is that the discriminant test itself produces a rational witness.

Define

```text
mu_bal := (D + X - Y) / (2D).                         (8)
```

Because

```text
D + X - Y = C + 2X,
D - X + Y = C + 2Y,
```

`C>0` and `X,Y>=0` give

```text
0 < mu_bal < 1.                                       (9)
```

Now the two square slacks have the **same discriminant**:

```text
(D + X - Y)^2 - 4DX
  = (D - X - Y)^2 - 4XY
  = Delta,                                             (10)

(D - X + Y)^2 - 4DY
  = (D - X - Y)^2 - 4XY
  = Delta.                                             (11)
```

Since `Delta>0`, dividing (10)-(11) by `4D^2>0` yields

```text
mu_bal^2 > X/D,
(1-mu_bal)^2 > Y/D.                                   (12)
```

Equivalently,

```text
X < D * mu_bal^2,
Y < D * (1-mu_bal)^2.                                 (13)
```

Therefore the polynomial feasibility check does more than prove that some split exists: it constructs one explicitly.  If `D,X,Y` are rational, `mu_bal` is rational automatically.  No `sqrt`, rational-density theorem, numerical optimization, or grid search is needed.

This witness is a **feasibility-balanced** witness, not necessarily the decay-optimal one.  The maximum admissible anchor for fixed centered gain occurs at the limiting real choice `mu=sqrt(X/D)`.  The balanced witness instead stays strictly inside both inequalities and is ideal for a simple exact checker/Lean interface.

---

## 4. Specialization to T-P5-020

Put

```text
D := 2285 * Vstar,
X := 13600 * ell2 * Vstar,
Y := 11424 * B2.                                      (14)
```

Because `2285 = 5*457`, condition `X < D*mu^2` is exactly the strict version of the centered condition:

```text
2720 * ell2 < 457 * mu^2.                             (15)
```

The anchor condition is already

```text
11424 * B2 < 2285 * Vstar * (1-mu)^2.                 (16)
```

Define the route-specific linear headroom

```text
C_P5 := 2285*Vstar - 13600*ell2*Vstar - 11424*B2.     (17)
```

Then `T-P5-020` has a valid strict split whenever and, at the mathematical level, exactly when

```text
C_P5 > 0,                                             (18)
C_P5^2 > 621465600 * ell2 * Vstar * B2.               (19)
```

The integer in (19) is exact:

```text
621465600 = 4 * 13600 * 11424.
```

A canonical rational witness is

```text
mu_bal
 = (2285*Vstar + 13600*ell2*Vstar - 11424*B2)
   / (4570*Vstar).                                    (20)
```

Under `ell2>=0`, `B2>=0`, `Vstar>0`, (18)-(19) imply

```text
0 < mu_bal < 1,
2720*ell2 < 457*mu_bal^2,
11424*B2 < 2285*(1-mu_bal)^2*Vstar.                   (21)
```

Therefore (18)-(19) can be used as a **single no-search checker frontend** to the already derived `T-P5-020` energy barrier.

---

## 5. Quarter-barrier corollary

For the moving-frame quarter barrier used earlier,

```text
Vstar = 1/4,
```

multiply `D,X,Y` by four to avoid fractions:

```text
Dq := 2285,
Xq := 13600 * ell2,
Yq := 45696 * B2.
```

Define

```text
Cq := 2285 - 13600*ell2 - 45696*B2.                  (22)
```

The exact checker target becomes

```text
Cq > 0,                                               (23)
Cq^2 > 2485862400 * ell2 * B2.                        (24)
```

with

```text
2485862400 = 4 * 13600 * 45696.
```

The corresponding rational witness is

```text
mu_q = (2285 + 13600*ell2 - 45696*B2) / 4570.         (25)
```

If `B2=0`, (23)-(24) reduce to the pure centered threshold

```text
13600*ell2 < 2285
iff
2720*ell2 < 457,
```

as expected.  If `ell2=0`, they reduce to

```text
45696*B2 < 2285,
```

which is exactly the `mu=0` additive quarter-barrier threshold from `T-P5-019`/`T-P5-020`.

---

## 6. Common physical-margin corollary

`T-P5-020` also records the common position/velocity margin barrier

```text
17823 * (1-mu)^2 * sigma^2 > 3716608 * B2.            (26)
```

Since `17823 = 39*457`, the centered inequality can be put over the same denominator with

```text
D_sigma := 17823 * sigma^2,
X_sigma := 106080 * ell2 * sigma^2,
Y_sigma := 3716608 * B2.                              (27)
```

Define

```text
C_sigma
 := 17823*sigma^2
    - 106080*ell2*sigma^2
    - 3716608*B2.                                     (28)
```

For `sigma^2>0`, a strict split exists if

```text
C_sigma > 0,                                          (29)
C_sigma^2
  > 1577031106560 * ell2 * sigma^2 * B2.              (30)
```

where

```text
1577031106560 = 4 * 106080 * 3716608.
```

The canonical rational witness is

```text
mu_sigma
 = (17823*sigma^2
    +106080*ell2*sigma^2
    -3716608*B2)
   /(35646*sigma^2).                                  (31)
```

Again, no square root appears in the checker-facing statement.

---

## 7. Exact failure boundary

The discriminant form separates two different obstructions that a scalar `mu` search can hide.

### 7.1 Linear headroom failure

If

```text
C = D-X-Y <= 0,
```

then even the squared centered and anchor fractions already consume at least the whole unit budget.  No `mu in [0,1)` can satisfy both branches.

### 7.2 Cross/tangency failure

It is possible to have `C>0` but

```text
Delta <= 0.
```

Then the two square-root budgets touch or overlap.  At `Delta=0`, the limiting relation is

```text
sqrt(X/D) + sqrt(Y/D) = 1.
```

This gives at best tangency (`Vdot<=0` in the idealized scalar comparison), not the strict inward derivative required by the first-exit barrier.  Therefore the strict `Delta>0` is mathematically meaningful and should not be weakened silently to `>=0` when the consumer needs strict invariance.

### 7.3 Zero barrier

`Vstar=0` is outside this normalization because `D=2285 Vstar` must be positive.  The zero-energy/equilibrium case should use the pure centered contraction theorem directly, not this anchor-normalized first-exit interface.

---

## 8. Source/checker consequence

If a source lane eventually produces exact rationals

```text
ell2 = JF2   (or another certified centered squared gain),
B2           (nominal-anchor squared residual cap),
Vstar > 0,
```

it need not search a family of `mu` values.  It can compute exactly

```text
C_P5,
Delta_P5 := C_P5^2 - 621465600*ell2*Vstar*B2,
```

and accept this mathematical child only if

```text
C_P5 > 0,
Delta_P5 > 0.
```

It may then emit `mu_bal` from (20) as an exact rational witness for the existing `T-P5-020` theorem chain.  This also makes near-boundary failures interpretable: `C_P5<=0` is a first-order budget failure, whereas `C_P5>0` but `Delta_P5<=0` is a centered/anchor interaction (square-root tangency) failure.

This does **not** weaken the source boundary from `T-P5-020`: an affine positive-offset envelope still does not prove `ell2`; raw IEEE maps still need a genuine centered increment theorem or must stay in `B2`.

---

## 9. Suggested Lean theorem decomposition

The strongest reusable algebraic primitive is source-independent:

```lean
-- Strict, division-free balanced split.
theorem balanced_square_split
    (D X Y : ℝ)
    (hD : 0 < D)
    (hX : 0 <= X)
    (hY : 0 <= Y)
    (hC : 0 < D - X - Y)
    (hDelta : 4*X*Y < (D-X-Y)^2) :
    let mu := (D + X - Y) / (2*D)
    0 < mu /\
    mu < 1 /\
    X < D*mu^2 /\
    Y < D*(1-mu)^2 := by
  ...
```

The proof should use the two exact identities

```text
(D+X-Y)^2 - 4DX = (D-X-Y)^2 - 4XY,
(D-X+Y)^2 - 4DY = (D-X-Y)^2 - 4XY,
```

plus positivity of `D`, `C+2X`, and `C+2Y`.  This is a good `ring_nf` + `nlinarith` target and needs no `Real.sqrt`.

Then add thin arithmetic corollaries:

```lean
p5_centered_anchor_balanced_mu
p5_quarter_discriminant_barrier
p5_common_margin_discriminant_barrier
```

The formalization should remain an abstract exact-real sidecar; `ell2` and `B2` source binding stays outside it.

---

## 10. Integration boundary

This child sharpens the *consumer* interface only.  It does not establish any of:

- a same-domain Jacobian/Frobenius or centered increment bound for the deployed residual;
- a nominal-flowpipe bound for the anchor residual;
- Float64/solve/controller centered semantics;
- P8 flowpipe/domain coverage or continuation;
- P5/P8/M4 parent closure;
- registry admission.

Recommended downstream use: keep `T-P5-020` as the conceptual centered/anchor theorem, and optionally place this child in front of it as an exact rational parameter-elimination/checker theorem.  The source lane then needs to output only `(ell2,B2,Vstar)` plus the semantic evidence for those quantities.

**Status: pending.  待封不觉独立验证 / 待梁智炜收割与最终整合。**
