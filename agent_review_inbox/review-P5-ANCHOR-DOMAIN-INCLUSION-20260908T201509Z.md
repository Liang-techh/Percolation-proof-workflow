---
kind: review_result
review_id: review-P5-ANCHOR-DOMAIN-INCLUSION-20260908T201509Z
task_id: P5-ANCHOR-DOMAIN-INCLUSION-20260908
source_agent: Codex-anchor-domain
created_at: 2026-09-08T20:15:09Z
inspected_commit: ce7163d1f6ca10435136894d4484ac78de1fb68d
status: EXACT_HYBRID_BUDGET_CRITERION_DERIVED_ACTUAL_COVERAGE_PENDING
integration_status: pending
admission_label: pending
actual_anchor_domain_verified: false
actual_path_coverage_verified: false
source_binding_proven: false
lean_run: false
lake_run: false
producer_run: false
registry_promoted: false
formal_certificate_allowed: false
P5_closed: false
---

# 最小 anchor-domain inclusion：一个 hybrid budget + 路径域/FD域分离

## 结果

现有 caller 已给出可利用的具体 domain 结构：全六维机械状态的加权椭球与 joint limits。
保持 actual qD/dqD 后，anchor 是否仍在该椭球，精确压成一个 scalar obligation：

```text
pD(actual) + pB(nominal) <= rho.                       (A)
```

加上 nominal block 的 joint-limit membership，(A) 与 actual endpoint membership
可推出整个 local straight segment 的物理域包含性。这里 rho 是 domain threshold，
不是 context eta，也不是 absorption mu 或 mass regularizer。
但这还不是某个已验证 derivative-cell family 的覆盖，亦不证明 Float64 full solve。
本轮分别给出 physical-domain、evaluation-halo、graph-lift、actual-flow 四个窄接口。

只新增本 immutable review，不修改 shared/state/registry，不跑 Lean/Lake、Julia、
interval producer、轨迹或回归；没有搜索 K_path 数表。

## 1. 实际文件与 domain 来源

外部根 E = `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。

| 实际 source 位置 | 可用事实 | 不提供的结论 |
|---|---|---|
| routeB_interval_branch_bound.jl:37–43,57–67 | 声明 proof-facing p=(3/2)sum(q_i²)+(4/5)sum(dq_i²)，p_bounds 遍历全部6个q及6个dq | 不自动证明某条 actual flow 位于该域 |
| 同文件:187–198 | global_root 取 joint limits 与坐标半径交集，含6维速度盒与w盒 | root矩形并非整个椭球；也不是所有盒都已通过 |
| routeB_export_traj.jl:41–46,81–87 | T=1；joint limits为1/2/4/5关节±pi、3关节±5pi/6、6关节±2pi；只检查q | 没有返回全时刻速度或hybrid-anchor inclusion proof |
| 同文件:89–109,131–161 | 同一ramp w=cw*t；数值步进；失败/越界sample跳过 | 不能把筛选后的sample表提升为actual flowpipe coverage |
| routeB_interval_bounds.jl:35–38,1207–1289 | 读取同一M0 CSV；对q/dq/w盒构造完整6D RHS/solve及block residual | 函数调用或inverse flag不是已认证的source/domain witness |
| 同文件:613–635；dhport_lib.jl:73–99 | 对6个坐标分别调用q±h e_k上的mass/potential | FD评估点未必属于physical joint-limit域 |

所选椭球是 **branch-and-bound 的全12维 proof-facing domain**，不是 exporter 中
block-only pv，也不是初始半径0.15的球。复用时要明确选择这个 domain；
不能用 block norm 控制 remote 八坐标。
代码中的 BigFloat/Float64 endpoint与权重实现仍需 outward/constant桥；
下文针对源码声明的 exact-real/rational domain 推导，不把这些数值计算当已认证证明。

## 2. 具体 physical predicate 与必要充分的 anchor 条件

B=(4,5)、D=(1,2,3,6)，均 human/Julia 1-based。
定义

```text
pB(q,v) = (3/2)*(q4²+q5²) + (4/5)*(v4²+v5²)
pD(q,v) = (3/2)*sum_{i in D} q_i² + (4/5)*sum_{i in D} v_i²
p = pD+pB

Physical(rho,q,v,t,w,c) :=
  JointLimits(q) and p(q,v)<=rho and
  0<=t<=1 and w=c*t and c²<=3.
```

这是为实际 source 标量/域接线选定的 predicate，并非 descriptor evaluator 内已有的
runtime guard。JointLimits 的 exact endpoints或其认证外包端点必须固定，不能混淆
实数pi、Float64 pi与BigFloat(pi)的不同解释。

从上一轮 error convention，z=(qB-qbarB,vB-vbarB)。保持 actual qD/vD、t/w/c 和
同一 nominal reference。anchor 用(qhatB,vhatB)=(qbarB,vbarB)。因此

```text
p(qhat,vhat) = pD(q,v)+pB(qbarB,vbarB).
```

若 actual 已在 Physical 中，则 hybrid anchor 的 time/ramp/context 与 remote limits
全部继承。新增且充分的物理条件只有：

1. qbar4、qbar5 在对应 joint limits 内；
2. (A)：pD(actual)+pB(nominal)<=rho。

第二项既是必要也是充分的**椭球分量**条件，没有再丢失相关性。
用 margin 形式可直接交checker：
`hybridSlack = rho-pD(actual)-pB(nominal) >= 0`。
对同一actual/context族，可给精确区间证明
`upper(pD(actual)+pB(nominal))<=rho`；拆成两个独立upper是更保守的充分条件。
不得因 margin 未能证明就把对应actual state从原覆盖目标静默删除。

### 为什么“actual与nominal都在同一椭球”仍不足

精确集合反例，非trajectory反例：取rho=28/5、t=1/2、c=w=0。
actual仅v6=5/2，故p(actual)=5；nominal仅qbar4=1，故p(nominal)=3/2。
两点均满足上述椭球与joint limits，但hybrid保留actual v6并加入nominal q4：

```text
p(hybrid)=5+3/2=13/2 > 28/5,
hybridSlack=-9/10.
```

不能从两个不同remote context的endpoint membership推出(A)。
这只否定一个错误的domain推理，不说明实际nominal/actual轨迹会取这些点。

## 3. 整条 local path 的 exact inclusion，无需声称它是轨迹

定义0<=s<=1：

```text
q_s[D]=q[D],                  v_s[D]=v[D]
q_s[B]=(1-s)*qbarB+s*qB,       v_s[B]=(1-s)*vbarB+s*vB
t_s=t, w_s=w, c_s=c.
```

s=0是hybrid anchor，s=1是actual base state；nominal reference参数固定。
由于只在B插值，有确切恒等式

```text
p(q_s,v_s)
 = (1-s)*p(qhat,vhat)+s*p(q,v)
   -s*(1-s)*[(3/2)||qB-qbarB||²+(4/5)||vB-vbarB||²].    (B)
```

最后一项非负，故actual membership与(A)给p(q_s,v_s)<=rho。
joint intervals凸；actual和nominal B端点membership给所有q_s满足limits。
ramp关系因t/w/c不变精确保持。因此(A)加nominal B limits已经闭合**理想physical
predicate**的整段包含性，既不需要角度逐点采样，也不要求远端状态随nominal改变。

如果local stateMap不是上述误差/仿射坐标，须先给出source→z identity；
本(B)式不能无条件迁移到任意非线性chart。

## 4. physical、derivative cover、FD evaluation halo 不是同一个域

physical inclusion只说明路径未离开所选数学域。为了使用某个已有局部Jacobian界，
还需：整条(q_s,v_s,w)落在该bound的已认证cover内。
最小单盒检查可以使用包含两端点local坐标的区间 hull，remote坐标保持actual/context盒：

```text
Qpath[D]=Qactual[D]; Vpath[D]=Vactual[D]
Qpath[B]=hull(Qactual[B],Qnominal[B])
Vpath[B]=hull(Vactual[B],Vnominal[B]).
```

证明该盒或该盒与Physical的交集包含路径，再使用在相同集合上成立的界。
若采用多个盒，须给有限分段0=s0<...<sR=1及每段归属；仅两端点各在某个pass盒不够。
interval branch的root box/名为RESOLVED的旧cell不能代替这个新hybrid-path cover。
矩形hull角点可能在椭球外，不可因路径在椭球内就声称整个hull也在椭球内。

FD调用需要更小而准确的额外接口：

```text
forall s in [0,1], k in {1..6}, sign in {-1,+1},
  q_s + sign*h*e_k belongs to OmegaEval.
```

不要求这些扰动点是物理轨迹，通常也不应要求其仍在原physical joint limits内。
可选OmegaEval为Qpath逐坐标扩张|h|的评估盒；只需证明mass/potential与所用
FD/导数证据在这个外扩盒有效。库的q±h计算有舍入时，外扩半径必须覆盖实际
Float64加减偏差；不能只给理想|h|而不处理source输入lift。

G0是固定global-origin调用，还需静态覆盖0与0±h e_k。它们未必在此次Qpath halo内，
可用单独的reference-evaluation域/receipt，且必须同一h与regularizer。
**不需要在每个FD扰动点重新求解acceleration**：当前source仅在中心q_s求解M a=R，
FD扰动点只是mass/potential评估。将两种义务分开能避免不必要的全halo solve要求。

实际精度接缝：interval_bounds.jl:32采用BF("1e-5")，dhport_lib.jl:28与:76采用
Float64 step。二者须由精确h身份或覆盖区间连起来，不能因字符串同写1e-5直接相等。
本轮不运行其interval实现，也不认证其bounds。

## 5. 完整graph lift与冻结Mref/context

对每个中心路径点需要一个同语义的完整6D解：

```text
a_s := unique a satisfying M(q_s)*a=R(q_s,v_s,w)
Gamma(s) := (q_s,v_s,t,w,c,a_s, fixed-reference/context).
```

不能令a_s=(1-s)*ahat+s*a_actual；M/R随q/v变化，这种线性插值通常不满足graph。
保持qD/vD不意味着保持aD。选定exact-real Gram source并证明正regularizer下界时，
上一轮mass结构给中心路径全部点的唯一解。操作性Float64 map则须返回值/solve defect
与其域有效性证明，不能把\符号当作精确等式。

Mref始终来自同一routeB_Mq_M0.csv读取/对角选择（S:22–23；interval:35–38），
G0、controller、nominal reference、h、regularizer也固定。每个s只重新计算依赖
q_s/v_s的frames、lifts、M/C/G、R与a_s，不把Mref替换成MBB(q_s)。
anchor是Gamma(0)，actual graph point是Gamma(1)；需要graph uniqueness/source identity
把后者与已有actual acceleration witness识别，而不只比较q/v坐标。

## 6. 可验证的窄typed/domain contract

下面是review里的设计记法，不是新增或已编译Lean代码。将前述代数构造作为定义，
不额外要求producer提供一条任意黑箱路径：

```text
AnchorDomainData:
  sourceKey, semanticsKey, MrefKey, referenceKey
  rho, jointIntervals, Qpath, Vpath, OmegaEval, derivativeCover
  qbarB, vbarB, lbar, t, w, c

AnchorDomainProof (actual):
  actualPhysical : Physical(rho,q,v,t,w,c)
  referenceSameContext : selected nominal values at THIS t/input/context
  nominalLocalLimits : qbarB in limits_B
  hybridBudget : pD(q,v)+pB(qbarB,vbarB)<=rho
  pathCover : forall s in [0,1], (q_s,v_s,w) in derivativeCover
  fdHalo : every source FD perturbed q_s lies in OmegaEval
  referenceHalo : fixed G0 evaluation points covered
  graphLift : forall s in [0,1], exists unique full a_s with same-source graph
  sourceIdentity : full residual at Gamma(s) is the selected evaluator/interpretation
```

`pathPhysical`与anchorPhysical可由actualPhysical、nominalLocalLimits、hybridBudget
和(B)推导，不必重复作为独立待填字段。
`pathCover`可以通过单盒hull inclusion或实际分段证据实现；不能用代数physical证明
绕过某个局部bound只覆盖子域的限制。字段中的keys/hashes定位数据，不构造证明。

实际flowpipe只需在最终调用侧证明

```text
forall t in I, sourceActual(t) has AnchorDomainProof with selected reference(t).
```

这并不要求Gamma_t(0)或Gamma_t(s)属于actual flowpipe。
需要的是它们在derivative/graph评估域，而非同一initial-value solution上。
因此“hybrid anchor不在actual flowpipe”本身不是失败；真正缺口是(A)、local limits、
path cover/halo与同source graph lift尚未对该actual/reference族证明。

如果(A)不成立，可另行认证更大domain上的derivative/graph界，但不能沿用旧rho域
的证书并只改域标签。也不能通过删去不满足(A)的actual点冒称原flowpipe全覆盖。

## 7. 精确剩余工作与证据等级

已完成的是：从实际domain source提取了可用结构，给出(A)/(B)及针对hybrid graph的
具体predicate接线。没有交付任何actual nominal表或uniform hybridBudget证据。
最小上游补交为同时间reference B盒/值与actual remote预算的关联界；
随后补已认证cell/path cover、FD外扩与完整solve source bridge。
不需要先搜gain表、重做toy SPN或把anchor当轨迹传播。

既有artifacts/task_GBB_fullstate_descriptor_gate_20260907/contract.json的
minimum_domain_premises及N1/N6仍是fail-closed接口：其中full-state盒、FD与continuation
要求可作字段参考，但没有本轮hybrid budget witness。所读GY/GAV报告的历史开放状态
也不被本轮源码阅读刷新为已验证。

## 8. 本轮源码行与SHA-256绑定

W=`C:/Users/z5242/Desktop/重构版/工作流`。E前缀见第1节。hash均本轮读取。

| 文件 | SHA-256 |
|---|---|
| E/routeB_interval_branch_bound.jl | a2bd89c923ab646bcb138372e4c74a5980afe5d5906f21080b6781e03051869c |
| E/routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| E/routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| E/routeB_descriptor_residual_interface.jl | d3d21705e5e904a080e4b86dc4c380788d2323c155570a8e7b40d62b11bb0a24 |
| E/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| E/routeB_Mq_M0.csv | 28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40 |
| W/artifacts/task_GBB_fullstate_descriptor_gate_20260907/contract.json | 2660a5ea347e1c7df317f6226c429f30412c52c960e3bcd002e1ad795bacf4f1 |
| W/agent_review_inbox/review-P5-CENTERED-ANCHOR-INSTANTIATION-20260908T200937Z.md | ad847dc2b2ac822a4bce1c2388ee32e211a22a665e7ed456966fed58b365c2eb |

只读命令用于取文本/行号/hash/Git/时间；数学恒等式与集合反例为本轮推导，未作
Lean/kernel或source arithmetic运行。没有认证interval package、global coverage、
source equivalence、P5 closure或registry promotion。保持pending。
