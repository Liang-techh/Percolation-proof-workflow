---
kind: task_claim
task_id: T-P5-151-VERTEXWISE-END-TO-END-ROBUST-RESET
source_agent: 红莲魔尊
created_at: 2026-09-09T11:50:00Z
inspected_commit: c23a72cb79099f36724f327011bf628c20a8186e
status: completed
completed_at: 2026-09-09T11:55:00Z
review_commit: 0b8117e5f6b829f1e6bc161d1e0cb80ee2fd3671
review_path: agent_review_inbox/review-T-P5-151-VERTEXWISE-END-TO-END-ROBUST-RESET-honglianmozun-20260909T1150Z.md
---

# Claim — T-P5-151 vertexwise end-to-end robust reset

No new explicit 梁智炜 mention for 红莲魔尊 was found in the inspected queue/board snapshot. T-P5-150 has already closed the shared-cap polytope seam and explicitly leaves parameter-dependent caps available when a downstream theorem can consume them.

This child does not repeat T-P5-148/149/150. It closes the narrower mathematical question: avoid forcing all uncertainty vertices through one shared augmented Schur cap by carrying each vertex all the way through the bounded quotient-cell reset/Lyapunov multiplier and only then taking a common scalar reset floor.

Completed deliverable: exact vertexwise robust-reset theorem, nonnegative gap decomposition, strict separation example (`R=1/4`: exact vertexwise floor `1` versus every shared-matrix-cap-first route at least `5/4`), and fail-closed range/domain boundaries. No source admission, provenance audit, Lean compilation, runtime/Float64 claim, coverage promotion, or registry mutation.