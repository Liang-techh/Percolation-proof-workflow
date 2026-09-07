---
kind: review_result
review_id: review-T-M4-008-daai-xianzun-20260907T0102
task_id: T-M4-008
source_agent: 大爱仙尊
claimed_at: 2026-09-07T00:53:00-06:00
created_at: 2026-09-07T01:02:00-06:00
inspected_commit: b58f3dec5e1185e686344d858d2a48b49fed069d
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: formalize_weighted_rho_moment_then_bind_same_domain
---

# T-M4-008 — the P7 × P8 × M4 seam only needs a weighted rho moment

## Scope

`T-M4-006` composed the conditional P7 tail charge, the P8 ramp `s(t)=c t`, and the widened M4 terminal gate by using the sufficient pointwise condition `rho(t) <= rhoBar`; at the old C4 gate this produced the convenient target `rhoBar <= 16`.

`T-P7-002` then showed that P7 itself needs the same physical normalization scalar bounded below by `rho0`, while the downstream bookkeeping seemed to ask for the pointwise upper bound `rho <= 16`.

This review sharpens that cross-branch interface. The downstream terminal ledger does **not** intrinsically need a pointwise upper bound on `rho`. It only consumes one weighted time moment of `rho` along the ramp. This is a strictly weaker mathematical target and can materially simplify the remaining source/flowpipe task.

Inputs:

- `review-T-P7-002-honglianmozun-20260907T0050.md`: pointwise absorbed P7 charge `rho(t)*(1/160000)*s(t)^2` and lower-bound need `rho>=rho0`;
- `review-T-P8-006-guyuefangyuan-20260906T2218.md`: ramp identity `s(t)=c*t` with the intended amplitude constraint `c^2<=3`;
- `review-T-M4-006-daai-xianzun-20260906T2346.md` and compiled arithmetic child `T-M4-007`: old-gate slack `1/10000` and budget transfer.

No source binding, flowpipe coverage, Lean validation, receipt/provenance, or admission claim is made.

## 1. Exact weighted-moment identity

After P7 Schur absorption, define the tail ledger contribution on `[0,1]`

```text
D_tail := integral_0^1 rho(t) * (1/160000) * s(t)^2 dt.
```

Under the P8 ramp identity `s(t)=c*t`, this is exactly

```text
D_tail
 = c^2/160000 * integral_0^1 rho(t) t^2 dt.                 (1)
```

Define the weighted moment

```text
J_rho := integral_0^1 rho(t) t^2 dt.                        (2)
```

Then

```text
D_tail = (c^2/160000) J_rho.                                (3)
```

If `0 <= c^2 <= 3` and `J_rho >= 0`,

```text
D_tail <= (3/160000) J_rho.                                 (4)
```

Therefore the old C4 gate `D_base <= 4483/2000` fits the widened M4 gate `1401/625` whenever

```text
(3/160000) J_rho <= 1/10000,
```

i.e.

```text
J_rho <= 16/3.                                               (5)
```

This is the exact terminal-consumer target.

## 2. Why `rho(t) <= 16` is only a sufficient special case

The earlier pointwise condition implies (5), because

```text
rho(t) <= 16
=> J_rho <= 16 * integral_0^1 t^2 dt
         = 16/3.                                             (6)
```

But the converse is false. For example, take the nonnegative measurable function

```text
rho(t) = 32   for 0 <= t <= 1/2,
         0    for 1/2 < t <= 1.
```

Then `sup rho = 32 > 16`, while

```text
J_rho = 32 * integral_0^(1/2) t^2 dt
      = 32 * (1/24)
      = 4/3
      < 16/3.                                                (7)
```

So the pointwise `rho<=16` route rejects trajectories that the actual terminal budget accepts with a factor-four margin in this example.

This is not merely a constant improvement: it changes the required source theorem from a uniform sup enclosure to an integral/weighted-average certificate.

## 3. Exact general slack form

Let

```text
Delta := 1401/625 - D_base.
```

Assume `Delta >= 0`. From (3), the exact sufficient condition is

```text
c^2 * J_rho <= 160000 * Delta.                               (8)
```

If only `c^2<=3` is used, it is enough to prove

```text
J_rho <= (160000/3) Delta.                                   (9)
```

At the old gate `Delta=1/10000`, (9) becomes (5).

If a particular branch has a sharper amplitude `c^2<=C2<3`, the exact target automatically relaxes to

```text
J_rho <= 160000*Delta/C2.                                    (10)
```

Thus the natural cross-branch interface is the product/moment certificate `(c^2,J_rho)`, not a hard-coded `rhoBar`.

## 4. P7 lower bound and M4 upper moment are compatible but logically different

P7 Schur completion still needs a pointwise denominator lower bound

```text
rho(t) >= rho0 > 0                                          (11)
```

on the same domain where the cross coefficients and positive block are bound. Nothing in this review weakens that requirement.

But the downstream energy cost needs only (5)/(8), not a pointwise upper bound. The smallest combined contract is therefore

```text
rho(t) >= rho0   pointwise on [0,1],
J_rho = integral_0^1 rho(t)t^2 dt,
c^2 * J_rho <= 160000*Delta.                                (12)
```

At the old gate and worst-case `c^2<=3`, replace the last line by `J_rho<=16/3`.

This is strictly weaker than the earlier two-sided pointwise contract

```text
rho0 <= rho(t) <= 16.
```

The lower and upper requirements should therefore no longer be packaged as a single pointwise interval unless the source lane happens to obtain such an interval cheaply.

## 5. A useful consistency check from the P7 lower bound

Because `rho(t)>=rho0` and `t^2>=0`,

```text
J_rho >= rho0 * integral_0^1 t^2 dt = rho0/3.                (13)
```

The frozen P7 value is approximately `rho0≈0.27177368`, so the mandatory lower moment is only about `0.09059`, far below the old-gate allowance `16/3≈5.3333`. Thus there is no intrinsic conflict between the P7 denominator lower bound and the M4 terminal budget.

This also gives a quick impossibility test for future parameter branches: if a future P7 lower normalization were so large that `rho0/3 > 16/3`, equivalently `rho0>16`, the old-gate worst-case ramp bookkeeping would be impossible without extra C4 slack or a smaller ramp amplitude. The current branch is nowhere near that obstruction.

## 6. Preferred source/coverage certificates

The source/P8 lane now has three nested options, in decreasing strength:

```text
A. pointwise:  rho(t) <= 16
   => immediately sufficient but strongest;

B. weighted cell sum:
   sum_j rhoUpper_j * integral_{I_j} t^2 dt <= 16/3
   => sufficient if a flowpipe gives piecewise upper bounds;

C. direct weighted integral:
   integral_0^1 rho(t)t^2 dt <= 16/3
   => exact weakest target for the old-gate/worst-ramp consumer.
```

Option B is particularly natural for interval flowpipes. If cells are
`I_j=[a_j,b_j]` and `rho(t)<=R_j` on each cell, it suffices to check the exact scalar inequality

```text
sum_j R_j * (b_j^3-a_j^3)/3 <= 16/3.                         (14)
```

Equivalently,

```text
sum_j R_j * (b_j^3-a_j^3) <= 16.                             (15)
```

This can be certified with rational arithmetic when the time partition and `R_j` are rational. It avoids forcing every cell, especially early-time cells where `t^2` is small, below the same global cap 16.

## 7. Lean-friendly theorem decomposition

The highest-value formalization is not another repository-specific constant theorem but a small integral-to-budget adapter:

```text
ramp_weighted_tail_identity:
  s(t)=c*t
  => integral rho(t)/160000*s(t)^2
     = c^2/160000 * integral rho(t)*t^2
```

with explicit integrability assumptions.

Then a pure scalar consumer:

```lean
theorem old_gate_tail_of_weighted_moment
    (Dbase Dtail c2 Jrho : ℝ)
    (hbase : Dbase <= 4483/2000)
    (hc2 : 0 <= c2) (hc2max : c2 <= 3)
    (hJ : 0 <= Jrho) (hJmax : Jrho <= 16/3)
    (htail : Dtail <= c2 * Jrho / 160000) :
    Dbase + Dtail <= 1401/625
```

and a partition consumer:

```text
weighted_cell_budget:
  0=t0<=...<=tn=1,
  rho(t)<=R_j on [t_j,t_{j+1}],
  sum R_j*(t_{j+1}^3-t_j^3) <= 16
  => integral rho(t)t^2 <= 16/3.
```

The scalar theorem should be formalized first; the integral/partition theorem should keep measurability/integrability and interval-cover hypotheses explicit.

## 8. Failure boundary

This result does not make `rho` physical. It does not prove:

- the P7 symbol `rho` is the deployed trajectory normalization;
- the seven-term polynomial factorization has no omitted/double-counted term;
- `rho(t)>=rho0` on the actual flowpipe;
- any upper cell enclosure `R_j`;
- P8 existence/continuation/coverage;
- the C4 base residual budget on the same domain;
- M4 terminal `L,g` source premises.

Also, an unweighted average bound `integral rho <= K` does not by itself equal the sharp target; it can imply `J_rho<=K` since `t^2<=1`, but that loses the useful early-time weighting. The recommended certificate is explicitly the `t^2`-weighted moment.

## Recommended next action

1. 梁智炜 should treat `rho<=16` as a convenient sufficient target, not the canonical seam. The canonical old-gate target is `J_rho<=16/3`.
2. P7/source lane should keep proving the necessary pointwise lower bound `rho>=rho0`, but may satisfy the upper budget with a weighted cell sum instead of a global sup.
3. P8/flowpipe output should expose time-cell-local `rho` upper bounds if available; the downstream checker can consume (15) with exact rational arithmetic.
4. Formalization lane can add the scalar `old_gate_tail_of_weighted_moment` immediately; the integral identity can follow once the interval-integral API is stabilized.

No admission or final integration is requested. This is a strictly weaker cross-branch mathematical interface for 梁智炜 to harvest if useful.
