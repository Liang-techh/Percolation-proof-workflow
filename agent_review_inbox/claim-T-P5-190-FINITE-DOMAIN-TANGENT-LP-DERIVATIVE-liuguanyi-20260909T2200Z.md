---
kind: task_claim
task_id: T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T22:00:00Z'
lease_expires_at: '2026-09-09T23:00:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN, T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION, T-P5-189-KERNEL-GAUGE-DINI-LYAPUNOV-ENVELOPE]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — finite-domain tangent cone and exact one-sided reduced-energy derivative

## Scope
Close one narrow boundary/trajectory seam left by T-P5-189. For the PSD inherited orthant quadratic, characterize exactly which external boundary directions preserve local finiteness by the critical recession cone; then prove that along every such feasible direction the one-sided derivative of the reduced value is the minimum frozen slope over the T-P5-188 minimizer slice. Compress that slope to an exact LP/primal-dual certificate on the zero-residual coordinates.

## Non-overlap
Do not redo T-P5-186 recession-fan construction, T-P5-187/188 pointwise minimizer compression, or T-P5-189 Dini upper-bound argument. Do not perform source/provenance/admission/re-audit, Lean compilation, or physical coverage work. A direction leaving the finite-value parameter cone is a mathematical obstruction to this reduced-energy consumer, not a claim that the underlying ODE/PDE is impossible.

## Intended deliverable
An exact finite-dimensional theorem package: the polyhedral finite-value parameter cone; its tangent cone at a boundary state; a sharp critical-recession obstruction for directions that immediately make the reduced value `-infinity`; an exact right directional derivative formula on feasible rays; and an inverse-free rational LP primal/dual packet for the derivative using the T-P5-188 zero-residual affine slice.
