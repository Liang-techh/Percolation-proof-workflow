---
kind: review_result
review_id: review-GH-MATH-P4-DIRECT-BLOCK456-BETA-DESIGN-codex-20260908
task_id: GH-MATH-P4-DIRECT-BLOCK456-BETA-DESIGN
agent: codex-block456-beta-math-lane
source_agent: codex-block456-beta-math-lane
created_at: 2026-09-08
inspected_commit: 29fc6330213f11f34e618d3857a599c44d7c17c2
status: pending
integration_status: pending
admission_label: pending
proof_status: bounded_exact_arithmetic_and_mathematical_derivation
lean_compile_status: not_run
registry_eligible: false
final_integration: false
artifact_path: examples/routeb_block456_beta_design_research/NEW_BETA_DESIGN_check.py
proposed_integration_target: P4.direct_block456.beta_design_and_acceleration_domain
requested_action: retain beta_a=3/25 as a local design candidate only; harvest the nonzero-q6 zero-acceleration obstruction and exact beta interval; supply a physical acceleration graph and same-metric energy split before another direct-target certificate search
---

# beta_a=3/25 的完整目标影响与不可由 beta_a 修复的方向

结论：增加 beta_a 改善 direct residual target，但降低固定 dissipation certificate 的余量。
更强的是，**当前 factorized descriptor ideal 上存在非零 q6、零加速度的精确反例，
任何 beta_a 都无法修复**。因此 `3/25` 不是当前完整代数目标的充分参数设计。

本轮沿用已提供的原点惯性块判定，不重算其 principal minors 或正负定性。
只读外部 source，新增一个 bounded Python sidecar 和本 review；无 Julia/SOS/CI/Lean、
无分区遍历或全回归、无 state/registry/source 修改，不声称 VERIFIED 或闭合。

## 1. 精确定义与参数增量

以下 source 名称相对
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`。

`routeB_compact_block456_descriptor_structure_audit.jl:17-76` 使用
`C=(4,5,6), D=(1,2,3)`，定义

```text
M = M0_CC,  W = M^-1,
F = (IVAL_i*fC_i)_(i in C),
l_base = F - M*a,
M_DD(q)*vD + DeltaM_DC(q)*a = 0,
r = M_CD(q)*vD,
l_total = l_base + r.
```

这里的 `vD` 是 descriptor 辅助变量，不应仅凭名称等同于实际速度或 full ODE acceleration。
这些三条 remote/port/total 关系尚未将 `a_C` 约束成真实 full-DH acceleration。

`routeB_compact_block456_residual_schur_interface_audit.jl:25-35` 定义

```text
A = ||a_C||²,
B = (1/10)*(||q_C||²+||dq_C||²) + (1/20)*w²,
beta_C(b) = b*A+B,
P_b = beta_C(b) - l_total' W l_total.
```

固定所有其他变量、域、矩阵、参数后，从 `b0=1/100` 改为 `b1=3/25` 的增量是

```text
delta = 11/100,
P_b1 = P_b0 + (11/100)*A.
```

该点态单调性对整个 target 成立，不局限于原点，也不依赖 descriptor 等式。
它不控制 `A=0` 的方向。target 的次数、变量 support 和已有 degree cap 不因这次
系数改变而增加；任何现有 Gram/certificate 的 coefficient equality 仍须重新满足。

## 2. D_base、stacked Schur 的相反符号

`routeB_compact_block456_fd_stacked_pmi_structure_audit.jl:15,46-56` 冻结 `s=5` 并定义

```text
Dcore = -dq_C' F + w²,
D_b = Dcore + dq_C' l_base + s*||l_base||² - s*(b*A+B),
h = dq_C + 2*s*l_base.
```

因此

```text
D_b1 = D_b0 - (11/20)*A.
```

现有 stacked PMI 只在左上角出现 beta；其余块和 h 不变。于是同一参数改变为
负半定的 top-left 更新 `-(11/20)*A*e0*e0'`，不会改善该 PMI。
`routeB_compact_block456_stacked_pmi_schur_reduction_audit.jl:26-32` 的标量为

```text
S_b = D_b - rho_DH²*A_DH - A_FD - ||h||²/22,
S_b1 = S_b0 - (11/20)*A.
```

这是参数敏感性恒等式，不认可旧 stacked 文件的 dense-metric/Euclidean remainder
绑定，也不需要重做该 metric transport lane。
如果重新选择 s、nu、storage 或 residual evaluator，就必须按新对象重建公式；
不能把这组冻结参数差值当作重设计后的全部变化。

特别地，已有 `D_b0≥0` 或 `S_b0≥0` 不足以迁移；需要至少
`D_b0≥(11/20)A` 或 `S_b0≥(11/20)A` 的同域余量。

## 3. 非原点、零加速度的 exact direct-target obstruction

这是新方向，不重复已给出的原点 acceleration-block audit。
取非零 `t`，例如 `t=1/1000`，指定

```text
q6=t; 所有其他 q、全部 dq、w、a_C、vD、r_C 均为 0;
c2=c3=c4=c5=1, s2=s3=s4=s5=0;
所有 link/force auxiliary channels 均为 0;
l_total=(0,0,-(43/100)*t).
```

这使用 descriptor source 的**实际 nominal joint6 系数**：
`IVAL6*fC6=-(Kp6+MGL6)*q6=-(2/5+3/100)*q6`。
没有将其换成其他 controller lane 的系数。

该点满足所读取的整个结构等式集合：

- circle 等式成立，并与真实 q2–q5 的三角值一致；q6 不参与四个 circle pairs。
- 72 个 link 等式的两端为 0，因为 a_C=vD=0。
- 36 个 force-channel 等式的两端为 0，因为 link channels=0。
- remote balances 的 `vD`、`DeltaM*a_C` 为 0；port balances 亦为 0。
- total-link 三式正是 `l_total=F-M*a_C+r_C`。

因此包括四个 circles 的 121-row split ideal，以及代入 force 后的 85-row eliminated
ideal，都允许该点。相关 builder 只装配 target SOS 和这些 equality multipliers；
不能通过增高 degree 或更换稀疏 Gram 使其在这个可行点非负。
此处 ideal membership 是按 source 定义逐组推导；Python 并未完整 reify 每条 Julia 多项式。

仅为计算这条非零 q6 ray，重用 exact coefficient table 所定义的 nominal metric：

```text
M = [[350003/3000000, 0, 1/60],
     [0, 200739/4000000, 0],
     [1/60, 0, 50003/3000000]],
W66 = 350003000000/5000400003.
```

该矩阵来自 `routeB_analytic_mass_full_cs_polynomial.csv` 的有理系数与明确 regularizer，
没有将 rounded `routeB_Mq_M0.csv` 解释成 exact matrix，也没有重复原点定性筛选。
保留 dense 的 4–6 coupling 后，target 精确为

```text
P_b(t) = [1/10 - (43/100)²*W66]*t²
       = -642155146997/50004000030 * t² < 0.
```

**对所有 b 都成立**，包括 `3/25`，因为 A=0。
在 `t=1/1000`，值为 `-642155146997/50004000030000000`。
这个点可以任意靠近原点，满足通常正半径的 q6 bounds；但未证明它属于任何尚未绑定的
active-energy sublevel。其正负结论不以能量域推断为前提。

这反驳的是当前代数 descriptor-domain 的 target 非负性，**不是完整物理 ODE 或
控制器稳定性的不可能定理**。加入真实 acceleration graph 可以排除此点；
不能将“当前 ideal 允许”写成“该物理轨迹可达”。

## 4. 不只 beta_a：当前 beta_x 的双阶段区间也不相交

同一 ray 上，若只把 state 系数改为任意 x，direct target 非负要求

```text
x ≥ (43/100)²*W66 = 64715554700/5000400003  (>12).
```

当前 Euclidean `D_base` 在该 ray 上为

```text
D_b(t) = 5*[(43/100)²-x]*t²,
```

所以 `D_base≥0` 要求 `x≤1849/10000`。两区间严格不交，且都与 beta_a 无关。
在当前 x=1/10 时，`D_base=(849/2000)t²>0`，正是 direct target 失败；
提高 x 去修复 direct target 则破坏该 D_base。

这个 obstruction 针对**当前两个显式表达式**，其中一个用 W、另一个用 Euclidean norm。
它不是“所有正确 metric-consistent 重设计都无解”。若把 D 也重构为
`Dcore+dq'l+s*(l'Wl-beta)`，在此零功率 ray 上两条件仅能在
`x=(43/100)² W66` 同时取等，不能得到两边独立的严格正余量。

无需借用旧 block45 `beta_budget_tension` 的数字，也无需重新审计全域 external rho。
该旧文件的 block、controller 和 metric 均不同，本 review 没有把它拼入 block456。

## 5. 可消费的 exact beta 条件

### 固定现有目标的点态/全域可行区间

在同一源变量、同一声明域 Omega 上，记

```text
L = l_total' W l_total,
Dstar = Dcore + dq_C'l_base + s*||l_base||² - s*B,
R = 固定的同域 robust/Schur reserve,
D_b-R = Dstar-R-s*b*A.
```

当 A>0，两阶段的 exact simultaneous gate 是

```text
(L-B)/A ≤ b ≤ (Dstar-R)/(s*A).
```

当 A=0，必须单独验证 `L≤B` 和 `Dstar≥R`；任何 b 都不能改变它们。
全域条件是上述不等式对 Omega 内每一点成立，而不是只比较原点或若干采样。
用 sup lower/inf upper 表达时也必须保留 A=0 条件，且还需 b 的其他符号/预算约束。

固定 `b=3/25,s=5` 时，等价迁移要求为

```text
P_(1/100) ≥ -(11/100)*A,
D_(1/100)-R ≥ (11/20)*A.
```

第 3 节的点违反第一组的 A=0 条件，所以当前 Omega 上该参数区间为空。

### 若先补入物理 acceleration graph

现有 remote elimination 在已证明 `M_DD` 可逆时给出

```text
T(q)=M+M_CD(q)*M_DD(q)^-1*DeltaM_DC(q),
l_total=F-T(q)*a.
```

令 `H_b=b*Id-T'WT`，则完整 direct target 精确展开为

```text
P_b = a'H_b*a + 2*a'T'WF + B-F'WF.
```

若 H_b 正定，写 `g=T'WF`，配方得到

```text
P_b = (a+H_b^-1*g)'H_b*(a+H_b^-1*g)
      + B-F'WF-g'H_b^-1*g.
```

因此对固定配置与 force，**所有自由 a** 上非负的 exact condition 是
`B≥F'WF+g'H_b^-1*g`。只验证 `H_b>0` 漏掉了 force 和交叉项。
H_b 奇异半正定时还需 `g` 的 range compatibility，并使用相应广义逆；本轮不隐藏该条件。

如果只要求实际 graph `a=A_source(q,dq,w)`，则应直接在该 graph 上验证展开式，
不必强求所有自由 a 的更强条件。必须提供同一 source、regularizer、controller/FD
语义下的 graph 或足够的 acceleration-domain generator，证明所需域上的包含。
当前三条 remote balance 本身不提供这个 witness。

## 6. energy / terminal budget 的准确解释

beta 是 residual certificate 的预算系数，调 beta 本身没有改变物理 kinetic storage
或其真实导数。它改变的是把 residual bound 代入 dissipation proof 时的余量。

在已正确绑定同一 metric 的 energy split 中，若

```text
E = -Vdot + supply,
D_b = E + s*(l'Wl-beta_C(b)),
P_b = beta_C(b)-l'Wl,
```

则恒等式 `E=D_b+s*P_b` 中 beta 完全相消。
因此不能把 `P_b` 的增益当作免费新增 dissipation。

当前文件的 D 使用 `l'l`，direct 使用 `l'Wl`；它们的和含
`s*l'(Id-W)l`，不是上述相消式。须有正确 metric transport/重写或有证明的
norm domination 才能消费；本 review 不代替另一条 metric lane 的 source witness。

若已有旧 D 证明，而新 direct bound 只允许把 energy inequality 放宽为
`Vdot≤supply+(11/20)||a_C||²`，则在 [0,T] 上新增的 terminal 上界费用为

```text
Delta_energy = (11/20)*integral_0^T ||a_C(t)||² dt.
```

剩余可用 terminal/energy slack 为 m 时，足够的附加 witness 是
`integral ||a_C||² ≤ (20/11)*m`。若仅有已证明的点态 `||a_C||²≤R_a²`，
可用更强的充分条件 `(11/20)*T*R_a²≤m`。
这些积分、regularity、同域 path、原 initial bound 和 storage/threshold 绑定均为额外前提，
没有从 q/dq caps 或 beta_a 的原点测试自动导出。

## 7. 有界验证和交付边界

Sidecar：`examples/routeb_block456_beta_design_research/NEW_BETA_DESIGN_check.py`。
使用标准库 Fraction 读取有理 mass table，核对 inverse identity、q6-ray 数值、
两个系数迁移和不相交区间；关键 source snippets 做限定检查，并输出读取文件的 SHA-256。
读取前后检查输入字节未变，所有结果只写 stdout；不执行外部 Julia 文件。

复现：

```powershell
python -B examples/routeb_block456_beta_design_research/NEW_BETA_DESIGN_check.py --self-test
```

实际 exit 0；四个负控被拒绝：beta 单独修复 A=0 ray、D 随 beta 增大而改善、
Euclidean 与 nominal metric 相同、该 ray 的 beta_x 两区间相交。
该脚本不是 Lean verifier，也不宣称完整 Julia descriptor parser/reifier。

关键读取版本：

| Source | SHA-256 |
|---|---|
| `routeB_analytic_mass_full_cs_polynomial.csv` | `1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451` |
| `routeB_compact_block456_descriptor_structure_audit.jl` | `9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79` |
| `routeB_compact_block456_residual_schur_interface_audit.jl` | `3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98` |
| `routeB_compact_block456_fd_stacked_pmi_structure_audit.jl` | `9050e40ab2daf7231df8a623a5201e44890d35b68d5ba0e9e5611d49d7cc07db` |
| `routeB_compact_block456_manual_sparse_gram_probe.jl` | `be1ed8d5cad271a24fea8856b0ad646133e72026a32035bf9443f6004e3cbaa6` |

最终：`3/25` 保留为局部设计候选；当前 full direct polynomial 的 beta-only repair
在所读取的 descriptor ideal 上被非零 q6 ray 排除。要继续，优先补 full physical
acceleration/domain binding 并对齐 energy metric，再使用第 5–6 节的 exact gates。
没有 full physical infeasibility、全域 remainder/coverage/flowpipe、P4/P5 closure 或 admission claim。
