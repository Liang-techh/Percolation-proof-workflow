---
kind: task_claim
task_id: T-P5-271-MULTICOMPONENT-SEMIALGEBRAIC-FIBER-DECOMPOSITION
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T18:50:00Z
inspected_commit: dca236762bf7fa0687e0d6fbcaf030d895561a92
status: completed
admission_label: pending
result_commit: 28be4ab630470caae390cfef4b534a0c96091076
companion_commit: e1b523169a11fe02e692b4560f86f7af379f0ee3
completed_at: 2026-09-10T18:56:00Z
---

# Claim — T-P5-271 multi-component semialgebraic fiber decomposition

承接 T-P5-270 明确保留的下一条数学 seam：当 source fiber 不是单一 endpoint graph，而是由 `P(q,s)>=0` 或 `P(q,s)<=0` 给出的多分量一维 semialgebraic fiber 时，建立 branch-safe 的 exact 分解与 Lyapunov quadratic clamp。重点处理：固定 discriminant-free q-cell 上的实根排序与符号区间、component-wise LEFT/RIGHT/INTERIOR clamp、discriminant/degree-drop 点上的 merge/split point-cell 语义，以及 compact q 区间上的有限 exact dispatcher。

目标：证明对一元 fiber polynomial，真正的多分量几何仍可在 q 轴上有限分层为若干连续代数 root branches 与 point cells，因此 signed quadratic energy debit 无需引入二维黑箱优化；同时给出不能把多个 fiber components 用 convex hull 代替的精确反例。只做数学/Lyapunov closure，不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、独立验证或 parent closure。

完成结果见 `review-T-P5-271-MULTICOMPONENT-SEMIALGEBRAIC-FIBER-DECOMPOSITION-honglianmozun-20260910T1850Z.md`，中文交接见 `companion-T-P5-271-MULTICOMPONENT-SEMIALGEBRAIC-FIBER-DECOMPOSITION-honglianmozun-20260910T1854Z.md`。数学结果建立 parity-aware squarefree factor atlas、interval/singleton component decomposition、component-wise quadratic Lyapunov clamp、singular q point-cell dispatcher，并给出 convex-hull false FAIL、discriminant-point false PASS 与 ordinary squarefree source corruption 三类 exact counterexample。结论保持 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。