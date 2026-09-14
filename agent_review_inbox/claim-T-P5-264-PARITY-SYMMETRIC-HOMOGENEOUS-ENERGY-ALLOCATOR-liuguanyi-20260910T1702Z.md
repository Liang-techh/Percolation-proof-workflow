---
kind: task_claim
task_id: T-P5-264-PARITY-SYMMETRIC-HOMOGENEOUS-ENERGY-ALLOCATOR
agent: 柳冠一
source_agent: 柳冠一
created_at: 2026-09-10T17:02:00Z
inspected_commit: c2bc716919d62ba984a02eda8e16c4bcced824ca
status: completed
admission_label: pending
result_commit: 32dbdb379152b48355b110682cfc1314c0ff231a
companion_commit: 6a421338fd68f7fa545e6ac752ce59c858c7f037
completed_at: 2026-09-10T17:15:00Z
---

# Claim — T-P5-264 parity-symmetric homogeneous energy allocator

承接 T-P5-263 明确留下的 sum-of-homogeneous-degrees seam。只做数学层：对 `P(u)=sum_j P_j(u)` 的不同齐次次数分量，证明 centered symmetric source ball 上跨奇偶次数的 signed cancellation 不能作为 uniform reserve；给出 even/odd reflection identity、仅依赖逐次数常数时 triangle budget 的 minimax sharpness、保留同奇偶/同总次数 cancellation 的 typed cross-energy contract，以及不含平方根的 rational weighted fallback。目标是把 T-P5-263 的单次 homogeneous certificate 接到真实 nonhomogeneous polynomial remainder，而不把 source binding、coverage、Float64、Lean/kernel、封不觉验证或 admission 当作已完成。避免与 T-P5-262 mixed-metric lane 重叠，不做 provenance/receipt/re-audit。

完成结果见 `review-T-P5-264-PARITY-SYMMETRIC-HOMOGENEOUS-ENERGY-ALLOCATOR-liuguanyi-20260910T1712Z.md`；中文协作交接见对应 companion log。结论保持 `CONDITIONAL_PASS_MATHEMATICAL_CHILD / pending source binding`。
