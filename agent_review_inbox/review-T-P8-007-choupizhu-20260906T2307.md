---
kind: review_result
review_id: review-T-P8-007-choupizhu-20260906T2307
task_id: T-P8-007
parent_task_id: T-P8-006
source_agent: 臭屁猪
created_at: 2026-09-06T23:07:00-06:00
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_by_封不觉
---

# T-P8-007 — portable Lean formalization of ramp-tail reconstruction

## Scope

This formalizes the pure calculus child proved mathematically in `T-P8-006`.
It does **not** perform source binding, provenance, receipt, flowpipe coverage,
or registry/admission work.

The first formalization deliberately uses a stronger implementation boundary
than the eventual P8 theorem should need: scalar coordinate functions are
assumed differentiable on all of `ℝ` through pointwise `HasDerivAt`
hypotheses.  The weaker interval-local/end-point formulation remains an open
refinement and is not silently claimed here.

Current repository snapshot observed after the focused CI pass:

- main head after unrelated later work: `21ec7b34033ba8a2a62c8831e4d20b59635d0ac0`;
- focused passing sidecar commit: `0723aea49d4051af7cb1c6e5848b1a1984e6bbdc`;
- `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`
  blob: `0bcac8908b2492ae72279ef0cd05b2d6634bc3a9`;
- `examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh`
  blob: `89144cf54bcdc1d71db8230b9387103c5298b1cf`.

## Formalized statements

The sidecar proves:

```text
ramp_c_constant:
  c(0)=c0 ∧ (∀t, c'(t)=0) -> ∀t, c(t)=c0

ramp_w_eq_mul:
  w(0)=0 ∧ (∀t, c(t)=c0) ∧ (∀t, w'(t)=c(t))
  -> ∀t, w(t)=c0*t

ramp_reconstruction:
  combines the previous two conclusions.
```

It also introduces the typed P8 tail shape

```text
State14 := Fin 14 -> ℝ
wSlot = 12
cSlot = 13
```

and proves:

```text
state_tail_reconstruction:
  z(t)[cSlot]=c0 ∧ z(t)[wSlot]=c0*t

state_terminal_one:
  z(1)[wSlot]=c0.
```

The proof uses Mathlib's `is_const_of_deriv_eq_zero` and ordinary derivative
rules; no ODE solver, numerical trace, source snapshot, or external axiom is
introduced.

## Portable GitHub-CI implementation

Files created:

- `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`
- `examples/routeb_p8_ramp_reconstruction_sidecar/lean-toolchain`
- `examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh`
- `examples/routeb_p8_ramp_reconstruction_sidecar/README.md`

The sidecar pins `leanprover/lean4:v4.32.0`, matching the repository's
`examples/local_fkg` Lake environment.  `verify.sh` contains `CI_PORTABLE=1`,
locates `lake` from `PATH`, rejects toolchain mismatch, and contains no
`/home/z5242/...` or Windows user-directory dependency.

Focused command executed by the GitHub-hosted workflow is effectively:

```text
cd examples/local_fkg
lake env lean -DwarningAsError=true \
  ../routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean
```

## GitHub Actions compile evidence

Workflow: `.github/workflows/lean-agent-sidecars.yml`

Final passing run:

```text
run_id = 34085393805
job_id = 101628339820
head_sha = 0723aea49d4051af7cb1c6e5848b1a1984e6bbdc
runner = ubuntu-24.04
job conclusion = success
portable-sidecars step = success
```

The actual focused log reports:

```text
Running examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
'RouteBP8RampReconstruction.ramp_c_constant' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.ramp_w_eq_mul' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.ramp_reconstruction' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.state_tail_reconstruction' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBP8RampReconstruction.state_terminal_one' depends on axioms:
  [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
P8_RAMP_RECONSTRUCTION_FOCUSED_CHECK=PASS
PORTABLE_SIDECARS_RUN=2
```

No `sorryAx` appears in the final passing theorem set.

For completeness, GitHub CI also caught and rejected two real Lean issues on
intermediate commits rather than hiding them as an environment problem:

1. run `34085002837` / job `101627229462` rejected the first repair because
   `HasDerivAt.sub` produced pointwise function subtraction rather than the
   lambda-shaped target;
2. run `34085159285` / job `101627671006` then exposed the final algebraic
   target mismatch `w t - c0*t = 0` versus `w t = c0*t`.

Both were repaired before the passing run.  This confirms that the GitHub
Lean/Lake infrastructure is actually exercising the kernel-facing source.

## Evidence boundary / remaining obligations

This compiled candidate closes only the abstract ramp-tail calculus seam under
the stated stronger differentiability assumptions.  It does not close:

- the interval-local version on `[0,1]` with minimal endpoint regularity;
- the deployed Julia/DH first-12 mechanical RHS semantic binding;
- existence/regularity of the actual P8 ODE trajectory;
- outward interval containment, Picard/local flowpipe existence;
- continuation and full `[0,1]` coverage;
- true-DH flowpipe, downstream terminal comparator, or M4;
- final independent validation/admission.

## Handoff

`封不觉` should independently inspect the passing GitHub Actions run and the
current blob hashes before assigning any stronger label.  If a later P8 parent
needs only interval-local differentiability rather than global differentiability,
one formalization agent should add that weaker theorem as a separate child and
prove that the parent hypotheses instantiate it.
