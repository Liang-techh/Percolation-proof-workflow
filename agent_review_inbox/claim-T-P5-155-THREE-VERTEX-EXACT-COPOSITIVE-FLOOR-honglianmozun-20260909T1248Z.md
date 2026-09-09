---
type: review_claim
review_id: RVW-T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR-HLMZ-20260909T1248Z
task_id: T-P5-155-THREE-VERTEX-EXACT-COPOSITIVE-FLOOR
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T12:48:00Z'
lease_expires_at: '2026-09-09T13:48:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909T1233Z]'
---
# Review Claim — three-vertex exact copositive floor

## Scope
Advance the exact copositivity seam left by T-P5-154 without duplicating its generic PSD fast path. Specialize the uniform additive-floor problem to the first genuinely multiway case of three homothetic vertices with a common cell scale `g`, and derive a finite exact rational active-set criterion for the sharp floor over the full 2-simplex.

## Route
1. Reduce the three-vertex floor to minimizing `q(x,y,z)=a xy+b xz+c yz` on `x+y+z=1`, `x,y,z>=0`.
2. Prove all boundary minima are captured by the three exact edge midpoint gates.
3. Derive the unique possible isolated interior stationary point and a division-free test for when it lies in the open simplex.
4. Show degenerate interior stationary sets touch the boundary at the same value, so they create no extra hidden floor.
5. Package the result as a root-free exact rational checker and give sharp regressions, including the T-P5-154 barycentric counterexample.

No source admission, provenance/receipt audit, runtime/Float64 claim, registry mutation, Lean/kernel validation, or independent re-audit is in scope.