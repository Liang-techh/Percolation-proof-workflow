---
kind: review_result
review_id: review-P5-SOURCE-KPATH-REPAIR-BOUNDARY-20260908T200217Z
task_id: P5-SOURCE-KPATH-REPAIR-BOUNDARY-20260908
source_agent: Codex-source-kpath-contract
created_at: 2026-09-08T20:02:17Z
inspected_commit: b68cb241619b2fe1710b8500c8173fc98dd550c3
status: MINIMAL_TYPED_CONTRACT_DEFINED_ACTUAL_INSTANCE_PENDING
integration_status: pending
admission_label: pending
actual_arithmetic_inputs_ready: false
source_binding_proven: false
comparison_entries_checked: 0
lean_run: false
lake_run: false
producer_run: false
registry_promoted: false
formal_certificate_allowed: false
P5_closed: false
---

# 最小 source → K_path repair contract

不再搜索 K_path 数表。本轮仅回读已定位接口、source 定义与上一份 obstruction review，
复核指定文件 hash，新增本 immutable review。未修改 state/registry/shared scripts，
未运行 Lean/Lake、producer、checker 或回归。

## 结论：分开“可以算”与“绑定 actual source”

八项算术从 UNKNOWN 进入可计算，只需要已选定坐标下的有理 A/Hjac/Scoord 和 G。
K_path 可由三表重算，不需要另外猜八个数。
但其结果要成为 actual comparison，还必须给出 source/centering/normalization 的
typed identity、同域 PathBinding，以及 G 与实际选定 certificate family 的 identity。
这些 proof fields 不能由 hash、schema flag 或 arithmetic pass 构造。

最小推荐实例不是继续把 MBD 改名为 gain，而是直接对**已归一化、完整 residual 的
centered difference**建八项界。此时可采用一个逻辑段，A=I2、Scoord=I4，K_path=H。
两个 identity 矩阵是接口选择，不是 toy gain；实际 H/G 八项值仍未供给。

## 1. 最小 source 类型：full、centered、bias 是不同字段

以下为 typed contract 设计记法，不是本轮新 Lean 声明，也没有编译 claim。
令 Vec=Fin4→ℝ，Force=Fin2→ℝ。`X` 是 actual source witness，可包含 q/dq/time/w、
参数及满足 descriptor graph 的 acceleration；不把 workflow state.json 当数学 X。

```text
SourceContext:
  X : Type
  D : X -> Prop
  z : X -> Vec                     -- exact order x4,x5,y4,y5
  eta : X -> Eta                   -- independent nonlocal/context variables
  fullForce : X -> Force           -- actual full residual, already in consumer force units
  anchor : X -> X
  sourceIdentity : actual selected residual expression = fullForce on D
  anchorDomain : D x -> D(anchor x)
  anchorLocal : D x -> z(anchor x)=0
  anchorContext : D x -> eta(anchor x)=eta(x)
  anchorZeroFibre : D x -> z(x)=0 -> fullForce(anchor x)=fullForce(x)

  bias(x) := fullForce(anchor x)
  rc(x) := fullForce(x)-bias(x)
  fullSplit : fullForce(x)=rc(x)+bias(x)  -- derived, not another estimated bound
```

`anchorZeroFibre` 可由 actual graph 的唯一性与选定坐标/eta identity 推出，
也可直接提供；只要求 anchorLocal 不能推出它。不要添加不必要的全空间逆映射要求。
eta 不能把需要随 z 改变的 acceleration 也当作“保持不变的独立参数”。
anchor 改变 local state 后，相关 acceleration 必须重新满足同一 actual graph。

**两个 reference 不可混同：**已存在的 `full_equations_to_port` 使用 nominal a0，
其中 hSameB 要求 projB(a0)=projB(a)。这是消元用 reference；它没有要求 z=0。
centering anchor 要求 z=0，但其 aB 通常须由 anchor graph 重新确定。
不能把 hSameB 的 a0 直接塞进本契约 anchor，除非另外证明两者身份完全相同。

sourceIdentity 必须明确实际项与符号，包括 controller branch、regularizer、
analytic/FD/rounding/solve residual 的边界。不能把 source 的
`lTotal=lBase+rB` 简化为 fullForce=rB 而删除 lBase。

若本轮上游只能交**remote port**，允许另选 component 契约：

```text
fullForce = portForce + otherForce;
rcPort = portForce - portForce(anchor);
fullForce = rcPort + portForce(anchor) + otherForce.
```

这时八项界只针对 rcPort。otherForce 仍是依赖 actual state 的余项，不能改名为
“常数 anchor bias”，也不能在 full consumer 中消失。最小 full 契约不需要这个额外字段；
只有选择 component route 时才必须携带它及其后续 ledger。

## 2. Normalization contract：一次转换，明确加法与 power 单位

固定 force 顺序 human joints (4,5)，state 顺序 (x4,x5,y4,y5)。
source MBD 的列 (1,2,3,6) 是 distal acceleration correction，绝不使用同一个 state 索引类型。

最小 required fields 是：

- `stateMap`：actual q/dq 等到 z 的确切表达式、尺度及单位；不能仅列四个字段名。
- `forceMapIdentity`：raw/source residual 到 fullForce 的表达式与尺度。
- `powerIdentity`：选定 actual P5 residual power 等于 `(Lz)·fullForce`，
  L=[[1,0,1,0],[0,1,0,1]]；若另有项，必须单列 remainder。
- source/controller/normalization 的 version 与 byte hashes，和以上 typed identities 对应。

由运算维数推断，K[a,k]、G[a,k] 的单位必须相同且为 force[a]/z[k]。
x4+y4、x5+y5 的相加也需要 stateMap 给出相容尺度；ℝ 类型本身不会认证物理单位。
mass regularizer、M0BB 与 IVAL 是三个不同对象，不能互换。

已有 `normalizeRawPMI` 定义 diag(1/5,1/10) 的一次转换，但只针对真正的 RawPMIForce。
已是 MBD*v 或 IVAL*f-M0*a 的 generalized force，不再乘这次转换。
若 path increments 仍在 raw-PMI 单位，A 承担这一次转换；若 increments 已是
fullForce 单位，则 A=I2。二者是择一契约，不得叠加。

## 3. 对应现有 PathBinding 的最小有理数据与证明字段

```text
R,m,n : Nat
Aq : Fin2 -> Fin m -> Rational
Hq : Fin R -> Fin m -> Fin n -> Rational       -- all >=0
Sq : Fin R -> Fin n -> Fin4 -> Rational         -- all >=0
dxi : X -> Fin R -> Fin n -> Real
de  : X -> Fin R -> Fin m -> Real

state_bound     : D x -> |dxi[x,s,j]| <= sum_k cast(Sq[s,j,k])*|z[x,k]|
increment_bound : D x -> |de[x,s,i]| <= sum_j cast(Hq[s,i,j])*|dxi[x,s,j]|
force_eq        : D x -> rc[x,a] = sum_i cast(Aq[a,i])*sum_s de[x,s,i]
```

这些字段正好实例化 `NEW_KPATH_INTERFACE_Core.PathBinding D z rc`，没有额外隐藏
几何、FTOC、source witness。Aq 是固定矩阵，不是随 x 变化的 MBD(q)。若沿用变量质量块
分解，其变化项必须进入 de/increment bound 或另证完整 force_eq，不能冻结后丢项。
Hq 是 increment/Jacobian bound，不能拿 cone gap H 替代。

按有理算术定义
`Kq[a,k]=sum_{s,i,j} |Aq[a,i]| Hq[s,i,j] Sq[s,j,k]`。
现有 checker 要求 payload 同时携带此 Kq 并检查重算相等；它是冗余回执字段，不是
另一组独立估计。要绑定现有 transportedGain，还需有限和与 cast 的 exact equality。
若真正 source 表只有有理上界，应对该上界构造 PathBinding，或显式证明
`K_real<=Kq`；不能用不等式冒充 ExactComparisonBinding.path_entry_eq。

### 最小单段实例：把缺口压成实际 H 的八项界

在 fullForce 已有正确 source/normalization/anchor identity 时，可以定义：

```text
R=1, m=2, n=4;
Aq=I2, Sq[0]=I4;
dxi[x,0,k]=z[x,k];
de[x,0,a]=rc[x,a].
```

则 state_bound 与 force_eq 都是 identity 接线；唯一实质 bound 为

```text
forall x in D, forall a in Fin2,
  |fullForce(x)[a]-fullForce(anchor(x))[a]|
       <= sum_k cast(Hq[0,a,k])*|z(x)[k]|.
```

于是 Kq=Hq[0]，八项 comparison 恰好是 Hq[0,a,k]≤Gq[a,k]。
这不是通过定义 rc/de 证明该 bound；其八个 Hq 参数与实际 bound witness 仍待上游交付。
这里只压缩接口，不保证单段 estimate 足够锐利或可行。

若通过导数实现，可把实际 graph 参数化为 F(eta,z)，固定 eta，在 anchor 到 z 的合法
线段上证明 `|∂F_a/∂z_k|<=Hq[0,a,k]`、所需正则性与整段域包含性，再积分。
若当前 D 不允许该直线，回到多段 PathBinding；不能强行假设 star-shaped。
无需为了纯八项算术先提供 trajectory/terminal/全域覆盖证明，但这些 source/path
前提必须在宣称 actual bound 时履行。

## 4. 同一 G-family：字段共享，不靠重复字符串“相同”

```text
Gq : Fin2 -> Fin4 -> Rational, Gq>=0
G := NonnegativeGain(cast Gq)
Q : Vec -> Real
mu : Real
gap : ConeGapBinding G Q mu
cert : forall r : Representative, SPNWitness(gap.H(representativeCone r))
familyIdentity : selected certificate blob/entries realize THIS G,Q,mu,chart,L and cert
```

如果 certificate 使用有理 quadratic Q，则还给出 Pq 与
`Q(z)=sum_ij cast(Pq[i,j])*z[i]*z[j]`，不要额外假设 μ=某个 toy 值。
μ 是 absorption 参数，不是 descriptor mass regularizer。
同一 G 必须直接作为 comparison 与 gap 的共同参数；不允许二者各填一张同名表。
family hash 应覆盖 gain、μ、Q representation、chart convention、18个标签与证书数据，
不能只 hash 八项 gain，因为统一数值或排列对称性可能掩盖错误索引。

标签沿用现有 ConeIndex=(c4,c5) 的36项，18代表由首通道 IDs (0,2,3) 选择，
整对反号 rev=(1,0,5,4,3,2)。不重命名为旧64符号 schema，也不按矩阵数值去重。
`gap.flip_eq` 与 `gap.exact_gap` 是证明字段，不从标签数量推出。

## 5. 算术输入 ready 的最小门槛与最终 consumer 边界

一个外层 immutable manifest 引用现有严格 arithmetic payload，不往该 payload
添加 source 字段或修改 checker。最少记录 source/context/normalization/anchor 身份，
canonical rational payload bytes hash、family bytes hash，以及两者共享的 coordinate order。
实际证明对象由上面的 typed contract 提供；manifest 只负责定位，不能证明相等。

现有 payload 固定键 schema/scope/coordinates/path/K_cert；path 含 A/Hjac/Scoord/K_path。
使用 canonical rational strings、正分母，满足现有尺寸限制，足以重算八项并取
`cross[a,k]=num(Gq[a,k])*den(Kq[a,k])-num(Kq[a,k])*den(Gq[a,k])`。
comparison pass 当且仅当全部 cross>=0 且三表重算 identity 成立。
单段 full-force route 下仅缺8个 Hq 与8个选定 Gq 数值，而非缺一套新 schema。

三层状态必须分开（仅本 review 的概念分层，不修改 registry/state）：

1. **Arithmetic input ready**：有理表与同一 G 数据身份齐全，可以计算；尚非 source proof。
2. **Source-bound comparison**：上游 actual source/anchor/PathBinding 与 cast identities 齐全，
   八项 proof 可构造 `ExactComparisonBinding.toComponentLE`。
3. **Full power consumer**：同一 gap/cert 与 actual powerIdentity 齐全，得到 centered power
   界；full residual 仍保留 `(Lz)·bias`，component route 还保留 otherForce 的 power。

即使8个 cross全部非负，也不能直接声称 full residual power≤μQ。若需要此最终式，
须另证 bias/other power 为零或以预算吸收。相同地，μ<1、Q coercivity 与 Vdot/trajectory
结论属于后续消费者所需条件，不是有理 comparison 的输入门槛。

## 6. 已有 artifact 到字段的精确满足程度

以下路径前缀 W=`C:/Users/z5242/Desktop/重构版/工作流`；
E=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。
P=W/examples/routeb_p5_feasible_cone_spn_proof_attempt。
本轮逐项重新读取 hash；“有定义”不等于“已有 actual instance/proof”。

| 路径 | 已有字段/边界 | SHA-256 |
|---|---|---|
| E/routeB_compact_direct_descriptor_structure.jl | B/D indices、nominal rB/lBase/lTotal 公式、regularizer与分支定义；没有 actual graph/anchor/path bound | 2c2f623f966425952cbbbd3c04bae84858147fe7fdd386f5bc5f4ff35e2fb98c |
| E/routeB_compact_direct_descriptor_structure_dh.csv | 记录 dh 分支；不是 sourceIdentity 证明或 H 表 | 2ff3a201f480dbf5c697dcee01ee5e6f42583f20bc33176a5bf95983c9128b39 |
| P/NEW_P4_032_BlockDefects.lean | raw-PMI 一次 normalization 定义与带 eD/eB 的条件 port identity；未认证实际单位或消去 defects | aa1cce18e39b1b675483c9ece7cecbc1a2740c65df1846582ca57963c0a6cc51 |
| P/NEW_KPATH_INTERFACE_Core.lean | PathBinding/ComponentBinding、G-indexed gap/cert consumer 的类型；没有本轮 actual instance | 10c7e769e772a2f4475def1eb061e52319510cb906cb879c4234653f2d64a17c |
| P/NEW_KPATH_INTERFACE_RationalBinding.lean | 完整 cast identities + 8项 rational comparison 的 typed seam；没有 source proof instance | 2f46e4c077c44c91d5a9152140f2253dcfdf8c7d3edbebd4c4a6617c2e4ad06d |
| P/NEW_KPATH_INTERFACE_Comparison.py | 现成纯有理重算/cross-difference 算法；strict scope 仍 unbound，未运行 | d7dd1275a46bda19733d0d3e2700ca891f4759c918e62f786bd2a238f5c08392 |
| W/agent_review_inbox/review-P5-ACTUAL-KPATH-G-COMPARISON-20260908T195508Z.md | 前轮已限定范围的缺失/列错位报告；本轮不重新搜索数表 | d4a9fa3a38ae01751ea3472b86ce11d848809bab365db5b74190ef9eb9c85bc8 |

当前最小 obstruction 仍只有三个：
**实际 full/component residual 与正确 anchor/normalization 未实例化；
该对象的8项 H bound 未提供；同一坐标下选定 G-family 未绑定。**
新增泛型 adapter、复制 toy 表、重复 search 或旧 schema pass 均不补这三项。
上述单段 identity specialization 能减少上游需要交付的表，却不能产生缺失的 H/G。

本轮保持 pending；无 actual arithmetic run、无 Lean receipt、无 source/registry promotion。
