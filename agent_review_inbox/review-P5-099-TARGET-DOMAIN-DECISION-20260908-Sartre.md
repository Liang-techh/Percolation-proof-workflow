---
kind: review_result
task_id: P5-099-TARGET-DOMAIN-DECISION
reference_revision: 864
status: pending
analytic_measurable_input_domain_excludes_witness: false
full_horizon_static_ramp_domain_excludes_witness: false
certified_reachable_set_exclusion: pending
frozen_target_on_witness_containing_domain: rejected
source_binding_proven: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# P5-099: intended domain / flowpipe 能否排除 exact witness？

## 1. 决定与边界

不能依据本轮检查到的实际 domain/flowpipe 材料，合法排除 revision 864 的 q=v=0,w=1 反例。需要区分三个结论：

1. **analytic 首段的 measurable |w|<=2 域不排除它。** 零机械状态属于完整初始球；w=1 是允许的输入，源码并未要求 w(0)=0。
2. **原始 ramp 家族排除它作为 t=0 初始点，但不排除全时域的静态 graph 点。** 例如 t=3/4,c=4/3 时 w=ct=1、c^2=16/9<3，q=v=0 满足所读 joint/椭球限制，saved-V tube 的代数条件也不排除它。
3. **这个点是否真正被原始 ramp 的某条 full-X0 solution 到达，仍未确定。** 未找到可用于该判定的全时域、同源、完整覆盖 flowpipe exclusion receipt。静态 membership 不是 reachability；缺少 reachability 证明也不是 exclusion。

所以：若当前 P5 辅助 target 要求在所读静态域/analytic 域上逐点非负，它已经 rejected；若只要求在尚未精确给出的可达域上成立，则 domain/source join 仍 pending，不能据此恢复 frozen target 的可行标签。这不是对原始 block45 domain/terminal theorem 的轨迹反例。

本轮仅新增此 immutable review。没有改 state/registry/shared scripts、旧 review 或任何 source，没有运行 Lean/Lake、producer、数值回归、轨迹或新的 mass solve。只读检查原始源码、JSON 的必要字段、现有 review 和 SHA-256；数学条件由精确输入关系与已有 source witness 推导。

## 2. 真实输入域不是同一个对象

根 E=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`；W=`C:/Users/z5242/Desktop/重构版/工作流`。外部相对路径均以 E 为根。

### A. analytic vanis2 首段

`robot_formal_v1/exact_checks/initial_analytic_slab.py` 与独立 checker 实际使用：

```
X0: sum(q_i^2+v_i^2)<=9/400,
input: measurable |w|<=2,
RHS force interval includes +/-2*GwI_i,
M = rational mass CSV + (1/1000000)I6,
damping = (13/10,11/10,19/20,4/5,13/20,1/2).
```

它不带 c 状态，也未强制 w=ct。实际 `half_active_vanis2_domain_probe.json` 记录：
initial_radius=3/20、velocity_radius=3、angle_radii=(9/20,19/50,37/100,19/50,37/100,9/20)、step=1/512、formal=false。

因此 x0=(q,v)=0 和常值输入 w=1 满足声明的初值/input 条件，所有显示的空间盒也包含该点。这里不需要以“没有模拟到该点”为理由保留排除的可能。它的 analytic pointwise target 若声称在该整个域非负，就直接遇到既有 exact graph obstruction。checker 源码支持这些域语义；本轮未重跑 checker 或将该 JSON 认证为连续系统 theorem。

### B. full-X0 ramp 合同

`artifacts/routeb_agent_full_x0_flowpipe_contract_20260906/full_x0_flowpipe_contract.json` 声明

```
state=(q1..q6,v1..v6,w,c), dimension 14,
initial: sum(q_i^2+v_i^2)<=9/400; w=0; c^2<=3,
w'=c, c'=0, w(t)=c*t,
0<=t<=1.
```

`routeB_dense_Mq/routeB_export_traj.jl:89–109` 的实际模拟也用每条轨迹固定 cw，wv=cw*tk。`gen_trajectories` 使用半径3/20的12维球内随机初值和全组 |cw|<=sqrt(3)，不是任意 measurable input。故不能拿 A 的“允许 w(0)=1”直接当作 B 的初始条件。

对 w=1 的 ramp 输入 membership，有精确条件

```
1=w^2=c^2*t^2<=3*t^2.
```

因此 t=0 或 0<=t<1/sqrt(3) 真正排除了 **这个 w=1 值**。特别是 t<=1/512 时 3t^2<=3/262144<1。但全时域 [0,1] 并未排除；取有理 t=3/4,c=4/3 即满足全部 input/time 等式，而且不依赖末端 t=1 的边界解释。

这只是 input-coordinate 结论。把 q=v=0 与 (t,c) 拼成一个静态 admissible graph 点，不等于从 X0 构造了相应机械 solution。

## 3. 空间 domain 与 saved-V tube 不能提供排除

`routeB_interval_branch_bound.jl:37–43,57–67,187–198` 的全状态 proof-facing 域是

```
p_full=(3/2)sum_i q_i^2+(4/5)sum_i v_i^2<=eta,
joint limits, independent w box approximately [-sqrt(3),sqrt(3)].
```

对任意正 eta，q=v=0 满足 p_full=0，所有 joint limits 含零，w=1 位于这个 w box 的内部。其 `local_root` 只是围绕另一个数值见证的局部盒；该局部盒不包含原点不等于 parent/full-domain 排除原点。收缩全域为一个局部 root 必须另证覆盖。

`docs/routeb-block-targets-v2.md` 与原 `routeB_pmi_certificate.jl` 则保留原 block45 目标：

```
p45=(3/2)(q4^2+q5^2)+(4/5)(v4^2+v5^2)<=28/5,
qpoly45=3(q4^2+q5^2)+2(v4^2+v5^2)<=12 at t=1,
saved V(q4,q5,v4,v5,t)<=t^2.
```

原点的 p45 与 qpoly45 都是0。它们不是 block456 residual target，也不是同一个12维椭球；但无论采用哪个所读空间域，都不能仅靠这些不等式排除原点。不能将 block456 辅助 target 失败说成原 block45 terminal property 已失败。

为避免漏掉 tube 的潜在排除，本轮还直接筛选了 `routeB_certificate_V.csv` 的零空间指数项，得到

```
V(0,t) = -0.11705920463516882
         -0.21295054667008032*t
         +0.2672395546940304*t^2
         -0.1568490889444761*t^3
         -0.024452143069624944*t^4.
```

将这些存储 decimal 视为其精确有理系数时，V(0,t)-t^2 的五个系数全部严格为负，因此对所有 t>=0 都有 V(0,t)<t^2。这里只用系数符号，不运行轨迹或采样。Julia 将这些数解析为 Float64 的系数解释仍有相同严格符号；这不代替原证书的 exact recovery、polynomial identity 或 Float64 运算误差证明。它说明所读 saved polynomial 的 tube 条件不是所需排除依据，不能凭一个未证明的 V-domain guard 删除该点。

## 4. 已读 flowpipe 材料没有完成排除

### full-X0 合同仍是空证据字段

上述14维合同当前文件中：verified=false、verdict=OPEN_NEEDS_ODE_RECEIPTS；RHS local-Lipschitz receipts、cell-wise RHS receipts、initial boxes、existence witnesses、cell witnesses 均为空。covers_exact_contract=false，initial/time/exit accounting 和 same_semantics 均为 false。

空的 box 列表不能解释为“可达集为空”或“不包含 witness”；它没有 cover 证明。文件名/数组形状也不提供 ODE existence、continuation 或 disjointness。

另有实测 provenance 问题：该旧合同列出的 `robot_final/routeB_interval_bounds.jl` hash 为
`d51f7c43a1389edb4c4d5e1d6c492a864bcb55229f99e7032a1ec9c9239f99f1`，
当前同路径文件 hash 为 `03679C7B686842EF9504886614E3498FB9FBF4A6C1466F8E44DCC505D21E3609`。
不能把旧 BOUND_SOURCE_FIELDS_ONLY 字段认定为 live source binding，更不能把 `robot_final` 与 `routeB_dense_Mq` 两个路径的 interval source 不经核对地互换。

### partial analytic chain 不是完整 ramp exclusion

`dynamic_descriptor_l2_chain_v3.json` 当前字段为：

```
status=PARTIAL_DYNAMIC_DESCRIPTOR_SINGLETON_CHAIN,
formal=false,
step_count=183,
verified_end_time=183/512,
stop.reason=guard_or_endpoint_domain_exit.
```

producer `dynamic_descriptor_l2_chain.py` 的 descriptor cap 使用输入界 Q(2)，输入 generators 同样按幅值2生成；它不是携带 w,c 的14维 ramp fiber exclusion 证书。名称 SINGLETON 不能被解释为只包含一条已验证机械轨迹。该输出亦没有覆盖 [0,1]，本轮没有运行 checker 或确认其名称中的 verified 字段具有 theorem 地位。

即使另行加上 ramp 输入关系，183/512<1/sqrt(3) 只说明这个较短时间段不可能取 w=1；后续允许 w=1 的时间尚未被该链覆盖，不能把缺失后缀当作排除。

### 数值导出/历史 current audit 不是 exclusion receipt

`routeB_export_manifest.toml` 明确 evidence_level=empirical、coverage_kind=trajectory_monte_carlo_only、global_box_coverage=false。exporter 会跳过求解失败或越 joint limit 的 samples；只观察留存样本不覆盖全部 X0/ramp。没有 sample 精确落在 q=v=0 也不是集合排除。

`task_routeb_flowpipe_frontier_current` 和 `task_routeb_flowpipe_terminal_current` 的报告基于历史 DAG v268/v262，自己保留 flowpipe/first-exit open。这里将它们作为历史边界说明，不用目录名 current 推断其已刷新到 revision 864 或本轮最新 state。

## 5. 排除 w=1 的早时段也不能挽救静态域 target

真实 analytic RHS 在 q=v=0 有 R=GwI*w，所以沿这条 source graph 轴

```
alpha(w)=alpha(1)*w,
r(w)=0,
ell(w)=k*w,
P(w)=(b-h)*w^2=-G*w^2,  G=h-b>0.
```

对任意非零 w 都为负。取 t=1/1024、c=1、w=1/1024，便在 ramp 首段 t<=1/512 内得到另一个同源静态点；q=v=0、input relation、空间域和上面的 saved-V tube 全部满足。其 target 为 -G/1048576<0。这是已知 exact source 轴的代数缩放，不是新 toy、数值采样或已证明可达轨迹。

因此，仅排除早时段的特定 w=1，或者把 input 幅值改小但仍允许该静态原点轴上的非零输入，并不能修复 frozen static-domain target。若要依靠真实 flowpipe 获救，必须证明它避开相关负值区域，而不仅证明一个孤立点没有出现。严格负值及源函数的连续性还意味着局部负值邻域；其与可达集的分离需要实际证据。

## 6. 无合法域排除时的必要 beta/target 阈值

以下仅针对包含原 exact witness 的域，或含其非零缩放轴的同类齐次域，不升级为全域充分条件。保持同一 source、H、units。令

```
S=|aC_*|^2,
b=S/100+1/20,
h=k'Hk,
d=(589578/1000000)*sum_i ((133374,50185,33335)_i/1000000)*aC_*,i^2.
```

这些数的完整 Fraction 值在已锁定的 parameter-envelope review 第2节。定义

```
G=h-b,
Gamma=2h-b,
Gamma_old=2h-b+2d.
```

其中 G>11/100、Gamma>31/100、1/2<Gamma_old<3/5。确切值不是这些下界；其精确表达式才用于设计。

若 beta 增加 scalar g、目标从0改为 t=-tau，则在 witness：

| 保留的证明配置 | 必要净修正 g_*+tau_* |
|---|---|
| exact target；或最优补偿 split 与 sharp cap | >=G |
| 原 split、lambda=2、sharp point cap=0 | >=Gamma |
| 原 split、lambda=2、旧 global-cap 点值 d | >=Gamma_old |

原 split、sharp cap=0 若只调有限 lambda，需要 g_*+tau_*>G，等号仅是 lambda->infinity 的极限，不是该 split 的有效 consumer witness。最优补偿 split 可在有限 lambda 下达到 G，但仍需要 beta/floor 的真实修正，不能靠 split 单独越过 G。

只改共同 acceleration 权重 beta_a、保留 beta_w=1/20 时，新系数分别需要

```
beta_a >= (h-1/20)/S,
beta_a >= (2h-1/20)/S,
beta_a >= (2h+2d-1/20)/S.
```

只改 input 权重 beta_w、保留 beta_a=1/100 时，分别需要

```
beta_w >= h-S/100,
beta_w >= 2h-S/100,
beta_w >= 2h+2d-S/100.
```

第1行是 exact/最优分配条件；后两行对应表中固定配置。所有公式为 Fraction 级阈值；若 required target>0，还须增加相应目标值。q/v 权重在 witness 为零，单改它们无效。

beta 增大或目标下界降低会改变显示的局部 theorem/预算。若要保持原 P>=0，不可把 beta 增量当作免费钱；同额加回 target 会抵消修复。来自更大 theorem 的预算搬移必须有 donor 并扣账。改变输入律/域同样改变量词，除非明确证明该子域覆盖原允许轨迹。均不在本轮实施。

## 7. 真正的下一跳：最小 exclusion 或 inclusion 接缝

调用侧须明确选择 analytic measurable-input static domain、ramp static/tube domain，还是原 full-X0 reachable domain，并绑定原 block45 目标与拟用 block456 residual lemma 的关系。

若选择 reachable-only 路线，最低交付为：

1. 完整12维 X0、固定 ramp 参数 c、时间窗、实际 DH/analytic/FD/Float64 语义 key；
2. 全部初值/输入覆盖、同源 ODE existence 与连续传播/first-exit 证据，不能只给 samples；
3. 对所有允许 t,c 和所有覆盖分支的 disjointness / separator 证明，至少排除所用负值区域；
4. 用该已证域重新检查 residual/cap/allocation，而非只修改 domain 标签。

q=v=0 处加速度非零并不禁止轨迹瞬时经过该点，不能用“不是平衡点”作为 exclusion。相反，静态 domain membership 也不证明从允许初值可达。只针对单一数值轨迹、单个初值或 partial horizon 的结果都不能决定 full-X0 问题。

在这些材料缺失时，decision 是 **没有已建立的合法 domain/flowpipe 排除**。包含反例的 static-domain frozen target 保持 rejected；原 ramp trajectory theorem 保持未决，而不是被本 review 宣告为假或真。

## 8. 本轮锁定 source / artifact hashes

| 路径 | SHA-256 |
|---|---|
| E/routeB_dense_Mq/routeB_interval_branch_bound.jl | A2BD89C923AB646BCB138372E4C74A5980AFE5D5906F21080B6781E03051869C |
| E/routeB_dense_Mq/routeB_pmi_certificate.jl | 235F4876ED1A3343F6D84F83C0079B4D279886585DC36AEB55B9FC0289177A77 |
| E/routeB_dense_Mq/routeB_export_traj.jl | 35EBE806A46273068AF1AF937C0C0152378D6889024EC5586BF3C7AABD30ECCF |
| E/routeB_dense_Mq/routeB_export_manifest.toml | 5B61D624F4F6060DA8C33A51FA7982BEF8206D2C3924BABB512440DEFAD89187 |
| E/routeB_dense_Mq/routeB_certificate_V.csv | CAB4A5182981BCCBDE18ACE2D26ECE5C0D7B7D3C3CF4A5A7E02E7FCDA9B80601 |
| E/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| E/routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| E/robot_formal_v1/exact_checks/initial_analytic_slab.py | 97C96FB01BC9318AF258A75D6B1371E3EEF665FA760F401CE9F5A422CA164998 |
| E/robot_formal_v1/exact_checks/check_initial_analytic_slab.py | EFA9F57D42E6CD70BD0CC5AFDEEF68A35673A880F5C53E992A2A182C4CA36340 |
| E/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| E/robot_formal_v1/exact_checks/dynamic_descriptor_l2_chain.py | E50074944C1689043A12E4D1A6C825FB6B5CF0534B491AECA229C1A2C5F505AF |
| E/robot_formal_v1/interval_bounds/dynamic_descriptor_l2_chain_v3.json | 1E1301289F1398D3D0762F64607987A0BB27CD670C924F315DC7557CC96CCF7F |
| E/robot_final/routeB_interval_bounds.jl | 03679C7B686842EF9504886614E3498FB9FBF4A6C1466F8E44DCC505D21E3609 |
| W/docs/routeb-block-targets-v2.md | 489DAC0AE88F4E15988C2E87E9D390E349E5C7562DA80D52F33872E7CE5D38C1 |
| W/artifacts/routeb_agent_full_x0_flowpipe_contract_20260906/full_x0_flowpipe_contract.json | D1D5006E264A99FB17CE4FD43F81DEC359391C2A9E2D2E67CECDA44E0775AC02 |
| W/artifacts/task_GBB_fullstate_descriptor_gate_20260907/contract.json | 2660A5EA347E1C7DF317F6226C429F30412C52C960E3BCD002E1AD795BACF4F1 |
| W/agent_review_inbox/review-P5-K7-ACTUAL-Q-DELTA-PACKET-20260908-Sartre.md | 95F4913696A909364F907664CD22D28024568A3E28B9382917C9438600420E05 |
| W/agent_review_inbox/review-P5-PARAMETER-FEASIBILITY-ENVELOPE-20260908-Sartre.md | 62839A3212DD9BDF16A3C4684071C084B4DA86B380822C3D4F7CEC9E868FEC22 |

以上 hash 本轮重新计算，只固定读取身份。范围是列出的源码与 receipts，不是对全机器“排除证明不存在”的穷尽断言。没有执行本机 Lean 或回归，没有改变任何 admission gate；源静态域结论、可达集未知和所需参数修正严格分开。
