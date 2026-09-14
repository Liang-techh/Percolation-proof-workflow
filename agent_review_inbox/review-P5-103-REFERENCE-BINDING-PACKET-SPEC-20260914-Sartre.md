---
kind: mathematical_handoff_specification
task_id: P5-103-REFERENCE-BINDING-PACKET-SPEC
source_agent: Sartre
date: 2026-09-14
status: SPECIFICATION_ONLY_REFERENCE_UNSELECTED
actual_packet_instantiated: false
source_binding_proven: false
formal_certificate_allowed: false
state_registry_mutated: false
---

# Minimal same-context reference-binding packet / GitHub math-agent handoff

## 0. 交付与非交付

这是可直接实现的规范，不是已存在的 reference 数据或 theorem。当前 source 尚未提供
选定的 `qbarB,vbarB,referenceKey,lbar` 实例。本规范不选择零 reference、不默认相同初值、
不设置 `lbar=0`，不更改原 P5 target，不重做 anchor-domain 预算或全量回归。

本文件仅新增到 review inbox；没有发起 GitHub 任务、PR 或运行 producer。

## 1. 固定唯一数学合同

设 B=(4,5)、D=(1,2,3,6)，均为 human/Julia 1-based 顺序；B 的 zero-based 顺序是(3,4)。
P5 block state 固定为 `(q4,q5,v4,v5)`，其中 v=dq，不是 remote acceleration-difference port。

从同一个配置 C 定义：

```text
Mref = diag(M0_csv[4,4],M0_csv[5,5])  -- parsing semantics belongs to C
I_B  = diag(IVAL4,IVAL5)
u_C(qB,vB,w) = I_B * nominal_f_C(qB,vB,w)_B
            = g_C*w - D_C*vB - K_C*qB  -- exact-model identity to prove

actual full-source evaluator: a = A_C(q[1:6],v[1:6],w)
l    = u_C(qB,vB,w)       - Mref*aB
lbar = u_C(qbarB,vbarB,w) - Mref*abarB
x = qB-qbarB;  y = vB-vbarB;  r = l-lbar
```

qbarB 与 vbarB 必须是被 referenceKey 标识的同一个 reference 的位置/速度，不是从
actual 行另取一个不相关时刻。abarB 是该 reference 的 acceleration 数据/表达式，不能
直接取 `nominal_f`：后者经 I_B 与 Mref 归一化后才进入 acceleration。

源字面常量按理想实数解释时：

```text
D_C = diag(4/5,13/20)
K_C = [[3/4,-1/100],[-1/200,29/50]]
g_C = [1/5,1/10]
```

这些有理数只属于对应 exact interpretation，不能取代部署 Float64 的计算结果。
M0 CSV 第一项 token `0.116667666666667` 也不能换成 `350003/3000000`。

reference 支持两个互斥构造，不允许隐式切换：

1. `descriptor_reference`：选定 qbar0/vbar0、forcing、lbarLaw 后构造/给定
   `qbar'=vbar, Mref*vbar'=u_C(qbar,vbar,w)-lbarLaw`。
   exporter 输出 abarB 与 signed lbar，并验证它们满足该方程。
   若 lbarLaw=0，必须是明确记录的 reference 选择，不是缺字段默认值。
2. `full_source_reference`：选定完整六维 reference 初值/轨迹，以同一 A_C 求 abar6；
   qbarB/vbarB/abarB 是其 B 投影，lbar 按上式求值。
   reference 的 remote 状态也必须提供。它一般不等于 actual remote 状态。

只有 pointwise 表格而没有 trajectory law 可以交付 pointwise evidence，但不升级为
trajectory reference；reference.mode 与 evidence.scope 必须分别表达构造与证据范围。

## 2. 精确定义、单位与符号

令角坐标单位为 A、模型时间单位为 T、generalized-force 单位为 F。此 source 未给出
物理单位认证：默认使用名义维度 A/T/F；若 consumer 声称 rad/s/N·m，必须另行提供
单位映射。禁止仅因名字叫 torque 就声称 SI 标定已完成。三角输入必须使用同一角度
归一化；源中的 pi 与 sin/cos 对应弧度约定，不能塞入未转换的 degree 数。

| 字段 | 精确定义/顺序 | 单位与符号 |
|---|---|---|
| qbarB | reference 在同一 t 的(qbar4,qbar5) | A；不是 error，也非自动物理零点 |
| vbarB | 同 reference 的(vbar4,vbar5)；轨迹层要求 qbar'=vbar | A/T |
| abarB | 同 reference 的 acceleration；轨迹层要求 vbar'=abar | A/T² |
| l | actual 的 `u_C-Mref*aB` | ℝ²向量，每个分量单位 F；非平方范数 |
| lbar | reference 的 `u_C-Mref*abarB` | 两个带正负号的 F 分量，按(4,5)排序 |
| signedResidual r | `l-lbar` | F；actual minus reference |
| accelerationResidual | 若提供，仅可明确记作 `-Mref^{-1}*r` | A/T²；不是 r，且要求同 Mref 可逆 |
| x,y | actual minus reference | A、A/T |
| referenceKey | 对具体 reference descriptor 字节的内容键 | 无单位；不是 traj 编号/随机种子/M0 hash |

上表“两个 F 分量”不表示 norm(l)^2；后者单位为 F²且丢失符号、方向。
Mref、D_C、K_C 的单位分别为 F*T²/A、F*T/A、F/A；g_C 的单位为 F/W，W 是
forcing w 的模型单位，ramp slope c 单位为 W/T。若额外无量纲化，packet 必须记录
可逆 scale 映射及 consumer 方程转换；不可把归一化矩阵悄悄吸收进 lbar。

## 3. 最小填充格式：一次配置、一次 reference、逐行 sample

使用三个普通 UTF-8 JSON payload：`context.json`、`reference.json`、`samples.jsonl`。
不要求新建数据库/registry。大 proof/evaluator 可用 path+SHA-256 引用而不重复内嵌。
以下必填字段无默认值；MISSING 是规范标记，不能写成可接受的数值。

### 3.1 context.json

```text
schema = routeb-p5-reference-binding-v1
source: evaluatorPath, entryPoint, sha256
dependencies: [{path,sha256,role}]  -- all used model/config files incl dhport_lib and M0
producer: sourcePath,sha256,runId,runtimeVersion,numericEncoding
semantics: kind, configurationValues, modelInterpretation
  kind = julia_float64_fd | exact_model
  configurationValues = all consumed DH/controller parameters + G0 construction/value
                        + regularizer + FD step + Mref parsing/selection
  modelInterpretation = exact_model requires complete explicit lift of all constants/operations;
                        float64 requires operation path and raw bit encoding
normalization: blockOrder,remoteOrder,stateOrder,residualOrder,
               units,angleConvention,scales,residualSign='actual_minus_reference',
               Mref, I_B, D_C, K_C, g_C, coefficientDerivationRef
forcing: law, timeDomain, parameterValues, evidenceRef
```

冻结 Mref 不能取当点 M_BB(q)，不得在 reference 点重建 G0。
所有“同配置”字段必须同一内容对象，不只要求相同文件名。
forcing 若为 ramp，记录 `w(t)=c*(t-t0)`、t0、c、时间单位及域，不按 sample 重选 c。
一般 forcing 可引用唯一函数/数据，但 actual/reference 必须引用同一个 forcing 对象。

### 3.2 reference.json

```text
contextKey
mode = descriptor_reference | full_source_reference
selection: provenanceRef, initialTime, initialState, timeDomain
lawRef: path,sha256,entryPointOrDefinition
  descriptor_reference additionally: lbarLawRef
  full_source_reference additionally: full6InitialState, sourceEvaluatorRef
representation: function | sampled_pointwise | certified_piecewise
sampleDataRef: path,sha256                 -- if values supplied as data
interpolationRuleRef: path,sha256          -- required if claiming between-sample values
trajectoryEvidenceRef: path,sha256,scope  -- absent => no trajectory admission
```

selection 必须来自可追踪的任务选择/既有 source 配置，不允许 exporter 静默挑选
qbar0=vbar0=0 或 actual 初值。相同初值若为用户/任务选定，应记录该选择，并另外
核对初始坐标相等；不是 reference 规范自身的默认公理。

### 3.3 每个 sample 行

```text
contextKey, referenceKey, actualRunKey, timeValue, timeIndex
actual: q6,v6,a6,l[2]
reference: qbarB[2],vbarB[2],abarB[2],lbar[2]
  full_source_reference additionally: qbar6,vbar6,abar6
forcingValue: w                              -- c is bound by context if ramp
signedResidual[2]                           -- exact intended definition l-lbar
evidence: scope, actualEvaluationRef, referenceEvaluationRef,
          residualRelationRef, pairingRef
```

sample 的 actual 完整 q6/v6 供 source 重算和后续 hybrid anchor 使用；a6 是完整 solve
结果，不能只保留 aB 并让 remote graph 变成不可复查。reference 的 full6 分支须验证
barB 与 full6 投影完全同序。descriptor 分支不需要虚构 nominal remote 状态。

最小 source export 工作是在已经持有完整 actual 状态/forcing 的调用点记录这些值，
同时消费明确选定的 reference evaluator。只记录 old traj CSV 的六列无法补齐 packet。
绝不因缺少 selected reference 而偷偷运行/选择一个 nominal trajectory。

### 3.4 无循环内容键

```text
contextKey   = 'sha256:' + SHA256(exact UTF-8 bytes of context.json)
referenceKey = 'sha256:' + SHA256(exact UTF-8 bytes of reference.json)
```

context.json 不含自己的 key；reference.json 含 contextKey 但不含自己的 key，且不能
引用含 referenceKey 的 samples.jsonl 作为 sampleDataRef（否则循环）。reference 的
原始 data blob 必须独立于 joined sample 表、且不反向包含 referenceKey。
最后可用独立 receipt 记录 joined samples 文件 hash；其 hash 不进入以上两个 key。
不要求 JSON 语义重排后 hash 相同：验证原始字节即可。path 是定位信息，hash 才固定内容。

数值编码：Float64 用16位 hex bits（及可选展示小数）；exact rationals 用互素
numerator/positive-denominator 字符串。禁止 NaN/Inf、不带语义的 JSON 浮点转换，或
把打印小数 token 直接宣称为运行时 exact 值。原始 bits 的精确有理解释仍不证明
浮点算法等价于 real source 的所有运算。

## 4. 数学 agent 必须交付的最小 lemma 与证据层级

### L1: 固定配置的 residual identity

证明 exact 模型中的 `u_C(qB,vB,w)=g_C*w-D_C*vB-K_C*qB`，并将该 u_C 和 Mref
接到选定 source interpretation。禁止只证明任意矩阵的泛化版本后声称 source 已接通。

### L2: pointwise subtraction（不需要域预算）

从两条同配置、同 w 的 residual 等式直接推出：

```text
Mref*(aB-abarB) + D_C*y + K_C*x = -r.
```

这是 pointwise acceleration identity，不是 ODE theorem。
若 forcing 不同，右侧多出 `g_C*(w_actual-w_ref)`；validator 应拒绝“common forcing”
标记，不可省掉该项。若系数不同，还存在相应 coefficient-mismatch 项；不能消去。

### L3: trajectory promotion（独立 gate）

在同一明确区间上给出 q'=v、v'=a 和 bar 侧对应关系的证据；可选 a.e./绝对连续
合同，但两侧导数与 residual 方程必须同一语义。随后才可推出
`x'=y, Mref*y'+D_C*y+K_C*x=-r`（按所选 pointwise/a.e. 合同）。
离散积分器的输出、有限采样表、插值曲线本身均不证明该 ODE。

### Float64 与误差项：禁止用容差偷换 L1/L2

令所有导出的数按声明解释映射到实数，并定义可检查的 signed defects：

```text
epsilonA = Mref*aB    +D_C*vB    +K_C*qB    -g_C*w+l
epsilonR = Mref*abarB +D_C*vbarB +K_C*qbarB -g_C*w+lbar
epsilonS = r_export -(l-lbar)
```

那么精确恒等式为
`Mref*(aB-abarB)+D_C*y+K_C*x = -r_export+epsilonS+epsilonA-epsilonR`。
这解释 source 浮点公式与 rational consumer 之间所有算术差异该放在哪里；它不自动
证明 defects 很小，也不证明导出的 acceleration 属于 exact source graph。
要进入无误差版本必须证明对应组合为零并完成 source/trajectory binding；否则给
严格 enclosure 并显式保留误差项。当前 P5 consumer 若无预算接口，保持 pending，
不得改写既有 target 来吸收误差。本轮只定义合同，不声称取得误差界。

## 5. Fail-closed 判定（缺失与不一致分开）

| 条件 | 判定 |
|---|---|
| 缺 selected reference、qbar/vbar/abar/lbar/r 任一必填字段 | pending / MISSING_REFERENCE_FIELD；不得补0 |
| 缺 source/config/forcing/provenance 引用或依赖 hash | pending / INCOMPLETE_CONTEXT；无 source admission |
| 给出的 hash 无法匹配、维度/索引/符号/归一化冲突、含非有限数 | rejected / MALFORMED_OR_MISMATCHED_PACKET |
| 把 l2、remote vbar2、acceleration residual 填成 signed force residual | rejected / WRONG_RESIDUAL_TYPE |
| reference/actual forcing 不同却要求 L2 的 common-input 版本 | rejected / FORCING_MISMATCH |
| 所有字段齐全且 hash/类型/配对通过 | packet_complete_only；不是 L1/source theorem |
| 只有 runtime evidence，或 reference 表格没有导数/ODE evidence | numerical_or_pointwise_only；trajectory admission=pending |
| exact L1/L2 的 source binding 成功，无 L3 | pointwise_bound_only；不闭合 P5 trajectory |
| L1–L3 完成且误差处理与 consumer 一致 | eligible_for_separate_review；仍不得直接写 registry |

若仅用名义单位 A/T/F 可做同单位数学定理；缺 SI 标定只阻止相应 physical-unit claim。
若 consumer 要求某一无量纲/物理 normalization 而映射缺失，则该 consumer 必须 pending。
缺 initial matching 不阻止一般 nonzero-initial-error identity，但阻止 zero-initial-error
specialization。这个区别必须体现在判定中，不能把更强前提偷偷设为默认。

## 6. 可直接交给 GitHub 数学 agent 的任务说明

> 实现 P5-103 的最小 same-context reference-binding packet 与 source-specific subtraction
> proof。以 `routeB_descriptor_residual_interface.jl::evaluate`、其实际 dhport_lib/M0 依赖
> 和本规范为合同；先核对 source hash。保留 B=(4,5)、signed force residual
> `l=I_B*f_B-Mref*aB` 及 `r=l-lbar`。第一步确认任务提供了 selected reference 的来源、
> mode、初值/forcing/trajectory 或 pointwise evaluator；若缺失，交付精确 missing-field
> list 与未实例化模板，不得自行选择零 reference 或 lbar=0。
>
> 在授权的新目录交付：(a) context/reference/joined sample 格式与 fail-closed validator；
> (b) source export 的最小局部接线说明或获授权的新 wrapper，完整捕获实际 q6/v6/a6/w；
> (c) L1/L2 的 source-specific proof attempt；(d) 独立 L3/rounding-error 待办与判定。
> Float64 payload 只作 runtime evidence；exact-model 必须声明并证明 source interpretation。
> 不得为了获得 reference 而全量重跑轨迹，不得修改 state/registry/shared adapters。
> 未获共享 source 修改授权时只给 patch proposal/wrapper，不改部署入口。
>
> 最小验证只检查真实 packet（若存在）及定向负例：删除 lbar、交换4/5、反转 r 符号、
> 替换 referenceKey/forcing 对象、替换 Mref 为理想 rational、把 l2 当向量、缺导数 evidence。
> validator 必须给出上述精确拒绝或 pending 类别；负例是格式/身份门测试，不是物理反例。
> 若环境可编译，仅报告实际执行的命令、环境、输出与 axioms；否则标 UNCOMPILED。
> 交付所有新文件路径/hash、实例字段 completeness、L1/L2/L3 各自状态，不准用一个
> 总体 PASS 掩盖 trajectory 或 source binding 缺口。不做 anchor-domain 代数或泛化审计。

### 任务完成条件

本规格任务的完成不要求伪造一个不存在的 reference。agent 必须交付可填充 schema、
类型/身份 fail-closed 门、source-specific proof obligations 与精确判定；如果选定对象
仍缺失，应明确 `packet_instantiated=false, source_binding_proven=false`。
只有真实 reference 被提供且通过其对应 gate，才能另报该层完成。

## 7. 本轮事实依据

直接重新阅读 S=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`
下 `routeB_descriptor_residual_interface.jl:22–59`，并以
`review-P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING-20260914-Sartre.md` 的字段/hash 快照
作为前轮本地证据。规范中的 packet、validator、source-export wrapper、L1–L3 均是待交付项，
本轮没有创建其实际实例或运行 Lean/Lake/Julia/回归。
