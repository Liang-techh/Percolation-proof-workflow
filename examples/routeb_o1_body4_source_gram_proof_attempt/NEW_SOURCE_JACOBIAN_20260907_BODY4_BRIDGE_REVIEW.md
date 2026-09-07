# Route-B O1 body-4 source Jacobian bridge

日期：2026-09-07。状态：`SOURCE_JACOBIAN_PROOF_SKELETON_UNCOMPILED`。

配对文件：`NEW_SOURCE_JACOBIAN_20260907_BODY4_BRIDGE.lean`。
本轮仅新增这两个同 stem 文件。没有修改旧 attempt/review、targets、state、registry、
共享 adapter、构建配置或其他 agent 文件，也没有发送远端任务。
未运行、安装或探测 Lean/Lake，未做远端编译。elaboration/kernel 证据数量为 **0**。
以下内容均是未编译候选脚本及静态审阅，不是编译成功、VERIFIED 或 admission 结论。

## 交付端点与依赖

新 namespace 为 `RouteBO1Body4SourceJacobianBridge20260907`。
只直接导入 `RouteBO1Body4SourceGramTargets`，不导入旧 proof attempt 或 Gram repair。
最终声明直接引用原目标，没有重定义/放宽它们：

```lean
theorem jv_attempt : Body4JvTarget := by
  exact jv_of_source_geometry source_axes source_displacements

theorem jw_attempt : Body4JwTarget := by
  exact jw_of_source_axes source_axes
```

这两个脚本的声明类型没有新前提，但尚不能据文本认定实际 inhabitant 已建立。
中间的 `jv_of_source_geometry` 明确依赖原 `Body4SourceAxesTarget` 和
`Body4DisplacementsTarget`；`jw_of_source_axes` 只依赖前者。
这些 conditional ports 不是独立完成的 source 证明。最终脚本使用本文件的
`source_axes/source_displacements` 候选证明来填充它们，未将未完成 child 变成公理。

| 层 | 本文件内容 | source 依赖/边界 |
|---|---|---|
| 索引 | `activeJoint`, `prefixSlot`, `parent_slot`, `active_guard`, `activeJoint_roundtrip` | 显式 Fin 4 → Fin 6/7；保留父轴槽与 joint 值相同 |
| 最小 frame 几何 | `frame_origin_prefix`, `frame_axis_prefix`, `step3_translation`, `slot4_translation`, `frame_origin4` | 只展开 slots 0..3 的 origin/z 列及 slot 4 平移，不要求 X/Y 列或 slot 4 旋转矩阵 |
| source 绑定 | `source_origin_prefix`, `source_axes`, `source_com`, `source_displacements` | 使用现有 source-to-frame/index adapter，将源列表接口连接到上述坐标 |
| 基底 | `lift_cross`, `basis_cross`, `lift_dot_isometry` | 叉积保持进入 Jv 证明；内积保持独立留给后续 Gram 消费 |
| Jacobian | `active_cross_columns`, `active_jv_of_geometry`, `active_jw_of_axes`, `inactive` | active 0..3，inactive 4/5；结合为原 Jv/Jw 目标 |

`frame_origin_prefix/frame_axis_prefix` 的有界展开保留 accessor 的左结合乘积。
slot 4 仅通过 `F4 = F3 * T3` 和 `T3[:,3] = (0,0,19/100,1)` 处理。
因此没有把 joint 3 的旋转角误带入 COM 平移，仍保留父轴的
`+ cos(phi) e_z` 符号。

## body 3、active joint 3 与 inactive columns

`body4_index` 明确 human body 4 是 `(3 : Body)`。
`body4_com_indices` 明确其 COM 使用 origin slots 3 和 4；source COM 脚本实际调用
`source_body4_com_uses_slots_3_4`，而非改用其他 body 的 COM 公式。

| joint 索引 | source guard | Jv 列 | Jw 列 |
|---|---|---|---|
| 0 | active | `vec q (-d) (aa q) 0` | `vec q 0 0 1` |
| 1 | active | `vec q (pp q) 0 (-qq q)` | `vec q 0 1 0` |
| 2 | active | `vec q (e*cos(phi q)) 0 (-e*sin(phi q))` | `vec q 0 1 0` |
| 3 | active | 平行叉积得到零 | `vec q (sin(phi q)) 0 (cos(phi q))` |
| 4, 5 | inactive，`3 < j.val` | `bodyJv_zero_of_inactive` 得零 | `bodyJw_zero_of_inactive` 得零 |

joint 3 的关键链是
`displacement q 3 = (fun a => e * prefixZ q 3 a)`，随后
`cross3 u (fun a => e * u a) = 0`。
`active_cross_columns` 对该分支显式调用 `joint3_cross_zero`。
`active_joint3_source_columns` 再将两个最终目标专门实例化到 source body/joint 3，
同时列出零 Jv 和保留的 Jw。该分支不调用 inactive cutoff。

对于任意 `Joint`，最终脚本以 `j.val < 4` 分支；active 分支通过
`activeJoint_roundtrip` 消去 Fin proof 字段的包装，inactive 分支以严格不等式调用
两个 source semantic lemma，并枚举候选表的零列。这不是从 Fourier 缺行推断零列。
全域仍为任意 `q : Q6`，没有数值采样、q-cell 或非退化条件前提。

## lift / isometry 的精确含义

`lift q u = vec q (u 0) (u 1) (u 2)`，即绕世界 z 轴的定向旋转。
`lift_cross` 逐分量处理叉积：前两分量为环恒等式，第三分量用
`Real.sin_sq_add_cos_sq (q 0)`。`basis_cross` 用三元坐标向量实例化它，连接到原目标。

`lift_dot_isometry` 的完整结论为
`dot (lift q u) (lift q v) = dot u v`，有限和先规约为三个分量再使用单位圆。
这指欧氏内积保持，不声称裸 `Fin 3 → ℝ` 默认 Pi/sup 范数的 metric `Isometry`。
内积保持本身不能保证叉积方向；二者各有独立脚本。

原 `vcol/wcol` 已经是世界坐标向量，不需要在 source 接口再乘一次 lift。
Jv 的 source 绑定实际消费的是叉积运输；dot isometry 不是几何/source 等式的替代品，
也没有从局部 Gram 表反向恢复 source Jacobian。

## 精确 source mass 接口的后续边界

已读取 `RouteBO1PerBodyExactSource.lean`：`sourceBodyMass` 是
`contractMass (sourceContract q)`，现有 `sourceBodyMass_eq_bodyMass` 暴露其真实
`bodyMass/linkMass` 展开。body 3 的质量为 `2/5`，惯量对角项已经是 `1/15`，不可再除三。

未来须先让本文件及依赖在一致环境中通过编译/审计，才能把 Jv/Jw 等式与独立完成的
`Body4LinearGramTarget`、`Body4AngularGramTarget`、`Body4InertiaTarget` 及惯量收缩
组合成 `Body4SourceGramTarget`。旧 Gram repair 只是另一个未编译输入，不能作为已有
kernel 证据。新文件没有声明 `source_gram`、expected-entry、trace-fold 或 `h_body_4`。
piecewise 标量归一化、tagged trace fold、Float64 绑定、总矩阵与 registry admission
都不由这两个 Jacobian 目标自动得到。

## 已执行检查

静态检查覆盖直接 import、原目标端点、active/inactive guard、Fin 索引桥、显式条件
参数及写入范围。本文件包含 3 个定义、30 个 theorem 候选与对应 30 条未执行的
`#print axioms`。无 `sorry`、`admit`、新增 `axiom` 或 `unsafe` 声明；这仅描述本文件
文本，未审计传递依赖闭包。另检查行尾空白及旧输入/同目录旧文件的 SHA-256。

使用本机 Python/SymPy 1.14.0 做一次有针对性的内存内精确检查，未创建额外脚本或结果文件：

- 手工转录 `realDHStep`、Route-B 前四步 ct/st 与 alpha/a/d 常数，按原顺序乘矩阵。
- 用独立符号 `s0,c0,s1,c1,s2,c2`、角和多项式及有理系数，模三个单位圆关系约化。
- 覆盖 origin slots 0..4 的 15 项、父轴 0..3 的 12 项、COM 3 项、displacement 12 项、
  六列 Jv/Jw 各 18 项、joint 3 平行关系 3 项与角轴单位长度 1 项，以及 lift 叉积 3 项/
  内积 1 项；共 **86 个标量余项为零**，最终检查命令退出码 0。

检查首次因 Gröbner 基默认整数系数域不能接收 `21/100` 而中止；将检查器显式设为
`domain=QQ` 后通过。这是 Python 检查器的修正，没有发生 Lean 诊断或据此修改数学目标。
该检查不解析 Lean、不验证 source-list 接口或 import，也不是 elaboration/kernel 证据。

## 待执行的 Lean 检查

实际 Lean 错误日志：无。以下是静态风险与未来验证顺序，不是已观察到的编译错误。

1. 先在单一、记录版本的 Lean/Mathlib 环境按实际 imports 构建依赖，确保原 targets 可加载。
   若依赖先失败，记录原文件首个诊断；本任务不授权修改共享依赖。
2. 核对 prefix macro 的 Complex `.re` 常数、`Matrix.one_apply/mul_apply`、有限和与 match
   是否完全消去；这是新文件最主要的未运行几何证明点。若失败，在本文件拆分 slot lemma。
3. 核对 `prefixSlot/activeJoint/prevOrigin` 的转换与 adapter 的改写形状，特别是
   `frame_origin4/source_com` 的字面槽号，以及 `activeJoint_roundtrip` 的实例化。
4. 核对 `basis_cross` 的向量定义等同、有限分量归约、两个 conditional port 到最终
   原 target 的组合；确认 joint 3 仍走 active 分支且 Jw 未消失。
5. 整模块成功后检查全部 30 条 axiom 输出与依赖，排除 `sorryAx`/未授权新公理，保留完整
   日志、退出码与源码/olean 身份。仅出现 `#print axioms` 文本或孤立输出不算成功。

## 输入身份与范围核对

开始读取后的 Git HEAD 快照：`7cdeeb7764c70b4480b9db3d4b069d741d730699`。
哈希只绑定下列文件，不代表 import 闭包或编译证明。

| 文件 | SHA-256 |
|---|---|
| 新 `NEW_SOURCE_JACOBIAN_20260907_BODY4_BRIDGE.lean` | `F6C2EBB98CC50F4183B348EC95CFA722AEA6F3E72E31375E49B42F4B5A99628E` |
| `RouteBO1Body4SourceGramTargets.lean` | `2D0D2794EDFE745D63A2970C36B53765F3B4BD747480107B1EAB51CF2E2C3CA9` |
| `RouteBO1PerBodyExactSource.lean` | `C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553` |
| `BodySemanticCore.lean` | `FE15F6CA9993F55FC56E6D2C9CCA5FA8C7F6E9530B9B900A6F111ED96715149C` |
| `SourceContractIndexAdapter.lean` | `2A18C7B6733AF6245F3E5BA6DEDD714A9EC7F28FD010122C0258611CE7AAC452` |
| 旧 `RouteBO1Body4SourceGramProofAttempt.lean` | `8D8477F64347B6875B0995D2094FB6F8E8ABA837BC25FFDEF53310EB98B1A322` |
| 旧 `NEW_REPAIR_20260907_BODY4_GRAM_ALGEBRA.lean` | `B508CA7FB043B2E365E4A99650D9C60C7B4420E01DC221401C13768EABD0D94E` |
| 旧 `REVIEW_20260907_BODY4_SOURCE_GRAM_PROOF_ATTEMPT.md` | `9641D8336AFC705B292C460C25679BF70805515FAFD3B02FD386B457E11F8E86` |
| 旧 `REVIEW_20260907_NEW_REPAIR_BODY4_GRAM_ALGEBRA.md` | `0C6A3B614E64F8F8D8E4300C444B25504506DE006503DCC4572DEB96F64F3D6A` |

工作期间 Git 状态出现其他 agent 的 task queue、body-5、O0 source seam 与 cone 文件变动。
最终只读检查还观察到 `artifacts/routeb_6dof/state.json` 的并发修改标记；本轮没有
写入或恢复该文件。因此这里不声称整个工作区/state 在时间上保持不变。
本轮未写入、恢复或提交这些并发变动；本任务的写操作仅针对上述两个新文件。
