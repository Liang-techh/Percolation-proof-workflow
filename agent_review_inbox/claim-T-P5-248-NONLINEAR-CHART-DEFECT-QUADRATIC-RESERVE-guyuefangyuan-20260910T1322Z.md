---
kind: task_claim
task_id: T-P5-248-NONLINEAR-CHART-DEFECT-QUADRATIC-RESERVE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T13:22:00Z
inspected_commit: cc3c1f109dbd8c56b63bb584ad4763be831da8bc
status: completed
admission_label: pending
result_review: review-T-P5-248-nonlinear-chart-defect-quadratic-reserve-guyuefangyuan-20260910T1322Z
---

# Claim — T-P5-248 nonlinear chart defect quadratic reserve

认领 T-P5-247 明确留下的最小独立数学 seam：在精确可逆仿射部分 `y=Pz+h` 已经零成本归一化之后，研究非线性/近似 chart `y=Pz+h+r(z)` 的 defect 如何消费已有严格二次 reserve。

本轮已完成数学 child 并写回 immutable review/companion。核心包括：一阶 relative defect cone 的 center-gradient sharp obstruction；`a0=0` 分支的 exact homogeneous S-lemma LMI；二阶 remainder 恢复 quadratic absorption；以及独立的 physical source-ellipsoid inclusion cone-LMI。数学 only：不做 provenance/receipt/admission/re-audit，不声称 Lean/kernel、真实 source binding、tube/cell coverage、Float64 或 parent closure。