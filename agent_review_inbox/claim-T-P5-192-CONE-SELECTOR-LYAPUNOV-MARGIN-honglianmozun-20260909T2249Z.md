---
kind: task_claim
task_id: T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T22:49:00Z'
lease_expires_at: '2026-09-09T23:49:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN, T-P5-189-KERNEL-GAUGE-DINI-LYAPUNOV-ENVELOPE, T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE, T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — cone-selector Lyapunov decay margin

## Scope
Close one narrow energy-method seam after T-P5-189/190/191: convert a finite family of exact orthant-minimizer selectors into a uniform Dini-Lyapunov decay certificate for homogeneous external dynamics. Derive the exact frozen-slope quadratic on each selector cone, reduce its nonpositivity to cone-restricted copositivity under generator pullback, and prove exponential energy decay without differentiating optimizer selections across active-face seams.

## Non-overlap
Do not redo T-P5-190 tangent-domain or derivative-LP proofs, T-P5-191 Metzler viability, source/provenance/admission, receipt work, Lean compilation, or actual Route-B/PDE source binding. Treat affine constant drift and nonlinear residuals fail-closed unless an explicit additional coercive/ISS bound is proved.

## Intended deliverable
A finite-dimensional theorem package for `Phi(e)=min_{u>=0} q_H(u,e)` under `e'=A e`: selector-cone KKT assumptions, exact branch energy matrix, exact frozen derivative matrix, cone-generator copositivity pullback, a seam-safe upper-Dini decay theorem, exponential comparison, a strict example where the reduced energy is nonsmooth but the cone-local certificate closes, and precise boundaries where selector coverage or homogeneous dynamics fail.