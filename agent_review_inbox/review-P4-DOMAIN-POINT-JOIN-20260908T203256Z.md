---
kind: review_result
task_id: P4-DOMAIN-POINT-JOIN-20260908
review_id: review-P4-DOMAIN-POINT-JOIN-20260908T203256Z
source_agent: Codex-domain-audit
created_at: 2026-09-08T20:32:56Z
inspected_commit: 8a8a61e2deecb667f253b71c31ed2dfb41947b2e
status: PENDING
new_admission_evidence_search: NEGATIVE_NO_ACTUAL_FLOW_OR_REFERENCE_RECEIPT
integration_status: pending
admission_label: pending
candidate_geometric_inclusion: true
initial_ramp_point_included: false
actual_ramp_flow_membership_verified: false
actual_source_binding_verified: false
lean_run: false
producer_run: false
sampling_run: false
state_registry_mutated: false
P5_closed: false
---

# P4 domain-point join：静态包含成立；intended ramp flow 归属仍 PENDING

## 落盘状态与本轮结论

P5-098 已有独立 immutable review：
`W/agent_review_inbox/review-P5-098-ANCHOR-BUDGET-INSTANTIATION-20260908T202703Z.md`，
SHA-256 `81e50fc3a40332450029bc6c336b0d58b0420f88231a7bd1bd0f3800c34c9637`。
其结论仍是 Mref 已定位、actual nominal reference/context 缺失；本轮没有修改该 review，
也没有取得足以把它升级为 actual anchor budget 的新证据。

本文件补齐此前 P4 反例点 `q=0,v=0,w=1` 的 domain join。
**NEGATIVE** 仅表示没有检索到新的 actual-flow/reference admission receipt；
不是系统不稳定或 intended trajectory 存在反例的判定。最终 intended-flow 归属
**PENDING**，但下列较窄几何包含/排除可以明确判断。

本轮只新增本 review；未改 state/registry/shared scripts、旧 review 或 source。
未跑 Lean/Lake、Julia、producer、sampling、ODE、Q/K 搜索或旧 Fraction solve。

路径根：

- E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`
- W = `C:/Users/z5242/Desktop/重构版/工作流`

## 1. 一个点，五个不同的 domain 问题

| 所核对的集合/语义 | q=v=0,w=1 的判定 | 实际 source 依据 |
|---|---|---|
| 12D mechanical initial ball，半径3/20 | 包含 mechanical projection，因为 norm²=0 | E/robot_formal_v1/interval_bounds/active_angle_domain_v1.json:4,10 |
| imported analytic slab 的显式 q/v box 与 measurable |w|<=2 范围 | 包含静态点；所有 q/v 为0，且1<=2 | 同 JSON:3–21：formal=false，角半径均正、速度半径2、step1/256 |
| intended ramp 的扩展初始状态 t=0,w=c*t | 排除该扩展点：w(0)=0≠1 | E/routeB_dense_Mq/routeB_export_traj.jl:99–100,149,165–166 |
| intended ramp，0<=t<=1/256、c²<=3 | 排除：w²=c²t²<=3/65536<1 | 同 ramp source，加上述 slab 的 step；只用平方不等式 |
| intended ramp 全 horizon 的静态 time/input 图 | (t,c)=(1,1) 使w=1合法；但不证明q=v=0是此时的机械状态 | exporter:41,135–149,165–166；W/examples/routeb_p8_ramp_tube_transport_lean/P8RampTubeTransport.lean:46–57 |

因此 active_angle_domain_v1.json 的显式 domain scope **足以证明候选几何/输入范围包含**，
不必把这个包含问题一概写成“无法判断”。但它的 formal=false、imported analytic
语义以及外包形式，都不足以证明 intended full true-DH/P8 flowpipe 包含。
该 JSON 的三个 source_hashes 已重新核对对应 analytic CSV 字节一致；哈希一致不是
analytic-vs-FD source equality 的证明，也不是重新运行并认证该 slab checker。

q=v=0 还满足全12D proof-facing `p=(3/2)sum(q²)+(4/5)sum(v²)=0<=rho`
及 joint limits；依据 E/routeB_dense_Mq/routeB_interval_branch_bound.jl:37–43,
57–67,187–198。这个集合比某个特定证书的完整 semialgebraic/trajectory domain
可能更大；未逐一绑定的额外谓词不能被省略。runtime eta 默认2.7，可由环境覆盖，
也不能把所有 branch-bound runs 自动标为rho=5.6。

## 2. P8 现有 carrier 的额外陷阱：constant-w 初始盒不是 ramp 初始集

重新读取了 E/robot_final/cross_validation/routeB_reachability_full_dh_probe.jl。
其与 routeB_dense_Mq/cross_validation 的同名文件本轮哈希相同。

- :20–22,31–37：默认 horizon1、R_INIT0.15、WMAX=sqrt(3)，默认 center=zeros(13)，
  均有环境覆盖入口；本轮只判断这些明确的默认参数，不认证某次 runtime 配置。
- :162–165：机械12个导数后，尾坐标为 `du[13]=0`。
- :171–175：初始集为13维 `Hyperrectangle(center,[R_INIT×12,WMAX])`。

所以默认 probe 的初始矩形确实包含 q=v=0,w=1，但这对应 constant-w 参数族，
不是 w=c*t、w(0)=0 的 intended ramp 初始集。机械部分也是盒外包，不是完整初始球
的精确集合相等。不能拿这个默认 probe 的 X0 membership 为 ramp initial membership 背书。

W/examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json:157–190 的
局部候选盒反而只有 q/v/w∈[-1/100,1/100]，故排除 w=1；但它明确仅是一盒，
不是 intended full-horizon domain。:210–230 明示 `ramp_binding=OPEN`、w_rhs=0、
c 未由13-state source消耗。:248–258 所钉 source hash 与本轮读取一致。

W/examples/routeb_p8_ramp_tube_transport_lean/P8RampTubeTransport.lean:46–57,
79–87 的 `RampTube`/`PullbackDomain` 清楚保留机械 tube predicate B。
这是本轮读到的条件式源码接口，未运行 Lean，不采用旧编译状态为本轮证据。
即使 (t,c)=(1,1) 满足 ramp graph，仍需 `B 1 1 mechanical_zero`；当前没有该证据。

## 3. First-exit/slab 能说明什么，不能说明什么

读取 E/robot_formal_v1/exact_checks/check_initial_analytic_slab.py，未执行。
其检查包括 source hashes、全6D matrix/RHS enclosure、正收缩数据，以及每个坐标
的 `initial+h*acceleration_radius<velocity_radius` 和
`initial+h*velocity_radius<angle_radius_i`。
RHS 以 `2*gw[i]` 控制输入，没有额外 ramp-time relation。

这是“若相应模型、初值、微分方程及已验证 enclosure 前提成立，则解在首段不越出
外包箱”的 first-exit 方向。它并不说外包箱的每一点都由某条 intended ramp trajectory
达到。尤其不能倒用 `Reach(t)⊆Box` 得到 `Box⊆Reach(t)`。

本轮能够在 t=0 和 0<=t<=1/256 排除 w=1 的 ramp 点；更晚时刻的 input graph
允许该值并不排除它，也不保证 mechanical_zero。要决定后者，最小新增证据是：

1. 固定 intended 初始集、c、t 和同 source/semantics 的 ramp-lift 身份；不能用 w'=0
   probe 代替 w'=c。
2. 同模型 full mechanical trajectory/tube 的对应 membership 或 exclusion 证明，
   例如证明某个坐标在该时刻离开0，或提供满足初始条件和ODE的实际 witness。
3. 将此前 exact analytic graph 与当前 FD/Float64 source、regularizer、solve semantics
   接线；mere shared DH 常量或哈希不构造该等价/误差桥。

没有这些新证据，不能判断指定晚时刻点是否在 intended actual flowpipe；“未找到
membership receipt”也不是 exclusion theorem。

## 4. 不改 source target 的 domain restriction 必要条件

此前 W/agent_review_inbox/review-P4-ACTUAL-BLOCK456-AFFINE-METRIC-DELTA-james-20260908T135717.md
:175–209 已给特定 ideal analytic target 在 q=v=0,w=1 的负值 `<-11/100`，并指出
该零机械状态 slice 上按 w² 缩放。本轮只重新核对 review 哈希和阅读结果，没有重做
其矩阵/解/target 算术，不升级为 FD runtime 或 intended trajectory 反例。

对固定函数 F，若改用更窄 D' 而不改 target，则恢复统一 F>=0 至少需要

```text
intended Reach ⊆ D' ⊆ D,
D' ∩ {X | F(X)<0} = ∅.
```

单独“删掉w=1”不能宣称这两条已满足。根据前述已报告的 w² slice identity，
若静态域允许 q=v=0、t=w=1/256、c=1，则该点满足首段 ramp 与初始机械盒几何，
而继承的同一 ideal target 仍 `<-11/6553600`。这是继承旧 exact target 结论后的
代数推论，不是新算出的 actual-flow 反例；若有额外域约束，必须另外检查这些约束。

因此缩短正 horizon 或缩小为任意非零 input 幅度，并不自动修复该 unrestricted
algebraic zero-state slice 的 target。真正的 domain-only 修复需证明 intended Reach
被保留，同时所有负 target 点均被排除；不能靠删除未证明不可能的 actual 状态过关。

## 5. 本轮实际读取/核对的路径与 SHA-256

| 路径 | SHA-256 |
|---|---|
| E/robot_formal_v1/interval_bounds/active_angle_domain_v1.json | c1637ae0160c0535b6be1dc147602266b43564f76806aa9df3178c6aec0c6cba |
| E/robot_formal_v1/exact_checks/check_initial_analytic_slab.py | efa9f57d42e6cd70bd0cc5afdeef68a35673a880f5c53e992a2a182c4ca36340 |
| E/robot_final/cross_validation/routeB_reachability_full_dh_probe.jl | 12292f8841ef79cfa58d07facbec4ca739e27346b11b6ec57e290638b7d8b93a |
| E/routeB_dense_Mq/cross_validation/routeB_reachability_full_dh_probe.jl | 12292f8841ef79cfa58d07facbec4ca739e27346b11b6ec57e290638b7d8b93a |
| E/routeB_dense_Mq/routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| E/routeB_dense_Mq/routeB_interval_branch_bound.jl | a2bd89c923ab646bcb138372e4c74a5980afe5d5906f21080b6781e03051869c |
| E/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| E/routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv | 2760489cba6dc2f2d25ac8f33fa5a25e430bb92040c022004d1ef949d3e09c5d |
| E/routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv | cdc587afd26b2ab5498c5917e8c620e7c9aada8b2f5b4128c88df14e78b4e4bb |
| W/examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json | c8045946c2e087ff8b31010a823f7ead6a1af56d2d84d68dd39d62c70a6eed34 |
| W/examples/routeb_p8_ramp_tube_transport_lean/P8RampTubeTransport.lean | 297776f2d95e511ae4dab4b0891f3f20ec7d425085a5b45637a389cbabe62224 |
| W/agent_review_inbox/review-P4-ACTUAL-BLOCK456-AFFINE-METRIC-DELTA-james-20260908T135717.md | 8c881691cce558c0796eb821d4e411838ec232b6f80cf8e7aa818b30f20dd874 |
| W/agent_review_inbox/review-P5-098-ANCHOR-BUDGET-INSTANTIATION-20260908T202703Z.md | 81e50fc3a40332450029bc6c336b0d58b0420f88231a7bd1bd0f3800c34c9637 |

三份 analytic CSV 本轮仅核对哈希与 domain artifact 所引哈希一致，没有重新评估其
多项式或声明其与 full true-DH/FD source 相等。所有实际归属/准入结果继续 PENDING。
