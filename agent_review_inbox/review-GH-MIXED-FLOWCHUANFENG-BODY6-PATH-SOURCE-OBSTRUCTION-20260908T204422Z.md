---
kind: review_result
review_id: review-GH-MIXED-FLOWCHUANFENG-BODY6-PATH-SOURCE-OBSTRUCTION-20260908T204422Z
task_id: GH-MIXED-FLOWCHUANFENG-BODY6-PATH
source_agent: codex-body5-interface-lane-takeover
created_at: 2026-09-08T20:44:22Z
inspected_commit: ea2354fa764390d8a0ba8acb925fde8974b51c37
status: FIELD_LEVEL_SOURCE_COVERAGE_OBSTRUCTION
integration_status: pending
admission_label: pending
source_binding_proven_this_review: false
concrete_contract_constructed: false
lean_lake_run: false
state_mutation: false
registry_mutation: false
requested_action: retain separate column-source and storage-path obligations; supply authoritative instance fields before assembly
---

# BODY6 path lane：真实 source 接线的字段级 obstruction

结论：现有通用消费者足以表达条件式转移，继续增加同类 wrapper 不会构造真实实例。
本轮只新增本 review，不新增重复 Lean。当前所读 physical-column handoff 的
`physical_instance.status=MISSING`，五个 witness、参数清单和 raw provenance 全为 null。
在下列明确检索范围内，contract 的出现均为定义、消费者参数或 probe，没有找到具体
source/path 实例；这不是对全仓或外部 source 的穷尽不存在证明。

检索范围为 body comparator 与 `routeb_o0_h_acc_source_refinement` 两个 example 目录，
关键词为 SixthColumnPathContract、ConsumerPremises、TransferInputs、PathLedgerBinding；
另只读源定义、相关 review/receipt、冻结 Julia 源快照。未运行任何 checker、Lean/Lake、
Julia、producer、regression、integrator 或远端任务。没有读取/改写当前 state 以重判 frontier。

## 1. 两个同名近似的 path lane 必须分开

| 精确接口 | 已有条件式结论 | 不含的结论 |
|---|---|---|
| `NEW_PATHCONTRACT_REASSIGNED_20260908.SixthColumnPathContract`（namespace Body6PathContractReassigned） | body index 5、column index 5 的物理量等于 canonical evaluator，并转移绝对值 cap | storage initial/growth、strict ledger barrier、完整 36-entry h_body_6 |
| `NEW_BODY6_SLICE_PATHREASSIGNED20260908.TransferInputs` | 给定固定 D、wholePath、Q-wide identity、sourceCap、single-shift budget，转移 G 的全路径 cap | physicalRow 或 sourceBodyMass/canonical identity |
| `NEW_BODY6_SLICE_PATHCONTRACT20260908.PathContract` | initial + 已积分 growth + on-path G=F+B + pointwise budget → FullPathCap G | 固定物理域 D、域内全部点的 identity、ODE/coverage |
| `ALIGNEDPATHCAPCONSUMER.ConsumerPremises` | f=1,h=0 的特定 actual-storage specialization 通过 Alignment 生成上述 identity | active candidate 本来就是该 specialization 的证据 |

PATHCONTRACT 的 value 只有 path 上量词，不能推出 TransferInputs 的 Q-wide value；
这不是算术不可组合：已有 seam adapter 可取 cap=bar−B，但 projection、wholePath、
Q-wide identity 仍须另外提供。反向取 b(t)=cap−F(0,path(0)) 只是已知 full cap 的重包装，
不是从源微分不等式积分产生的增长证据。没有理由重做该 generic adapter。

## 2. SixthColumnPathContract：逐字段阻碍

参见 `NEW_PATHCONTRACT_REASSIGNED_20260908.lean:17–30`。

| 字段/索引 | 真实绑定需要什么 | 当前可确认的缺口 |
|---|---|---|
| X、Physical、embed、qOf | 权威 full-state 顺序、实际 joint angle 提取、是否需由 tracking error 恢复 reference、单位与 DH convention | 都是自由参数；令 embed=id 或把误差向量直接当角度不能充当源证明 |
| domain、Omega、path | 调用者固定的全状态域、有效配置域、实际路径与参数区间的定义 | 未提供具体对象或权威 manifest；便利地令 domain=univ/pullback 不解决 physical domain |
| projection | 所有 t∈[0,1]、x∈domain(t) 的 qOf(embed x)∈Omega | 无实例；不只是在初值或某些样本检查 |
| inclusion | 同一个 path 在整个 [0,1] 内属于指定 domain(t) | 无 ODE existence/continuation、invariance、validated tube 或其他全程覆盖 witness |
| physicalIdentity | 域内全部 x 上 physicalRow = **未加 regularizer 的单个 body-6** sourceBodyMass 第六列 | 未指定 physicalRow 是 body contribution、总质量矩阵还是 Float64 output；见下一节的实际语义差别 |
| sourceIdentity | 同一 rows 在所有 q∈Omega、六个 i 上绑定 sourceBodyMass | CanonicalRow 是规范化 ℚ value record；raw export/reification 与 source theorem 仍是前提，hash 不代替它们 |
| canonicalCap | 同一路径、每个 t 和 i 的绝对值界 | 无具体 cap/witness；选 cap=abs(evaluator) 可得到平凡类型实例，但不给调用者固定预算 |

现有 `NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean` 的 consumer 始终接收 h；
Fin 6 的 5 值等式和 `#check` 不会制造 h。sourceIdentity 只覆盖最后一列，不能仅凭这个
contract 关闭 full source comparator 或 `Body6LegacyTraceTarget rows`。

## 3. 源快照暴露的一个具体 semantic adapter 缺口

本轮直接读取的是冻结快照
`examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl`，
不是重新确认的外部现用源。文件 hash 与同目录 SHA256SUMS.csv 的记录一致；
其部署权威性、是否仍被现用程序载入以及参数 overrides 未在本轮核验。

该文件 46–60 行的 mass_matrix 循环累加六个 body contribution，随后加
`Float64(regularization)*I`；默认 MASS_REGULARIZER=1e-6（27 行）。
31–43 行通过 Float64 DH transforms 产生 frame/axis，52、58 行使用
`Ri * (I_val[ii]/3 * I) * Ri'`。Lean `sourceBodyMass` 则是 exact-real
`contractMass` 的单 body，使用已经除以 3 的对角惯量，没有总和和 regularizer。

不能因此不加区分地写

```text
physicalRow := mass_matrix(q)[:,6]
physicalIdentity := rfl
```

但也不能笼统声称“最后一列还必有其他五个 body 的非零贡献”：
Julia 的 jj=1:ii 和 Lean BodySemanticCore 的 inactive-joint guards 显示，
body index b<5 的第六个 Jacobian 列为零。在**精确实数模型且先证明 source bridge**后，
可由零列消去得到

```text
S(q,i) := sourceBodyMass q 5 i 5
M_total_mu(q,i,5) = S(q,i) + if i=5 then mu else 0.
```

因此正 regularizer 的确定性 correction 仅落在该列的 i=5 对角项；
不能给六个 entry 都重复加 mu，也不能直接漏掉最后一项。若另外已提供
Body6SixthDiagonalTarget，并选 exact-real mu=1/1000000，则目标对角值为
1/60+1/1000000，而不是 1/60。这个条件化代数观察不是 Float64 输出相等的证明。

还需要将旋转惯量化为 isotropic inertia 的 exact orthogonality 源桥；
Float64 frame products 不应被假定具有精确正交性。源码 decimal 1e-6 转成 binary64
也不能无误差视作 ℚ 的 1/1000000，除非单独定义 exact-real reference 并纳入表示误差。

最窄的后续接口草案（仅数学 typed contract，没有声称 Lean elaboration）：

```text
fixed qOf, embed, domain, actual path, rows, mu, eps, requested cap
same-source exact-body/canonical identity + wholePath/projection
runtimeRefinement:
  ∀ s∈[0,1], ∀ i,
    |R s (embed(path s)) i -
      (S(qOf(embed(path s)),i) + if i=5 then mu else 0)| ≤ eps s i
canonicalCap:
  ∀ s∈[0,1], ∀ i, |Eval(rows,qOf(embed(path s)),i,5)| ≤ C s i
--------------------------------------------------------------
  |R s (embed(path s)) i|
    ≤ C s i + |if i=5 then mu else 0| + eps s i
```

R 必须是预先确定的实际 evaluator/输出模型；不能把 R 重新定义成 S 来填补 source 字段。
若选择“只证明 exact-real body contribution”，可以保留旧 contract 不变，但交付名称和
claim 必须限于该对象；若选择 deployed Float64 total mass，以上 refinement/error 和
参数绑定不可缺。此处既未产生 eps，也未把任何数值测试提升为误差证书。

## 4. storage/path consumer 接入真实 ledger 的最小额外字段

`COMPILEDLEDGERBINDING` 的 Sample={q,v,slope}、time-dependent StorageData，
与 ALIGNED 的 State=(q,v)、f=1,h=0、固定 p 不是同一 typed model。

- **state/storage transport**：提供 rho(Sample)=(q,v) 与 path composition，
  固定域 D_sample→D_state 的 transport，以及 `actualAt d t x = source m t (rho x)`。
  后者需实际 d 的 f/h/p、质量、势能归一化和 H 的 specialization；不能靠变量同名。
  h=0 分支可能令 storage 值不依赖 slope，但不能丢弃原域对 slope 的限制后反推原路径覆盖。
- **Alignment.sameMass**：body-6 单列/单体 equality 不是完整 Mactual=Mencoded。
  全质量、regularizer 与另外五体仍须按实际消费对象另接。
- **Alignment.sameRemainder**：U−Uzero 的物理势能 identity 和 H/p 的二次补偿；
  现有 `remainder_from_source_fields_attempt` 只消费 hU/hQuad，不创建它们。
- **initial/start**：InitialSetCap 与 path(0)∈X0 是两项；某个 V0 数值吻合不能代替任一项。
- **growth/uniformGrowth**：IntegratedGrowth 已经是逐时全程上界的定义，
  不是 FTC theorem；需源轨迹 regularity、导数/积分估计或另一路严格 producer。
- **time/parameter meaning**：当前 interval 只是 [0,1]。若真实时间 tau=t0+T*s，
  必须 transport source/time/domain，并在源微分增长推导中计入 T；
  若 s 是静态空间插值，不能将它自动当成 ODE 时间或流动后的 path sheet。
- **fixed-domain coverage**：对 x∈D 成立的导数/identity 用于所有 path(s)，必须有全程 inclusion。
  若 D 本身按待证 barrier 定义，须另交 first-exit/continuation 论证，不能循环回填。
- **strict threshold**：ledger 要 tube<1；FullPathCap 给 ≤bar，不产生 strict gap。
  G=F+B 不是 ledger sameStorage 的零偏移相等，必须选择消费 F 还是 G 并保持预算。
  对 normalized-origin 条件 F(0)=0 和当前 B=4079979/400000，要求 G 的 bar=1
  是具体预算不相容，不是“编译缺口”；不能靠重复/省略 B 修补，也不是控制器失败定理。

以上字段仍未提供真实 source 实例。没有选新 D、F/G、rows、cap、active candidate 或
改变 bar 来绕过它们。

## 5. receipt 与编译边界

现存 `NEW_SEAM_BODY6_TYPED_RECEIPT.json` 的已存 runs[0] 记录 adapter-only exit 0，
同时显式 `complete_PATHCONTRACT_checked=false`、`source_binding_proven=false`、
`concrete_path_contract_inhabited=false`。本轮只读字段，不重演、不将历史输出说成新验证。

另一个 `NEW_BODY6_PATHCONTRACT_HANDOFF_Receipt20260908.json` 属于上文
SixthColumnPathContract/probe，`compile.status=NOT_RUN`、physical_instance=MISSING。
不能用第一个 storage seam 的成功记录填第二个 physical-column handoff 的 compile 或 source 字段。
目录已有 .olean 也不提供这些实例。

最小后续工作不是新增抽象 record，而是先提交两项权威选择：
(1) physicalRow 的实际对象及 exact-real/Float64/regularizer convention；
(2) 固定状态域、path 与参数语义及其 coverage producer。
随后逐字段填 physicalIdentity/sourceIdentity/canonicalCap；storage 支线另交
actualAt specialization、growth、strict ledger bridge。未提供时状态保持 pending。

## 6. 只读输入快照

以下为本轮读取的字节 SHA-256；只用于追溯，不表示 kernel/source admission。
写入后复核同一组输入。原有文件与共享状态不由本轮修改。

```text
examples/routeb_b45_source_comparator_lean/NEW_PATHCONTRACT_REASSIGNED_20260908.lean
ff5e2dfbcf0375d96cce232c739e0098381ce5b1828f7142dae23ac3e86a68fc
examples/routeb_b45_source_comparator_lean/NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean
78cd395e47fc5edc7e781ba1574562ddcb8fa41135c0c3e8613cdcbfd7e98206
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean
2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHCONTRACT20260908.lean
bd96b283accae86e695a180bfe9223e9b396b6efdd0178dac380394eac6321f2
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean
f55de2b76ed401e7962b1494d02826c8fc2f951d7137f02461edeb56d5757d62
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean
f698d8c56c83005df0e0a907452ae7a6f083eb3736e6df60db4d0190084367dd
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean
f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f
examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_COMPILEDLEDGERBINDING20260907.lean
0de2680d048c620a05fd2e02402b24c333a63e9c768c3193c819e09e48eaeb9b
examples/routeb_b45_source_comparator_lean/RouteBO1Body6CanonicalExportTargets.lean
24635bd0356e6c9a83b15eb0f616327b547caf9257f8992f99b5fb1b7983ce2c
examples/routeb_b45_source_comparator_lean/RouteBO1PerBodyExactSource.lean
c09b84677adef121488b3ceb53e886d0ef0b028c7979d91f8a7f9ba0fbfcd553
examples/routeb_b45_source_comparator_lean/NEW_BODY6_PATHCONTRACT_HANDOFF_Receipt20260908.json
b245d21e552edeeb739d89d9bb77f7604767d13ef74862adad8c70ef3c9ac3a0
examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
examples/routeb_o0_h_acc_source_refinement/NEW_SEAM_BODY6_TYPED_RECEIPT.json
bb0fb659825a27411887075876e44e3f93a3c8b4e959eb347291fd6188d8093b
```

