# Body-5 G3/G4 与有限 trace decomposition：可修复证明骨架

日期：2026-09-07。状态：`OPEN_UNCOMPILED_PROOF_SKELETON`。
human body 5 = zero-based body 4；下文 joint、entry、q 均使用 zero-based 编号。

本轮新增两份 Lean 文件，包含 21 + 29 = 50 个具体 theorem proof body，
以及本 review。所有声明都只是未编译尝试：`parsed=false`、`elaborated=false`、
`kernel_checked=false`、`axioms_checked=false`、`verified=false`。
没有运行本机 Lean/Lake，没有启动远程编译，也没有产生编译 receipt。

## 交付与源绑定前提

- `NEW_BODY5_GramTraceSkeleton20260907.lean`：G3 对角惯量缩并、G4 标量叶、
  上三角与对称性接线；最终 source-to-piecewise 仍显式接收 columns 和 isometry。
- `NEW_BODY5_FiniteTraceSkeleton20260907.lean`：完整标签编码、57 行 canonical
  permutation、任意 seed 的 fold、q3 源行切片、独立 trace 转置，以及条件式最终接线。

两文件只导入既有 targets / 新 Gram 文件。已经完整阅读既有
`RouteBO1Body5GeometryColumnsProofAttempt20260907.lean`，但不把它作为新文件的 import：
这样 G3/G4 与 trace 的后续检查不必先接受尚未编译的 G1/G2 尝试。

| 依赖 | 数学或源绑定作用 | 本次接口如何体现 |
|---|---|---|
| `Body5ColumnsTarget` | 真实 sourceContract 的 bodyJv/bodyJw 等于局部列的 lift；这是几何源绑定前提 | `columns_to_gram_attempt` 与最终 `source_trace_conditional_attempt` 的显式参数 |
| `Body5LiftIsometryTarget` | dot 的旋转不变性；纯标量代数，不是新的外部 source 数据 | 为忠实实现既有 G3 类型保留为参数；既有 geometry 文件有独立未编译尝试 |
| `sourceBodyMass_eq_bodyMass` 与具体 mass/inertia 定义 | 固定本体编号、质量 3/10 和已经除以 3 的惯量 1/30 | 使用当前导入定义；不增加一次 `/3`，不假设一般惯量也各向同性 |
| `canonical_codes_attempt` / 解码后的 Perm | 冻结 generated rows 与新 canonical rows 的完整源数据绑定 | 封闭的有限 `decide` 证明尝试；不是外加公理，也尚未执行成功 |
| `off_body_tags_attempt` | 全列表中前四块和 body 6 块的 body 标签排除本体 4 | 只检查标签，配合任意 seed 的通用消去引理 |
| `q3_source_codes_attempt`、`transpose_codes_attempt` | 分别绑定原始 q3 切片和完整转置多重集 | 保留全部原始标签、重数与分母；各有独立有限尝试 |

最终 `source_trace_conditional_attempt` 的外加参数只有 columns 与 isometry。
这不意味着其他叶已经有 kernel 证明：它引用的 source 定义、数据 Perm、fold 和标量
证明体也全部需要检查。G1/G2 的旧文件或 receipt 不能代替这两个参数的已接受 witness。
CSV → generated evaluator 的生成正确性、外部 source/state key 的权威性、Julia Float64、
libm、覆盖与 O0 都不由这个 exact-real 定理接口证明。本轮不新增这些前提的 witness。

## G3：缩并先于几何展开

`diagonal_inertia_attempt` 对任意 u,v : Fin 3 → ℝ 处理

```text
sum_a sum_b u[a] * I4[a,b] * v[b] = (1/30) * dot(u,v).
```

它只展开 9 个惯量项；对角项留下 3 项，非对角项为零。
`columns_to_gram_attempt` 再将四个实际 Jv/Jw 列函数替换为 lift，并调用两次
isometry。它不重新展开 prefix frame、COM、叉积或全部 source trace。
v3=0、v4=0 和 joint 5 inactive 都属于 columns 前提的来源，不能从 Gram 的结果反推。

## G4：给出残差系数，避免大规模盲目三角展开

令 x=q1、phi=q1+q2，沿用 targets 的 A、P、Q。标量证明体使用
`linear_combination` 的确切有理系数，方便后续定位归一化错误。

| 标量叶 | 精确恒等式 / 残差分解 |
|---|---|
| `sin_square_attempt` | sin²(t)=(1-cos(2t))/2，由单位圆与 cos(t+t) 各取 1/2 |
| `sin_cross_attempt` | sin(x)sin(phi)=(cos(q2)-cos(2x+q2))/2 |
| `cos_cross_attempt` | cos(x)cos(phi)+sin(x)sin(phi)=cos(q2) |
| `pq_norm_attempt` | P²+Q²=401/5000+(399/5000)cos(q2)；单位圆残差系数 441/10000、361/10000，cross 残差系数 399/5000 |
| `pq_projection_attempt` | P cos(phi)+Q sin(phi)=19/100+(21/100)cos(q2)；残差系数 19/100、21/100 |
| `gram00_attempt` | 两个 sin-square 残差系数 1323/100000、1083/100000；sin-cross 残差系数 1197/50000 |

G11、G12、G22、G33 分别只需乘对应叶以 3/10、57/1000、1083/100000、1/30。
G44 先将 w4 的四次表达式因式分解为

```text
sin²(q3) * (sin²(phi) + cos²(phi)) + cos²(q3) = 1.
```

因此 w4 本身含 q3，但 G44 不含 q3。不能把含 q3 的列与含 q3 的 entry 混为一谈。
`gram_upper_attempt` 枚举 21 个上三角位置，其中六个使用专用 Gram 叶；
其余是有限坐标代数，包括 G04 的 product-to-sum。下三角通过
`gram_swap_attempt` 和直接核对冻结 piecewise 的 `piecewise_swap_attempt` 补齐。

旧 `O1_BODY_5_SOURCE_BRIDGE_RECEIPT.json` 的 `entry_2_3` prose 仍然有误。
本轮不改旧证据：正确值是 G23=G32=G34=G43=0；所有含 joint 5 的 entry 为零。
19 个非零位置、17 个零位置与既有 piecewise 保持一致。

## 有限 trace：先绑定整行，再重排加法

`RowCode` 精确保留 body、row、col、完整 Fin 6 频率函数，以及 real/imag 的
四个 numerator/denominator 标签。没有转成规范化有理数，没有遗忘转置或频率符号。
`decode_code_attempt` 是左逆；对编码后的 `List.Perm` 再 map 解码函数，得到原行 Perm。
这样不需要改 generated `BodyTraceRow` 或给它添加全局 DecidableEq 实例。

新的 `constants`、`reps17`、`repsQ3` 明列 7、17、8 行，canonicalRows 为
7 + 2*(17+8) = 57 行。常数包括 (1,2) 与 (2,1)，并非全部在对角线；各只计一次。
正频率 imaginary coefficients -63/12500、-57/12500 经
`a cos(theta) - b sin(theta)` 的约定合并后产生正的 sine 项。

`fold_add_sum_attempt` 对任意 seed 归纳：

```text
foldl (acc + contribution) rows seed = seed + sum(map contribution rows).
```

`full_to_block_attempt` 只用 append 与 off-body 标签消去 prefix/suffix；其他本体的
三角函数不进入实数计算。`block_to_canonical_attempt` 通过源行 Perm、有限和交换律、
flatMap 配对，得到 canonicalValue。`canonical_to_piecewise_attempt` 在共轭已经
合并后核对 36 个 entry；剩余是 guards、phase 和有理系数归一化，不需要 Fourier
唯一性、正交积分、无限级数或数值采样。

现有 `body5ConstantRows` / `body5RepresentativeRows` 在定义内使用 classical
判定。对这些定义直接 `decide` 可能卡在非计算性判定；新路线对显式 literal lists
做可计算编码判断，保留它们到原始 generated rows 的完整 Perm 义务。
这没有修改旧 targets，也没有把旧 F1 自动记为完成。

兼容入口的边界如下：

- `regroup_from_partition_attempt`：给定旧 `Body5ExactPartitionTarget`，用它的
  Perm 分量提供 F3 尝试；完整旧 F1 的 witness 仍未交付。
- `old_paired_to_piecewise_conditional_attempt`：显式要求旧常数筛选与 constants、
  旧代表筛选与 reps 的两个 Perm，提供旧 F4 的条件式尝试；这两个 filter bindings
  没有被悄悄当作已证事实。
- 新的直接 trace handoff 不依赖这两个兼容前提；它依赖更直接的原始 57 行 Perm。
  旧 `Body5Q3ExactPairsTarget` 的 classical-filter 类型同样没有被新编码定理冒充。

## q3 与转置的独立覆盖

| 有向 entry | 代表频率 (q1,q2,q3) | 每个原 atom 的 real coefficient | 共轭合并 |
|---|---|---|---|
| (0,4)、(4,0) | (1,1,-1) | +1/120 | +cos(phi-q3)/60 |
| (0,4)、(4,0) | (1,1,1) | -1/120 | -cos(phi+q3)/60 |
| (1,4)、(4,1)、(2,4)、(4,2) | (0,0,1) | +1/60 | cos(q3)/30 |

partner 是整个频率向量取负，所有这些 imag 标签都是 0/1。
`sourceQ3Rows` 在冻结 bodyTraceRows5 上按 frequency 3 ≠ 0 做新的可计算筛选。
`q3_source_codes_attempt` 将这 16 条实际源行绑定到 8 对；
`q3_source_fold_attempt` 与 `q3_source_off_support_attempt` 将完整有限 fold 接到
六个有向 entry，并在其余 entry 保持原 seed。
G04 的几何值 sin(phi)sin(q3)/30 正好接到上表两个 cos 项。

`transposeRow` 只交换 row/col，既不翻转频率，也不改变 imag。
`transpose_codes_attempt` 检查全体 57 行转置后与原列表的多重集相同；
`transpose_contribution_attempt` 交换 entry guard；`trace_transpose_attempt`
通过 Perm + sum 得到任意 seed 下的 trace 对称性。
它不使用 Gram 对称性。共轭配对和转置覆盖是不同的证明义务。

## 执行证据与具体修复入口

本次仅运行内存中的 Python/SymPy 1.14.0 精确诊断，不写诊断脚本或结果文件：

- 从当前 generated body-5 文本提取 57 条原行，从新 Lean 文件提取 7+17+8 条
  canonical 定义；按全部原始标签比较 Counter，完全一致。
- 转置 Counter 一致；q3 原始切片精确恢复 16 行，支持恰为六个有向 entry；
  57 个 entry/frequency keys 唯一，所有分母非零。
- 检查 G00、P/Q norm、P/Q projection、w4 因式分解和 q3 product-to-sum 的精确残差。
  数学表达式人工转录；这不是 Lean interpreter，也没有刷新旧 CSV checker 的等级。
- 初次诊断的 Unicode 输入解析失败，未执行完检查；改为显式 UTF-8 输入及 ASCII
  数字提取后，完整诊断通过。没有浮点采样。

两个新 Lean 文件共 50 个 theorem 声明；文本扫描未见 sorry/admit/axiom 声明、
native_decide/unsafe/implemented_by 或尾随空白。文本扫描不是 import/axiom 审计。
没有运行 Lean，所以以下是后续检查定位建议，不是已观察到的编译错误：

1. 先检查 diagonal_inertia、columns_to_gram 的 `change`/列函数 rewrite 匹配；
   如果 elaboration 未识别函数列，分别用 `congrFun (hcols q i).1 a` 建立逐坐标叶，
   再在三项 dot 内替换。不要扩大为 source prefix 全展开。
2. 标量叶失败时保留 phi 为同一个 trig atom，只规范化角参数；上表的线性组合
   已给出残差系数。w4 先因式分解，随后两次单位圆，不依赖四次全局求解。
3. 先单独检查 code/decode、fold 归纳和 List.map/Perm.sum_eq 的 API，再接数据。
   若 `decide` 的计算资源不足，把同一编码表按 (row,col) 分块并用 Perm.append
   合成；不得只证明 partner existence、忘记 multiplicity 或改用 native_decide。
4. 旧 classical-filter 兼容性用 predicate 化简/Perm.filter 单独建立；不要向旧
   filter 强塞计算实例，也不要改原文件。直接 canonical handoff 可先独立检查。
5. 本轮不执行上述编译步骤；import resolution、tactic 完成、资源用量、kernel 与
   依赖公理检查均未发生。所有 G/F 与最终 h_body_5 的接受状态保持 OPEN。

## 文件快照与写入边界

关键输入 SHA-256 在写入新文件前读取、写入后复核相同。以下散列只是字节绑定，
不证明数学或编译状态；没有宣称完整传递 import closure 已核查。

```text
RouteBO1Body5SourceTraceTargets.lean
aa314706ef2a42dca2e73b8b5ded22dc2f598e395e775e860f993da34739d9a9
RouteBO1Body5GeometryColumnsProofAttempt20260907.lean
ef515a822e237ae30b90caec9c2d3b123671d351d37ac0c27f337d210960a11b
RouteBO1PerBodyTraceAdapter.lean
6b50ae63c9770e3481f79511141c8cc55d592b5c550f686654c5e756584399ef
BodyTraceEvaluator.lean
b9845d37b5dcd16e1f9e142cb2e4d0e5571452993e843c85ac8cd643f6ba5dea
RouteBO1PerBodyExactSource.lean
c09b84677adef121488b3ceb53e886d0ef0b028c7979d91f8a7f9ba0fbfcd553
../routeb_body_semantic_core_lean/BodySemanticCore.lean
fe15f6ca9993f55fc56e6d2c9cca5fa8c7f6e9530b9b900a6f111ed96715149c
O1_BODY_5_SOURCE_TRACE_DECOMPOSITION_RECEIPT_20260907_44fcccf7bd1a.json
44fcccf7bd1aa2184802d63d1808a14a3551aeebc0edc6c4f4bc167f3d1e80f0
O1_BODY_5_GEOMETRY_COLUMNS_PROOF_ATTEMPT_RECEIPT_20260907_de0ef64225e3.json
de0ef64225e397fc6ea0846433cb17940950a905d1e4dcc3e5948da2563b22f9

NEW_BODY5_GramTraceSkeleton20260907.lean
118da0d3619e620c3f8c5f7869a20b325f363cd4434c3001867d2ef474bad626
NEW_BODY5_FiniteTraceSkeleton20260907.lean
16973c7960e15796b974dfeb15fb17ee07917126a93d0e5fe12cc7ceb5902f06
```

另外阅读了两个 receipt 对应的 decomposition/geometry review、旧 body-5 bridge
review/receipt、target check 与 COMPILATION_STATUS；旧编译描述不作本轮当前证明证据。

本轮所有写入均由 apply_patch 限于上述两个 NEW_BODY5_*.lean 与本 REVIEW_*.md。
没有修改 state、主 adapter、registry、generated evaluator、旧 receipt/review、
其他 agent 文件或构建配置。检查期间工作区出现范围外的并发变化，包括 state 与
其他脚本；本轮未修改、归属为本轮输出或回滚它们。
`registry_promoted=false`、`comparator_accepted=false`、`formal_certificate_allowed=false`。
