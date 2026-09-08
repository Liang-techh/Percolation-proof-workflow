# Body-5 API repair：tuple code 上的 q3 筛选与解码接线

状态：`OPEN_UNCOMPILED`。日期：2026-09-08。
`lean_run=false; lake_run=false; parsed=false; elaborated=false;
kernel_checked=false; axioms_checked=false; verified=false;
registry_promoted=false; formal_certificate_allowed=false`。

本轮只新增两个 `NEW_BODY5_API_REPAIR_*.lean` 与本 review，未改接原 skeleton。
“repair”是供后续编译定位的替代证明体，不是编译成功声明。
没有运行本机或远程 Lean/Lake、数据 decision、comparator 或整仓回归。

## 阅读与增量

完整阅读指定的 GramTraceSkeleton、FiniteTraceSkeleton 和
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md；补读 targets、记录结构及已有 repair。
既有 SliceCore/Q3FromFull 已有“完整行 Perm → 行 filter → 配对 fold”。
本轮新增“编码表 filter → decode → 实际行 filter”的精确交换接口，
将有限判定面放在纯 Fin/Int tuple 上，不重复提交 57 行或 8 代表 literal 表。

- `NEW_BODY5_API_REPAIR_CodedFilterCore20260908.lean`：7 个泛型 lemma。
- `NEW_BODY5_API_REPAIR_TupleQ3Join20260908.lean`：8 个具体接口 lemma。

两份文件均不导入旧 skeleton 或旧 API repair。第一份无项目依赖；第二份导入
targets 与本轮 core。这仅隔离旧尝试的 proof bodies，不移除 targets 的传递依赖。

## 四类替代入口

| skeleton 风险面 | 本轮候选 | 精确保留的条件 |
|---|---|---|
| `(h.map f).sum_eq` | `perm_sum` | 对 Perm 的四个构造归纳；AddCommMonoid，不丢行重数 |
| fold 与 flatMap | `seeded_sum`、`flatMap_sum` | 任意 seed；AddMonoid 足够；任意空块/重复块，不要求不交 |
| G3 双重 Finset 和 | `coordinate_sum_congr` | 两次 sum_congr，输入逐坐标等式；不替代 columns/isometry |
| RowCode decode | `decode_map`、`decode_filtered_map`、`rows_perm_of_filtered_codes` | 编码左逆 + predicate 兼容；不要求源行 DecidableEq |
| q3 slice | `decode_source_slice`、`slice_codes_from_full`、`q3_rows_perm` | 原始列表到编码 slice 的 Perm 仍是显式输入 |
| q3 求值 | `q3_seeded_pairs`、`q3_seeded_value` | 先未合并两 atom 和；最终值另以 hValue 输入 |

核心新等式是：

```text
decode(map encode source |> filter keepCodeQ3)
    = filter keepRowQ3 source.
```

它由列表归纳、`decode (encode r) = r` 和
`keepCodeQ3 (encode r) = keepRowQ3 r` 推出；不是通过相等散列或规范化系数推断。
Bool 两分支用普通 simp 归约 if，避免只展开 filter_cons 后残留条件表达式。

`RowCode` 保留 body、row、col、完整六个 Int 频率、real/imag 四个原始分子分母。
新类型虽也名为 RowCode，但在新 namespace，频率部分是六元组，不是旧频率函数类型。
不能把旧函数型 coded Perm 直接当本轮 hCodes；需重新构造 tuple coded Perm，
或先由旧左逆恢复整行 Perm，再 map 新 encode。
不把 1/2 与 2/4 合并，不识别转置，不独立翻转频率各分量。

`decode_encode` 拆解 BodyTraceRow 和两个 RationalTag；唯一函数相等步骤是
`frequency_eta`，用 funext 后枚举 Fin 6。不存在 source-row 全局 equality instance。
code 的 Bool predicate 只读频率第 3 坐标，即 zero-based q3 / CSV nu4。

## q3 数据与数学义务没有消失

有两种调用路径：

1. 直接提供原始编码表按 keepCodeQ3 筛选后，与 paired reps 编码表的完整 Perm。
2. 提供完整原始编码表到 canonical 编码表的 Perm，并提供 canonical 编码 filter
   等于目标 slice 的等式；`slice_codes_from_full` 用 Perm.filter 推导上述小型义务。

两者都保留重数。只有提供具体 reps 的数据绑定后，才能接到既有 8 代表/16 原行结论。
本轮不执行这两类有限判定，不把任意 reps 隐式当作旧 repsQ3。

`q3_seeded_pairs` 的终点是实际 bodyTraceRows5 slice 的任意 seed fold，等于
seed 加每个代表与其整个频率取负的 partner 的贡献和。
它不推断共轭恒等式、非零分母、8 行值、支持集或任何几何列 witness。
`q3_seeded_value` 要求独立 hValue；旧 review 的六个有向位置应分别供应：

- (0,4)、(4,0)：`[cos(phi-q3)-cos(phi+q3)]/60`。
- (1,4)、(4,1)、(2,4)、(4,2)：`cos(q3)/30`。
- 其余位置：0；代入该 hValue 后才可用 add_zero 得到保持 seed。

这里复述的是原目标公式，不是本轮重新验证的具体行求值结果。
旧 classical-filter `Body5Q3ExactPairsTarget` 没有被替代成已证结论。
源 G1/G2、G3/G4 标量叶、最终 h_body_5 与源到生成器的权威绑定仍各自开放。

## import / tactic 最小风险面

仅查阅本地源文本，没有调用 Lean/Lake，且没有修改依赖或获取其他 checkout。

参考源码的版本不是目标环境验证：

- Lean 源目录：`C:/Users/z5242/.elan/toolchains/leanprover--lean4---v4.33.1/src/lean`。
  `Init/Data/List/Perm.lean:213` 的 map 参数顺序是函数在前、Perm 在后；
  `:233` 的 filter 同样 predicate 在前、Perm 在后。故新代码使用全限定调用。
  `Init/Data/List/Lemmas.lean:1267` 的 filter_cons 右侧确实含 Bool 条件 if。
- 本地 Mathlib 参考 checkout：
  `examples/anthropic_flt_reusable_lean/.lake/packages/mathlib`，
  HEAD `db584cd6d46c92f209a44c0f1c829460d327499d`。
  `Mathlib/Algebra/BigOperators/Group/List/Basic.lean:250` 有带 to_additive 的
  `Perm.prod_eq`，提供 sum_eq 的源码生成依据；不能因此把原 sum_eq 判成不存在。
  `Group/Finset/Basic.lean:104` 有带 to_additive 的 prod_congr，对应 sum_congr。
- 所读相邻 routeb_b45_source_mass_fourier_bridge_lean manifest 的 Mathlib pin 是
  `0df444a360eaa60ab8c11dca51a86af692955474`，与上述参考 checkout 不同。
  本轮没有确定 body-5 实际 import resolver、闭包或 pin，也没有将相邻 manifest
  冒充 body-5 构建凭据。

最小可隔离候选集合，而非已实测最小 imports：

| 层 | 本轮直接 import / tactic | 剩余风险 |
|---|---|---|
| List/fold/filter | Group.List.Basic；基础 induction/cases/rw/simp | Perm 构造分支、flatMap_cons、map_append、sum_append 的目标 pin API |
| 坐标和 | Group.Finset.Basic；两次 sum_congr | 不贸然仅用 Defs：本地参考的对应 congr 声明在 Basic |
| tuple 左逆 | targets + 显式 Mathlib.Tactic.FinCases；funext、fin_cases、rfl | Fin 6/vector notation 的归约、tuple pattern 与记录 eta |
| body-5 fold | targets + 本轮 core；rw/simp | traceRowContribution 的参数顺序与 body5Fold 展开匹配 |

core 不再导入 BigOperators.Fin：它只需要给定 Finset 的和，不做固定 Fin 坐标展开。
第二份仍经 BodyTraceEvaluator.lean:1 传递导入 Mathlib；不能把少量直接 imports
表述为项目闭包已最小化。FinCases 显式列出是声明 tactic 需求，当前宽闭包下可能冗余。

本轮不使用 norm_num、ring、linear_combination、omega 或大型闭合 decide proof。
predicate 定义中的 decide 只是整数非零 Bool 定义，并非已执行的数据证据。
原 Gram 中 fin_cases/norm_num/ring/linear_combination 仍需各自 tactic import；
phi 角参数 rewrite、两次 isometry rewrite 和三角残差符号仍是独立检查点。
不要为消除 API 错误改 shared adapter 或向 source filter 增加 classical 决策。

后续最小检查顺序：core → frequency_eta/decode_encode → decode_source_slice →
条件式 q3 fold → 最后才单独接具体数据 Perm 与 hValue。
该顺序只是 review 建议，本轮没有执行。

## 静态检查与字节快照

仅做文件阅读、API 源文本检索、Git diff/status、声明/禁用标记扫描与 SHA-256。
15 个 theorem proof body，新增 Lean 文本未见 sorry/admit/axiom/native_decide/
unsafe/implemented_by 或尾随空白；这不构成 syntax/type/kernel 或传递公理审计。
写入前后原两 skeleton 散列一致，目标目录 tracked diff 为空。原有两个 BODY6 .olean 未触碰，
不作为本轮运行产物或证据。没有修改 state、registry、shared adapter、generated rows、
已有 NEW_BODY5 文件、已有 review 或构建配置。

最终 status 出现范围外并发变更，包括 state.json、integrate_agent_reviews.py 与
其他 review/script；本轮没有写入、回滚或把它们归为本轮产物。

```text
NEW_BODY5_GramTraceSkeleton20260907.lean
118da0d3619e620c3f8c5f7869a20b325f363cd4434c3001867d2ef474bad626
NEW_BODY5_FiniteTraceSkeleton20260907.lean
16973c7960e15796b974dfeb15fb17ee07917126a93d0e5fe12cc7ceb5902f06
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md
bd935fa5c94642da017871364fe5e05dba3439270dfe83ddf4526784361e0173
NEW_BODY5_API_REPAIR_CodedFilterCore20260908.lean
5d51b0450dc09b358ee483c7e23c4cdf1628f3a6cc21b0bc0d717667aeb9c140
NEW_BODY5_API_REPAIR_TupleQ3Join20260908.lean
2d8541489d7cd5e3090c12d338e8308c5c28a20cdf8edf41b1037634f70ce0f5
```

没有编译 receipt，没有 registry promotion，也没有“可编译已确认”的结论。
