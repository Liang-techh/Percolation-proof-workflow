# Body-6：最小 A/X/Y source-binding 契约

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明内核验证、coverage 或 registry admission。

本次新增 `NEW_BODY6_SLICE_SOURCEBLOCKBIND20260907.lean`（102 行）及本定向 review。
直接导入 `NEW_BODY6_SLICE_SCHURREMAINDER20260907` 和 `NEW_BODY6_SLICE_MASSMIX_Source20260907`。
目标是将已有外部块余项接口接到明确的实际 source 条目，并保留尚未提供的候选表绑定义务。

## 核对到的现有接口

- `sourceTail q` 是实际 `sourceBodyMass q 5` 在有序 `{3,4}` 两列上的 `2×2` 子块。
- `CenterOffsetTarget` 要求所有配置和坐标上的实际 body-6 质心等于终端原点加 `offset` 倍终端轴，`offset = 7/200`；本叶不构造这个几何见证。
- tail 与 mixed 命名空间分别有 `SourceWeightsTarget`，定义均为实际 `routeBMass 5 = m` 与 `routeBInertiaScalar 5 = kappa`。
- mixed 与 tail 的 `tailJoint` 均将内部 `Fin 2` 的 `0,1` 映射为真实关节 `3,4`；源侧转换保持这个次序。
- weighted mixed 已有条件式 `source_weighted_mixed_attempt`；实际质量条目的对称性由 `source_mass_symmetric_attempt` 提供。
- 已检查的 `SELF3_Source` 提供前三列 velocity/axis Gram 接口；它自身未提供任意候选 `A` 的质量加权条目绑定。本叶不重复推导该加权表。

## Typed 绑定结构

body 固定为 `(5 : Fin 6)`，即通常编号的 body-6。
前三列经 `firstJoint : Fin 3 → Fin 6` 映射到 `{0,1,2}`，tail 经已有映射到有序 `{3,4}`。

| 字段 | 候选类型 | 必须绑定的实际条目 |
| --- | --- | --- |
| `bindA` | `Fin 3 → Fin 3 → ℝ` | `sourceBodyMass q 5 (firstJoint i) (firstJoint j)` |
| `bindX` | `Fin 3 → Fin 2 → ℝ` | `sourceBodyMass q 5 (firstJoint i) (tailJoint a)` |
| `bindY` | `Fin 2 → Fin 3 → ℝ` | `sourceBodyMass q 5 (tailJoint a) (firstJoint j)` |

这些字段组成 `SourceBlockBinding q A X Y : Prop`；不允许只绑定 X 而把 Y 的方向留给默认约定。
`q : Fin 6 → ℝ` 是任意配置参数，绑定针对传入配置；若需所有配置上的候选绑定，应提供 `∀ q, SourceBlockBinding q ...`。

`sourceA/sourceX/sourceY` 是实际 source 条目的符号引用，不是新数值表。
`raw_source_binding_attempt` 对这些引用给出反身绑定；它没有验证独立输入的候选系数。

## 已有 mixed 表的条件式接入

`mixedX q m kappa` 取已有 `explicitMixed q offset m kappa`，
`mixedY q m kappa` 取其索引转置。

`mixed_x_binding_attempt` 在 `CenterOffsetTarget` 和 tail 权重绑定前提下，转换定义相同的 mixed 权重目标，并消费已有 weighted mixed source 接口。
`source_y_transpose_attempt` 使用实际 source 质量条目的对称性，证明反向条目与正向转置相等。

`mixed_binding_from_A_attempt` 因而可填写 X/Y 字段，但明确要求调用者提供
`hA : FirstBlockBindingObligation q A`。
它没有推断任意 `A` 已绑定，也没有从 CSV、数值样本或仅同维度的数组构造证明。

## 定向 obstruction：尚缺什么

对一个独立候选 `A`，尚需提供全部 `Aij = sourceA q i j` 的证明项；该义务被命名为
`FirstBlockBindingObligation`，并保留为 mixed 构造器的必需参数。
本任务没有收到独立候选 A 的值和绑定见证，因此没有生成其无条件完整绑定。
这是本叶当前未提供的见证，不是宣称数学上不可能由 self3 Gram 继续推导。

若选择 `A = sourceA q`，该字段可用反身性满足，但 A 仍是实际 source 表达，不能把这一选择报告为显式候选表已验证。
对任意另行输入的 X/Y，同样必须填写对应字段；已有 mixed 构造器只覆盖所定义的 `mixedX/mixedY`。

缺少见证不等于已经证明不匹配。`A_mismatch_rejects_binding_attempt` 仅在提供
`∃ i j, Aij ≠ sourceA q i j` 的实际反证项时，才推出该候选不能满足 `SourceBlockBinding`。
本叶未断言存在这样的反证项，也未伪造任何数值。

## 消费契约的余项定理

`bound_remainder_coefficient_attempt` 消费全部三个绑定字段，把已有余项表达改写为

\[
R_{ij}=M_{f_i f_j}
-\frac{M_{f_i t_0}M_{t_0 f_j}}{\kappa+m\,offset^2\sin^2(q\,4)}
-\frac{M_{f_i t_1}M_{t_1 f_j}}{\kappa+m\,offset^2},
\]

其中 `Mab = sourceBodyMass q 5 a b`、`fi = firstJoint i`、`t0=3`、`t1=4`。
这是实际条目绑定后的代数公式；单独的展开定理不表示分母已可逆。

`bound_source_remainder_attempt` 进一步在中心偏移、权重绑定、`kappa > 0`、`m ≥ 0`、
`offset² ≥ 0` 和 `SourceBlockBinding` 全部前提下，返回：

1. 既有 `SchurRemainderContract`，包含实际 tail 的左右逆、分母正性及求解接口；
2. 上述对所有 `i,j : Fin 3` 的实际 source 条目余项公式。

没有据此声明完整矩阵 PSD、Schur PSD 等价性、全系统消元证明或特征值结论。

## 本次检查与未闭合边界

只做定向接口阅读、静态 import/占位检查，以及小型索引枚举：确认 A/X/Y 的 `3×3`、`3×2`、`2×3` 形状、front/tail 不相交和 X/Y 条目方向互为转置。
没有重新计算 Gram 或 Fourier 数值，没有运行旧检查脚本或大回归。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`；这不构成 Lean 编译或依赖闭包验证。

sidecar 实际字节 SHA-256：
`417c632bf25ab97b14af539e344a22720181d01da1b0e905fb70143e93f119a3`。

本次只新增上述两文件。候选 A 绑定见证、无条件 CenterOffset/权重见证、完整 Schur PSD、Fourier、coverage、Lean 验证及 registry admission 均保持未闭合；未修改共享脚本或准入状态。
