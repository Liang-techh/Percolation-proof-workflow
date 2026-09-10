---
kind: task_claim
task_id: T-P5-248-NONLINEAR-CHART-DEFECT-QUADRATIC-RESERVE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T13:22:00Z
inspected_commit: cc3c1f109dbd8c56b63bb584ad4763be831da8bc
status: claimed
admission_label: pending
---

# Claim — T-P5-248 nonlinear chart defect quadratic reserve

认领 T-P5-247 明确留下的最小独立数学 seam：在精确可逆仿射部分 `y=Pz+h` 已经零成本归一化之后，研究非线性/近似 chart `y=Pz+h+r(z)` 的 defect 如何消费已有严格二次 reserve。

本轮目标是给出一个 exact homogeneous cone/S-lemma gate：当 `r` 只是一阶 relative defect 时，刻画 target defect `2(l+G(Pz+h))^T r+r^TGr` 何时能被 `rho*z^TMz` 吸收；同时证明 affine-center gradient 非零时的 sharp obstruction，并给出二阶 remainder `r=O(||z||^2)` 恢复 quadratic absorption 的条件。另行给出 physical source ellipsoid inclusion 的 exact cone-LMI，避免把 target reserve 与 source coverage 混同。数学 only：不做 provenance/receipt/admission/re-audit，不声称 Lean/kernel、真实 source binding、tube/cell coverage、Float64 或 parent closure。