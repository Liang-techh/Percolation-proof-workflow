---
kind: task_claim
task_id: T-P5-273-NESTED-SEMIALGEBRAIC-FIBER-ELIMINATION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T19:20:00Z
inspected_commit: 58b13647bef268cb7dbfcc4a1862b82e2f6f1f84
status: completed
admission_label: pending
review_commit: 2452690d4c89057795bd9c3b27b6974cc304ccac
companion_commit: 30a89a217b32c02cf88556fdf4e9c66b7a5f16fa
---

# Claim — T-P5-273 nested semialgebraic fiber elimination

承接 T-P5-272 明确保留的下一条数学 seam：研究二维但保持 triangular / graph-like 结构的 source fiber，例如 `s ∈ F_q`、`t ∈ [a(q,s), b(q,s)]`，且 Lyapunov slack 对内层变量 `t` 为至多二次时，能否先对每个 `(q,s)` 精确消去 `t`，再把安全性降回一维 `s` 的代数符号问题，而不跳到一般 bivariate CAD 或二维非线性优化。

本轮已经完成数学 child 并写回正式 review 与中文 companion。结果证明：对有理移动内层区间和关于 `t` 的二次 slack，`forall t` 可以精确消去为 `(q,s)` 上有限 Boolean polynomial-sign 公式；`H<=0` 的 concave/affine 分支由两个端点和新的 fraction-free chord 恒等式闭合，`H>0` 由 LEFT/RIGHT/INTERIOR clamp 闭合；零宽度下 strict/weak 端点语义也已单独处理。所得外层 violation 公式可直接交给 T-P5-272 common-root arrangement。actual P5 source binding、coverage、Float64、Lean/kernel、独立验证及 admission/registry 仍保持开放。