---
kind: task_claim
task_id: T-P5-201-MIXED-DOMAIN-AUGMENTED-COPOSITIVE-SUPPORT
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-10T01:00:00Z'
lease_expires_at: '2026-09-10T02:00:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-198-QUADRATIC-DOMAIN-RADIAL-CAP-COPOSITIVE-REDUCTION, T-P5-199-POLYHEDRAL-DOMAIN-SELECTOR-LP-DUAL-TRANSPORT, T-P5-200-GAUGE-INVARIANT-AFFINE-AMPLITUDE-CUBIC-ABSORPTION]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — mixed-domain augmented copositive support

## Scope
Close the smallest mixed-domain seam left explicitly open by T-P5-198/T-P5-199/T-P5-200. For selector states `y>=0` constrained simultaneously by a polyhedral cell `C y<=d` and a quadratic cap `y^T P y<=rho`, derive a finite exact certificate for a signed physical support bound `b^T y<=B` that combines both constraints without inverting the selector map and without discarding signed cancellation.

## Non-overlap
Do not redo the pure quadratic rank-one gate of T-P5-198, the pure polyhedral LP dual of T-P5-199, the signed affine-amplitude absorption identity of T-P5-200, source provenance/admission, Float64 enclosure, global coverage, or Lean/kernel verification. The child is only the mixed polyhedral-plus-quadratic support theorem, its exact-gap identity, coordinate/gauge transport, and a fail-closed recession obstruction.

## Intended deliverable
Construct an augmented `(1+y)` copositive matrix from nonnegative multipliers `lambda,tau` such that its copositivity implies `b^T y<=B` on the mixed domain by an exact slack decomposition. Show exact recovery of the pure-polyhedral route, composition with the pure-quadratic route, a physical-coordinate pullback theorem preserving selector gauges, an exact rational example where neither pure route proves the sharp bound but the mixed packet does, and a recession witness that rules out any finite mixed support bound when a zero-quadratic-cost feasible ray carries positive target slope.