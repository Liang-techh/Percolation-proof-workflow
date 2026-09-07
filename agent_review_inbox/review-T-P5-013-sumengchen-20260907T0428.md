---
kind: review_result
review_id: review-T-P5-013-sumengchen-20260907T0428
task_id: T-P5-013
source_agent: 苏梦辰
created_at: 2026-09-07T04:28:00-06:00
inspected_commit: 590a3f53212710bc00f7e13714b7184b83e92425
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_validation_then_coordinator_harvest
---

# T-P5-013 — finite-horizon mixed P5 energy-budget Lean sidecar

## Scope

This formalizes the source-independent algebraic core of 红莲魔尊's
`review-T-P5-013-honglianmozun-20260907T0358.md`.  It does **not** claim the
calculus/ODE first-exit argument, source/IEEE execution binding, numerical
`S_F/Hbar/Rbar/W_min`, P8 ramp-domain coverage, registry admission, P5 closure,
or M4 closure.

The formalization was intentionally kept separate from 柳冠一's subsequent
`T-P5-014` weighted-dual source-coordinate adapter so the energy consumer and
the source bridge remain independently checkable.

## Files

- `examples/routeb_p5_finite_horizon_budget_lean/P5FiniteHorizonBudget.lean`
- `examples/routeb_p5_finite_horizon_budget_lean/README.md`
- `examples/routeb_p5_finite_horizon_budget_lean/verify.sh`
- `examples/routeb_p5_finite_horizon_budget_lean/lean-toolchain`

The sidecar is pinned to `leanprover/lean4:v4.32.0`.  `verify.sh` finds `lake`
from `PATH`, uses `examples/local_fkg` by default, checks the pinned toolchain,
compiles with `-DwarningAsError=true`, and is marked `CI_PORTABLE=1` for
`.github/workflows/lean-agent-sidecars.yml`.

## Kernel statements

The sidecar contains the following minimal statements.

### 1. Square domination to absolute-value domination

```text
0 <= y,
x^2 <= y^2
----------------
|x| <= y.
```

Lean declaration:

```text
abs_le_of_sq_le_sq_nonneg
```

### 2. Cubic power absorption from an energy barrier

For nonnegative `A`, `Lambda`, and `g`,

```text
A <= K Z,
PC^2 <= Lambda A^3,
Lambda K Z <= g^2
----------------------
|PC| <= g A.
```

Lean declaration:

```text
cubic_absorption_from_energy_barrier
```

This is deliberately source-independent and reuses the same square-only
mathematics as `T-P5-011` without importing a sibling example module.

### 3. Weighted-dual work charging without square roots

For `A>=0`, `gR>0`, `BR>=0`,

```text
PR^2 <= R A,
R <= 4 gR BR
----------------
PR <= gR A + BR.
```

Lean declaration:

```text
dual_work_budget
```

This is the exact consumer needed after a source adapter has produced the
weighted-dual generalized-force quantity.  `T-P5-014` is the disjoint source
adapter lane; this theorem does not manufacture that source quantity itself.

### 4. Mixed pointwise energy-rate ledger

Given the cubic hypotheses above, the dual-work hypotheses above, a one-sided
ramp cap `hRamp <= Hbar`, and

```text
Zdot <= -(gC+gR) A + PC + PR + hRamp,
```

the theorem proves

```text
Zdot <= Hbar + BR.
```

Lean declaration:

```text
mixed_energy_rate
```

This is only a **pointwise differential inequality consumer**.  The theorem does
not silently turn it into a trajectory integral or a first-exit theorem.

### 5. Algebraic terminal step after a calculus layer has supplied linear growth

If

```text
Zt <= Z0 + t B,
t <= T,
0 <= B,
Z0 + T B < Zstar,
```

then

```text
Zt < Zstar.
```

Lean declaration:

```text
linear_growth_stays_below_barrier
```

The missing upstream calculus theorem is therefore isolated cleanly: one still
has to derive `Z(t) <= Z(0)+tB` from a derivative bound along the actual
trajectory/first-exit interval.

### 6. Exact rational `T=1`, 50/50 headroom conversion

With `SF>0`, `g0>0`, the checker-facing hypothesis

```text
26*SF*g0*(Z0+Hbar) + 13*SF*Rbar
  < 36000000000000000*g0^3
```

implies

```text
Z0 + Hbar + Rbar/(2*g0)
  < (18000000000000000*g0^2)/(13*SF).
```

Lean declaration:

```text
t1_fifty_fifty_headroom_from_rational
```

No square root is introduced; this keeps the final checker arithmetic rational.

### 7. Kernel-checked failure boundary

The theorem

```text
upper_storage_coercivity_counterexample
```

constructs `A=0`, `Z=1`, `K=1` and proves that the available one-sided storage
relation `A <= K Z` cannot by itself imply any uniform asymptotic estimate of
the form

```text
-A <= -alpha Z,  alpha>0.
```

This prevents the finite-horizon barrier from being overinterpreted as an
asymptotic exponential-decay theorem.

## Real GitHub Actions repair loop

### First compile: semantic/type repair

The initial CI run exposed two issues in this new sidecar:

1. an unused `ht0` hypothesis in `linear_growth_stays_below_barrier` under
   `warningAsError`;
2. an invalid cancellation attempt using `(mul_lt_mul_left hdenG).mp hscaled`
   in the rational headroom theorem.

Both were repaired without weakening the statements.  The second proof now
uses contradiction plus multiplication by the positive factor `2*g0`.

### Second compile: linter repair

GitHub Actions run `34110863351`, job `101706542314`, typechecked all seven
new declarations and printed their axiom reports, but `warningAsError` rejected
one tactic-style linter warning:

```text
Used `tac1 <;> tac2` where `(tac1; tac2)` would suffice
```

at the local `field_simp`/`ring` proof in the rational headroom theorem.  This
was repaired by replacing the unnecessary sequence-focus combinator with
`all_goals ring`; no theorem hypothesis or conclusion changed.

### Final focused compile

GitHub Actions run `34111257698`, job `101707796366`, on commit
`590a3f53212710bc00f7e13714b7184b83e92425`, reports for this sidecar:

```text
AXIOM_AUDIT=PASS
P5_FINITE_HORIZON_POINTWISE_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_finite_horizon_budget_lean/verify.sh
```

All seven printed declarations depend only on

```text
[propext, Classical.choice, Quot.sound]
```

and the sidecar has no `sorryAx`.

The overall `portable-sidecars` job is still red, but the remaining failures are
unrelated pre-existing artifacts and were not taken over in this task:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still has the
  `../local_fkg` relative-path failure;
- `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
  still has unused `hκ1`, an invalid disjunction projection, and `sorryAx` in
  the zero-kappa branch.

The new T-P5-013 sidecar itself is an explicit CI PASS in that same job.

## Dependencies and remaining formal obligations

The following are still external to this compiled child:

1. a calculus/trajectory first-exit theorem converting the pointwise bound into
   `Z(t) <= Z(0)+tB` on the actual finite horizon;
2. the `T-P5-014` weighted-dual source-coordinate adapter formalization and,
   separately, runtime/source numerical bounds that instantiate it;
3. exact source/checker binding for `S_F`;
4. a same-domain ramp-work cap `Hbar`;
5. a same-domain weighted-dual execution cap `Rbar` including the intended
   controller/solve/IEEE remainders exactly once;
6. a same-domain lower bound for the modified nonkinetic storage (`W_min`, or
   the equivalent shifted-storage premise);
7. P8 ramp-graph pullback-domain coverage on the whole requested horizon;
8. ODE existence/continuation and actual trajectory coverage needed by the
   first-exit argument.

No registry entry, authoritative state, P5 status, M4 status, or final DAG
conclusion was modified here.

**Status: `compiled_candidate`.  待封不觉独立验证 / 待梁智炜最终整合。**
