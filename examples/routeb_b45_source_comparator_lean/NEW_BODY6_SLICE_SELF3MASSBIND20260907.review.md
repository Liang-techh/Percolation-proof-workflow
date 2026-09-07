# Body-6：SELF3 Gram 到前三列质量块 A 的绑定

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明内核验证、完整矩阵或 registry admission。

新增 `NEW_BODY6_SLICE_SELF3MASSBIND20260907.lean`（105 行）及本定向 review。
直接导入 `SOURCEBLOCKBIND` 和 `SELF3_Source` 对应的 20260907 模块。

## 核心结论与证据分层

SELF3 的 Gram/geometry 单独不等于质量条目。
但当前代码还提供明确的 `source_mass_gram_attempt`：实际 body-6 的质量条目等于
`(3/20) * velocity Gram + (1/60) * axis Gram`。
因此，在中心偏移与实际权重绑定前提下，组合这些接口能条件式覆盖前三列 A 的**全部九项**，不需要凭空添加独立质量数值表。

新 `SelfMassAdapter m kappa : Prop` 显式分开四个字段：

| 字段 | 提供的证据 | 来源 |
| --- | --- | --- |
| `weightBinding` | 实际 body-6 质量、已除惯量分别等于 `m,kappa` | `SourceWeightsTarget` 前提 |
| `massLaw` | 每个实际 `sourceA` 条目等于加权的两个实际 Gram | 已有 `source_mass_gram_attempt` 加权重转换 |
| `velocityGram` | 实际前三列速度 Gram 等于 SELF3 速度表 | `source_self_velocity_attempt hc` |
| `axisGram` | 实际前三列 axis Gram 等于 SELF3 轴表 | `source_self_axis_attempt` |

`self_mass_adapter_attempt` 消费 `CenterOffsetTarget` 与实际权重绑定，构造这四种证据。
mass law 是独立字段，不是把 Gram 结论改名为质量条目。
底层消费者接收上述证明项包；中心偏移经 velocity Gram 证据传递，上层构造器仍明确要求中心偏移前提。

## 六项独立公式与九项 typed 覆盖

body 固定为 `(5 : Fin 6)`，即通常编号的 body-6。
`i,j : Fin 3` 均经既有 `firstJoint` 映射到实际关节 `{0,1,2}`；`q : Fin 6 → ℝ` 任意。

令 `a,b,p,r,u,v` 分别为既有 `coeffA/coeffB/coeffP/coeffR/coeffU/coeffV q offset`。
这些量保留真实几何和 `offset = 7/200`；本叶不重新展开或证明这些几何表达。

定义 `weightedA = m * selfVelocityEntry + kappa * selfAxisEntry`，其显式表是

\[
\begin{pmatrix}
m(a^2+b^2)+\kappa & -map & -mau\\
-map & m(p^2+r^2)+\kappa & m(pu+rv)+\kappa\\
-mau & m(pu+rv)+\kappa & m(u^2+v^2)+\kappa
\end{pmatrix}.
\]

| 独立索引 | 加权质量表达 | 不能遗漏的内容 |
| --- | --- | --- |
| `(0,0)` | `m*(a²+b²)+kappa` | 速度项乘质量，另加惯量 |
| `(0,1)` | `-m*a*p` | axis Gram 为零不使速度项为零 |
| `(0,2)` | `-m*a*u` | 同上 |
| `(1,1)` | `m*(p²+r²)+kappa` | 惯量贡献 |
| `(1,2)` | `m*(p*u+r*v)+kappa` | 非对角项也有惯量贡献 |
| `(2,2)` | `m*(u²+v²)+kappa` | 惯量贡献 |

`explicitWeightedA` 存放完整九项，`weighted_table_attempt` 逐项连接加权定义与显式表。
`weighted_A_binding_from_adapter_attempt` 将 mass law 中的两个实际 Gram 改写为 SELF3 表，得到 `FirstBlockBindingObligation q (weightedA ...)`。
`explicit_A_binding_attempt` 再将其连接到显式九项表。

该绑定只使用质量／惯量加权恒等式，不需要另加正性前提。
其实际权重由 `SourceWeightsTarget` 限定为 `m=3/20`、`kappa=1/60`；`kappa` 已是约定的已除惯量，不再乘质量或重复除以 3，也不加入总矩阵正则项。
后续逆块或 Schur 求解仍需各自原有的符号前提。

## 哪些条目仍缺独立见证

对于本叶定义的规范加权表，在适配器前提下没有剩余的逐项质量绑定缺口：全部九项均被条件式覆盖。
这不是无条件证明；中心偏移、实际权重绑定及导入 proof attempts 的 Lean 验证仍未完成。

对于另行提供的任意候选 A，全部相关条目的候选恒等式仍需证明。
新义务 `CandidateMassIdentity q m kappa A` 明确要求 `∀ i j, Aij = weightedA q m kappa i j`。
`candidate_binding_iff_mass_identity_attempt` 在 `SelfMassAdapter` 下证明它与原 `FirstBlockBindingObligation q A` 等价。

这给出定向 obstruction：缺少候选恒等式见证时，不能自动接入独立 A。
即使候选自称对称或只给六项，仍需适当证明才能满足 typed 的九项绑定；本叶不替候选补齐假设。
缺少见证不等于已经发现错误。`candidate_mismatch_rejects_attempt` 只在存在具体不等式证明
`Aij ≠ weightedAij` 时，才拒绝该候选的实际 source 绑定。

## 接回 SOURCEBLOCKBIND

`explicit_A_mixed_source_binding_attempt` 在同一中心偏移和权重绑定前提下，使用
`explicit_A_binding_attempt` 填写旧 `mixed_binding_from_A_attempt` 的 A 字段。
返回的是规范加权 A 与已有 `mixedX/mixedY` 的 `SourceBlockBinding`，未构造完整矩阵或 Schur PSD 结论。

原来“任意候选 A 仍需绑定”的义务保持有效；本叶只为这里明确给出的加权表提供了新的条件式见证。

## 定向检查与开放边界

只执行一次小型 Python/SymPy 精确代数检查：将 SELF3 的六个几何系数视为自由符号，检查
`m*velocityTable + kappa*axisTable` 与新九项表的差，九项均为精确零。
另确认原速度 Gram 与加权质量表达并非一般恒等，尤其 `(1,2)` 项保留 `kappa`。
这是自由符号的代数核对，没有伪造机器人配置或 source 数值，也不证明几何绑定。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
未执行 Lean/Lake、旧 Gram/Fourier 检查或大回归，未修改共享脚本、旧叶、state 或 registry。

sidecar 实际字节 SHA-256：
`1b198a0846bc118042741410a488e5f9eefbf9dcb50b709d15a44b37b47b53ab`。

仍未闭合：独立候选 A 的质量恒等式、无条件中心偏移／权重见证、导入和新增 Lean 脚本的内核验证、完整 Schur PSD、Fourier、coverage 与 registry admission。
