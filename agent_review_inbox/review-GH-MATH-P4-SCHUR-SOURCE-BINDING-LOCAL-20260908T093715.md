---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-SOURCE-BINDING-LOCAL-20260908T093715
task_id: GH-MATH-P4-SCHUR-SOURCE-BINDING
source_agent: Codex-independent-schur-source-lane
created_at: "2026-09-08T09:37:15-06:00"
inspected_commit: 5ce2f4582bca68ceac53dff49627e00c22f7e31d
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BlockDefects.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurElimination.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ClosureResearch20260908.lean
  - examples/routeb_physical_schur_binding_lean/PhysicalSchurBinding.lean
  - agent_review_inbox/review-GH-MATH-P4-DIRECT-BLOCK456-METRIC-TRANSPORT-codex-20260908T090216.md
  - agent_review_inbox/review-GH-MATH-P4-DIRECT-BLOCK456-Q6-RAY-SOURCE-BINDING-20260908T152743Z.md
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_factorized_descriptor_model.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_analytic_mass_full_cs_polynomial.csv
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_block456_port_bi_partition_probe.jl
integration_status: pending
admission: pending
admission_label: pending
proof_status: EXACT_MISSING_WITNESS_CONTRACT
source_binding: false
lean_compile_status: not_run
registry_mutation: false
state_mutation: false
formal_certificate_allowed: false
requested_action: retain the three-dimensional same-source witness contract and descriptor-only obstruction; do not instantiate scalar bindings by names or promote to registry
---

# Block-(4,5,6) Schur/source binding — independent local review

## 结论

当前缺口不是 generic Schur 代数，而是**同一 source state、同一块顺序、同一 metric、
同一 energy/residual/normalization 的 witness**。三个关键区别：

1. generic allocation 可以取 n=3；现有 force_absorption/accel_absorption 仍继承
   B=(4,5)、D=(1,2,3,6) 的 Fin 2/Fin 4 类型，不能直接作为 block456 producer。
   标量 absorb_relative_additive 本身不受此维数限制，可在三维预算另获证明后消费它。
2. 实际 target 是 beta_C−||ell+r||²_H；原 SchurPMIBinding 的 E−Q≤margin
   不等于 generic allocation 给出的 Young 下界。
3. 即使 r=0、descriptor 九条直接约束成立，也不推出 beta_C 足够、Schur binding
   或 FeedbackBinding。下面给出当前 beta 模板下的精确 descriptor 特例。

本轮只写此新 review，没有执行 Lean/Lake、Julia、solver、interval producer 或全回归。
纸面推导与一次 Fraction 检查均不是 compiled candidate，更不是 source closure。

## 1. 从当前 source 固定对象，不沿用二维符号偷换

以下 q_conf 是构型；Q 是标量平方残差，避免与 Lean 参数 q 混淆。
source 文件用 Julia 一基数组：C=[4,5,6]、D=[1,2,3]；
Lean 所需 cIdx=![3,4,5]、dIdx=![0,1,2]，均为 Fin 3 → Fin 6。

令 K=M0CC456=origin(Mdirect_CC)+10^-6 I，H=K^-1。
regularizer 只加一次；H 必须与 source 的 inv(M0CC456Q) 对应，不是 I、
B_up^-1、当前 M_CC(q_conf)^-1 或二维 nominal metric。

descriptor 定义的是以下**约束多项式**，不是实际执行状态自动满足的定理：

    M_DD^mu v + DeltaM_DC a = 0
    r = M_CD v
    ell = diag(IVAL_C) f_C − K a
    lT = ell + r

若另有 J M_DD^mu=I，则前两条给
v=−J DeltaM_DC a，r=R a，R=−M_CD J DeltaM_DC。
这是无 defect 的 nominal port。若实际 balance 是
M_DD^mu v+DeltaM_DC a=e_D，则 r=R a+M_CD J e_D；
若 local port 另有 e_C，则再加 e_C。不能忽略这些项或混淆 force/acceleration defect。
这个正号来自此处 balance convention；不能机械复制另一个 condensed forcing
表达式中的 e_C−M_CD J e_D。

同源 source witness 必须证明 state→descriptor valuation 满足这些等式，并把 a、
f_C、lT 对应到指定 reference/controller/solve。仅定义 lT:=ell+r 只闭合抽象对象，
没有证明其等于实际 residual。CS 变量还须绑定 sin/cos(q_conf)；
孤立单位圆约束不等于完整 source graph。

## 2. generic allocation 逐项对齐

选择固定实线性 T，证明对全部 z∈R³：
sq(Tz)=z^T H z。不能把默认 Pi/sup 范数当作这里的 Euclidean sq。

| generic 参数/前提 | 必须绑定的 block456 对象 |
|---|---|
| n | 3，不是旧 BVec 的 2 |
| ell, r | T ell_source, T r_source；同一个 T |
| base | betaC456(state)，不是 feedback 的 base |
| target | 所需 source margin floor t，当前 nonnegative target 可取 0 |
| sq r ≤ W | Q:=r_source^T H r_source ≤ W，非 Euclidean r² |
| lam>1 | source LAMBDA456=2，或另有绑定的局部 lambda |
| schurNumerator≥0 | (lambda−1)(beta_C−t−lambda W)−lambda L≥0，L:=ell^T H ell |
| total equality | lT=ell+r 和 T 的线性，不能由名字推出 |
| conclusion | t≤P_direct:=beta_C−lT^T H lT |

源码当前选
rho²=589578/1000000，
B_up=diag(133374,50185,33335)/1000000，
E_A=Aup=a^T B_up a，W=rho² E_A，
beta_C=(1/100)||a||²+(1/10)(||q_C||²+||dq_C||²)+(1/20)w²。
它们在文件中是固定诊断模板，文本中的 upward/resolved 不等于本轮已认证 bound/cover。

正确关系为：

    P_relaxed = beta_C − lambda W − lambda/(lambda−1) L ≤ P_direct.

source schur456 是 P_relaxed，direct_total456 是 P_direct；
lambda=2 时 generic numerator 恰为 P_relaxed−t。
精确恒等式保留补平方与 port slack 两项：

    (lambda−1)(P_direct−t)
      = (lambda−1)(beta_C−t−lambda W)−lambda L
        + ||T ell−(lambda−1)T r||²
        + lambda(lambda−1)(W−Q).

不能将 lT 放入 relaxed nominal square 后再扣 lambda W；
也不能从该恒等式推出 numerator≥0 或 W−Q≥0。

producer 的匹配列是 rho2_m0_upper，而非 rho2_upper/rho2_bchol_upper。
其代码注释与计算使用 L0^-1 R B_up^-1/2，其中 L0 L0^T=Mzero_CC。
尚需认证 Mzero_CC=K、正规向外舍入、每个 cell 状态及完整域覆盖。
本轮只定位/读取 producer 的有关表达式，不认证 ledger。

## 3. 两个 scalar Binding 不能按名称接线

### SchurPMIBinding

定义精确要求 E−Q≤margin。若取常见的
E=E_A、Q=r^T H r、margin=P_direct，展开后它等价于

    E_A ≤ beta_C − L − 2 ell^T H r.

generic allocation **没有给这条式子**，它只给包含 nominal loss 和 lambda charge
的下界。矩阵 Schur 消元恒等式也不产生它。

一种合法但不同的重新参数化是
E_star=beta_C−lambda/(lambda−1)L，Q_star=lambda Q。
Young 给 E_star−Q_star≤P_direct。
但是原 budget Q≤rho E_A+B 不能就此改名为
Q_star≤rho E_star+B；需重新证明能量比较，并相应缩放 rho/bias。
AbsorbedAt 还要求 E_star≥0。禁止把改名当成证据。

另一合法路线取 E=beta_C、Q=lT^T H lT，使 binding 为定义等式；
代价是必须另证**总**残差的 relative/additive budget，不能使用 port-only budget。
对已有 generic consumer，最小路线反而是不经过旧 SchurPMIBinding，
直接消费第 2 节的 matching-metric cap 与 allocation。

### FeedbackBinding

它独立要求 base≥0 与 E≤base+Q，而 residual budget 只有 Q≤rho E+B。
Schur lower comparison、matrix elimination、port cap 均不产生逆向比较。
同源 witness 必须明确 base 的含义和依赖；用 base:=E 虽形式上可满足，
却不会建立独立的能量上界。当前源 beta_C 也不能无证明地充当 feedback base。

若有合法闭环才可用 delta>0、rho+delta≤1 导出
delta E≤base+B，delta Q≤rho base+B。
gain c≠1 时门槛变为 1−c rho>0；不能只沿用 rho<1。
这些都仍是预算不等式，不是实际 trajectory bound 或 registry 事实。

## 4. 精确 obstruction：原点 port=0 不闭合 nominal budget

这是**九条直接 descriptor 约束的测试点族**，不声称机器人可达状态，
也不声称已证明完整 lifted ideal 或 source graph 上存在该状态。

取 q_conf=dq=w=0，CS 为真实原点，a=t e1，v=0，r=0。
此时 DeltaM_DC=0，f_C=0，所以三个 remote balance、三个 port balance 成立；
取 ell=lT=−K a 后三个 total balance 也成立。

在 K 对称且 H=K^-1 的 source 数学解释下，
L=lT^T H lT=a^T K a。
当前 CSV 有 296 数据行，M44 完整三行是物理行 269、270、271；
原点 270 的 sin5² 项消失，269 与 271 相加，再加一次 mu 得：

    K11 = 350003/3000000,
    Q = 0,
    E_A = (66687/500000)t²,
    P_direct = (1/100−K11)t² = −(320003/3000000)t².

因此 t≠0 时，端口平方为零仍有 P_direct<0。
SchurPMIBinding E_A Q P_direct 不成立；
FeedbackBinding E_A Q 0 也不成立。
若强用 base=beta_C，则 E_A−beta_C=(61687/500000)t²>0，仍失败。

这不是“机器人不稳定”或 source trajectory 反例。
它精确说明：当前九条 descriptor 接口与 port cap 不足以证明这些绑定或当前 beta positivity。
补救必须是：
- 给出真实 graph/domain 限制并证明它排除此类自由 a 点；或
- 更换 beta/能量分配并证明新 allocation；或
- 提供其他确实成立的 scalar binding。
不能仅给 total_eq456 的文本、r=0 或已编译 generic theorem。

本轮 Fraction 检查只核对当前 CSV 的 M44 原点和上述有理系数；
没有核验完整矩阵 SPD/inverse、Julia 解释器或 Lean source reification。
故反例的矩阵化结论仍明确使用对称/逆身份，不将 Fraction 升级为 source closure。

## 5. 最小缺失 witness 包

对指定域 X 的每个 x，只需要一个不可拆换来源的包：

1. **Identity:** source/config 哈希、C/D 顺序、一次 mu、reference/actual 语义、
   valuation 和 source residual 等式；直接 descriptor 九式成立；缺陷项要么证明为零，
   要么保留并预算。不要求先展开所有全局 DH 逆矩阵。
2. **Metric:** source K/H 的 reification 与 inverse/对称性，或直接给定 T 并证明
   sq(Tz)=z^T H_source z 及线性；两条 residual 使用相同 metric。
3. **Port budget:** 对同一 x 的 Q≤W。若经 absorption，另交三维 norm/action identity、
   defect branch、envelopes 和 strict slack；旧二维 typed producer 不可直接套用。
4. **Allocation:** lambda>1 与明确 t 的 numerator≥0，或直接证明 t≤P_direct；
   generic algebra 本身不生成 positivity。
5. **Optional scalar consumer:** 若仍要使用 SchurPMIBinding/FeedbackBinding，
   逐字提供它们的 scalar inequalities 与所有 E/Q/base/margin 同一性。
   不使用这些 consumer 的路线不必强求它们。
6. **Physical handoff:** 若要求 physical margin，再给 P_direct≤margin_physical
   的同一 normalization/domain 比较，以及 coverage/trajectory 等后续义务。

上述是 exact missing-witness contract，不是已填结构体。
在 inspected definitions 中没有发现可直接填充此包的 block456 artifact；
结论不扩大为“整个仓库不存在任何相关结果”。

## 6. 证据等级与文件身份

exact source identity 是源语义/valuation 等式；
budget inequality 是指定域上的单向估计；
compiled candidate 至多证明被编译声明及其显式前提；
registry admission 还要独立准入。四者不能互换。
本轮没有收集或声称任何新编译成功/VERIFIED；未读取现有 .olean 为本 lane 的证据。

| 主要输入 | 当前 SHA-256 |
|---|---|
| GenericSchurAllocation20260908.lean | A76375770D563F86F7DE80FDEA970E8D0D0FADD1ED917C262B725C7A8BA47648 |
| SchurPMIAbsorption.lean | F18F9FB180AEAFAAD0DC3CD5149894D03EE111DB5C45ABFB86CAA927DF4050E3 |
| BlockDefects.lean | AA1CCE18E39B1B675483C9ECE7CECBC1A2740C65DF1846582CA57963C0A6CC51 |
| descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |
| residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| factorized_descriptor_model.jl | C3007D5E30FEEB963A86B9589ADE3CA7D95B16316E753E8D18B007AA044CD427 |
| analytic_mass_full_cs_polynomial.csv | 1A1DB0B737ABAC58AFAE06E95766D2DA91C12425FE1BE388364F1DCA7DB59451 |

旧 metric review 内 generic hash 与当前不同；采用当前文件而非旧快照。
工作树起始有两个 body6 .olean 未跟踪文件，未触碰。外部 Julia/source 不属于此 workspace
commit 的版本保证范围，故单列字节哈希。无 state/registry/共享脚本写入、无旧 review 修改。

