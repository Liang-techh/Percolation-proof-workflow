# Body-5 API repair：编码 slice 到 seeded fold 的边界

状态：`OPEN_UNCOMPILED_API_CANDIDATES`。2026-09-08。
仅新增两个 `NEW_BODY5_API_REPAIR_*.lean`（4 + 3 个 theorem）及本 review。
未运行 Lean/Lake、远端编译、有限数据 decide、producer 或 comparator。
`parsed=false; elaborated=false; kernel_checked=false; axioms_checked=false; verified=false`。
这里的“替代接口”是供后续编译检查的候选，不是已经可编译的结论。

## 本轮增量

完整阅读指定的 Gram skeleton、Finite skeleton、G3/G4 finite-trace review，
并读取已有 ListFinset、RowCode、Independent、SliceCore、Q3FromFull、
CodedFilterCore、TupleQ3Join repair。基本 Perm/sum、decode 和配对归纳已有候选；
本轮不复制其数据表，也不改这些文件，而补齐可独立消费它们的边界接口。

| 新文件 / lemma | 最小作用与尚需提供的前提 |
|---|---|
| SliceBoundaryCore / `encoded_slice_fold` | `dec (enc r) = r`、编码/原行 Bool predicate 一致、完整编码 slice Perm → 原行 slice 的任意 seed fold |
| SliceBoundaryCore / `encoded_slice_blocks` | 上一接口接任意 `List.flatMap` block；特殊化 `[r, conjugate r]` 得到未合并配对和 |
| SliceBoundaryCore / `fold_zero_on` | 每行贡献为零 → 原 seed 不变，只需 AddMonoid |
| SliceBoundaryCore / `coordinate_bilinear_congr` | 双 Finset 和中的列逐坐标替换；`term` 实际可为任意二元函数，未假设线性 |
| Q3GuardBoundary / `q3_blocks_from_codes` | 特殊化冻结 bodyTraceRows5、frequency 3 非零与 body index 4；编码类型保持参数化 |
| Q3GuardBoundary / `contribution_off_entry` | row 或 col 不匹配时，仅由 if guard 消去贡献，不展开 atom |
| Q3GuardBoundary / `q3_off_support` | 显式提供每条 slice 行的有向 entry 排除条件，得到 seed 不变 |

文件全名分别为 `NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908.lean`、
`NEW_BODY5_API_REPAIR_Q3GuardBoundary20260908.lean`。

## 对四类原接口的替代接线

1. **List.Perm / sum。** 新接口复用 CodedFilterCore 的 `perm_sum`（Perm 构造归纳）
   和 `seeded_sum`。重排需 AddCommMonoid，顺序 fold 展开与零贡献消去只需 AddMonoid。
   任意 seed 保留，故不能把列表等式仅替成 seed=0 的数值等式。

2. **Finset / flatMap。** List 承载源行和重数；Finset 只承载坐标索引。
   不把源行转换为 Finset，也不要求 blocks 不交。`flatMap_sum` 将任意 block 的内部和
   接到外层 List 和；partner 恰等于自身时仍保留两个位置。
   G3 若整列 rewrite 不匹配，可从列函数相等用 `congrFun` 取得逐坐标等式，再走
   `coordinate_bilinear_congr`。本轮不提供实际 columns/isometry witness，
   也不把任意 `term` 接口说成已经完成带惯量系数的 G3 缩并。

3. **RowCode decode。** 新桥不选择新的数据格式，接收 `enc`、`dec` 和左逆律。
   原函数频率 RowCode 可用已有 constructor-cases/rfl 左逆候选；tuple-frequency
   RowCode 则仍需 `frequency_eta` 的 funext + 六坐标证明。它们是两种不同的编码类型，
   不能未经绑定便交替使用某份 coded Perm。左逆保留 body、row、col、六维频率和四个
   原 numerator/denominator 标签；不需要反向 `enc (dec code) = code`，也不引入
   BodyTraceRow 的全局 DecidableEq。不用规范化 ℚ 代替原始分数标签。

4. **q3 slice。** `q3_blocks_from_codes` 直接消费

   ```text
   Perm ((bodyTraceRows5.map enc).filter keepCode)
        ((reps.flatMap blocks).map enc)
   ```

   配合 decoder 左逆和 predicate 一致性，得到原始 slice 的 fold。此处特意不用
   whole-list binding 推测 slice binding。若从完整 Perm 取得 slice，应另外使用已有
   Q3FromFull 路线并证明常数排除、共轭保持 predicate；不能省略这些前提。
   对八个代表行取 `blocks r = [r, body5Conjugate r]` 后还需要共轭标量恒等式及八行
   值求和，才接回原 `q3Value`。当前新文件没有供给这些数据或标量 witness。

原 skeleton 的 q3-off-support 先计算 `q3Value` 再枚举 36 个 entry；新增的 guard 路线
只消费每条 slice 行的 row/col 排除。要由原 `¬q3Entry i j` 使用此接口，仍须证明冻结
slice 的有向支持包含于那六个 entry。frequency 3 非零本身不能推出该支持结论。
不把转置视为共轭，不把含 q3 的局部列等同于含 q3 的 Gram entry。

## 最小 import 与 tactic 风险

- 新 generic 文件只直接 import 已有 CodedFilterCore；其直接 Mathlib imports 为
  `Mathlib.Algebra.BigOperators.Group.List.Basic` 与
  `Mathlib.Algebra.BigOperators.Group.Finset.Basic`。不需要全量 Mathlib 或专用算术 tactic。
  但 CodedFilterCore 本身未在本轮编译，仍是传递阻塞点；“复用”不等于“已核验”。
- Q3 文件另 import `BodyTraceEvaluator`，不 import Gram/Finite skeleton、targets 或 shared
  adapter。evaluator 第 1 行是 `import Mathlib`，因此这里只缩小了项目依赖，不是最小
  Mathlib 闭包。禁止改 evaluator 的范围内不能进一步抽出轻量 record 模块。
- 本地只读参考 Mathlib 的 `Group/List/Basic.lean:250` 有
  `@[to_additive] lemma Perm.prod_eq ...`，它生成 `List.Perm.sum_eq`。
  因此不能把 grep 不到 `sum_eq` 声明当作真实 API 缺失；旧 skeleton 中该调用本身
  不构成已观察到的编译错误。新接口用构造归纳只是替代选择。
- 参考 checkout 是 `examples/anthropic_flt_reusable_lean/.lake/packages/mathlib`，
  HEAD `db584cd6d46c92f209a44c0f1c829460d327499d`；该示例 toolchain 文件为
  `leanprover/lean4:v4.33.1`。这是读取文件/git 得到的参考，不证明 body-5 的实际 pin、
  import resolution 或 .olean 可用。没有运行版本命令或启动 Lean。
- 新证明体只用基础 tactic、`simp`/`simp only`、`rw` 与构造式证明；不使用
  `fin_cases`、`norm_num`、`ring`、`linear_combination`、`omega` 或闭合 theorem `decide`。
  `keepQ3` 定义仍使用整数不等式的 `decide`，不是本轮执行有限源表判定的记录。
- filter 消去仍依赖 Bool 分支化简；保留 CodedFilterCore 中 `cases` 后的普通 `simp`。
  不把它机械缩成只含 `List.filter_cons` 的 `simp only`，否则可能留下 Bool/if redex。
  新零 fold 归纳显式 `revert hz`，固定 ih 的 seed/support 参数顺序。
- `q3Rows` 放在 noncomputable section；不为导入的 generated list 承诺可执行代码生成。
  编码 predicate 的可计算性、逻辑定义的 kernel reduction、整个 source module 的代码生成
  是不同问题。后续决定是否运行 `decide` 时需针对精确环境另检。

后续获准编译时，顺序应为 CodedFilterCore → 新 SliceBoundaryCore → 新 Q3GuardBoundary，
然后独立检查具体 RowCode 左逆与 coded slice 数据叶；最后才接共轭/八行求值和原 targets。
这只是定位建议，本轮没有执行任何阶段。

## 文本检查与写入边界

新文件共 7 个 theorem；文本扫描没有发现 sorry/admit、axiom 声明、native_decide、
unsafe、implemented_by。此检查不是 parser、elaborator、kernel 或 import/axiom 审计。
没有数值或符号回归，也没有重新检查原 review 所述 57/16 行数据结果。

写入前后 11 个既有 NEW_BODY5 Lean 文件的 SHA-256 全部相同，指定旧 review 与
BodyTraceEvaluator 的 hash 也相同。未写 state、registry、shared adapter、构建配置或 receipt。
工作区原有其他 body-6 .olean / cone 文件未触碰；不将其视为本轮编译证据。

字节快照（不代表证明）：

```text
NEW_BODY5_API_REPAIR_SliceBoundaryCore20260908.lean
c3e3c04a5a461d711190063a167dc593620853c26dd7894b83ce3cefff468dca
NEW_BODY5_API_REPAIR_Q3GuardBoundary20260908.lean
a3bd86fb97bda1c8bd8882f478e584eb2f76b15b55cc58d5c3ed05c8e0ec7a46
NEW_BODY5_API_REPAIR_CodedFilterCore20260908.lean
5d51b0450dc09b358ee483c7e23c4cdf1628f3a6cc21b0bc0d717667aeb9c140
NEW_BODY5_GramTraceSkeleton20260907.lean
118da0d3619e620c3f8c5f7869a20b325f363cd4434c3001867d2ef474bad626
NEW_BODY5_FiniteTraceSkeleton20260907.lean
16973c7960e15796b974dfeb15fb17ee07917126a93d0e5fe12cc7ceb5902f06
REVIEW_BODY5_G3_G4_FINITE_TRACE_20260907.md
bd935fa5c94642da017871364fe5e05dba3439270dfe83ddf4526784361e0173
BodyTraceEvaluator.lean
b9845d37b5dcd16e1f9e142cb2e4d0e5571452993e843c85ac8cd643f6ba5dea
```

所有 G/F/source/PDE admission 状态不由本 review 改变；无 registry promotion，
无 comparator acceptance，也无正式证书可用性声明。
