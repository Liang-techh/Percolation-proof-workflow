---
kind: review_result
review_id: review-T-P5-010-juyangxianzun-20260907T0047
task_id: T-P5-010
source_agent: 巨阳仙尊
continuation_of: review-T-P5-010-youhunmozun-20260907T0026
claimed_at: 2026-09-07T00:32:00-06:00
created_at: 2026-09-07T00:47:00-06:00
inspected_commit: f4654e3612bbe2f17628bffd2b58fa7c9097aadd
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_validation_then_coordinator_harvest
---

# T-P5-010 — cubic-power small-gain Lean sidecar

## Scope

This review is the formalization continuation of the mathematical result in
`review-T-P5-010-youhunmozun-20260907T0026.md`.  It deliberately stays at the
source-independent consumer layer: no central-FD tensor/source binding, P8
velocity/sublevel coverage, controller/solve bias closure, registry mutation,
or parent P5/M4 admission is claimed.

Portable sidecar:

- `examples/routeb_p5_cubic_small_gain_lean/P5CubicSmallGain.lean`
  - blob `cf8577b62ee1a0b1f202f2f9f041d960631377f5`
- `examples/routeb_p5_cubic_small_gain_lean/verify.sh`
  - blob `6f0235f5c94ae5354e006bf4131572ff373a2141`
- `examples/routeb_p5_cubic_small_gain_lean/lean-toolchain`
  - pinned `leanprover/lean4:v4.32.0`
- `examples/routeb_p5_cubic_small_gain_lean/README.md`

`verify.sh` uses `lake` from `PATH`, checks the sidecar toolchain against
`examples/local_fkg`, carries `CI_PORTABLE=1`, runs with
`-DwarningAsError=true`, checks every `#print axioms` line, and rejects
`sorryAx`/Lean errors.

## Formalized theorem set

1. `scaled_young_division_free`

```text
2 ai aj x y <= aj^2 x^2 + ai^2 y^2.
```

This is the portable no-division kernel needed by a future coordinate-weighted
quadratic certificate.

2. `cubic_relative_small_gain`

```text
dE <= -A + PC + PR + PB,
PC <= kC A,
PR <= kR A
---------------------------------
dE <= -(1-kC-kR) A + PB.
```

This is the exact power-level composition seam between the C-FD cubic lane and
the relative residual lane.

3. `cubic_relative_small_gain_strict`

If additionally

```text
A > 0,
kC+kR < 1,
PB <= 0,
```

then `dE < 0`.

4. `cubic_absorption_of_energy_sublevel`

The square-root-free sublevel adapter is now kernel-checked:

```text
0 <= A,
0 <= Lambda,
0 <= kappa,
PC^2 <= Lambda*A^3,
A <= R^2,
Lambda*R^2 <= kappa^2
---------------------------------
|PC| <= kappa*A.
```

5. `nonzero_cubic_ray_not_globally_quadratic_absorbable`

For any `c != 0`, `a > 0`, and finite real `kappa`, Lean proves

```text
not (forall t >= 0, |c|*t^3 <= kappa*a*t^2).
```

Thus the mathematical scaling obstruction is preserved as a theorem rather
than only prose: a nonzero cubic cannot be globally absorbed by a quadratic
budget on an unbounded velocity ray.

## GitHub Actions repair loop

The sidecar went through two real CI repair iterations before the successful
focused result.

### Attempt 1

- run: `34091581332`
- job: `101645978507`
- head SHA: `a535bc3ae1163b4b6ec810321c996e87d325dd36`
- real Lean error: attempted use of `(mul_le_mul_right ht2).mp` did not match the
  current Mathlib API.
- repair: replaced the cancellation API dependency by a contradiction using
  `mul_lt_mul_of_pos_right`.

### Attempt 2

- run: `34091856088`
- job: `101646829837`
- head SHA: `5a5a3ca0a9d76ea6c9b16f8c91e6c84d93d8c88d`
- all six declarations elaborated with no `sorryAx`, but
  `-DwarningAsError=true` rejected a redundant trailing `ring` after
  `field_simp` (`'ring' tactic does nothing`).
- repair: removed the redundant tactic without changing the theorem statement.

### Focused PASS

- run: `34092184909`
- job: `101647828389`
- head SHA: `f4654e3612bbe2f17628bffd2b58fa7c9097aadd`
- toolchain reported by runner: Lean `4.32.0`, Lake `5.0.0-src+8c9756b`.
- sidecar output:

```text
AXIOM_AUDIT=PASS
P5_CUBIC_SMALL_GAIN_FOCUSED_CHECK=PASS
FD_TENSOR_SOURCE_BINDING=OPEN
P8_VELOCITY_SUBLEVEL_COVERAGE=OPEN
CONTROLLER_SOLVE_BIAS_CLOSURE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_cubic_small_gain_lean/verify.sh
```

All six declarations report only the standard Mathlib axioms

```text
[propext, Classical.choice, Quot.sound]
```

and no `sorryAx`.

The **overall portable-sidecars job is still red**, but not because of this
sidecar.  The same run independently records failures in
`anthropic_flt_quotient_transport_sidecar/verify.sh` (bad relative Lake path)
and `routeb_p5_weighted_dual_residual_lean/verify.sh` (its own Lean errors).
The workflow now runs all portable sidecars before failing, so the explicit
`SIDECAR_RESULT=PASS` above is a valid focused result for this path while the
aggregate job remains fail-closed.  Those unrelated failures were not modified
in this task.

## Dependencies / remaining formalization boundary

This candidate is ready to consume future mathematical/source premises, but it
does not manufacture them.  Still open:

1. `T-P3-008` or a successor must bind the actual central-FD Christoffel tensor
   remainder and supply the concrete `Lambda` or coordinate-weighted gain.
2. P8/first-exit analysis must prove the same-domain velocity box or energy
   sublevel `A <= R^2`.
3. The controller/solve residual lane must establish a nonpositive/vanishing
   bias, or expose it separately; otherwise the strict theorem is not the right
   consumer.
4. No source, coverage, registry, or P5/M4 parent gate is closed by compilation
   of this abstraction.

## Requested next action

Treat this result as `compiled_candidate` only.  It is **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.  Once a source-side `Lambda,R,kappa` contract exists, the shortest formal route is to instantiate
`cubic_absorption_of_energy_sublevel`, compose it with the relative residual
consumer through `cubic_relative_small_gain`, and use
`cubic_relative_small_gain_strict` only when the residual bias premise has been
closed on the same domain.
