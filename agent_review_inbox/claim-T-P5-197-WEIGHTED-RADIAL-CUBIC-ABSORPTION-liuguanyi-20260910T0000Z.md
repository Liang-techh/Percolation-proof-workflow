---
kind: task_claim
task_id: T-P5-197-WEIGHTED-RADIAL-CUBIC-ABSORPTION
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-10T00:00:00Z'
lease_expires_at: '2026-09-10T01:00:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN, T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER, T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE, T-P5-196-SIGN-DEFINITE-QUADRATIC-RESCUE]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — weighted radial absorption of the T-P5-196 cubic defect

## Scope
Close the smallest bounded-domain mathematical seam left explicitly by T-P5-196. On one selector cone `C=cone(V)`, assume the projected generator scalar has fixed sign so that after pullback `e=Vy`, `y>=0`, its homogeneous pieces are a nonnegative linear form `c^T y` and a copositive quadratic form `y^T Q y`. Let the affine amplitude be `h0+b^T y>=0` and let the actual consumed sector carry an exact weighted radial cap `a^T y<=R` with `a_j>0`.

Prove an exact-rational bridge that absorbs the positive cubic term `(b^T y)(y^T Q y)` back into a quadratic form using only the radial cap, with a sharp scalar domination constant computable by generator ratios. Then expose the resulting matrix/linear packet in the same copositivity shape consumed by T-P5-192.

## Non-overlap
Do not redo T-P5-196 fixed-sign characterization, T-P5-195 projected-skew theorem, T-P5-194 zonotope support algebra, semialgebraic decomposition, source extraction/provenance, admission, Lean compilation, or physical coverage. Do not claim the radial cap is available from source unless separately bound.

## Intended deliverable
A source-independent theorem package proving: (1) the sharp weighted generator inequality `b^T y <= kappa a^T y` on `y>=0` with `kappa=max_j b_j/a_j` under `b>=0`, `a>0`; (2) on `a^T y<=R`, the T-P5-196 cubic term is bounded by `kappa R y^TQy`; (3) the whole affine-amplitude fixed-sign defect is bounded by one explicit linear term plus one explicit symmetric quadratic form; (4) the resulting Lyapunov gate reduces to the existing copositivity/entrywise machinery; and (5) failure of the radial-cap premise is a routing obstruction, not a mathematical FAIL for the source system.