---
kind: review_result
review_id: review-GH-MATH-P4-SOURCE-ROWS-WEIGHTED-PACKET-LOCAL-codex-20260908T103648
task_id: GH-MATH-P4-SOURCE-ROWS-WEIGHTED-PACKET
source_agent: codex-source-rows-weighted-packet-lane
created_at: 2026-09-08T10:36:48-06:00
integration_status: pending
admission_label: pending
proof_status: BUILDER_CONTROLLER_OMISSION_AND_MISSING_ACTUAL_PACKET
source_binding_proven: false
actual_source_constraints_supplied: false
actual_source_rows_recovered: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: reconcile the missing signed controller terms before treating payload rows as measurements; then certify the common actual residual and weighted constraints without silently discarding defects
---

# Complete source rows 与 weighted constraints：当前不能形成 actual packet

## 1. 结论及只读范围

**当前 inspected artifacts 不能拼成同一 X/z/configuration 的 actual packet。**
阻塞不只是 missing rows1/2/3/6：现有 preconditioned rows4/5 的 controller support
与其声称的完整 X*(-tau_DH) 不一致，尽管相邻 bridge 的元数据和共有 source hashes 相同。
必须区分 builder 的表达式遗漏、measurement mismatch 和 actual physical defect。

本轮读取协调 companion `companion-GH-MATH-P4-ALL6-SOURCE-ROWS-20260908.md`，
并实际核对外部 P=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized` 下：

- `robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py`；
- `robot_formal_v1/exact_checks/build_force_balance_bridge_dh.py`；
- 对应两个 `interval_bounds/*_dh_v1.json` 与 `half_active_vanis2_domain_probe.json`；
- `routeB_dense_Mq/dhport_lib.jl` 的 gain、regularizer、tau 与 backslash solve 定义行。

只执行标准库 JSON/Fraction/hash 读取和 controller coefficient 对照，没有运行/导入
builder、Julia、Lean、solver、rank/inverse 检查或全回归。只新增本 review。
两条 weighted 恢复公式消费前轮结果，不重新证明 rank defect=2。

## 2. Fresh builder/payload 证据：共有 hashes 不能证明表达式相同

两个 builder 的外层都是 `for i in (3,4)`，两个 JSON 都只提供 rows=[4,5]。
内部 `range(6)` 是每行的 component 求和，不是输出六条实际 force rows。
本轮仅复核这两个 DH families；companion 对其他 families 的调查不当作本轮全量重查。

preconditioned builder 的 controller 片段是

```python
add(poly, ("q", i + 1), X[i][a] * kp[a] if a == i else Q(0))
add(poly, ("dq", i + 1), X[i][a] * (kd[a] + bfr[a]) if a == i else Q(0))
```

而完整的第 i 行控制项应为

```text
sum_j X_ij [kp_j q_j+damp_j dq_j-gwi_j w-g0_j].
```

这里 controller 自身是逐关节对角反馈，并不意味着左乘 dense X 后仍只含第 i 个坐标。
neighbor bridge 对 q/dq 使用 `[X[i][j]*gain[j] for j in range(6)]`，确实保留所有分量。
preconditioned builder 中 disturbance 与 constant 的代码仍对所有 a 求和；
本次已定位的遗漏是 q/dq channel，不应泛称所有 controller 项都缺失。

精确解析实际 JSON 得到：

| payload row | q/dq 实际 support | 缺失但应非零的 joint indices | bridge coefficients 与 X*gain 对照 |
|---|---|---|---|
| 4 | 仅 4 | 1,2,3,5,6 | 全部一致 |
| 5 | 仅 5 | 1,2,3,4,6 | 全部一致 |

每行每个 q/dq channel 缺五项，共 20 个已确认非零系数遗漏。
两 payload 的完整 controller metadata 相等，共有 source_hashes 无冲突；
仍不足以弥补这种 support-level 不一致。没有执行 builder 或证明整个多项式/运行语义。
bridge 的 controller 部分完整，也不代表 bridge 已证明六行或 actual acceleration 代入成立。
其 unresolved obligations 仍包括 physical acceleration lift/equality-ideal/positivity/flowpipe。

## 3. 正确的六行目标与三层误差

固定 analytic chart、一次 regularizer、同一 DH 配置和 actual decoded acceleration ahat：

```text
z_A = M_A^mu ahat-F_A,
F_A = -Kp*q-damp*dq+G0+GwI*w-C_A(q,dq)*dq-G_A(q),
y_A = X z_A.
```

完整实际方程是 `M_A^mu ahat=F_A+e_A`、`z_A=e_A`、`y_A=X e_A`。
定义 e_A 为 residual 可以使等式成立，但不证明 e_A=0 或其可用 bound。
`X z_A=0` 的六维字符串、symbolic polynomial identity 或 source hash 都不能填充这个零值断言。

### 层 A：builder 的已知 signed omission

对输出行 i=4,5 定义

```text
m_i=sum_(j!=i) X_ij*(kp_j*q_j+damp_j*dq_j).
```

在其他 mass/C/G/lift 通道均已正确解释的条件下，builder 表达式 b_i 满足
`b_i=(y_A)_i-m_i`，故 `(y_A)_i=b_i+m_i`。
这个 sign 来自 residual 中的 -tau_DH。修复的是确定的表达式遗漏，不是物理随机误差。
如果把 b_i=0 当作已知，即使它真的成立，也只能推出 `(y_A)_i=m_i`，不推出零。

最小 code 修复方向应是用每个 j 的 q_j/dq_j key 添加 X_ij*gain_j；
仅把外层循环扩成六行会复制该错误到六行。本轮不改源码、不重建或覆盖 payload。
修复后须新 producer/payload 版本及独立 source witness，不能覆盖旧 hash 后宣称旧 receipt 有效。

### 层 B：measurement / preconditioner mismatch

若实际记录还含评价误差 nu_i，写
`bhat_i=(y_A)_i-m_i+nu_i`，则 `(y_A)_i=bhat_i+m_i-nu_i`。
若测量用 X_actual 而恢复系数绑定 X0，还须保留 `(X_actual-X0)z_A` 的修正。
同样的字段名/域 hash 不证明 X 的加载值、索引、单位、source valuation 一致。

### 层 C：actual physical/model residual

若运行方程用 M_R、F_R，定义 `e_R=M_R ahat-F_R`，则

```text
e_A=e_R+(M_A^mu-M_R)ahat+(F_R-F_A).
```

analytic-vs-FD、controller、assembly/solve 差异须在这些项中一致计入。
dhport `exact_ddq` 实际返回 `Mq \\ (tau-Cdq-Gq)`，函数名不是 e_R=0 证明。
本轮只查看定义，不运行或认证浮点行为。
builder omission m 不能替代 e_A，也不能在 source discrepancy 中重复当作另一物理 defect。

## 4. 与两条 signed weighted constraints 的精确连接

消费前轮同一 rational X 的恢复 covectors，C=P_B X^-1：

```text
w4=alpha*y_A1+gamma*y_A6,
w5=eta*y_A1+theta*y_A2+iota*y_A3,  eta<0,
(e_A)_B=diag(beta,kappa)*(y_A4,y_A5)+(w4,w5).            (R)
```

系数沿用 `review-GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS-LOCAL-codex-20260908T102742.md`
及其 rank review；不重新估计、四舍五入或改写符号。
两条 NEW source obligations 是这些完整 y_A 的 weighted 值/界，不是 incomplete builder
的四个未输出行，也不是仅展开两个公式就已证明为零。

设真正的 source witnesses 给

```text
(bhat4,bhat5)=b+db,
(w4,w5)=c+dw,
D=diag(beta,kappa).
```

结合已知 omission 与 measurement error，得到

```text
(e_A)_B = D(b+m_B)+c + [D(db-nu_B)+dw].                (WP)
```

m_B 的 signed 值在 nominal RHS 内保留；若只控制它的 enclosure，应相应纳入剩余误差，
但只能计入一次。若加权测量本身也有误差，应加入 dw，不能默认 w 完全精确。

如果未来真的有完整六维 bhat=y_A-m+nu，才可定义
`what4=alpha*bhat1+gamma*bhat6` 等，并写整体 `P_B e_A=C(bhat+m-nu)`。
当前没有这些输出，不能拼造 missing rows 或假设它们与 row4/5 有同一个 defect 结构。

完整六行 actual witness 若已交付，本可直接投影得到 e_A,B；weighted 组合只是等价压缩。
四个 signed measurements 路线则可避免要求每个远端行单独为零。
两条路线均不把 builder 的“有六维 equation 文本”变成实际六行证据。

## 5. Principal residual packet：保持 joint6，而不是消除 source coupling

选定同一 configuration/Omega，B=(4,5)、E=(1,2,3)。从 (WP) 得

```text
S=(M_A^mu)_BB, u=ahat_B,
e0=D(b+m_B)+c,
delta_e=D(db-nu_B)+dw,
f0=F_A,B-(M_A^mu)_BE*ahat_E-(M_A^mu)_B6*ahat6+e0,
S u=f0+delta_e.
```

physical a6 与预条件 y_A6 不是同一个量。前者留在完整 RHS；后者出现在 w4 的 source
constraint 中。两者同时出现不是重复 charge，不得因加了 w4 就删掉 M_B6*ahat6。
principal 两行路线不需要 actual row6 为零或 d≠0，也没有得到 Schur elimination。

metric 必须控制本式的 delta_e 或完整 e_A,B，不能借用 nominal port-only H-budget。
若联合 measurement error 有已证 ellipsoid，可通过恢复 map 运输；若 metric/H/configuration
不同，须另给 comparison。m_B 如已并入 f0，不再按同一遗漏独立扣一次。

同一固定 observable nu_obs 的 packet 必须使用

```text
determinant=det(S),
N=nu_obs^T adj(S)*(f0+delta_e).
```

N 中 controller omission correction、actual a6/remote、weighted eta 的负号与 measurement
mismatch 必须整体保留。det(X)、preconditioner row support、port norm cap 不替代 det(S)
下界或这个 N 的 signed 同域包络；最终 observable/单位/导数绑定仍需独立交付。

## 6. 当前 intake 状态

| 检查层 | 本轮结果 |
|---|---|
| rational X / configuration 字段 | 两个 payload 的 controller metadata 与共有 hashes 一致；不代表 runtime 身份 |
| builder controller algebra | 已确认 rows4/5 的 20 个非零 q/dq 系数遗漏；neighbor bridge 对应系数完整 |
| 六行输出 | 两个已检查 DH payload 都只输出 rows4/5；没有 complete-six-row actual packet |
| measurement y=Xz | 被 omission 阻断直接认同；其他通道及 actual valuation 还需独立证明 |
| 两条 weighted constraints | 只有待填公式，没有实际同源 signed 值/defect witness |
| physical row recovery | 条件式 (WP) 已明确；实际 e_A,B 尚未认证 |
| det/numerator/metric/observable | 没有本轮新证据；不能从前述 metadata 自动推出 |

下一步应先在明确授权的新 source 版本修正完整 signed controller polynomial，
同时选择“实际六行方程”或“正确已有两行加两条 weighted constraints”的证明入口，
并保留实际 defect。不能先宣称 source 恢复、再把 mismatch 留作无关后续问题。

本结果是 builder/source binding obstruction，不是物理反例或不可行性证明。
无 actual source admission、无 registry promotion、无状态变更。

## 7. 本轮字节 anchors

| P 下路径 | SHA-256 |
|---|---|
| `robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py` | `925f3818146e7e4154bff07ef16cc6c93db8609ae15be20a8551b4f15dca1c5f` |
| `robot_formal_v1/exact_checks/build_force_balance_bridge_dh.py` | `a5082a12d267380a01d9e9c7965fbf17fa7fdb62c2d963110da38a192470aa15` |
| `robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json` | `28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e` |
| `robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json` | `e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48` |
| `robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json` | `3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107` |

所有 hashes 与 coefficient 对照是只读检查，未证明历史 builder 执行、依赖包络或浮点语义。
旧 payload/source/review 均保持原样，仅新增本 immutable review_result。
