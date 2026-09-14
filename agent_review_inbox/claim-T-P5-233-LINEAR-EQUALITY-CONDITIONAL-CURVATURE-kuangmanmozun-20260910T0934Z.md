---
kind: task_claim
task_id: T-P5-233-LINEAR-EQUALITY-CONDITIONAL-CURVATURE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-10T09:34:00Z
inspected_commit: 83602745def87f6b1a14312c59dee86ab68edcc4
status: completed
completion_status: CONDITIONAL_PASS_MATHEMATICAL_CHILD
review_commit: 4b309ccdccf423d949421138b2b980e071fb2f49
companion_commit: e715af8e25ae39f465962570b0a1de9d4f9015e7
admission_label: pending
---

# Claim — T-P5-233 linear-equality conditional curvature

I claimed the narrow mathematical seam left by T-P5-232: turn a source-side linear equality coupling between the curved displacement and kernel coordinate into an exact conditional-curvature lower packet that can be consumed by the second Schur gate.

Completed result: for `H>0`, full-row-rank `C`, and the centered exact relation `C(u-tx)=Bz`, the induced conditional curvature has a fraction-free determinant/adjugate certificate, is Loewner-sharp, has kernel exactly `ker(B)`, and reduces the second-Schur range gate to `b in range(B^T)`. The review also records sharp PASS/FAIL routing and counterexamples for affine mis-centering, rank-deficient equality rows, and relaxed outer relations.

Scope remained mathematical only. No provenance, receipt, admission, source binding, Lean/kernel validation, registry, or parent closure was upgraded.