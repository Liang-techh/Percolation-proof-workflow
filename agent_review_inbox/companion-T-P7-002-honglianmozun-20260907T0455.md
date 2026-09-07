---
kind: companion_log
task_id: T-P7-002
source_agent: 红莲魔尊
created_at: 2026-09-07T04:55:00-06:00
inspected_commit: 4030b35ae0ade996946dbbeea0901a1018bde297
continuation_of: review-T-P7-002-honglianmozun-20260907T0050
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_rho_free_direct_schur_cost_and_compare_with_M4_slack_then_source_bind_unnormalized_cross_covector
---

# T-P7-002 continuation — eliminate the normalization scalar from the energy charge

## Scope

The previous `T-P7-002` review proved the diagonal Schur completion through the normalized parameter

```text
eta = (u1^2/a + u2^2/d)/rho
```

and then used the fixed choice `tau=1/160000`, producing the downstream pointwise charge

```text
rho * tau * s^2.
```

That route creates a two-sided source seam: `rho>=rho0` is used to prove `eta<=tau`, while `rho<=rho_bar` is later used to budget the absorbed term.

This continuation observes that the normalization is algebraically auxiliary.  If the actual unnormalized cross covector `u` and positive block are already source-bound, the sharp Schur charge is the inverse quadratic itself, and `rho` cancels completely.  For the two already frozen P7 coefficient boxes this gives a tail cost far below the existing M4 residual slack and removes the need for a physical upper bound `rho<=16` from this bookkeeping route.

No deployed-source identification, Float64 equality, seven-term factorization binding, P8 coverage, provenance, admission, or registry claim is made.

## 1. The intrinsic Schur cost does not contain `rho`

Let `A` be positive definite, `u,x` vectors of compatible dimension, and `s` a scalar.  Define the intrinsic dual quadratic

```text
Q_A(u) := u^T A^{-1} u.
```

The exact completion is

```text
x^T A x + 2 s u^T x + Q_A(u) s^2
 = (x + s A^{-1}u)^T A (x + s A^{-1}u).              (1)
```

Hence

```text
-2 s u^T x <= x^T A x + Q_A(u) s^2.                  (2)
```

This coefficient is sharp for fixed `A,u`: choosing

```text
x = -s A^{-1}u
```

makes (1) an equality and shows that no smaller scalar coefficient than `Q_A(u)` can dominate the cross term for all `x` when `s!=0`.

The normalized theorem from the previous review is exactly the same identity written with

```text
eta = Q_A(u)/rho,
Q_A(u) = rho*eta.
```

At the sharp threshold `tau=eta`, the normalized energy payment is

```text
rho*tau*s^2 = Q_A(u)*s^2.                                  (3)
```

Therefore a source-independent energy theorem does not intrinsically need `rho`.  The scalar `rho` is needed only if one insists on certifying the sufficient fixed normalized threshold `eta<1/160000` before recovering a cost as `rho/160000`.

## 2. Robust diagonal bound using the already derived exact-real block

For the exact-real P7 block from `T-P3-010` / the previous `T-P7-002` review,

```text
A(q) = diag(m44(q5),m55),
m44(q5) >= a0 := 350003/3000000,
m55          = d0 := 200739/4000000.
```

For `|u1|<=U1`, `|u2|<=U2`,

```text
Q_A(u)
 = u1^2/m44(q5) + u2^2/m55
 <= U1^2/a0 + U2^2/d0
 =: Qbar(U1,U2).                                            (4)
```

Equivalently, with

```text
A0 = 3000000/350003,
D0 = 4000000/200739,
```

we have

```text
Qbar = A0*U1^2 + D0*U2^2.                                  (5)
```

Combining (2) and (4) yields the fully robust pointwise consumer

```text
-2 s (u1*x1+u2*x2)
 <= m44*x1^2 + m55*x2^2 + Qbar*s^2.                         (6)
```

No lower or upper bound on `rho` appears.

For the information set consisting only of independent lower bounds `a>=a0`, `d>=d0` and independent boxes `|ui|<=Ui`, the coefficient in (5) is also sharp: the abstract extremizer is `a=a0`, `d=d0`, `|ui|=Ui`.  This is an information-set sharpness statement, not a claim that the physical trajectory attains all extrema simultaneously.

## 3. Exact rational values for the two frozen P7 boxes

For the first box from `TailGlobalBound.lean`,

```text
U1_01 = 4557183030309 / 62500000000000000,
U2_01 = 68513 / 500000000,
```

exact evaluation gives

```text
Qbar_01
 = 115189604728130718929049301461377
   / 274450203972656250000000000000000000000
 ~= 4.19710399412227e-7.                                   (7)
```

For the second box,

```text
U1_02 = 6213654909 / 40960000000000,
U2_02 = 615204634373 / 2621440000000000,
```

exact evaluation gives

```text
Qbar_02
 = 4465066517112964865570193481
   / 3448699320153491374080000000000000
 ~= 1.29471029585561e-6.                                   (8)
```

Both satisfy the simple uniform rational cap

```text
Qbar_j < 13/10000000 = 1.3e-6.                             (9)
```

The decimal values above are explanatory only; (7)--(9) are exact rational statements and can be discharged by `norm_num` once the constants are unfolded.

## 4. P8 ramp integration: direct tail budget is at most `Qbar`

Suppose the already separate P8 ramp theorem supplies on `t in [0,1]`

```text
s(t)=c*t,
c^2<=3.
```

Using the pointwise direct charge `Qbar*s(t)^2`,

```text
D_tail
 := integral_0^1 Qbar*s(t)^2 dt
 = Qbar*c^2 * integral_0^1 t^2 dt
 = Qbar*c^2/3
 <= Qbar.                                                   (10)
```

Consequently either frozen P7 box gives

```text
D_tail < 13/10000000.                                      (11)
```

This is the same completion mathematics as the normalized route, but it avoids replacing the true inverse-quadratic coefficient by the much coarser fixed payment `rho/160000`.

For a general horizon `T>=0` with `s(t)=c*t`, the corresponding formula is

```text
D_tail <= Qbar*c^2*T^3/3.                                  (12)
```

## 5. Direct M4 budget transfer removes the `rho_bar<=16` gate

`T-M4-006` records

```text
D_old = 4483/2000,
D_new = 1401/625,
D_new-D_old = 1/10000.                                     (13)
```

The old normalized bookkeeping required

```text
D_tail <= rho_bar/160000
```

and therefore imposed `rho_bar<=16` to fit the `1/10000` slack.

Using (11) instead,

```text
D_base <= 4483/2000
```

implies

```text
D_base + D_tail
 < 4483/2000 + 13/10000000
 < 1401/625.                                                (14)
```

The remaining exact slack after the uniform direct P7 cap is

```text
1/10000 - 13/10000000
 = 987/10000000
 = 0.0000987.                                               (15)
```

So the direct P7 charge consumes at most 1.3% of the old-to-new M4 slack and leaves 98.7% unused.  With the exact larger-box value (8), the consumed fraction is only about 1.29471%.

Thus, **conditional on binding the unnormalized physical cross covector and the exact-real diagonal positive block**, the P7->M4 energy seam no longer needs either

```text
rho>=rho0
```

or

```text
rho<=16.
```

Those `rho` conditions remain relevant only for the historical normalized `eta<1/160000` presentation, not for the intrinsic completion theorem (6).

## 6. Failure boundary / what cannot be silently cancelled

The rho-free simplification is valid only if the `u` entering (4)--(6) is exactly the **unnormalized force/cross covector** in the physical bilinear term

```text
-2 s u^T x.
```

If the external checker instead reports a normalized vector `uhat` related by

```text
u = alpha(rho,q,...) * uhat,
```

then the actual intrinsic cost is

```text
Q_A(u) = alpha^2 * Q_A(uhat),                               (16)
```

and the scale factor must be carried explicitly.  One cannot delete `rho` merely because it disappears from the abstract completion algebra.

Similarly, (9) is a mathematical consequence of the frozen `U1,U2` constants only after a source adapter proves that those constants bound the same physical unnormalized cross coefficients on the same domain.  This continuation does not prove that identification.

The seven-term polynomial/no-double-counting issue is also unchanged: (6) consumes exactly one identified bilinear tail and must not absorb unrelated FD, IEEE, solve, controller, or reference residuals.

## 7. Lean-friendly theorem package

The smallest new source-independent child is simpler than the normalized theorem:

```lean
-- Exact diagonal direct-cost completion.
theorem diagonal_schur_direct_cost
    (a d x1 x2 u1 u2 s : ℝ)
    (ha : a != 0) (hd : d != 0) :
    a*x1^2 + d*x2^2
      + 2*s*(u1*x1+u2*x2)
      + (u1^2/a + u2^2/d)*s^2
      = a*(x1+s*u1/a)^2 + d*(x2+s*u2/d)^2
```

and the robust consumer

```lean
theorem diagonal_schur_direct_absorb
    (a d a0 d0 x1 x2 u1 u2 U1 U2 s : ℝ)
    (ha0 : 0<a0) (hd0 : 0<d0)
    (ha : a0<=a) (hd : d0<=d)
    (hU1 : 0<=U1) (hU2 : 0<=U2)
    (hu1 : |u1|<=U1) (hu2 : |u2|<=U2) :
    -2*s*(u1*x1+u2*x2)
      <= a*x1^2 + d*x2^2 + (U1^2/a0+U2^2/d0)*s^2
```

followed by exact rational corollaries

```lean
theorem qbar01_lt_uniform : Qbar01 < 13/10000000
theorem qbar02_lt_uniform : Qbar02 < 13/10000000
```

and the pure arithmetic M4 consumer

```lean
theorem old_gate_plus_direct_tail
    (Dbase Dtail : ℝ)
    (hbase : Dbase <= 4483/2000)
    (htail : Dtail <= 13/10000000) :
    Dbase + Dtail < 1401/625
```

The integral/ramp theorem can stay separate, as in `T-M4-006`, to avoid entangling the algebraic child with Mathlib's interval-integral API.

## 8. Recommended integration decision

Prefer the direct-cost seam whenever source binding can expose the actual unnormalized `u` and exact-real positive block:

```text
physical cross covector + positive block
  -> Q_A(u) bound
  -> sharp Schur cost Qbar*s^2
  -> P8 ramp integration D_tail<=Qbar
  -> M4 residual ledger.
```

Keep the historical normalized seam only as a fallback:

```text
eta<=1/160000 + rho upper bound
  -> rho/160000*s^2
  -> M4 ledger.
```

The direct seam is strictly stronger for the currently frozen P7 boxes and removes a source obligation (`rho_bar<=16`) rather than merely tightening its constant.

## Remaining blockers

1. Bind the frozen `U1,U2` boxes to the **unnormalized** deployed P7 cross coefficients.
2. Bind the positive block to the exact-real diagonal `M_BB` slice on the same covered domain.
3. Bind `s` to the P8 ramp coordinate on that same trajectory/domain.
4. Prove seven-term factorization/no-double-counting at the source interface.
5. Retain independent P8 existence/coverage and M4 base-residual premises.

This result remains `pending`.  It is a source-independent energy simplification only; it does not close P7, P8, M4, or the registry.
