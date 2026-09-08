# Body-4 minimal Z/O source Jacobian bridge

状态：CONDITIONAL_SOURCE_JACOBIAN_SKELETON_UNCOMPILED；admission=pending；source_binding_proven=false。
本轮没有运行、安装或探测 Lean/Lake，没有编译、kernel 或 VERIFIED 声明。

## 本轮增量

配套文件：`NEW_SOURCE_JACOBIAN_20260908_MINIMAL_ZO_BRIDGE.lean`。
仅新增该 Lean 文件和本 REVIEW；没有修改旧 proof attempt、共享 adapter、state、registry 或其他 agent 文件。

已阅读原 `RouteBO1Body4SourceGramTargets.lean`、`RouteBO1PerBodyExactSource.lean`、
`RouteBO1Body4SourceGramProofAttempt.lean`，现有 BODY4_BRIDGE 的几何部分、BODY4_PORTS、
FRAME_HANDOFF，以及实际 `BodySemanticCore.lean` / `SourceContractIndexAdapter.lean`。
旧全量尝试同时展开几何、Jacobian、Gram 和 expected-entry；本轮只提取 Jacobian 所需的最小接口。

FRAME_HANDOFF 目前消费完整 `Body4PrefixColumnsTarget`：4 slots × 3 spatial rows × X/Y/Z/O，
共 48 个标量等式。新增局部 `PrefixZO` 只要求原 accessor 的 Z/O，共 24 个标量等式。
它不是原 target 的替代定义，也没有导出完整 prefix target；`zo_of_full_prefix` 只有从完整 target
到 Z/O 的单向投影。所有等式仍对同一个实际 `routeBFrameSlot q`、全部实数 q 量化。

条件链是：`PrefixZO + Body4Slot4TranslationTarget → SourceGeometry → Body4JvTarget ∧ Body4JwTarget`。
未提供这两个几何前提的无条件 inhabitant。旧 proof-script 文本不自动闭合它们。

## 逐分支依赖

| 出口 | 实际依赖与索引 |
|---|---|
| source axes | Z 列，active joint j 的 parent slot 为 j；Fin 4 嵌入 Joint=Fin 6 |
| source COM | human body 4 = Body 3；midpoint(origin slot3, origin slot4) |
| source displacements | source COM 减 parent origin slot j，而不是减 body 的另一端点 |
| Jv columns 0–2 | 实际轴、实际 COM 位移、定向 cross transport，接回原 vcol |
| Jv column 3 | joint 3 仍 active；slot4 translation 给位移 `(19/200)*Z3`，平行叉积为零 |
| Jw columns 0–3 | 仅需 Z 列；joint3 输出 Z3，不是零，也不是 slot4 的轴 |
| columns 4、5 | `3 < j.val` 的 inactive guard，无几何前提；额外给出精确索引 iff |

`jw_of_axis_columns` 单独暴露角 Jacobian 的更小前提；不要求 O、COM 或 slot4 translation。
`joint3_linear_of_translation_only` 复用已有 FRAME_HANDOFF 的较短脚本：只消费 translation，
不需要 Z/O 的显式三角坐标。这个脚本及整个 import 闭包同样未经本轮编译。

## lift / isometry 与 source 边界

`lift q u = vec q (u 0) (u 1) (u 2)` 是绕世界 z 轴的定向旋转。
复用 PORTS 中分开的 `lift_dot_isometry` 与 `lift_cross` 候选：前者是欧氏 dot 保持，
不是默认函数空间 Pi/sup norm 的 metric `Isometry`；后者还要求正确的定向。
仅有 dot 保持不能代替 cross transport，也不能识别 source 列；`vcol/wcol` 已经 lift 到世界坐标。

本文件没有把局部 Gram 恒等式升级为 source theorem。
`RouteBO1PerBodyExactSource.sourceBodyMass` 实际定义为具体 `sourceContract` 的 `contractMass`；
后续若进入该出口，仍需原 Jacobian 目标闭合、body mass `2/5`、已除三的 inertia 对角 `1/15`、
完整 Gram 表及相应归约。这里没有导出 `Body4SourceGramTarget`、expected-entry、h_body_4、
Fourier/trace 或跨语言 Julia runtime 结论，也不将 mass regularizer 搬入 body Jacobian。

## 静态检查与待验证项

本轮仅静态核对原目标类型、adapter 索引、guard、几何公式和新增文件文本。
没有使用数值采样、局部 Gram 或已有 olean 文件作为证明证据。
新增文件不含 `sorry`、`admit` 或新 `axiom` 声明；这不是 elaboration 成功的证据。

后续需在获授权的一致 Lean/Mathlib 环境中验证完整 import 闭包，再检查本文件的 elaboration
与列出的 `#print axioms` 输出。重点检查 `PrefixZO` 的 accessor/vector definitional equality、
Fin proof-irrelevance 转换、`rw` 对 `prefixSlot 3` 的匹配及现有 PORTS 的有限列分支。
还必须实际证明 Z/O 和 translation 两个上游几何输入；编译一个条件蕴含本身不等于无条件
source binding。只有本轮新增文件的静态检查，不存在编译 receipt 或登记升级。
