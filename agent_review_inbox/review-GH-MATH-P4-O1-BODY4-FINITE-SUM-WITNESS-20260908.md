---
task_id: GH-MATH-P4-O1-BODY4-FINITE-SUM-WITNESS
status: EXACT_SOURCE_FINITE_SUM_CANDIDATE_UNCOMPILED
integration_status: pending
admission: pending
source_binding_proven: false
lean_lake_run: false
---
# Body-4 step-3 三行有限和 witness

本轮交付隔离候选
`examples/routeb_o1_body4_source_gram_proof_attempt/NEW_FINITE_SUM_20260908_STEP3_TRANSLATION.lean`。
SHA-256：A7144407F5AA2C5F8BC4F30D2327B39CB22F1A587A0F0A141B5E22605A344B8E。
本 review 按任务要求放入 agent_review_inbox；没有写入旧 review 或旧候选。

结论：已给出原 `Body4Slot4TranslationTarget` 的无几何前提候选证明文本，
不是新 axiom 或 target-valued 参数；未运行 Lean/Lake，因此尚不能认证为可消费的 inhabitant。
可供审阅/未来编译消费的是精确字段映射与完整候选脚本，不是 VERIFIED theorem。

## 1. 三行有限和与字段映射

设 `F3=routeBFrameSlot q 3`、`F4=routeBFrameSlot q 4`、
`T3=routeBStepFunction q 3`。以下均为零基索引：

| 字段 | 来源及本轮候选声明 |
|---|---|
| T3[0,3]=0 | imported realDHStep 的 ct*a，routeBA 3=0；step3_column 第一字段 |
| T3[1,3]=0 | imported realDHStep 的 st*a，routeBA 3=0；第二字段 |
| T3[2,3]=19/100 | imported routeBD 3 的实部；第三字段 |
| T3[3,3]=1 | imported realDHStep 的 homogeneous entry；第四字段 |
| F4=F3*T3 | prefixFrame slots 3/4 的同一左结合定义；slot4_product |
| (F*T)[r,3]=sum(k:Fin4,F[r,k]*T[k,3]) | Matrix.mul_apply；product_column_four_terms |
| original target 的 a | embed3 a : Fin4，保持 a.val，a 只取0/1/2 |

三个 exact spatial equations 明确为：

```text
F4[0,3] = F3[0,0]*0 + F3[0,1]*0 + F3[0,2]*(19/100) + F3[0,3]*1
        = F3[0,3] + (19/100)*F3[0,2]
F4[1,3] = F3[1,0]*0 + F3[1,1]*0 + F3[1,2]*(19/100) + F3[1,3]*1
        = F3[1,3] + (19/100)*F3[1,2]
F4[2,3] = F3[2,0]*0 + F3[2,1]*0 + F3[2,2]*(19/100) + F3[2,3]*1
        = F3[2,3] + (19/100)*F3[2,2]
```

`source_row_four_terms` 给出代入列值后的四项式，
`source_row_translation` 用 ring 重排，`spatial_translation_fields`
将三行分为可投影的 conjunction，`slot4_translation_attempt`
最终把 row=embed3 a、column3=origin、column2=zAxis 接回原 target。

不需要假设 F3 正交、底行 homogeneous 或知道其具体坐标；泛化有限和引理对任意 F/T
成立，source specialization 则严格使用实际 routeBFrameSlot/routeBStepFunction。
此处没有将 generic 矩阵恒等式直接命名为 source theorem，所有 source 代入步骤单列。

## 2. 哈希与 snapshot 字段对应

本轮重新计算三个 snapshot 哈希，均匹配前轮审计及现有 body-trace manifest：

- `artifacts/task_routeb_body_trace_sink_current/source_snapshot/routeB_fourier_rational_probe.py`：
  9460181770E47BE0ECBDE43A8A29EF285DA1168C3121FAB18D5378C671401A7B。
- 同目录 `dhport_lib.jl`：
  AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936。
- 同目录 `routeB_fourier_mass_full_rational.csv`：
  A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8。

source key 仍是
`routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)`。
aggregate hash 只作来源标识，不证明 frame 字段。

generator 行19–22 给出 step3 的 A=0、D=Q("0.19")、offset=0、alpha=-pi/2；
行118–121 给出最后一列 (ct*A,st*A,D,1)；
行125 在乘 step 前读取父轴，行126 的 matmul(Tc[-1],A) 对应 F3*T3。
Julia 快照第4个 DH 行及 fk_frames（行31–43）使用同向乘法和父轴读取。
本轮未运行它们；Julia 浮点常数/乘法不是精确实数等式的证明。

Lean 候选中的 19/100 是被证明等式的右端，左端经
RealDHStep -> FourierNormalForm 的既有 routeBA/routeBD 定义归约；
没有新增独立 DH 参数表，更没有把快照解析值作为假设直接塞进 theorem。
同源快照与 Lean 的跨语言语义认证仍独立于这份 Lean exact-real 候选。

## 3. 最短消费位置与仍缺 witness

未来编译成功并审计 imports/axioms 后，可以直接将
`RouteBO1Body4FiniteSum20260908.slot4_translation_attempt`
传给 FRAME_HANDOFF 的 `joint3_linear_of_translation`。
这一步只闭合 translation 子目标，不要求 PrefixColumnsTarget。
human body4=Body3；COM slots3/4；joint3 active，父轴来自 slot3：
midpoint(F3.origin,F4.origin)-F3.origin=(19/200)*F3.zAxis，Jv 由平行叉积为零。
它不让 joint3 的 Jw 变成零；inactive columns 仍仅4/5。

最小剩余 witness：

1. 一致的 pinned Lean/Mathlib import 环境，以及本文件确切字节的成功 elaboration/退出码。
2. step3_column 的 norm_num 源常数归约、Fin4 sum 展开、embed3 定义等价的实际通过记录。
3. 最终 slot4_translation_attempt 的 axiom 输出与完整 source/import 身份。
4. 若宣称 generator/Julia 对应真实运行时语义，再另交跨语言/refinement 证据；
   不能把本轮 snapshot hash 校验充作该 witness。

文件仅导入原 RouteBO1Body4SourceGramTargets，不导入旧 proof attempts、
FRAME_HANDOFF 或 PORTS；没有在新候选中接 mass/Gram/trace 或完整 Jv/Jw。
#print axioms 只是未来命令文本，未执行。本轮静态扫描未发现 sorry/admit/axiom/unsafe 声明，
这不等于传递依赖审计。没有跑本机 Lean/Lake、生成器、符号验证或全回归。
未修改 state、registry、旧 artifacts、旧候选或其他 agent 文件。

