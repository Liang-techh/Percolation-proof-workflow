---
kind: task_claim
task_id: T-P5-265-RATIONAL-RADIAL-POLYNOMIAL-INTERVAL-CERTIFICATE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T17:22:00Z
inspected_commit: 66ce97393a21d0db9a52f75dc1f271af751fd70c
status: claimed
admission_label: pending
---

# Claim — T-P5-265 rational radial-polynomial interval certificate

承接 T-P5-264 明确留下的 full-radial-interval seam。只做数学层：当 same-parity / same-total-degree cancellation 被保留后，把 `Q(u)` 归约成 `q∈[0,R]` 的有理 signed radial polynomial，建立不依赖浮点 root finder 的 exact interval upper-bound certificate；优先给出 fraction-free Bernstein/interval transport、严格负 margin 的有限 subdivision closure、以及 certificate 失败不等于数学 FAIL 的边界。目标是让 T-P5-264 的 `energy_layer(total_degree)` 真正可消费，而不做 provenance/receipt/admission/re-audit，不声称实际 P5 source binding、coverage、Float64 或 Lean/kernel 已闭合。
