---
kind: review_result
task_id: T-P4-036
source_agent: 01a07bb4-d8f2-7ba0-8258-8754bf2ea0f8
created_at: 2026-09-07
integration_status: pending
---

独立 source-binding 审阅确认 deployed `dhport_lib.jl` 的角度形成是
`th=q[ii]+DH[ii,1]`、`al=DH[ii,4]`，随后进入 `cos/sin` 和 DH 链。六条 theta
相位为 `0,-1,+1,0,0,0`，alpha 相位为 `-1,0,+1,-1,+1,0`。

每个 link 的 theta/alpha 均应拆成四类义务：

1. `AF-i-theta` / `AF-i-alpha`：Float64 angle formation inclusion；
2. `RR-i-theta` / `RR-i-alpha`：实际参数到 exact-real reduction 的 inclusion；
3. `LC-i-theta` / `LC-i-alpha`：实际 libm `sin/cos` enclosure；
4. `DAG-i-theta` / `DAG-i-alpha`：从 trig 输出到 `A_i`、后续 DH/FK、COM、J、M、P 的有限传播。

建议的接口名称：`RouteB.P3.DHThetaPhaseContract`、
`RouteB.P3.DHAlphaPhaseContract`、`RouteB.P3.ExactRealTrigRangeReductionLeaf`、
`RouteB.P3.Float64AngleFormationInclusion`、
`RouteB.P3.Float64LibmSinCosEnclosure`、`RouteB.P3.DHLinkFiniteDAGEnclosure`、
`RouteB.P3.DHChainFloat64EvaluatorEnclosure`。其中 Float64/libm/DAG 接口只能是
open interface draft，不能注册或关闭 O2。

剩余硬义务包括 12 个 angle-formation、12 个 range-reduction、12 个 libm
enclosure、6 个 link DAG，以及 central-FD、regularizer、backslash solve、box
coverage、Lean compile/zero-sorry/axiom/comparator receipts。
