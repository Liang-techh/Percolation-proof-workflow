---
kind: review_result
task_id: P5-103-ACTUAL-REFERENCE-CONTEXT-BINDING
source_agent: Sartre
review_date: 2026-09-14
status: MISSING_ACTUAL_REFERENCE_CONTEXT
integration_status: pending
reference_packet_complete: false
source_binding_proven: false
formal_certificate_allowed: false
lean_run: false
lake_run: false
producer_run: false
regression_run: false
state_registry_mutated: false
---

# P5-103: actual reference context 的字段级缺口

## 结论

在下述真实 source/outputs 中，没有找到已选定且同 context 的
`qbarB, vbarB, referenceKey, lbar` 四字段实例。已定位的是 actual residual
evaluator、actual 数值轨迹、冻结参考质量与若干 nominal acceleration 定义。
这些不能合成为一个 nominal trajectory/reference packet。

本轮新增的区分是：**已有 exporter manifest 的四条文件哈希均匹配当前文件，
但匹配的对象不包含 nominal reference。** 因此障碍不是简单的输出文件哈希损坏，
而是缺字段、缺配对与缺 normalization/source identity。不能用一个新造的
referenceKey 字符串或把 actual 状态重命名为 nominal 来补齐。

缺失证据维持 pending；没有得到 actual reference 不等于证明这种 reference 不存在，
也不是 anchor-domain、P5 或原 block45 轨迹定理的反例。本 review 不重复预算代数。

## 1. 查阅范围与直接证据

路径根：

- E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`
- S = `E/routeB_dense_Mq`
- W = `C:/Users/z5242/Desktop/重构版/工作流`

已定向搜索 E 的 Julia/Python/MATLAB/JSON/TOML 中 `qbarB, vbarB, dqbar,
referenceKey/reference_key, lbar, q_ref/dq_ref, q_nom/dq_nom`，并另查 `qbar/vbar`
与 nominal trajectory/solution 名称。排除依赖 depot、ref_tssos、备份与恢复副本；
重点阅读 S、robot_final、robot_formal_v1。W 的 examples/artifacts 精确字段搜索
排除 Mathlib、runtime 与历史 checkpoint；接口/review 的假设不计作实例。
没有解析不相关二进制 MAT 数据或声称遍历整个磁盘。

| 实际文件/位置 | 找到的对象 | 为何不是完整 reference |
|---|---|---|
| S/routeB_descriptor_residual_interface.jl:22–38 | M0 CSV 对角参考、常量、`nominal_f(q,dq,w)` | 是函数，不指定 nominal 初值、曲线或 pointwise reference |
| 同文件:40–59 | `evaluate(q,dq,w)` 求完整 acceleration，再输出 force residual | 无 qbar/vbar 参数、reference identity 或 lbar 定义 |
| 同文件:62–85；同名 CSV header | sample,q4,q5,dq4,dq5,w,a4,a5,l4,l5 等 | 是孤立 actual 回归输入；无 nominal 四坐标、t/c、remote 状态 |
| S/routeB_export_traj.jl:89–109,135–212 | actual 六维数值推进；输出 `(traj,t)` | 没有并行 nominal 状态推进/paired initial data；cw 与 remote 状态未写入输出 |
| S/routeB_state_samples.csv header | `traj,t,q4,q5,dq4,dq5` | 全是 actual block 状态，且只是选择时刻 |
| S/routeB_traj_all.csv header | `traj,t,V,tube,p,ratio,bound,l2` | `l2` 是 actual `norm(lv)^2`，不是 signed lbar 向量 |
| S/routeB_export_manifest.toml | empirical run、四条文件 hash、seeds、FD knobs | 无 referenceKey、reference output hash 或 actual-reference 配对表 |
| S/routeB_compact_nominal_descriptor_interface.csv:2–6 | B=(4,5), D=(1,2,3,6)，nominal remote acceleration 方程 | algebraic remote acceleration 不是 nominal block position/velocity |
| S/debug_12e_nominal_v.jl:13–38,58–83,106–148 | `v=a_true,D-a_nom,D`、`vbar2=max(norm(v)^2)` | v 的含义是 acceleration 差；输出只有采样聚合量，不是 vbarB |
| S/routeB_block_solve.m:6–18,74–90 | work30 cubic nominal block，`l=ddq_exact-ddq_nominal` | 不同 nominal model、不同 residual 单位/符号；也不输出 reference 曲线 |

T-P5-018 review 的两条同 forcing descriptor 方程、`lbar=0` 特例以及相同初值
均是条件。P5-098 与 centered-anchor review 已指出 reference 缺口；本轮直接查源
补充字段证据与 hash 区分，不把旧 review 当作已选定实例。

## 2. 可以固定的 partial identity packet

下面是 source 身份事实，不是完整 reference packet。

```text
blockOrderHuman = [4,5]
remoteOrderHuman = [1,2,3,6]
blockOrderZeroBased = [3,4]
localStateOrder = [q4,q5,dq4,dq5]
actualEvaluator = S/routeB_descriptor_residual_interface.jl::evaluate
actualInputOrder = (q[1:6],dq[1:6],w)
actualAcceleration = arm_MCG(q,dq).M \ (tau-Cdq-G)
residualOrder = [l4,l5]
residualDefinition = diag(IVAL[4:5])*nominal_f(q,dq,w)[4:5]
                     - Mref*actualAcceleration[4:5]
MrefDefinition = diag(Float64(CSV[4,4]),Float64(CSV[5,5]))
massRegularizer = source literal 1e-6
coriolisGravityFDStep = source literal 1e-5
runtimeSemantics = Julia Float64 DH-chain + central FD C/G + linear solve
referenceKey = MISSING
qbarB = MISSING
vbarB = MISSING
lbar = MISSING
actualReferencePairing = MISSING
```

M0 CSV 无 header；上述 `[4,4]` token 为 `0.116667666666667`，`[5,5]` 为
`0.05018475`。按 decimal-exact 解释，第一项是
`116667666666667/10^15`，并非理想 `350003/3000000`，两者相差 `1/(3*10^15)`。
部署代码却读取 Float64；decimal-exact、理想 rational 与 binary64 三种解释不得混用。
本轮未运行 Julia parse/solve，也未生成其运算误差 receipt。

在“源字面常量作理想实数解释”的层次，descriptor 的 force normalization 为：

```text
Mref*aB + D*vB + K*qB = g*w - l
D = diag(4/5,13/20)
K = [[3/4,-1/100],[-1/200,29/50]]
g = [1/5,1/10]
```

这是 normalization 对照，不是 Float64 运算的逐步等式证明。注意本 source 的
`nominal_f` 不是最终 `a_nom`：零 force residual 的 acceleration 应是
`Mref^{-1}*diag(IVAL_B)*f_B`。因此 `ddq_exact-ddq_nominal` 即便使用这个相同
nominal acceleration，也等于 `-Mref^{-1}*l`，不是 l；旧 MATLAB cubic nominal
更不能直接套用这个换算。`lbar` 必须使用相同两维 force 顺序、符号和 Mref。

## 3. 精确 missing-field obstruction

| 必需字段 | 当前缺口 | 最小可接受补件 |
|---|---|---|
| qbarB | 无 nominal 两坐标实例或函数，actual q4/q5 不能改名顶替 | 指定 reference 的函数/数据及 pointwise 时刻；若采样数据，注明插值/区间语义 |
| vbarB | 无 nominal 速度；debug vbar2 类型错误 | 同 reference 的两个速度分量；若接轨迹定理，还需 vbarB=d(qbarB)/dt 的证明/receipt |
| referenceKey | 无可解引用的 reference 对象、选择记录和配对键 | 明确对象及内容 hash、初值/选定规则、时间域、forcing key；key 必须绑定内容，不只是标签 |
| lbar | 无 signed force residual 双分量或选定的零 residual 声明 | 同 descriptor 下 lbar 的定义/函数与 hash；理想零 residual 必须明示选择并证明对应方程 |
| common context | actual exporter 未保存 cw/w、remote 八坐标与 paired nominal | pointwise packet 补齐这些值或引用可信记录，时间/forcing/source/semantics 必须一致 |
| normalization | reference 侧未指定 Mref、误差方向、排列、单位和数值解释 | 与第2节精确同一对象，或单独给出有误差控制的转换，不接受近似相等 |

如果选择 ideal nominal reference，需要实际选定初值和同 forcing，再定义/构造对应
nominal solution；仅 `nominal_f` 和 Mref 不决定唯一 reference。若选择另一条完整
DH actual trajectory 作为 reference，lbar 还依赖其完整六维状态及同源 acceleration，
不能仅靠 qbarB/vbarB 算出。若只为 pointwise anchor，暂不需要 nominal ODE 存在性，
但仍需四坐标与其 context identity；后续 incremental dynamics 要额外验证 nominal 方程。

不能从 `l2` 恢复 lbar：即使 l2 属于 reference（现有文件并非如此），平方范数也丢失
方向/符号。不能跨 CSV 以 `sample=traj` 拼接：两种编号由不同 producer/seed 生成，
没有配对合同。不能将 `G0_ref` 或 M0 文件 hash 当作 referenceKey：它们分别是重力
补偿常量与质量参考，不指定 nominal position/velocity。

## 4. Hash provenance：匹配了什么，尚未绑定什么

2026-09-14 重新计算下面12个文件的 SHA-256，与暂停前读到的值一致。
manifest 的 `export_source_sha256, certificate_V_sha256, trajectory_output_sha256,
state_samples_output_sha256` 四条均与当前对应文件匹配。

这个 manifest 没有记录 dhport_lib/M0 内容 hash，也没有 nominal output hash。
本 review 记录当前依赖 hash 仅建立当前源快照，不能倒推这些依赖在历史运行时的字节，
更不能补出历史 nominal reference。exporter 与 residual-interface 是不同入口，
表达式静态相符也不是跨入口运行等价 receipt。

全部相对 S：

```text
routeB_descriptor_residual_interface.jl
D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24
dhport_lib.jl
AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936
routeB_Mq_M0.csv
28D98AD71D1D6C2CBE830872CAD9077F2F7B4E2D932794217EB68868FD2E2B40
routeB_descriptor_residual_interface.csv
ED10D0335DEBACD670A26871CAD9CE51FC871CB86F6AE956125AEAE3DEE00E24
routeB_export_traj.jl
35EBE806A46273068AF1AF937C0C0152378D6889024EC5586BF3C7AABD30ECCF
routeB_export_manifest.toml
5B61D624F4F6060DA8C33A51FA7982BEF8206D2C3924BABB512440DEFAD89187
routeB_state_samples.csv
AC0839DA41C789D0F951E814ECF7789E87E8EA1B423AE5520E404022A96B2191
routeB_traj_all.csv
634E9FF32CFCD91DB757F0942ADE8DE1F913C0A50DD0FEDB964AF9C09B53AF7F
routeB_certificate_V.csv
CAB4A5182981BCCBDE18ACE2D26ECE5C0D7B7D3C3CF4A5A7E02E7FCDA9B80601
debug_12e_nominal_v.jl
D2FBD18E6072B876C405B0DF7F1AFACDD7A44D258D1645CA1D657D93A953011B
debug_12e_nominal_v.csv
08EFB823497F983D973660C2F452AA9BD57EF39B5E5264A54F6579ADAAE3C739
routeB_compact_nominal_descriptor_interface.csv
AB36538B5AA9AB9B62012D2AB90A1E20E3A226110B97F95D5E9D270F0B5A0375
```

## 5. Handoff boundary

交付的是 missing-field obstruction 和可复查的 partial source identity，不是填充好的
reference packet。下一步需取得/明确选择实际 reference 对象及其同 forcing、同 normalization
的记录；不能由本审查擅自选择 zero reference 或设 lbar=0。

本轮只新增本 immutable review。无 state/registry/共享文件写入，无 Lean/Lake、Julia、
MATLAB、solver、producer、采样或回归运行；既有 CSV 只读字段/少量行及文件 hash。
没有 source binding、formal certificate 或 VERIFIED 声明。
