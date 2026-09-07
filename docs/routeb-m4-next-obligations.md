# Route-B M4 / P4：下一组最小联合不等式

日期：2026-09-06。本文是只读数学瓶颈审查的产物；只新增本文件，不修改
`state`、registry、canonical source 或外部源，也未运行全局长任务。

## 结论

当前 `M4` 仍是 open。`D_* = 4483/2000` 已经由 F4 exact comparator 验证为
一个有严格余量的算术门槛，但“deployed true-DH 轨迹的 `D <= D_*`”尚未证明。
短缺不是再找一个更松的标量幅值上界，而是把同一条六轴轨迹上的

1. `p/sigma` 相关性；
2. P4 的 D-row/Schur 残差；
3. residual 的统一平方积分；以及
4. terminal variation-of-constants/kernel 比较

接成一个联合链。建议的最小链如下：

```text
C1 joint p/sigma correlation
        |
        v
C2 P4 source/D-row + residual normalization
        |
        +--> C3 joint energy seam (可选的 JointPSigmaBudget 分支)
        |
        v
C4 uniform D budget on the same covered domain
        |
        v
C5 terminal kernel comparison + first-exit composition --> M4
```

C3 是构造 `L` 或 block tube 的辅助分支；若 C5 直接从线性 kernel 给出 `L`，
它可以跳过，但不能用来替代 C4。

## 固定目标与归一化

对 `B={4,5}` 写

```text
P_B(t) = 3/2*(q4(t)^2+q5(t)^2) + 4/5*(v4(t)^2+v5(t)^2),
Q_B(1) = 3*(q4(1)^2+q5(1)^2) + 2*(v4(1)^2+v5(1)^2),
D(e)   = integral_0^1 sum_{i=1}^6 e_i(t)^2 dt,
D_*    = 4483/2000.
```

这里的 `e` 必须先固定语义：是 force residual、acceleration residual，还是
经过质量矩阵缩放后的 residual。P4 现有语义审计中的 `l45` 是 force-side
linking row；terminal flowpipe 报告中的 `D` 是 acceleration-side 量。不得
在没有质量/逆质量范数不等式的情况下把二者同名相加或直接识别。

## 按依赖顺序的最小 child theorem

### C1 — `joint_p_sigma_correlation`

这是第一个真正需要把两个已提交代数叶接入物理变量的 adapter；它本身不是
预算闭合。

建议的精确前提（对所有 `t ∈ [0,1]`，以及允许的初值和 ramp 参数）：

```text
m4 > 0, m5 > 0;
p_B(t) = M_BB(q(t))*v_B(t) + M_BD(q(t))*v_D(t);
R_B = reference block,  sigma_B(t) = p_B(t) - R_B*v_B(t);
the exact trig-slot/source map used by the deployed model;
the two momentum identities p4-R4*v4=sigma4 and p5-R5*v5=sigma5.
```

结论应保留联合形式，而不是只输出两个独立的 `|sigma_i|` cap：

```text
p_B = R_B*v_B + sigma_B,
v_B = R_B^{-1}(p_B-sigma_B)  (when R_B is positive/invertible),
sigma_B = M_BD*v_D + (M_BB-R_B)*v_B + e_B.
```

`MomentumIdentity.p4_minus_R4v4_eq_sigma4`、`p5_minus_R5v5_eq_sigma5` 可以
直接作为两个分量的 algebraic leaves。`Quasimomentum` 可以接入 `v6` 方向：
在 `m46 = (50000/50003)*cos(y)*m66` 的前提下，`v6` 系数为零；但它的
`q6Drive + fdDefect` 仍必须作为显式 residual 输入，不能在 C1 中设为零。

精确缺口是：当前两个叶把 trig/source/DH 变量当作任意实数，没有证明上述
`M_BB,M_BD` 与 deployed DH/Float64 量相等。

### C2 — `p4_source_drow_residual_normalization`

这是 P4 的最短物理接口。它应把 source descriptor、D-row auxiliary variables
和 residual 的单位一次性固定，然后才调用 Schur/PMI。

所需前提：

```text
M(q)*a = tau - C(q,dq)*dq - G(q)              (deployed descriptor semantics);
the exact Kp/Kd/friction/gravity/input source expansion;
the regularizer and both diagonal M0 entries, with exact source binding;
l45 = [I4*f4, I5*f5] - diag(M0[4,4],M0[5,5])*a_B;
the exact correspondence between D0,c1,c2,D_elim_c and both PMI blocks;
full-state PSD (or weighted full-state PSD) on the current cell;
an explicit map between force residual e_F and the chosen e in D.
```

最小结论应是点态联合不等式，而不是仅有矩阵恒等式：

```text
P(v,w) + <e_F,v>
  <= (631227/1086800)*w^2
     + sum_i e_F_i^2/(2*D_i),
```

再由已提交的 `RouteBResidualPower.supply_with_squared_force_error` 或等价
加权版本得到所选 residual 归一化下的 `rho(t)`。若使用 P4 Schur 形式，则
必须同时证明 deployed D-row 落在 abstract `ell*x+d*a=0` 的接口上；现有
`P4InterfacePMI` 只在显式 `FullStatePSD` 前提下给出这一推论。

可接入性：`P4InterfacePMI`、`SourceToP4Bridge` 和 `ResidualPower` 可作为
精确实数骨架；但当前 source bridge 的 `sourceD` 只是 decimal Float64
snapshot，不能充当本 theorem 的 source-binding 前提。

### C3 — `joint_filtered_energy_seam`

这个 child 只负责把点态 derivative inequality 变成可以消费的联合 energy
seam。建议使用两条明确分开的实例化方式之一：

**过滤器分支（可接 `JointPSigmaBudget`）：** 对 `i=4,5` 给出

```text
p_i = m_i*v_i + sigma_i,
xq_i=q_i, xp_i=p_i/m_i,
xq'_i=xp_i, xp'_i=-kappa_i*xq_i-lambda_i*xp_i+forcing_i,
lambda_i>0, m_i>0, kappa_i>=0,
IntegratedEnergySeam_i:
  V_i(T)-V_i(0) <= accumulatedForcing_i/(4*lambda_i)+sigma_i(T)^2,
ForcingBudget_i and SigmaTerminalBound_i.
```

结论是两个 `V_i(T)` 上界及其有限和，再用
`JointPSigmaBudget.velocity_sq_of_joint_state` 得到含 `sigma_i^2/m_i^2`
的速度上界。这里 `IntegratedEnergySeam_i` 是前提，不是该叶自动产生的
积分定理。

**P4 residual 分支：** 若从 C2 得到

```text
E'(t) <= gamma*w(t)^2 + rho(t)   a.e.,
E is absolutely continuous, E(0)<=E0,
integral_0^1 rho(t) dt <= R,
w(t)=c*t, c^2<=3,
```

则应证明

```text
E(1) <= E0 + gamma + R.
```

不得把后一分支伪装成当前 `IntegratedEnergySeam`，除非另有 theorem 证明
两种 `E/V/sigma/forcing` 定义逐项相同。`JointPSigmaBudget` 能接入 C1 的
动量分解和 C3 的过滤器实例，但不能单独产生 P4 的 `D` 或 deployed DH
trajectory seam。

### C4 — `uniform_full_domain_residual_budget`

这是 `D <= 4483/2000` 的核心 child，也是当前最实质的 open obligation。

必须对同一套原始目标量化：

```text
forall x0, ||x0||_2^2 <= 9/400,
forall c, c^2 <= 3,
forall deployed trajectories z on [0,1],
  z satisfies the same exact/Float64 source semantics and domain contract.
```

并提供：

```text
z is covered/continued on every time cell (or a valid first-exit proof);
e = e_ref + e_FD + e_round + e_solve with typed units;
rho(t) >= sum_i e_i(t)^2 on the whole covered domain;
integral_0^1 rho(t) dt <= 4483/2000.
```

若 `rho` 从分量包络构造，必须在平方前保留交叉项；所有 FD truncation、
Float64 rounding、linear-solve/execution residual 和 mass/reference mismatch
只能收费一次。单点、采样最大值、FD-only budget、局部 cell 或 `p`-only
bound 都不能推出本 theorem。

该 child 可以消费 C2 的 residual inequality，也可以消费 C3 产生的 energy
seam；但无论哪条路，domain、full-X0、ramp、T=1 和 residual normalization
必须完全相同。当前 P3/flowpipe receipts 尚未提供这个全局量化结论。

### C4b — `relative_bias_residual_split` (new obstruction)

`T-P5-005` 的数学审查（见
`agent_review_inbox/review-T-P5-005-kuangmanmozun-20260906T2307.md`）表明，
不能从当前抽象 `forceError` 或 `FDForceBudget.envelope` 自动推出
`|r_i| <= rho_i |v_i|`：generic interface 允许在 `v=0` 时存在独立的
gravity/controller mismatch，而 FD envelope 的 channels 1--4 还有正的
additive offset。这个结论是接口 obstruction，不是对实际 deployed trajectory
的反例；实际 source 仍需额外的 equilibrium/state binding。

因此 P5/M4 的 admissible 分解应显式写成：

```text
e = e_rel + e_bias;
B(e_rel) <= kappa^2 A(v),  kappa < 1;
E' <= -(1-kappa) A(v) + <e_bias,v> + input_supply.
```

只有在同一 covered domain 上证明 `e_bias=0`（或它也随状态消失）时，才可
把该式收缩为 strict zero-input decay。否则 `e_bias` 必须进入 C4 的统一
residual ledger，并继续使用 absolute/ultimate-bound 路线；不得通过调 Young
常数伪造 relative closure。C4b 只改变 proof decomposition 和 frontier
排序，不改变 `D_gate=4483/2000`、C5 target 或 admission gate。

### C5 — `terminal_kernel_and_m4_composition`

最后一个 child 把 C4 的 `D` 送入 terminal comparator，同时保留 domain
first-exit 结论。

所需前提：

```text
exact variation-of-constants: x(1)=x_lin(1)+r;
full initial ball and the same deployed/exact model semantics;
x_lin(1)^T*C*x_lin(1) <= L;
r^T*C*r <= g*D(e);
Q_B(1) = x(1)^T*C*x(1);
P_B(t) < 28/5 for all t in [0,1] (or a proved FirstExitSafe premise);
D(e) <= 4483/2000;
g >= 0 and the fixed normalization id
  F4_DIRECT_QPOLY_LG_D4483_V1.
```

先证明唯一需要的新联合不等式：

```text
Q_B(1) <= (3/2)*L + 3*g*D(e).
```

随后可直接调用已提交的
`RouteBF4DirectQpolyComparator.qpoly_terminal_comparator`，得到
`Q_B(1)<12`。`TerminalTransferContract`/GAE 类组合 theorem 可以保留
`FirstExitSafe`，但它们只组合 `hcompare`、`hD` 和 scalar gate，不产生
variation-of-constants、kernel bound、first-exit 或 C4。

## 四个已提交叶的接入判定

| 叶 | 可以接入的位置 | 必须补的前提 | 不能提供的结论 |
|---|---|---|---|
| `JointPSigmaBudget` | C1、C3 过滤器分支 | 实际 joint filter dynamics、`IntegratedEnergySeam`、正的 `m/lambda`、terminal sigma bound | 不产生 deployed residual `D`、source binding 或 global coverage |
| `MomentumIdentity` | C1 的 `p=Rv+sigma` 分量恒等式 | trig slots 与真实 source/DH 变量的 extensional map | 不产生 sigma cap、sigma variation 或 trajectory bound |
| `Quasimomentum` | C1/C2 的 `v6` cancellation 与 residual 分解 | affine profile、系数等式、`q6Drive/fdDefect` 的真实预算 | 不证明 cancellation along deployed trajectory，也不消灭 open inputs |
| `Terminal comparator` | C5 的最后 scalar gate | `Q<=3L/2+3gD`、`D<=4483/2000`、固定 normalization | 不产生 `D`、kernel inequality、first-exit 或 DH semantics |

## 明确禁止的 amplitude-only 路线

以下路线不得作为 C1--C5 的替代：

1. 只假设 `|sigma_i(t)|<=S_i`，把 `sigma` 当任意 measurable input，再声称
   得到原始 block tube 或 terminal bound。已有连续 piecewise-affine relaxed
   filter witness 在 `S=59/500` 下给出 `-5<v5(1)<-4`，并导致 terminal
   quantity `>32`；这否定的是该放松类，不是原始 DH theorem。
2. 由 `|sigma|` cap 推出 `|sigma'|` cap，或忽略速度公式中的 terminal
   feedthrough `-sigma(T)/m`。两者都没有逻辑依据。
3. 将 `V=v2+v3` 拆成独立 `|v2|+|v3|` 并以更大的 absolute-coefficient
   bound 代替真实 cyclic/momentum correlation。
4. 用 `p<=28/5` 直接推出 `qpoly<=12`。精确关系仅为
   `2p<=qpoly<=(5/2)p`；见证 `q4=q5=v5=0,v4=5/2` 给出
   `(p,qpoly)=(5,25/2)`。若走纯 set comparison，至少需要 `p<=24/5`；
   更合适的是 C5 的 direct comparator。
5. 用 block-only 或 remote-zero 初值替代完整的
   `sum_i(q_i(0)^2+v_i(0)^2)<=9/400`，或用局部 cell/采样轨迹替代全域
   first-exit 与 continuation。

## 最短执行建议

优先实现 C1+C2 的 typed adapter，并在一个已固定 cell 上尝试 C2 的 residual
normalization；若 force/acceleration 单位或 D-row 对应关系不能同时成立，应
立即停止铺开 branch tree。只有 C2 成功后，C4 才值得做全域积分账本；C5 的
算术部分已经足够，不能把它的 conditional PASS 写成 M4 closure。

参考：

- [`examples/routeb_joint_psigma_budget_lean/JointPSigmaBudget.lean`](../examples/routeb_joint_psigma_budget_lean/JointPSigmaBudget.lean)
- [`examples/routeb_momentum_identity_lean/RouteBMomentumIdentity.lean`](../examples/routeb_momentum_identity_lean/RouteBMomentumIdentity.lean)
- [`examples/routeb_quasimomentum_cancellation_lean/QuasimomentumCancellation.lean`](../examples/routeb_quasimomentum_cancellation_lean/QuasimomentumCancellation.lean)
- [`examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean`](../examples/routeb_terminal_qpoly_comparator_lean/F4DirectQpolyComparator.lean)
- [`examples/routeb_residual_power/ResidualPower.lean`](../examples/routeb_residual_power/ResidualPower.lean)
- [`artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/AUDIT_REPORT.md`](../artifacts/routeb_agent_p4_semantic_contract_20260906T100000Z/AUDIT_REPORT.md)
- [`artifacts/task_routeb_terminal_arithmetic_current/REPORT.md`](../artifacts/task_routeb_terminal_arithmetic_current/REPORT.md)
- [`examples/routeb_momentum_filter/DERIVATION.md`](../examples/routeb_momentum_filter/DERIVATION.md)
