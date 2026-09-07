# Body-6: six source axis dot products

本轮为真实 `SourceAxisDotTarget` 新增六个轴点积 source-seam proof attempt，并接入已有 endpoint→center→第六列 Fourier 候选链。**所有 Lean 声明仍为 UNCOMPILED / NOT_RUN**；没有运行 Lean/Lake，也没有给出已验证的 source、coverage、registry 或完整 `h_body_6` 结论。

## 新增文件

| 文件 | 职责 |
| --- | --- |
| `NEW_BODY6_SLICE_AXIS_Core20260907.lean` | 只导入 Mathlib：两个旋转的点积不变性、局部轴表达式、六个点积的标量证明候选 |
| `NEW_BODY6_SLICE_AXIS_Geometry20260907.lean` | 真实 source axis→parent slot→prefix rotation column→局部旋转表达式→六个点积；不导入 body Fourier 表 |
| `NEW_BODY6_SLICE_AXIS_Consumer20260907.lean` | 精确接入既有 `SourceAxisDotTarget`、第六列 source/slice equality 与 `1/60` 对角候选；保留全矩阵边界 |
| `NEW_BODY6_SLICE_AXIS_check20260907.py` | 只读 exact symbolic polynomial 检查；读取并锁定既有 DH source 定义，不读取 Fourier CSV |
| 本 review | 数学结构、索引契约、依赖、检查及剩余边界 |

本轮只新增指定目录内以上五个文件，没有修改之前的 body-6 文件、body-5 文件、state、registry、共享脚本或其他任务文件。没有执行 git add/commit 或 comparator。

## 导入依赖与建议分离检查

直接导入如下；这些是源码层依赖，不是已确认可解析的 Lake import closure。

| 新模块 | 全部直接 imports |
| --- | --- |
| `NEW_BODY6_SLICE_AXIS_Core20260907` | `Mathlib` |
| `NEW_BODY6_SLICE_AXIS_Geometry20260907` | `NEW_BODY6_SLICE_AXIS_Core20260907`、`FrameSlotHomogeneousPrefixV2`、`SourceContractAdapter` |
| `NEW_BODY6_SLICE_AXIS_Consumer20260907` | `NEW_BODY6_SLICE_AXIS_Geometry20260907`、`NEW_BODY6_SLICE_STEP6_DataLeaf20260907` |

关键既有传递依赖：

- `FrameSlotHomogeneousPrefixV2` → `ConcreteStepHomogeneous`、`HomogeneousPrefixProjection`、`FrameSlotAccessor`。
- `ConcreteStepHomogeneous` → `RealDHStep`、`HomogeneousRotationProjection`；`RealDHStep` → `FrameRecursion` → `FourierNormalForm`，用于准确的 DH 相位/常数定义，不是 body Fourier CSV。
- `HomogeneousPrefixProjection` → `HomogeneousRotationProjection`、`RotationPrefixOrthogonality`；后者导入 `MatrixOrthogonalityClosure`。本轮没有把既有 row-orthogonality 当成任意矩阵的 column-orthogonality；点积不变性使用新 Core 的显式三维旋转证明候选。
- `SourceContractAdapter` → `FrameSlotAccessor`、`BodyContractCore`；slot accessor 经 `FramePrefixIndex` 连接 source frame list 与有限 prefix。
- 只有 Consumer 引入旧 `STEP6_DataLeaf` → `STEP6_Bridge` → `STEP6_Core`、`NEW_BODY6_SLICE_20260907`，再连接旧 literal data、canonical evaluator 与 `RouteBO1PerBodyExactSource`。

本 review 不声称以上列举替代完整 import-closure receipt。建议未来获授权后先独立检查 Core，再 Geometry，最后 Consumer；否则旧 610-row literal/旧 tactic 的失败可能遮住六轴 geometry 自身的检查结果。本轮没有执行这些 Lean 检查。

## 精确索引与 source 边

索引契约如下：

| 对象 | Lean 类型及含义 |
| --- | --- |
| `i` | `Fin 6`，零基 human joint index `0..5` |
| `prevOrigin i` | `Fin 7`，值严格为 `i.val`，parent frame slot；不是 `nextOrigin i` |
| `a` | `Fin 3`，笛卡尔分量 `0..2` |
| rotation column | `2 : Fin 3`，prefix rotation 的第三列 |
| homogeneous embedding | `Fin 3 → Fin 4`，保留 `.val`；既有两个 `embed3` 定义仅范围证明项不同 |
| 第六刚体 | `5 : Fin 6`；其第六关节使用 slot 5，尚未乘第六 DH step |

`source_axis_rotation_column_attempt` 的具体函数等式是：

```lean
(sourceContract q).axes i =
  column (rotationAt q (prevOrigin i)) (2 : Fin 3)
```

它先使用已有 `source_axis_function_eq_frame_contract`，再通过 `FrameSlotHomogeneousPrefixV2` 的 prefix shape bridge 和 `homogeneousPrefix_rotationBlock_eq` 投影到既有 `stepRotation` 的 prefix。没有引入自由的“source 与局部模型相等”假设，也没有用 CSV 行或 Python 布尔结果替代该接线。

`stepRotation` 继续来自真实 `routeBRealStepMatrix` 的左上 `3×3` 子块。前五步平移不参与轴点积；第六步角度也不应进入 parent axis 5。

## 共同旋转与局部向量

设零基角坐标为 `q 0,...,q 5`，令

\[
x=q_1+q_2,\qquad y=q_3,\qquad z=q_4.
\]

这里 `q_1+q_2` 对应 human `q₂+q₃`。定义

\[
Y(t)u=(u_0\cos t-u_1\sin t,\;u_0\sin t+u_1\cos t,\;u_2),
\]
\[
P(x)u=(\cos x\,u_0+\sin x\,u_2,\;u_1,\;-\sin x\,u_0+\cos x\,u_2).
\]

二者的点积不变性只用相应 `sin²+cos²=1` 和有限三项展开。局部轴取

\[
\begin{aligned}
w_0&=(0,0,1),\\
w_1=w_2&=P(x)(0,1,0),\\
w_3&=P(x)(0,0,1),\\
w_4&=P(x)(-\sin y,\cos y,0),\\
w_5&=P(x)(\cos y\sin z,\sin y\sin z,\cos z).
\end{aligned}
\]

真实 source 接线的候选结论为 `axes_i = Y(q 0) w_i`。因此点积的 `q 0` 依赖通过共同旋转消去；不是通过 Fourier 支持中 `nu1=0` 反推消去。

实际 prefix 推导只需：

- slot 0、1、2 的第三列，以及 slot 3 的三列，做至多前三个 `3×3` step 的有界展开。原定义中的 human q₂ 偏移 `-π/2` 与 q₃ 偏移 `+π/2` 均通过 `routeBRealCos/Sin` 读入。
- slot 3 的列依次为 `Y P e₀、Y P e₁、Y P e₂`。
- 第四步（zero-based step 3）对任意 prefix `R` 的列递推：`C₀'=cos y C₀+sin y C₁`，`C₁'=-C₂`，`C₂'=-sin y C₀+cos y C₁`。
- 第五步（zero-based step 4）第三列为 `sin z C₀'-cos z C₁'`，得到 `w₅`。

后两步保持任意 prefix 矩阵作为参数，只展开单次三项乘法；没有展开 source list、body mass 或 610 行 Fourier fold。

## 六个 source 点积

以下每一项都有独立命名的 source theorem candidate，左端都是 `Σ a : Fin 3, (sourceContract q).axes i a * (sourceContract q).axes 5 a`：

| `i : Fin 6` | 右端 | 候选名 |
| --- | --- | --- |
| 0 | `cos x cos z - sin x cos y sin z` | `source_dot_0_5_attempt` |
| 1 | `sin y sin z` | `source_dot_1_5_attempt` |
| 2 | `sin y sin z` | `source_dot_2_5_attempt` |
| 3 | `cos z` | `source_dot_3_5_attempt` |
| 4 | `0` | `source_dot_4_5_attempt` |
| 5 | `1` | `source_dot_5_5_attempt` |

`source_dot_all_attempt` 统一量化任意 `q` 与所有 `i : Fin 6`。Consumer 中的 `source_axis_dot_target_attempt` 仅展开 `phi/dotResult/sixthAxisDot`，连接到原目标；没有改变目标的定义、角符号或域。

第六列 candidate chain 现在是：

```text
真实 source axes / prefix rotation
  → source_axis_local_attempt
  → source_dot_all_attempt
  → source_axis_dot_target_attempt : SourceAxisDotTarget

此前 endpoint/center/source Gram + 23-row Fourier/data 候选
  + source_axis_dot_target_attempt
  → sixth_source_slice_attempt
```

因此本轮新第六列 theorem 候选不再将 `SourceAxisDotTarget` 暴露为调用者需要供应的参数；但整个导入与 proof-attempt 链仍未获本机 Lean 验证。这是候选代码层面的推进，不是 source proof 的准入。

`sixth_source_diagonal_attempt` 消费相同 source Gram 和轴点积候选，得到真实第六对角 `1/60` 的尝试；该值仍无法区分 aggregate 与 body-6，因为其他刚体的 joint 6 不活跃。

## 符号检查及其限度

运行：

```text
python -B examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_AXIS_check20260907.py
```

使用 SymPy 1.14.0，检查器从 SHA-256 锁定的 Lean source 文本读取 `routeBRealCos/Sin` 的实际相位分支、`routeBCosAlpha/SinAlpha`，核对 `realDHStep` 左上九项，再从单位矩阵按右乘顺序构造六个 parent axes。

它检查独立书写的局部旋转公式，结果：

- 18 个坐标残差逐项为零多项式，尚不需要使用单位圆约束。
- 六个点积残差对 `s_k²+c_k²-1`（`k=0..4`）做精确有理系数 polynomial reduction，余项全部为零。
- axes 均不含第六步的 `s5/c5`；parent/pre-step 索引正确。
- 未读取 Fourier CSV；没有数值采样、容差或拟合。
- Geometry 的直接 import 仅 Core、FrameSlotHomogeneousPrefixV2、SourceContractAdapter；新 Lean 文件无 `sorry/admit/axiom/opaque` 声明。

这是数学公式和源常数转写的符号核对，不是对 Lean tactic 的解析、elaboration、kernel check 或编译 receipt。特别是 import closure、V2 投影、finite-index reduction 和 tactic/API 使用仍可能需要后续环境中的修复。

```text
Core SHA-256:     8b4d51e5b77847f29d67314d55e7d785171d515894a35bb18f53bd31b9cd2e2f
Geometry SHA-256: c06310d20f7317d196317da4b185fd5c6e56a01b5cc5fc1feb05f428a1ef3ca4
Consumer SHA-256: e9c51cdc7106728425f25469a79b25666f8d468085ea3fd0064d75ced76764fb
```

## 仍保持的缺口

全域 `q : Fin 6 → ℝ` 不变，没有换成 `q=0` 或 cell 内陈述。`full_source_boundary_attempt` 仍明确要求 `AllEntriesGramFourierTarget` 与 `EmptyFourierTarget`：全部 36 个条目及一基 `(4,5),(5,4),(5,6),(6,5)` 的零补集不能由第六列候选替代。`LegacyTraceBindingTarget` 也没有在本轮填充。

下一条独立数学瓶颈可以从左上 `5×5` 的 source linear-velocity Gram 着手；那里平移、质量与二次项真正参与，不能沿用第六列 `v₅=0` 消项。它仍需十四个非零上三角条目、一个上三角零条目、转置及 Fourier 接线，才能考虑完整 body-6 equality。

本轮不写 state/registry，不运行 comparator，保持 `lean_lake_run=false`、`source_axis_dot_proven=false`、`source_binding_proven=false`、`source_coverage_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。未提供正式 coverage、registry 或 O1 aggregate certificate。

## 未闭合前提逐层清单

| 层 | 本轮精确范围 | 仍未闭合/未核验的前提 |
| --- | --- | --- |
| Source geometry | 全域 `q : Fin 6 → ℝ`，全部六个真实 parent axes，以及与 axis 5 的六个点积 | 新 Core、prefix projection、索引桥与 source geometry proof bodies 尚无 Lean kernel/axiom receipt；符号检查不能代替它们 |
| Source mass | 通过旧 endpoint/center/source Gram 候选消费新轴点积，尝试证明第六列及第六对角 `1/60` | 旧 source mass/endpoint/Gram 导入链同样未在本机核验；左上 `5×5` 的真实速度 Gram 未闭合 |
| CSV / finite rows | 本轮 source geometry 完全不读取 body CSV；Consumer 复用之前的 23-row/literal 候选 | 旧 610-row filter 到 23-row list 的 Lean literal equality、map/sum/fold 接线及 `LegacyTraceBindingTarget` 仍无已验证 receipt；Python 系数相等不是证据替代 |
| Coverage | 保留全域全部 36 个矩阵项和四个零项的显式前提 | `AllEntriesGramFourierTarget`、`EmptyFourierTarget` 均未供应；单列与其对角不代表完整 body-6 coverage，更不是 aggregate coverage |
| Lean environment | 只有源码候选；没有运行 Lean/Lake | pinned toolchain、Mathlib/import closure、全部 tactic elaboration、编译结果和 axiom report 尚未核验 |
| Comparator / registry | 无写入、无 comparator run | 独立 payload/source key 的权威 source binding、同 key comparator receipt、覆盖证明和显式准入均未供应；registry 保持 pending、不可准入 |

## 建议 DAG child（仅建议，未创建节点）

以下名称是待讨论/登记的 child 标识建议，不是现有 node id，也没有写入 state。

| 建议 child | 数学产物 / 接口 | 父依赖与出口边界 |
| --- | --- | --- |
| `O1_body6_source_axis_dot` | 本轮 Geometry 的全域六轴点积及 Consumer 的 `SourceAxisDotTarget` | 依赖源定义、prefix rotation/index bridge 与 Core；当前状态建议 `candidate_uncompiled`，不可作为已完成 source leaf |
| `O1_body6_column6_literal_binding` | 独立 Lean 证明完整表第六列 filter = 23-row list，并证明其 Fourier fold | 依赖固定 CSV/literal identity 与 STEP6 Core；不依赖从 Fourier 反推 source，也不供应 coverage |
| `O1_body6_column6_source_slice` | `∀ q i, sourceBodyMass q 5 i 5 = sliceEvaluator q i 5` | 合并 endpoint/center/source Gram、六轴点积和 literal/Fourier 三条链；即使未来该 child 核验通过也只覆盖第六列 |
| `O1_body6_top_left_velocity_gram` | 左上 `5×5` source 速度列、质量项及 Gram 展开 | 下一条独立数学工作；保留真实 origins/center/axes 来源，不能用第六列消项或 CSV 支持替代 |
| `O1_body6_all_entries_zero_complement` | 全 36 项 source/Fourier equality 与四项零补集 | 依赖左上块、末行/列、对称性及精确 Fourier 证明；出口才可能供应完整 `SourceBindingTarget`，仍不直接登记 registry |
| `O1_body6_legacy_trace_and_admission` | canonical evaluator→既有 trace evaluator 的接线及后续准入证据审计 | 依赖完整 source/coverage、literal provenance、未来获授权的 Lean/axiom 和同 key comparator receipts；必须单独 fail-closed |

当前可交付状态：**五个 scoped 新文件完成；符号公式检查通过；全部 Lean/source/CSV-lift/coverage/registry 的正式证据仍按上述边界开放。**
