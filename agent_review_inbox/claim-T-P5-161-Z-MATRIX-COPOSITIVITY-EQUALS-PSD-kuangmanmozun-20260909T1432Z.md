---
type: review_claim
review_id: RVW-T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD-KMMZ-20260909T1432Z
task_id: T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T14:32:00Z'
lease_expires_at: '2026-09-09T15:32:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-154-UNIFORM-ADDITIVE-SIMPLEX-FLOOR-kuangmanmozun-20260909, review-T-P5-158-FINITE-SUPPORT-KKT-COPOSITIVITY-DECISION-honglianmozun-20260909T1400Z, review-T-P5-159-MONOTONE-SYMBOLIC-FLOOR-BRACKETING-liuguanyi-20260909T1410Z]'
---
# Review Claim — Z-matrix copositivity equals PSD fast path

## Scope
Attack a disjoint mathematical closure seam after T-P5-154/158/159: identify a structural sign regime in which the fixed-floor copositivity obligation collapses exactly to ordinary PSD, eliminating support enumeration without duplicating T-P5-160's degenerate-kernel work.

## Route
1. Prove for a real symmetric Z-matrix (all off-diagonal entries nonpositive) that copositivity is equivalent to PSD, using the absolute-value domination q(|x|) <= q(x).
2. Specialize this to the simplex floor matrix M_D with off-diagonal sign gate K_ij + D(g_i+g_j) <= 0.
3. Give exact rational checker consequences (LDL/principal PSD witness) and a sharp family where the fast path detects the true multiway floor.
4. Give a counterexample showing the sign gate is essential: generic copositive matrices need not be PSD.
5. Record minimal Lean theorem statements and fail-closed boundaries; no source/provenance/admission work.
