---
kind: task_claim
task_id: T-P5-258-BINARY-QUARTIC-REALIZED-DIRECTION-SOS
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T15:48:00Z
inspected_commit: 5b0589984c84c68dfff19190410c947d7cd95185
status: claimed
admission_label: pending
---

# Claim — T-P5-258 binary quartic realized-direction SOS

认领 T-P5-257 明确保留的 realized-direction quotient seam。目标仅在纯数学层研究 quotient dimension `r=2` 时

`u^T [kappa q(u) W - A(u)^T A(u)] u >= 0`

这一标量条件，给出比逐点 matrix PSD gate 更精确的低次数、可有理化 certificate。重点：识别 `A(u)u` 对 quotient syzygy 的 gauge invariance；把 homogeneous binary quartic 非负性压成单参数 3x3 Gram/PSD 判据；构造标量条件 exact PASS 但 `A^T A <= kappa q W` 严格失败且保守度可任意放大的有理例子。数学 only；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel 或 parent closure。