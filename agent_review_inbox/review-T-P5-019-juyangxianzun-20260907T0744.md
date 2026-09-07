---
kind: review_result
review_id: review-T-P5-019-juyangxianzun-20260907T0744
task_id: T-P5-019
source_agent: 巨阳仙尊
agent: 巨阳仙尊
claimed_at: 2026-09-07T07:34:00-06:00
created_at: 2026-09-07T07:44:00-06:00
inspected_commit: 50b0aed44a19d561069b1b52b2244196a04990b0
claim_commit: 89a618e28ed85d6ce54602dd867d03fc96cd6b5c
formalization_commits:
  - 06c1f2528e2146221f10596a69b92921ccaff9e4
  - 1dd825a40805562d57739776c43be6d8e7ad2a26
  - c61ab9425dd377a32af0e35997aa2ceed9e7860f
  - 62de17c6ba724b114d00eef8db2c681037f55643
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_then_coordinator_harvest
---

# T-P5-019 — direct block-(4,5) residual metric Lean formalization

## 0. Scope and boundary

This result formalizes the source-independent algebra in
`review-T-P5-019-honglianmozun-20260907T0702.md` only.  In particular it does
**not** claim 柳冠一's separate FD/runtime source adapter from
`review-T-P5-019-liuguanyi-20260907T0730.md`; that lane remains independent.
No Julia/DH/Float64 semantic binding, P8 flowpipe coverage, ODE continuation,
registry admission, or P5/P8/M4 closure is claimed here.

Portable sidecar:

```text
examples/routeb_p5_direct_residual_metric_lean/
  P5DirectResidualMetric.lean
  README.md
  verify.sh
  lean-toolchain
```

The sidecar is pinned to `leanprover/lean4:v4.32.0`.  `verify.sh` resolves
`lake` from `PATH`, checks the sibling pinned `examples/local_fkg` toolchain and
`lake-manifest.json`, sets `CI_PORTABLE=1`, compiles with
`-DwarningAsError=true`, and fails on Lean errors, missing axiom reports, or
`sorryAx`.

## 1. Formalized theorem surface

The exact block constants are frozen as

```text
m4 = 350003/3000000,   m5 = 200739/4000000,
d4 = 4/5,              d5 = 13/20,
k44 = 3/4,             k55 = 29/50,
k45 = -3/400.
```

`qDissipation` is the scalar expansion of the T-P5-019 dissipation quadratic.
The main theorem

```lean
theorem block45_direct_metric (x4 x5 y4 y5 : ℝ) :
  5*((x4+y4)^2 + (x5+y5)^2) ≤ 17*qDissipation x4 x5 y4 y5
```

is obtained through the exact diagonal lower bound

```text
Q >= (143/200)x4^2 + (1849/3200)x5^2
   + (2034997/3000000)y4^2 + (2398011/4000000)y5^2,
```

plus the two exact scalar metric-gap lemmas.  The proof uses only rational
arithmetic, nonnegative squares, and `nlinarith`; no matrix inverse, eigenvalue,
square root, or floating-point computation is part of the theorem statement.

The square-only residual consumer is formalized as

```lean
theorem residual_square_absorption
    (z Q R2 : ℝ)
    (hQ : 0 ≤ Q) (hR : 0 ≤ R2)
    (hz : z^2 ≤ (17/5 : ℝ)*Q*R2) :
    |z| ≤ (1/2 : ℝ)*Q + (17/10 : ℝ)*R2
```

using a separate reusable `abs_le_of_sq_le_sq_nonneg` bridge.  This yields the
pointwise derivative consumer

```text
Vdot <= -Q + |z|
      <= -(1/2)Q + (17/10)R2.
```

The sidecar also proves the storage-level refinement

```text
(457/672)V <= Q
=> Vdot <= -(1/2)Q + (17/10)R2
=> Vdot <= -(457/1344)V + (17/10)R2,
```

and freezes the improved exact barrier arithmetic:

```text
ultimate gain = (17/10)/(457/1344) = 11424/2285 < 5,
2285*Vstar > 11424*L2  => boundary drift < 0,
45696*L2 < 2285        => quarter-barrier drift < 0,
17823*s^2 > 3716608*L2 => common-margin barrier drift < 0.
```

There are 15 printed declarations in the focused axiom audit.

## 2. Real GitHub Actions compile

A later repository push includes this sidecar and therefore provides a genuine
portable-CI compile against the pinned environment:

```text
workflow: Lean agent sidecars
run:      34128525393
job:      101762972457
head:     4fd1616362771e8613a6b8aac89fdaa38a6d7a58
Lean:     4.32.0
Lake:     5.0.0-src+8c9756b
```

The log for this sidecar contains, verbatim at the status-marker level:

```text
AXIOM_AUDIT=PASS
P5_DIRECT_RESIDUAL_METRIC_FOCUSED_CHECK=PASS
SIDECAR_RESULT=PASS path=examples/routeb_p5_direct_residual_metric_lean/verify.sh
```

All real-valued declarations report only

```text
[propext, Classical.choice, Quot.sound]
```

and the pure integer `barrier_constant_checks` reports only `[propext]`.
There is no `sorryAx` in this sidecar.

The **shared workflow job is still red**, but not because of this result.  The
same real log shows independent failures in other lanes:

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` uses the bad
   relative `../local_fkg` path;
2. the newly added `examples/routeb_p5_component_relative_decay_lean/` has a
   `Finset.sum_sub_distrib` type mismatch and resulting `sorryAx` downstream;
3. `examples/routeb_p5_weighted_dual_residual_lean/` still has the existing
   unused `hκ1`, invalid disjunction projection, and resulting `sorryAx`.

Those sidecars belong to other agents and were not modified in this claim.

## 3. Remaining formal/physical boundary

The new Lean theorem is a consumer.  The remaining non-formalized premises are
source/domain obligations:

- identify the exact actual-minus-nominal block residual `l=(l4,l5)` in the
  same generalized-force coordinates used by the theorem;
- prove a same-domain bound `l4^2+l5^2 <= L2`, including Julia/DH/Float64,
  central-FD, controller, and solve defects as applicable;
- provide the P8 nominal flowpipe/physical-domain margin that determines the
  admissible `Vstar` or `s`;
- bind actual and nominal initial states where zero incremental storage is used;
- prove ODE differentiability/existence/continuation and the first-exit bridge
  that turns the pointwise inward inequality into a trajectory invariant.

柳冠一's T-P5-019 review gives a promising separate adapter from existing
block-(4,5) FD/runtime component boxes to such an `L2`; it should remain a
separate source-to-math interface and must not be silently folded into this
compiled algebraic theorem.

## 4. Status

`compiled_candidate` only.  No authoritative DAG state, registry, or final
Route-B conclusion was modified.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
