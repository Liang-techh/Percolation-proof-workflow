# O1 human body-4 source Gram：独立 proof-attempt review

日期：2026-09-07。状态：`EXPERIMENTAL_PROOF_ATTEMPT_UNCOMPILED`。

本文件为 immutable review revision 1，定稿后设置文件只读属性并记录 SHA-256。
后续发现、修复及远端 Lean 结果只能新增独立命名的 successor review，引用本版
哈希；不得原地更改本文件。只读属性是防误改措施，内容身份以哈希为准。

本轮新增同目录的 `RouteBO1Body4SourceGramProofAttempt.lean` 与本 review，
没有修改原 target、主 adapter、state、registry、构建配置或 CI，也没有创建
receipt、提交 GitHub agent 任务或运行本机 Lean/Lake。
这里的 theorem 声明均为未经 elaboration 的证明尝试；不能据此认定实际
inhabitant 已建立，也没有编译成功或 VERIFIED 结论。

## 1. 实际推进与边界

输入 `RouteBO1Body4SourceGramTargets.lean` 的 26 个 `Body4…Target` 均有
直接的 `theorem name : 原Target := by …` 候选脚本，另外有 10 个辅助 theorem，
总计 36 个。没有重新定义目标，没有把最终 equality 或任何未完成 child 作为
新增 theorem 参数；失败必须通过修复 proof body 解决。

全部输入变量仍为任意 `q : Q6`；human body 4 使用零基索引 `3`。
惯量对角系数 `1/15` 已含原 source 的除三，不再次除三。
端点为原 adapter 的 `h_body_4_expected_entry_target` 和
`h_body_4_source_expanded_target`。`h_body_4_trace_fold_target`、`h_body_4`、
Float64 绑定、总质量矩阵及 registry admission 均没有在本尝试中完成。

## 2. 候选声明与证明依赖

以下 theorem 名属于 `RouteBO1Body4SourceGramProofAttempt`。
下表全部 26 项的状态均为 **未编译 attempt／未验证**，没有例外；未获得任何
一项的本轮 Lean 结果。表中“证明内容”仅描述脚本意图，不是验证结论。

| 原 Target（省略 Body4 / Target） | 候选 theorem | 证明内容 |
|---|---|---|
| UnitCircle | `unit_circle` | `Real.sin_sq_add_cos_sq` |
| AngleAddition | `angle_addition` | `Real.sin_add`、`Real.cos_add` |
| MixedTrig | `mixed_trig` | 加角后用 `cos y` 乘单位圆等式 |
| SquareTrig | `square_trig` | 加角 x+x、单位圆、`nlinarith only` |
| ProductTrig | `product_trig` | x+(x+y) 的余弦与 mixed 等式作线性组合 |
| BasisDot | `basis_dot` | 三项有限和，单位圆乘 `r*r'+t*t'` |
| BasisCross | `basis_cross` | 两分量 `ring`，第三分量单位圆乘 `r*t'-t*r'` |
| PrefixSlots | `prefix_slots` | 现有左结合 accessor 的五个 `rfl` |
| PrefixColumns | `prefix_columns` | 48 个空间列分量；源 DH 常数、4 项乘法、加角、ring |
| Slot4Translation | `slot4_translation` | 只展开 F3*T3 的平移列；不展开 F3 或 q3 旋转 |
| SourceOrigins | `source_origins` | source origins→frame bridge，再接 prefix 与 slot4 |
| SourceAxes | `source_axes` | `source_parent_axis_slot`，保留 parent 索引 |
| Com | `com` | `source_body4_com_uses_slots_3_4`、中点、ring |
| Displacements | `displacements` | 已求 COM 减 source 的原点槽，12 个坐标 |
| Inactive | `inactive` | 已有两个 `zero_of_inactive`，显式传 body、joint、axis |
| Jv | `jv` | active_jv 的 4 个 active 分支，及 j=4/5 inactive 分支 |
| Jw | `jw` | active_jw 的 parent 轴，及 j=4/5 inactive 分支 |
| LinearGram | `linear_gram` | 全部 36 格，basis_dot、phi 单位圆、ring |
| AngularGram | `angular_gram` | 全部 36 格，含 (0,3)/(3,0)/(3,3) |
| Inertia | `inertia` | source 质量向量与对角惯量定义 |
| SourceGram | `source_gram` | sourceBodyMass→bodyMass→linkMass，Jv/Jw，9 项惯量和 |
| QuadraticReduction | `quadratic_reduction` | 两个带精确有理数系数的等式组合 |
| Scalar00 | `scalar00` | 两个平方恒等式、一个乘积恒等式，直接引用 body_4_piecewise |
| GramToPiecewise | `gram_to_piecewise` | 全 6×6 枚举，先二次量归约再展开 P/Q |
| ExpectedEntryHandoff | `expected_entry_handoff` | source_gram 与 gram_to_piecewise 的 trans |
| ExpandedHandoff | `expanded_handoff` | 定义展开到同一个 bodyMass，复用 expected entry |

十个辅助 theorem 是 `dot_zero_left`、`dot_zero_right`、`step3_translation`、
`frame_origin_prefix`、`frame_axis_prefix`、`frame_origin4`、
`source_origin_prefix`、`active_jv`、`active_jw`、`diagonal_angular_sum`。
这十项也全部为 **未编译 attempt／未验证**。因此全部 36 个声明中，本轮有
Lean 编译或 kernel 检查证据的数量为 **0**，没有可报告的成功 exit code。

`active_jv` 对 j=3 仍调用 active formula：其零值来自
`cross(vec(sin phi,0,cos phi), vec(e*sin phi,0,e*cos phi))` 的三个环恒等式。
只有 `3 < j.val` 才使用 inactive theorem。

`scalar00` 的三个线性组合系数是 `441/25000`、`361/100000`、
`399/25000`，分别乘 sin²(x)、sin²(phi)、sin(x)sin(phi) 的等式。
先显式改写 `2*phi = 2*q1+2*q2`，再做多项式整理。

## 3. API 核对与最小远端修复点

本地只读源码已找到所有使用的项目级定义和 bridge，没有发现必须添加新
几何公理或加强 target 假设的缺口。Mathlib 的三个三角引理名有现有源码用例；
这不能代替在所选 pinned checkout 中核对其实际类型与编译兼容性。

**本轮实际 Lean 诊断：无（未运行）。** 下面是静态识别的 elaboration 风险，
不是已观察到的编译报错，也不表示这些脚本一定失败。

| 检查点 | 精确局部目标／可能的最小修复 |
|---|---|
| 导入原 Target | 该 source comparator 目录没有独立 lakefile/lean-toolchain；先建立一致的模块搜索路径和依赖 olean。若原依赖先失败，单独报告原文件、行号、完整诊断，本轮范围不授权修改它。 |
| `prefix_columns` | 将 Fin 4 的 matrix product、Fin 3→Fin 4 的 embed3 和 Complex 常数 `.re` 化成实数多项式。若 norm_num 留下投影或 match，补精确的坐标 simp；若耗时，按 slot 分段并复用前槽结果。无需 slot4 的旋转公式。 |
| `frame_origin_prefix`／`source_axes` | proof-irrelevant 的 Fin 嵌入应可定义等同；若 rewrite 未命中，只补 `change`、`Fin.ext` 或 `[frameContract, prevOrigin]` 的 `simpa`，不改 sourceContract。 |
| `active_jv`／`active_jw` | 核对参数次序：Jv active API 是 origins, axes, body, joint, axis, guard；Jw 少 origins。若 Fin 包装令 rw 未匹配，固定局部 joint 并显式转换相等索引。 |
| `basis_dot`／`basis_cross` | `Fin.sum_univ_succ`、向量投影应在 linear_combination 前消去；若留下 Pi/Matrix 投影，增加局部 simp。叉积第三分量的单位圆乘子已经明确。 |
| `linear_gram`／`angular_gram` | 若 match 或常数乘法阻止 basis_dot 重写，先归约 i.val/j.val，再调用 basis_dot；Gv22 剩余式正好是 e² 倍的 phi 单位圆。 |
| `diagonal_angular_sum` | 9 项总和中的非对角条件全部可决定；若 `inertia.2` 不被 simp 接受，先命名 `have hI := inertia.2`，只在有限坐标上改写。 |
| `gram_to_piecewise` | 保持 h11/h12 改写早于 pp/qq 的展开；若简化器改变结合次序，显式 `change` 成 target 中的 P²+Q² 或 e*(P*cos+Q*sin) 后 rw，再 ring。 |
| 三角 leaf／`scalar00` | `linear_combination` 的乘子是已给出的多项式；若 API/normalizer 不兼容，可用 `calc` 展开成同一残差加这些单位圆/三角等式的倍数，再 rw/ring。不需要新的三角前提。 |

这些点的最小缺口是**尚未获得 elaboration 结果及 kernel 检查证据**。
不伪造 `unknown identifier`、unsolved goal 或 exit code；远端若出现错误，应附
首个错误所在文件/行列、完整原文、剩余 goal、已尝试的局部修复与结果。

## 4. 给 GitHub Lean agent 的执行交接（未发送／未执行）

在 GitHub 隔离工作区仅修复本 sidecar。先选择并记录可复建的单一 Lean / Mathlib
环境，不混用不同版本的旧 olean。原 `COMPILATION_STATUS.md` 记有一次未完成
尝试：Lean 4.33.1、Mathlib `0df444a360eaa60ab8c11dca51a86af692955474`；
这只是该文件的历史记录，不是本轮验证过的可用环境。

依赖从源码按实际 imports 拓扑构建：FourierNormalForm → FrameRecursion →
RealDHStep → FrameOriginAxis → FramePrefixIndex → FrameSlotAccessor；
BodySemanticCore → BodyContractCore；两支汇合到 SourceContractAdapter，
再到 SourceContractIndexAdapter／SourceBodyMassExtensionalProbe →
RouteBO1PerBodyExactSource；同时准备 BodyTraceEvaluator，再构建
RouteBO1PerBodyTraceAdapter → RouteBO1Body4SourceGramTargets → 本 sidecar。
以上每个模块来自仓库现有同名文件，不复制历史绝对 run 目录。

在远端既有 Lake 项目中、导入路径准备好后，单模块入口形状为：

```sh
lake env lean /remote/worktree/examples/routeb_o1_body4_source_gram_proof_attempt/RouteBO1Body4SourceGramProofAttempt.lean
```

这是带占位远端路径的交接命令，不是本地可直接运行的已配置构建方案。
按文件声明顺序定位首个失败，先修叶子再修下游。原依赖若阻断，保留原 target
和 adapter，报告最小外部依赖缺口；不要把上游未建立的声明当成可用证明。

回传 repo commit、源码哈希、Lean 精确版本、Mathlib SHA、实际命令、完整日志、
exit code、成功模块清单和输出 olean 的哈希（若生成）。文件末尾为 26 个 target
候选各留了 `#print axioms`；它们本轮没有执行。远端必须确认最终端点依赖中
没有 `sorryAx` 或新增公理，并检查依赖源码的占位情况；仅存在 theorem 名或
出现 `#print` 输出不足以说明整模块成功。远端后续结果应新增 successor review，
引用本 review/sidecar 哈希，不追改本轮未编译的历史状态。

## 5. 静态验证与源码绑定

起始 repo HEAD：`fa48149e77a3be9c8a9a2a57b913f64e20855999`。
sidecar SHA-256：`8D8477F64347B6875B0995D2094FB6F8E8ABA837BC25FFDEF53310EB98B1A322`。

| 已读取的输入文件 | SHA-256 |
|---|---|
| RouteBO1Body4SourceGramTargets.lean | `2D0D2794EDFE745D63A2970C36B53765F3B4BD747480107B1EAB51CF2E2C3CA9` |
| RouteBO1PerBodyTraceAdapter.lean | `6B50AE63C9770E3481F79511141C8CC55D592B5C550F686654C5E756584399EF` |
| RouteBO1PerBodyExactSource.lean | `C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553` |
| SourceContractIndexAdapter.lean | `2A18C7B6733AF6245F3E5BA6DEDD714A9EC7F28FD010122C0258611CE7AAC452` |
| SourceContractAdapter.lean | `58C0B15B6FCEB1064F773ACDB9F684DC55A021AC69A030C13E1C8B46F7B9A8DC` |
| FrameSlotAccessor.lean | `F497BD1F45FAE4DD385F4D0F46DF79252C92E5CD027B29D5DC55011F91525C31` |
| FrameOriginAxis.lean | `8F8D3333C9D4FF2E5A4A3CF25FA1C11BA6C6C719B10598F8B0E03162C524EF39` |
| RealDHStep.lean | `9C04DA5B9627EE749C53009733006934F95B2D33265E46CA59D0725AA453786A` |
| FourierNormalForm.lean | `56EC2F2D29A22942BCB83A3BA98197AE1CE4D607340072B81C013B8D358D3218` |
| BodySemanticCore.lean | `FE15F6CA9993F55FC56E6D2C9CCA5FA8C7F6E9530B9B900A6F111ED96715149C` |
| BodyContractCore.lean | `525E564BDBB57976F0C8A119A6E4BF9294D979DBFCC35CA705BF12A7AD95A4DB` |

这里只绑定列出的直接数学输入，不声称已审计整个传递导入闭包。
定稿前重新计算上述 11 个输入哈希，均与初始读取一致。

PowerShell 静态文本检查结果：26 个 target、26 个同类型直接候选、0 个缺失，
36 个 theorem 声明；sidecar 中禁止词 `sorry/admit/axiom/unsafe/native_decide/run_tac`
的独立 token 数为 0，行尾空白为 0。`#print axioms` 是检查命令，未引入公理。
此检查不解析 Lean，不证明目标，也没有运行数值/SymPy 回归。

工作期间观察到其他任务改动 `scripts/register_routeb_sidecar_frontier.py`，
并新增 body-5 geometry proof-attempt 与 O0 refinement 路径；本轮没有编辑、回退、
提交或注册这些变动。新增范围仅为本目录内上述两个文件。
最后一次状态检查还观察到 `artifacts/routeb_6dof/state.json` 及 O0 路径的并发
变动和 P5 sidecar；这些均不是本轮工具写入。因此本 review 只声明“本轮未修改
state”，不声明整个并发工作区的 state 文件字节始终不变。
