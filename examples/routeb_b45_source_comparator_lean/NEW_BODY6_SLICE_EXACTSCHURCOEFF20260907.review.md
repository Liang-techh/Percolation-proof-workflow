# Body-6：source-to-Schur 逐项精确系数接口

状态：**UNCOMPILED PROOF ATTEMPT**。未运行 Lean/Lake，不声明自动 source margin、完整矩阵 PSD、coverage 或 registry admission。

新增 `NEW_BODY6_SLICE_EXACTSCHURCOEFF20260907.lean`（98 行）及本定向 review。
唯一直接 import 为 `MARGINUNIFORM20260907` 对应模块，继承既有 source 绑定、余项和 margin 接口。

## 记号与类型边界

为避免把不同 S 混用，本叶记 tail 方块为 `B = sourceTail q`、其条件式逆为 `D = inverseTail ...`。
因此所需余项是 `R = A − X*B⁻¹*Y = A − X*D*Y`。
旧 `solvedRight` 中的 S 表示 `D*Y`，类型为 `2×3`，不是应当再求逆的 tail 方块。

A/R 为 `3×3`，X 为 `3×2`，Y 为 `2×3`。front 索引为 `{0,1,2}`，tail 顺序为 `{3,4}`；body 索引 5 表示通常编号的 body-6。
`q : Fin 6 → ℝ` 任意，`q 4` 使用从 0 开始编号，`offset=7/200`。

## 逐项 source 系数

`sourceCoefficient q m kappa i j` 明确定义为

\[
M_{f_i f_j}
-\frac{M_{f_i t_0}M_{t_0 f_j}}{\kappa+m\,offset^2\sin^2(q\,4)}
-\frac{M_{f_i t_1}M_{t_1 f_j}}{\kappa+m\,offset^2},
\]

其中 M 是实际 `sourceBodyMass q 5`，`fi = firstJoint i`，`t0=3,t1=4`。
这是实际条目的符号表达，没有注入新的测量、CSV 或 cross-block 数值。

`ExactSourceEntries q m kappa R` 要求全部九项 `Rij = sourceCoefficient ... i j`。
在 `SourceBlockBinding q A X Y` 下，`exact_entries_iff_remainder_attempt` 尝试证明它与
`∀ij, Rij = schurRemainder ... A X Y i j` 等价。
该 iff 消费旧 `bound_remainder_coefficient_attempt`，不重新推导有限和或质量表。

纯系数等式没有断言分母已可逆；有效逆块语义由下述契约的 tail 证明包独立提供。

## 精确契约及 uniform consumer 连接

`ExactSchurCoefficientContract` 保存：

1. 实际 A/X/Y 的 `SourceBlockBinding`；
2. `SchurRemainderContract`，包含实际 tail 的正分母、两侧逆和列求解义务；
3. R 的 `ExactSourceEntries`。

`exact_source_contract_attempt` 明确要求中心偏移、实际权重绑定、`kappa > 0`、`m ≥ 0`、
`offset² ≥ 0`，以及候选 A/X/Y 绑定和候选 R 的余项恒等式。
它不要求或构造 margin。

`uniform_margin_with_exact_seam_attempt` 另行消费域 D 上的精确契约家族和
`UniformMargin D R mu`，将二者组装为同一 mu 的 `SourceSchurMarginContract` 家族。
这个结果可交给已有 `uniform_residual_consumer_attempt`。
两个输入互不替代：uniform margin 不能填补精确系数字段，精确 source 系数也不能自动填补 margin 字段。

## 对称性究竟来自哪里

`exact_entries_symmetric_attempt` 从实际 source 的质量对称性取得 `sourceAij = sourceAji`，
从已有 `source_y_transpose_attempt` 取得 `sourceYaj = sourceXja`。
将这些等式代入精确 R 系数后，用实数乘法交换律得到 `Rij=Rji`。

因此一旦 R 的实际逐项绑定成立，这里不再独立要求 R 对称性见证。
这个结论没有仅凭 uniform margin 推断 cross-block 系数，也没有从 A 的 SELF3 绑定推断 X/Y。

对于未完成 source 绑定的外部块，需要独立证明其相应条目身份；若采用一般抽象对称 Schur 论证，还需相应 A 对称、Y=Xᵀ 等假设。
`RemainderMargin` 的确包含候选 R 自身的对称性，但这不能倒推出 A/X/Y 的条目或转置绑定，更不能确定 R 的具体系数。

## 精确 obstruction 反例

`uniform_margin_not_coefficient_identity_attempt` 是抽象矩阵反例，明确不代表 body-6 source 数据。
取抽象 `A=I₃`、`X=Y=0`、`D=I₂`。则确切余项为 `I₃`。
常值族 `R₁(q)=I₃` 和 `R₂(q)=2I₃` 在整个配置空间上都对称且具有统一 margin 1。
但候选 `R₂` 的 `(0,0)` 条目为 2，而余项系数要求为 1。

代码中的 `z=h=m=0,kappa=1` 仅用于该抽象标量逆表达的实例化，未声称符合实际 body-6 权重绑定。
这个反例说明 margin／对称性信息不足以确定余项等式，不能当作实际机器人存在系数错误的证据。

`coefficient_mismatch_rejects_attempt` 则提供定向拒绝接口：只有取得某项
`Rij ≠ sourceCoefficientij` 的真实证明，才能拒绝相应 `ExactSourceEntries`。
缺少绑定证明仍是待证明义务，不等于已经发现数值不匹配。

## 仍需外部提供的内容

- 对任意候选 A，SELF3MASSBIND 仅为规范加权表提供条件式绑定；其他 A 仍需候选质量恒等式。
- X/Y 必须具有正确的实际 mixed 条目与方向绑定；A 的质量绑定不能填补这两块。
- 候选 R 必须具有逐项余项／source 系数恒等式，不能仅提交 PSD 或 uniform margin 证明。
- 合法逆的中心偏移、实际权重与符号前提仍由 source 构造器消费；未构造无条件见证。
- 域内统一 margin、配置域覆盖、Lean 验证及 registry admission 不由本系数接口产生。

## 定向检查

一次小型 Python/SymPy 精确符号检查：在自由对称 A 与 `Y=Xᵀ` 下，
`A−X*diag(1/p,1/r)*Xᵀ` 与其转置的九项差均为零；另核对抽象反例中 `(0,0)` 的 2 与 1 不相等。
这些是符号／抽象矩阵检查，不验证实际 source 数值或 source 几何。

静态检查确认直接 import 文件存在，新 sidecar 未见 `sorry`、`admit`、`axiom` 或 `opaque`。
没有运行 Lean/Lake、旧数学检查或宽回归，也没有修改 StateStore、registry、共享脚本或既有叶。

sidecar 实际字节 SHA-256：
`0d48dc828ba8a025ca409ddc8ddc49fbd5450955a66bb060683ec1b3fa14a444`。

全部结论保持 proof-attempt／条件式边界，不声明完整 `5×5`／6DOF PSD、Fourier、coverage 或内核验证。
