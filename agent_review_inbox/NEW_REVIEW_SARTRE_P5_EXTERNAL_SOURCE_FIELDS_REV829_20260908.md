---
kind: review_result
review_id: NEW_REVIEW_SARTRE_P5_EXTERNAL_SOURCE_FIELDS_REV829_20260908
task_id: SARTRE-P5-EXTERNAL-SOURCE-FIELDS-REV829
agent: Sartre
state_revision_observed: 829
status: SAME_TUBE_SOURCE_JET_PACKET_NOT_FOUND
integration_status: pending
admission_label: pending
source_binding_proven: false
commands: read_only_source_export_inspection_and_hashing
---

# Revision 829：外部真实 source/export 字段检查

本轮直接读取外部项目，未复用前轮 ledger 结论作为发现依据。结论仍是：
找到了可生成部分数学字段的真实代码和部分 exact 导出，但没有找到能共同提供
F、DF、W、Wt、DW、b、Db、e 与同 tube coverage 的 source packet。
不存在“完全没有导数/metric 文件”的断言；下表说明已有字段为何不能直接拼接。
不重复 rational/Neumann 审计，不优化常数，不构造 synthetic 实例。

## 读取范围

外部根 E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`。
D = E/routeB_dense_Mq；I = E/robot_formal_v1/interval_bounds。
读取 state 时 revision=829；仅作工作入口，不写 state。

I 下枚举到147个 JSON，定向搜索 variational、Lie/base-flow、same-tube、metric/
material derivative、Jacobian 与 F/DF/W/Wt/DW/Db/b/e 键；命中中的 w 是输入或
monomial 标签，不是变分 metric。这个搜索只是定位，结论还基于下面的真实代码/
CSV header/JSON 字段读取。没有遍历整个外部机器或声称全局不存在。

## 逐字段 source/export 对照

| P5字段 | 真实文件/代码或导出 | 精确缺口 |
|---|---|---|
| F | D/dhport_lib.jl:102–110 的 exact_ddq：M\(tau-Cdq-Gq)，tau 含现有 Kp/Kd/b_fr/G0/input | 是6维 acceleration 的执行函数，不是 xdot=-F+b 的完整12/14维 exact-real source binding；函数名 exact 不改变 Float64/FD/solve 语义 |
| DF | D/routeB_analytic_fourier_dynamics_probe.py:26–31 的 derivative；36–39 c_entry；98–104 计算 dM/C/G | 确有 exact Fourier coefficient 求导器，但导出的是 mass/C/G；未找到 full closed-loop F 的 Jacobian CSV/typed equality。dM 或 Christoffel coefficients 不是 DF |
| W | D/routeB_physical_rational_energy_metric.csv，header row,col,num,den；producer routeB_physical_rational_descriptor_bridge.py:156–167 | 实际是4x4 remote/complement 能量 G_D=diag(S' M0_DD S,1/rho)，不是已经绑定到完整状态/variation 的 W(t,x)；缺 carrier/chart/source/tube 映射 |
| W备选 | D/routeB_compact_block_local_storage_metric_audit.py:34–77 及对应 CSV 的 M0_BB_44/55、K_B0_velocity_lower、composition_proved | 是 block-local storage 比较，composition_proved=False；不能把其2维速度系数填成全状态 variational metric |
| W备选 | D/routeB_compact_bi_m0_metric_ledger.py:58 及 CSV rho2_m0_upward/theta/lambda/schur_charge/margin | 测量 r_B' M0_BB^-1 r_B 的 port metric；另有 M_BB(q5)^-1 lane，不能与常量 M0 metric 静默混用。CSV admissible=True 不是 P5 moving-metric source closure |
| Wt,DW | 上述 metric/CSV 没有 time/derivative-coordinate/material-derivative 字段 | 不能因某张表是常量就替真实 W 宣称 Wt=DW=0；先要证明它就是目标空间中的实际 metric。点态 mass metric也未附对应 derivative packet |
| b | D/routeB_fourier_fd_error_bounds.csv：kind,row,col,coordinate,num,den；producer:48–61,154–168 | 是 mass/potential central-difference derivative 截断误差幅值；未定义 actual base-flow minus nominal base-flow 的同源函数 b，也没经过完整 acceleration/solve/state-map 接线 |
| Db | 同一 FD 导出只有 mass_derivative/gravity_derivative 类型与 num/den | coordinate 是原 mass/potential 求导索引，不能充作 Db；没有对已绑定 b 再求状态导数的表达式/误差证书 |
| e | D/routeB_descriptor_residual_interface.jl:43–63 的 evaluate 返回 a,l,descriptor_err,link_err；输出 header sample,q4,q5,dq4,dq5,w,a4,a5,l4,l5,... | l 是两维 block 辅助残差，descriptor_err 是状态方程残差范数，不是 actual variational equation 的 additional e；缺 xi、Db*xi 与 r+d 的语义拆分 |
| domain coverage | I/half_active_vanis2_domain_probe.json 的 scope/angle_radii/velocity_radius/step；dynamic_descriptor_l2_chain_v3.json 的 domain_bank/steps/stop | 有 analytic slab/chain 候选，但没有上述 jet 字段共用的 tube_id/函数域/derivative-validity/全程包含 witness；两者 formal=false |
| coverage备选 | D/routeB_partition_coverage.csv：geometry_coverage_complete,dynamics_coverage_complete,evidence | 已读取行明确 true,false,geometric_superset_only，不能作为 dynamics tube |
| coverage备选 | D/routeB_export_traj.jl:24–32,65–80，读取 certificate_V 并仿真 | 导出轨迹时序，不是 universal coverage；V系数经 Float64 解析，也不是 W/Wt/DW 的 exact packet |

`routeB_factorized_link_jacobians_body_rational.csv` header 为
link,kind,output,joint,nu1..nu6,real_num,real_den,imag_num,imag_den；kind=Jv/Jw。
这是真实 body kinematic Jacobian export，不是闭环 vector-field DF。不能仅因文件名
含 Jacobian 就用来填 DF。

## 已有 exact 部分可保留，但必须保留边界

analytic_fourier_dynamics_probe.py 明确说明它是 parallel mathematical interface，
不替换 dhport_lib.jl；其 derivative 通过 Fourier frequency 精确生成系数。
mass/coriolis/gravity CSV 与 routeB_analytic_*_cs_polynomial.csv 是可继续使用的真实
中间表达式。FD error 表的理想实数截断估计也可作为未来 b 的一个组成部分，
但不含 solve/source-state 变换及 Db，更不是 Float64/libm/refinement 证明。
本轮没有执行脚本中的随机/高精度检查，也没有使用这些检查值作证据。

descriptor interface 的 nominal_f 加了 KC*q5/KC*q4，而 actual tau 没有该项；
因此 nominal/actual 分拆必须显式绑定。不能把 l=0、b=0 或 e=0 当默认。
同样，输入 law、状态排序、质量 regularizer、analytic vs FD C/G 必须进入共同 key，
不能只匹配部分 M/C/G hash 就宣称所有字段同源。

## 最小下一 witness：实际闭环 descriptor jet，而非新常数

建议先由现有 analytic M/C/G 导出器派生一个明确同域的 closed-loop jet receipt，
而不是重跑当前 bound 表或把任意 metric 塞进去：

1. 固定真实 source/controller/input/state-map 与一个已存在 cell，交 exact RHS R、
   acceleration a 的同域 descriptor identity M*a=R 和可解性证据。
2. 沿每个真实状态方向交 exact derivative witness
   `M*Da = DR - DM*a`，再按实际状态排序拼出 DF；必须是对该 source 的证明，
   上式这里只列请求的 witness 类型，本轮未构造其 inhabitant。
3. 明确哪个已有 metric 要作用于哪个 carrier，并交该映射及 W/Wt/DW 的 derivative
   identity；remote G_D、block K_B0、port M0^-1 不得互相顶替。
4. 若要消费093/091，先绑定 actual/nominal base difference b，再交 Db；从真实
   variational equation 定义额外 e，明确 Db*xi 不重复计入 e。
5. 同一 receipt 绑定 source hashes、cell/time/input law、函数/导数有效域与轨迹覆盖。
   缺少 coverage 时只能保留点态条件接口，不能宣布 same-tube invariance。

这份最小 jet packet 可共同支撑090/091/093；当前文件只提供部分 M/C/G 与几何/能量
中间数据。没有被哈希/源码身份验证的 DF、W、Db 等字段之前，继续优化 rates 无济于接线。

## 本轮 live 文件 SHA-256

以下均在 D 中重新计算，未写入外部目录：

| 文件 | SHA-256 |
|---|---|
| dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |
| routeB_analytic_fourier_dynamics_probe.py | A340D353F326B12A43564E5F0D45723A433611914038219E9E92D57FE177A9CE |
| routeB_fourier_fd_error_bounds.csv | 58C706D5ABC8565F61CF50C1958317D04174A5DEF93CB15A23232D9D9B082F63 |
| routeB_physical_rational_descriptor_bridge.py | D50CC1880536A30A2E44F67A49B648E99E51F8DD17598A4E50F3E0EADC9EDFFF |
| routeB_physical_rational_energy_metric.csv | F51B6638AF78A830A5DB307B94A73CB555C13FF9817B8CD89B66A70DB30091B6 |
| routeB_descriptor_residual_interface.jl | D3D21705E5E904A080E4B86DC4C380788D2323C155570A8E7B40D62B11BB0A24 |
| routeB_export_traj.jl | 35EBE806A46273068AF1AF937C0C0152378D6889024EC5586BF3C7AABD30ECCF |
| routeB_partition_coverage.csv | 230AF31BAA11ADA8DB514489DC8EE3A0306AE9B45B251ED8D72B9C92399B9C9A |

哈希仅固定所读 live 字节，不是 kernel/source theorem。只新增本 NEW_REVIEW，
没有改外部项目、StateStore、registry、旧候选；未运行 Lean/Lake/全回归，未声称 VERIFIED。
