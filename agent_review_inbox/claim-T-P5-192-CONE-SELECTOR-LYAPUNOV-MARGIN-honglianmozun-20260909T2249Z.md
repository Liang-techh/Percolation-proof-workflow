---
kind: task_claim
task_id: T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T22:49:00Z'
lease_expires_at: '2026-09-09T23:49:00Z'
completed_at: '2026-09-09T22:52:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN, T-P5-189-KERNEL-GAUGE-DINI-LYAPUNOV-ENVELOPE, T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE, T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY]'
status: completed
result_path: agent_review_inbox/review-T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN-honglianmozun-20260909T2250Z.md
result_commit: 86d3e6a59cf11c4d1bd28ffa5a6ab7a66cd20eda
companion_path: null
companion_commit: null
---
# Review Claim — cone-selector Lyapunov decay margin

## Scope
Close one narrow energy-method seam after T-P5-189/190/191: convert a finite family of exact orthant-minimizer selectors into a uniform Dini-Lyapunov decay certificate. Derive the exact frozen-slope quadratic on each selector cone, reduce its nonpositivity to cone-restricted copositivity under generator pullback, and prove exponential energy decay without differentiating optimizer selections across active-face seams. The final review also closes the affine constant-drift extension by an independent first-order cone gate.

## Non-overlap
Do not redo T-P5-190 tangent-domain or derivative-LP proofs, T-P5-191 Metzler viability, source/provenance/admission, receipt work, Lean compilation, or actual Route-B/PDE source binding.

## Delivered
Exact finite-dimensional theorem package for `Phi(e)=min_{u>=0} q_H(u,e)`: selector-cone KKT assumptions; exact branch-energy matrix `Q`; exact frozen derivative matrix `L`; exact separation of affine mixed-degree decay into quadratic and linear cone gates; generator pullback of the quadratic gate to ordinary copositivity; seam-safe upper-Dini decay; exponential comparison; a rational nonsmooth regression with `Phi=min(e1,e2)^2`; and a scalar affine-drift obstruction showing viability does not imply zero-centered Lyapunov decay.