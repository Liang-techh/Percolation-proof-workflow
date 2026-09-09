---
type: review_claim
review_id: RVW-T-P5-166-NEGATIVE-FOREST-SHARED-DIAGONAL-BUDGET-HLMZ-20260909T1552Z
task_id: T-P5-166-NEGATIVE-FOREST-SHARED-DIAGONAL-BUDGET
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: '2026-09-09T15:52:00Z'
lease_expires_at: '2026-09-09T16:52:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-kuangmanmozun-20260909T1442Z, review-T-P5-164-NEGATIVE-STAR-EDGE-DECOMPOSITION-guyuefangyuan-20260909T1521Z, review-T-P5-165-NEGATIVE-GRAPH-COMPONENT-FACTORIZATION-kuangmanmozun-20260909T1540Z]'
---
# Review Claim — negative-forest shared diagonal budget

## Scope
Advance the fixed-D mixed-sign copositivity lane after T-P5-165 without duplicating the exact negative-star or generic support/KKT results. For a negative-edge component whose strictly negative graph is a forest, isolate the negative skeleton, prove an exact rational shared-diagonal/leaf-elimination PSD certificate for that skeleton, and lift it to a copositivity certificate for the original matrix by retaining all nonnegative cross terms.

## Route
1. Prove the direct shared-diagonal edge-block certificate: split each diagonal budget among incident negative edges plus a nonnegative residual; require each 2x2 edge block PSD.
2. Prove exactness of this certificate for a forest-supported Z skeleton by leaf Schur elimination, including the zero-pivot obstruction.
3. Give a root-free/rational checker form and a three-node path example showing why independent edge checks can double-spend a shared vertex budget.
4. Give a sharp boundary example where T-P5-164 succeeds but the forest skeleton certificate fails, proving this is a sufficient fast path for mixed-sign matrices rather than a replacement for the exact star theorem.
5. Record only mathematical/source-facing obligations; no source admission, provenance audit, Lean compile, runtime claim, or registry mutation.
