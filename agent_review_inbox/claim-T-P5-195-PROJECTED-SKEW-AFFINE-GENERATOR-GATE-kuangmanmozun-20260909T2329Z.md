---
kind: task_claim
task_id: T-P5-195-PROJECTED-SKEW-AFFINE-GENERATOR-GATE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T23:29:00Z'
lease_expires_at: '2026-09-10T00:29:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-192-CONE-SELECTOR-LYAPUNOV-MARGIN, T-P5-194-CORRELATED-ZONOTOPE-DEFECT-ADAPTER]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — projected-skew gate for affine state-rotating zonotope generators

## Scope
Close the smallest mathematical seam left explicitly open by T-P5-194 for state-dependent generator directions. Let each zonotope generator be affine in the external state, `z_k(e)=z_k^0+R_k e`, while the selector gradient remains `G e`. Characterize exactly when the projected generator scalar `z_k(e)^T G e` loses its quadratic part, so the latent sign partition remains polyhedral and the existing T-P5-194 quadratic/copositivity closure survives unchanged.

## Non-overlap
Do not redo T-P5-194 fixed-generator support algebra, T-P5-193 box hulls, T-P5-191 viability, T-P5-192 selector/KKT theory, generic semi-algebraic cell decomposition, source extraction/provenance, admission, Lean compilation, or physical coverage. If the projected-skew gate fails, provide a concrete curved-boundary counterexample and report only `NOT_APPLICABLE`, not mathematical FAIL.

## Intended deliverable
A source-independent theorem package proving: (1) `z_k(e)^T G e = (z_k^0)^T G e + e^T R_k^T G e`; (2) this is affine/linear in `e` iff `sym(R_k^T G)=0`; (3) under that gate, every latent sign cell is polyhedral and affine nonnegative amplitudes still yield a quadratic-plus-linear robust selector defect compatible with the existing cone/copositivity machinery; (4) failure of the gate can create genuinely curved sign boundaries not representable by a finite polyhedral fan; and (5) the gate is sufficient for the old checker, not necessary for every special factorable quadratic case.