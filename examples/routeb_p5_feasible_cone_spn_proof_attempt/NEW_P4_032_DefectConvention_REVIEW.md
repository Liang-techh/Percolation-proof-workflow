# P4：force-side 与 O1 defect convention 的 typed adapter

日期：2026-09-07。新增 `NEW_P4_032_DefectConventionCore.lean` 与本 review。
**未编译、source-independent skeleton**；未运行 Lean/Lake，未做 PSD、范数、数值、
coverage 或 registry 工作，未修改旧文件、state 或共享脚本。

新文件只依赖已有 SchurElimination/BlockDefects 声明，未重写消元证明。
`ForceSideDefects` 与 `O1Defects` 是不同结构类型，没有隐式 coercion。

## 1. 能连接整套 balance 的转换

固定同一 M、aB，并记 `J=MDDinv`、`T=MBD*J`。force-side 约定是：

```text
MBB*aB+MBD*aD=FB+epsilonB，
MDD*aD+MDB*aB=FD+epsilonD。
```

另外显式选择参考加速度 aD0、参考块 MDB0。`adapt` 定义：

| O1 变量 | 精确转换 |
|---|---|
| delta_aD | aD−aD0 |
| DeltaMDB | MDB−MDB0 |
| rB_O1 | FB−MBB*aB−MBD*aD0 |
| dO = eD_O1 | FD+epsilonD−MDD*aD0−MDB0*aB |
| bO = eB_O1 | −epsilonB |

`balances_iff` 的候选结论是原两条 force-side 方程与以下两条 O1 方程双向等价：

```text
MDD*delta_aD + DeltaMDB*aB = dO，
rB_O1−MBD*delta_aD = bO。
```

这个变量代换本身不需要 inverse。aD0/MDB0 是显式数学参数，不被声明为实际
reference source；rB_O1 是表中定义的变量，不自动等于任何另外命名的部署 residual。

若还提供 reference distal balance
`MDD0*aD0+MDB0*aB=FD0+epsilonD0`，`adapted_distal_with_reference` 给出：

```text
dO = (FD−FD0)+(epsilonD−epsilonD0)−(MDD−MDD0)*aD0。
```

因此 reference force/defect 和质量块变化均不能因为选择了参考量就自动删除。

## 2. Condensed identity 的精确等价

保留显式左逆 `J*MDD=I`、矩阵乘法顺序及同一个 T。定义：

```text
forceRHS = (FB−T*FD)+(epsilonB−T*epsilonD)，
o1RHS = Rport(MBD,J,DeltaMDB)*aB + T*dO+bO。
```

`condensed_residual_identity` 比两个命题等价更强，其目标是以下向量残差恒等式：

```text
rB_O1−o1RHS = forceRHS−Schur*aB。
```

它用左逆消去 reference acceleration 项；矩阵动作按原顺序展开，只在取分量后
用标量环运算。`condensed_iff` 因而连接 `Schur*aB=forceRHS` 与 `rB_O1=o1RHS`。
`o1_from_force_balances` 实际调用既有 `port_identity_with_defects`。

若已有一个独立 O1 record，`identified_condensed_iff` 必须另外接收
`o = adapt(...)` 的精确变量身份。字段同名、向量形状相同或共享某个 defect 值，
都不满足该参数。这里没有任意 O1 record 与任意 force-side record 的无条件等价。

## 3. 仅比较 correction 两项时的附加条件

不要将上一节整套变量转换简化成 defect 的单独重命名。对于独立 f/o，
`corrections_equal_iff` 的候选充要条件是：

```text
epsilonB−T*epsilonD = T*dO+bO
  iff T*(epsilonD+dO)=epsilonB−bO。
```

这允许 T 的核空间及两个 port 项相消，不强制逐个 defect 为零。
`correctionOnlySignFlip` 取 `dO=−epsilonD,bO=epsilonB`，确实匹配 correction 向量，
但它**不是** `adapt`，不能据此推断两套 balance、rB 或名义 forcing 部分一致。

若把两个 defect 值原样复制，即 `dO=epsilonD,bO=epsilonB`，
`unchanged_values_iff` 给出 correction 相等的充要条件 **T*epsilonD=0**。
所以原样复制一般不成立；也不能把这个条件误写成 epsilonD=0，因为 T 不一定单射。

## 4. 精确剩余前提

- 本文件及所导入 skeleton 的 elaboration/kernel、公理检查。所有 `#print axioms`
  均未执行，没有编译或 proof receipt。
- 实际 M、aB、forcing、两种 defects、reference aD0/MDB0 与定义记录的精确身份；
  独立 O1 residual 必须满足表中的 rB_O1 身份，不能只凭名称绑定。
- condensed 消元需要同一个 J 的精确左逆；近似 inverse 的缺陷未被此文件吸收。
- 若用 reference-source 解释 dO，需明确 reference balance 及其 epsilonD0。
  两种 convention 的 forcing/defect 定义、坐标和一次性 normalization 必须一致。

本轮没有 source/Float64、PSD、norm、coverage、admission 或 registry 结论。
