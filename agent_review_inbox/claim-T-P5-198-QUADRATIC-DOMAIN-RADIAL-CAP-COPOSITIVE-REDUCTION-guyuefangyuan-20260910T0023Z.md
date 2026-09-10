---
kind: task_claim
task_id: T-P5-198-QUADRATIC-DOMAIN-RADIAL-CAP-COPOSITIVE-REDUCTION
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-10T00:23:00Z'
lease_expires_at: '2026-09-10T01:23:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN, T-P5-197-WEIGHTED-RADIAL-CUBIC-ABSORPTION]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — quadratic-domain radial-cap copositive reduction

## Scope
Close the smallest domain-math seam left by T-P5-197. Replace its externally supplied weighted radial cap `w^T y <= R` by an exact finite algebraic condition when the consumed selector sector already carries a homogeneous quadratic domain cap `y^T P y <= rho`. Derive a root-free/copotisivity equivalence for a proposed rational radial bound and feed it directly into the cubic-to-quadratic absorption coefficient.

## Non-overlap
Do not redo T-P5-197 weighted-gauge algebra, T-P5-192 selector Dini/copotisivity theory, source provenance/admission, actual-domain extraction, Float64 enclosure, or Lean/kernel verification. Do not claim a quadratic domain exists unless supplied by the source/domain lane.

## Intended deliverable
An exact theorem characterizing `beta^T y <= B` on `{y>=0 : y^T P y <= rho}` by copositivity of `B^2 P - rho beta beta^T`, including zero-curvature recession directions, a rational checker form with no square roots/inverses, the sharpened T-P5-197 defect matrix using `B` directly, and a counterexample showing PSD is unnecessarily strong relative to orthant copositivity.
