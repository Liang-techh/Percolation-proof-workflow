---
kind: task_claim
task_id: T-P5-280-CUBIC-FOUR-FUNCTIONAL-DIRECTIONAL-UNCERTAINTY-ADAPTER
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T21:00:00Z
completed_at: 2026-09-10T21:14:00Z
inspected_commit: f0cf42ddad5fa5b5a24c2e8ebb66b5c66e2fe4d8
status: completed
admission_label: pending
review_commit: db44c62644ef571a900d89abc93342c3fb3e2d06
review_path: agent_review_inbox/review-T-P5-280-CUBIC-FOUR-FUNCTIONAL-DIRECTIONAL-UNCERTAINTY-ADAPTER-liuguanyi-20260910T2102Z.md
companion_commit: e54ad544c68ac17b3c44b81020a258f12d51748f
companion_path: agent_review_inbox/companion-T-P5-280-liuguanyi-20260910T2113Z.md
---

# Claim — T-P5-280 cubic four-functional directional uncertainty adapter

承接 T-P5-279 明确保留的 actual-source one-sided coefficient/FD perturbation seam，但本轮不做 provenance/receipt/admission/re-audit。本轮只证明 source uncertainty 到 cubic clamp 数学消费者之间的最小桥：把任意三次扰动在固定 fiber `[L,R]` 上改写为两个端点值与两个 endpoint curvature/remainder functional，并证明这四个 directional support bound 足以产生 exact shape-preserving lower support；进一步给出保持 quadratic consumer degree 的最优标量 barrier、四 functional 坐标的可逆性、仿射 fiber 坐标协变性，以及 fail-closed 边界。

依赖：T-P5-279（one-sided cubic lower support），并与 T-P5-247（affine chart covariance）、T-P5-270/T-P5-276（selected algebraic endpoints）接口兼容。actual P5 source binding、same-key provenance、coverage、Float64/interval、Lean/kernel、封不觉独立验证与 admission/parent closure 保持 OPEN。

结果：数学 review 与中文 companion 已写回；状态保持 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。