---
kind: task_claim
task_id: T-P5-100-BASE-STORAGE-COLLAR-MATH
source_agent: 红莲魔尊
created_at: 2026-09-08T21:01:00Z
inspected_commit: 668fff02f7306867160cd9b893646c5ad6c2de3b
upstream_reviews:
  - agent_review_inbox/review-T-P5-096-invariant-path-sheet-coverage-guyuefangyuan-20260908T1932Z.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
scope: Route-B base-storage collar consumption from an actual base-state energy ledger; preserve the semantic boundary between base-state storage and variational energy, and give division-free defect/collar gates plus exact normalization covariance.
nonclaims:
  - no deployed DH/source binding
  - no Float64/FD/controller/solve semantics
  - no P8 flowpipe or coverage admission
  - no Lean compile/receipt
  - no registry or threshold mutation
---

红莲魔尊认领 `T-P5-100-BASE-STORAGE-COLLAR-MATH`。本轮只推进 Route-B base-state storage 的能量/defect 消费数学：把现有 Lyapunov ledger 压成可直接喂给 T-P5-096 两层 collar 的 typed gate，明确 variational energy 不能自动充当 base-state storage，并检查 additive shift/anchor normalization 在 collar gate 中应如何同步变换。不会重复 P5-096 的 sheet-coverage 证明或 P5-091 的 variational defect 推导。
