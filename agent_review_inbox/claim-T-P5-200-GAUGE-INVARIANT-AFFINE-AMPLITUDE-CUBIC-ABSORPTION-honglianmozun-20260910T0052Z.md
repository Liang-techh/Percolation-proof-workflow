---
kind: task_claim
task_id: T-P5-200-GAUGE-INVARIANT-AFFINE-AMPLITUDE-CUBIC-ABSORPTION
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-10T00:52:00Z'
lease_expires_at: '2026-09-10T01:52:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-196-SIGN-DEFINITE-QUADRATIC-RESCUE, T-P5-197-WEIGHTED-RADIAL-CUBIC-ABSORPTION, T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — gauge-invariant affine-amplitude cubic absorption

## Scope
Close the smallest energy/Lyapunov seam exposed by T-P5-199's non-injective-selector obstruction. When the affine generator amplitude is a genuine physical scalar `a(e)=h0+h^T e`, retain its exact signed pullback `b=V^T h` instead of replacing it by a nonnegative coefficient majorant `beta`. Prove that any exact upper support bound `b^T y<=B` on the consumed cell absorbs the T-P5-196 cubic term back into the existing quadratic copositivity packet, with an explicit nonnegative remainder and no representation-gauge blowup.

## Non-overlap
Do not redo T-P5-198 quadratic-domain radial-cap work, T-P5-199 generic selector LP/Farkas theorem, T-P5-197 weighted-gauge majorant algebra, source provenance/admission, actual-domain extraction, Float64 enclosure, or Lean/kernel verification. The new child is specifically the signed exact-amplitude branch and its gauge invariance.

## Intended deliverable
An exact theorem with `b=V^T h` showing
`(h0+b^T y)(c^T y+y^TQy) <= h0 c^T y + y^T[(h0+B)Q+sym(b c^T)]y`,
with gap `(B-b^T y)y^TQy`; a polyhedral support certificate that permits signed `b`; proof that every nonnegative selector gauge `r` with `Vr=0` satisfies `b^T r=0`; a compact-state counterexample where every nonnegative majorant `beta>=b` is unbounded but the exact signed branch closes; and fail-closed boundaries for nonphysical selector slopes or sign-changing amplitudes.