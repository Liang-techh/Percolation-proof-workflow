---
kind: task_claim
task_id: T-P5-272-MULTICONSTRAINT-SEMIALGEBRAIC-FIBER-ARRANGEMENT
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T19:01:00Z
inspected_commit: 51b169287280752164a02827b76340dd797ef57b
status: claimed
admission_label: pending
---

# Claim — T-P5-272 multi-constraint semialgebraic fiber arrangement

承接 T-P5-271 明确保留的下一条数学 seam：对同一个一维 fiber 变量 `s`，source 由有限个多项式原子 `P_i(q,s) ⋚ 0`（`⋚ ∈ {>,>=,=,<=,<}`）经有限 Boolean 公式组合给出时，证明在有限 exceptional `q`-set 之外存在一个共同 ordered-root arrangement，使每条 open strip 上所有原子真值固定，边界 root branch 的激活/切换可由 pairwise resultants 与 multiplicity parity 精确追踪，并保留 equality-only singleton components。

本轮目标是给出 source-to-math 的实质 theorem：把一般有限 Boolean 一维 semialgebraic fiber 在 `q` 轴上压成有限 cell atlas，允许逐 component 消费既有 quadratic LEFT/RIGHT/INTERIOR clamp；同时证明仅对 weak inequalities 做闭包替换会改变 strict/equality 语义，因此 dispatcher 必须显式记录 boundary truth vector。只做数学证明与最小形式化接口，不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、独立验证或 parent closure。