---
kind: review_result
task_id: P5-098-ANCHOR-BUDGET-INSTANTIATION
review_id: review-P5-098-ANCHOR-BUDGET-INSTANTIATION-20260908T202703Z
source_agent: Codex-source-audit
created_at: 2026-09-08T20:27:03Z
inspected_commit: 2b1e03aa23cb28c462bfc3c9b67616fae38d827c
status: MREF_LOCATED_REFERENCE_CONTEXT_MISSING
integration_status: pending
admission_label: pending
actual_anchor_budget_verified: false
conditional_initial_ball_arithmetic_checked: true
source_binding_proven: false
lean_run: false
sampling_run: false
producer_run: false
state_registry_mutated: false
registry_eligible: false
P5_closed: false
---

# P5-098：实际 Mref 已定位；不能凭 nominal_f 实例化 nominal reference

## 结论

当前查到的 source/context 足以固定 residual evaluator、Mref 的真实文件和
block/remote 索引；**不足以读取一个已选定的 actual qbarB/vbarB reference 实例**。
因此不能诚实地报出 actual `pD+pB<=rho` 已通过。

这不是预算不等式的反例。最小缺口是同一个实际 context 中的 nominal 四坐标及其
reference identity，并为 full-state domain 固定 rho；若要在一般时刻检查，还需
actual remote 八坐标或其已认证预算上界。

已用 Fraction 检查真实 CSV token 的质量参考值，并得到有源初始球上的条件预算：
若另行绑定 nominal 与 actual 的相同初值，则
`pD(actual(0))+pB(nominal(0)) <= 27/800 < 28/5`，余量至少 `4453/800`。
这里相同初值仍是待绑定条件，不是已交付的实际 nominal 实例。

本轮只新增本 immutable review；未改 state、registry、shared scripts 或 source，
未运行 Lean/Lake、Julia、producer、求解器、轨迹或采样。只读了一个既有 deterministic
origin regression 行以辨别其字段，不将该行当作证明。Fraction 运算仅输出 stdout。

## 1. 实际 source/context 查到什么

路径根：

- E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`
- F = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1`
- W = `C:/Users/z5242/Desktop/重构版/工作流`

| 路径及行号 | 本轮实际读取的内容 | 不能由此推出 |
|---|---|---|
| E/routeB_descriptor_residual_interface.jl:22–30 | Float64 读取 M0 CSV，取 (4,4)/(5,5) 对角；固定 IVAL、KP、KD、GW、KC、G0 | Mref 不是 nominal position/velocity trajectory |
| 同文件:32–38 | `nominal_f(q,dq,w)` 为六维向量场，4/5 具有 KC cross terms | 没有 qbar/vbar 初值、nominal solution、referenceKey 或 lbar 表 |
| 同文件:40–59 | 完整 M\R solve；`l=diag(IVAL_B)*f_B-Mref*a_B` | 不生成 actual-minus-nominal context |
| 同文件:62–68；E/routeB_descriptor_residual_interface.csv:1–2 | 预置 origin q=v=0,w=0 的回归输入；CSV 原点行及有限 block 字段 | 无 nominal reference；无 t/c；CSV 本身还不含 remote 坐标 |
| E/routeB_interval_branch_bound.jl:37–43,57–67 | full-six-q/full-six-v 权重为声明的精确 3/2、4/5 | 不是 exporter 的 block-only p |
| 同文件:187–198,426–432 | full-domain root 与 w box；rho 对应 runtime eta；默认 eta 是 2.7，由 P3_BB_ETA 可覆盖 | 不能默认此 runtime 已选择 rho=5.6 |
| E/routeB_export_traj.jl:41–46,89–109,135–166 | T=1、R_init=0.15、eta_star=5.6、joint limits、w=cw*t 与 actual 数值积分 | 不是 nominal-reference producer 或 certified flowpipe |
| 同文件:189–212 | 输出状态表仅 traj,t,q4,q5,dq4,dq5；主表仅 V/tube/block-p/ratio 等 | 没有 pD 的 remote 八坐标，没有 cw/w，也没有 paired nominal 四坐标 |
| E/routeB_compact_nominal_descriptor_interface.csv:2–6 | B=(4,5)、D=(1,2,3,6)；所谓 nominal 是 remote acceleration equation | 不能把 aDnom 当作 qbarB/vbarB |
| F/interval_bounds/active_angle_domain_v1.json:3–10 | formal=false；imported analytic first-slab scope；初始半径明确为 3/20 | 不认证 FD source，也不提供 nominal reference |
| W/agent_review_inbox/review-T-P5-018-guyuefangyuan-20260907T0634.md:49–63,259–276 | nominal 同 forcing 方程及“若相同初值”的条件接口 | review 的假设不是实际 reference 数据 |

另外读取 W/artifacts/task_GBB_fullstate_descriptor_gate_20260907/contract.json，
其 state/source/full-domain 字段仍是设计接口，不是填好值的 anchor packet。
对 E 的非 debug Julia/JSON/TOML reference 名称及相关 nominal/reference 数据文件做了
定向检查，并检查 W 的相关 P5/anchor/reference 接口；未找到可与此 evaluator 配对的
qbarB/vbarB/referenceKey。此结论限于本轮查阅范围，不声称整个磁盘不存在 reference。
搜索到的 body-frame vbar 和 nominal distal acceleration 不是这里的 nominal velocity。

## 2. Mref：真实 token 与理想参考不能混用

E/routeB_Mq_M0.csv 第4行第4列、第5行第5列分别为：

```text
0.116667666666667
0.05018475
```

将这两个十进制 token 精确解释为有理数，Fraction 得到

```text
Mref_token = diag(116667666666667/1000000000000000,
                 200739/4000000).
```

与另外常见的理想参考 `diag(350003/3000000,200739/4000000)` 比较，差为
`diag(1/3000000000000000,0)`，不是完全相等。

该 Julia source 实际用 Float64 读 CSV；本机 Python 对相同 token 作 binary64 解码为

```text
2101697840504747/18014398509481984
452024042799363/9007199254740992.
```

这是本机 token 解码，不是运行 Julia 的 parse/solve receipt，也不是把 CSV decimal
或 compact rational reference 认证为部署 source 的 exact-real 同一对象。
E/dhport_lib.jl:27–29 固定 regularizer=1e-6、FD step=1e-5；这些语义也不能省略。

重要的是，当前 scalar hybrid budget 的 p 权重是 **3/2 和 4/5**，不是 Mref。
Mref 接线用于后续 residual/reference 方程；重算或替换 Mref 不能补上缺失的 qbar/vbar。

## 3. 已完成的 Fraction 级窄检查，以及适用条件

B=(4,5)、D=(1,2,3,6)，定义同上一份 anchor-domain review：

```text
pD = (3/2)*sum_D q_i^2 + (4/5)*sum_D v_i^2
pB_nom = (3/2)*(qbar4^2+qbar5^2) + (4/5)*(vbar4^2+vbar5^2).
```

### 3.1 源码原点回归输入：只确定了 actual 一侧

在 S:63 明确写出的 q=v=0,w=0 输入，`pD=0` 精确成立。
但该行没有 qbar/vbar/reference，所以 `pB_nom` 仍为 UNBOUND，而不是 0。
G0 是 gravity evaluation reference，不是 qbar=vbar=0 的 selection receipt。
不能据此把 `0+0<=28/5` 报成 actual anchor budget。

### 3.2 有源初始球：给出可直接复用的条件预算

取 F 的明确有理初始球几何
`sum_i(q_i^2+v_i^2) <= (3/20)^2 = 9/400`。
由于 `4/5<=3/2`，纯代数给全状态 `p<=27/800`，也给 `pD<=27/800`。
这是初始集合的几何事实；F 的 imported analytic 模型不是部署 FD 模型，不能顺带
搬运它的 slab/flow 结论。exporter 的 Float64 采样也不提供整个球的 certified coverage。

若 nominal 与 actual 具有 T-P5-018 所要求且实际绑定的同一初值，则初始 hybrid=actual，
于是无需求解 nominal ODE 就有下列**条件式初始时刻**检查：

```text
R^2 = 9/400
pD(actual(0))+pB(nominal(0)) = p(actual(0)) <= 27/800
rho = 28/5
rho - 27/800 = 4453/800 > 0.
```

Fraction 对上述等式和比较全部通过。rho=28/5 在这里是沿用上一份 review 与
exporter target 的明确理想域选择；不是对 branch-bound 默认 eta=2.7 的改写。
使用此检查仍需给 full-state domain 的实际 rho/context key。

若 reference 初值并不匹配，则由初始球只能给一个保守的充分条件：
`pB_nom<=4453/800`。该数字是 nominal budget 的可用上限，**不是已有 nominal
预算的测量值或证明**。它保留了“actual remote budget + nominal block budget”语义。
此初始球上界不延伸为 t>0 的 actual pD 上界。

本轮精确算术：Python `Fraction`，仅通过 stdin 运行，输出 stdout；无脚本/数据文件新增。

## 4. 最小补交项：分开 scalar 检查与后续 P5 admission

要得到第一条真正的 actual scalar 检查，只需上游补齐一个同 context 的记录：

1. **Reference binding**：qbar4,qbar5,vbar4,vbar5 的确切值或有理 enclosure；
   其 source/hash、referenceKey 与该时刻 t 的身份。若走初始匹配路线，提供
   nominal initial data 与 actual initial data 的同一性即可，不必先给全轨迹。
2. **Actual remote budget**：同一 actual 的 q1,q2,q3,q6,v1,v2,v3,v6，或有源的
   pD 上界。一般时刻不能用 block-only state_samples/轨迹主表恢复这些字段。
3. **Domain/context key**：选择 full-state 3/2,4/5 椭球而非 block-only p；固定 rho
   的 exact/interval 解释及该 runtime 配置。actual/nominal 保持同 t,w,c/input identity。

对给出的单点或盒，可以随后只用 Fraction 检查
`upper(pD+pB_nom)<=rho`，同时检查 nominal block joint limits。若数值上不通过，
应报告该 context 的负 slack；若字段缺失，保持 pending，不能填0、删 actual 点或换域。

`lbar`、nominal 方程、error scaling、source reification/Float64 defects、完整 graph lift、
derivative-path cover/FD halo 与 actual flowpipe continuation 不参与这个 scalar 的裸计算，
但仍是接回 P5 centered residual/closure 的独立义务。本 review 不把它们全部混成
“必须先有完整 nominal trajectory 才能检查一个 anchor”的过强前提。

## 5. 本轮读取的 SHA-256

| 路径 | SHA-256 |
|---|---|
| E/routeB_descriptor_residual_interface.jl | d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24 |
| E/routeB_Mq_M0.csv | 28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40 |
| E/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| E/routeB_interval_branch_bound.jl | a2bd89c923ab646bcb138372e4c74a5980afe5d5906f21080b6781e03051869c |
| E/routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| E/routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| E/routeB_descriptor_residual_interface.csv | ed10d0335debacd670a26871cad9ce51fc871cb86f6ae956125aeae3dee00e24 |
| E/routeB_compact_nominal_descriptor_interface.csv | ab36538b5aa9ab9b62012d2ab90a1e20e3a226110b97f95d5e9d270f0b5a0375 |
| F/interval_bounds/active_angle_domain_v1.json | c1637ae0160c0535b6be1dc147602266b43564f76806aa9df3178c6aec0c6cba |
| W/artifacts/task_GBB_fullstate_descriptor_gate_20260907/contract.json | 2660a5ea347e1c7df317f6226c429f30412c52c960e3bcd002e1ad795bacf4f1 |
| W/agent_review_inbox/review-T-P5-018-guyuefangyuan-20260907T0634.md | af7492a242d4fadf9f95bbd677725cc65ef94478e6b7020c64496f5104a39270 |
| W/agent_review_inbox/review-P5-CENTERED-ANCHOR-INSTANTIATION-20260908T200937Z.md | ad847dc2b2ac822a4bce1c2388ee32e211a22a665e7ed456966fed58b365c2eb |
| W/agent_review_inbox/review-P5-ANCHOR-DOMAIN-INCLUSION-20260908T201509Z.md | b4838d514846244073e708ca98b970a2c5dbf8faec2e908b0e747212323b620c |

未取得 actual reference/context receipt，故 actual_anchor_budget_verified=false。
没有 concrete K_path、P5 closure、source coverage 或 registry admission 声称。
