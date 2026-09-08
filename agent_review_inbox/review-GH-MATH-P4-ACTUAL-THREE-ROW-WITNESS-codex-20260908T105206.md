---
kind: review_result
review_id: review-GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS-codex-20260908T105206
task_id: GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS
source_agent: codex-actual-three-row-refresh
created_at: 2026-09-08T10:52:06-06:00
integration_status: pending
admission_label: pending
proof_status: CURRENT_CANDIDATES_DO_NOT_SUPPLY_RUNTIME_ACTUAL_WITNESS
source_binding_proven: false
actual_preconditioned_rows456_supplied: false
actual_signed_weighted_constraints_supplied: false
physical_rows_recovered: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: obtain a same-call decoded solve/refinement witness or a separately defined exact-model witness; retain joint6 defect and distinguish preconditioned row6 from physical row6
---

# Actual preconditioned rows4/5/6：当前候选仍缺运行语义 witness

## 1. 刷新结果与范围

**没有在本轮检查范围内找到同一 full-state configuration/domain 的 actual
preconditioned rows4/5/6 与 signed weighted constraints packet。**
当前材料最多提供 analytic candidate enclosures、symbolic/nominal transforms 和
corrected-builder 规格，不能推出 runtime actual 行方程。这里的“不能推出”限定为
当前证据的逻辑能力，不是证明未来不可能补齐，也不是物理反例。

本轮读取新协调记录 `companion-GH-MATH-P4-CORRECTED-BUILDER-SPEC-20260908.md`，
并刷新外部 P=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`
下已知 domain、两个 DH row payload、physical acceleration bridge 与 producer/source hashes。
在 robot_formal_v1 文件名与 interval_bounds 文本中定向查找 runtime、solve residual、
backward error、joint6 defect、rows456；没有命中可新增消费的 actual receipt。
这是 bounded search，不是全机器/全仓库证据不存在证明。

没有读取/修改 state 或 registry，没有修改旧 artifacts、source 或其他 agent 文件。
只新增本 review；无 Lean/Lake、Julia、builder/checker、solver 或全回归执行。

## 2. 本轮实际版本与新增规格

- force_balance_bridge_dh_v1.json 仍是 rows=[4,5]、formal=false，并明确保留
  physical acceleration substitution、equality-ideal、positivity/flowpipe obligations。
- preconditioned_force_balance_identity_dh_v1.json 仍是 rows4/5；本轮哈希与前轮相同。
  已知 controller omission 的算术不重复。新规格将其 complete-DH-equation claim
  视作 semantic-rejected 历史候选；本轮不修改其标签或文件。
- corrected-builder companion 状态为 VERSIONED_BUILDER_SPEC_NO_SOURCE_REPAIR，
  明确没有 source repair。已检查 interval_bounds 下 `*force*dh*v2*` 无文件。
  因而不能把规格当作 corrected six-row producer、payload 或执行 receipt。
- 两个 builder 与 dhport_lib.jl 字节均未变；本轮不再次审查遗漏系数。
- 当前 domain 仍为 half_active_vanis2 的 analytic first slab，formal=false。
  本轮只固定该域，不混入 earlier eta/box83 的预算，也不引入新域。

Omega 的记录是六维 angle radii
`(9/20,19/50,37/100,19/50,37/100,9/20)`、各 |dq_i|<=3、|w|<=2。
initial radius=3/20 和 step=1/512 是独立记录，不能自动证明 runtime trajectory 落在 Omega。

## 3. 三种“row6”必须分开

### Lift coordinate 的第六行

physical_acceleration_bridge_v1.json 中 raw_from_lift_matrix 的第六行实际为
`[0,0,1,0,0,0]`，lift order 为 `(y1,y2,y3,z,a4,a5)`。
为避免与预条件 y 混淆，记 lift 为 eta_acc。该行只给

```text
ahat=T_lift eta_acc  =>  ahat6=eta_acc,3.
```

它不证明左侧 source valuation，也不说明 eta_acc,3 为零或有合法界。
它不是物理 joint6 force balance，更不是其 solve defect 证据。

### 物理第六行 defect

同一 analytic chart 下 `z_A=M_A ahat-F_A`，物理第六行是

```text
(z_A)6=(M_A)6,* ahat-(F_A)6.
```

它包含全部 acceleration/coupling；把 a6 的一个坐标公式代入不证明该残差为零。

### 预条件第六行 measurement

同一 X 下 y=Xz_A，则

```text
y6=sum_j X6j*(z_A)j.
```

这不是 z_A,6。即使物理第六行 defect 为零，远端 defects 仍可能贡献 y6；
即使 y6=0，也不能单独推出 physical row6 为零。
两条 weighted constraints 中使用的 y6 必须是这个 preconditioned measurement。

## 4. 一个实际可复核 witness 必须绑定的对象

固定同一次 runtime call 的输入 chi=(q,dq,w)、configuration、mu、FD step、X 和
decoded finite values：实际 mass M_R、实际 assembled RHS F_R、返回值 ahat。
令 M_A、F_A 是明确的 corrected analytic chart；定义

```text
e_solve=M_R ahat-F_R,
e_model=(M_A-M_R)ahat+(F_R-F_A),
z_A=e_solve+e_model,
y=Xz_A.                                               (R)
```

physical joint6 与 requested preconditioned rows 需分别使用

```text
z_A,6=e_solve,6+(M_A-M_R)6,* ahat+(F_R-F_A)6,
y_i=X_i,* (e_solve+e_model), i=4,5,6.
```

浮点 assembly 与 F_R 的定义必须统一；不能把已舍入存储 RHS 与理想 tau-C-G 混用。
用浮点重新算一个 residual 仍需评价误差界，不等同 (R) 的精确实数 residual。
同源 e_model 包含 FD/G0/reference/controller 与 mass discrepancy，不仅 joint6 一项。

最小**单点**可复核运行证据可保存这次输入/configuration、M_R/F_R/ahat 的完整 bit-level
身份并做独立 exact-dyadic residual 或可信 enclosure；这样才有该调用的 e_solve。
当前 payload 不保存这样一组同次调用的 values/receipt。
即使将来有一个单点 receipt，也不是全 Omega witness；域上还需统一误差定理/包络
或有覆盖证明的逐 cell receipts。本轮不运行或采集这些数据。

若目标改为 exact-real analytic/FD 解，应明确声明另一语义，给方程解的存在/逆身份。
它可以为该数学模型提供行方程，但不得把它认作 Float64 ahat。

## 5. Acceleration substitution 仍是独立接口

取 centered map A_lin 与 delta_a，定义

```text
r_sub=ahat-(A_lin chi+delta_a),
E_ctr=X[M_A(A_lin chi+delta_a)-F_A],
y=E_ctr+X M_A r_sub.
```

corrected full controller chart 只修复 E_ctr 的表达式。
实际代入需要 ahat=T_lift eta_acc 与 r_sub=0 或其有界值；即使 r_sub=0，
也仍须 E_ctr 的 actual 值/defect，不会由表达式正确自动得到 E_ctr=0。
定义 delta_a=ahat-A_lin chi 可以消掉 r_sub，但不能给 delta_a 的既有 bound 或 force equation。

analytic interval 的 radius 按其模型方程构造；对当前 ahat，
`|ahat|<=C|ahat|+d+|Xz_A|` 多出 actual residual 项。
没有同源 |Xz_A| 证据时，不能将旧 analytic radius 当作 runtime acceleration/defect 认证。
当前 physical bridge、domain 和 centered payload 都未供应 (R) 的联合证明。

## 6. Requested rows456 与 signed constraints 的合法组合

消费前轮同一 rational X 的 dual covectors，不重新做 rank：

```text
w4=alpha*y1+gamma*y6,
w5=eta*y1+theta*y2+iota*y3,
z_A,4=beta*y4+w4,
z_A,5=kappa*y5+w5.
```

如果有同源 (R)，这些 weighted 值可直接由 X(e_solve+e_model) 形成并认证，
保持 eta 的负号与 correlation。此时不必单独宣称所有 y 行取零。
如果只交 requested y4/y5/y6 的测量值，仍缺 w4 中的 y1 信息及 w5 的加权信息；
已给 y6 可以减少 w4 的未知部分，但不会免费产生两条 source constraints。
从 full equation 可直接投影 physical rows；从 partial measurements 需对应 weighted recovery。

当前既无 actual y456 witness，也无同源 w4/w5 值或 bounds。
这些公式只是定义/恢复接口，不是实际 source 已满足零约束。

得到 e_B=z_A,B 后才有保留 coupling 的 principal packet：

```text
(M_A)_BB ahat_B=F_A,B+e_B-(M_A)_BE ahat_E-(M_A)_B6 ahat6.
```

principal rows 不需要 row6 为零或 Schur pivot 条件；actual row6 的取得仍有价值，
但不能以“补齐三行”为名将 joint6 coupling/defect 省略。
随后还需同域 metric、det/numerator、observable witnesses。本轮不制造这些数据。

## 7. 当前候选为何不足：不是再找一个状态数值

已检查 payload 的输入/输出只固定 analytic expressions、候选域/变换和部分行结构，
没有约束 actual call 的 M_R/F_R/ahat 或统一 refinement。
现有 transforms 对自由 lift 向量仍是代数恒等式；改变未绑定的 acceleration valuation
不改变这些文件的 identity/metadata，却改变 M_A ahat-F_A。
因此这些 identity/metadata 无法逻辑上决定 actual residual 的零值或所需 bound。
这是模型层的未绑定变量说明，不构造物理状态、不声称可达反例。

本轮核心缺口定位为同配置 runtime-to-chart witness (R) 及 actual substitution，
而不是 corrected controller coefficient、有限维 rank 或新的 scalar absorption。
下一份有辨别力的 artifact 应绑定 actual call 或提供全域 refinement 定理，
显式包含 joint6/远端 solve 与模型差异；仅重跑 builder 或 metadata checker不足。

## 8. Fresh anchors 与最终状态

| 相对 P 路径/对象 | SHA-256 |
|---|---|
| interval_bounds/half_active_vanis2_domain_probe.json（robot_formal_v1 下） | `28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e` |
| 同目录 force_balance_bridge_dh_v1.json | `3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107` |
| 同目录 preconditioned_force_balance_identity_dh_v1.json | `e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48` |
| 同目录 physical_acceleration_bridge_v1.json | `01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede` |
| robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py | `925f3818146e7e4154bff07ef16cc6c93db8609ae15be20a8551b4f15dca1c5f` |
| robot_formal_v1/exact_checks/build_force_balance_bridge_dh.py | `a5082a12d267380a01d9e9c7965fbf17fa7fdb62c2d963110da38a192470aa15` |
| routeB_dense_Mq/dhport_lib.jl | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |

JSON/hash/定向文本检查只读，无 Lean/Lake、实际求解或 formal validation。
最终 pending / missing-actual-witness；不声称 VERIFIED、物理 closure 或 source admission。
