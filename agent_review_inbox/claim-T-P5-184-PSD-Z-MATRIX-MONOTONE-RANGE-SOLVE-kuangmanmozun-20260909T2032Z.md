---
kind: task_claim
task_id: T-P5-184-PSD-Z-MATRIX-MONOTONE-RANGE-SOLVE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T20:32:00Z'
lease_expires_at: '2026-09-09T21:32:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT, T-P5-161-Z-MATRIX-COPOSITIVITY-EQUALS-PSD]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — PSD Z-matrix monotone range solve

## Scope
Close one narrow mathematical gate left by T-P5-182: when the PSD eliminated block is also a symmetric Z-matrix and the desired right-hand side is entrywise nonnegative, prove that ordinary linear consistency already implies existence of a nonnegative solve. Derive a root-free positive-part construction, its columnwise matrix form, and the exact specialization `F=-B^T` needed by the orthant-feasible Schur transport.

## Non-overlap
Do not redo T-P5-182's Schur-complement equivalence, T-P5-183's complementary/nonzero-residual transport, generic LP/Farkas feasibility, source/provenance/admission audit, Lean compilation, or copositivity support enumeration. If the Z-sign gate fails, return a routing condition rather than a mathematical failure.

## Intended deliverable
Elementary exact-real/rational proof; matrix-column corollary; checker packet using any ordinary rational solve followed by positive-part truncation; counterexamples showing PSD, Z-sign, and range/consistency hypotheses are all material; suggested theorem statements and next integration point.
