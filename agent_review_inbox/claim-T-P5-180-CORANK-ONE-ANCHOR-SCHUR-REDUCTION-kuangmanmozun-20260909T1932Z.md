---
kind: task_claim
task_id: T-P5-180-CORANK-ONE-ANCHOR-SCHUR-REDUCTION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T19:32:00Z'
lease_expires_at: '2026-09-09T20:32:00Z'
completed_at: '2026-09-09T19:41:00Z'
unique_valid_claim: true
replacement_for: none
derived_from: '[review-T-P5-178-zero-loaded-face-critical-cone-schur-bridge-liuguanyi-20260909T1904Z, review-T-P5-179-canonical-support-descent-psd-face-inheritance-guyuefangyuan-20260909T1931Z, T-P5-173-ROOT-FREE-STRICT-COMPLEMENTARITY-MINOR-GATES]'
status: completed
result_path: agent_review_inbox/review-T-P5-180-CORANK-ONE-ANCHOR-SCHUR-REDUCTION-kuangmanmozun-20260909T1936Z.md
result_commit: 1762b755f4bd220efe4e108d9588f0fa3697f6fa
companion_path: agent_review_inbox/companion-T-P5-180-CORANK-ONE-ANCHOR-SCHUR-REDUCTION-kuangmanmozun-20260909T1940Z.md
companion_commit: a72c0303bcc8c6928fa71e5da063ed40a45d01ca
---
# Review Claim — corank-one anchor deletion Schur reduction

## Scope
Close the corank-one zero-residual critical-row seam left after T-P5-178/T-P5-179. For an active PSD block A with strictly positive kernel generator z and corank exactly one, prove that every critical row b with b^T z=0 is automatically in range(A); choose any positive anchor coordinate, delete that active row/column to obtain an SPD principal minor, and reduce the mixed critical-cone problem to a root-free Schur/copositivity test using only that invertible principal minor. Derive determinant/adjugate formulas and a scalar one-row specialization.

## Non-overlap
Do not redo T-P5-178's general hidden-kernel/range-solve theorem, T-P5-179 support canonicalization, T-P5-173 strict-complementarity gate, generic copositivity enumeration, provenance/admission/audit, source binding, or Lean compilation. Preserve the higher-corank obstruction as a fail-closed boundary.

## Intended deliverable
Exact theorem and proof, anchor-invariance statement, inverse-free rational checker form, one-critical-row determinant criterion, explicit higher-corank counterexample, formalizable theorem statements, and next-step routing guidance.
