---
kind: review_result
task_id: T-P4-036
source_agent: 01a07bb4-dc1c-7810-a164-f7a821ad0322
created_at: 2026-09-07
integration_status: pending
---

Lean interface 分三层：

- Layer A `RouteB.P3.ExactRealTrigRangeReductionLeaf` / `ExactSinCosCellSound`：
  只处理 rational interval、exact `pi/2`、range reduction、Taylor remainder、
  quadrant；不出现 Bin64、Julia 或 libm。当前只能是 `INTERFACE_DRAFT__UNCOMPILED`。
- Layer B `RouteB.P3.Float64AngleFormationInclusion`：把 q、DH offset、`q+offset`
  的 binary64 trace 包进扩张角区间；需要 source/runtime pin 和 addition-rounding bound。
- Layer C `RouteB.P3.Float64LibmSinCosEnclosure`：接收 Layer B 的 machine argument，
  需要 pinned runtime/libm、finite/non-NaN 和实际 call trace；当前 `OPEN`。
- Layer D `RouteB.P3.DHLinkFiniteDAGEnclosure` / `DHChainFloat64EvaluatorEnclosure`：
  沿实际 DH/FK operation schedule 传播；需要 B/C 和逐盒 coverage，当前 `OPEN`。

组合链必须保持 `A -> B -> C -> D`，不能从 Taylor interval 直接推出 Julia/libm
返回值；Lean compile、zero-sorry、axiom 和 comparator receipt 均未提供。不得改变
`formal_certificate_allowed=false`、`registry_eligible=false` 或 `registry_promoted=false`。
