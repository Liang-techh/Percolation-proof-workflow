---
kind: task_claim
task_id: T-P5-273-NESTED-SEMIALGEBRAIC-FIBER-ELIMINATION
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T19:20:00Z
inspected_commit: 58b13647bef268cb7dbfcc4a1862b82e2f6f1f84
status: claimed
admission_label: pending
---

# Claim — T-P5-273 nested semialgebraic fiber elimination

承接 T-P5-272 明确保留的下一条数学 seam：研究二维但保持 triangular / graph-like 结构的 source fiber，例如 `s ∈ F_q`、`t ∈ [a(q,s), b(q,s)]`，且 Lyapunov slack 对内层变量 `t` 为至多二次时，能否先对每个 `(q,s)` 精确消去 `t`，再把安全性降回一维 `s` 的代数符号问题，而不跳到一般 bivariate CAD 或二维非线性优化。

本轮目标是给出 exact nested-fiber theorem、所有退化分支与 denominator/root-selection 边界，并明确何时内层 quadratic clamp 产生纯有理/代数外层条件、何时需要额外 cell refinement；同时给出 counterexample 说明把 triangular fiber 粗化成 rectangle 会制造 false obstruction。只做数学证明与最小形式化接口，不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、独立验证或 parent closure。