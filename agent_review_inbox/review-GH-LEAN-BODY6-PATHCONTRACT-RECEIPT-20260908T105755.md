---
kind: review_result
review_id: review-GH-LEAN-BODY6-PATHCONTRACT-RECEIPT-20260908T105755
task_id: GH-LEAN-BODY6-PATHCONTRACT-RECEIPT
source_agent: codex-local
created_at: 2026-09-08T10:57:55-06:00
inspected_commit: a4adf0ebc4f2b708df2873ff0fb6da4cde9ba744
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_PATHCONTRACT_REASSIGNED_20260908.lean
artifact_sha256: ff5e2dfbcf0375d96cce232c739e0098381ce5b1828f7142dae23ac3e86a68fc
proof_status: OPEN_UNCOMPILED
integration_status: pending
admission_label: pending
source_receipt_status: not_supplied_for_this_contract
compile_receipt_status: missing_for_new_candidate
compile_performed: false
kernel_verified: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: Supply same-source contract fields and a separately authorized pinned Lean/source receipt; do not promote from theorem decomposition.
---

# BODY6 第六列 typed path contract

新增一个 Prop structure 与两个 theorem 候选，namespace
`Body6PathContractReassigned`。本 review 名含 RECEIPT，但它只是 prep envelope，
不是编译或 source receipt。未运行本机/远程 Lean/Lake、checker 或任何 receipt。
仅新增指定候选与本 review；旧文件、state、registry 与其他 agent 文件不变。

## 固定参数与五个字段

SixthColumnPathContract 的全部字段共用以下固定参数：

```text
embed : X → Physical
qOf : Physical → Q6
domain : Real → Set X
Omega : Set Q6
path : Real → X
rows : List CanonicalRow
physicalRow : Real → Physical → Fin 6 → Real
cap : Real → Fin 6 → Real
```

| 字段 | 精确义务 |
|---|---|
| projection | x∈domain(t) ⇒ qOf(embed(x))∈Omega，t∈[0,1] |
| inclusion | path(t)∈domain(t)，t∈[0,1] |
| physicalIdentity | physicalRow(t,embed(x),i)=sourceBodyMass(qOf(embed(x)),5,i,5)，在同一 domain 上 |
| sourceIdentity | sourceBodyMass(q,5,i,5)=body6CanonicalEvaluator(rows,q,i,5)，在同一 Omega 上 |
| canonicalCap | 沿同一 embed/path/qOf 的 canonical 第六列绝对值≤cap(t,i) |

physical_eq_canonical_on_path 只组合两项同一性；transport_physical_row_cap
通过该等式重写，消费输入 cap。没有产生任何新 cap 常数、增长估计、ODE 或
路径实例。embed 只是显式函数参数，不附加 Injective；此单向运输无需单射，
若应用需要逆向恢复或物理状态唯一性，须另给单射/等价 witness。

固定 interval 为 [0,1]，固定 human body6=Fin6 值5、column6=值5，i 保持任意
Fin6 有向行。函数 physicalRow 的名称不证明其来自实际实现；physicalIdentity
正是待补的 exact-real 同源前提，不可由 digest、CSV 名称或 Float64 近似代替。

## 与已有第六列候选的最小接法

令 rows=NEW_BODY6_SLICE_20260907Data.canonicalRows。已有
NEW_BODY6_SLICE_AXIS_Consumer20260907.sixth_source_slice_attempt
在声明类型上给出全 q 的 sourceBodyMass 第六列等于 sliceEvaluator；后者按定义
就是该 rows 的 body6CanonicalEvaluator。因此未来取得该链的已接受 witness 后，
可将它限制到 Omega 填 sourceIdentity，不需要新增三角展开。

本文件刻意不导入 AXIS/STEP6/Data 候选链，只导入 canonical targets，以免将
该 source witness 的 elaboration 状态混入纯 transport prep。没有给出具体
contract inhabitant。projection、inclusion、physicalIdentity、canonicalCap
均尚未交付，sourceIdentity 也没有本轮 source receipt。

两列/矩阵存储等式不是本结论：第六列不足以填 full-matrix sameMass 或机械能
alignment，也不能自动转成完整 row norm、Schur cap 或 aggregate mass 结论。

## canonical 与 raw provenance 的边界

CanonicalRow 保留 row/col、完整 Fin6→Int 频率及 rational real/imag 值；没有
body 字段，也不保留原始 numerator/denominator spelling。
Data.toCanonical 是语义转换，不是 raw-code 可逆解码。因而本 contract 的
sourceIdentity 是值函数相等，不证明 CSV 字节、原始行标签、多重集或生成正确性。

若要求 raw provenance，独立 receipt 必须绑定原始 body=6 标签、CSV 一基→Lean
零基 row/col、六维有符号频率、系数标签及精确列表/重数；不能只比较 normalized
Rat、rowKey 或行数。row 5 与 column 5 仍不可与“本体编号5”混淆。

## API / import / receipt 风险

直接 import 为 RouteBO1Body6CanonicalExportTargets，其传递闭包包含 source
adapter 与 evaluator/Mathlib，不是最小 Mathlib 闭包或已审计环境。
新 proof body 只用 Prop 字段、Eq.trans 和 rw；主要待检点为隐式类型参数、
有限索引 numeral 与 rewrite elaboration。没有算术求解、native_decide、
新增公理或 placeholder witness；文本结构检查不等于依赖公理审计。

后续独立授权的 receipt 至少应绑定此新源 SHA、直接/传递 source pins、
Lean/Mathlib versions、完整 command/exit/logs、OLean hashes、两个 theorem
的 elaborated types/#print axioms，以及所实例化 rows/source witness 的身份。
另需实际 embedding/domain/path/cap 实例的源与证明。没有这些材料，维持 pending；
即使此纯组合候选以后编译成功，也不自动升级 source 或 registry。
