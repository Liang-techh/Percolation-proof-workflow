---
kind: task_claim
task_id: T-P5-268-CONCAVE-QUADRATIC-PARAMETER-CLAMP
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T18:00:00Z
inspected_commit: e30ed917daeb5fa5ad46450b7b01b1110990749b
status: claimed
admission_label: pending
---

# Claim — T-P5-268 concave quadratic parameter clamp

承接 T-P5-267 明确留下的 concave-quadratic parameter seam。只做数学层：对 `A(q,s)=A0(q)+A1(q)s-A2(q)s^2`、`s∈[a,b]`、`A2(q)>0`，证明参数最大值的 exact clamped-vertex 分支；将 interior maximum 的除法表达式改写为 fraction-free polynomial gate；给出由一元 Sturm/Bernstein sign cells 驱动的有限 exact dispatcher，并明确 `A2=0`、moving fiber、outer box、source membership 与 zero-margin 的边界。目标是把 T-P5-267 的 vertex lane 扩展到第一个真实 interior maximizer；不做 provenance/receipt/admission/re-audit，不宣称 source binding、coverage、Float64、Lean/kernel 或 parent closure。