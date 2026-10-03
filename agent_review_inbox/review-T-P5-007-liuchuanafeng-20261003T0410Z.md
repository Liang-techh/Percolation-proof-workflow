---
kind: review_result
review_id: review-T-P5-007-liuchuanafeng-20261003T0410Z
source_agent: 流川枫
created_at: 2026-10-03T04:10:00Z
inspected_commit: 767a6a29397e33b9078aad4a4538a43f24ee61e0
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P5-007-choupizhu-20260906T2329.md
  - examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean
  - examples/routeb_p5_weighted_dual_residual_lean/README.md
  - examples/routeb_p5_weighted_dual_residual_lean/verify.sh
  - examples/routeb_p5_weighted_dual_residual_lean/lean-toolchain
  - examples/routeb_p5_residual_power_lean/DissipativeResidualPower.lean
  - examples/routeb_p5_residual_power_lean/compile_receipt.json
task_id: T-P5-007
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P5-007 audit: weighted dual residual sidecar is source-independent and uncompiled here

## Question

At commit `767a6a29397e33b9078aad4a4538a43f24ee61e0`, does `WeightedDualResidual.lean` formalize `dualSq d r ≤ kappa² * dampedSq d v` into retained damping without square roots, keep the `kappa=0` boundary, and retain a generic force-error counterexample, and can that sidecar be admitted as true-DH source binding or P5/M4 closure?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The file states the requested source-independent implication, the zero-kappa boundary, and a separate additive-error counterexample, and the displayed statements do not use square roots. This pass did not run Lean, so the file is not a `compiled_candidate`. It is not `verified`. It is not `rejected`: the algebraic shape matches the task. It is not `architecture_only`: the obstruction is pinned to missing compile/axiom receipt and missing source premises.

Prior review `review-T-P5-007-choupizhu-20260906T2329.md` is left intact. Its GitHub Actions run `34086964924` is not rechecked here and is not treated as a current exit code.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `task_queue.md` lists `T-P5-007` as `open`. Required object: the damping-weighted implication without square roots, plus the generic force-error counterexample as a separate theorem, or a precise compile obstruction. Forbidden: treating abstract premises as true-DH source binding, or promoting compilation into the verified registry.

2. **Sidecar blobs at this commit.**
   - `WeightedDualResidual.lean` blob `aeeef5fbac51ddff147aae16710223e3407a44dc`
   - `README.md` blob `2ae86af7a251d3b264d51c0fd31827ec534c3369`
   - `verify.sh` blob `62f327cf0140ed94c72607c5125d49301c0867d3`
   - `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`, text `leanprover/lean4:v4.32.0`

3. **Statements avoid square roots.** Definitions are

```text
dampedSq d v = ∑ i, d i * v i ^ 2
dualSq   d r = ∑ i, r i ^ 2 / d i
dot      r v = ∑ i, r i * v i
```

   `weighted_young_component` is the component inequality `2*κ*(r*v) ≤ κ²*(d*v²) + r²/d` under `0 < d`, derived from `(κ*d*v - r)² ≥ 0`. `weighted_dot_le_of_dualSq` consumes `dualSq d r ≤ κ² * dampedSq d v` and `0 < κ` to get `dot r v ≤ κ * dampedSq d v`. `weighted_residual_decay` then gets `dE ≤ -(1-κ)*dampedSq d v` from `dE ≤ -dampedSq d v + dot r v` and `0 < κ < 1`. No `Real.sqrt` appears in these statements.

4. **`kappa=0` is a separate theorem, not a specialization of the positive-kappa theorem.** `weighted_dot_le_of_dualSq` requires `0 < κ`, so it does not cover zero. `weighted_residual_decay_kappa_zero` uses `dualSq d r ≤ 0`, nonnegativity, and `dualSq_eq_zero_forces_component_zero` to force every `r i = 0`, then `dot r v = 0`, then `dE ≤ -dampedSq d v`. That is the exact zero boundary requested by the task, provided the zero-forcing lemma compiles.

5. **Counterexample is separate and does not depend on the decay theorems.** `generic_force_error_not_velocity_relative` exhibits channel 0 with gravity component `1`, all other summands `0`, and velocity `0`, so `|error| = 1 > ρ * |v i|` for every real `ρ`. It does not claim this witness is the deployed gravity term.

6. **Compile receipt is absent for this sidecar.** `examples/routeb_p5_residual_power_lean/compile_receipt.json` is a different file (`DissipativeResidualPower.lean`, exit code 0, axioms `propext`, `Classical.choice`, `Quot.sound`, `physical_source_binding: false`). That receipt does not cover `WeightedDualResidual.lean`. `verify.sh` expects a Lake env at `examples/local_fkg` and greps the seven declarations; this pass did not execute it. No exit code is claimed.

7. **Candidate compile risk, not a measured failure.** In `dualSq_eq_zero_forces_component_zero`, the step

```text
apply (div_eq_zero_iff).mp at hterm
exact hterm.1
```

   selects the left disjunct of `r i ^ 2 = 0 ∨ d i = 0` without an explicit `d i ≠ 0` case split. This may be a real Lean elaboration error. It is recorded only as a repair target for the next pinned compile, not as an observed exit code.

## Obstruction

```text
interface: dualSq d r ≤ κ² * dampedSq d v, with d i > 0
proved_shape: source-independent retained decay and kappa=0 boundary
counterexample: additive channel-0 error 1 at velocity 0, separate theorem
missing: pinned Lean exit, #print axioms, placeholder scan on this file
missing: deployed DH/FD/solve witness for dualSq d r ≤ κ² * dampedSq d v
source_binding: not claimed
```

## Assumptions still required

- a pinned `lake env lean` receipt on `leanprover/lean4:v4.32.0` for this sidecar, including the zero-forcing lemma;
- axiom output limited to the standard kernel axioms already seen on the sibling residual-power receipt, with no `sorryAx`;
- a same-domain source proof of the dual-square premise and of `0 < d i`;
- coverage and comparator gates before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P5-007` open.
- Requested action: next Lean owner should run `examples/routeb_p5_weighted_dual_residual_lean/verify.sh` and, if the zero-forcing lemma fails, repair only that case split. Do not import the sibling residual-power receipt as evidence for this file. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat abstract premises as true-DH source binding.
- Did not promote compilation, or the sibling exit-0 receipt, into the verified registry.
- Did not close P5 or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
