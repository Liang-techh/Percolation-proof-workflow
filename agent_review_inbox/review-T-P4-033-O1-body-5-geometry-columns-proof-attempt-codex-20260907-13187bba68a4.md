# O1 human body-5 G1/G2 source proof-attempt review

日期：2026-09-07。状态：`OPEN_UNCOMPILED_PROOF_SKELETON`。
human body 5 = zero-based body 4；本文 joint 5 = zero-based joint 5（human joint 6）。

## 交付与证据等级

新增 sidecar：
`examples/routeb_b45_source_comparator_lean/RouteBO1Body5GeometryColumnsProofAttempt20260907.lean`
SHA-256：`ef515a822e237ae30b90caec9c2d3b123671d351d37ac0c27f337d210960a11b`。

文件含 28 个带具体 tactic proof body 的 theorem 声明，消费已有
`RouteBO1Body5SourceTraceTargets`。本 review 将其归类为 **proof skeleton /
source proof attempt**：已有可审阅的推导结构、真实 source 绑定和证明代码，
但尚未通过 Lean parser、elaborator 或 kernel 检查。它不是 kernel proof；
声明写作 `theorem ... := by`、没有占位符，也不能替代 kernel acceptance。

| 层级 | 本轮证据 | 可作出的结论 |
| --- | --- | --- |
| 源码尝试 | 28 个声明及具体证明体；文本扫描 | 有待验证的实现，不能认为声明已经成立 |
| 精确代数诊断 | 一次 SymPy 1.14.0 有理/符号计算 | 转录模型的恒等式相符，不验证 Lean 文件 |
| Kernel proof | 未运行 Lean/Lake，未取得 proof term 检查结果 | G1/G2 及所有新叶仍 OPEN；不宣称编译或 VERIFIED |

## Source 叶与 G1/G2 接线

优先叶均直接量化实际 `sourceContract q`，不假设 `Body5GeometryTarget`：

- `origin_mul_step4_attempt` 对任意父矩阵 F 使用 step 4 的
  a4=d4=0；`source_o5_eq_o4_attempt` 经既有 source/frame accessor 接到 o5=o4。
- `origin_mul_step3_attempt` 对任意 F 使用 a3=0,d3=19/100；
  `source_o4_sub_o3_attempt` 接到 o4-o3=(19/100)z3。
- `source_com_eq_o4_attempt` 使用 body 4 的 COM endpoints 4、5。
  `source_v3_zero_attempt` 依赖上述平行位移及 cross(u,r*u)=0；
  `source_v4_zero_attempt` 依赖 COM=o4。二者的零值原因不同。
- `source_joint5_inactive_attempt` 使用真实 ancestor guard 4<5，
  同时处理 Jv/Jw；不把 source axis 5 设为零，也不把 active joint 4 当作 inactive。

`lift_sub_attempt`、`lift_cross_attempt` 和 `lift_isometry_attempt`
消费已有 `body5Lift`；cross bridge 保持右手方向。若临时以 c,s 表示
cos(q0),sin(q0)，cross 的残差仅第三分量为
(c²+s²-1)(u0*v1-u1*v0)，dot 残差为
(c²+s²-1)(u0*v0+u1*v1)。证明体尝试用既有三角单位圆恒等式消去它们。

G1 的前缀标量化限制在 slots 0..3；slot 4 的 origin/axis 使用单步引理，
slot 5 仅使用零平移，不计算其 orientation 或 source axis 5。
`body5_geometry_attempt : Body5GeometryTarget` 尝试提供全部
6 origins、5 parent axes 的真实 source witness，不新增 geometry 参数。

`local_cross_columns_attempt` 处理 5 个 active local cross。
`body5_geometry_to_columns_attempt : Body5GeometryToColumnsTarget`
以 geometry 前提接 COM、lift/cross 和 inactive guard，提供 G2 的具体证明体。
最终 `body5_columns_attempt : Body5ColumnsTarget` 使用本文件 G1 尝试消去该前提。
这是完整接线的无外加 geometry 前提尝试；其内部叶全部仍待 kernel 检查。
Lift isometry 只作为可复用叶提供，不声称完成 G3。

## 本轮检查与局限

一次 inline Python / SymPy 1.14.0 精确符号诊断通过：
6 origins、5 parent axes、o5=o4、o4-o3=(19/100)z3、
5 active local crosses，以及 lift cross/dot 的残差因式分解。
没有浮点采样。DH 参数、相位和目标公式根据绑定的 Lean 源码人工转录；
诊断不解析 Lean、不检查 tactic 是否成功。Joint 5 inactive 仅按 source guard
和现有 lemma 签名进行源码审阅，不将其记为 Python 执行的 Lean 证明。

文本检查发现 28 个唯一 theorem 名称；没有 sorry/admit/axiom 声明、
unsafe/native_decide/implemented_by；没有展开 fold 的引用或尾随空白。
这不是 parser、依赖或 axiom 审计，也不保证导入文件没有额外公理依赖。
13 个读取前固定的 input SHA-256 在写 receipt 前复核一致；
`git diff --name-only` 当时为空。另有其他任务新增的未跟踪文件，未触碰或纳入本 receipt。

尚未检查 import resolution、当前 toolchain/Mathlib 可用性、
Fin coercion 的 elaboration、宏展开、rewrite 匹配、norm_num/ring/
linear_combination 的执行与资源使用。这里只记录未检查项，不声称发现了编译错误。
没有修改构建配置，也没有发起本地或远程编译请求。

## 不变边界与后续入口

本任务只新增一个独立 sidecar 和本 review/配套 receipt。已有 target、
decomposition、主 adapter、其他 sidecar、generated evaluator、state/registry 均未改动。
没有展开 57-row fold，没有补 G3/G4、sourceBodyMass=piecewise、
trace equality 或 h_body_5；也不处理 O0/P-NE、数值执行器或覆盖证明。

G1、G2、lift bridge、isometry 的 admission status 全部保持 OPEN_UNPROVEN，
lean_compiled=false、kernel_checked=false、axioms_checked=false、
verified=false、registry_eligible=false、registry_promoted=false。
后续若另有授权验证，应先检查单步 source 叶，再检查 lift、bounded G1、G2，
保留同一输入绑定并另建 receipt；本轮不启动该流程。

本 review 与 receipt 使用内容 SHA-256 前 12 位命名，写入后设 Windows 只读。
未来修订另建快照。只读属性可撤销，不是 WORM；
内容哈希用于检测字节变化，不能证明数学结论。
