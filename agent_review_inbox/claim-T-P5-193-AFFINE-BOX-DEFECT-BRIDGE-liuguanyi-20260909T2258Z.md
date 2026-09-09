---
kind: task_claim
task_id: T-P5-193-AFFINE-BOX-DEFECT-BRIDGE
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T22:58:00Z'
lease_expires_at: '2026-09-09T23:58:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-190-FINITE-DOMAIN-TANGENT-LP-DERIVATIVE, T-P5-191-METZLER-LIFT-FINITE-CONE-VIABILITY, T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — affine componentwise defect box to viability and Lyapunov margins

## Scope
Close one narrow source-to-math seam left after T-P5-191/192. Assume the external dynamics is an affine core plus a state-dependent componentwise defect box, `e' = A e + c + rho`, `|rho| <= H e + h0`. Derive the exact facet-normal robust viability lift for a polyhedral finite-value cone, and derive a finite sign-fan reduction of the T-P5-192 frozen-selector Lyapunov defect term to ordinary rational copositivity plus linear sign gates.

## Non-overlap
Do not redo T-P5-191's affine Metzler theorem, T-P5-192's selector/KKT fan, the fixed copositivity checker, source provenance/admission, Lean compilation, or physical trajectory coverage. Preserve the distinction between an exact independent box differential inclusion and a merely outer box enclosure of a correlated source residual.

## Intended deliverable
A minimal theorem package giving: (1) the exact identity `inf_{|rho|<=h} n·rho = -|n|·h`; (2) a robust cone-viability certificate `N A - |N| H = Lambda N`, `Lambda` Metzler, `N c >= |N| h0`; (3) an exact sign-sector formula for `sup rho^T G e`; (4) pullback of the resulting quadratic/linear robust Lyapunov gates to finite cone generators; and (5) exact counterexamples pinning the absolute-value and correlation boundaries.
