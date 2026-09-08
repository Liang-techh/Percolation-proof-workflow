---
kind: review_result
review_id: review-GH-MATH-P4-ADJUGATE-PROJECTION-PACKET-LOCAL-20260908T094933
task_id: GH-MATH-P4-ADJUGATE-PROJECTION-PACKET
source_agent: Codex-independent-adjugate-packet-lane
created_at: "2026-09-08T09:49:33-06:00"
inspected_commit_start: 9ac591a4222f2d41f8bdf689c8f7bf202f32d7bf
inspected_commit: a370eff67b6d694a7387525a3a53ea94c85bd582
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean
  - agent_review_inbox/review-GH-MATH-P4-ADJUGATE-ACCEL-codex-20260908T082413.md
  - agent_review_inbox/review-GH-MIXED-ADJUGATE-REASSIGNED-codex-20260908T0830.md
  - agent_review_inbox/companion-T-P4-DESCRIPTOR-ACCEL-BRIDGE-liuguanyi-20260908T1215.md
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/dhport_lib.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/half_centered_bound_v1.json
integration_status: pending
admission: pending
admission_label: pending
proof_status: EXACT_MISSING_SOURCE_WITNESS_CONTRACT
source_binding: false
lean_compile_status: not_run
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: preserve signed projection and explicit source/observable binding; obtain one same-cell witness packet without mixing reduced matrices or numerator semantics
---

# Signed projected-adjugate packet — same-source interface audit

## 结论与增量

现有 source-independent 2x2 脚本的代数链在纸面上成立，但没有填入真实 source
的 SameCellEvidence。对 examples 中 SameCellEvidence/RationalPacket/
observableAcceleration 的定向文本搜索只找到该 sidecar 本身的定义及消费者，
未找到外部 source 实例；这不是整个仓库不存在任何相关证据的断言。

本轮增量是把缺失接口收窄成一个共同的 source→两行 descriptor→signed projected
numerator→affine second derivative 见证，并明确：
- 六维 source 的两行 restriction 与精确 Schur reduction 是两种不同合法入口；
- determinant、numerator、force defect 与 observable 必须使用同一入口/缩放/cell；
- 常数 packet 的独立 det/numerator bounds 有额外保守性，不等价于精确 ratio cap；
- singular、未绑定 observable、先绝对值化和跨 source 拼接的 obstruction 必须保留。

只新增此 review，不改 sidecar、旧 review、state、registry、共享脚本；
无 Lean/Lake、Julia、生产器执行、全回归或 source admission。

## 1. 现有数学端点的精确含义

对同一点的对称矩阵 S=[[a,b],[b,c]]、两行 S u=f，令

    D=a*c−b²
    N1=c*f1−b*f2,  N2=a*f2−b*f1
    Ntheta=ell1*N1+ell2*N2
          =(ell1*c−ell2*b)*f1+(ell2*a−ell1*b)*f2.

cramer_identity 不用 D≠0，即给 D*u1=N1、D*u2=N2；
projected_identity 给 D*(ell·u)=Ntheta。
这两条是恒等式，不包含界，也不包含 source 或微分语义。

projected_accel_bound 另消费
0<delta≤D、|Ntheta|≤R、R≤delta*A，
由 delta|ell·u|≤D|ell·u|=|Ntheta|≤R≤delta A 得 |ell·u|≤A。
本 packet 使用正 determinant；它不自动处理 D<0 或 D=0。
对称+det>0 不单独推出 SPD，例如 S=−I。加速度代数本身不需要 SPD。

RationalPacket 的 delta/R/A 是有理数，乘法 gate 是精确算术；
数字存在和 gate 成立不证明源表达式的 enclosure。
该结构没有单独保存 R≥0：非空同域 numerator_upper 会蕴含 R≥0，
但空 cell 上 evidence 可以真空成立。不得从一个空 cell packet 推全域覆盖。

## 2. 最小共同 source witness：逐项映射

| packet 字段/前提 | 必须提供的同一 source 见证 |
|---|---|
| DescriptorFields.domain 与 cell | 一个具体状态语义 X、目标域、cell 集合/边界；不能只有同名 box |
| a,b,c | 同一个对称 2x2 descriptor S 的三个 entry；固定 coordinate order |
| acceleration1/2 | 同一 source acceleration 在两个指定坐标的投影 |
| f1/f2 | 完整有效 RHS，包括 retained coupling 或精确消元及保留的误差 |
| row1,row2 | 对域内每个 x，真实 S(x)u(x)=f(x)，而不是数值 solve 被命名 exact |
| determinant_lower | 同一 S 的 a*c−b²，在同一 cell 有 delta≤D |
| numerator_upper | 对同一 S,f,ell 的完整有符号 Ntheta，先代数合并再 enclosure |
| ell1,ell2 | 冻结常数、单位与坐标投影；不能拿每 cell 不同 ell 拼成一个固定 observable |
| observable_binding | observableAcceleration=ell·u 的真实导数/语义证明 |
| RationalPacket gate | 同一 delta/R/A，且数值 interpretation 和 rounding witness 明确 |

最小逻辑构造就是现有 SameCellEvidence src cell p 的五个 field：
row1、row2、determinant_lower、numerator_upper、observable_binding。
无需新增泛型矩阵逆范数、sqrt 或全坐标加速度 cap。
但 src 必须绑定到目标 source；若仅新建一套满足五 field 的抽象函数，仍未完成真实 bridge。

Provenance 最小外壳：source bytes/config、exact-real/FD/runtime 语义标签、
coordinate map、reduction kind、force convention、cell identity、observable coefficients、
normalization scale 和 producer/checker 身份。哈希防止对象换源，但不证明五个 field。

## 3. 当前六维 DH source 到两行 descriptor 的两个合法入口

实际读取 dhport_lib.jl：
mass_matrix 由完整六体 Jacobian/惯量求和再加 mass regularizer；
arm_MCG 使用中心差分 C/G；
exact_ddq 最后计算 Mq \ (tau−Cdq−Gq)。
名字 exact_ddq 不使 Float64 backslash 成为精确方程。
mu/h 可通过参数覆盖；mutable globals、实际加载值和同一调用配置都需要绑定。

若选择旧 B=(4,5)，D=(1,2,3,6)，必须记录这个顺序。
不能把三维 block-(4,5,6) 数据当成 2x2；若从该三维块再消去 joint6，
需要另一条精确消元见证。

**入口 A：保留远端耦合的两行 restriction。**
从完整 exact balance M a=F 得

    S=M_BB, u=a_B, f_eff=F_B−M_BD a_D,
    S u=f_eff.

这里 a_D 不是无关常数，f_eff 的 enclosure 必须保留其 source 关系或另有界。
直接令 f_eff=F_B 会丢掉耦合。若 source solve 有 M a=F+e，
有效 RHS 应为 F_B+e_B−M_BD a_D。

**入口 B：精确 Schur descriptor。**
另给 J=M_DD^-1 的适当逆身份与同一完整 balance，得到

    S=M_BB−M_BD J M_DB,
    f_eff=F_B−M_BD J F_D.

要使用当前 symmetric packet，还须证明 S 对称；例如 M 对称且 J 为对称逆。
若有 source balance defect e，则
f_eff_total=f_eff+e_B−M_BD J e_D。
若只证明左逆，可得到相应消元恒等式，但不要据名字直接推对称/正定/det bound。

入口 A 的 det(M_BB) 与入口 B 的 det(S) 不是同一个 denominator。
Ntheta 也必须由对应的 f_eff 形成。全六维 det(M) 更不是任意两者的 det。

误差若通过某个模型 S0 保留，正确式为
S0 u=f0+[(f_actual−f0)−(S_actual−S0)u]。
必须对这个完整 e_model 的 projected adjugate contribution 处理；
不能只给 RHS difference 而忽略矩阵误差。对于固定同一 S，
Ntheta(f+e)=Ntheta(f)+ell^T adj(S)e；
可以分别认证并相加，但这是更保守的策略，不得宣称原有 cancellation 仍完整保留。

## 4. Affine observable 的最小微分义务

若实际观测为 theta(t)=ell1*q_B1(t)+ell2*q_B2(t)+theta0，
ell 与 theta0 固定，q 有相应二阶可微性，且 source u=q_B''，
才有 theta''=ell·u。sidecar 的 observable_binding 不证明这些事实。

对 theta=ell(t)·q(t)+theta0(t)，还会有
theta''=ell·q''+2 ell'·q'+ell''·q+theta0''。
对非线性 h(q)，还要 Hessian quadratic term。
最小反例：q1(t)=t、ell1(t)=t，则 u1=0，但 theta=t²、theta''=2。
任何忽略导数修正而用 R=0 的 packet 都会给错误 cap。

坐标/时间单位也必须相同。若 physical theta=s*theta_packet，
则 acceleration cap 要乘 |s|；若时间重参数化，还要对应二阶缩放。
theta0 只有在真正常数时才无加速度贡献。

## 5. Cancellation、分母关联与保留的 obstruction

### 两层 signed cancellation

已有族 S(t)=[[1,t],[t,1+t²]]、f=(t,1+t²)、u=(0,1)、ell=(1,0)
满足 D=1、Ntheta=0。在 |t|≤T，先拆成绝对值上界会产生
2T(1+T²)>0 的保守损失。这不是有效 upper bound 被证伪，而是最优零 cap 被抹掉。

另一个投影层反例：S=I，u=f=(t,t)，ell=(1,−1)。
N1=N2=t 各自非零，但 Ntheta=0。
即使先精确算 N1,N2，再分别取绝对值、最后三角合并，也会丢失 observable 特有 cancellation。
因此最佳入口是完整 ell^T adj(S)f 的相关表达式。

### det/numerator 同源与缩放

S'=s S、f'=s f（s≠0）保持 u，且在 2x2 中 D'=s²D、Ntheta'=s²Ntheta。
cell-dependent s 也逐点成立，但新的 delta/R 都必须对缩放后对象认证。
只换 determinant 或只换 numerator 不能保持 packet 含义。
一般逐行不等比例缩放还可能破坏显式对称形式，不能继续用同一个 b。

保留源关联还有第二种益处：取同源族 S=diag(d,1)、f=(d,0)、u=(1,0)、
ell=(1,0)，d∈[epsilon,1]，
0<epsilon<1。于是 D=Ntheta=d，真实 cap=1。
独立常数界 delta=epsilon、R=1 只能通过 A≥1/epsilon 的 gate。
这说明现有 packet 是充分条件，而非精确 ratio cap 的必要条件。
可选更强接口是 D>0 与 |Ntheta|≤A*D（仍 division-free、同点相关）；
该接口是本 review 的数学建议，不是现有 packet 已实现的新 theorem。
若 epsilon→0，uniform delta 消失，但每个 d>0 的 cap 仍为1，不能据无 uniform delta
宣称加速度无界。

### singular 与未绑定 observable

S=diag(1,0)、f=0、u=(0,t)、ell=(0,1) 时 D=Ntheta=0，
两个 descriptor 行都成立而 observable acceleration=t 无任意固定 cap。
不能把 0/0 cancellation 当成 D>0 的替代。
特定 singular observable 在 row space 内可能另有界，但须另立定理，不属于当前 packet。

若 observableAcceleration 是独立未绑定字段，即使 S=I、f=u=(1,0)、
ell=(1,0)、delta=R=A=1 全部满足，填 observableAcceleration=2 仍破坏结论。
这是现有 observable_binding 非可选的精确 obstruction。

## 6. 当前候选数据不能填什么

本轮重读两个 analytic remainder JSON 的顶层字段/状态：
均为 COMBINED_POLYNOMIAL_DESCRIPTOR_BOUND、formal=false，
scope 为 analytic CSV model、相同对称域及 |w|≤2、Not a flowpipe。
其来源/用途详见已读旧 adjugate review；本轮没有重跑 producer 或递归验证依赖。

JSON 顶层没有本 packet 的同一 2x2 descriptor、delta、Ntheta/R、ell 或 derivative binding。
六维 preconditioned remainder/acceleration remainder 不能按名字转为有效 RHS 或 observable cap。
旧 review 中的哈希匹配结果也不是本轮重新认证的 enclosure。
因此保留数据为 pending 候选输入，不填 SameCellEvidence，不做 source admission。

最小下一步不是重复 Cramer proof，而是 source lane 选定入口 A 或 B、冻结 observable，
提交一个实际 cell 的五项精确证据及 delta/R/A rational gate。
若要声称全域或时间区间成立，再补 cell cover 与 trajectory containment。
不要求 packet 自身承担 flowpipe，但不能在调用它后省略这一范围桥。

## 7. 检查范围与哈希

本轮检查：读取现有 sidecar 全文与 prior reviews，读取 dhport_lib 全文，
JSON 顶层/schema 状态、限定符号检索、数学恒等式与 obstruction 的纸面核对。
未编译 Lean、未执行 Julia/数值抽样/生产器/全回归。
源码写有 theorem 或 packet，最多是候选文本，不是本轮 kernel/compiled 证据。
exact source identity、enclosure inequality、compiled candidate、registry admission 四层独立。

| 输入 | SHA-256 |
|---|---|
| AdjugateAcceleration.lean | A39485ADEA19FFD31A2F46A9B6CF0160D888D08CA36C64F4D0E9461FB406B616 |
| review GH-MATH-P4-ADJUGATE-ACCEL | B337B05CF863A9DF7DB9074A399CB65BF81B9D46689609D1F2D417F53A7E08C7 |
| review GH-MIXED-ADJUGATE-REASSIGNED | 2CA3E8F8C1F5EA2509E7E1B11E51B9B0C8033F9E3024AF856DF3353FD7515AE7 |
| companion DESCRIPTOR-ACCEL-BRIDGE | 9E2F010E6E3AD37BD9921385ABAB5BEE624001AF50AF8DC82708357F74622BD5 |
| dhport_lib.jl | AEBE6DB09B2D943448C5D701631109DBA8F5EEB070CC66593E5DBACA26485936 |
| combined_descriptor_remainder_v1.json | 68596F1557AA709D86BC8711ED7985552684DFFE7FDE290ABF03B511F6BD9805 |
| half_centered_bound_v1.json | 225DAC3905B873B1FC4B8E2F4F5333CD985B909643C651CD63146A506F2E9DFC |

HEAD 在并行工作期间变化，以上文件字节分别取哈希；外部 source 不归此 workspace
commit 保证。没有修改或恢复其他 agent 文件。
