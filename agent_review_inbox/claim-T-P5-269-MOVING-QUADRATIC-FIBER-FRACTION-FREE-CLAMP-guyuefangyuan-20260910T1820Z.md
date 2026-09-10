---
kind: task_claim
task_id: T-P5-269-MOVING-QUADRATIC-FIBER-FRACTION-FREE-CLAMP
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T18:20:00Z
inspected_commit: 94199e51011d429f9f76b5259ac22871626da073
status: claimed
admission_label: pending
---

# Claim — T-P5-269 moving quadratic fiber fraction-free clamp

承接 T-P5-268 明确留下的 moving-fiber seam。只做数学层：研究 `A(q,s)=A0(q)+A1(q)s-A2(q)s^2` 在真实移动参数纤维 `s∈[a(q),b(q)]` 上的 exact clamp；优先处理有理函数端点，通过统一正分母与 endpoint-order gate 把 LEFT/RIGHT/INTERIOR 条件及 reserve 全部化为一元 fraction-free polynomial sign 问题，给出分母退化、端点碰撞和 algebraic endpoint 的明确边界与 counterexample-guided dispatcher。目标是避免把真实 moving fiber 粗化成固定 outer box，同时保持 T-P5-268 的一元 Sturm/Bernstein exact 路线；不做 provenance/receipt/admission/re-audit，不宣称 source binding、coverage、Float64、Lean/kernel 或 parent closure。