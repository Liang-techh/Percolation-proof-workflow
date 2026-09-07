# Body-5 trace skeleton：小范围 Lean API repair

日期：2026-09-07。状态：`OPEN_UNCOMPILED_API_REPAIR`。

本轮新增四份 `NEW_BODY5_API_REPAIR_*.lean`，共 29 个 theorem 候选，以及本 review。
只做源码阅读、接口对照、文本检查和整数标签诊断；没有运行本机或远程 Lean/Lake，
没有解析、elaboration、kernel check、公理审计或 comparator 结果。
“repair”表示供后续编译检查的替代接口，不表示已定位到实际编译错误或已编译通过。

完整阅读了 `NEW_BODY5_GramTraceSkeleton20260907.lean`、
`NEW_BODY5_FiniteTraceSkeleton20260907.lean` 和
`REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md`，另读相关 targets、行结构和 evaluator 定义。
两个旧 skeleton 与旧 review 均未修改，也没有导入两个旧 skeleton。

## 交付与替换位置

所有文件位于本 review 同目录。以下名称均指新 namespace 内的声明，未覆盖旧声明。

| 新文件 | 替代入口 | 对应旧入口及边界 |
|---|---|---|
| `NEW_BODY5_API_REPAIR_ListFinset20260907.lean` | `map_decode_encode`、`perm_of_encoded`、`map_sum_perm`、`fold_add_sum`、`fold_add_perm` | map 解码显式归纳；Perm 到加法和用构造子归纳；任意 seed 保留 |
| 同上 | `pair_map_sum`、`fold_pairs` | 替换 `pair_sum_attempt` 周围依赖全局 simp 的 flatMap 接线；每次只展开一个 cons |
| 同上 | `sum_congr_on`、`fin3_sum`、`fin6_sum` | coordinate Finset 的逐点替换，以及三/六项有限和的固定左结合展开 |
| `NEW_BODY5_API_REPAIR_RowCode20260907.lean` | `decode_rowCode`、`perm_of_rowCodes` | 原函数型 RowCode 的同字段替代；不依赖 `map_map` 后 lambda/id 被 simp 自动识别 |
| 同上 | `frequency_eta`、`decode_tupleRowCode`、`perm_of_tupleRowCodes`、`tuple_codes_to_row_codes` | 六坐标整数元组编码；保留完整行解码和回到原函数型编码 Perm 的出口 |
| `NEW_BODY5_API_REPAIR_Q3Slice20260907.lean` | `q3_filter_perm`、`q3_conjugate_keep`、`source_q3_frequency` | 显式 Bool predicate；筛选原始 bodyTraceRows5，验证整向量取负保持 q3 非零判据 |
| 同上 | `phase_frequency`、`contribution_pair`、`q3_pairs_value`、`q3_value_off_support` | phase 先规范化；共轭 atom 身份为显式前提；八代表求值；off-support 只拆 guard |
| 同上 | `q3_source_fold_pairs`、`q3_source_fold_conditional`、`q3_source_off_support_conditional` | 原始切片的 coded Perm 是显式参数；先给未合并 pair sum，再接 q3Value 与任意 seed |
| `NEW_BODY5_API_REPAIR_Q3DataLeaf20260907.lean` | `q3_source_tuple_codes`、`q3_counts`、`q3_source_binding` | 单独存放未执行的 16 行 `decide` 候选及解码接线，不把 counts 当作 Perm |

示例接线：原 `fold_perm_attempt` 的目标展开 `body5Fold` 后可使用
`fold_add_perm (traceRowContribution body5Index i j q) h seed`。
原 `pairedRows` 展开一次后可使用 `pair_map_sum body5Conjugate f rs`。
旧 F1 的 Perm 分量可交给上述通用接口；F1 的其他分量不会因此成立。

Gram 层的 dot 交换可使用 `sum_congr_on Finset.univ`，逐坐标提供 `mul_comm`。
columns 的函数等式若 rewrite 匹配不稳定，先用 `congrFun` 取出对应坐标等式，再对有限和
使用该接口。`fin3_sum` 固定给出三项左结合加法，`fin6_sum` 固定给出六项左结合加法；
这可避免反复 `Fin.sum_univ_succ` 后把 `Fin.succ`、零项和结合方向全部交给大规模 simp。
本轮没有重写 G3/G4 标量证明，也没有提供几何 columns 或 isometry 的 witness。

## API 源码依据与实际风险

本目录 `COMPILATION_STATUS.md` 记录的历史 pin 为 Lean commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`、Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`。本轮按这些 commit 阅读上游源码；
没有核实当前构建器、olean 或完整依赖闭包与这些历史 pin 一致。
本机 v4.33.1 目录的 List 源码也仅作为文本阅读，未执行其中工具。

- `List.Perm.map` 的显式调用顺序为函数、Perm 证据；`List.Perm.filter` 同样先接
  Bool predicate。旧 `h.map f` 不是本轮发现的错误；新文件只是写出完整调用并固定中间类型。
  [Lean List.Perm 源码](https://raw.githubusercontent.com/leanprover/lean4/819816b2e0a3bf405af45ae5c7af2491d8f5bee6/src/Init/Data/List/Perm.lean)。
- Mathlib 的 `Perm.sum_eq` 来自 `Perm.prod_eq` 的 additive 生成，因此只搜索字面
  `theorem ...sum_eq` 可能漏掉它。旧 `(h.map f).sum_eq` 有源码依据；本轮的构造子归纳
  去掉了对该生成名字的直接依赖，仍要求 `AddCommMonoid`。
  [List big operators 源码](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Algebra/BigOperators/Group/List/Basic.lean)。
- 配对是 `List.flatMap`，不是 `Finset.flatMap`。`pair_map_sum` 只要求 `AddMonoid`，
  不交换次序；即使 partner 与原行相等，也仍保留两个位置。不可用 `toFinset` 去重代替
  完整行 Perm，不能把只有有限坐标指标的 Finset 与源行多重集混为一谈。
- `fin3_sum` / `fin6_sum` 对应 `Fin.sum_univ_three` / `Fin.sum_univ_six`；同样由
  multiplicative 声明生成。它们的结果是左结合，接到其他正规形时可能仍需 `add_assoc`。
  [Fin big operators 源码](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Algebra/BigOperators/Fin.lean)。
- `decode_rowCode` 先拆行结构及两个 RationalTag，再 `rfl`。通用 map 解码定理逐项归纳，
  不依赖高阶 simp 将解码复合函数识别为 `id`。TupleRowCode 的左逆额外使用六坐标
  `frequency_eta`；这里仍有 `fin_cases` 与向量记号的 elaboration 风险，未经运行。

TupleRowCode 保留 body、row、col、全部六个频率整数、real/imag 的四个原始分子分母。
它没有把频率缩成三维，也没有把 `1/2` 与 `2/4` 认作相同行标签。
该编码让闭合 Perm 的相等判定只涉及 Fin、Int 与乘积；不需要函数型 RowCode 的
可计算函数相等实例，也不新增 BodyTraceRow 的全局实例。原函数型 RowCode 并未被判为不可计算；
元组方案是降低实例依赖的替代入口。

## import 与 tactic 的最小风险面

这里给出的是按源码选择的直接 import 集，不是通过编译删减得到的严格最小依赖证明。

| 层 | 当前直接 import / tactic | 剩余风险 |
|---|---|---|
| ListFinset | `Mathlib.Algebra.BigOperators.Group.List.Basic`、`Mathlib.Algebra.BigOperators.Fin`；`induction`、`rw`、`simp only` | 已绕开项目 adapter；仍需匹配的 Mathlib 环境、additive 声明和基础 tactic 可见性 |
| RowCode | `BodyTraceEvaluator` + ListFinset；另用 `funext`、`fin_cases` | evaluator 自身 `import Mathlib`，因此当前实际依赖仍宽；未修改它来缩 import |
| Q3Slice | `RouteBO1Body5SourceTraceTargets` + RowCode；另用 `norm_num`、`ring` | targets 传递导入 shared adapter、exact source 和未完成编译的 source probe；未移除这个现有依赖风险 |
| Q3DataLeaf | Q3Slice；两处普通 `decide` | 分离了闭合决定计算，但它仍依赖 Q3Slice 全模块，包括标量求值叶；不是无 scalar 依赖的独立工程 |

如果以后在允许调整依赖的环境抽取更小模块，额外 tactic 的明确候选 import 是
[`Mathlib.Tactic.FinCases`](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Tactic/FinCases.lean)、
[`Mathlib.Tactic.NormNum`](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Tactic/NormNum.lean) 和
[`Mathlib.Tactic.Ring`](https://raw.githubusercontent.com/leanprover-community/mathlib4/0df444a360eaa60ab8c11dca51a86af692955474/Mathlib/Tactic/Ring.lean)。
本轮不改任何旧 import。新代码未使用 `linear_combination`、`omega`、`simp_all`、
`native_decide`，也未提升文件全局 heartbeat。两个 DataLeaf 的资源选项仅局部作用于
对应声明；4096 / 800000 是未测量的候选预算，不是成功编译数据。

q3 标量风险集中在 `q3_pairs_value` 的 36 个 entry 分支：RationalTag 先转 Rat 再转 Real，
guard、负频率角度和 `body5Phi` 的加法正规形必须一致。`phase_frequency` 先给出统一角度，
后续 `ring` 只做代数归一化。不能让 `ring` 代替角度不同的三角恒等式证明。
`q3_value_off_support` 用两个否定 guard 直接化简，无须重复 36-case 枚举。

## q3 的源绑定和证明边界

八个代表与旧 skeleton 的 `repsQ3` literal 行相同；伴随行对六个频率坐标整体取负。
直接源切片使用 `frequency 3 ≠ 0`，对应 zero-based q3、CSV 的第四频率坐标。

| 有向 entry | 正代表系数及频率 | 合并值 |
|---|---|---|
| (0,4)、(4,0) | +(1/120) at (1,1,-1)，-(1/120) at (1,1,1) | [cos(phi-q3)-cos(phi+q3)]/60 |
| (1,4)、(4,1)、(2,4)、(4,2) | +(1/60) at (0,0,1) | cos(q3)/30 |

`q3_source_fold_pairs` 只接收 coded Perm，返回未合并的实际 contribution 对之和；
`q3_source_fold_conditional` 额外接收 `Body5ConjugateAtomTarget`，才返回 q3Value。
这是可审查的条件式 API，没有借用旧 skeleton 的 `conjugate_atom_attempt` 作为已证事实。
`q3_source_off_support_conditional` 同样明确保留这两个前提与原 seed。

这些声明不提供完整 57 行 canonical Perm、旧 classical representative/filter bindings、
`Body5Q3ExactPairsTarget`、最终 h_body_5 或 G1/G2。q3 的六个有向 entry 没有通过对称性合并。
slice 支持不等于完整 body-5 matrix 支持；它也不证明 q3Value 在每个输入角度均非零。

## 本轮静态检查与未发生的检查

用内存中的 PowerShell 文本解析读取实际 generated body-5 行及新八代表，逐行比较
body/row/col + 六个频率整数 + 四个原始有理数标签组成的 13 字段排序多重集：
源 q3 切片 16 行，新配对 16 行，完全相同；代表 literal 与旧 skeleton 的八行相同；
有向 entry 恰为 (0,4)、(1,4)、(2,4)、(4,0)、(4,1)、(4,2)。
排序列表没有去重，因此这项文本诊断保留重数；它不是 Lean Perm 的证明。

第一次诊断把 PowerShell 的 `-join` 与 `-cne` 写在同一表达式中，触发了错误的比较并停止。
改成先分别保存两个排序后的字符串再比较后诊断通过；没有修改 Lean literal 来迎合诊断。
没有新增诊断脚本、JSON、构建配置、receipt 或状态文件。

新 Lean 文本扫描未见 sorry/admit/axiom 声明、native_decide/unsafe/implemented_by 或尾随空白。
这不是 parser、tactic 执行、传递依赖公理审计或语义验证。`parsed=false`、`elaborated=false`、
`kernel_checked=false`、`axioms_checked=false`、`verified=false`。

## 写入边界与快照

所有写入通过 apply_patch，只涉及四个新 `NEW_BODY5_API_REPAIR_*.lean` 和本 review。
未修改已有 NEW_BODY5 文件、旧 review、state、registry、shared adapter、generated evaluator。
检查期间出现其他目录的并发新增文件；末次检查还观察到
`artifacts/routeb_6dof/state.json` 有范围外修改。本轮未写入该文件，
未把这些并发变化归为本轮输出，也未编辑、删除或回滚它们。

以下六个输入的 SHA-256 在写入前读取、写入后复核相同；只表示字节一致：

```text
NEW_BODY5_GramTraceSkeleton20260907.lean
118da0d3619e620c3f8c5f7869a20b325f363cd4434c3001867d2ef474bad626
NEW_BODY5_FiniteTraceSkeleton20260907.lean
16973c7960e15796b974dfeb15fb17ee07917126a93d0e5fe12cc7ceb5902f06
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md
bd935fa5c94642da017871364fe5e05dba3439270dfe83ddf4526784361e0173
RouteBO1Body5SourceTraceTargets.lean
aa314706ef2a42dca2e73b8b5ded22dc2f598e395e775e860f993da34739d9a9
RouteBO1PerBodyTraceAdapter.lean
6b50ae63c9770e3481f79511141c8cc55d592b5c550f686654c5e756584399ef
BodyTraceEvaluator.lean
b9845d37b5dcd16e1f9e142cb2e4d0e5571452993e843c85ac8cd643f6ba5dea
```

将来获准检查时，建议按 ListFinset → RowCode → Q3Slice → Q3DataLeaf 顺序定位失败。
本轮没有执行这个流程，也没有作出编译、comparator 接受或 registry promotion 的声明。
