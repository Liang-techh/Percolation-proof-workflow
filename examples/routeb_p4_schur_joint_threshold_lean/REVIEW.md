# P4 Schur joint threshold：纯 Real 候选

状态：`OPEN_UNCOMPILED / pending`。未运行本机或远程 Lean/Lake；没有 parsed、
elaborated、kernel_checked、axioms_checked、compiled 或 VERIFIED 结论。

新增 `NEW_JOINT_THRESHOLD_20260908.lean`，namespace
`RouteBP4SchurJointThreshold`，7 个 theorem 候选。只按本次请求明确给出的恒等式
推导；没有读取或认证 revision 782 的外部源，也不把该编号当 source witness。

## 精确代数

假设 P=beta-L-2c-Q，则

```text
binding: E_A-Q ≤ P  iff  L+2c+E_A ≤ beta
target:  t ≤ P      iff  L+2c+t+Q ≤ beta
both                iff  L+2c+max(E_A,t+Q) ≤ beta
```

binding 中 Q 抵消；target 中 Q 保留。不能把联合阈值写成
L+2c+max(E_A,t)，也不能仅凭 binding 宣称 target 成立。
例如 L=c=E_A=beta=0、Q=1、P=-1、t=0，恒等式及 binding 均成立，target 不成立；
正确联合阈值要求 beta≥1。此处为精确纸面反例，未运行 Lean 证明该例。

所有变量均可为任意实数；不需要 L,Q,E_A,t 非负，不需要 c 的符号，尤其不能
无声地把 c 换成 |c|。`square_joint_iff` 只是 L=ell²、Q=q²、E_A=e²、t=z² 的
代入实例，不要求或声称所有应用中的 t 都能表示成平方。

## 候选接口

- `binding_iff`、`target_iff`：两个独立线性叶。
- `joint_iff_two_thresholds`：保留两个义务的合取。
- `joint_implies_max_threshold`：用 max_le 合并两个上界。
- `max_threshold_implies_joint`：用 le_max_left/right 拆出两个上界。
- `joint_iff_max_threshold`：组合两个方向。
- `square_joint_iff`：平方实例；无需 nlinarith 或展开平方。

显式 imports 为 `Mathlib.Data.Real.Basic` 与 `Mathlib.Tactic.Linarith`。
不导入项目 shared adapter，不使用完整 `import Mathlib`、decide/native_decide、
数值常量比较、matrix inverse、sqrt、PSD tactic 或有限枚举。
最小 API 风险是当前 pinned Mathlib 是否通过这些 imports 提供上述 max 引理，
以及 linarith elaboration；均未测试，不能称为已确认的最小依赖闭包。
Lean 会省略声明中未使用的 section 变量：binding_iff 没有参数 t，target_iff
没有参数 E_A；候选调用按这个显式顺序编写，后续应优先核对两个叶的类型。

## Admission 与写入边界

恒等式 hP、L/Q/c/E_A/t 的源含义、binding 对真实残差的充分性、target 的物理
含义及 coverage 全部在本候选范围外。即使未来编译成功，也只是接受给定假设下
的标量等价式，不自动证明 Schur 正性、物理域或 registry eligibility。

仅新增本目录候选和本 REVIEW.md；没有修改 state、registry、已有 Lean 或共享
脚本，没有创建 toolchain/lake 配置或编译产物。检查时工作流 HEAD 为
`2fd011fa6ffdc61f5167cf715d4c7e2453994178`，不是候选已提交的声明。
