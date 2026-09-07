# Body-6 endpoint / 23-row Fourier proof attempts

本轮新增三份 Lean proof-attempt 文件、一份只读 Python 检查和本 review，均在指定目录。没有改动上一轮 slice、state、registry、shared scripts 或其他任务文件。**未运行 Lean/Lake；所有 theorem 声明都是未编译候选，不是已核验的 source/coverage 证明。**

本轮具体推进：`Body6EndpointTarget` 已有接到真实 source 定义的证明代码候选；`SixthColumnFourierTarget` 已有纯三角折叠、完整列过滤和 literal 数据归约组成的候选链。第六列实际 source 等式仍需 `SourceAxisDotTarget`。整个 `sourceBodyMass q 5` 的全矩阵等式仍需独立的 36-entry Gram/Fourier 证明及零补集、旧 evaluator 接线。

## 文件与独立边界

| 文件 | 角色 |
| --- | --- |
| `NEW_BODY6_SLICE_STEP6_Core20260907.lean` | 只导入 `Mathlib`：通用末列矩阵乘法、endpoint→center→速度零、23 行纯 Fourier 三角恒等式 |
| `NEW_BODY6_SLICE_STEP6_Bridge20260907.lean` | 接入已有真实 source 定义；压缩相位到 canonical atom 的有限和 lift；generic filter；条件式 source 与全矩阵 seam |
| `NEW_BODY6_SLICE_STEP6_DataLeaf20260907.lean` | 将完整 610 行表的第六列 filter 与精确 23 行表的 literal equality 隔离为 `rfl` 归约候选；连接 Fourier 目标 |
| `NEW_BODY6_SLICE_STEP6_check20260907.py` | 默认只读、stdout 输出；解析 Core 中实际 23 行 literal，与固定 CSV 和独立 exact Laurent 运算核对 |

“source-independent”指 Core 的证明只依赖任意实矩阵/向量/相位以及本文件的明确有限列表。Core 没有导入 sourceContract、真实 DH 定义、610 行数据或任何 receipt。Bridge 才把通用结论接到已有 source；不能把 Core 的局部恒等式直接当作 source proof。

## Endpoint 的最小代数结构

对任意实 `4×4` 矩阵 `F,A`，若 `A` 的第四列为 `[0,0,d,1]ᵀ`，则

\[
(FA)_{a,3}=F_{a,3}+dF_{a,2}.
\]

`product_endpoint_attempt` 只展开这一列的四项有限和；不要求 `F` 正交，也不要求其末行为 homogeneous 标准形式。它没有展开前五步 DH。

实际第六步接线分为三处：

1. `step6_last_column_attempt` 从既有 `routeBRealStepMatrix 5 t`、`realDHStep`、`routeBA` 和 `routeBD` 展开四个末列元素，使用 `a₆=0,d₆=7/100`。
2. `slot6_recursion_attempt` 按现有 `prefixFrame` 的乘法括号结构，以 `rfl` 连接 `slot6 = slot5 * step6`。
3. `source_endpoint_attempt` 通过既有 source origin/axis 函数等式，连接真实 `sourceContract` 的 `o₅,o₆,z₅`，再应用通用末列恒等式。

得到的目标仍精确是：

```lean
∀ q a, (sourceContract q).origins (6 : Fin 7) a =
  (sourceContract q).origins (5 : Fin 7) a +
    (7 / 100 : ℝ) * (sourceContract q).axes (5 : Fin 6) a
```

`source_center_attempt` 随后消费这份 endpoint 候选，给出 `c₆=o₅+(7/200)z₅`；`source_sixth_linear_zero_attempt` 接到真实 `bodyJv` 的第六列，利用 `z₅×((7/200)z₅)=0`。`source_gram_attempt` 消费 center 候选及上一轮 source-column/diagonal-inertia 候选，保持质量 `3/20`、惯量 `1/60` 不变。

这些声明引用的现有 lemma 与上一轮 tactic body 都没有在本机重编译；代码链完整并不构成该链已经通过 Lean 的证据。

## 23 行完整带符号 Fourier 折叠

Core 使用三个任意实数 `x,y,z`，后续实例化为零基 Lean 坐标：

```text
x = q 1 + q 2
y = q 3
z = q 4
```

每行保留 `(row,nx,ny,nz,coeff)`，lift 后频率严格是 `[0,nx,nx,ny,nz,0]`，列索引恒为 `5 : Fin 6`，虚部恒为零。这里利用该列实际支持中的 `nu2=nu3`；没有压缩整个 body-6 的一般频率，更没有删掉负频率或增加因子二。

`rows23_fold_attempt` 的具体目标是：

\[
\operatorname{eval23}(x,y,z)=\frac1{60}
\begin{bmatrix}
\cos x\cos z-\sin x\cos y\sin z\\
\sin y\sin z\\
\sin y\sin z\\
\cos z\\
0\\
1
\end{bmatrix}.
\]

其代码对六个 row 分情况，以 `Real.cos_add/sin_add` 等展开 23 个实 Fourier atom 后 `ring`。各行系数数目是 `12,4,4,2,0,1`。这是实际 tactic attempt，未把这个三角等式作为新的假设或 axiom。

后续连接：

```text
rows23_fold_attempt
  + lift_atom_attempt / lift_rows_attempt
  → local_column_fold_attempt

generic filter_column_attempt
  → full_filter_attempt

literal_column_binding_attempt [isolated rfl attempt]
  + local_column_fold_attempt + full_filter_attempt
  → sixth_column_fourier_attempt : SixthColumnFourierTarget
```

`filter_column_attempt` 对任意 canonical list 做列表归纳；选中列的和与完整 evaluator 在该列的值相同。它不要求源支持恰为 23 项，也不从 row count 推导数据相等。

DataLeaf 中的 `literal_column_binding_attempt` 要求的是完整具体列表等式 `sixthColumnRows = localCanonicalRows`，包含频率、条目和精确有理系数。`rfl` 候选可能在后续 Lean 环境中需要归约/栈深/API 修复；本轮没有试运行它。独立文件仅局部设置 `maxRecDepth 8192`，没有外部 oracle、`native_decide`、占位证明或 admission 标记。

## 第六列的剩余 source 义务

`source_sixth_column_with_axis_premise_attempt` 只剩一个显式数学前提：

```lean
SourceAxisDotTarget
```

即对每个任意 `q`、每个 `i : Fin 6`，证明真实 source axes 的 `Σₐ zᵢ[a] z₅[a]` 等于既有 `sixthAxisDot q i`。endpoint 只决定 translation/center，不能推出这些轴点积。最小下一步是利用前五步 rotation 的结构证明这六个轴点积；不应继续从 610 行数量或 Python 结果添加假设。

“只剩一个前提”描述本轮第六列候选 theorem 的接口，不表示导入链、endpoint、finite fold 或 literal binding 已获 Lean 验证。

## 全域、36 项和零补集继续保留

`global_source_and_zero_seam_attempt` 仍要求：

```lean
(hall : AllEntriesGramFourierTarget)
(hzero : EmptyFourierTarget)
```

其中 `hall` 量化所有 `q : Fin 6 → ℝ`、所有 `i,j : Fin 6`，涵盖完整 36 项；`hzero` 明确保留 CSV 一基 `(4,5),(5,4),(5,6),(6,5)` 的四项零补集。该 seam 同时输出全域 `SourceBindingTarget` 与四项真实 source 为零的结论，不能用第六列 theorem 调用它。

未提供 `AllEntriesGramFourierTarget`、`EmptyFourierTarget` 或 `LegacyTraceBindingTarget` 的无条件证明。没有将 cell 内等式或 `q=0` 等式替代全域目标。`mu*I` 继续排除在 body slice 外。

610-row aggregate-shaped bucket 继续不作为 source 证明；此前 57 个差异系数的负控没有改变。第六列本来与 aggregate 相同，所以本轮 23 行结果也不能用作 body 标签鉴别或 aggregate 准入证据。

## 已执行检查与状态

执行：

```text
python -B examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STEP6_check20260907.py
```

检查通过：Core 仅导入 Mathlib；23 个 literal 与固定 canonical CSV 第六列按顺序逐项相等；六行解析式经独立 Fraction/Gaussian-rational Laurent 运算逐键相等；计数为 `12,4,4,2,0,1`；新 Lean 文本无 `sorry/admit/axiom/opaque`；全矩阵和零补集前提仍存在。旧 CSV、旧 Data.lean、旧 seam.lean 的 SHA-256 与上一轮一致。

这些检查不解析、elaborate 或 kernel-check Lean。检查器的解析式是 Python 中独立书写的对应数学表达式，不会检验 Lean tactic 的正确性。

```text
Core SHA-256:     6093cab91de8c12fb165e0a5e75e812ed9a52a8c7a87365f849c03dfe7ebbf28
Bridge SHA-256:   f33a23b7f7510d652a6a03c31b1f7f32f5485a14637064cb4eb332814c0d5cea
DataLeaf SHA-256: 691d91adc207decf4e373e520363e94ab736aa9520a6200fd58bb5e126a8ab13
```

本轮保持 `lean_lake_run=false`、`source_endpoint_proven=false`、`source_binding_proven=false`、`source_coverage_proven=false`、`lean_literal_binding_proven=false`、`registry_eligible=false`、`registry_status=pending`、`formal_certificate_allowed=false`。这里只输出新 sidecar 候选及检查结果，没有写入 state/registry 或运行任何 comparator。
