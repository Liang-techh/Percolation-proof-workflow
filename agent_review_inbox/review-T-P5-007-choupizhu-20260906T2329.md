---
kind: review_result
review_id: review-T-P5-007-choupizhu-20260906T2329
task_id: T-P5-007
source_agent: 臭屁猪
created_at: 2026-09-06T23:29:00-06:00
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: continue_github_ci_then_independent_verify
---

# T-P5-007 — damping-weighted dual residual Lean sidecar

## Scope

Formalize the source-independent implication from the mathematical review
`T-P5-005`:

```text
dualSq_d(r) <= kappa^2 * dampedSq_d(v)
```

into retained damping, preserving the exact `kappa = 0` boundary and a generic
additive-force-error counterexample.  This result does not derive the premise
from deployed DH/FD/solve code and does not claim P5/M4 closure.

## Files added

- `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`
- `examples/routeb_p5_weighted_dual_residual_lean/lean-toolchain`
- `examples/routeb_p5_weighted_dual_residual_lean/verify.sh`
- `examples/routeb_p5_weighted_dual_residual_lean/README.md`

The sidecar pins `leanprover/lean4:v4.32.0`, matching `examples/local_fkg`, and
`verify.sh` contains `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks the
pinned toolchain, and contains no machine-specific `/home/z5242/...` or Windows
user-directory path.

## Theorem decomposition

The new sidecar defines

```text
dampedSq d v = sum_i d_i v_i^2
dualSq   d r = sum_i r_i^2 / d_i
dot      r v = sum_i r_i v_i
```

and proposes the following kernel-facing statements.

1. `weighted_young_component`

```text
0 < d
=> 2*kappa*(r*v) <= kappa^2*(d*v^2) + r^2/d.
```

This is the division-free weighted Young step after multiplying by the positive
`d`; the proof is generated from the square `(kappa*d*v-r)^2 >= 0`.

2. `weighted_dot_le_of_dualSq`

```text
(forall i, 0 < d_i), 0 < kappa,
dualSq d r <= kappa^2*dampedSq d v
=> dot r v <= kappa*dampedSq d v.
```

3. `weighted_residual_decay`

```text
0 < kappa < 1,
dualSq d r <= kappa^2*dampedSq d v,
dE <= -dampedSq d v + dot r v
=> dE <= -(1-kappa)*dampedSq d v.
```

4. `dualSq_nonneg` and `dualSq_eq_zero_forces_component_zero` isolate the exact
`kappa=0` case.

5. `weighted_residual_decay_kappa_zero`

```text
dualSq d r <= 0,
d_i>0,
dE <= -dampedSq d v + dot r v
=> dE <= -dampedSq d v.
```

6. `generic_force_error_not_velocity_relative` records the mathematical
interface obstruction separately: an additive gravity-like mismatch can be 1
while the corresponding velocity is 0, so no finite `rho*|v_i|` bound follows
from a generic additive-error interface alone.

## Current GitHub Actions status

The portable workflow was actually triggered by the sidecar commits:

```text
workflow = Lean agent sidecars
run_id   = 34086964924
job_id   = 101632786695
runner   = ubuntu-24.04
```

At the time of this review writeback, GitHub reports:

```text
Install checksum-verified Elan               success
Bootstrap pinned local-FKG Lake environment  in_progress
Run portable agent sidecars                  pending
```

Therefore no compile PASS is claimed yet.  The important environment boundary
is now resolved correctly: GitHub is providing the pinned Lean/Lake toolchain,
and any subsequent failure in the portable-sidecars step will be treated as a
real theorem/import/API error to repair rather than as a missing-local-Lean
excuse.

## Evidence/admission boundary

Still open:

- final result of GitHub Actions run `34086964924`;
- any concrete Lean repair exposed by that run;
- independent `#print axioms` / statement-identity gate by `封不觉` after a
  successful compile;
- deployed DH/FD/solve same-domain proof of the weighted residual premise;
- P5/M4 integration.

Even after a green compile, the correct status is only
`待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合`.
