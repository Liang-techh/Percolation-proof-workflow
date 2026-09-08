---
kind: task_claim
task_id: T-P5-045
agent: 柳冠一
source_agent: 柳冠一
claimed_at: 2026-09-07T20:59:00-06:00
inspected_commit: 12f8650e72e5555eb2aafe51653af391d623928d
scope: robust_interval_transport_from_signed_2x2_u_to_l_block_to_T-P5-044_correlated_gate
boundary: mathematics_and_source_to_math_interface_only; no Lean compile, provenance, admission, receipt, registry, Float64 execution, or coverage audit
related_tasks:
  - T-P5-041
  - T-P5-042
  - T-P5-043
  - T-P5-044
status: claimed
---

# 柳冠一 claim — T-P5-045

I claim one narrow mathematical/interface obligation left explicitly open by `T-P5-044`: derive an exact-rational, source-facing robust interval theorem for a state-dependent signed `2x2` `u -> l` block `K(z)` and transverse/additive remainder `b(z)`, so that interval Jacobian data can certify the positive-definite reserve and correlated adjugate bias gate without destroying skew/cross cancellation.

I will not re-audit `T-P5-040/042/043/044`, perform Lean/kernel/provenance work, or claim source/coverage/admission. The result will stop at a minimal theorem/adapter contract plus exact obstruction/fallback conditions.