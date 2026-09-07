---
kind: companion_log
task_id: T-P5-019
source_agent: 柳冠一
created_at: 2026-09-07T07:34:00-06:00
related_review: review-T-P5-019-liuguanyi-20260907T0730
status: pending
---

# T-P5-019 协作摘要

本轮把 `T-P5-009` 的仿射 FD 分量包络与 `T-P5-018` 的 block-(4,5) incremental tube 接起来了。最重要的接口变化是：`T-P5-018` 只需要同域的两通道 Euclidean residual budget `r4^2+r5^2<=L2`，因此正 offset 不再需要硬转成 `rho|v|`；只要 source/domain 能给 `0<=cap<=Ccap`，就可以直接把 axis 4/5 的两个 affine envelope 平方后相加。

当前 axis-(4,5) 对应 `FDForceBudget` 的 `Fin 6` 内部 indices `(3,4)`。FD-only 的精确两通道多项式已经算出：

```text
P45(c)=A45*c^2+B45*c+C45,
A45=3527749689493/7330491270144000000000000000000,
B45=397329089/171904000000000000000000000000,
C45=47155689/12800000000000000000000000000000.
```

若还有 runtime/solve/controller 或 nominal residual，只需先做 component box 聚合，再用

```text
L2 <= (E4+Z4+N4)^2 + (E5+Z5+N5)^2.
```

这个 bound 在只有独立分量 box 信息时是 sharp 的，不需要额外 factor 2。

另一个可立即复用的桥是现有 weighted power budget 到 `T-P5-018` Euclidean tube：对 block damping `d4=4/5,d5=13/20`，有精确恒等式

```text
(8/5) W45 - (r4^2+r5^2) = (3/13) r5^2 >= 0,
```

所以 `L2<=8/5 W45<=8/5 W6`，其中 `8/5` 在只知道 weighted norm 时是 sharp 常数。这样现有 `FDForceBudget.polynomialBudget` 可作为快速但较保守的 fallback；真正 source/checker 应优先直接抽 axis 4/5，因为 full-six fallback 对常数 offset 的收费约大 1552 倍。

需要特别提醒接口层：`FDForceBudget.efd` 在现有 Lean 抽象中是直接加到 `DHPowerBinding.forceError` 上的 generalized-force error，因此进入本桥时不能再乘一次 `I_B`。如果 concrete interval generator 输出的仍是 raw PMI `f_B` 坐标，那么应在 source binding 上游只做一次 `I_B=diag(1/5,1/10)`；重复 normalization 会把平方 residual budget 错缩小 25/100 倍。

建议形式化 Agent 只落五个小 theorem：`component_box_to_block_l2`、`block45_weighted_to_euclidean`、`diagonal_block_l2_identity`、`block45_fd_polynomial_exact`、`block45_fd_of_cap_le`，不要重复 `T-P5-018` 的 hypocoercive sidecar。

当前真正剩余的 source 义务已经压成：`BLOCK45_AXIS_INDEX_BINDING`、`BLOCK45_RESIDUAL_FORCEERROR_BINDING`、`BLOCK45_FORCE_COORDINATE_BINDING`、`P8_SAME_DOMAIN_CAP_BOUND`、`RUNTIME_COMPONENT_BOXES`。待封不觉独立验证、待梁智炜收割与最终整合；不改变 P5/P8/M4 当前最终状态。
