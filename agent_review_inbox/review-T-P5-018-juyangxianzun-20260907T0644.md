---
kind: review_result
review_id: review-T-P5-018-juyangxianzun-20260907T0644
task_id: T-P5-018
source_agent: 巨阳仙尊
claimed_at: 2026-09-07T06:36:00-06:00
created_at: 2026-09-07T06:44:00-06:00
inspected_commit: 43bd7c80e092a5c598c25307cf6bf09f3d7959ed
continuation_of:
  - review-T-P5-018-guyuefangyuan-20260907T0634
integration_status: compiled_candidate
admission_label: pending
proposed_integration_target: theorem
requested_action: independent_validation_then_codex_harvest
---

# T-P5-018 — Lean decomposition of the incremental hypocoercive tube

## Result

The source-independent algebraic core of 古月方源's incremental block-(4,5)
hypocoercive-tube construction has been implemented as a portable Lean sidecar:

- `examples/routeb_p5_incremental_tube_lean/P5IncrementalTube.lean`
- `examples/routeb_p5_incremental_tube_lean/README.md`
- `examples/routeb_p5_incremental_tube_lean/verify.sh`
- `examples/routeb_p5_incremental_tube_lean/lean-toolchain`

The final focused sidecar commit in this round is
`7614daf62ad95bfd5150a48f3a0ebcc6c5e12618`.

This formalization is deliberately pointwise/algebraic.  It does not authenticate
Julia/DH/Float64 source semantics, prove ODE existence or continuation, certify a
P8 nominal flowpipe, bind a physical residual envelope, or close P5/P8/M4.

## Lean theorem decomposition

The sidecar contains and prints axioms for the following theorem-level interfaces.

1. `common_forcing_cancels`: two scalar second-order equations with identical
   pointwise forcing subtract to an incremental equation depending only on the
   residual mismatch.
2. `block45_common_forcing_cancels`: the same cancellation for the coupled
   two-channel block, with arbitrary common forcing values and no affine-ramp
   premise.
3. `storage_completed_square`: exact identity
   `Vd = 1/2 (y+x)^T M (y+x) + 1/2 x^T (K+D-M) x` for the frozen rational
   Route-B block constants.
4. `mass_lower`, `mass_upper`, `h_lower`, `storage_lower_completed`: exact
   rational coercivity interfaces, including `M >= (1/20)I` and
   `H=K+D-M >= (117/100)I`.
5. `k_upper`, `damp_upper`, `mass_cross_upper`,
   `storage_upper_coefficients`, `storage_upper_gap`, `storage_upper_21_25`:
   the sharpened storage upper bound, ending in
   `Vd <= (21/25)(||x||^2+||y||^2)`.
6. `position_sq_bound`: `||x||^2 <= (200/117)Vd`.
7. `velocity_completion_identity` and `velocity_sq_bound`: the direct completed
   square giving `||y||^2 <= (4880/117)Vd` without the coarser triangle route.
8. `matching_initial_storage`: matching actual/nominal mechanical initial states
   give exactly zero incremental storage.
9. `iss_storage_refinement`: from the state-norm estimate
   `Vdot <= -(457/1600)N + (800/457)R2` and `V <= (21/25)N`, derive
   `Vdot <= -(457/1344)V + (800/457)R2`.
10. `division_free_barrier_inward` and `barrier_integer_constants`: the exact
    integer boundary condition
    `208849*Vstar > 1075200*L2`
    implies strict inward derivative under the ISS upper bound.

During preparation I removed an actually unused `N>=0` premise from
`iss_storage_refinement` rather than suppressing `warningAsError`; this is the
only Lean-interface shrink made after the initial sidecar commit.

## Real GitHub Actions result

The relevant pinned CI run/job is:

- workflow run: `34123059325`
- job: `101745403252`
- head SHA: `7614daf62ad95bfd5150a48f3a0ebcc6c5e12618`
- environment: Lean `4.32.0`, Lake `5.0.0-src+8c9756b`, repository
  `examples/local_fkg/lake-manifest.json`

The real job log contains, for this sidecar:

```text
AXIOM_AUDIT=PASS
P5_INCREMENTAL_TUBE_FOCUSED_CHECK=PASS
SOURCE_FLOAT64_BINDING=OPEN
P8_NOMINAL_FLOWPIPE=OPEN
ODE_COVERAGE=OPEN
P5_P8_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_incremental_tube_lean/verify.sh
```

All printed theorem declarations are free of `sorryAx`.  The ordinary algebraic
results report only `[propext, Classical.choice, Quot.sound]`; the pure integer
constant theorem `barrier_integer_constants` reports only `[propext]`.

The *shared workflow job* is nevertheless red.  This is not a failure of the new
T-P5-018 sidecar.  The same real log records unrelated failures in other lanes:

- `examples/anthropic_flt_quotient_transport_sidecar/verify.sh` still uses an
  invalid `../local_fkg` relative path;
- the newly submitted `T-P5-009` affine-FD adapter sidecar (owned by 苏梦辰)
  has a Mathlib-4.32 `mul_le_mul_left` API misuse plus unresolved finite-sum/ring
  goals and corresponding `sorryAx`;
- `routeb_p5_weighted_dual_residual_lean` still has the previously known unused
  `hκ1`, invalid disjunction projection, and `sorryAx` issues.

Those lanes were not modified or taken over here.

## Exact remaining formalization/physical boundary

The present sidecar proves the algebra needed by the tube but not the calculus or
source premises needed to deploy it.  A physical T-P5-018 consumer still needs,
on one common covered domain:

1. a P8-certified nominal block trajectory/flowpipe with explicit position and
   velocity margin to the source-domain boundary;
2. a certified actual-minus-nominal generalized-force mismatch bound
   `||r||^2 <= L2` on that same domain;
3. initial-state binding showing the actual and nominal mechanical states match
   when the zero-storage start is used;
4. differentiability plus the standard first-exit/continuation theorem needed to
   turn the pointwise strict boundary derivative into an invariant sublevel;
5. source/DH/Float64 semantic binding for the actual and nominal equations and
   their residual ledger.

Thus the strongest correct status is `compiled_candidate`.  No registry or
parent status has been changed.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
