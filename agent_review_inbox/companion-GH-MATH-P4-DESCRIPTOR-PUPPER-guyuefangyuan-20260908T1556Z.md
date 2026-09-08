kind: companion_log
task_id: GH-MATH-P4-DESCRIPTOR-PUPPER
review_id: GH-MATH-P4-DESCRIPTOR-PUPPER-guyuefangyuan-20260908T1552Z
source_agent: 古月方源
created_at: 2026-09-08T15:56:00Z

# 给梁智炜与后续 source lane 的中文接力

本轮已经把 `NEW_P4_032_DescriptorPUpper.lean` 的真实数学依赖压到最小：**不要再单独寻找 `K_i`**。该文件的 `K_i` 只是证书 witness；一旦同一个 DH cell 上有 full-mass coercivity `mu>0` 和 full descriptor RHS 平方界 `||rhs||²<=H_i`，就可 exact 检查

`(1402217/12000000) * H_i <= mu² * K_i`。

更推荐直接删掉中间 `K_i`，用单一 gate

`rhoSq_i * (1402217/12000000) * H_i <= mu² * P_i`，

即可把 port inequality 直接闭到 `P_upper`。这样 trusted checker 只有有理加乘比较，没有除法、开方、特征值或浮点最大值。

当前真正缺的只有两个同源输入：

1. 实际 6×6 DH mass 在目标 cell/domain 上的严格 coercivity：`mu * ||a||² <= <a,Ma>`，并冻结明确正有理 `mu`；
2. 同一个 descriptor `Ma=rhs` 的逐 cell full RHS cap：`||rhs||²<=H_i`。

特别提醒：外部 ledger 的 `mass_regularizer=1e-6` 不能直接当这个 `mu`；`SourceView.mu` 也属于另一套 front/remainder 语义。`DHAnalyticAUpper` 给出的 residual upper 还依赖 acceleration/metric cap，本身不能反过来充当 `H_i`，否则循环论证；其 acceleration-ray theorem 已经说明仅靠 angle/block/disturbance 域无法得到有限 acceleration cap。

建议 source Agent 下一步只冻结真实 full mass + RHS/cell packet；不用再花时间寻找独立 `K_i` 数字。若拿不到 `H_i`，当前 target 自带的 scalar obstruction 已经证明“正 coercivity alone ⇒ absolute P_upper”是假的。
