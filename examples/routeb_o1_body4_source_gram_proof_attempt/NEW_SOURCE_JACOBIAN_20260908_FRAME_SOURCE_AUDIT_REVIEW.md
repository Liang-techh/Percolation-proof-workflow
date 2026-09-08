---
task_id: GH-MATH-P4-O1-BODY4-FRAME-HANDOFF
status: HASHED_SOURCE_DATA_FOUND_EXACT_TARGET_INHABITANTS_NOT_ESTABLISHED
integration_status: pending
admission: pending
source_binding_proven: false
lean_lake_run: false
---

# Body-4 frame handoff — 同源数据与 inhabitant 缺口

结论：找到已有哈希关联的 exact Fourier generator / Julia DH 快照及一致的
Lean frame 定义；没有找到足以把 FRAME_HANDOFF 两个前提认定为已闭合的证明证据。
不是“缺少 DH 数值”，而是“具体 frame 列恒等式的认证 inhabitant 未建立”。
已有 proof-attempt 文本可以作为后续验证候选，不可当作当前已验证 theorem。
本轮仅新增此 review，未创建 sidecar、未执行生成器、符号检查或 Lean/Lake。

## 1. Source identity：当前检查与不能混同的哈希

原 `O1_BODY_4_SOURCE_GRAM_TARGETS_RECEIPT.json` 与
`O1_BODY_4_SOURCE_BRIDGE_RECEIPT.json` 同用：

`routeb-exact-fourier-mass:a986a208b62f585c6ca1b9c81b958710d2043e5bf786ddc930a6fa29f7a232b8|mu=1/1000000|contract=exp(i*nu*q)`。

本轮重新计算 `artifacts/task_routeb_body_trace_sink_current/source_snapshot/`
内三个文件的 SHA-256，均与其 `outputs/manifest.json` 记录一致：

| 角色/文件 | 实测 SHA-256 |
|---|---|
| frozen aggregate / routeB_fourier_mass_full_rational.csv | A986A208B62F585C6CA1B9C81B958710D2043E5BF786DDC930A6FA29F7A232B8 |
| exact generator / routeB_fourier_rational_probe.py | 9460181770E47BE0ECBDE43A8A29EF285DA1168C3121FAB18D5378C671401A7B |
| Julia snapshot / dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |

`a986...` 是 aggregate 字节身份，不是 frame 数据证书或 Julia source hash。
manifest 的 `BOUND_TO_HASHED_ARTIFACT_COPY` 与 `PASS_EXACT_FOURIER_COPY`
只记录该副本/trace 工作的范围；它明确保留 Julia runtime OPEN。
本轮没有重新验证外部 live canonical 文件，不能把 snapshot identity 当作其当前状态。
`mu` 是 mass post-loop regularizer，不进入任何 body 的 frame、COM 或 Jacobian。

还重新核对以下六个当前 Lean 文件，均匹配原 body4 targets receipt 的 evidence 哈希：

- PerBodyExactSource：C09B84677ADEF121488B3CEB53E886D0EF0B028C7979D91F8A7F9BA0FBFCD553。
- FourierNormalForm：56EC2F2D29A22942BCB83A3BA98197AE1CE4D607340072B81C013B8D358D3218。
- RealDHStep：9C04DA5B9627EE749C53009733006934F95B2D33265E46CA59D0725AA453786A。
- FrameSlotAccessor：F497BD1F45FAE4DD385F4D0F46DF79252C92E5CD027B29D5DC55011F91525C31。
- SourceContractAdapter：58C0B15B6FCEB1064F773ACDB9F684DC55A021AC69A030C13E1C8B46F7B9A8DC。
- SourceContractIndexAdapter：2A18C7B6733AF6245F3E5BA6DEDD714A9EC7F28FD010122C0258611CE7AAC452。

这些匹配只排除所列字节漂移，不是完整 import closure / cross-language 证明。
审计对象 FRAME_HANDOFF 实测：
8EBF458E0812B63A911EE4EB64A5A621D6F1ACA074EB7950D7746BEA09A64512。

## 2. 已找到的逐字段上游数据

generator 的 DH_OFF/DH_D/DH_A/DH_ALPHA（行 19–22）与 Lean
FourierNormalForm 对应参数定义（行 59–98）在本次文本核对中一致：

| zero-based step | offset / (pi/2) | a | d | alpha / (pi/2) |
|---|---:|---:|---:|---:|
| 0 | 0 | 2/25 | 1/10 | -1 |
| 1 | -1 | 21/100 | 0 | 0 |
| 2 | 1 | 0 | 1/20 | 1 |
| 3 | 0 | 0 | 19/100 | -1 |

这里列出的是已有数据审阅，不是新增常数作为 target inhabitant。
Julia 行 6–11 的十进制/pi 表对应同一意图，但 Float64 运算不是这些精确实数恒等式。

- 初始 frame：generator `Tc=[eye()]`；Julia `Tc=[Matrix{Float64}(I,4,4)]`；
  Lean `prefixFrame ... 0 = 1`。
- 乘法方向：generator 行 126 为 `matmul(Tc[-1], A)`；Julia 行 40 为
  `Tc[end] * A`；Lean accessor 保留 `((I*T0)*T1)*T2` 的左结合。
- 父轴：generator 行 125 在 append 当前 step 前读取 `Tc[-1][k][2]`；
  Julia 行 36 同样先读取父轴。Lean `source_parent_axis_slot` 使用 `prevOrigin joint`。
- 平移：generator A 的最后一列是 `(ct*a,st*a,d,1)`，step 3 的已有参数
  给出候选 `(0,0,19/100,1)`；RealDHStep 行内定义同形。
- 输出限制：现有 trace/aggregate CSV 的 schema 是 body/mass/Fourier 系数，
  没有 slot、spatial-row、frame-column 或 frame-expression 字段。
  generator 内部确实计算 Tc/origins/axes，但该 manifest 未列出认证 frame 列导出。

## 3. 两个 target 的字段缺口

记 `V(r,t,z)=vec q r t z`、`phi=q 1+q 2`，b/c/d 沿用原 target 定义。
`Body4PrefixColumnsTarget` 要求所有 q、四个 slots、三个 spatial rows、四个 columns
的 48 个标量等式，而不只是 Z/O。原目标右端逐列如下：

| slot | X | Y | Z | O |
|---|---|---|---|---|
| 0 | (1,0,0) | (0,1,0) | V(0,0,1) | 0 |
| 1 | V(1,0,0) | V(0,0,-1) | V(0,1,0) | V(2/25,0,1/10) |
| 2 | V(sin(q1),0,cos(q1)) | V(cos(q1),0,-sin(q1)) | V(0,1,0) | V(2/25+b,0,1/10+c) |
| 3 | V(cos(phi),0,-sin(phi)) | V(0,1,0) | V(sin(phi),0,cos(phi)) | V(2/25+b,d,1/10+c) |

逐字段共同缺口：`routeBFrameSlot q slot (embed3 a) col` 到上表各函数的
认证等式；slot 0 仍需处理世界基与 vec 零分量，slots 1/2 需具体 DH 归约，
slot 3 需正确 offsets、乘法次序及 angle-addition。没有从 CSV 提供这些字段。
FRAME_HANDOFF 实际只消费 Z/O 的 24 个等式，但输入沿用完整 48 等式 target；
不能静默声称只证明 Z/O 已满足原 target 的 X/Y 字段。

`Body4Slot4TranslationTarget` 要求所有 q、三个 spatial rows：
`origin(F4) a = origin(F3) a + (19/100)*zAxis(F3) a`。
其最短候选依赖按字段为：

1. `F4=F3*T3`：accessor 定义确实具有所需结构；只是结构，不是具体列恒等式。
2. `T3 k 3` 的四个 entries：0、0、19/100、1；已有 source 定义和
   `step3_translation` 候选脚本，缺少针对当前 import 闭包的认证证明结果。
3. 三个 spatial rows 的 `Matrix.mul_apply` 有限和归约，匹配 origin/zAxis 的
   `embed3` 索引；已有 `slot4_translation` 候选，缺少同环境编译/axiom 证据。

原 `RouteBO1Body4SourceGramProofAttempt.lean` 行 85、106 有两个 exact target
的候选声明；20260907 BODY4_BRIDGE 行 149 有 translation 候选，其 prefix 则只
分别给出 origin/axis 候选，不能直接作为完整 PrefixColumnsTarget 的 inhabitant。
没有找到这些 exact target 的成功编译 receipt。原 targets receipt 自身明确
`OPEN_PROP_DEFINITIONS_NO_INHABITANTS_UNCOMPILED`；其 273 项 SymPy 检查
手工镜像参数，不解析 Lean，不证明 transcription/source binding，本轮没有重跑。

## 4. 索引和不可拼接证据

human body4 = zero-based Body 3；Julia ii=4 对应 Python i=3。
COM 取 Lean/Python slots 3、4，即 Julia origin columns 4、5。
human joint4 = active joint3：其 parent axis 来自 slot3（Julia z column4），不是 slot4。
位移为 `(19/200)*Z3` 时 Jv 由平行叉积为零，Jw 仍为 Z3。
inactive 仅 joints 4、5，不能将 Jv 的零误写为 joint3 inactive。

- FrameSlotAccessor FINAL_RECEIPT 历史记录报告 slot/list 结构桥成功，且明确
  DH entries 保持 opaque、Float64/full-mass open；不是这 48+3 个几何等式的证明。
- AgentFrameTransport 历史 receipt 是 generic homogeneous-step 条件下的七槽形状，
  不导入实际 DH/accessor；不能提供具体 Z3、O3 或 step3 translation。
- minimal frame-prefix RESULT 记录 pure shape 成功但 concrete adapter/import timeout；
  不能从 pure shape 的 olean 推出具体 target。上述均为读取历史记录，不是本轮重验。
- 局部 Gram/质量 Fourier trace 丢失定向 frame 信息，不能反推出轴、原点或叉积。
- lift 的 dot 保持与 oriented cross 运输分开；均不替代 source geometry。
  两个 exact targets 对所有 q 量化；receipt 的 qcell state_key 只是 provenance，
  不能用某 qcell 数值样本或另一 body 的几何证明拼接。

## 5. 最短下一步与本轮边界

先在未来授权的一致 pinned 环境核验 step3_translation + slot4_translation 候选，
可先闭合 active joint3 的较短 Jv 分支；再核验原完整 prefix_columns 候选，或另行
明确授权改接口只消费 Z/O（本轮没有修改接口）。收集确切 target 类型、源码/import
哈希、工具链/Mathlib 身份、退出码及 axiom 输出后，才可消费 FRAME_HANDOFF。
若还要跨到 hashed generator/Julia 语义，另需对应 source 解析/语义桥；字节匹配不等于它。

定向搜索范围：examples 与 artifacts 中相关 Lean/receipt（排除 runtime/state 内容），
以及 body-trace snapshot/manifest。没有全机“证据不存在”的断言。
本轮仅静态读取、哈希检查和新 review 写入；不跑本机 Lean/Lake/全回归，不声称 VERIFIED。
没有修改 state、registry、旧 artifacts、共享 adapter 或其他 agent 文件。
