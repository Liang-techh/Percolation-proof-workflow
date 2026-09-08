---
kind: review_result
review_id: review-GH-MATH-P4-CORRECTED-ACTUAL-ROWS-LOCAL-codex-20260908T104515
task_id: GH-MATH-P4-CORRECTED-ACTUAL-ROWS
source_agent: codex-corrected-actual-rows-lane
created_at: 2026-09-08T10:45:15-06:00
integration_status: pending
admission_label: pending
proof_status: CORRECTED_CHART_STILL_MISSING_ACTUAL_SUBSTITUTION_AND_DEFECT
corrected_source_written: false
source_binding_proven: false
physical_rows_recovered: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: supply same-configuration actual acceleration valuation and certified analytic-to-runtime/solve defect, then recover physical rows by full balance or signed weighted measurements
---

# Corrected full controller chart 不等于 actual rows4/5

## 1. 判定

在**假设已采用 corrected full controller expression** 后，现有 bridge/interval payload
仍不能提供同一 X/z/configuration 的实际 physical rows4/5 witness。
本轮不重复 controller omission 的系数计算，也不修改或生成 corrected 外部源码。

主要剩余断点是：

1. corrected expression 的解释恒等式尚不等于 actual acceleration 使它取零/指定 defect；
2. physical acceleration bridge 是坐标变换，不是把运行 acceleration 代入 force 方程的证明；
3. analytic interval radius 不认证 Float64 solve defect；
4. preconditioned rows4/5 即使有实际值，也仍需完整方程或两条 signed weighted constraints
   才恢复物理 rows4/5。这里不重复 rank 算术。

只新增本 review；无外部编辑、builder/checker 执行、Julia/Lean、solver、全回归或 admission。

## 2. 已读 artifacts 分层

外部根 P=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`。
本轮实际读取 JSON 元数据/结构及对应 builder/checker 文本：

| 对象 | 实际提供 | 不提供 |
|---|---|---|
| force_balance_bridge_dh_v1.json | rows4/5 的 centered expression、完整 controller coefficients、27 变量列表、6x13 A 的形状 | actual substitution、force residual 的实际值、rowspace recovery |
| check_force_balance_bridge_dh.py | 检查状态、行号、gains、hash、shape、counts 的代码 | 不代入实际 acceleration，不验证 solve/FD defect，不证明 physical row equations |
| physical_acceleration_bridge_v1.json | 六维 raw_from_lift_matrix、D=(1,2,3,6)、B=(4,5)、rational nominal energy/cross identities | 运行向量确为该 lift 值、同域 centered delta_a 的认证 bound、动力学方程 |
| half_active_vanis2_domain_probe.json | analytic mass/RHS intervals、X、contraction data、acceleration radius、候选 first slab | 运行 ahat 的 source refinement、Float64 backward error、实际轨迹落域证明 |
| descriptor_defect_contribution_audit_v1.json | gravity/coriolis/mass_variation 对已有 analytic remainder bounds 的分解 | runtime solve residual 或当前 vanis2 同域 defect bound |

centered bridge 明确保留 unresolved：physical acceleration lift 代入 A*x/delta_a、
Fourier equality-ideal bridge、positivity/flowpipe。
checker 即使未来返回 OK，其上述检查项也不能替代这些 obligations；本轮未执行它。

physical bridge 的 source_hashes 仅指向 decimal M0 CSV 与 rational complement CSV；
centered DH bridge 指向 analytic M/C/G、linear A、domain、dhport 等，二者无共有 source key。
这不证明它们不兼容，但没有一条共同 reference/valuation identity 可仅由这些元数据推出。
相同“physical”或“bridge”标签和兼容维度都不补齐该身份。

defect decomposition 的五个 domains 是 initial_analytic_slab、expanded_analytic_slab、
adaptive_domain_0/1/2；**不含 half_active_vanis2_domain_probe**。
本轮只读取其 domain 名与 producer 的分解算法，未验证巨大的 bound 数值。
不能不经域包含及模型一致性证明移植到当前 vanis2。

## 3. Corrected centered expression 的最小 actual-substitution 接口

令 chi=(q,dq,w) 为完整 13 维源状态，A_lin 为 centered 6x13 map，M_A 为 analytic
regularized mass（mu 只加一次），F_A 为 corrected DH analytic forcing。
用 eta_acc 命名 lift 变量，避免和 rowspace measurement y=Xz 混淆。

centered expression 的理想形式是

```text
E_ctr(chi,delta_a)
 = X [M_A delta_a+(M_A-M0)A_lin chi+M0 A_lin chi-F_A]
 = X [M_A(A_lin chi+delta_a)-F_A].                     (C)
```

第二行只是代数恒等式，甚至不要求 A_lin 是当前系统真实 Jacobian；
但已有 delta_a 的预算若依赖某个特定 A_lin/model，则必须保持该绑定。

令 ahat 为需要认证的 actual acceleration，定义 substitution discrepancy

```text
r_sub=ahat-(A_lin chi+delta_a),
z_A=M_A ahat-F_A,
X z_A=E_ctr+X M_A r_sub.                              (A)
```

因此只有另证 r_sub=0，才能从 centered expression 的**实际值**运输到 Xz_A。
再另证 E_ctr=0 或已知 defect，才获得相应零值或 defect 行。
给出 (C) 的语法表达式不证明 E_ctr=0。

若把 delta_a 定义成 ahat-A_lin chi，r_sub=0 的确可按定义成立；
但这不生成 E_ctr=0，也不证明旧 remainder bound 适用于这个 actual delta_a。
这条定义可以消除一个记号接口，不能消除动力学/solve 证据。

physical bridge 设 raw acceleration=T_lift eta_acc。正确接线还需
`ahat=T_lift eta_acc`，然后 `delta_a=T_lift eta_acc-A_lin chi`。
T_lift 的 energy identity 不给该 source valuation，也不证明其取值落在已认证域。
如果使用近似 lift，只能把 lift discrepancy 留进 r_sub 并预算。

## 4. Ideal analytic、exact-real FD 与 decoded runtime 是三种目标

### Ideal analytic

可在另有 invertibility 前提下定义 a_A=M_A^-1 F_A，使 M_A a_A=F_A。
这证明的是选定数学模型的加速度，不是 dhport 返回值 ahat，也不自动给轨迹/覆盖。
不能仅因得到 analytic 行等式就重新命名为 actual runtime rows。

### Exact-real FD

若目标是使用固定 h、mu 和明确实数运算定义的 FD 模型，需另给 M_FD/F_FD 的实际
解释及解方程关系。analytic 与 FD 差别仍须运输；实数 FD 方程本身不证明浮点执行等于它。

### Decoded runtime

dhport 明确用 Float64 mass/central differences，默认 mu=1e-6、h=1e-5，并返回
`Mq \ (tau-Cdq-Gq)`；G0 也在原点通过同一 FD routine 计算。
设 M_R、F_R 是实际调用中返回/组装的有限浮点数按实数解码后的对象，定义

```text
e_solve=M_R ahat-F_R,
z_A=e_solve+(M_A-M_R)ahat+(F_R-F_A).                   (S)
```

e_solve 是 decoded values 的精确实数 residual，不等于再用浮点计算一次 residual
所得的数，除非额外控制该评价舍入。F_R 必须清楚包含实际 RHS 组装的舍入；
不能有时取存储 RHS、有时取理想 tau-C-G，再把 assembly defect 丢掉。
bounded evaluation、FD discrepancy、G0/reference、controller 常数解码与 mass discrepancy
均按同一 convention 放入 (S)，不隐含 e_solve=0。

源码 backslash 的存在不提供这些数值界；本轮未运行解算器或进行误差分析认证。
若采用 backward-error 证明，也须明确其对这个库调用、norm、precision 和输入域适用。

## 5. Interval payload 为什么不能反推 actual equation

读到的 initial_analytic_slab.py 构造 C>=|I-XM_A|、d>=|X F_A|，
检查 weighted contraction kappa<1，并构造 acceleration supersolution。
该机制对满足 analytic 方程的 a_A 使用

```text
a_A=(I-XM_A)a_A+X F_A,
|a_A|<=C|a_A|+d.
```

如果 ahat 的 analytic residual 是 z_A，则实际关系多出一项：

```text
ahat=(I-XM_A)ahat+X F_A+X z_A,
|ahat|<=C|ahat|+d+|X z_A|.                            (I)
```

在同一正确 enclosure 与 contraction 前提下，另有 |Xz_A|<=b_z 才可用相应
`(I-C)^-1(d+b_z)` 型上界。旧 payload 中的 `(I-C)^-1 d` 不供应 b_z，也不能据
“ahat 恰好在该 box 内”推出其 residual 为零。
若先用该未扩展 acceleration radius 来界 (M_A-M_R)ahat，再用结果认证同一 radius，
就需独立闭合证据，不能循环使用待证 cap。

interval algebra 可以为以后 analytic existence/uniqueness/containment 提供条件，
但本轮未验证其依赖库、历史执行、向外包络或轨迹连接。
descriptor_defect_contribution_audit 分解的是已有 nonlinear remainder，不是 (S) 的
Float64 solve defect；名称带 defect 不构成同一对象。

## 6. 从 corrected preconditioned rows 到 physical principal packet

即使 (A) 已给实际测量 y=Xz_A 的 rows4/5，也不能仅凭这两行恢复 z_A,4/5。
消费已建立的 dual 结构，不重复 rank：

```text
z_A,4=beta*y4+w4,
z_A,5=kappa*y5+w5,
w4=alpha*y1+gamma*y6,
w5=eta*y1+theta*y2+iota*y3.
```

因此可选的真正 witness 入口是：

- 直接提供完整 (S) 的 source equation 与 defect，投影得到 z_A,B；或
- 提供 corrected rows4/5 的 actual measurement 值及两条 same-X signed weighted 值/界。

新 corrected expression 不自动提供 w4/w5；如还有 measurement evaluation mismatch，
需按前轮 recovery identity 保留其映射项。

得到 e_B=z_A,B 后，principal packet 才能写

```text
S_B=(M_A)_BB,
S_B ahat_B=F_A,B+e_B-(M_A)_BE ahat_E-(M_A)_B6 ahat6.
```

joint6 coupling 与远端 acceleration 必须保留；不需要也没有由此获得 joint6 消元。
随后 metric cap 必须对应 e_B/选定实际 residual；det(S_B)、完整 signed numerator、
固定 observable/units 和同 Omega 的 gate 都是独立义务。

## 7. 最小剩余 witness 与当前 disposition

| 所需 witness | 当前能否填充 |
|---|---|
| corrected chart expression | 本任务作为条件采用；现有 centered controller 完整，不代表完整 source 认证 |
| ahat 与 T_lift eta_acc、A_lin chi+delta_a 的实际代入 | 缺失；coordinate transform 与字符串 substitution 不够 |
| analytic/FD/runtime 同一配置与 (S) 的有效 defect | 缺失；无 solve/assembly/FD 联合界 |
| measured rows 与 physical rows 的恢复 | 仍需完整 balance 或两条 weighted actual constraints |
| 当前 full-state domain 上的 margin packet | det/numerator/metric/observable/trajectory witnesses 未提供 |

最有用的下一份 artifact 应明确选择 ideal analytic / exact-real FD / decoded runtime
中的目标，给 actual acceleration valuation 和有界 residual refinement，再生产同源物理两行。
不能仅重跑 corrected builder 或 metadata checker 就把上述缺口标为完成。

这是缺失 witness 判定，不是物理反例、实际不稳定或 packet 不可能存在的证明。
pending；无 source admission、registry promotion 或 closure。

## 8. 新检查 anchors

| 文件 | SHA-256 |
|---|---|
| physical_acceleration_bridge_v1.json | `01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede` |
| descriptor_defect_contribution_audit_v1.json | `65a4d583913e8cc7402a22b3ad5a09676fec74e7251b48e491f9f82f13cbbfd9` |
| half_active_vanis2_domain_probe.json | `28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e` |
| force_balance_bridge_dh_v1.json | `3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107` |
| check_force_balance_bridge_dh.py | `e6eae6cf23a492ecd758cfeb0c7b744301c41f7969c000cac10fe56c847e079b` |
| initial_analytic_slab.py | `97c96fb01bc9318af258a75d6b1371e3eef665fa760f401ce9f5a422ca164998` |
| build_physical_acceleration_bridge.py | `5424fb59df6b88b07c3577b907abfef7300113ec781f4cb0ed2fad2283cc10f7` |
| descriptor_defect_contribution_audit.py | `fbd6ff362469e3c353251870a9bbcd63ac467658234fb9163dd0fb36cdeab984` |
| dhport_lib.jl | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` |

文本、结构与 SHA 读取不构成 producer/checker 执行 receipt。
本轮只新增本 immutable review_result，外部源码/payload、旧 reviews、state/registry 均未修改。
