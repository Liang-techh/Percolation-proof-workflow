---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-OBSTRUCTION-20260914T211034Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: codex-independent-source-interface-audit
created_at: 2026-09-14T21:10:34Z
inspected_commit: 53e497f9d09de120db0f16da87b7d6e07e0e6e00
status: EXACT_SAME_CONFIGURATION_OBSTRUCTION
integration_status: pending
admission_label: pending
actual_source_packet_found: false
source_binding_proven: false
runtime_verified: false
signed_output_instantiated: false
lean_lake_run: false
synthetic_helper_run: false
state_mutation: false
registry_mutation: false
requested_action: supply one actual residual refinement and source-derived affine map with matching reference and signed bounds; do not substitute old absolute port bounds
---

# P4 signed Schur：同配置实际 source witness 仍缺

结论：所读材料不能组成同一个实际配置下的 y=Xz_A、d=A y+b、H=M0_CC^-1、
u/s/D packet。H 的 source formula 已定位，不能再笼统称为“不知道 dense metric”；
第一缺口仍是实际残差 measurement/refinement 与选定 port-defect 的 source identity。

本轮增量是把现有 block456 descriptor 的远端行化成一个明确的**条件式 source-map**
公式，并定位 corrected-DH 与旧 factorized controller 的精确设计增益差。
它们说明 J_d/b 应如何来自 source，而不是从同维矩阵或 synthetic helper 里任选。
没有计算/输出实际 A,b,y、signed caps 或 gate pass。

恢复工作后重新读取并计算 11 项输入 SHA-256，均与本任务 2026-09-08 暂停前读值相同。
截至此次有界检索，相关 external interval 输出未出现新的 capture/signed packet；
这不是整台机器或所有外部任务的穷尽不存在证明。只写本 immutable review。

## 1. 本轮实读来源与状态

外部根 E：
C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized。

- E/routeB_dense_Mq/dhport_lib.jl：mass regularizer、FD C/G、tau 和实际 backslash solve。
- E/routeB_dense_Mq/routeB_factorized_descriptor_model.jl：
  analytic M/C/G CSV 的加载与旧 controller 参数（187–200 行）。
- E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl：
  C=(4,5,6)、D=(1,2,3)、MDD/MDC/MCD/M0CC、nominal_eq/port_eq/total_eq。
- E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl 与其 CSV：
  H、ell=lBase、beta、direct_total 和旧 absolute-port Young 分支。
- E/robot_formal_v1/interval_bounds 下 domain、corrected force bridge、
  preconditioned identity、physical acceleration bridge、combined remainder 五份 JSON。
- workspace/examples/routeb_p4_schur_joint_threshold_lean/
  NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean：只读其真实 hypothesis。

旧 source-followup、signed-affine、metric-reference 与 actual-cell review 用于定位；
本次列出的 source/JSON 字段和 hash 已直接复核。未运行 helper、Python 数值程序、
Julia、Lean/Lake、producer、solver、regression、integrator 或任何 runtime capture。
源文件存在与哈希匹配不证明它们就是某次实际调用加载的字节；运行配置仍缺。

## 2. 最接近的配置并非一个完整已绑定实例

vanis2 domain 明列 rational 6x6 preconditioner X；
angle radii=(9/20,19/50,37/100,19/50,37/100,9/20)，velocity_radius=3，
step=1/512。scope 是 imported analytic model、initial ball 0.15、
measurable |w|≤2、first slab only，formal=false。

这些是已存候选域字段，不是实际 y 的 six signed intervals，也不是 trajectory coverage。
rhs_intervals 是 forcing/RHS 的界，acceleration_radius 是加速度量；
不能给它们改名为 lo≤Xz_A≤hi。

corrected force bridge 的 source_hashes 指向同一个 domain 和 dhport 源字节；
但其 rows=[4,5]，linear_map_A_shape=[6,13]，substitution 为 a=A*x+delta_a。
它既没有当前任务的 3x6 port chart，也明确留下 physical lift substitution、
equality-ideal、positivity/flowpipe 义务。physical acceleration bridge 则采用
B=(4,5)、D=(1,2,3,6)，不是 block456 的分块。

## 3. 从现有远端 descriptor 得到 J_d/b 的最小条件式候选

以下为符号推导，不是 new synthetic numerical instance，也不是已交 source witness。
采用原 source 的 block order C=(4,5,6)、D=(1,2,3)。为避免 A 重名，定义：

```text
M_A = 被选择的 analytic/reference full mass（包含该模型的一次 regularizer）
F_A = 同一 corrected source convention 的 full RHS
ahat = 实际返回 acceleration，作为待绑定的同一向量
z_A = M_A*ahat - F_A

N = (M_A)_DD, K = (M_A)_DC, K0 = (M_A(0))_DC, Cmat = (M_A)_CD
aC = E_C*ahat
Fref_D = 明确选定的远端参考 RHS
N*eta_D = Fref_D - K0*aC
vD = E_D*ahat - eta_D
r_actual = Cmat*vD
```

N 的可逆性、eta_D 的这个定义和 r_actual 的这个物理/参考解释均须实际提供。
它不是源码独立变量 vD456 自动具有的语义。远端行相减给出

```text
N*vD + (K-K0)*aC = E_D*z_A + (E_D*F_A - Fref_D).
```

于是，若把名义 port 定义为源码 homogeneous operator 对同一个 aC 的作用，

```text
r0 = -Cmat*N^-1*(K-K0)*aC
d  = r_actual-r0
J_d = Cmat*N^-1*E_D                    : R6 -> R3
b   = Cmat*N^-1*(E_D*F_A-Fref_D)        : R3

d = J_d*z_A+b.
```

若另给 X 可逆、实际 y=Xz_A，则

```text
A_chart = Cmat*N^-1*E_D*X^-1            : R6 -> R3
d = A_chart*y+b.
```

因此：

- J_d 不是 E_C，也不是随便一个 3x6 selector；它从远端行和相同 mass block 解出。
- b=0 只能来自 Fref_D=E_D F_A，或另证相应 image 为零；缺 reference 字段不能默认零。
- r0 必须使用同一实际 aC。若 r0 来自别的 nominal acceleration，差项还需显式保留。
- 该推导的 d 是**名义减除 port 的变化**。若目标 d 是全 l_actual 的变化，还必须绑定
  l_actual=ell+r_actual，并核对 ell 的参考差项；不能用此式自动代替 total-force identity。
- N,Cmat 随 q 变化。即使 X、H 固定，A_chart 通常仍是状态函数；
  现有 fixed rational affine-box helper 不能通过一次 freeze 证明全 slab/cell 的 bound。
- 若 measurement 是 yhat=y+xi，正确 offset 为 b−A_chart*xi，不能丢掉误差或改变符号。

这给出一个可检验的 source-map 路径，但本轮没有把缺失的实际向量、域内可逆 witness、
模型/运行身份和 reference contract 倒填为已知。

## 4. 具体 controller seam：同名 DH 不等于同一 F/ell

直接读取的 rational factorized source 使用：

```text
Kd_fac = (4,5,3,1,2,3)/5
Bfr_fac = (1,2/5,7/20,3/10,1/4,1/5)
Kd_fac+Bfr_fac = (9/5,7/5,19/20,1/2,13/20,4/5).
```

corrected-DH JSON 的 Kd_plus_Bfr 为

```text
(13/10,11/10,19/20,4/5,13/20,1/2).
```

这与 dhport 文件的设计十进制 Kd/b_fr 表达式对应。对**相同 analytic M/C/G、
同一 q/v/w、同一其余 force convention**，其有理设计阻尼差是

```text
DeltaD = damping_fac - damping_DH = (1/2,3/10,0,-3/10,0,3/10)
F_fac - F_DH = -diag(DeltaD)*v.
```

不能把该设计级 identity 冒充 binary64 运算逐位 identity；实际 rounding 和 FD 仍需 refinement。

若在第 3 节取 F_A=corrected analytic DH、Fref_D=旧 factorized analytic RHS 的 D 行，
则 controller-only offset 必须保留

```text
E_D F_A - Fref_D = (v1/2,3*v2/10,0)
b_controller = Cmat*N^-1*(v1/2,3*v2/10,0).
```

同时 block456 的 lBase 直接用旧 Kd/Bfr 生成 fC456。
保持其余 nominal q/cross/reference 项和同一 aC 不变，仅改 corrected damping 时，

```text
ell_fac - ell_corrected = (3*v4/10,0,-3*v6/10).
```

所以只修远端 b 不会自动修正 ell；反过来只换 H 或改一个 rho 也不会改变这些 source 身份。
旧 controller 可能是有意的名义 reference，本 review 不要求改源；要求的是明确登记其差项。
若选择其他参考、FD 而非 analytic Fref，必须重新写出完整差式，不能只保留上述 controller 部分。

## 5. actual y 的 missing witness 仍在这些代数之前

dhport_lib 的实际路径为 regularized Float64 mass、central-difference C/G、
tau−C−G，然后 Mq\\RHS 返回 ahat。没有实际 capture tuple 或全域 refinement 交付时，
不能令 z_A=0，也不能将“analytic equality row=0”当作运行方程。

正确拆分（所有量须嵌入相同实数语义）：

```text
e_solve = M_R*ahat - F_R
z_A = e_solve + (M_A-M_R)*ahat + (F_R-F_A)
y = X*z_A.
```

缺的是同配置 M_R/F_R/ahat、实际加载 X、mu/FD-step bits、model-vs-FD/roundoff/solve
refinement，以及相同 Omega 上的 signed y enclosure。只有 y_solve=X*e_solve 仍不够。

有界文件检索未找到该 runtime capture 或 actual signed packet；已读 preconditioned
identity 的 scope 只含 analytic rows 4/5，formal=false。combined remainder 的比较算子、
forcing/acceleration radius 不能填充本任务 y/u/s/D。

## 6. H 和 signed Schur 输出：哪些字段已有，哪些没有

H 的准确**source 定义**已存在：
descriptor 先从 Mdirect 的 origin substitution 取 M0CC，再在三条对角各加一次
MU456=1/1000000；Schur source 取 H=inv(Matrix{Q}(M0CC456))。
C 顺序固定 (4,5,6)，不是点态 M_CC(q)^-1，也不是 X 或 physical.S_metric。
此定义不含 controller，但把 H 与实际 force packet 同源连接仍需指定质量与 regularizer
语义；binary64 常数 rationalization 不能无声明与设计有理数混用。

physical.S_metric 的三维空间来自旧 D=(1,2,3,6) complement lift，且作用于 acceleration
energy；仅形状 3x3/SPD 不使它等于 block456 force 的 M0_CC^-1。
现有 source formula 和历史 exact factor 说明 dense metric 可表达；
本轮不重新求逆，也不把未提供的实例说成只是“缺一个平方根”。

目标 signed 输出必须为同一个 d、ell、r0、H：

```text
u = ell^T H d
s = (ell+r0)^T H d
Dquad = d^T H d
L = ell^T H ell, c0 = ell^T H r0
Qactual = (r0+d)^T H (r0+d)
P0 = beta-(ell+r0)^T H (ell+r0)
Pactual = P0-2*s-Dquad
        = beta-L-2*(c0+u)-Qactual.
```

NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.joint_of_signed_defect_caps 接收的实际义务：

| Gate 字段 | 当前 obstruction |
|---|---|
| hActual、hChange | 缺 physical total/reference split 与同一 H 的 source 身份；generic 展开不代替 |
| u≤U、s≤S | 没有实际 y/chart/reference 的 signed output witness |
| Dquad≤Dcap | 没有该 d 在相同 H 下的独立二次型 witness；两条 dual 不决定 Dquad |
| 2U≤beta−L−2c0−E_A | 没有相同 actual configuration 的 binding allocation |
| 2S+Dcap≤P0−t | 没有相同 actual configuration 的 target allocation |

旧 CSV 实际输出 status=BLOCK456_RESIDUAL_SCHUR_INTERFACE_AUDIT，
formal_certificate_allowed=false，包含 lambda、rho2_m0、BUP、target degree/support 和
effective beta diagnostics；没有本次 actual u/s/D 字段。
其 rho 对应旧 homogeneous r0 类 operator，不是上面新 d 的 squared cap。
不能将旧 absolute port bound 改名 Dcap；也不能把合成 helper 的 negative signed upper
或先前单点 source-graph 运算搬来填满全域 runtime packet。本轮没有这样做。

## 7. 最短重开条件与停止位置

已完成的是 source-text 对照、参数差式和条件式 port-map 推导；没有发现可消费的完整 packet。
第一批必须交付：

1. 固定 configuration/Omega/coordinate order，actual ahat/refinement 与 signed y；
2. 按第 3 节或另一条明确源推导绑定 r_actual/r0/d/eta/Fref，以及同域 N、X 可逆；
3. 明确旧/改正 controller、ell 和 offset，固定 H 的 mass/regularizer reference；
4. 同域可变 chart 的有效 bounds，分别交 U/S/Dcap 与两个 allocation。

未给这些字段前，不运行 synthetic helper、不重算旧 absolute remainder、不改源配置，
也不扩大 claim 为 trajectory/coverage/Lean/source admission。状态保持 pending；
missing witness 不是所有参数选择的数学不可能性。

## 8. 字节快照

以下是恢复后重新计算的 SHA-256；11 项均与暂停前读值相同，写入后复核。
它们不构成 runtime provenance、kernel receipt 或 source verification。

```text
E/routeB_dense_Mq/dhport_lib.jl
aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
E/routeB_dense_Mq/routeB_factorized_descriptor_model.jl
c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427
E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl
9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79
E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl
3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98
E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.csv
393d33c621be7927e2ff0e79e75f6059c2d0c5bf35af41be3e3f5789792861c3
E/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json
28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e
E/robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json
3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107
E/robot_formal_v1/interval_bounds/physical_acceleration_bridge_v1.json
01022d32673ad10e9b1b1da398da15ce624c3f077734c2343e1ec9813fc6bede
E/robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json
e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48
E/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json
68596f1557aa709d86bc8711ed7985552684dffe7fde290abf03b511f6bd9805
workspace/examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean
91a3a598ba6c6fb0278a127c8b94a34839f74eb3cd88d46b6d2ca4d4169c5ba7
```

