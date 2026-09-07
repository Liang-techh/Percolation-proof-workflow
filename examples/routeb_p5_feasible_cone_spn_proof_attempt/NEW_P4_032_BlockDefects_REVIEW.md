# T-P4-032：有序 block projection 与 defect-aware O1 skeleton

日期：2026-09-07。新增 `NEW_P4_032_BlockDefects.lean` 与本 review。
状态为 **source-independent、未编译 Lean skeleton**；未执行 Lean/Lake、求解器、
source checker 或数值测试，未改旧 O1 候选、state、registry、共享脚本及其他文件。

依据为 `agent_review_inbox/review-T-P4-032-liuguanyi-20260907T1210.md`，并读取
同目录 `review-T-P4-032-codex-20260907.md` 与 `review-T-P4-032-repair-20260907.md`
中的乘法括号/API 注意事项。新 sidecar 独立导入 Mathlib，不导入旧 O1 artifact。

## 已写出的实际类型及证明连接

`bIdx : Fin 2 → Fin 6 = [3,4]`，`dIdx : Fin 4 → Fin 6 = [0,1,2,5]`，
对应物理顺序 B=(4,5)、D=(1,2,3,6)。分别附 injective、disjoint、cover 证明脚本。
这是从块槽到全轴槽的 embedding；从六向量到块向量则由 `projB/projD` 完成，
不存在把全部六个轴强行映射成单个 B 或 D 槽的隐式选择。

`sum_partition` 以明确有限和保留每个轴一次。`projD_mulVec` 与 `projB_mulVec`
将其用于矩阵每一行，目标是：

```text
projD(M*a) = MDD*projD(a) + MDB*projB(a)，
projB(M*a) = MBB*projB(a) + MBD*projD(a)。
```

乘法均为 `Matrix.mulVec`，不要求 M 对称。D 最后一个槽始终是物理轴 6。

`distal_difference_identity` 从两条共用同一个 aB 的 distal balance 推导：

```text
MDD*(aD−aD0) + (MDB−M0DB)*aB
  = (FD−F0D) − (MDD−M0DD)*aD0。
```

`projected_distal_defect` 进一步从完整六轴方程 `M*a=F`、`M0*a0=F0` 及
`projB(a0)=projB(a)` 得到该式。`canonicalDistalDefect` 保留右端两项；
`zero_distal_of_compatibility` 只在另给精确 forcing/reference 兼容条件时消去它。
不同 aB 的两套比较方程不在这个最小接口中，需另补对应差异项，不能忽略。

## Defect-aware 消元

`Rport = −MBD*(MDDinv*DeltaMDB)` 固定乘法顺序 `2→4→4→2`，使用右结合括号。
只要求左逆 `MDDinv*MDD=I`，不构造 inverse，不引入右逆、SPD 或数值解。

`port_identity_with_defects` 以以下三条为显式前提：

```text
MDDinv*MDD=I，
MDD*delta_a_D + DeltaMDB*aB=eD，
rB−MBD*delta_a_D=eB。
```

证明脚本先左乘 MDDinv，再左乘 MBD，目标为：

```text
rB = Rport*aB + (MBD*MDDinv)*eD + eB。
```

没有对矩阵乘法使用交换律。leading minus 来自移项，不允许转移到 DeltaMDB
而保持其他契约不变。`full_equations_to_port` 将分块、distal 比较及此消元直接汇合，
保留 canonical eD。`zero_defect_port_identity` 是 eD=eB=0 的直接推论。
两项分别为零是充分条件；不声称必要，因为非零 defect 的映射与 eB 也可能相消。

## 一次性 normalization 与语义类型

新建不同结构类型 `BlockAcceleration`、`DistalAccelerationCorrection`、
`DistalGeneralizedForce`、`PortGeneralizedForce`、`RawPMIForce`，避免仅因向量
长度相同就隐式混用。`typed_port_identity` 的消元变量是 acceleration correction，
没有任何名为 physical velocity/dq 的别名或自动转换。

`normalizeRawPMI : RawPMIForce → PortGeneralizedForce` 显式应用一次
`diag(1/5,1/10)`；`normalization_components` 展开两个分量。
它不接受 `PortGeneralizedForce` 作为输入。`portFromAcceleration` 的质量块乘
加速度修正直接产生 generalized force，Rport 与 DeltaMDB 内没有 normalization。

这些结构只约束接口，不认证用户包装进去的数据来源或单位。主动解包再错误包装
仍可能绕过语义意图，因此 actual raw-PMI 身份及 normalization 约定必须在上游证明。
本轮没有把 port 分量识别为整个 P4 residual。

## 精确剩余前提

- 编译新文件并检查 elaboration/kernel、公理；本轮末尾 `#print axioms` 均未执行。
- source 六轴次序、M/M0/加速度/广义力与部署变量的真实身份；实际与参考 aB 相同。
- 实际求解所满足的精确 balance。Float64 backslash 不自动给出 `M*a=F`；若有
  solve defect，应显式进入有效 forcing，继而进入 eD/eB，不能从推导中删去。
- 作为消元算子的 MDDinv 的**精确左逆证明**。近似逆若有缺陷，需扩展公式加入
  相应项，本 skeleton 不接受其数值近似替代左逆身份。
- 实际 eD/eB 身份，以及下游对 `(MBD*MDDinv)*eD+eB` 的界或相消证明。
  controller、C/G、timer/ramp、distal forcing、参考模型差异均不因 O1 系数形式而自动消失。
- raw/normalized force 的源契约、绝对 source-domain coverage、P4/P5 absorption、
  ODE/flowpipe/terminal transfer 与 admission，均保持开放。

本轮交付的是可审阅的具体 Fin/Matrix proof skeleton，不是 Lean compile、
deployed Float64 solve、source/coverage 或 registry closure 的证明。
