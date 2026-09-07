---
kind: review_result
review_id: review-T-P8-009-sumengchen-20260907T0118
task_id: T-P8-009
source_agent: 苏梦辰
claimed_at: 2026-09-07T01:10:00-06:00
created_at: 2026-09-07T01:18:00-06:00
inspected_commit: 4883445bf63b5366a696b5c7201b288cf79bf233
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_by_封不觉_then_harvest_by_梁智炜
---

# T-P8-009 — interval-local ramp calculus refinement

## Scope

This formalizes the coordinator-assigned refinement of the already compiled
P8 ramp reconstruction theorem.  The old sidecar required `HasDerivAt` on all
of `ℝ`; the new theorem only assumes continuity on `[0,1]` and one-sided/right
`HasDerivWithinAt` witnesses on `[0,1)`, which is exactly enough for the
terminal endpoint `t=1`.

The existing compiled sidecar
`examples/routeb_p8_ramp_reconstruction_sidecar/` was not modified.
Source binding, ODE existence/uniqueness, interval enclosure, first-exit,
flowpipe coverage, and registry/admission remain outside this result.

## Lean artifact

Created a separate portable sidecar:

- `examples/routeb_p8_interval_ramp_lean/P8IntervalRamp.lean`
  - blob `0904bd9510ccc672436459caa40d827c879bba07`;
- `examples/routeb_p8_interval_ramp_lean/verify.sh`
  - blob `349729525f9475bac05c8869e1e3db034583712a`;
- `examples/routeb_p8_interval_ramp_lean/README.md`
  - blob `b20c99a724d17aba18234b188c324d1c8fe8280e`;
- `examples/routeb_p8_interval_ramp_lean/lean-toolchain`
  - pin `leanprover/lean4:v4.32.0`, matching the shared `examples/local_fkg`
    environment.

`verify.sh` carries `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks the
shared Lake root/toolchain, compiles with `-DwarningAsError=true`, and fails if
`sorryAx`, an unknown module, or a compiler error is present.

## Theorem decomposition

The main scalar theorem now has the interval-local contract

```lean
theorem ramp_c_constant_on_Icc
    (c : ℝ → ℝ) (c0 : ℝ)
    (hc0 : c 0 = c0)
    (hcont : ContinuousOn c (Set.Icc (0 : ℝ) 1))
    (hc : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt c 0 (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, c t = c0
```

using Mathlib's `constant_of_has_deriv_right_zero`.

The ramp coordinate is then compared against `t ↦ c0*t` via
`eq_of_has_deriv_right_eq`:

```lean
theorem ramp_w_eq_mul_on_Icc
    (w c : ℝ → ℝ) (c0 : ℝ)
    (hw0 : w 0 = 0)
    (hcconst : ∀ t ∈ Set.Icc (0 : ℝ) 1, c t = c0)
    (hwcont : ContinuousOn w (Set.Icc (0 : ℝ) 1))
    (hw : ∀ t ∈ Set.Ico (0 : ℝ) 1,
      HasDerivWithinAt w (c t) (Set.Ici t) t) :
    ∀ t ∈ Set.Icc (0 : ℝ) 1, w t = c0 * t
```

The combined theorem `ramp_reconstruction_on_Icc` proves both statements on
`[0,1]`.

The P8 tail slots remain typed:

```text
State14 = Fin 14 -> ℝ
wSlot   = 12
cSlot   = 13
```

and `state_tail_reconstruction_on_Icc` transports the scalar theorem to these
coordinates.  Finally,

```lean
state_terminal_one_interval : z 1 wSlot = c0
```

is obtained using the endpoint membership `1 ∈ [0,1]`; no derivative premise
at `t=1` and no premise outside `[0,1]` is used.

This is strictly closer to the mathematical contract requested by T-P8-006:
endpoint continuity plus right derivatives on the half-open proof horizon are
sufficient for terminal transfer.

## GitHub Actions / focused compile

The sidecar triggered the shared portable workflow at the pinned source head:

```text
workflow: Lean agent sidecars
run_id:   34094488050
job_id:   101654953313
runner:   ubuntu-24.04
Lean:     4.32.0
Lake:     5.0.0-src+8c9756b
```

The focused log for this sidecar is:

```text
Running examples/routeb_p8_interval_ramp_lean/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
'RouteBP8IntervalRamp.ramp_c_constant_on_Icc' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8IntervalRamp.ramp_w_eq_mul_on_Icc' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8IntervalRamp.ramp_reconstruction_on_Icc' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8IntervalRamp.state_tail_reconstruction_on_Icc' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8IntervalRamp.state_terminal_one_interval' depends on axioms:
  [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
P8_INTERVAL_RAMP_FOCUSED_CHECK=PASS
SOURCE_BINDING=OPEN
FLOWPIPE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p8_interval_ramp_lean/verify.sh
```

Thus all five T-P8-009 theorems kernel-compile under the pinned GitHub-hosted
Lean environment and no `sorryAx` occurs in this theorem set.

The aggregate Actions job still concludes `failure`, but for disjoint existing
sidecars: the FLT quotient verifier has a bad relative Lake path, and the P5
weighted-dual residual sidecar still has its previously reported zero-kappa
compile/sorry issue.  T-P8-009 itself is an explicit focused PASS; I did not
modify those other agents' files.

## Remaining formalization / semantic boundary

This child proves only interval-local calculus.  Still open:

- deployed first-12 source semantic binding (`T-P8-008` lane);
- proof that an actual trajectory exists with the stated continuity/right-
  derivative hypotheses;
- outward RHS enclosure, first-exit, continuation, and `[0,1]` flowpipe
  coverage;
- source identification of the 14-state lifted tail with the physical adapter;
- terminal downstream physical premises and final P8/M4 admission.

The theorem should therefore remain `compiled_candidate` only.  It is **待封不觉独立验证 / 待梁智炜最终整合**.
