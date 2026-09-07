# T-P4-032：weighted three-term 平方预算与 defect 类型

日期：2026-09-07。新增 `NEW_P4_032_WeightedThreeTerm.lean` 与本 review。
状态：**source-independent、未编译 skeleton**。未运行 Lean/Lake、数值或 source checker，
未修改旧文件、state、registry 或共享脚本；未重做 scalar triangle 或 quadratic-load 消费。

依据：`agent_review_inbox/review-T-P4-032-defect-quadratic-liuguanyi-20260907T1306.md`。

## 加权平方接口

`Weights` 固定 Fin 3 顺序为 `(u,D,B)`，要求三个权重严格为正且倒数和不超过 1。
`reciprocal_iff_polynomial` 给出带正性前提的确切等价：

```text
1/λu+1/λD+1/λB≤1
iff λD*λB+λu*λB+λu*λD≤λu*λD*λB。
```

`ofPolynomial` 消费右端无除法条件，同时保留全部三项严格正性证明。
不能在零/负权重时只检查多项式便宣称倒数条件成立。

`weighted_scalar` 通过既有有限和 Cauchy lemma，使用系数
`fᵢ=λᵢ*xᵢ²`、`gᵢ=1/λᵢ` 得到 `(Σxᵢ)²≤Σλᵢ*xᵢ²`。
随后 `weighted_three_term_norm_sq` 按向量坐标求和，目标是：

```text
||u+v+w||₂² ≤ λu*||u||₂² + λD*||v||₂² + λB*||w||₂²。
```

这是任意有限维 `Fin n→ℝ` 的 **Euclidean ℓ₂** 版本，足以覆盖 Route-B 的 n=2。
`norm2_sq_sum` 显式连接 `WithLp.toLp 2` 与坐标平方和；本轮没有扩展到任意无限维
Hilbert space，也没有形式化权重条件的必要性定理。证明路线不使用 scalar triangle cap，
不需要为有理预算选取平方根或构造数值权重。

## Route-B typed budget

`routeB_port_defect_quadratic_budget` 接受同一组向量的身份和平方预算：

```text
rB=u+v+w， ||u||₂²≤rhoA*energy， ||v||₂²≤UD， ||w||₂²≤UB，
```

得到 `||rB||₂²≤λu*rhoA*energy+λD*UD+λB*UB`。
这里端口 energy 的模型/单位身份仍需外部证明，不能仅凭变量名推断它是实际 metric。
预算值的非负性由对应平方上界前提蕴含；若另作 relative/additive 参数化，其参数
符号和域条件属于下一层接口，本轮未自动构造。

`action_squared_budget` 复用前轮 `ActionBound` 和安全平方界：给定 tau≥0 的作用界
及 `||eD||₂²≤ED`，得到 `||T*eD||₂²≤tau²*ED`，不计算 sqrt(ED)。

新建不同结构类型，分别固定不同算子：

| 输入类型 | distal port 分量 | 所需 ActionBound |
|---|---|---|
| `DistalForceDefect` | `(MBD*J)*eD.value` | MBD*J 的 tau 界 |
| `DistalAccelDefect` | `MBD*eD.value` | MBD 的 tau 界 |

`force_defect_budget` 与 `accel_defect_budget` 均输出
`||rB||₂²≤λu*rhoA*energy+λD*tau²*ED+λB*EB`，但 identity 和 action-bound 类型各不相同。
它们保留端口加速度、generalized-force residual 与 local port defect 的结构标签，
不允许仅凭相同 DVec 形状自动选择是否多乘一个 J。

`force_accel_term_identity` 只有在另给精确 `ea.value=J*ef.value` 时才连接两个分量。
backward residual `rhs−M*a` 的符号、forward acceleration error 的参照解、J 的真实身份
不能从这个转换条件中推断。每个 typed budget 的完整 `rB=u+v+w` 仍是外部证明参数。
在 O1 特化时 R 应识别为既有 Rport，J 的左逆和 balance 前提在上游 identity 中处理。

## 边界与剩余前提

这条加权界直接消费不同平方预算，并不声称优于仅给三项标量 cap 时的
`(cap_u+cap_D+cap_B)²` 最坏情形。没有提供未经权重 gate 的无系数平方和界。

尚需：真实正权重/gate 证明；同一 source 状态、regularizer/key、域、B/D 顺序和
generalized-force normalization 下的 identity、port energy、作用界及 defect 平方预算；
source solver diagnostic 与 force/acceleration defect 类型的精确身份。
质量块乘加速度已经产生 generalized force，本文件不再次应用 raw-PMI normalization。

所有接口均为条件式。结构标签不认证包装的数据；全域有效性要逐点提供同域前提。
本文件及导入的 skeleton 尚需 elaboration/kernel 与公理检查。末尾 `#print axioms`
没有执行输出，不声称编译、source binding、coverage、P4/P5 closure 或 registry admission。
