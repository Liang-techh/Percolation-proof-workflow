---
kind: task_claim
task_id: T-P5-213-ACTIVE-KERNEL-DEBIT-DICHOTOMY
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-10T04:22:00Z
inspected_commit: 7fcad4d53fbddf6307e972b556f1c502c45fea0b
status: completed
completed_at: 2026-09-10T04:28:00Z
review_id: review-T-P5-213-active-kernel-debit-dichotomy-guyuefangyuan-20260910T0426Z
review_commit: 94648fb1f758e81f3755e839f98f55283a551d20
companion_commit: b434b9e3a1029ef955276145dc9c46a04c85bd93
---

# Claim — T-P5-213 active-kernel debit dichotomy

Completed by `古月方源`.

The result closes a disjoint mathematical child of T-P5-210/T-P5-212 at the debit-witness layer, while reusing rather than duplicating the T-P5-178 mixed Schur/range theorem.

Main result: under the T-P5-210 copositive common-zero hypotheses and the T-P5-178 endpoint zero-sheet hypotheses, with a complete active kernel basis `N` and complete zero-loaded reduced-kernel generator packet, a positive second-order debit witness exists iff

`N^T P N != 0 OR M0 != 0`.

If the active pullback is nonzero, a pure-active kernel vector is already a witness. If it vanishes, PSD plus mixed-cone nonnegativity force all active/reduced debit cross terms to vanish, reducing exactly to T-P5-212.

See the linked immutable review and companion for assumptions, regressions, formalization targets, and open source/coverage boundaries.
