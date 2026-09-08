---
kind: review_result
review_id: review-T-P4-ACTIVE-ENERGY-ORIGIN-source-normalization-codex-20260908T0840
task_id: T-P4-ACTIVE-ENERGY-ORIGIN
agent: codex-active-energy-math-lane
source_agent: codex-active-energy-math-lane
created_at: 2026-09-08T08:40:03-06:00
inspected_commit: 76160eda3cb3d701d3b44e9a3740249b7678569f
status: pending
integration_status: pending
admission_label: pending
proof_status: mathematical_derivation_and_exact_symbolic_check_only
lean_compile_status: not_run
source_binding_status: exact_real_transcription_only
registry_eligible: false
final_integration: false
proposed_integration_target: P4.active_energy.source_potential_and_block_initial_bound
requested_action: harvest the concrete DH height identities and restricted mass formula into the existing sourceContract chain; select and bind the actual target storage before origin or barrier admission; do not transfer the old V<=1 barrier across storage normalizations
---

# Active-energy origin：找到具体 source 数学桥，但原 V≤1 迁移不成立

本轮新增两项可直接交给 source Lean lane 的数学结果：

1. 按 `dhport_lib.jl` 的精确实数 DH 解释，**整个势能函数**满足
   `U_DH(q) = U_audit(q) + 10791/4000`，不再只是原点数值相差一个常数。
2. 对原增益、原 `10^-6` mass regularizer 和 block-only 初始球，归一化的六坐标
   能量满足 **`E_norm ≤ 27/4000`**。此推导不依赖 targeted `V_eps`、其 cross term、
   原 V0 CSV 标量或被引用的局部 Hessian 常数。

这些是具体 exact-real source 转录的数学推导及精确符号校验，尚未成为当前
`sourceContract` 的 Lean theorem，也不是 Julia Float64 执行等价证明。
现有 active candidate 仍未指定其值级定义，不能因此宣布 `V(0,0)≤1` 或 P4/P5 closure。
本轮仅写此 review；未运行会写 CSV 的旧脚本，未修改 source、state、registry、既有证明。

## 1. 当前实际消费链混用了哪些对象

外部 source 根目录为
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`。
以下均为本轮直接读取，不只依赖旧 review。

| 对象 | source 定义/用法 | 能推出什么 |
|---|---|---|
| `V_saved` | `routeB_export_traj.jl:66-77` 从 `routeB_certificate_V.csv` 重建 `(q4,q5,v4,v5,t)` 多项式 | 固定时间的四坐标函数，不控制其他坐标 |
| `V_eps` | `routeB_compact_targeted_nonlinear_strictification_audit.jl:19-35` 用 `Kp+(0,6,2,0,0,0)`、`eps=1/1000`、`q'Mv` 的导数 | 值级加常数仍未被该导数表达式固定；它是 full-state targeted storage，不是四坐标 CSV 多项式 |
| 原 V0 producer | `routeB_compact_energy_storage_to_block_audit.py:17-23,44-51,78` 给出 block-only X0 上的 targeted bound | 标量 `492033745203/25600000000000` 绑定的是所假设的 targeted envelope |
| barrier 消费者 | `routeB_compact_block_energy_barrier_audit.py:18,49-54,92-103` 读取这个 V0，设置 `V_BAR=1`，使用 full-energy q/v lower bounds | 未定义/比较实际 V 函数；CSV 的 `energy_first_exit_closed=True` 是条件算术结果 |
| `E_norm` | `K+U(q)-U(0)+(1/2)sum Kp_j q_j²`，原增益且 exact-real origin compensation=0 | 原点为 0；不自动非负或 coercive |
| `E_shift` | `K+U_audit+Cg+(1/2)sum Kp_j q_j²`，`Cg=205029/40000` | 具备所引用 shift 下界的候选；其原点大于 1 |

因此必须同时区分：**四坐标 storage**、**full-state storage 的 block-only 初始集**、
**六坐标目标能量**。初始集只有四个自由坐标，不意味着对应 storage 函数只依赖四个坐标。

## 2. 具体 DH → 势能恒等式：补齐旧 origin-only ledger

令 `c_j=cos(q_j), s_j=sin(q_j)`，并记

```text
C23 = c2*c3 - s2*s3
S23 = s2*c3 + c2*s3
Z = C23*c5 - S23*c4*s5.
```

用 `dhport_lib.jl:6-11,31-43` 的六个 DH 矩阵，角偏置与 alpha 的四分之一转取精确值，
十进制几何参数按其标示的有理数解释。七个 frame-origin 的 z 分量严格为

```text
h0 = 0
h1 = 1/10
h2 = h3 = 1/10 + (21/100)*c2
h4 = h5 = 1/10 + (21/100)*c2 + (19/100)*C23
h6 = 1/10 + (21/100)*c2 + (19/100)*C23 + (7/100)*Z.
```

这是逐次矩阵乘法恒等式；不是状态抽样或势能导数假设。
再用 source 的 midpoint COM、质量
`(1,4/5,3/5,2/5,3/10,3/20)` 和重力 `981/100`：

```text
U_DH = sum[b=1..6] m_b*(981/100)*(h_(b-1)+h_b)/2
     = 10791/4000
       + (762237/200000)*c2
       + (242307/200000)*C23
       + (20601/400000)*Z
     = 10791/4000 + U_audit.
```

`U_audit` 正是 `routeB_compact_energy_power_rewrite_audit.jl:102-107` 的表达式。
本轮将 12 个 c/s 变量当独立形式变量，以 SymPy 1.14.0 的有理多项式展开检查，
`U_DH-U_audit-10791/4000` 的全部系数为零。该等式甚至不需 circle ideal 约化。
所以在真实 sin/cos 代入后，所有实数配置上都有

```text
U_DH(q)-U_DH(0) = U_audit(q)-U_audit(0).
```

这是完整的势能归一化数学桥。它**没有**改变质量、增益、cross term、时间或状态映射。
若这些字段相同，归一化能量相等；若不同，势能桥本身不足以消去差异。

`U_audit(-q)=U_audit(q)` 还给出 exact-real central FD 的 `sourceG(0)=0`：
每个分量的 numerator 为 `U_DH(h e_j)-U_DH(-h e_j)=0`。
这不把 fixed-step `sourceG(q)` 当成 analytic gradient；只利用原点的对称性。
Float64 的角常量、libm、矩阵乘法、累加和 `G0_ref` 仍需其独立数值语义证据。

### 可直接进入现有 typed chain 的小叶

现有 `SourceContractAdapter.lean::source_origin_function_eq_frame_contract` 已提供
source list-slot origins 到 frame slots 的接口。建议只补七个 height 等式，再在
`NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907.lean:155-158` 的真实
`sourcePotential := sum routeBMass*(981/100)*bodyCom(sourceContract.origins)` 上有限求和。

所需具体目标为：

```text
sourcePotential q = auditedGravity q + 10791/4000
sourcePotential q - sourcePotential 0
  = auditedGravity q - auditedGravity 0
sourceG 0 = 0.
```

这些目标不需要全 M/C/G 比较、全轨迹覆盖或重新做外部 provenance 审计。
本轮没有假装这些目标已在 Lean 中证明。

## 3. 原点常数与固定阈值的精确反例

记 `A*=2029689/400000`、`Cg=205029/40000`、`beta=A*+Cg=4079979/400000`。
共用同一 kinetic/controller 表达式时，严格有

```text
E_raw = E_norm + A*
E_shift = E_norm + beta
E_DH_raw = E_norm + 3108789/400000.
```

在 `q=v=0`，kinetic 与 controller 项均为 0：

| 表达式 | 原点值 |
|---|---:|
| `E_norm` | 0 |
| `E_raw` | 2029689/400000 > 1 |
| `E_DH_raw` | 3108789/400000 > 1 |
| `E_shift` | 4079979/400000 > 1 |

这是省略常数转移 `E_norm≤1 ⇒ E_shift≤1` 的单点反例，且原点属于 block-only 初始集。
正确阈值关系是 `E_shift≤b+beta ↔ E_norm≤b`。
提高阈值时，原来从 `E_shift≤1` 推出的 `(5/2,15)` 全坐标 caps 和依赖它们的
FD/damping/tube 算术必须相应更新，不能保留原预算数字。

也不能靠更紧的纯重力常数把问题消掉：真实三角域上 `-A*≤U_audit≤A*`，
因为 `|Z|≤1`（旋转的单位轴 z 分量）。`q2=pi,q3=q5=0` 达到 `-A*`。
因此使重力自身全局非负的最小常数为 `A*`，其 shifted-energy 原点仍为
`2*A*=2029689/200000>1`。这只是**纯重力 shift** 类别的最优性，
不是所有联合势能、其他 storage 或局部域设计的不可行性结论。

## 4. 四坐标 CSV 与六坐标能量：常数修补也不成立

精确读取 CSV 十进制系数得

```text
k = V_saved(0,0,0,0,0)
  = -5852960231758441/50000000000000000 < 0.
```

CSV 导出器实际解析 Float64。仅对该常数做本机 Python binary64 解析得到
`-8435004646003727/72057594037927936<0`，它与上面的 decimal-rational 不同。
本 review 的精确有理式指 CSV 十进制数学解释，不冒充 Julia 全 evaluator 执行证明。
下述**依赖坐标缺失**的结构反例不依赖这两个负数之间的微小差别。

令 `q=a e1, v=0, t=0`。由第 2 节的完整势能式，`U(q)=U(0)`，
且原 `Kp1=1`，所以

```text
V_saved(q4,q5,v4,v5,0) = k
E_norm(a e1,0) = a²/2
E_shift(a e1,0) = beta + a²/2.
```

取两个任意邻近点 `a=0` 与 `a=1/10`：两者 CSV 值完全相同，full energy 相差 `1/200`。
故任何仅对 CSV 加常数（甚至固定仿射缩放）都不能使它在包含这两点的域上等于 full energy。
两点属于半径 `3/20` 的 full12 初始球，但第二点**不属于 block-only X0**；
不能把此反例误报为对 block-only 初始包含的反证。

如果要直接反驳从 block tube 推 full caps，取 `a=3`：
`V_saved=k<0≤t²=0`、`p45=0`，而 `E_norm=9/2>1`、`|q1|=3>5/2`。
`3<pi` 使其仍满足该关节的界限。它是状态集合反例，不声称轨迹可达。
无额外 remote-coordinate 域约束时，沿此 fiber 不存在全空间统一有限差值预算。

## 5. 可用的替代初始上界：实际 block-only source slice

取精确初始集

```text
q_j=v_j=0 (j not in {4,5}),
q4²+q5²+v4²+v5² ≤ 9/400.
```

势能直接简化为

```text
U_DH(q)-U_DH(0) = (20601/400000)*(cos q5-1) ≤ 0,
Uctrl(q) = (3/10)*q4² + (1/4)*q5².
```

更关键的是，source DH 的相关 2×2 质量子块在这条 slice 上精确为

```text
M_BB = diag(7/60 + 1/1000000 + (147/800000)*sin² q5,
            1/20 + 1/1000000 + 147/800000),
M45=M54=0.
```

推导使用 `dhport_lib.jl:46-60` 的 midpoint-Jv Gram、各 body 的 isotropic `I_val/3`
和同一个 regularizer。身体 1–3 不作用于这两个 Jacobian 列；身体 4、5 的相关
COM 平动列为零；身体 6 的 COM 到 frame 5 距离为 `7/200`，贡献系数
`(3/20)*(7/200)²=147/800000`。
相邻轴正交使 off-diagonal 为零；三个 rotational prefix 项对 joint4 求和为
`1/15+1/30+1/60=7/60`，joint5 为 `1/30+1/60=1/20`。

本轮按 source 矩阵/Jacobian 重算，并在
`c4²+s4²=1,c5²+s5²=1` 的有理 polynomial ideal 下约化，四个残差均为零。
使用 `R*(I_val/3)*Id*R^T=(I_val/3)*Id` 的前提是精确 DH rotation orthogonality；
这个数学前提在真实 sin/cos 下成立，不能直接移植到机器旋转矩阵而忽略舍入。

因此

```text
M_BB ≤ (1402217/12000000)*Id < (3/5)*Id,
K(q,v) ≤ (3/10)*(v4²+v5²),
E_norm(q,v) ≤ (3/10)*(q4²+q5²+v4²+v5²) ≤ 27/4000.
```

这给出实际原增益 exact-real full energy 的初始包络；比原标量小，且无需为
targeted cross term 付差值。但若消费者选择 `E_shift`，同一结论只变为

```text
E_shift(X0) ≤ 27/4000 + beta = 4082679/400000 > 1.
```

原点已经证明 threshold 1 的 shifted 初始包含为假，不是提高初始估计精度能解决的。

若确实选择 normalized targeted `V_eps`，在 X0 上 gain correction
`3*q2²+q3²` 恰为零，但 `eps*q'Mv` 一般不为零；该值级表达式与常数仍须单独绑定。
本节不需要也不声称 `V_eps=E_norm`。

### 不能用归一化换取原点包含后保留旧 coercivity

原增益的另一个 source slice 是 `q=t e2,v=0`：

```text
E_norm = A* (cos t-1) + (2/5)t².
```

在 `t=1/10`，用交错 Taylor 上界 `cos t≤1-t²/2+t⁴/24` 得

```text
E_norm ≤ -683199037/32000000000 < 0.
```

这排除把 shifted energy 的 `V≥(1/5)||q||²` 和 kinetic lower bound
原样用于 normalized energy。`PotentialSlice.lean::rational_configuration_negative`
已有同类 encoded-potential 结论；本轮第 2 节补的是 source 数学等式，尚无该等式的 Lean receipt。
此点不是 block-only X0，但关系到声称覆盖 remote coordinates 的 full active domain。

## 6. 最小 source witness 与收割顺序

1. **Origin-only 任务：** 指定实际 V 的 evaluator、常数、时间/坐标/lift 映射，
   给出单点 `V(0,0)≤1` 即可。不要求先证明全局 V 恒等式。
   若绑定到上述 normalized full energy，原点为 0；若绑定到 raw/shifted 能量，
   该单点请求被精确反例拒绝。CSV origin 虽满足不等式，也不会因此变成 full energy。
2. **真实 source 势能桥：** 将七个 frame heights 接到 `sourceContract`，证明
   `sourcePotential=auditedGravity+10791/4000` 与 `sourceG(0)=0`。
   这是具体有限代数叶，替代对任意域/任意势能的全局 derivative-transport 假设。
3. **真实初始 bound：** 在 `sourceAggregateM` 上证明本 review 的 block M_BB slice，
   绑定原 Kp、regularizer、exact-real compensation 和 block-only X0，
   得 `InitialBoundBinding X0 E_norm (27/4000)`。
   这是明确可检验的源公式，既不需要 Ve 的 source identity，也不要求全域 M operator upper。
4. **Barrier/target 迁移：** 使用同一个 V、常数、阈值、full domain、path 和 derivative budget。
   若从其他 storage 迁移，需域上的 equality 或方向正确的
   `V_target≤V_source+delta`，并将 delta 计入 initial/tube/threshold。
   full coordinate lower bounds须针对最终选定的 V 重证；`V_norm(0)=0` 不能替代它。

第 2–3 步是本轮建议优先形式化的 source 数学叶；第 1 步的实际 evaluator 选择及
第 4 步的真实 source-to-flow 绑定仍未给出。不存在可以自动收割为 closure 的当前实例。

## 7. 验证证据及版本

本轮只读 PowerShell source inspection、Python 3.13 的 Fraction CSV 解析，以及
SymPy 1.14.0 有理符号计算；Python 通过 stdin 执行并使用 `-B`，无导出文件。
没有运行旧 Julia/CSV producer、数值仿真、SDP、Lean/Lake 或远端 CI。
符号 checker 返回：全势能恒等式 residual 0；restricted mass 四个 circle-reduced
residual 全 0；`1402217/12000000<3/5`、`27/4000<1` 和上述反例有理界成立。

以下 source 文件为本轮读取版本，路径均相对本 review 开头的外部 source 根：

| 文件 | SHA-256 |
|---|---|
| `dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |
| `routeB_certificate_V.csv` | `cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601` |
| `routeB_export_traj.jl` | `35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf` |
| `routeB_compact_block_energy_barrier_audit.py` | `62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927` |
| `routeB_compact_energy_storage_to_block_audit.py` | `80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9` |
| `routeB_compact_targeted_nonlinear_strictification_audit.jl` | `41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1` |
| `routeB_compact_energy_power_rewrite_audit.jl` | `7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf` |
| `routeB_compact_closed_loop_energy_audit.jl` | `9631e727a76ea32651ba7ca8e175e632d1ded6cda98bba2fd81e33d24f959c09` |

相关已读 review：`review-T-P4-ACTIVE-ENERGY-ORIGIN-liuguanyi-20260907T1900.md`、
BODY6 `ACTIVEENERGYORIGIN` / `STORAGEIDENTITY` / `KEYEDSTORAGETRANSFER` reviews、
`review-T-P4-033-O1-body6-slice-actual-storage-align-20260908T052659Z.md`、
`review-GH-MATH-P4-TARGET-CAPS-codex-20260908T083041.md`。
引用它们用于接口定位，不继承其编译或 admission 状态。

最终保持 **pending / fail-closed**：没有实际 active V 选择、没有新 kernel receipt、
没有 Float64/source-to-flow 覆盖、没有 P4/P5/P8/M4 closure 或 registry promotion。
