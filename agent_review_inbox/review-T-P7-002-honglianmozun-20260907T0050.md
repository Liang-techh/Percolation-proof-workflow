---
kind: review_result
review_id: review-T-P7-002-honglianmozun-20260907T0050
task_id: T-P7-002
source_agent: 红莲魔尊
claimed_at: 2026-09-07T00:45:00-06:00
created_at: 2026-09-07T00:50:00-06:00
inspected_commit: abef65742bf8f9d4b1230468376fd7d44e6d6045
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_diagonal_schur_completion_and_bind_same_physical_rho_two_sided
---

# T-P7-002 — diagonal block-(4,5) Schur completion and the exact two-sided `rho` seam

## Scope

This pass completes the source-independent mathematics requested by `T-P7-002`, but uses the newly available exact-real block-(4,5) formula from
`review-T-P3-010-guyuefangyuan-20260907T0035.md` to remove unnecessary generic 2x2 inverse machinery from the P7 mathematical lane.

Inputs inspected:

- `review-T-P3-010-guyuefangyuan-20260907T0035.md`:
  exact-real regularized block
  `M_BB(q)=diag(m44(q5),m55)` with global lower bounds;
- `examples/routeb_p7_tail_bound_lean/TailGlobalBound.lean`:
  `rho0`, `target=1/160000`, two checked `(U1,U2)` pairs, and historical
  `inv00,inv01,inv11` arithmetic constants;
- `review-T-P7-001-honglianmozun-20260906T2244.md`:
  completion-of-square interpretation of the checked P7 `eta` threshold;
- `review-T-M4-006-daai-xianzun-20260906T2346.md`:
  downstream terminal budget `D_tail <= rho_bar/160000`, with the old C4 gate
  permitting `rho_bar <= 16`.

No Float64/source semantic equality, physical variable identification, coverage,
receipt, provenance, admission, or registry claim is made.

## 1. The new block formula makes the Schur inverse exact and diagonal

From T-P3-010, in exact-real regularized semantics,

```text
m44(q5) = 350003/3000000 + (147/800000) sin(q5)^2,
m55     = 200739/4000000,
M_BB(q) = diag(m44(q5),m55).
```

Hence for every real `q5`,

```text
m44(q5) >= a0 := 350003/3000000 > 0,
m55          = d0 := 200739/4000000 > 0.
```

Therefore

```text
M_BB(q)^(-1)
  = diag(1/m44(q5), 1/m55),
```

and the global safe inverse-entry bounds are exactly

```text
1/m44(q5) <= A0 := 3000000/350003,
1/m55      = D0 := 4000000/200739,
offdiag inverse = 0.                                      (1)
```

No eigenvalue solver, determinant enclosure, or generic 2x2 inverse estimate is needed for this block.

## 2. Robust inverse-quadratic bound

Let `u=(u1,u2)` and suppose

```text
|u1| <= U1,
|u2| <= U2,
U1,U2 >= 0.
```

Then from (1),

```text
u^T M_BB(q)^(-1) u
 = u1^2/m44(q5) + u2^2/m55
 <= A0*U1^2 + D0*U2^2.                                 (2)
```

This is the exact source-independent robust-box theorem P7 needs once the physical positive block is identified with the exact-real `M_BB` block.

If the physical normalization satisfies

```text
rho >= rho0 > 0,
```

then

```text
eta_exact(q,u,rho)
 := [u^T M_BB(q)^(-1) u]/rho
 <= [A0*U1^2 + D0*U2^2]/rho0
 =: eta_safe(U1,U2).                                  (3)
```

The proof uses only positivity and monotonicity of reciprocal/division.

## 3. The two P7 boxes remain strictly below `1/160000`

Using the exact constants already frozen in `TailGlobalBound.lean`, define

```text
rho0 = 10616159325566083327957 / 39062500000000000000000,
A0   = 3000000/350003,
D0   = 4000000/200739.
```

For the first checked pair

```text
U1 = 4557183030309 / 62500000000000000,
U2 = 68513 / 500000000,
```

exact rational evaluation gives

```text
eta_safe_01 ~= 1.544337926198738e-6
eta_safe_01 / (1/160000) ~= 0.2470940682 < 1.          (4)
```

For the second pair

```text
U1 = 6213654909 / 40960000000000,
U2 = 615204634373 / 2621440000000000,
```

exact rational evaluation gives

```text
eta_safe_02 ~= 4.763928213668077e-6
eta_safe_02 / (1/160000) ~= 0.7622285142 < 1.          (5)
```

Thus both exact-real diagonal-block cases retain the same substantial strict
headroom as the earlier arithmetic P7 child. The second case still uses only
about 76.23% of the target.

These are rational inequalities after the `(U1,U2,rho0,A0,D0)` definitions are expanded, so a future Lean child can discharge them with `norm_num`; no trigonometric reasoning remains in this final step.

## 4. Exact diagonal Schur completion

For positive `a,d,rho`, arbitrary reals `x1,x2,u1,u2,s,tau`, define

```text
eta = (u1^2/a + u2^2/d)/rho.
```

Then the following identity is exact:

```text
a*x1^2 + d*x2^2
+ 2*s*(u1*x1 + u2*x2)
+ rho*tau*s^2

= a*(x1 + s*u1/a)^2
+ d*(x2 + s*u2/d)^2
+ rho*(tau-eta)*s^2.                                  (6)
```

Therefore if `tau >= eta`, the left-hand side is nonnegative. Equivalently,

```text
-2*s*(u1*x1+u2*x2)
 <= a*x1^2 + d*x2^2 + rho*tau*s^2.                   (7)
```

The threshold is sharp: take

```text
x1 = -s*u1/a,
x2 = -s*u2/d.
```

Then the completed squares vanish, leaving exactly
`rho*(tau-eta)*s^2`. For nonzero `s`, no smaller `tau<eta` can work globally.

Combining (3)--(5) with `tau=1/160000` yields the desired conditional P7 tail absorption theorem for either checked `(U1,U2)` box.

## 5. Important correction: the historical `inv00` is not a generic coefficientwise upper bound for this exact-real block

The current P7 arithmetic file contains a historical rational `inv00` approximately

```text
8.571355102670523.
```

But the exact-real global mass-block inverse bound from T-P3-010 is

```text
A0 = 3000000/350003 ~= 8.571355102670548.
```

In fact, exactly,

```text
A0 - inv00
= 5974374999999999996652321913701217162334355777000000
  / 243957827913757155349724374999999609434208920389036822837175005777
> 0.                                                       (8)
```

So one must **not** reinterpret the historical `inv00` as a coefficientwise
upper bound on the exact-real `M_BB(q)^(-1)` for all `q`. The failure is tiny
(~`2.45e-14`) but logically real; at `q5=0,u2=0` it is enough to break such a generic claim.

The old arithmetic `eta` inequalities remain valid as statements about their own frozen constants. Moreover, for the two concrete P7 `(U1,U2)` pairs, the new safe diagonal formula (2) is actually slightly *smaller* than the old expression because the exact inverse off-diagonal is zero. Thus replacing the historical inverse constants by `(A0,0,D0)` is both logically safer and still comfortably below the target.

This is a useful fail-closed distinction: scalar arithmetic success does not automatically identify those historical inverse constants with the newly derived physical mass block.

## 6. The exact cross-branch interface is a two-sided bound on the same `rho`

The completion theorem uses `rho` in the denominator of `eta`, so P7 requires a **lower** bound

```text
rho(t) >= rho0 ~= 0.2717736787.                         (9)
```

But after absorption, the energy ledger pays

```text
rho(t) * (1/160000) * s(t)^2,
```

so M4/P8 budgeting requires an **upper** bound

```text
rho(t) <= rho_bar.                                      (10)
```

The M4-006 old-gate transfer says `rho_bar<=16` is sufficient for the terminal
budget. Therefore the smallest physically meaningful adapter joining P7 to the
existing M4 seam is not merely `rho>0`; it is the same-domain two-sided contract

```text
rho0 <= rho(t) <= 16                                    (11)
```

for the **same physical normalization scalar** appearing in both the P7 Schur
completion and downstream energy cost.

This sharply identifies the next source-math task: prove (11), together with the
identification of the P7 cross coefficients `u1,u2` and positive block, on the
same covered trajectory/domain. If the source `rho` is a different normalization
object from the energy multiplier, a scale-conversion theorem is required; the
symbols cannot be silently reused.

## 7. Lean-friendly theorem package

Recommended formalization decomposition:

```lean
-- Generic diagonal completion, no repository constants.
theorem diagonal_schur_completion
    (a d rho tau x1 x2 u1 u2 s : ℝ)
    (ha : a ≠ 0) (hd : d ≠ 0) :
    a*x1^2 + d*x2^2 + 2*s*(u1*x1+u2*x2) + rho*tau*s^2
      = a*(x1+s*u1/a)^2 + d*(x2+s*u2/d)^2
        + rho*(tau-(u1^2/a+u2^2/d)/rho)*s^2
```

with `rho≠0` added if `eta` is unfolded inside the identity.

```lean
-- Robust inverse box estimate.
theorem diagonal_inverse_quadratic_bound
    (a d a0 d0 u1 u2 U1 U2 : ℝ)
    (ha0 : 0 < a0) (hd0 : 0 < d0)
    (ha : a0 <= a) (hd : d0 <= d)
    (hU1 : 0 <= U1) (hU2 : 0 <= U2)
    (hu1 : |u1| <= U1) (hu2 : |u2| <= U2) :
    u1^2/a + u2^2/d <= U1^2/a0 + U2^2/d0
```

```lean
-- Concrete exact-real P7 scalar children.
theorem eta_safe_01_lt_target :
  (A0*U1_01^2 + D0*U2_01^2)/rho0 < 1/160000

theorem eta_safe_02_lt_target :
  (A0*U1_02^2 + D0*U2_02^2)/rho0 < 1/160000
```

and then a typed consumer:

```text
rho0 <= rho <= rho_bar,
rho_bar <= 16,
|u1|<=U1_j, |u2|<=U2_j,
M_BB = diag(m44,m55),
m44>=a0, m55=d0
--------------------------------------
P7 cross term absorbed with tau=1/160000,
and its downstream scalar cost fits the M4-006 old-gate tail budget.
```

The final combined theorem should remain conditional on the source adapter; it
must not embed source identification as a definition.

## What remains open

- Float64/deployed-source equality to the exact-real block formula remains open.
- The P7 checker variables `u1,u2,rho` are not yet identified with deployed
  trajectory variables.
- The same physical `rho` has not yet been proved to satisfy the two-sided
  interval (11).
- The seven-term physical polynomial still needs a no-double-counting typed
  factorization into the cross term consumed by (7).
- P8 flowpipe/domain coverage remains independent.

## Recommended next action

1. Formalization lane: implement (6), the robust diagonal bound, and the two exact
   `eta_safe < 1/160000` rational corollaries as a tiny portable Lean sidecar.
2. P7/P3 source lane: bind the physical positive block to the exact-real diagonal
   block slice and prove the same-domain two-sided `rho0 <= rho <= 16` contract.
3. Do not reuse the historical `inv00` as a generic physical inverse upper bound;
   either keep it arithmetic-only or replace the physical adapter constants by
   the safe exact-real `(A0,0,D0)` package above.

This result remains `pending`: it is a mathematical bridge, not physical P7/M4 closure.
