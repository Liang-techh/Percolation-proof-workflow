---
kind: review_result
review_id: review-T-P7-001-honglianmozun-20260906T2244
task_id: T-P7-001
source_agent: 红莲魔尊
created_at: 2026-09-06T22:44:00-06:00
inspected_commit: 95824f5ea8484961071a604f393535a170aa4da8
continuation_of: review-T-P7-001-honglianmozun-20260906T2140
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_tail_absorption_bridge_then_source_bind
---

# T-P7-001 — physical rational tail: exact Schur-absorption mathematics

## Scope

The coordinator has now resolved the previously ambiguous P7 task to the concrete target:

- external checker: `robot_final/verify_physical_rational_tail_global_bound.py`;
- external inputs: `routeB_dense_Mq/routeB_physical_rational_tail_cs_polynomial.csv`,
  `routeB_dense_Mq/routeB_physical_rational_tail_global_bound.csv`,
  `routeB_dense_Mq/routeB_Mq_M0.csv`;
- exact arithmetic child: `examples/routeb_p7_tail_bound_lean/`.

This continuation does not repeat the unique validator's provenance/admission work. It asks the mathematical question needed by the energy/Lyapunov lane:

> What does the checked scalar `eta < 1/160000` actually buy once it is connected to a quadratic tail/cross term, and what exact source hypotheses are still required before it can be consumed by P4/P5/M4?

## Repository evidence used

At the inspected commit:

- `examples/routeb_p7_tail_bound_lean/TailGlobalBound.lean`
  - git blob `1ee671a8023ed40d91ec295fe28df91304b5ea27`;
  - defines
    `eta = (inv00*u1^2 + 2*|inv01|*u1*u2 + inv11*u2^2)/rho0`;
  - proves `rho0_pos`, `eta01_lt_target`, `eta02_lt_target` with
    `target = 1/160000`.
- `examples/routeb_p7_tail_bound_lean/compile_receipt.json`
  - git blob `28b6af4a7db0452a4248a5f1dc344dcd4b5ff4a3`;
  - records external checker SHA-256
    `013ff73e1e85afc2657e23d322e681130cf6c2e5022fe988a3998d66839aa6cb`;
  - records checker result `PHYSICAL_RATIONAL_TAIL_GLOBAL_CHECK_OK` with seven
    factorization terms;
  - explicitly leaves `physical_source_binding=false`,
    `full_residual_absorption=false`, `global_coverage=false`.
- `examples/routeb_p7_tail_bound_lean/REPORT.md`
  - git blob `38c036d3859ab6401b8968d9f602e6e51e41351c`;
  - records the focused Lean arithmetic candidate and its evidence boundary.

No external source file is present in this repository snapshot, so this review does not assert that the CSV/checker variables have already been identified with the deployed trajectory variables.

## Exact numerical headroom

Independent exact-rational recomputation from the constants in
`TailGlobalBound.lean` gives, for orientation:

```text
qmax = 13/50:
  eta ≈ 1.544337926198776e-6
  eta / target ≈ 0.2470940682
  unused target fraction ≈ 75.2906%

qmax = 3/8:
  eta ≈ 4.763928213668212e-6
  eta / target ≈ 0.7622285142
  unused target fraction ≈ 23.7771%
```

Thus even the larger checked `qmax=3/8` case is not merely barely below the arithmetic threshold; it retains about 23.8% relative headroom inside `1/160000`. These decimals are explanatory only; the Lean child already proves the strict rational inequalities exactly.

## Main mathematical lemma: Schur-tail absorption

Let `A` be a real symmetric positive-definite 2x2 matrix, `u in R^2`, `s in R`, and `rho>0`. Define

```text
eta_exact := (u^T A^{-1} u) / rho.
```

Then for every `x in R^2` and every scalar `tau`, the exact completion identity is

```text
x^T A x + 2*s*u^T*x + rho*tau*s^2
 = (x + s*A^{-1}u)^T A (x + s*A^{-1}u)
   + rho*(tau - eta_exact)*s^2.                 (1)
```

Therefore, if

```text
tau >= eta_exact,
```

then

```text
x^T A x + 2*s*u^T*x + rho*tau*s^2 >= 0.        (2)
```

Equivalently, the cross/tail term obeys the absorption inequality

```text
-2*s*u^T*x <= x^T A x + rho*tau*s^2.            (3)
```

The threshold is sharp: choosing `x = -s*A^{-1}u` turns (1) into

```text
rho*(tau - eta_exact)*s^2.
```

Hence for nonzero `s`, no smaller `tau < eta_exact` can make the quadratic globally nonnegative. This is the exact mathematical meaning of an `eta`-type Schur threshold.

## Robust-box version matching the checked formula

Write

```text
A^{-1} = [[a,b],[b,d]],
```

with `a>=0`, `d>=0`. Suppose the physical/source layer proves

```text
|u_1| <= U1,
|u_2| <= U2.
```

Then

```text
u^T A^{-1} u
 = a*u_1^2 + 2*b*u_1*u_2 + d*u_2^2
 <= a*U1^2 + 2*|b|*U1*U2 + d*U2^2.              (4)
```

Consequently, if `rho >= rho0 > 0` and the inverse-block entries used by the source theorem are either exactly or safely bounded by the checked `inv00, inv01, inv11`, then the P7 scalar

```text
eta_bound :=
  (inv00*U1^2 + 2*|inv01|*U1*U2 + inv11*U2^2) / rho0
```

is a valid upper bound on `eta_exact`.

Combining (1)--(4) with the already checked

```text
eta_bound < 1/160000
```

gives a strict quadratic absorption certificate with the rational budget

```text
tau = 1/160000.
```

This is the highest-value reusable mathematical bridge from the current P7 arithmetic child.

## How P7 can join the energy / residual lane

Suppose a P4/P5 pointwise derivative or supply inequality has been reduced to

```text
E_dot <= S_core + T_tail,
```

where, after source normalization, the tail has the bilinear form

```text
T_tail = -2*s*u^T*x
```

and the same positive block contributes `-x^T A x` to the dissipative side. Then (3) yields

```text
E_dot <= S_core + rho*(1/160000)*s^2.             (5)
```

So P7 does **not** by itself produce a full residual norm, a trajectory bound, or a flowpipe. Its mathematically legitimate role is narrower and useful:

- it eliminates one coupled quadratic tail/cross term;
- it converts that term into an explicit scalar supply cost;
- downstream C3/C4 energy integration may consume that scalar cost together with the other residual channels exactly once.

If `s` is the ramp/disturbance channel and a separate theorem gives `s(t)=c*t` with `c^2<=3`, then over `t in [0,1]` the integrated P7 cost is bounded by

```text
integral_0^1 rho(t)*(1/160000)*s(t)^2 dt.
```

A constant upper bound `rho(t)<=rho_bar` would further imply

```text
<= rho_bar*(1/160000)*c^2/3
<= rho_bar/160000.                                 (6)
```

Equation (6) is conditional on an **upper** bound for the same physical `rho(t)` and on a proven identification of the P7 scalar variable `s` with the ramp channel; the existing P7 arithmetic child provides neither. If instead `rho` is a normalization divisor rather than a physical multiplier in the final quadratic, the source theorem must state the correct scaling explicitly before (5)/(6) are instantiated.

## Exact blocker to physical admission

The current compiled arithmetic does not yet establish the hypotheses needed for (4):

1. the deployed polynomial's two cross coefficients are the `u_1,u_2` bounded by the checked `u1_eta*`, `u2_eta*` values on the claimed q-domain;
2. the deployed positive 2x2 block is invertible/positive definite on that domain;
3. its inverse quadratic form is represented or safely dominated by the checked `inv00, |inv01|, inv11` constants;
4. its normalization scalar has the required sign and the precise relation to `rho0`;
5. the seven-term factorization covers the whole physical tail, with no omitted FD/round/solve/reference remainder being charged a second time elsewhere;
6. the resulting absorbed scalar term is connected to the same trajectory/domain/units as P4/P5 and the P8 flowpipe.

Until those are source-bound, the correct status remains `pending` even though the scalar arithmetic itself is strong.

## Recommended Lean formalization handoff

For 苏梦辰 / 臭屁猪, the smallest source-independent mathematical children are:

```text
schur_tail_completion_2x2
  A positive definite ->
  x^T A x + 2*s*u^T*x + rho*tau*s^2
    = completed_square + rho*(tau-eta_exact)*s^2
```

and

```text
robust_inverse_quadratic_bound_2x2
  |u1|<=U1, |u2|<=U2, a>=0, d>=0 ->
  a*u1^2 + 2*b*u1*u2 + d*u2^2
    <= a*U1^2 + 2*|b|*U1*U2 + d*U2^2.
```

A third corollary can instantiate `tau=1/160000` using
`RouteBP7Tail.eta01_lt_target` / `eta02_lt_target` once a typed source adapter supplies the exact correspondence.

## Commands / results boundary

No Lean/checker rerun was performed in this mathematical pass. The existing immutable receipt already records focused compilation and the external checker result; re-running those belongs to the unique validator. This pass independently recomputed the exact rational `eta` values from the checked constants and proved the source-independent completion/absorption argument above.

## Conclusion

`T-P7-001` now has a clear mathematical role rather than being only an arithmetic tail badge:

```text
checked eta < 1/160000
        + typed 2x2 source/Schur binding
        => rigorous absorption of one physical quadratic tail
        => explicit scalar cost for the energy/residual ledger.
```

The arithmetic child is reusable, and the `qmax=3/8` case still has material strict margin. The remaining blocker is not another scalar inequality; it is the typed source theorem establishing that the seven-term physical polynomial, its inverse block, `rho`, and the P4/P5 residual variables are exactly the objects appearing in the Schur completion. P7 must not be used as a substitute for P8 flowpipe/domain coverage or for the full C4 residual budget.
