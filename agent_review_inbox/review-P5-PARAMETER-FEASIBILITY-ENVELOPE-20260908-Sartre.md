---
kind: review_result
task_id: P5-PARAMETER-FEASIBILITY-ENVELOPE-20260908
reference_revision: 864
status: candidate
integration_status: pending
frozen_target_at_reference_point: rejected
source_binding_proven: false
formal_certificate_allowed: false
lean_compile_status: not_run
---

# P5 参数化可行域：精确单点筛选，不是假定 frozen target 可行

## 1. 本轮增量与 revision 指向

已核对 `agent_review_inbox/collaboration_board.md` 的 revision 864 段和 `task_queue.md` 对应 harvest：指向同一个实际 full analytic graph 点 q=v=0,w=1、r=0，但当前 beta/descriptor target 为负的 obstruction。这里核对的是协作记录的 revision 关联，不声称读取了 revision 864 的完整 state 快照，也不把协作记录当作证明。

本轮在前两份 review 基础上新增：

- beta / target / residual 分配的统一参数域；
- 消去 lambda 的纯有理判据、可行 lambda 区间和一个显式有理 lambda witness；
- 六个 source-derived 系数阈值的 Fraction 表；
- 输入轴的端点条件、全域量词与单点可行域的严格区别。

仅新增本 review；不展开 Qs，不改 source、shared state/registry/scripts，不运行 Lean/Lake、求解器或轨迹/采样。运行的唯一数学计算是对既有精确 witness 做 Fraction 系数阈值运算，不重新求解 mass graph。所有“可行”默认只指所列单点代数条件。

## 2. 固定 source 与精确标量

外部根 E=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`；工作根 W=`C:/Users/z5242/Desktop/重构版/工作流`。

保持实际 mass CSV+(1/1000000)I、DH-gain analytic RHS、C=(4,5,6)、D=(1,2,3) 与 H=M_CC(0)^-1 不变。零位姿处实际 acceleration 的 C 分量是 a=nC/D0：

```
D0 = 55045306919641125471053338193373
nC = (15496010610460899685191174600000,
      57359628436617187133182572800000,
      82562335976049469352722168650000).

H = [[50003000000/5000400003,0,-50000000000/5000400003],
     [0,4000000/200739,0],
     [-50000000000/5000400003,0,350003000000/5000400003]].
```

令 N0=H^-1、k=GwI_C-N0*a。原 source 在该点满足 ell=k、r=0、lTotal=k。H 的正定性、inverse identity 和六行 M alpha=GwI 的精确检查保存在已锁定的 actual-Q-Delta review；本轮没有把自由 aC 当作实际 acceleration。

使用以下精确有理量：

```
S = a'a
  = 10346792641048372323505922719100268195440723404514027822500000000 /
    3029985813877491169216849944017076878485273952370238295541117129

h = k'Hk
  = 24620483671240352346790676593221927036621140442249040136757939902655625000000 /
    112645366956051638794181269352179574736504189937710462574954548286743824684259

b = S/100+1/20

d = (589578/1000000)*sum_i ((133374,50185,33335)_i/1000000)*a_i^2
  = 16679985913685612236554768565259685505490250470068766564369844793 /
    201999054258499411281123329601138458565684930158015886369407808600.
```

S>0、h>b、d>0。d 是原 global-cap 表达式在此点的值，实际 port 平方却为零。这里计算 d 不代表认可其全域 interval/source 证书。记 qH(x)=x'Hx，所有 scalar charge 都保留这个 metric；不允许改用默认 Pi/sup norm、无权欧氏平方或另一个 block 的 metric。

## 3. Beta / target 参数化：先写出真正可用的预算

采用与原 source 单位一致的设计族

```
beta_p(z) = sum_i p_i*aC_i(z)^2
            + beta_qv(z) + p_w*w^2 + g0,
target_p(z) = t0 + tau*w^2,
beta_qv(0,0)=0.
```

p_i 对应 joints 4,5,6 的 acceleration-squared 系数；beta_qv 使用原 q/v 类项。g0,t0 是 scalar charge，tau,p_w 是 charge/input-squared 系数。若设计另要求所有 beta 系数非负，应与下列可行域取交，不能从单点检查反推它们全域合法。

该点真正可用于 residual 的量为

```
Bavail = sum_i p_i*a_i^2 + p_w + g0-t0-tau.
```

共同 acceleration 系数 p_i=p_a 时，Bavail=p_a*S+p_w+g0-t0-tau。原 frozen 参数为 p_a=1/100,p_w=1/20,g0=t0=tau=0，故 Bavail=b<h。提高 q/v 系数在这个点不增加任何预算。单点参数只通过上述仿射组合进入；例如 beta 增量与 target 同额增量在 Bavail 中抵消，不产生修复。

## 4. 统一 residual-budget envelope

先保持原 total residual k 不变。把新的分配写成

```
u = theta*k + zperp,       <k,zperp>_H=0,
eta = qH(zperp) >= 0,
ell' = k-u,                r' = u,
Delta' = qH(u)+epsilon,    epsilon >= 0.
```

theta 是无量纲分配比例，可为实数；eta 和 epsilon 是 charge。epsilon 是新 cap 的多余量，不是可被忽略的真实 FD/force defect。因为 H 正定，任意 u 都可如此唯一分解；这里只是同源向量的点值参数化，不构造新的机器人模型。

固定 lambda>1，定义 Llambda=lambda^2/(lambda-1)。精确完成平方给出

```
lambda*Delta' + lambda/(lambda-1)*qH(ell')
= h + Llambda*(h*(theta-1/lambda)^2+eta) + lambda*epsilon.
```

因此该点 nonnegative allocation 的必要且充分条件是

```
Bavail >= h + Llambda*(h*(theta-1/lambda)^2+eta) + lambda*epsilon.   (F)
```

对于有理 lambda,theta,eta,epsilon,p_i,p_w,g0,t0,tau，(F) 仅需 Fraction 运算。它描述固定 lambda 下的凸二次可行域；在 theta/eta/epsilon 固定时，beta/target 参数域是闭半空间。不同 lambda 的并集不能未经证明仍称为凸集。

这个标量参数域不自动交付 source-defined u(z) 或其系数证书；指定一个有理 eta 也不等于已经构造出具有该 H-平方的有理向量 zperp。实际接合必须核对 u、正交性、eta 和 cap 的同源关系。

等价的可用 cap 松弛上限为

```
epsilon <= (Bavail-h-Llambda*(h*(theta-1/lambda)^2+eta))/lambda,
epsilon >= 0.
```

或写成分配偏差预算

```
h*(theta-1/lambda)^2+eta
  <= (lambda-1)/lambda^2 * (Bavail-h-lambda*epsilon).
```

右端为负即 rejected；不能将负预算截成零后宣称可行。自由优化 theta 且 eta=epsilon=0 时，theta=1/lambda 达到下界 h。因此自由补偿分配的投影可行域恰是 Bavail>=h，等号可由有限有理 lambda=2、u=k/2、Delta'=h/4 达到。这只消除证明松弛，不改变原 P。frozen Bavail=b<h，所以它不在这个最宽的补偿分配可行域内。

原 split 对应 theta=eta=0。此时 Delta'=epsilon；令 epsilon=0 得 sharp point cap，令 epsilon=d 则保留旧 global-cap 点值。不得把 d 当作真实 qH(r)，也不得把旧 cap 原封不动交给 r+u。

## 5. 消去 lambda：精确有理判据、区间与 witness

在某个已固定的 split/cap 下记 e=qH(ell')>=0、f=Delta'>=0、B=Bavail。要求

```
A(lambda)=(lambda-1)*(B-lambda*f)-lambda*e >= 0,
lambda>1.
```

等价二次式为 A=-f*lambda^2+(B+f-e)*lambda-B。

### e>0 且 f>0

存在有限实数 lambda>1 当且仅当

```
B-e-f >= 0,
(B-e-f)^2 >= 4*e*f.                                      (R)
```

这是 B>=(sqrt(e)+sqrt(f))^2 的无平方根形式；第一条符号条件不可删除，否则平方会引入伪解。令

```
Dlambda = (B+f-e)^2-4*f*B = (B-e-f)^2-4*e*f,
lambda_minus = (B+f-e-sqrt(Dlambda))/(2*f),
lambda_plus  = (B+f-e+sqrt(Dlambda))/(2*f).
```

满足 (R) 时可行 lambda 恰为 [lambda_minus,lambda_plus]，两个端点均大于 1。无需浮点近似根：若 B,e,f 全为有理数，直接选

```
lambda_cert = (B+f-e)/(2*f) > 1,
A(lambda_cert) = Dlambda/(4*f) >= 0.
```

这给出显式 Fraction 级可行参数，不需要最优 lambda=1+sqrt(e/f) 有理。lambda_cert 是 A 的顶点，不宣称它最小化归一化 Young charge。退化 Dlambda=0 时它就是唯一可行参数；仍不可把 lambda=1 当作合法端点。

### 零值边界必须单独处理

| e,f | 存在有限 lambda>1 的充要条件 | 可行 lambda |
|---|---|---|
| e>0,f=0 | B>e，严格不等式 | lambda>=B/(B-e) |
| e=0,f>0 | B>f，严格不等式 | 1<lambda<=B/f |
| e=f=0 | B>=0 | 任意 lambda>1 |

因此原 zero-port split 在 Bavail=h 时虽然 exact target 达到零，却没有有限 lambda allocation witness；Bavail>h 才可用此 split。通过补偿 split 达到同一 exact 边界，不与这里矛盾，因为 e,f 随 split 改变。不能用 lambda趋向无穷或趋向1的极限冒充现有 consumer 的参数。

## 6. Fraction 阈值表：不是 decimal 拟合

设 g0=t0=tau=0，保持原 residual 与 source。下表为新系数本身的最低值，不是相对原值的增量。每个 exact expression 使用第2节的精确分数；最后一列是本轮用整数/Fraction 运算验证的严格有理夹逼，统一分母10^6。

| 自由系数；另一系数固定 | 目标/证明配置 | 精确下阈值 | 严格位于 (L/10^6,U/10^6) |
|---|---|---|---|
| p_a；p_w=1/20 | exact target 或最优补偿 split | (h-1/20)/S | (49363,49364) |
| p_a；p_w=1/20 | 原 split,lambda=2,cap=0 | (2h-1/20)/S | (113369,113370) |
| p_a；p_w=1/20 | 原 split,lambda=2,cap=d | (2h+2d-1/20)/S | (161731,161732) |
| p_w；p_a=1/100 | exact target 或最优补偿 split | h-S/100 | (184418,184419) |
| p_w；p_a=1/100 | 原 split,lambda=2,cap=0 | 2h-S/100 | (402984,402985) |
| p_w；p_a=1/100 | 原 split,lambda=2,cap=d | 2h+2d-S/100 | (568133,568134) |

阈值本身由 exact expression 定义，不能用夹逼下端取代它。若需要有理可行点，上端仅能提供本点相应配置的严格余量，不是全域可行 witness。表中第1/4行等号由最优补偿 split 达到；若限制原 split 且只允许调有限 lambda，则必须严格超过这两行下阈值。

两参数/target 的边界不需要逐点枚举，例如原 split、lambda=2 时

```
p_w >= 2h+2Delta_* - p_a*S - g0+t0+tau,
Delta_* >= 0.
```

最优补偿 split 的对应边界为 p_w>=h-p_a*S-g0+t0+tau。对各向异性 acceleration 权重，用 sum_i p_i*a_i^2 替换 p_a*S 即得精确半空间；单点只能限制这个组合，无法确定各系数的全域作用。

## 7. 改 baseline 的参数不能伪装为预算重分配

若不补偿地移除 chi*k，则 total 变为 mu*k，mu=1-chi。这改变被认证的 residual。写 ell'=(mu-theta)k-zperp、r'=theta*k+zperp 后，(F) 一般化为

```
Bavail >= mu^2*h
          + Llambda*(h*(theta-mu/lambda)^2+eta)
          + lambda*epsilon.
```

自由 split 的最小 charge 从 h 变成 mu^2 h，原因是 target 变了，不是证明更强。原 scalar P 与新 P 的差为

```
P_new-P_old = (1-mu^2)*h = (2chi-chi^2)*h    在该点。
```

若原结论必须保持，就将新 target 增加相同 correction，或者从 beta 扣回它；预算增益随即消失。一般 source 点的 correction 必须用 2<lTotal,gvec>_H-qH(gvec)，不能把本点常量 h 当作全域 correction。

语义分类：

| 操作 | 是否保持原被认证结论 |
|---|---|
| 改 lambda、合法紧化同一 port cap、补偿 split、合法 graph-ideal multiplier | 保持；仅影响证明松弛，仍受 exact charge h 下界限制 |
| 增 beta 而保持 target | 改变局部 P；需单独证明上游预算可合法供给，才可能保持更大的最终 theorem |
| 同额增 beta 和 target | 保持，但 Bavail 不变，不能修复 |
| 降低 target，或加入负的 tau*w^2 floor | 弱化结论/改变 supply-rate；不能称为原非负 theorem |
| 未补偿的 nominal baseline 移动 | 改变 residual/target；实际 dynamics 可不变，但 source join 必须重做 |
| 从另一个已证非负项转移预算 g | 只可能保持其精确总和 theorem；必须 debit donor，不能重复记账 |
| 改 H、源参数、normalization、输入或域 | 改变语义/量词；不能作为同 theorem 的免费预算 |

尤其 P_local+P_donor 的已证总预算可按 +(g),-(g) 重分配，但不能因此宣称原 P_local>=0；这里原 P_local 在 witness 处确实为负。

## 8. 真实额外 residual 不等于 cap 松弛

若另有真实加性 force defect e_phys，其证据仅给 qH(e_phys)<=E，E>=0，且允许任意方向，则实际 total 从 k 变为 k+e_phys。点wise robust exact-target 的充要条件是

```
Bavail >= (sqrt(h)+sqrt(E))^2,
```

即 Bavail-h-E>=0 且 (Bavail-h-E)^2>=4hE。worst direction 是与 k 同向；这是整个 H-ball uncertainty family 的精确 envelope。如果 source 对 defect 方向有更强约束，该球条件仅为充分条件，不是实际 source 的必要障碍。本轮没有给 E 填数，也没有把 FD/runtime defect 当成零或当成 epsilon。要证明实际 runtime theorem，必须交付其同源误差合同，不能用 analytic 反例/可行参数替代。

## 9. 输入轴与全域 theorem 的量词

沿 q=v=0，actual alpha、ell 与 w 成正比，所有原二次 charge 与 w^2 成正比。假设所选 split、cap、baseline 参数也按此齐次方式定义，记其在 w=1 的 relaxed charge 为 Cpar。令

```
c0 = g0-t0,
c2 = sum_i p_i*a_i^2+p_w-tau-Cpar.
```

整条 |w|<=Wmax 轴上的 allocation 等价于 c0+c2*w^2>=0，因而精确充要条件是

```
c0>=0,
c0+c2*Wmax^2>=0.
```

vanis2 声明 Wmax=2 时，c0>=max(0,-4*c2)。没有常数修正时需 c2>=0；仅把允许幅值从2缩成任何正数，都不能修复负的齐次系数。若 g0=0 且 t0>0，则 w=0 已失败。以上条件只覆盖这条轴；只有 intended domain 包含相应点/轴段时，才能将失败用于排除全域参数。ramp-only/trajectory-restricted 域须独立证明包含或排除，不能由盒子元数据替代。

设实际域为 Omega、参数为 p。全域证书要求

```
for all z in Omega:
  actual source graph and metric identities,
  valid cap for the selected residual,
  allocation(z,p)>=0.
```

因此全域可行域包含于本 review 的 witness 参数域；本域只是必要的 outer screen，不是全域 inner certificate。固定 residual/cap/lambda 且只调 beta/target 的线性系数时，全域筛选是所有点半空间的交；若这些 source 对象也依赖参数，则必须保留其依赖，不能沿用线性结论。

特别是，逐点消去 lambda 得到 forall z exists lambda，并不自动给出 exists lambda forall z。若方案要求一个统一 lambda，须证明所有可行区间的交含某个有限数>1，并处理第5节的开边界。若采用 lambda(z)，必须明确它是允许的 pointwise proof 参数；若它进入 storage/其他可微对象，另需对应正则性与导数项，不能偷换量词。

## 10. Rejected 区域与下一跳

立即 rejected：保留原 total/metric 且 Bavail<h 的所有参数，不论如何选补偿 split、lambda 或更大 Q。原 frozen 参数属于这个区域。原 split 的 e>0,f=0,B=e 边界也不是 finite-lambda candidate。删除 (R) 的符号条件、沿用不匹配 port 的 cap、忽略真实 defect、拿点wise 参数当全域 theorem，均 rejected。

下一跳是先固定允许改变的 theorem 参数与预算来源，再用 (F)/(R) 和 Fraction 阈值筛掉单点已不可能的配置。通过筛选者只标 candidate；随后才值得做同 source 的全域 residual/cap、allocation、domain coverage 与最终目标接合。这里没有选择或实施新的 beta/theorem statement，更没有假设 frozen target 可行。

## 11. 本轮重算的身份与验证范围

| 路径 | SHA-256 |
|---|---|
| E/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |
| E/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| E/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| E/routeB_dense_Mq/routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04B764434601DD0C11B2A6554156FD4D948CF742DBF33472B960E0D54E8235C9 |
| E/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| W/agent_review_inbox/review-P5-K7-ACTUAL-Q-DELTA-PACKET-20260908-Sartre.md | 95F4913696A909364F907664CD22D28024568A3E28B9382917C9438600420E05 |
| W/agent_review_inbox/review-P5-TARGET-REPAIR-MINIMAL-20260908-Sartre.md | 6FB8F0F98883E762F99CFA70C047B6E42D407419EC3428A11C15423770BA580B |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | A76375770D563F86F7DE80FDEA970E8D0D0FADD1ED917C262B725C7A8BA47648 |

六个系数阈值及严格有理夹逼由 Fraction 运算检查，退出码0，输出 `FRACTION_PARAMETER_THRESHOLDS_PASS`。其余参数域公式是本轮代数推导，尚无 Lean/kernel receipt。哈希固定字节身份，不填补 source、domain、runtime 或全域 theorem 义务。只新增本 review，state/registry/shared scripts 均未改动。
