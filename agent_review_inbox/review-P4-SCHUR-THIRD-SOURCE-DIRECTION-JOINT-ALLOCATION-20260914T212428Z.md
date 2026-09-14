---
kind: review_result
review_id: review-P4-SCHUR-THIRD-SOURCE-DIRECTION-JOINT-ALLOCATION-20260914T212428Z
task_id: GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT
source_agent: codex-independent-mathematical-interface
created_at: 2026-09-14T21:24:28Z
inspected_commit: e5f3f7ec984511e5eec1fc17ff9cb17a652e00ec
status: CONDITIONAL_MATHEMATICAL_INTERFACE
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
lean_lake_run: false
state_mutation: false
registry_mutation: false
requested_action: check source-to-defect observation factorization first; then certify the missing signed coordinate against joint endpoint allocation
---

# P4 三维 defect：第三源约束的精确位置与联合 allocation

本轮只新增本 immutable review，不重复 generic Schur Lean sidecar，不运行 Lean/Lake、
source producer、synthetic helper 或回归。结论是带明示前提的数学接口，不是 actual source
witness，也不改变已有 source/coverage/admission 状态。

已读前序 observation-kernel repair、GYFY 的 w6 完成平方及 raw-box fallback。
因此不把“rank-two 加一个横截标量”“w6 平方 cap”或“八顶点 D cap”重新当作新贡献。
本轮增量有两项：

1. **在 source 空间判断到底缺几条观测**：二维 principal residual 不自动等于 d 的前两维；
   应检查输出 rowspace，而非只数已提供的 source rows。
2. **直接把第三方向的 signed interval 放入两条 Schur allocation**：
   得到四个一维端点不等式，保留 s 与 D 的相关性，避免分别取上界的额外损失。

## 1. “只补一条”究竟需要什么前提

首先区分三种对象：

- physical principal packet 恢复的 (z_A,4,z_A,5)，其中 z_A=M_A ahat−F_A；
- port defect d=r_actual−r0∈R³，坐标按 C=(4,5,6) 排列；
- scalar observations u=ell^T H d、s=(ell+r0)^T H d。

只有当现有两条 source-certified observations 在**同一个 d** 上确实具有 rank 2，
且其数值已有双侧/平方界时，一条横截其一维 kernel 的有界 scalar 才是一般情形的最小补充。
对 raw d4,d5，第三 row k4*d4+k5*d5+k6*d6 需 k6≠0。
对 u,s，需要先检查两个 covectors 独立；若 ell=0 或 r0 与 ell 共线，rank 可小于 2，
一个第三标量未必修复。已有 one-scalar generic result 的 rank-two 前提不能省略。

还需区分“rank 增加”与“达到预算”：近乎依赖的第三 row 会使 reconstruction 系数很大。
一侧约束 k^T d≤c 通常仍留下一条无界半射线；没有另一侧、平方约束或额外源域限制时，
它不能为 SPD D=d^T H d 提供有限 cap。

以上无界性讨论针对未附额外限制的 affine fibers。若真实源域另有 compactness、
graph equation 或有证据的非线性约束，可能使用这些约束替代线性观测；不能把自由 fiber
的数学反例称为实际可达轨迹。

## 2. 更合适的源层最小 gate：ker(R) 必须落入 ker(A)

固定配置/域中的一个参数值，写

```text
y ∈ R⁶,    d=A*y+b ∈ R³,
o=R*y+c_obs ∈ Rᵐ.
```

A 是 port-defect map，R 是真正已有的 source observations；不是从文件名推断的 selector。
对于固定有限矩阵、offset 与有界 observed o，仅靠这些观测控制 d 的充要结构条件是

```text
ker R ⊆ ker A
iff rowspace(A) ⊆ rowspace(R)
iff 存在 B，使 A=B*R.
```

充分性：d=B*(o−c_obs)+b。必要性：若 Rv=0 但 Av≠0，在同一非空 fiber
y=y0+tau*v 上 d=d0+tau*Av；SPD H 给正二次首项 (Av)^T H(Av)，D 随 |tau| 无界。
因此不是必须恢复全部六维 y，也不是必须让 R 本身 rank=6：
source 方向若落在 ker A，可被安全忽略。

允许添加自由选择的 exact linear rows、且不使用其他源域限制时，最少需要

```text
r_missing = rank([R; A]) − rank(R)
```

条新独立标量。证明：每加一行最多扩大 rowspace 一维；取 rowspace(A) 模掉
rowspace(R) 的一个基便达到这个下界。这是输出可观测性的计数，不是 source witness。

### 与上一轮实际 source-map 候选对照

上一轮在明确参考、同配置 N 与 X 可逆的前提下得到

```text
Dremote=(1,2,3), Bprincipal=(4,5)
N=M_DD, Cmat=M_CD
A = Cmat*N^-1*E_Dremote*X^-1.
```

若当前 principal packet 只恢复 z_A,4/5，则在 y 坐标中

```text
R = E_Bprincipal*X^-1.
```

右乘可逆 X 不改变 rank/rowspace 包含，且 E_Dremote 的行空间与 E_Bprincipal
的行空间相交为零。所以

```text
r_missing = rank(Cmat).
```

若 Cmat 的 rank 是 3，现有 z_A,4/5 对这个远端 defect map 并没有贡献两条有用方向，
一般需要**三条远端方向信息，而非再补一条 row6**。若 rank=2 或1，相应需要2或1条。
本轮没有计算/证明 actual Cmat 的 rank；这是带明确前提的 source-facing discriminator。
它不否定“已知 d4,d5 后补 w6”的定理，而是说明先要证明当前 packet 真的是 d4,d5。

这个结论也不自动涵盖所有其他 defect 定义。若 d 改成不同 total-force discrepancy，
应重新给 A/b 后计算上述 gate，不能把远端 map 的结果照搬。

### 比 rank tactic 更窄的 typed intake

令 T 是下节的可逆 3x3 defect 坐标变换。新增 source row k 后令 Rplus=[R;k]。
最适合可信 consumer 的证据可以直接是

```text
T*A = B*Rplus,
o_plus = Rplus*y+c_plus,
e = T*b-B*c_plus
--------------------------------
T*d = B*o_plus+e.
```

B 与 e 是精确证书数据；此式是有限 matrix/vector 代数，不需 kernel 内求逆/求 rank。
若观测使用带噪 yhat，必须把 measurement correction 纳入 o_plus/e，不能当成同一个 y。

参数随状态变化时，逐点 factorization 只证明值身份，不自动给 uniform bound；
还需同域 B/e 的有界性或直接的输出 enclosure。逐点 det≠0 不代替 uniform inverse cap。

## 3. 复用 exact H：同时运输 d、ell、r0，不只运输 D

使用前序冻结的候选 H=M0_CC^-1；它与真实 source 的身份仍须独立交付。记

```text
T(v) = (v4, v5, 350003*v6−50000*v4)
a4 = 3000000/350003 > 0
a5 = 4000000/200739 > 0
aw = 1000000/1750155002250009 > 0
H = T^T diag(a4,a5,aw) T.
```

第三坐标记 omega，不用外部 disturbance w 的名称：

```text
(p,q,omega) = T(d),     omega = 350003*d6−50000*d4
(e4,e5,ew) = T(ell)
(l4,l5,lw) = T(ell+r0).
```

同一个线性变换给出完整的 bilinear identities：

```text
D = a4*p² + a5*q² + aw*omega²
u = a4*e4*p + a5*e5*q + aw*ew*omega
s = a4*l4*p + a5*l5*q + aw*lw*omega.
```

这不是将原坐标 ell4,ell5,ell6 原样配给新的 diagonal metric；
第三 covector 的系数必须是 ew/lw，不能误用 ell6 或 (ell+r0)6。

若前面的 source intake 已证明 d=A*y+b，可先形成
omega=(350003*A6−50000*A4)y+(350003*b6−50000*b4)，再做有符号包络。
但它是否能从当前 Rplus 恢复，仍需第 2 节 factorization，而非仅凭这个形式恒等式。

## 4. 第三方向的 exact joint allocation：四个端点条件

先固定同一个 source parameter/valuation 中的 p、q、ell、r0、betaC、E_A、t；
所有系数/预算在本节 omega 区间上固定。定义

```text
QH(v)=v^T H v
Bbind = betaC−QH(ell)−2*ell^T H r0−E_A
Brem(p,q) = Bbind−2*a4*e4*p−2*a5*e5*q

Rtarget(p,q) = betaC−t−a4*(l4+p)²−a5*(l5+q)².
```

源第三约束为有证据的 lo≤omega≤hi，lo≤hi。desired binding 和 actual target 精确等价于

```text
2*aw*ew*omega ≤ Brem(p,q),                        (binding)
aw*(lw+omega)² ≤ Rtarget(p,q).                    (target)
```

第一式由 2u≤Bbind 得到；第二式由
Pactual=betaC−QH(ell+r0+d)≥t 得到。没有先对 s 取绝对值，也没有重复扣 D。

### Exact interval lemma

对整个闭区间 [lo,hi]，两式同时成立，当且仅当下列四个不等式成立：

```text
2*aw*ew*lo ≤ Brem,    2*aw*ew*hi ≤ Brem,
aw*(lw+lo)² ≤ Rtarget, aw*(lw+hi)² ≤ Rtarget.       (END4)
```

必要性：两端点都在区间内。充分性：binding 左侧线性，target 左侧为 convex quadratic，
各自在区间上的最大值出现在端点。lo=hi 退化为一个实际值，不需要除以 hi−lo。

证明完全不需要平方根。等价的几何解释是源 interval 被包含在一个线性半区间与
以 −lw 为中心的二次预算区间的交中。Rtarget<0 时没有可行 omega；
但不能通过人为缩小 source interval 或选择 omega 来制造包含关系。

这比仅给 Dcap 后检查 2*S+Dcap≤P0−t 更精确：
END4 直接控制同一个 omega 上的 2s+D，不把可能出现在不同端点的 worst s 和 worst D 相加。
原来的独立 cap consumer 仍正确，只是可能保守。

### 多参数/全 cell 的范围

若 p,q 也落在固定 box，且 ell/r0/betaC/E_A/t 在该 box 上固定，则对
(p,q,omega) 的八个 corner 分别检查

```text
2*u(vertex) ≤ Bbind
QH(ell+r0+T^-1(vertex)) ≤ betaC−t
```

即可且必须覆盖整个独立 transformed box：第一式 affine，第二式 convex quadratic。
这里新使用的是**带线性 signed 项的 total-target quadratic**；不重复前序单独 D cap 算法。
同一个 vertex 必须用于一次 target evaluation，不能从不同 source/metric 取各部分。

若 ell/r0/beta 等实际依赖这些变量，上述固定系数 convexity 结论不能原样使用。
合法做法是对剩余参数逐点给 END4 的同域统一证明，或证明完整实际表达式的所需
convexity/其他 enclosure。仅固定一个采样点不证明整个 source cell。
actual feasible set 小于 box 时，corner test 对该 box 精确，但对 actual set 可能保守。

## 5. 仍需独立输出 D 时如何接线

有 signed ranges p∈[pL,pU]、q∈[qL,qU]、omega∈[lo,hi] 时，前序完成平方给

```text
Dcap = a4*max(pL²,pU²) + a5*max(qL²,qU²) + aw*max(lo²,hi²).
```

这是独立 transformed box 的精确 D maximum，复用已有结果。
u/s 可由本节同一三变量 affine expressions 得到 signed upper/lower；
不能仅保留平方 caps 后宣称掌握了符号。

若只交 p²≤U4、q²≤U5、omega²≤Uw，则 D≤a4 U4+a5 U5+aw Uw 已足够。
但 signed Schur 的 u/s 仍需合法 upper bounds，或者采用上节联合直接 target。
从 squared caps 得到的对称 enclosure 会丢失符号信息，不应宣称等同 signed source intervals。

有两条合法消费路线：

- **兼容旧 gate**：提供 hActual/hChange、u≤U、s≤S、D≤Dcap 及两个 allocation，
  复用 joint_of_signed_defect_caps；
- **保留相关性的 gate**：直接证明 2u≤Bbind 与 2s+D≤P0−t，
  复用已有 actual_binding_iff、actual_target_iff，不要求先构造独立 U/S/Dcap。

两条路线都必须保留 same-source ell/r0/d/H 和 physical total identity。
后者免掉的是独立上界相加的损失，不是免掉第三源方向。

## 6. 可形式化但未实现的最小 lemma 接口

不新增 .lean，也不把以下 schematic signature 当作 elaborated theorem。

### L1 — affine_observation_factor_transport

```text
y: Fin n -> Real, A: Matrix (Fin 3) (Fin n) Real
R: Matrix (Fin m) (Fin n) Real, B: Matrix (Fin 3) (Fin m) Real
T: Matrix (Fin 3) (Fin 3) Real, b,c,d,o,e of matching dimensions

hd: d=A*y+b
ho: o=R*y+c
hfactor: T*A=B*R
hoffset: e=T*b−B*c
------------------------------------------------
T*d=B*o+e
```

只用 distributivity/finite sums；不需要 H SPD 或矩阵求逆。这个 exact factor witness
是“principal packet 已约束目标 defect”的入口，不和已存在的 rank-two abstract lemma重复。

### L2 — transformed_signed_quantities

给 hMetric:H=T^T diag(a4,a5,aw) T 与 T 的线性身份，
推出第 3 节 D/u/s 和 total norm 的表达式。可从已有 quadratic identity 极化，
或直接用 finite-sum ring identity。必须同时运输 ell、r0 和 d。

### L3 — interval_signed_quadratic_joint_iff

```text
a,c,L,B,R,lo,hi : Real
ha: 0≤a
horder: lo≤hi
------------------------------------------------
(∀ x, lo≤x -> x≤hi -> c*x≤B ∧ a*(L+x)^2≤R)
↔ (c*lo≤B ∧ c*hi≤B ∧ a*(L+lo)^2≤R ∧ a*(L+hi)^2≤R)
```

代入 a=aw、c=2aw*ew、L=lw、B=Brem、R=Rtarget。
证明可拆线性区间上界与平方端点上界；退化区间单独处理。
无 sqrt、无 inverse、无 source import，非空条件明确。

### L4 — source_endpoint_allocation_consumer

在同一个 configuration/domain parameter x 下：
给 source d/observation/metric/reference 身份，lo(x)≤omega(x)≤hi(x)，
以及逐 x 的 END4，输出
E_A−Qactual≤Pactual 且 t≤Pactual。
此处调用 existing iff gates，不复制 generic Schur proof body；
不是将所有参数全局冻结为常数。

后续真实 Lean 实现的关注点是矩阵/函数向量约定、transpose 方向、有限和与
Real inequality 的展开、interval 端点及 zero-width case。
本轮没有测试 import/tactic/axioms，也不声称这些 signature 已可编译。

## 7. 最小 source packet / exact obstruction

若已有数据真的是 d4,d5，下一份 packet 可小到：

1. 同源 defect/reference 与 H identity；
2. 第三 signed scalar omega 的 exact CSE（或一条可重建 omega 的横截观测），带 offset；
3. 同域非空双侧 interval 或平方 cap；
4. signed u/s 的上述身份与实际 E_A/betaC/t；
5. END4 或旧独立-cap allocation 的有效证明。

若已有数据只是 z_A,4/5，必须**先**交 T*A=B*Rplus 等输出恢复证书，
或交第 2 节算出的 r_missing 个有效方向；不能仍按“已有两维”直接索要一个 raw z_A,6。
例如远端 defect map 满秩时，z_A,6 甚至仍在 remote selector E_(1,2,3) 的补空间，
不控制缺失的远端三维 output。

若实际 source domain 已给别的足够约束，可把它们作为替代 producer；本轮没有构造这些对象。
既有 joint6 rational residual theorem、名义 port rho 或 source-independent generic lemma
都不是上述数值/域/source witness。

因此本轮交付的是更窄的输出恢复 gate 与联合 allocation 数学接口：
它指出怎样补、需要补几条、以及何时补完仍不够预算；没有 actual-source closure、
runtime/coverage、Lean/kernel 或 registry admission 声明。

## 输入字节快照

以下 SHA 仅追溯所读版本；写入后再次复核。未修改原文件、state 或 registry。

```text
agent_review_inbox/review_result_RVW-P4-SCHUR-ACTUAL-SOURCE-NEXT-GYFY-20260909T1123Z.md
6e06f14448c2314ecd46a35d77d22af67270bdfa133f9a713da1460257858d85
agent_review_inbox/review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-PACKET-kuangmanmozun-20260909T2232Z.md
9b034e45014b686a5d4c98edd9912d9413dc8c51df173bb866c62cef52283d06
agent_review_inbox/review-T-P4-OBSERVATION-KERNEL-REPAIR-kuangmanmozun-20260908T2242Z.md
113dfd96ec80bcc1c070aec37907e0c29b528301703a33ba8511950cb92bbb1f
agent_review_inbox/review-GH-MATH-P4-SCHUR-ACTUAL-SOURCE-NEXT-OBSTRUCTION-20260914T211034Z.md
784ed80bc9432fffc4d7f1ca624e8172237c79b326319bb95bbe93076c5a9233
agent_review_inbox/review-GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS-codex-20260908T110743.md
26628e5a9e7dffa08d0293068f19e1ea80382d6785cf7d565338b9957629715c
examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean
91a3a598ba6c6fb0278a127c8b94a34839f74eb3cd88d46b6d2ca4d4169c5ba7
```

