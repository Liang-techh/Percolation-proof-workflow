# Body-5 trace API repair：独立窄接口

日期：2026-09-08。状态：`OPEN_UNCOMPILED`。
`parsed=false; elaborated=false; kernel_checked=false; axioms_checked=false;
verified=false; registry_promoted=false; formal_certificate_allowed=false`。

新增 `NEW_BODY5_API_REPAIR_Independent20260908.lean`，14 个 theorem 候选。
没有运行本机 Lean/Lake、远程编译、数据判定或 comparator；不是编译 receipt。
“repair”表示供后续编译定位的替代证明体，不表示已观察到旧文件编译失败或本文件成功。

## 阅读与隔离

完整阅读用户指定的 Gram skeleton、Finite skeleton 与 G3/G4 review；补读 targets
定义、generated evaluator 的记录结构与 import，以及已有四份 20260907 API_REPAIR
文件。已有 repair 已覆盖大部分目标，本轮不覆盖或重命名它们，而补充一个独立入口。
新模块只直接导入 `RouteBO1Body5SourceTraceTargets`，不导入旧 skeleton 或 repair；
因而后续检查它不必先编译那两份 skeleton 的全部 proof bodies。
仍依赖 targets 的传递 imports，不表示这些依赖已经接受。

## 替代接口与风险

| 旧接口/风险点 | 新候选 | 保留的义务 |
|---|---|---|
| `(h.map f).sum_eq` 的 API 名称依赖 | `perm_map_sum` 对 Perm 的 nil/cons/swap/trans 归纳 | 值域必须 AddCommMonoid；swap 真正需要交换律 |
| 任意 seed 的 fold 与配对 flatMap | `seeded_sum`, `flat_pairs_sum` | 只需 AddMonoid；保留顺序、重复行以及 partner=x 时的两个位置 |
| Finset 求和与 Fin 固定坐标展开 | `coordinate_sum_congr`, `coordinates3`, `coordinates6` | Finset 仅用于坐标；不用 toFinset 丢掉源行重数 |
| decode 后 map_map/comp/id 的化简匹配 | `decode_map`, `decode_encode`, `row_perm` | 所有原始标签与完整频率函数保留，未规范化 Rat |
| q3 Bool filter 与 Perm.filter 参数顺序 | `q3_membership`, `filter_perm` | 构造子归纳与 Bool 分支；仍需检查 filter_cons 的本地归约行为 |
| q3 phase/product-to-sum 与源 fold | `phase3`, `q3_product`, `q3_fold_pairs` | 编码 Perm 显式输入；pair 尚未折成 trig 值 |

`coordinates3/6` 使用共同递推 API `Fin.sum_univ_succ` 与 `add_assoc`，不再依赖
专名 `Fin.sum_univ_three/six`。这只是收窄命名风险；Fin.succ 坐标归约是否被当前
simp 集完全处理仍未测试。`coordinate_sum_congr` 中 `∑ a ∈ s, f a` 是有限集合
求和记法，不是对源行另加一层去重。

`decode_encode` 先拆 BodyTraceRow，再拆两个 RationalTag，以 rfl 收尾；
`decode_map` 单独归纳列表，避免把函数复合的 eta 化简混入 source Perm。
函数型 RowCode 在此只被逻辑 transport 使用，没有执行其 DecidableEq。
若后续要执行数据 `decide`，可评估已有 TupleRowCode 路线，但须先取得它的
完整解码左逆；不能只比较六频率的哈希或归一化后的系数。

## 最小 import / tactic 风险

当前 `BodyTraceEvaluator.lean:1` 为 `import Mathlib`。因此新文件的一行直接 import
并非最小 Mathlib 闭包。本轮不改 evaluator、shared adapter、lake 配置或 toolchain。
可供后续单独拆分核对的候选模块为：

- 泛型 List 和：`Mathlib.Algebra.BigOperators.Group.List.Basic`。
- Fin 坐标：`Mathlib.Algebra.BigOperators.Fin`。
- source 接口：现有 `RouteBO1Body5SourceTraceTargets`，不能用纯代数 import 替代。
- tactic：本文件仅需要基础 induction/cases/rw/simp 与 `norm_num`、`ring`；若要收窄
  传递导入，可显式评估 `Mathlib.Tactic.NormNum` 与 `Mathlib.Tactic.Ring`。

这些是待核对的候选依赖，不是已测试的最小 import 集。未联网获取另一版本 API，
未运行本机命令来确认名称或 elaboration；避免把远端最新版当当前环境证据。

优先检查顺序：泛型 Perm/fold → Fin 坐标 → 记录左逆 → Bool filter → phase →
q3 条件 fold。构造子参数绑定、`List.flatMap_cons`、Bool `List.filter_cons` 的归约、
`h.map decode` 的参数 elaboration 和 rewrite 的目标匹配是具体 API 风险。
若 Bool 分支残留 if，可局部增加该版本对应的 if/Bool 归约 lemma；不要通过全局
classical 实例或修改原始 filter 来消除它。这里没有使用高 heartbeat 预算掩盖问题。

Gram skeleton 的 `change`/columns 函数 rewrite、`linear_combination`、`fin_cases`
仍是独立风险。本轮只给它的 Fin 求和层提供替代，不声称修复完整 G3/G4。

## q3 源绑定的准确终点

q3 是 zero-based `frequency 3`，不是第三个人类编号坐标。
`sourceQ3` 直接筛选冻结 `bodyTraceRows5`；`q3_membership` 同时保留源列表成员条件。
`q3_fold_pairs` 接收任意代表列表 rs 及其完整编码 Perm，推出任意 seed 的未合并
配对和；不提供该 Perm witness，不给 rs 的长度、非零分母或支持集作隐含保证。

原 review 的 8 代表/16 原行、六个有向 entry，以及 57 行 canonical binding
本轮没有重新判定。它们仍需各自的数据叶。`q3_product` 只处理两余弦与正弦乘积
恒等式；它不能证明 pair 列表恰好取这些频率或系数。
没有自动完成旧 classical-filter `Body5Q3ExactPairsTarget`、G1/G2、h_body_5 或覆盖。

## 静态检查与写入边界

仅用文本读取、git diff/status、SHA-256 与声明/禁用标记扫描。
新 Lean 文件计 14 个 theorem，扫描无 sorry/admit/axiom/native_decide/unsafe/
implemented_by；这不是依赖公理审计。旧 tracked 文件 diff 为空；本轮仅新增此
review 与上述一个 Lean 文件。范围外已有两个 BODY6 .olean 未触碰，不作本轮证据。

输入字节快照（不是编译证据）：

```text
NEW_BODY5_GramTraceSkeleton20260907.lean
118da0d3619e620c3f8c5f7869a20b325f363cd4434c3001867d2ef474bad626
NEW_BODY5_FiniteTraceSkeleton20260907.lean
16973c7960e15796b974dfeb15fb17ee07917126a93d0e5fe12cc7ceb5902f06
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md
bd935fa5c94642da017871364fe5e05dba3439270dfE83ddf4526784361e0173
```

两个 skeleton 写入前后散列相同；旧 review 的散列是在检查阶段读取。
检查时 HEAD：`97ce842068a036050fced394494403c2d133126d`。
未修改已有 NEW_BODY5、state、registry、shared adapter 或构建配置。
