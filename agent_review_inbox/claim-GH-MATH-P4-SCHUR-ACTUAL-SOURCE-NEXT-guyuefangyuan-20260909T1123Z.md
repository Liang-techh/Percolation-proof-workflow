---
type: review_claim
review_id: RVW-P4-SCHUR-ACTUAL-SOURCE-NEXT-GYFY-20260909T1123Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
derived_from: '[review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-guyuefangyuan-20260908T2230Z, review-GH-MATH-P4-BLOCK456-SOURCE-REIFICATION-codex-20260908T091914]'
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T11:23:00Z'
lease_expires_at: '2026-09-09T12:23:00Z'
unique_valid_claim: true
replacement_for: none
status: completed
result_path: agent_review_inbox/review_result_RVW-P4-SCHUR-ACTUAL-SOURCE-NEXT-GYFY-20260909T1123Z.md
result_commit: 79dc40e790939ce9b8260d8a3569ce8c4f44f0fd
companion_path: agent_review_inbox/companion_GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT_GYFY_20260909T1141Z.md
companion_commit: 9e93456a99ac5f8264ed64c4206ed5f6ac55f7fe
---
# Review Claim — actual-source block456 Schur refinement

Completed. The exact recorded block456 metric admits a sharp H-orthogonalized third scalar

```text
w6 = 350003*d6 - 50000*d4,
```

for which

```text
d^T H d
 = (3000000/350003)d4^2
 + (4000000/200739)d5^2
 + (1000000/1750155002250009)w6^2.
```

Thus a same-key source packet need only provide exact `d4,d5,w6` identities and quadratic caps to create an independent sharp D cap; it must not reconstruct D from `u/s`. If `d=A y+b`, `w6` should be formed as the signed affine row `(350003*A6-50000*A4)y+(350003*b6-50000*b4)` before intervalization. Actual source binding, H/source reification, coverage, Lean/kernel, independent validation, admission and registry remain pending. This result does not duplicate the separately claimed source-producer task owned by 狂蛮魔尊.
