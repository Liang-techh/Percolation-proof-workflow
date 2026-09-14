---
kind: task_claim
task_id: T-P5-256-STRUCTURED-HESSIAN-TENSOR-GRAM-MAJORANT
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T15:19:28Z
inspected_commit: e26b81d7442c0520b19ff292d29ed1b6313e73fd
status: completed
admission_label: pending
result_commit: e41a4f7fab94f40593cdbe66ae7c23094a8e7134
---

# Claim — T-P5-256 Structured Hessian tensor Gram majorant

认领 T-P5-255 明确保留的 structured-Hessian source seam。目标是在纯数学层把 polynomial/affine Hessian 的各向异性 tensor 结构直接压成 `B(theta)^T B(theta) <= kappa (theta^T M theta) D^T D` 的 exact PSD producer packet，而不退化成 ambient operator norm：先建立 coefficient outer-Gram / completely-positive transport lemma，再给 source ellipsoid 上 homogeneous tensor powers 的 graded `O(R^{r-1})` majorant，并用 rational weighted-Young 合并多个 degree；同时明确 singular source metric、`ker(D)` mixed-branch obstruction 与 radial-only fallback 的边界。数学 only；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel 或 parent closure。

完成：正式数学 review 已写入 commit `e41a4f7fab94f40593cdbe66ae7c23094a8e7134`；中文协作 companion 为 `0e6329bdac186edfc7d51bf1e0b4f1d14d31f133`。