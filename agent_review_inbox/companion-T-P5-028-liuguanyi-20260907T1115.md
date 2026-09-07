---
kind: companion_log
task_id: T-P5-028
source_agent: 柳冠一
agent: 柳冠一
created_at: 2026-09-07T11:15:00-06:00
related_review: review-T-P5-028-liuguanyi-20260907T1112
integration_status: pending
admission_label: pending
---

# T-P5-028 协作摘要

- 当前完成：把 block-(4,5) moving frame 的 actual-minus-nominal 差分精确写成 source 坐标稀疏映射。若 actual/nominal 在同一时刻共享同一个 ramp 参数 `c`，则 `Delta q=(Delta x)`、`Delta v=(Delta y)`、`Delta w=Delta c=0`，所以 `w/c` Jacobian columns 对 centered `K_path` 必须严格零收费，而不是因为 residual 对 `w/c` 敏感就加入保守预算。
- 参数不共享时：若 source/P8 能证明 `|Delta c| <= gamma · |Delta z|`，则对现有 anisotropic component matrix 只需增加 rank-one 非负修正 `K_eff = K0 + kappa(T) tensor gamma`；可直接交给 `T-P5-025/T-P5-026`，无需先坍缩为 Frobenius scalar。
- 明确 obstruction：若允许 `Delta z=0`、`Delta c!=0`，且 residual 沿 fixed-`z` 的 `c` fiber 发生变化，则任何有限四维 centered gain 都不可能成立。此时只能固定 common `c`、证明 `Delta c` 受 `Delta z` 控制、扩大 consumer state，或走 additive/transverse lane。
- 建议 source/P8 lane：在 residual/Jacobian receipt 中显式标记 `common_ramp_parameter` 或 `controlled_parameter_mismatch(gamma)`；前者应输出 `w/c` 零位移行，后者输出 `gamma`，不要把两种比较模式混在同一个未标注的 `ell2`/`K_path` 中。
- 建议形式化 lane：优先实现 `movingFrameSourceDifference_exact`、`movingFrameCommonParameter_cancel`、`movingFrameSegment_preservesRampFiber`、`movingFrameUniformTransport_of_parameterControl`、`movingFrameParameterCorrection_to_K`、`fourStateCenteredGain_implies_parameterFiberConstancy` 六个小代数 lemma；不需要重新证明 `T-P5-026` 的 SPN/copy cone 数学，也不需要引入 ODE API。
- 边界：仍缺具体 source/Float64 `H`、P8 cell chain/coverage、真实 source ordering/其他 distal coordinate transport、参数比较模式的物理 binding、Lean compile 与独立验证。P5/P8/M4 状态不变。

待封不觉独立验证 / 待梁智炜最终整合。
