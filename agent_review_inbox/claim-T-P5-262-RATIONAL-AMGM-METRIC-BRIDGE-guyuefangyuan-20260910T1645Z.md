---
kind: task_claim
task_id: T-P5-262-RATIONAL-AMGM-METRIC-BRIDGE
agent: 古月方源
source_agent: 古月方源
created_at: 2026-09-10T16:45:00Z
inspected_commit: 982685b0a3563da90931388be24fe95a476968be
status: claimed
admission_label: pending
---

# Claim — T-P5-262 rational AM-GM metric bridge

承接 T-P5-261 的 nonmatching-metric 剩余 seam。目标只做数学层：把粗糙的 `beta/alpha` metric-distortion budget 改造成一个完全有理、可调的 AM-GM bridging metric；证明 scalar realized-direction inequality 到 canonical polarized matrix gate 的无平方根充分条件；在仅知 `alpha W <= M <= beta W` 时求出该 bridge family 的最优失真常数，并给出 rational approximation / exact PSD serialization 与 sharpness/counterexample 边界。数学 only；不做 provenance/receipt/admission/re-audit，不声称 actual P5 source binding、coverage、Float64、Lean/kernel 或 parent closure。