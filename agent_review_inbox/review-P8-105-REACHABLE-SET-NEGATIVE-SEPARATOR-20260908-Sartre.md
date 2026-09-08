---
kind: review_result
task_id: P8-105-REACHABLE-SET-NEGATIVE-SEPARATOR
status: pending
existing_reachable_separator: not_established
local_analytic_inclusion_design: candidate
all_negative_prefix_exclusion_under_local_contract: rejected
original_w1_patch_reachability: pending
source_binding_proven: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# P8-105: reachable-set separator 与反向局部 inclusion 障碍

## 1. 结论先分两种负值集合

本轮没有找到或构造出已认证的 reachable-set separator。现有 full-X0/ramp flowpipe 合同仍为空 receipts，不能据此排除负值区域。

但不能只把问题留在“缺 flowpipe”。对于同源 exact-real analytic ODE，full-X0 是包含原点邻域的完整初始球。下文给出一个反向 Picard 构造：若交付局部 continuity/Lipschitz/source-axis 合同，则允许初值中存在一点，在小时间 tau 到达 q=v=0,w=tau,c=1，此时 frozen auxiliary target=-G*tau^2<0。因此在这些明确前提下，不存在将**所有负值点**与 full-X0 允许 solution prefixes 分开的 separator。

必须区分：

- N1：原 q=v=0,w=1 附近的一块负值邻域。它是否与原 full-horizon ramp reachability 相交，仍未决定。小时间构造不证明 w=1 可达，也不证明任意预先指定的 N1 都可达。
- Nall：选定同源 frozen target 的全部负值集合。小时间构造命中其中另一块 N_tau。仅排除 N1 不足以证明 frozen target 在所有允许轨迹前缀非负。

这里提供的是 source-indexed 条件性数学推导与 typed contract 设计，不是已实例化的 ODE/Lean/runtime receipt。没有宣告原 block45 domain、saved-V 或 terminal trajectory theorem 为假。

只新增本 immutable review；不改 state/registry/shared scripts/旧 agent 文件；不运行 Lean、采样、回归、Julia/interval producer、轨迹或 Q 展开。

## 2. 实际 source 与现有缺口

E=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`，W=`C:/Users/z5242/Desktop/重构版/工作流`。

重新读取的 full-X0 合同：

```
state14=(q,v,w,c),
X0: |(q,v)|_2^2<=9/400, w=0, c^2<=3,
F14(q,v,w,c)=(v,a(q,v,w),c,0),
0<=t<=1, w(t)=c*t.
```

当前合同 verified=false、OPEN_NEEDS_ODE_RECEIPTS，RHS-Lipschitz receipts=0、cell receipts=0、initial boxes=0、existence witnesses=0、cell witnesses=0、initial_cover=false、same_semantics=false。空列表不是空可达集证明。P5-099 已指出的旧 interval-source hash 漂移、partial chain 和 empirical export 边界不被本轮刷新为证明。

实际 analytic 定义来自所列 rational M/C/G CSV 和 `routeB_compact_dh_gain_descriptor_regeneration_audit.jl`：

```
M(q)=M_csv(lift(q))+(1/1000000)I,
R(q,v,w)=-Kp*q-d_DH*v+G(0)+GwI*w-C(q)[v,v]-G(q),
a(q,v,w)=M(q)^-1 R(q,v,w)                 在 M 可逆处。
```

这里 inverse 是 exact-real 数学定义，不是 Julia backslash 被自动赋予精确语义。source 的 c/s 多项式作物理 sin/cos pullback 后是光滑函数；局部 M 非奇异才允许推出 a 的局部光滑/Lipschitz。若 frozen residual 的 nominal remote elimination 使用 A=M_DD，还须其局部非奇异。相应 source/units/regularizer/metric 同一性仍要有 typed 证明，不能用文件名、旧 olean 或一次线性方程残差替代整个合同。

固定真实 C=(4,5,6) metric H=M_CC(0)^-1 与原 descriptor residual。既有 exact source-axis 计算给出

```
a(0,0,w)=a_* w,       a_*=M(0)^-1 GwI,
r(0,0,w)=0,
ell(0,0,w)=k w,
P(0,0,w)=beta-qH(ell+r)=-G w^2,
G=h-b>11/100>0.
```

G 的完整 Fraction 值及 a_* 的六维有理向量保存在 hash 锁定的 actual-Q-Delta review。此处沿用同一份 exact-axis 身份，不把任意 acceleration、toy 或 numerical interpolation 放入 graph。

## 3. 反向 Picard inclusion：最短局部数学构造

令 x=(q,v) 属于 R12，固定允许的 ramp slope c=1，定义

```
f(s,x)=(v,a(q,v,s)).
```

只需以下局部合同，不需要全局 flow inverse、全时域 flowpipe 或稳定性：

1. 某 r>0、Tloc>0，0<r<=3/20、0<Tloc<=1。
2. f 在 [0,Tloc]×closedBall(0,r) 上连续，并对 x 有统一 Lipschitz 常数 L>=0。
3. 同源零轴界 |f(s,0)|_2<=K*s，K>0；可取有理 K>=sum_i |a_*,i|，不需要有理平方根。
4. 所选小 cylinder 属于实际 evaluator/target 的有效域；若调用者还有 joint/tube 限制，另证 cylinder 在这些限制内，不能令该域预先假定 P>=0。

选择任意 0<tau<=Tloc，满足

```
L*tau<=1/2,
K*tau^2<r.
```

这些条件可以用有理 r,Tloc,L,K 和足够小的正 dyadic tau 认证。本轮没有填入新的数值 L/r/tau，也没有把此前举例 tau=1/1024 自动认定为满足它们。

在连续曲线空间的闭球 |x|_sup<=r 上定义 terminal-value Picard operator

```
(Phi x)(s) = - integral_s^tau f(u,x(u)) du.
```

两个精确估计为

```
|Phi x|_sup <= L*r*tau+K*tau^2/2 < r,
|Phi x-Phi y|_sup <= L*tau*|x-y|_sup <= (1/2)|x-y|_sup.
```

因此闭球上的 contraction 给固定曲线 x_tau。由积分方程：

```
x_tau(tau)=0,
x_tau'(s)=f(s,x_tau(s)),
|x_tau|_sup <= K*tau^2 / (2*(1-L*tau)) <= K*tau^2 < r.
```

取真实初值 x0=x_tau(0)，就有 |x0|_2<r<=3/20。再令 w(s)=s,c(s)=1，则 w(0)=0、c^2=1<=3，整个曲线是同源允许 ramp 的局部 solution。反向积分只是构造初值，所得曲线仍在正时间 s∈[0,tau] 满足正向 ODE，不是改变输入方向或物理时间。

终点因此满足

```
z_tau(tau)=(q=0,v=0,w=tau,c=1),
P(z_tau(tau))=-G*tau^2<0.
```

这给出**条件性的 reachable-prefix inclusion**，而不只是另一个静态点。初值依赖 tau，且一般不等于0；原 full-X0 允许整个初始球，这一自由度正是构造的关键。它不推出从固定初值 x0=0 的同一条轨迹在不同 tau 都返回原点。固定初值或离散浮点初值族会是不同合同。

因为 tau 可取任意充分小的正值，对每个这样选定的 tau，命中的严格负值点都有一个相对 source 域的负值邻域 N_tau（另由 P 连续性）。不能从这个结论跳到原 N1 或 w=1 可达。

## 4. 这些前提为何是 source 可定位的，而不是已经闭合

实际 M/R 是有限 rational-coefficient trig/polynomial 表达式；若交付 M(0) 非奇异与 source pullback equality，连续性给小邻域的非奇异，逆矩阵由 adj/det 表示，因而 f 在该邻域 C1。进一步在小 compact cylinder 上取 derivative bound 可给统一 L；有理上界可通过严格余量选择。A=M_DD 的局部单位证明同理处理 nominal port evaluator。

这解释了为什么上述 regularity 合同符合 source 结构，并不声称已经有可消费的定量 L、r、Tloc 和相应 source-bound receipt。已有 analytic slab 的 acceleration envelope / inverse guard 不等于自动提供了 state-Lipschitz bound；本轮没有重跑其 checker 或实现导数上界。

当这些局部前提被认证后，试图为 Nall 构造 universal full-X0 **prefix** exclusion 会与上面的 inclusion 冲突；不应继续寻找一个与同源局部可逆性矛盾的 separator。如果前提尚未认证，正确状态是 conditional obstruction candidate / source integration pending，不是已验证物理轨迹反例。

## 5. 最小 typed source / inclusion / exclusion 合同

以下为 review 中的类型设计记法，不是 Lean 文件或已编译声明。keys 固定身份，proof 字段必须实际证明其命题，不能用字符串或布尔 status 代替。

### 共用 source 层

```
SourceSemantics:
  mode = exact_analytic_real | ideal_fixed_FD_real | deployed_runtime_relation
  X = R12; Z = X x R_w x R_c
  rhs : Z -> Z
  target : Z -> R
  evaluatorDomain : Set Z
  sourceKey, massKey, gainKey, metricKey, residualKey, normalizationKey
  rhs_identity : rhs=(v,a,c,0) under the selected mode
  target_identity : target is the selected frozen block456 P
  initial : |x|_2^2<=9/400 and w=0 and c^2<=3

PrefixTrace(T,z0,z):
  0<T<=1; initial(z0); z(0)=z0
  z continuous/absolutely continuous on [0,T]
  z(t)=z0+integral_0^t rhs(z(s)) ds
  evaluatorDomain(z(t)) for every t in [0,T]
```

integral/source mode 对 deployed runtime relation 不能原封不动套用：若 source 是带舍入的离散程序，需相应 execution/transition relation 或经证明的 differential inclusion，不能擅自断言其为 C1 ODE。

### inclusion 合同与具体本轮出口

```
NegativePrefixInclusion:
  T,z0,z : actual objects
  trace : PrefixTrace(T,z0,z)
  endpoint_negative : target(z(T))<0

LocalBackwardInclusionInputs:
  r,Tloc,L,K with positivity/radius constraints
  continuous_rhs, uniform_state_Lipschitz
  same_source_axis_rhs_bound
  local_cylinder_evaluator_inclusion
  exact_axis_target : target(0,w,1)=-G*w^2, G>0
  source identities and local inverse witnesses

LocalBackwardInclusionInputs
  -> exists tau,z0,z, NegativePrefixInclusion(tau,z0,z)
```

若要求 inclusion 于仅包含完整 [0,1] 曲线的 ReachFull 集合，还必须附

```
extend_to_one : exists zFull, FullTrace(1,z0,zFull)
                and zFull restricted to [0,tau] equals z.
```

不能从局部存在擅自推出全时域 continuation。若一个拟议 full-X0 theorem 已承诺所有初值存在至1，那么由同源 uniqueness，它的完整解必须包含上述局部前缀；该 theorem 若还额外承诺 frozen P 全程非负，就会与本条件构造冲突。原 block45 theorem 并不等于这个额外承诺。

### exclusion 合同

```
ReachExclusion(Bad):
  sameSource and same initial/input/time semantics
  totality/nonvacuity appropriate to PrefixTrace or FullTrace
  Omega : certified outer cover of ALL specified traces and all relevant times
  disjoint : every point of Omega is outside Bad
```

可以使用 separator B(t,z) 代替直接 disjointness，最小逻辑接口是

```
barrier_initial : B(0,z0)>=0 for every permitted z0
barrier_transport : B(t,z(t))>=B(0,z0) on every covered trace
barrier_separation : Bad(t,z) -> B(t,z)<0
```

一份充分的可检查 transport payload 是：B 为 C1、Omega cover/continuation 不循环依赖 P>=0，且在同一 cover 上有 ∂t B+D_z B[rhs]>=0；沿 trace 积分得到 transport。只验证某处 B 的数值符号、只给边界方向口号或未覆盖的局部 derivative bound 都不满足它。

如果 Bad 只是 N1，而目标是证明 P>=0，还需独立的

```
negative_coverage : relevantDomain intersect {P<0} subset Bad.
```

“Bad 中所有点均负”是相反方向，不能代替 negative_coverage。排除一块已知负值 patch 不等于排除全部失败点。若直接定义 Bad={P<0}，则这个覆盖字段是定义性的，但第3节的条件 inclusion 正好阻止 universal prefix exclusion。

## 6. 明确的 negative results 与非结论

已确定不能作为 separator 的材料：空 flowpipe cells、缺失后缀、采样中没出现原点、t=0 时 w=0、q=v=0 不是平衡点、或只证明 N1 与某个未覆盖全初值的 hull 分离。非零加速度不禁止机械状态瞬时经过零点；本轮反向构造正是针对完整初始球。

在 LocalBackwardInclusionInputs 成立后，`ReachPrefix ∩ {P<0}=empty` 是 rejected；存在足够小的 tau 使相交。没有给出任何新的 source-bound 数值 tau、初值表、全时域 extension、N1 reachability 或 deployed runtime counterexample。N1 的单独 exclusion 仍 pending，即便日后成功，也不能绕过 N_tau 的另外障碍。

对于 ideal fixed-FD real model，如果另证同样的局部 C1/source-axis identity，可以复用该构造；不能仅凭 FD step 固定就把 Float64 程序当成光滑实数映射。特别是负余量 G*tau^2 随 tau->0 消失，固定绝对 rounding/solve error bound 可能压过它。runtime 转移需要在具体 tau 上证明误差小于相应负余量，或另给尺度兼容误差关系；本轮两者都没有提供。

原 block45 性质是 p45<=28/5、saved-V tube 与 t=1 的 qpoly45<=12。构造的局部终点 q=v=0 本身满足 p45=qpoly45=0，不能将 frozen block456 辅助 residual 为负偷换成上述性质为假。若要坚持原物理 theorem，应重审辅助 target/budget，而不是给不可能的辅助非负性赋予原 theorem 的地位。

## 7. 下一跳与状态

优先核验小的 `LocalBackwardInclusionInputs`，尤其 source 模式、局部 M/A 可逆、state-Lipschitz 与 axis target identity；它比全时域 separator 更能区分路线是否可能。若这些字段闭合，停止尝试将全部 frozen-target 负值区域与允许前缀分离，转向已授权的 beta/target/总预算修正。

若真正任务仅为排除 N1，则保留精确 N1 predicate、time/c fiber、source/initial coverage 和 separator transport，且明确它不完成 P5。完整原 ramp trajectory theorem、runtime bridge 与 continuation 均保持 pending。本轮未选择新 theorem statement，也未更改任何 gate。

## 8. 本轮实测 hashes

| 路径 | SHA-256 |
|---|---|
| E/routeB_dense_Mq/dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |
| E/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| E/routeB_dense_Mq/routeB_analytic_gravity_cs_polynomial.csv | 2760489CBA6DC2F2D25AC8F33FA5A25E430BB92040C022004D1EF949D3E09C5D |
| E/routeB_dense_Mq/routeB_analytic_coriolis_cs_polynomial.csv | CDC587AFD26B2AB5498C5917E8C620E7C9AADA8B2F5B4128C88DF14E78B4E4BB |
| E/routeB_dense_Mq/routeB_fourier_lifted_descriptor_model.jl | 0FCF733144B3D7B1B08F328FE4AD24477057C56976F0EF53633C450D8FC4729D |
| E/routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| W/artifacts/routeb_agent_full_x0_flowpipe_contract_20260906/full_x0_flowpipe_contract.json | D1D5006E264A99FB17CE4FD43F81DEC359391C2A9E2D2E67CECDA44E0775AC02 |
| W/agent_review_inbox/review-P5-099-TARGET-DOMAIN-DECISION-20260908-Sartre.md | D868D10670AFC6B935532A96F13B35B2BDA82A3CDA88926221DC84690D542E10 |
| W/agent_review_inbox/review-P5-K7-ACTUAL-Q-DELTA-PACKET-20260908-Sartre.md | 95F4913696A909364F907664CD22D28024568A3E28B9382917C9438600420E05 |
| W/docs/routeb-block-targets-v2.md | 489DAC0AE88F4E15988C2E87E9D390E349E5C7562DA80D52F33872E7CE5D38C1 |

hash 是字节身份，不是 Picard、source 或 kernel 证明。所有新合同/估计为本轮数学设计，未运行 Lean/采样/回归。仅新增本 review；没有共享状态或登记更新，也没有原 block45 trajectory theorem 的否定声明。
