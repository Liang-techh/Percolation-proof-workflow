---
kind: task_claim
task_id: T-P5-189-KERNEL-GAUGE-DINI-LYAPUNOV-ENVELOPE
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T21:49:00Z'
lease_expires_at: '2026-09-09T22:49:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION, T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE, T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN, T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — kernel-gauge observable and Dini Lyapunov envelope

## Scope
Close one narrow energy-method seam left after T-P5-187/188: the reduced orthant-minimized energy is value-continuous across valid active-face overlaps, but a singular kernel gauge can still change the retained observable `B u` and hence create a genuine derivative kink. Prove an exact frozen-state branch-switch identity, a supergradient/nondifferentiability criterion, and a selection-free upper-Dini Lyapunov inequality that remains sound through switching faces without differentiating an arbitrary optimizer selection.

## Non-overlap
Do not redo T-P5-185/186 fan construction or recession gates, T-P5-187 residual/value uniqueness, T-P5-188 minimizer-set characterization, source/provenance/admission, receipt work, Lean compilation, or global physical coverage. Do not claim global differentiability merely from pointwise kernel invisibility.

## Intended deliverable
Exact finite-dimensional theorem package for `Phi(e)=min_{u>=0} q_H(u,e)`: kernel-gauge observable criterion `B(z-y)`, branch-switch identity under external perturbations, nondifferentiability when active minimizers have distinct `B u`, an upper-Dini Lyapunov bound valid for every active minimizer, and a rational copositive regression showing a smooth full quadratic can reduce to a kinked Lyapunov envelope.