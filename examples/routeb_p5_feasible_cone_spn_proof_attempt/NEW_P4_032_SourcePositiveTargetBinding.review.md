# P4：positive target 与 true-DH/source/normalization 同域绑定

日期：2026-09-07。状态：**OPEN_UNCOMPILED**。
新增 `NEW_P4_032_SourcePositiveTargetBinding.lean` 与本 review。
只做定向代码/文档/记录检查和纸面推导；未运行 Lean/Lake、Julia 或大回归。
未修改旧记录、共享脚本或 registry。

## 当前所检记录能否给出正 target

本轮定向检索了 examples 中 PositiveTargetBudget/FrontFloors/ResidualCaps/NominalRealization
的 Lean 用法，以及 JSON/YAML/TOML 中 positive_target/alphaFloor/frontFloor/gainCap/betaCap/qCap。
找到的是当前 proof-attempt 定义和参数化消费者，未找到把这一新链实例化为具体 Route-B
正 target 的完整证据包。此结论仅限这次检索范围，不是全仓所有其他理论的不存在性证明。

具体核对的记录及其限制：

| 记录 | 本轮读取到的事实 | 对正 target 的意义 |
| --- | --- | --- |
| `NEW_P4_032_PositiveTargetFeasibility.lean` | 正 target 要求 target≤F-L 且 target>0 | 符号与 cap 存在不等于严格差额为正 |
| `NEW_P4_032_SplitAllocationObstruction.lean` | finite_front_floors 可取 alphaFloor=frontFloor=0 | 有限界存在不保证正 credit 或正 target |
| `NEW_BODY6_SLICE_SCHURMARGIN20260907.lean` | RemainderMargin 允许 mu=0，实际 margin 是外部前提 | 未提供统一正 mu 或 frontEnergy 正下界 |
| `docs/routeb-p4-kc-force-contract.md` | force/acceleration 缩放与 deployed tau 等价分别是义务；kc residual 不能删除 | 不能漏算 residual 来制造正预算差 |
| `docs/routeb-c2-d-normalization-audit.md` | I_B 与 M0_BB 不同，force residual 与 acceleration-side D 需要桥 | 不能把不同比例或单位的 qCap 直接代入本链 |
| `agent_review_inbox/review-T-P4-fresh-general-state-force-receipt-immutable-codex-20260907.md` | 该历史 receipt 自述 PENDING_JULIA_EXECUTION，未提供 fresh runtime 输出 | 它不构成此新正 target 的证明；本轮未重新探测 Julia/运行状态 |

文档记录的源语义没有在本轮重新对外部 deployed 文件执行验证；只用来定位未闭合义务，
不将旧 receipt 的运行环境状态声称为当前机器状态。

## 最小 typed source 接入

`SourceView Y` 显式保存模型域、energy、typed generalized-force residual、BODY6 remainder/front/mu、
alpha/beta/gain、offset/nominal 和 scalarMargin。
它只是待识别的模型函数包，名字不等于 true-DH 正确性证明；调用者还须将这些函数实例化为
正确的源方程并提供 source identity/provenance 与有效性证据。

`SameDomainBinding` 使用一个 embed:Y→X，在同一个源状态上绑定所有函数，并要求
源域每点映入 f.domain。特别地，q 必须等于同一 forceResidual 的 Euclidean norm 平方，
没有将 acceleration residual、三维 BODY6 front、二维 port 或不同 inertia normalization 混同。
若需要别的 residual normalization，应先证明相应 adapter，不能将此等式凭名称认定成立。

`source_residual_cap` 在这些绑定下传递实际 q≤qCap。
`source_prescribed_positive_margin` 还显式接收 CompositionContract、NominalRealization、
FrontFloors、ResidualCaps 与预设 target 的 PositiveTargetBudget，复用旧 split 消费器，
仅输出源视图域内 `0<target ∧ target≤scalarMargin`。
normalization comparison 与 nominal 的正确下界没有被 source 字段等式替代。

## 最小缺失 obligations

要为预设 target=t>0 关闭这条链，至少需要针对同一实例提供：

1. **精确预算差**：F=offsetFloor+alphaFloor*frontFloor、L=gainCap*(betaCap*qCap)，
   证明 t+L≤F；若只是寻找某个正 target，也必须证明 L<F。
2. **有效统一界**：alpha/front 的正确下界，beta/gain 的非负上界，以及实际同单位 residual
   的 q≤qCap，而不是未绑定的 cap 数值或采样最大值。
3. **nominal 与 comparison**：expression≤nominal 以及原 normalized BODY6-to-scalar 比较；
   不能从旧 nominal≤expression 反推。现有 specialization 合起来仍要求 nominal=expression。
4. **source 与域**：实际 true-DH/source 函数和同状态缩放等式、源域覆盖及参数统一有效性。

这些是此接口的充分证据要求，并非所有其他分析方法的必要条件。

## 新的数学 obstruction

`credit_not_exceeding_loss_blocks_positive` 直接消费旧 exact feasibility：若 F≤L，
则这组固定 records 不存在正 PositiveTargetBudget。
`positive_signs_not_positive_budget` 给精确 F=L=1 的例子：即便 front/gain/beta/qCap
都严格正，任意 t>0 仍不可分配。

`zero_floor_blocks_positive`：alphaFloor 或 frontFloor 为零且 offsetFloor≤0 时，
非负 residual loss 已足以排除正 target。
`zero_front_test_forces_zero_floor`：若域内含 front 向量 v=0，则统一 frontFloor 必为零，
即使 mu>0 也无济于事。这不反驳矩阵正定性；齐次二次型在零向量上本来为零。
若想证明正的标量 floor，需要明确的归一化/非零测试域、正 offset，或不同 target 形式，
不能未经授权把零向量从目标域删掉。

因此当前记录提供的非负符号、条件式 qCap 与抽象 source 接口不足以单独推出正 target。
本叶没有虚构具体反例 source，也没有确认真实系统 F≤L；记录缺失与数学不可能性保持区分。

保持 OPEN_UNCOMPILED；新文件与导入链未做 elaboration/kernel/public axiom 检查。
没有实际 true-DH/coverage/admission/registry 或 PSD 升级。
