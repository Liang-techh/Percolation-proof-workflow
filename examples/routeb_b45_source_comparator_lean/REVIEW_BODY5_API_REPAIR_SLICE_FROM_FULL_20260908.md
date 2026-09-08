# Body-5 API repair：由完整 Perm 推导 q3 slice

状态：OPEN_UNCOMPILED。本轮未运行本机或远程 Lean/Lake；未解析、elaborate、
kernel check 或检查 axioms。下面是带具体证明体的接口候选，不是可编译性结论。

## 阅读与写入范围

完整阅读用户指定的 GramTraceSkeleton、FiniteTraceSkeleton 和
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md，并阅读现有 ListFinset、RowCode、
Q3Slice、Q3DataLeaf、Independent API repair。既有修复已经覆盖基础接口，
本次新增的是从完整源行 Perm 推导切片的组合入口，不重复提交整套 57 行 literal 表。

只新增本 review 与两个 NEW_BODY5_API_REPAIR_*.lean：

- SliceCore20260908：9 个泛型 lemma，无 project/旧 NEW_BODY5 import。
- Q3FromFull20260908：4 个 body-5 lemma，仅导入 targets 与本轮 SliceCore。

未修改任何已有 NEW_BODY5 文件、state、registry、shared adapter、generated rows
或构建配置。已有范围外工作区变化不归属本轮，也没有回滚。

## 替换点与最小契约

| 原入口 | 新入口 | 前提与边界 |
|---|---|---|
| `(h.map f).sum_eq` | `sum_under_perm` | AddCommMonoid；直接对 Perm 构造归纳，重数不丢失 |
| seed fold 与 flatMap 配对 | `seeded_fold`、`pair_sum` | AddMonoid 足够；只有 Perm 重排才要求交换性 |
| 惯量/dot 的双重 Finset 和 | `double_sum_congr` | 每个坐标的相等证据；不自动提供列函数或 isometry witness |
| map/map/comp/id 解码化简 | `decode_mapped`、`decode_perm` | 显式左逆，不要求源行 DecidableEq |
| q3 再做 16 行 decision | `slice_from_full`、`q3_binding_from_full` | 完整源 Perm + 常数筛选为空 + partner 保持 predicate |
| q3 任意 seed fold | `q3_fold_from_full` | 返回未合并的两 atom 和；不偷用共轭恒等式、8 行值或 support |

完整编码继续保留 body/row/col、六坐标频率函数、四个原始分子分母标签。
`decode_encode` 拆解 BodyTraceRow 与两个 RationalTag 后用 rfl；
不规范化 Rat，不靠仅频率、仅系数和或 partner existence 恢复行。

新切片接线为：完整 coded Perm → decode Perm → filter Perm →
常数块消去 → filter 与成对 flatMap 交换 → seeded fold。
`keep_conjugate` 只用整向量取负后第 3 坐标非零等价；q3 指 zero-based q 3。
List.flatMap 保留两个位置，即便 partner x = x，也没有集合去重。

还需调用侧提供：

1. 原始 bodyTraceRows5 到 constants ++ paired reps 的完整 coded Perm；本文件没有证明该封闭叶。
2. constants.filter keepQ3 = []。在选定 literal constants 上这是小型数据义务，未在本轮运行。
3. 如需接旧 repsQ3 或旧 q3Value，另证 reps.filter keepQ3 与目标 8 行表的绑定，
   再接共轭合并和六个有向 entry 的值。新 theorem 不直接声称恢复具体 16 行或六位置覆盖。

## import 与 tactic 风险（静态判断，不是已观察到的编译错误）

- SliceCore 显式 import Group.List.Basic 与 BigOperators.Fin；没有 Mathlib 总入口。
  这是保守小集合，不是已验证最小闭包。Fin 入口可进一步尝试缩为 Finset big-operator
  Defs，但本轮不执行裁剪验证。所读本地参考 Mathlib 的 Group.List.Basic 确实公开
  import List.Perm.Basic；参考 checkout toolchain 是 v4.33.1，不能据此宣称目标 pin 兼容。
- Q3FromFull 经 targets/BodyTraceEvaluator 仍传递导入 Mathlib。新增 lemma 的接口虽小，
  不代表整条 project import closure 小或已通过检查。
- 不再依赖 Perm.sum_eq、Perm.filter 的名称/参数顺序；仍需目标 Lean 的 Perm
  构造归纳分支和 Perm.map API。List.flatMap_cons、filter_append、filter_cons、
  map_append、sum_append 仍是应首先检查的接口。
- 新 filter_under_perm 在 Bool 分支用普通 simp，使 if/Bool coercion 归约进入目标。
  旧 Independent 的 simp only 列表可能留下条件表达式；这是风险定位，未声称旧文件失败。
- decode 不用函数枚举，只要左逆即可传输给定的 Perm。RowCode 内含函数，若以后
  对编码直接 decide，不能假定总能取得可计算函数 DecidableEq；优先改用既有
  六 Int tuple 编码及其 frequency_eta 证明，仍须目标侧检查，不引入 classical 决策。
- 本轮无 fin_cases、norm_num、ring、linear_combination、native_decide 或大型闭合 decide。
  新模块不额外依赖这些 tactic；旧 Gram 标量叶仍需要原 tactic imports 与角参数正规化。
- 普通 simp 的全局 simp-set 仍有 pin 风险；后续编译若失败，应局部收紧化简集合，
  不改源定义、不展开 DH prefix，也不增加信任公理。

## 非编译检查与快照

只进行了文本阅读、声明/import/占位符扫描、Git diff 和 SHA-256。
新增 Lean 合计 13 个 theorem；扫描未见 sorry/admit/axiom/native_decide/unsafe。
目标目录 tracked diff 为空；新增文件没有改接原 skeleton。
这些检查不是 syntax、type、kernel 或依赖证明。

```text
NEW_BODY5_API_REPAIR_SliceCore20260908.lean
32232d3abaec56aa5fe5804c05ac8acf5234404e64fb74376d37264e6437338d
NEW_BODY5_API_REPAIR_Q3FromFull20260908.lean
36c2a7c3ce4852441605c972f3f71b86c6d03833ee2a8c1ac6e41bb87e41b9da
```

G1/G2 columns、isometry、完整数据叶、旧 classical-filter targets、最终 h_body_5
均未因此成为已接受 witness；没有 receipt 或 registry promotion。
