---
kind: review_result
review_id: review-GH-MIXED-BODY6-PATH-REASSIGNED-20260908T105201
task_id: GH-MIXED-BODY6-PATH-REASSIGNED
source_agent: codex-local
created_at: 2026-09-08T10:52:01-06:00
inspected_commit: 335ac7556da34fc9084c82c6261bda381af7738a
integration_status: pending
admission_label: pending
proof_status: SOURCE_PATH_INTERFACE_REVIEW_ONLY
compile_performed: false
kernel_verified: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: Bind the existing sixth-column candidate and a fixed physical embedding/domain/path; do not promote it to full-matrix storage alignment.
---

# BODY6 canonical → physical row → path：具体可消费端点

本轮只新增本 review；不改旧候选、state、registry 或其他 agent 文件，不运行
Lean/Lake、Python/Julia checker、receipt 或回归。不重复 generic path obstruction。
结论是“存在具体第六列 source 候选，但尚无所查链中的完整 typed physical
domain/path 实例”，不是所有候选都只有抽象 Prop，也不是已接受的 source theorem。

## 1. 已找到的具体候选，不再把 axis 当未交付参数

`NEW_BODY6_SLICE_AXIS_Consumer20260907.lean:23` 的
`sixth_source_slice_attempt` 类型为

```text
∀ q i, sourceBodyMass q (5 : Fin 6) i (5 : Fin 6)
     = sliceEvaluator q i (5 : Fin 6).
```

它调用 STEP6_DataLeaf 的条件列 theorem，并用本文件 source_axis_dot_target_attempt
提供 axis 参数。因此最终声明类型没有剩余 geometry 参数；不能只读中间
STEP6_DataLeaf 就把该 axis 义务继续列作尚无任何候选。
实际证明链仍全部需要相应编译/依赖审查，本轮没有读取/运行其完整 receipt。

链条是：STEP6_Bridge 的真实 frame slot 5→6 递推 → endpoint/center →
source_gram；AXIS_Geometry 的 source_dot_all → source_axis_dot_target；
STEP6_DataLeaf 的 literal_column_binding_attempt → sixth-column Fourier；
最后用相同 q/i/col=5 接上实际 sourceBodyMass。DataLeaf 的 rfl 是源文本证明
尝试，不是 JSON 字段；但尚未在本轮执行归约或确认 import closure。

这只是单列。AXIS_Consumer.full_source_boundary_attempt 仍显式要求
AllEntriesGramFourierTarget 与 EmptyFourierTarget；LegacyTraceBindingTarget
也是独立义务。单列不能填充完整质量矩阵 Alignment.sameMass，更不能只凭列
相同区分 body6 与 aggregate（其他 body 的 joint6 不活跃）。

## 2. 索引和 row 表示的实际接线

| 层 | 当前定义/映射 | 不能省略的区别 |
|---|---|---|
| 本体标签 | human body 6 → sourceBodyMass body=(5:Fin6) | 不是质量矩阵的行号，也不含 aggregate regularizer |
| CSV entry | generator 将一基 row/col 转为零基 Fin6 | CSV 标签与 Lean 的 0..5 需明确转换，不可模 6 截断 |
| raw row | Data.mkRow 固定 body=5，保留 row/col/Fin6→Int frequency 与四个整数系数标签 | body 不能从任意 normalized row 反推 |
| canonical row | Data.toCanonical 保留 row/col/frequency，系数用 RationalTag.toRat | 此映射丢弃 body 与原分子/分母表示；不是 raw-code 左逆 |
| 第六列 | canonicalRows.filter(col=5) | 有向 row i 保留，不能将 transpose 当同一记录 |
| STEP6 小表 | liftRow 的 col=5、frequency=(0,nx,nx,ny,nz,0)、imag=0 | 相位是 nx*(q1+q2)+ny*q3+nz*q4，全部为零基 q |
| front/tail block | firstJoint:Fin3→Fin6 为 0,1,2；tailJoint:Fin2→Fin6 为 3,4 | tail 不含第六 joint=5，不能混作 Fin3 的 4/5/6 block |

Data.taggedRows/map toCanonical 是具体候选；LabelSupportContract 中的 Nodup/
正分母/互素/非零频率支持仍是显式目标。在所查 BODY6 文件未找到 raw 全标签
RowCode 的 encode/decode 左逆接口。rowKey 仅含 body,row,col,frequency，不含系数。
因此不能将 rowKey 相等或 normalized canonical equality 当作原始字节标签等同。

最小补口并不必重建所有 610 行：若只消费第六列，可保留已有 LiteralColumnBindingTarget
作为数据等式叶；若需 authoritative CSV/raw provenance，则另给完整 raw tag code
及到冻结列表的绑定。canonical 的语义相等与 raw provenance 要分开接收。

## 3. 同一 Ω/domain 的最小可消费 packet（设计，未新增 Lean）

设 X 为实际全状态，D:Real→Set X 为固定物理域，qOf:X→Q6 为实际坐标投影，
Ω:Set Q6 为此次 row/source 与 cap 使用的共同配置域，path:Real→X。
第六列单 entry 的最小 packet 应含：

```text
hProject : ∀ t∈[0,1], ∀ x∈D(t), qOf(x)∈Ω
hPath    : ∀ t∈[0,1], path(t)∈D(t)
hPhysicalRow : ∀ t∈[0,1], ∀ x∈D(t), ∀ i,
  physicalRow(t,x,i)=sourceBodyMass(qOf(x),5,i,5)
hSlice   : ∀ q∈Ω, ∀ i,
  sourceBodyMass(q,5,i,5)=sliceEvaluator(q,i,5)
hCap     : ∀ t∈[0,1], ∀ i,
  |sliceEvaluator(qOf(path(t)),i,5)| ≤ cap(t,i)
```

然后才能逐时推出 |physicalRow(t,path(t),i)|≤cap(t,i)。这里 cap 是外部函数，
没有制造数字。hSlice 在候选类型层可由上面的全 q 第六列 theorem 限制到 Ω，
不需要新的三角展开；但已编译 witness/receipt 仍须单独取得。
hPhysicalRow 若 physicalRow 就定义为该 exact-real source 表达式可由 rfl 给出，
这只绑定该定义，不绑定另一个 CSV、Julia Float64 或物理实现。

未找到当前上述 qOf/D/Ω/path/physicalRow/cap 的共同具体实例。已有
PATHREASSIGNED.TransferInputs 的 value/sourceCap/budget 面向 scalar storage
F/G；其字段不能由矩阵某一列相等自动填入。若只转移 entry cap，可逐 i 取
F=|slice|、G=|physicalRow|，并以值等式给零 shift；这是定义性零差，不是新数值界。
若目标是机械能/storage cap，则还需完整 Ma=Me、sameRemainder、同一 source
storage 与 integrated growth/预算，而非仅六个 entry。

## 4. 已有 domain 与 key 接口的限度

CANDIDATEDOMAIN 区分 o1ConsumerCell、deliveryStateDomain/blockP 与
activeLiftedDomain(V)。它们是独立定义，不能随意把其中一个重命名为 Ω。
activeLiftedDomain 的 circle 条件没有一般的 cosine=cos(q)、sine=sin(q) 绑定；
若 cap 依赖这些 lift，必须补同一 q 的 lift graph。该文件的 origin 成员与
obstruction 不能充当逐时投影实例。

KEYEDSTORAGETRANSFER 的 keyMatches 与 comparison 是不同字段；digest 相同
不能生成 value inequality。SOURCEBLOCKBIND.raw_source_binding_attempt 是
对 sourceA/X/Y 自身的反身等式，不验证独立 candidate table；这些 block
也未覆盖完整 body6 六维矩阵。

## 5. Import/审查范围与最小缺口

第六列候选闭包经过 Geometry、STEP6 bridge、Data 及 source adapters，远大于
纯 path sidecar 的 Mathlib 闭包。风险集中在 Fin/phase 归约、610-row filter 的
rfl 资源、List map/filter 与真实 frame source rewrite。不能借通用 path
sidecar 的旧通过记录替代这条 source 链的 receipt。

本轮完整阅读 targets、slice 主文件、STEP6 bridge/DataLeaf、AXIS consumer、
SOURCEBLOCKBIND、KEYEDSTORAGETRANSFER；对大数据表只检查首部/转换尾部，对
generator 和 Geometry 做定向检索，未重新核验全部 literals 或完整 geometry。
没有依赖公理审计；未发现实例不等于实例在整个仓库绝不存在。

最小缺口是：已接受的第六列 Lean/source witness + 指定物理 row 映射 + 同一
D→Ω 的逐时投影/path 实例 + 同源 entry cap；若目标为 storage，再补完整
matrix/storage alignment。这比新增一个泛型 path theorem 更接近实际消费，
故本轮不增加重复 Lean skeleton。

当前源 SHA-256（相对 examples/routeb_b45_source_comparator_lean）：

```text
RouteBO1Body6CanonicalExportTargets.lean
24635bd0356e6c9a83b15eb0f616327b547caf9257f8992f99b5fb1b7983ce2c
NEW_BODY6_SLICE_20260907Data.lean
e26bb7bbed18325eee215060d37a16b2a5e71762e2689f464874a1aa1fe5a657
NEW_BODY6_SLICE_AXIS_Consumer20260907.lean
e9c51cdc7106728425f25469a79b25666f8d468085ea3fd0064d75ced76764fb
NEW_BODY6_SLICE_STEP6_DataLeaf20260907.lean
691d91adc207decf4e373e520363e94ab736aa9520a6200fd58bb5e126a8ab13
NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean
2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec
```

散列只绑定本次读取文件，不构成编译或 source admission。
