---
kind: review_result
review_id: review-T-P5-042-guyuefangyuan-20260907T2041
task_id: T-P5-042
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-07T20:26:00-06:00
created_at: 2026-09-07T20:41:00-06:00
claim_commit: 81229a80095bd9df52344f006f62bd0622d96da8
inspected_commit: 47a4fc8863bc829116a786f37eed10f1ce9383d0
inspected_paths:
  - agent_review_inbox/README.md
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/collaboration_board.md
  - agent_review_inbox/review-T-P5-040-honglianmozun-20260907T1950.md
  - agent_review_inbox/review-T-P5-041-liuguanyi-20260907T2020.md
  - agent_review_inbox/companion-T-P5-041-liuguanyi-20260907T2023.md
continuation_of:
  - review-T-P5-039-guyuefangyuan-20260907T1931
  - review-T-P5-040-honglianmozun-20260907T1950
  - review-T-P5-041-liuguanyi-20260907T2020
related_tasks:
  - T-P5-022
  - T-P5-028
  - T-P5-039
  - T-P5-040
  - T-P5-041
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_the_scale_free_centered_residual_decay_and_the_square_root_free_channel_budget_elimination; source_lane_should_emit_signed_ux_rows_or_Kpath_fallback_and_test_the_exact_branch_conditions_before_searching_rho
---

# T-P5-042 — scale-free centered residual closure and exact rational elimination of `rho`

## 0. Result

T-P5-041 exposes the correct source-side mixed row in the energy coordinates

```text
u := x+y,
V = (1/2) u^T M u + (1/2) x^T H x,
```

and, for one residual channel, allows a split

```text
|l_i| <= rho_i*|u_i| + beta_i,
beta_i^2 <= 2 V * C_i(rho_i).
```

T-P5-040 then uniformizes the second line on `V<=Vstar` into an additive square budget.  That is safe, but for the **centered/state-homogeneous** part it throws away useful scaling: `beta_i^2` is already proportional to the current `V`, not merely to `Vstar`.

Keeping that pointwise factor gives the stronger consumer

```text
V' <= -[ c - C4(rho4)/(2*(a4-rho4))
           - C5(rho5)/(2*(a5-rho5)) ] * V.              (0.1)
```

Thus the exact centered-residual strict-decay gate is

```text
C4(rho4)/(a4-rho4) + C5(rho5)/(a5-rho5) < 2*c.         (0.2)
```

For the current Pareto family

```text
c(r)  = (109-r)/200,
a4(r) = (250+53*r)/1500,
a5    = 1/6,
```

this is

```text
g4(rho4) + g5(rho5) < (109-r)/100.                     (0.3)
```

Unlike the `Vstar`-uniformized additive statement, (0.1) has **no additive ultimate floor**.  On any domain where the source row and energy identity remain valid, it is a genuine multiplicative decay estimate.  At a first-exit boundary it gives exactly the same feasibility condition that one gets by substituting the T-P5-041 budget `B_i=2 Vstar C_i` into T-P5-040, so this is a sharper composition/conclusion, not an inconsistent replacement.

The second result is an exact solution of the `rho` tradeoff that T-P5-041 deliberately left open.  For one channel define

```text
a > 0             energy reserve,
m > 0             corresponding diagonal entry of M,
R >= 0            coefficient of |u_i| in the source row,
C >= 0            all rho-independent dual-energy cost,
0 <= rho <= R,
rho < a,

g(rho) := [ (R-rho)^2/m + C ] / (a-rho).               (0.4)
```

Then:

1. `rho=0` is globally optimal exactly when

```text
m*C >= R*(2*a-R).                                       (0.5)
```

In particular, if `R>=2a`, **no positive relative charge can improve the certificate**.

2. If

```text
m*C < R*(2*a-R),                                        (0.6)
```

then a positive mixed split is useful.  Except for the harmless limiting case `R=a,C=0`, the exact minimizer is

```text
rho* = a - sqrt((a-R)^2 + m*C),                         (0.7)
```

with

```text
g* = (2/m) * [sqrt((a-R)^2+m*C) - (a-R)].              (0.8)
```

3. More importantly for a rational checker/Lean theorem, one never needs to compute that square root.  Given a requested rational channel budget `ell>0`, existence of an admissible `rho` with

```text
g(rho) < ell                                            (0.9)
```

has the following exact two-branch rational characterization.

### Vertex branch

If

```text
m*ell <= 2*R,
m*ell + 2*(a-R) > 0,                                   (0.10)
```

then (0.9) holds iff

```text
4*C < 4*(a-R)*ell + m*ell^2.                            (0.11)
```

A canonical rational witness is

```text
rho_ell := R - m*ell/2.                                 (0.12)
```

### Endpoint branch

If

```text
2*R < m*ell,                                            (0.13)
```

then (0.9) holds iff

```text
R^2 + m*C < m*a*ell,                                    (0.14)
```

and the canonical witness is simply

```text
rho_ell := 0.                                           (0.15)
```

Therefore the source/checker interface can eliminate `rho` entirely.  It may choose rational `ell4,ell5`, verify one exact branch per channel, construct `rho_i` deterministically, and finally check

```text
ell4 + ell5 < (109-r)/100.                              (0.16)
```

The resulting certified decay rate is at least

```text
kappa = (109-r)/200 - (ell4+ell5)/2 > 0.                (0.17)
```

This is fully square-root-free and division-free after positive denominators are cleared.

---

## 1. Why the pointwise T-P5-041 budget gives multiplicative decay

Use the exact Pareto energy certificate

```text
Q >= c*V + a4*u4^2 + a5*u5^2                           (1.1)
```

and the moving-frame power identity

```text
V' = -Q - u4*l4 - u5*l5.                               (1.2)
```

Suppose for each channel

```text
|l_i| <= rho_i*|u_i| + beta_i,
beta_i^2 <= 2*V*C_i,
0 <= rho_i < a_i.                                       (1.3)
```

Set

```text
t_i := a_i-rho_i > 0.                                  (1.4)
```

Then

```text
-u_i*l_i
 <= |u_i|*|l_i|
 <= rho_i*u_i^2 + beta_i*|u_i|.                         (1.5)
```

Hence

```text
V'
 <= -c*V
    -t4*u4^2 + beta4*|u4|
    -t5*u5^2 + beta5*|u5|.                              (1.6)
```

For each channel the exact square identity gives

```text
-t*u^2 + beta*|u|
 = beta^2/(4*t) - t*(|u|-beta/(2*t))^2
 <= beta^2/(4*t)
 <= [C/(2*t)]*V.                                        (1.7)
```

Summing proves (0.1).

This is the mathematically natural consumer for the **centered** T-P5-041 row.  If the real full residual has a state-independent anchor/Float64/solve bias, that bias does not satisfy `beta^2 <= 2VC` as `V->0` and must remain in the additive T-P5-040 lane (or use a separate reserve split).  This review does not erase that boundary.

---

## 2. Specialization of `C_i(rho_i)` to the T-P5-041 source row

For the residual row targeting channel `i`, T-P5-041 writes

```text
|l_i|
 <= R_i*|u_i| + R_j*|u_j| + T4*|x4| + T5*|x5|.         (2.1)
```

After choosing `0<=rho_i<=R_i`, its energy-dual bound has

```text
C_i(rho_i)
 = (R_i-rho_i)^2/m_i + Cperp_i,                         (2.2)
```

where

```text
Cperp_i
 := R_j^2/m_j + T^T H^{-1} T >= 0.                     (2.3)
```

The exact rational `H^{-1}` is already given in T-P5-041, so `Cperp_i` is rational whenever the source row is rational.

Thus the only source-independent optimizer is precisely (0.4) with

```text
R := R_i,
C := Cperp_i,
a := a_i,
m := m_i.                                              (2.4)
```

This also clarifies a subtlety in T-P5-041 Section 7: `C_i(rho)` itself decreases monotonically as `rho` increases, but the **consumed** quantity is

```text
C_i(rho)/(a_i-rho).                                     (2.5)
```

The denominator reserve shrinks at the same time.  Therefore “push rho as large as possible” is generally wrong; (0.5)-(0.8) give the exact balance.

---

## 3. Exact optimization of one channel

Set

```text
s := R-rho,
d := a-R.                                              (3.1)
```

Then

```text
a-rho = s+d > 0,

g = (s^2/m + C)/(s+d).                                 (3.2)
```

Differentiate with respect to `s` only as a derivation aid:

```text
dg/ds
 = [s^2 + 2*d*s - m*C] / [m*(s+d)^2].                  (3.3)
```

Define

```text
F(s) := s^2 + 2*d*s - m*C.                             (3.4)
```

On the admissible domain,

```text
F'(s)=2*(s+d)=2*(a-rho)>0,                              (3.5)
```

so `F` is strictly increasing.  At the `rho=0` endpoint, `s=R` and

```text
F(R)
 = R^2 + 2*(a-R)*R - m*C
 = R*(2*a-R) - m*C.                                    (3.6)
```

Therefore:

- if `F(R)<=0`, then `F(s)<=0` everywhere admissible, so `g` decreases as `s` increases and `rho=0` is the global minimizer;
- if `F(R)>0`, `F` crosses zero once before the `rho=0` endpoint and the mixed split is strictly better.

This proves (0.5)-(0.6).

Solving `F(s)=0` gives the positive admissible root

```text
s* = sqrt(d^2+m*C)-d,                                  (3.7)
```

hence

```text
rho* = R-s* = a-sqrt((a-R)^2+m*C).                     (3.8)
```

At the critical point, `m*C=s*^2+2*d*s*`, so

```text
g*
 = [s*^2/m+C]/(s*+d)
 = 2*s*/m,                                              (3.9)
```

which proves (0.8).

The only non-attained endpoint case under the strict reserve convention is

```text
R=a, C=0.                                               (3.10)
```

Then `inf g=0` as `rho -> a^-`; every strict rational budget `ell>0` still has an admissible rational witness via Section 4, so no checker completeness is lost.

A useful immediate obstruction is

```text
R >= 2*a  ==>  R*(2*a-R) <= 0 <= m*C,
```

hence `rho=0` is automatically optimal.  If a concrete source row lands in this regime, tuning the mixed split cannot rescue it; the row itself or the energy certificate must improve.

---

## 4. Square-root-free exact budget elimination

Fix a requested `ell>0`.  In the `s` coordinate,

```text
g(rho) < ell
```

is equivalent, because `m>0` and `s+d>0`, to

```text
Phi_ell(s) < 0,                                        (4.1)
```

where

```text
Phi_ell(s)
 := s^2 - m*ell*s + m*(C-d*ell).                       (4.2)
```

This is a convex quadratic with vertex

```text
s0 = m*ell/2.                                           (4.3)
```

### 4.1 Vertex lies in the admissible interval

The conditions

```text
m*ell <= 2*R,
m*ell + 2*d > 0                                        (4.4)
```

are exactly

```text
s0 <= R,
s0+d > 0.                                              (4.5)
```

Since `ell>0`, `s0>=0`; therefore `rho_ell=R-s0` obeys

```text
0 <= rho_ell <= R,
rho_ell < a.                                            (4.6)
```

At the vertex,

```text
Phi_ell(s0)
 = (m/4) * [4*C - 4*d*ell - m*ell^2].                  (4.7)
```

Thus an admissible `rho` with `g<ell` exists iff (0.11) holds, and the rational witness is (0.12).

### 4.2 Vertex lies to the right of the admissible interval

If

```text
2*R < m*ell,                                            (4.8)
```

then `Phi_ell` is decreasing throughout the admissible interval, so its minimum occurs at `s=R`, i.e. `rho=0`.  Direct substitution gives

```text
Phi_ell(R)
 = R^2 + m*C - m*a*ell.                                (4.9)
```

Hence existence is equivalent to (0.14), with witness `rho=0`.

### 4.3 Why there is no missing third branch

If the vertex is at or left of the strict-reserve lower boundary, then

```text
s0+d <= 0.                                              (4.10)
```

At the boundary `s=-d`,

```text
Phi_ell(-d) = d^2 + m*C >= 0.                           (4.11)
```

and `Phi_ell` is increasing on the admissible side.  Therefore no admissible `rho` can satisfy `g<ell` there.  This proves that the vertex and endpoint branches above are exhaustive.

So (0.10)-(0.15) are an exact iff, not merely a sufficient search heuristic.

---

## 5. Two-channel rational checker for the current Pareto family

Fix one rational Pareto parameter

```text
0 <= r <= 1.                                            (5.1)
```

Set

```text
c  := (109-r)/200,
a4 := (250+53*r)/1500,
a5 := 1/6.                                              (5.2)
```

For the two source rows compute exact rational quadruples

```text
(m4,R4,Cperp4,a4),
(m5,R5,Cperp5,a5).                                      (5.3)
```

Choose positive rational channel budgets `ell4,ell5`.  For each channel run exactly one of the Section 4 branches.  If both pass and

```text
ell4 + ell5 < (109-r)/100,                              (5.4)
```

then the constructed rational `rho4,rho5` satisfy

```text
g4(rho4) < ell4,
g5(rho5) < ell5.                                       (5.5)
```

Therefore (0.1) yields the explicit strict decay certificate

```text
V' <= -kappa*V,

kappa := (109-r)/200 - (ell4+ell5)/2 > 0.               (5.6)
```

This checker path uses only rational additions, multiplications, order tests and division by the literal `2` in the constructed witness.  No numerical eigensolver, square root, floating optimizer or `rho` grid is needed.

Because the target inequality is strict, if a real optimal pair has positive slack then rational `ell4,ell5` can be chosen with the same slack.  Thus the rational-budget representation does not lose strict feasibility; it merely exposes the witness in a kernel-friendly form.

---

## 6. Exact rational regression: `rho=0` fails but mixed split proves strong decay

This is a source-independent regression example using the actual frozen channel-4 mass and the `r=0` Pareto endpoint:

```text
r = 0,
c = 109/200,
a4 = 1/6,
m4 = 350003/3000000.
```

Take one abstract centered residual row with

```text
R = 3/20,
C = 1/100,                                              (6.1)
```

and no channel-5 residual.

### Pure-additive / `rho=0` route fails

The consumed channel ratio is

```text
g(0)
 = [R^2/m4 + C]/a4
 = 21300009/17500150.                                   (6.2)
```

But

```text
2*c = 109/100,

g(0)-2*c = 4449691/35000300 > 0.                       (6.3)
```

So the zero-relative specialization cannot certify inwardness/decay.

### Rational mixed witness succeeds

Choose the requested rational channel budget

```text
ell = 3/8.                                              (6.4)
```

Then

```text
m4*ell = 350003/8000000 <= 3/10 = 2*R,

m4*ell + 2*(a4-R) > 0,                                  (6.5)
```

and the exact vertex inequality has slack

```text
4*(a4-R)*ell + m4*ell^2 - 4*C
 = 90009/64000000 > 0.                                  (6.6)
```

Therefore Section 4 constructs

```text
rho_ell
 = R - m4*ell/2
 = 2049997/16000000.                                    (6.7)
```

The resulting exact ratio is

```text
g(rho_ell)
 = 10830027/29600144
 < 3/8.                                                 (6.8)
```

Since

```text
3/8 < 109/100 = 2*c,                                   (6.9)
```

we obtain the explicit decay margin

```text
kappa >= c - ell/2
       = 109/200 - 3/16
       = 143/400 > 0.                                   (6.10)
```

Thus the mixed optimizer is not a cosmetic reparameterization: there are exact rational rows for which the `rho=0` consumer fails while a deterministic rational mixed witness gives a large strict decay margin.

This example is only a mathematical regression; it is not asserted to be a deployed source row.

---

## 7. Recommended Lean theorem decomposition

The proof can stay source-independent and very small.

### `centered_mixed_channel_absorption`

Assume

```text
0 < t,
beta^2 <= 2*V*C.
```

Prove

```text
-t*u^2 + beta*abs(u) <= (C/(2*t))*V.
```

A division-free version multiplies by `4*t` and uses

```text
0 <= (2*t*abs(u)-beta)^2.
```

### `block45_centered_mixed_decay`

Consume the Pareto `Q` certificate, the power identity and two channel absorption premises; prove (0.1)/(5.6).

### `rho_zero_optimal_iff`

For `a,m>0`, `R,C>=0`, prove that `rho=0` minimizes (0.4) on the admissible interval whenever

```text
m*C >= R*(2*a-R),
```

and prove strict improvement is possible under the reversed strict inequality.

This theorem can be proved algebraically from the monotonic sign polynomial `F(s)`; no derivative API is required in Lean.

### `channel_budget_vertex_constructive`

From (0.10)-(0.11), define

```text
rho := R-m*ell/2
```

and prove `0<=rho<=R`, `rho<a`, `g(rho)<ell` after clearing positive denominators.

### `channel_budget_endpoint_constructive`

From (0.13)-(0.14), prove `g(0)<ell`.

### `channel_budget_iff`

Optional stronger theorem: combine the convex quadratic argument to prove the exact two-branch iff of Section 4.

### `block45_rational_channel_budget_decay`

Consume two successful channel-budget witnesses plus (5.4), and prove (5.6).

The regression in Section 6 should be a separate exact-arithmetic theorem to prevent future refactors from collapsing back to `rho=0` by default.

---

## 8. Assumptions, dependencies and remaining obstruction

Mathematical dependencies:

- T-P5-037/T-P5-036 convex Pareto family for `c,a4,a5`;
- T-P5-040 exact relative-plus-additive channel completion;
- T-P5-041 exact `(u,x)` storage diagonalization and energy-dual row budget.

This review deliberately does **not** consume or verify:

- a real deployed signed Jacobian / `K_path` row;
- Julia/Float64, finite-difference, controller or linear-solve semantics;
- a state-independent anchor bias (such a bias must remain additive and cannot be hidden inside `beta^2<=2VC`);
- P8 flowpipe/domain coverage or ODE continuation;
- Lean compilation, `#print axioms`, comparator/provenance receipts;
- P5/P8/M4 admission or registry promotion.

The next source-facing decision is now exact.  Given a real transformed row, first compute `R,Cperp`; test

```text
m*Cperp >= R*(2*a-R).
```

If it passes, stop searching `rho`: `rho=0` is already optimal.  If it fails, use the rational `ell` branch test rather than a `rho` grid.  If no pair of channel budgets can satisfy (5.4), the obstruction is genuinely in the source row / energy reserve and the lane should switch to a tighter signed-Jacobian, correlated-matrix/SPN, or source partition argument.

**Status: pending mathematical child — 待封不觉独立验证 / 待梁智炜最终整合。**
