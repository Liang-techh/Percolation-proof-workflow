---
kind: task_claim
task_id: T-P5-252-SOURCE-SLICE-PARTIAL-METRIC-COERCIVITY
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T14:18:39Z
inspected_commit: af5077437194e07f0418e86211c48cf87fe8d969
status: completed
admission_label: pending
result_review: review-T-P5-252-source-slice-partial-metric-coercivity-guyuefangyuan-20260910T1418Z
---

# Claim — T-P5-252 source-slice partial-metric coercivity

本轮已完成数学 child 并写回 immutable review/companion。核心结论：ambient `W>=0` 可以奇异；若 `range(D) ∩ ker(W)={0}`，则该 source residual image 上等价存在 `gamma>0` 使 `D^T W D-gamma D^T D>=0`。在 exact-center affine source slice `C xi0=0, D=CN` 上，这给出 partial-tube 到 Euclidean residual tube 的定量转换，并在 `eta=0` 时安全升级 `WCxi=0 -> Cxi=0`。同时给出 exact rank/kernel 等价、rational PSD-gap certificate、失败 witness 与 affine-offset 反例。数学 only；不做 provenance/receipt/admission/re-audit，不声称 Lean/kernel、真实 source binding、tube/cell coverage、Float64 或 parent closure。