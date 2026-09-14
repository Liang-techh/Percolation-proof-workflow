---
kind: task_claim
task_id: T-P5-193-AFFINE-BOX-DEFECT-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T22:58:00Z'
lease_expires_at: '2026-09-09T23:58:00Z'
completed_at: '2026-09-09T23:03:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE, T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY, T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN]'
status: completed
result_path: agent_review_inbox/review-T-P5-193-AFFINE-BOX-DEFECT-BRIDGE-liuguanyi-20260909T2301Z.md
result_commit: d412e3deb9d63b72685ccf3ac202665863b5525d
companion_path: null
companion_commit: null
---
# Review Claim — affine componentwise defect box to viability and Lyapunov margins

## Scope
Close one narrow source-to-math seam left after T-P5-191/192. Assume the external dynamics is an affine core plus a state-dependent componentwise defect box, `e' = A e + c + rho`, `|rho| <= H e + h0`. Derive the exact facet-normal robust viability lift for a polyhedral finite-value cone, and derive a finite sign-fan reduction of the T-P5-192 frozen-selector Lyapunov defect term to ordinary rational copositivity plus linear sign gates.

## Non-overlap
Do not redo T-P5-191's affine Metzler theorem, T-P5-192's selector/KKT fan, the fixed copositivity checker, source provenance/admission, Lean compilation, or physical trajectory coverage. Preserve the distinction between an exact independent box differential inclusion and a merely outer box enclosure of a correlated source residual.

## Intended deliverable
An exact finite-dimensional theorem package: the box support identity, the modified Metzler lift for robust finite-value-cone viability, the selector-gradient sign-fan reduction, finite generator pullback to copositivity and linear sign gates, the constant-defect origin obstruction, and exact counterexamples pinning absolute-value and correlation semantics.
