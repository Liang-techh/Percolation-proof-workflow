---
kind: task_claim
task_id: T-P5-196-SIGN-DEFINITE-QUADRATIC-RESCUE
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T23:52:00Z'
lease_expires_at: '2026-09-10T00:52:00Z'
completed_at: '2026-09-10T00:00:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN, T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER, T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE]'
status: completed
result_path: agent_review_inbox/review-T-P5-196-SIGN-DEFINITE-QUADRATIC-RESCUE-honglianmozun-20260909T2359Z.md
result_commit: af69121cff7bbb476aea1c6b528936d872f3e015
companion_path: null
companion_commit: null
---
# Review Claim — sign-definite quadratic rescue for failed projected-skew sectors

## Scope
Close the smallest mathematical seam explicitly left by T-P5-195. For one selector cone `C=cone(V)` and one state-rotating projected generator scalar

`phi(e)=ell^T e + e^T S e`, with `S=S^T`,

characterize exactly when `phi` has a fixed sign on the whole cone without semialgebraic subdivision, using only the existing cone/copotisivity machinery. Then determine what this does and does not buy for a Lyapunov robust-defect term `a(e)|phi(e)|` when `a(e)=h^T e+h0 >= 0` is affine.

## Non-overlap
Do not redo T-P5-195 projected-skew equivalence, T-P5-194 fixed-generator zonotope support algebra, generic semialgebraic cell decomposition, source extraction/provenance, receipt/admission, Lean compilation, or physical coverage. In particular, do not claim that fixed sign alone preserves quadratic degree when the amplitude has nonzero linear growth.

## Intended deliverable
A source-independent theorem package proving: (1) on an unbounded cone, `phi>=0` iff its linear part and homogeneous quadratic part are separately nonnegative; similarly for `phi<=0`; (2) for `C=cone(V)`, this is exactly an entrywise generator test for `ell` plus one pulled-back copositivity test for `S`; (3) under fixed sign, the absolute value disappears exactly; (4) constant amplitudes return to the T-P5-192 quadratic-plus-linear route; and (5) affine amplitudes generically create a positive cubic robust defect, with an exact ray-scaling obstruction to global quadratic-rate Lyapunov closure unless the cubic leading form vanishes on the consumed cone.