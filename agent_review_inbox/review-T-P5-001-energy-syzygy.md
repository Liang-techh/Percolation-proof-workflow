kind: review_result
task_id: T-P5-001
source_agent: Codex
created_at: 2026-09-06T20:39:00-06:00
integration_status: pending
---

# T-P5-001 review: Route-B energy-syzygy admission audit

## Inspected scope

Read-only audit only. I inspected the Route-B energy bridge files and the queue entry that isolates the task:

- `agent_review_inbox/task_queue.md`
- `docs/routeb-block45-proof-sketch.md`
- `examples/routeb_agent_exact_dh_loop_lean/RouteBAgentExactDHLoop.lean`
- `examples/routeb_agent_exact_dh_loop_lean/README.md`
- `examples/routeb_dh_power_binding/ExistingEnergyCore.lean`
- `examples/routeb_dh_power_binding/DHPowerBinding.lean`
- `examples/routeb_dh_power_binding/README.md`
- `examples/routeb_supply_core/RouteBSupplyCore.lean`
- `examples/routeb_residual_power/ResidualPower.lean`

Focused check run:

- `bash examples/routeb_dh_power_binding/verify.sh`
- exit code: `0`
- compiled `DHPowerBinding.lean` hash: `15a8e8ceb17131c32ceb02f4982d71807681d812d22de9f0b2fa206be346db5d`
- the script also recompiled `ExistingEnergyCore.lean`, `RouteBSupplyCore.lean`, `ResidualPower.lean`, and `ControllerPowerCore.lean` under the current Lean/Mathlib pin

## Theorem statement

The closest reusable exact statements already present are generic power / energy bridges, not a dedicated Newton–Euler energy syzygy theorem:

- `RouteBAgentExactDHLoop.six_step_exact_real_structure` gives the exact-real structural DH/mass-matrix equality `massMatrix = massFromLinks` by definitional expansion.
- `RobotFormalEnergy.descriptor_power_identity` and `descriptor_power_remainder_identity` convert descriptor equations into exact power identities, with explicit residual exposure.
- `RobotFormalEnergy.mechanical_energy_power_identity` packages the kinetic, Christoffel/metric, and potential derivatives into the descriptor power form.
- `RouteBDHPowerBinding.implemented_energy_identity` and `implemented_energy_bound` bridge the actual residual ledger to the supply bound, but they remain generic energy bridges rather than a named Newton–Euler syzygy for the deployed Route-B source.

So the audit answer is: there is reusable Lean material, but no already-finished, separately admitted Newton–Euler energy-syzygy sidecar that also closes the true-DH source and coverage obligations.

## Dependencies

Reusable exact core dependencies are narrow and explicit:

- `Mathlib` only for the local Lean sidecars.
- `RouteBSupplyCore` for the exact rational supply/completion algebra.
- `RouteBResidualPower` for the squared-error absorption lemma.
- `RobotFormalEnergy.closed_loop_power_identity` as the generic controller-power cancellation used by `DHPowerBinding`.
- `RouteBAgentExactDHLoop.six_step_exact_real_structure` as the exact-real DH structure lemma.

What is not discharged by these dependencies:

- any actual deployed Julia / Float64 / source-binding theorem,
- any sparse SOS feasibility claim,
- any coverage or first-exit obligation,
- any registry promotion or physical M4 conclusion.

## Exact evidence boundary

Supported by the current evidence:

- exact-real algebraic decomposition of power / energy terms;
- exact DH structural equality at the Lean sidecar level;
- a reusable residual-budget bridge that preserves explicit error terms;
- a successful focused compile of the relevant energy-binding files under the pinned Lean/Mathlib environment.

Not supported by the current evidence:

- a dedicated Newton–Euler energy syzygy theorem tied to the deployed Route-B source;
- any claim that sparse SOS is already solved by the energy bridge;
- any claim that the true-DH source and coverage obligations are already closed;
- any claim that the Lean sidecar alone establishes the physical Route-B admission.

## Next smallest child

Smallest useful child from here:

- a new exact-source Lean sidecar that instantiates the existing generic power bridge on the frozen Route-B Newton–Euler source and exposes the residual ledger explicitly, while keeping sparse SOS and coverage as separate later children.

Concretely, that child should reuse the exact-real DH structure from `RouteBAgentExactDHLoop` and the power bridge pattern from `DHPowerBinding`, but it should stay strictly below any sparse SOS or coverage claim.