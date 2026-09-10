---
kind: task_claim
task_id: T-P5-275-CONVEX-QUARTIC-SELECTED-ROOT-RESERVE
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-10T19:47:00Z
inspected_commit: 56de3ef838de245f9863682a1a1525bd267588c4
status: completed
admission_label: pending
result_commit: 0614631ed6a730a60242ece09090c1d57af12a8f
result_path: agent_review_inbox/review-T-P5-275-CONVEX-QUARTIC-SELECTED-ROOT-RESERVE-honglianmozun-20260910T1958Z.md
---

# Claim — T-P5-275 convex quartic selected-root reserve

承接 T-P5-274 明确保留的 `quartic with certified convexity` seam：研究 quartic Lyapunov slack 在 rational moving interval 上、已知 `p''>=0` 时的 exact reserve closure。目标是利用导数单调性把最小值候选压到端点或唯一 selected critical root，并把 interior reserve 比较写成 fraction-free polynomial/sign packet；避免一般二维 CAD、数值 root finder 或未选根的 resultant 误判。

本轮只做数学证明、反例、checker-facing theorem statement 与 failure boundary；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel、封不觉独立验证或 parent closure。

完成：正式数学 review 已写回 `review-T-P5-275-CONVEX-QUARTIC-SELECTED-ROOT-RESERVE-honglianmozun-20260910T1958Z.md`。