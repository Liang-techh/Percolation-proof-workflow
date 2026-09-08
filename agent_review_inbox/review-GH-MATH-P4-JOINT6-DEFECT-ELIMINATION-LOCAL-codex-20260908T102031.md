---
kind: review_result
review_id: review-GH-MATH-P4-JOINT6-DEFECT-ELIMINATION-LOCAL-codex-20260908T102031
task_id: GH-MATH-P4-JOINT6-DEFECT-ELIMINATION
source_agent: codex-joint6-defect-math-lane
created_at: 2026-09-08T10:20:31-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_EXACT_ELIMINATION_AND_METRIC_INTERFACE
selected_source_route: principal_restriction_retaining_joint6_coupling
schur_route_status: conditional_alternative_requires_actual_row6_and_nonzero_pivot
source_binding_proven: false
actual_same_cell_evidence_constructed: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: retain the selected principal source route; supply actual rows and full defects, and use the exact projected metric if a distinct Schur route is later authorized
---

# Joint-6 coupling：restriction、defect elimination 与同源 metric/numerator

## 1. 范围与结论

本轮消费以下现有接口，不重复 joint-threshold 标量分配或 cone-index 泛化：

- `review-GH-MATH-P4-3D-TO-2D-RESTRICTION-LOCAL-20260908T155955Z.md`；
- `examples/routeb_p4_3d_to_2d_restriction_lean/REVIEW.md`；
- `review-GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS-LOCAL-20260908T160325Z.md`；
- `review-GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE-LOCAL-20260908T160907Z.md` 中当前 restriction 与缺失 witness 段。

现有 source lane 已选 principal restriction，保留 joint6 与远端 coupling。
本轮不更换其域或路线；Schur elimination 作为条件替代接口单列。
当前缺口仍是 actual balance/defect witness，不是一个额外标量 threshold。
只新增本 review；无 Lean/Lake、producer、solver、全回归或 source/state/registry 修改。
下述是实数矩阵纸面推导，不是 compiled theorem 或实际源认证。

## 2. 固定同一个源状态与 defect convention

块序 C=(4,5,6)，B=(4,5)，j=6，E=(1,2,3)。固定完整 source state x∈Omega，
actual acceleration (u,v)=(a_B,a6)，以及一个明确选定的三维 descriptor：

```text
T = [[A,h],[h^T,d]],
T (u,v) = g0+epsilon,
g0=(p,s), epsilon=(epsilon_B,epsilon_6).                 (F)
```

这里先假定 T 对称，仅为使 h^T 对应下左块；非对称情形应另用 k^T，下文 h*h^T
改成 h*k^T，并且不能直接套 SPD metric/determinant API。

若 T=M_CC 且完整 convention 是 M a=F+e，则
`g0=F_C-M_CE a_E`、`epsilon=e_C`。p 已保留远端 acceleration，不能删掉。
若先消去 E，则 T 和 g0/epsilon 都改变，epsilon 变成
`e_C-M_CE M_EE^-1 e_E`；不得只换矩阵却保留原 RHS/defect。
以上两种 T 均不自动等于 nominal residual reference K=M0_CC。

若以模型 (T_m,g_m) 替换实际 (T_a,g_a)，精确同向 defect 是

```text
epsilon_m = epsilon_a+(T_m-T_a)(u,v)+(g_a-g_m),
T_m(u,v)=g_m+epsilon_m.
```

矩阵误差乘 actual acceleration 也必须控制；不能只预算 forcing 差。
若用待证 acceleration cap 证明这个 defect，再用该 defect 证明同一个 cap，
需要独立闭合论证，不能循环假设。

## 3. Principal restriction：没有除法，但不能丢 v

(F) 的前两行精确给出

```text
A u = f_pr+epsilon_B,
f_pr = p-h v.                                          (P)
```

其最小输入只是 actual rows4/5。无须 row6、d≠0、T invertible 或 SPD。
但需要绑定并控制同一 actual v；q6=0 不蕴含 a6=0。
仅当另证 h v=0 才能把 f_pr 改成 p。

若保留 p-h*v0 作为近似 RHS，遗漏项不是零，而是
`epsilon_pr=epsilon_B-h(v-v0)`。
若 v 已经作为 actual source 量放入 f_pr，其误差不得同时再按同一项重复计入 epsilon_B。

前两行不是完整三行的等价替代；(P) 不蕴含 row6。
已选 principal source lane 可以只为其两行消费者证明 rows4/5，但不能宣称 actual 三行已齐。

## 4. Schur elimination：d≠0 与完整 effective RHS

增加实际第三行与 d≠0：

```text
h^T u+d v=s+epsilon_6,
v=(s+epsilon_6-h^T u)/d.
```

代回前两行得到

```text
S=A-h h^T/d,
f0=p-h s/d,
epsilon_eff=epsilon_B-h epsilon_6/d,
S u=f0+epsilon_eff.                                    (S)
```

等价接口是“(S) **加上 v 的恢复式**” iff (F)，不是只留下二维方程就丢弃第三行。
如果 d(x) 在域内接近零，点态非零仍不供应统一数值界；应另给 |d|>=d_min>0，
或直接给所需 correlated quotient 的有效包络。SPD 足以给 d>0，但 descriptor 语法不给 SPD。

取 P_T=[I_2,-h/d]，则精确 residual elimination 为

```text
P_T [T(u,v)-g0] = S u-f0 = epsilon_eff.
```

同时保留第三行 residual，可组成可逆行变换
`Jrow=[[I_2,-h/d],[0,1]]`，所以 `(epsilon_eff,epsilon_6)` 才保留完整 residual 信息。
仅 epsilon_eff=0 不推出 epsilon=0：kernel 含 `(h t/d,t)`。

### 近似 inverse/pivot 不能假装 exact

若程序使用标量 j 近似 d^-1，定义 S_j=A-h j h^T、f_j=p-h j s，则精确式为

```text
S_j u=f_j+epsilon_B-h j epsilon_6-h(1-jd)v.             (SJ)
```

最后一项是 inverse defect；只有 jd=1 或额外证明它为零才可删除。
同理远端 E 的近似 inverse 也要保留其 inverse residual，不得仅凭求解器成功当精确消元。

### d=0 的边界

不能由 d=0 宣称完整 T 不可逆，也不能继续除以 d。
例如 T=[[1,0,1],[0,1,0],[1,0,0]] 的 determinant=-1，仍可逆。
可换一个合法 pivot/块，或保留 joint6。将方程乘 d 后得到的 scaled 二维关系在 d=0
只是必要关系，不能反推原三行；它会丢失约束。

## 5. Metric：RHS 消元矩阵 T 不必等于预算 reference K

令真正预算为 Q3=z^T K^-1 z，K 为同一 source reference 的 SPD 矩阵，分块
`K=[[K_B,k],[k^T,k6]]`，z=(y,t)。K 与 T 不应按维数或名称认同。

对任意满行秩二维投影 P，设 G=P K P^T，则 G SPD，且

```text
w=P z,
z_perp=z-K P^T G^-1 w,
P z_perp=0,
Q3=w^T G^-1 w+z_perp^T K^-1 z_perp.                   (M)
```

因此 `Q3<=W` 可给 `w^T G^-1 w<=W`，无需把 T=K 作为隐藏假设。
这也是同一投影值 w 上 Q3 的最小值：取 z=K P^T G^-1 w 达到第一项。

- Principal 投影 P=[I,0]：G=K_B，得到 y^T K_B^-1 y<=W。
  不是直接截取 H=K^-1 的左上块；那个块是下面 K_s^-1。
- T-based Schur 投影 P_T=[I,-q]，q=h/d：
  `G_T=K_B-k q^T-q k^T+k6 q q^T`。
  若 `K_s=K_B-k k^T/k6`、`v_K=q-k/k6`，则
  `G_T=K_s+k6 v_K v_K^T`。
- 只有 q=k/k6 时 G_T=K_s，才可无额外损失沿用 K 的 Schur metric。
  这要求块比值相等；仅 T、K 都 SPD 不够。

若消费者必须使用 K_s^-1 而非 G_T^-1，可给有证据的转换系数

```text
kappa=1+k6 v_K^T K_s^-1 v_K,
G_T <= kappa K_s,
w^T K_s^-1 w <= kappa w^T G_T^-1 w <= kappa W.
```

这来自 rank-one whitened comparison。全域需包住 kappa(x)，不得暗取 1。
metric 系数的转换不是 defect 重复计费，而是改变输出二次型所需的独立比较。

把 P 施于 residual 拆分时，必须同时施于 nominal、port 和实际 defect：
`P l_actual=P ell+P r_port+P defect`。P(x) 点态依赖状态不破坏此恒等式，
但其时间导数不能省略 dP/dt；它不自动构造固定 observable 的二阶导数。
此外 Q3 原预算若含 a6 的输入能量项，投影输出不能授权删除 RHS 上的该项。

## 6. Signed numerator：同一 S、完整 RHS、同一固定 observable

为对接现有对称二维 adjugate consumer，选定**一种**路线后的
`S=[[a,b],[b,c]]` 与 `f=f0+epsilon_eff`（principal 则 f_pr+epsilon_B）必须成对使用。
令 nu 为固定 observable covector，不是 nominal force ell。则

```text
D2=ac-b²,
N=nu^T adj(S) f
 =nu1(c f1-b f2)+nu2(a f2-b f1),
D2*(nu^T u)=N.
```

保留相关性的精确 defect 分裂：

```text
N=N0+Ndef,
N0=nu^T adj(S) f0,
Ndef=nu^T adj(S) (epsilon_B-h epsilon_6/d).
```

应先形成整个 signed N 再做同 cell enclosure。独立绝对值上界可作为明确标注的保守
fallback，但不能称为保留 signed cancellation。若只拿到 metric defect budget
`epsilon_eff^T G^-1 epsilon_eff<=Wdef`，设 b_obs=adj(S)^T nu，则
`|Ndef|²<=(b_obs^T G b_obs) Wdef`；这里必须使用对应的 G 与 epsilon_eff。
只有端口 Q3 上界不能替代实际 epsilon 的预算。

分母 gate 可以取同域有理 `delta>0, delta<=D2`、`|N|<=R`，再要求
`R<=delta*A_cap` 得 |nu^T u|<=A_cap。若 D2<0，数学上可走 |D2| 下界的另一个接口，
但不能把负 determinant 直接塞进当前正 determinant gate。

Schur 路线 det(T)=d det(S)。若 det(T)>=Delta>0 且 0<d<=d_upper，
则 det(S)>=Delta/d_upper。单有 d 的正下界不能给这个商的正下界。

无除法版本必须同时缩放矩阵、RHS、defect：

```text
S_tilde=d A-h h^T,
f_tilde=d p-h s+d epsilon_B-h epsilon_6,
det(S_tilde)=d² det(S)=d det(T),
N_tilde=nu^T adj(S_tilde) f_tilde=d² N.
```

二维 adjugate 的一次缩放与 RHS 的一次缩放产生 d²，不是 d。
d≠0 仍是等价性前提；d<0 时不能从 T 的 SPD 解释借正性。
scaled/unscaled numerator 和 determinant 必须整体配对认证，不能混用旧字段。

## 7. 三个定向边界检查

一次内存内 SymPy 精确有理计算（无 source import）核对下列例子及 (M)/(SJ) 实例：

1. T=[[2,0,1],[0,1,0],[1,0,1]]，g0=0，epsilon=(0,0,1)，actual (u,v)=(-1,0,2)。
   T(u,v)=epsilon；S=I_2，epsilon_eff=(-1,0)，nu=(1,0) 时 signed N=-1。
   只保留 epsilon_B=0 会错误给 u=0。近似 j=3/4 的 (SJ) 也精确成立，
   缺少最后 inverse-defect 项则不成立。
2. 取同一 K=T，但描述符投影 q=0，z=(2,0,1)。Q3=2；正确 principal metric
   y^T K_B^-1 y=2；误用 K_s^-1 得 4，违反未经转换的上界 W=2。
   因而一般 RHS 投影不能自动套 nominal Schur metric。
3. 取该 K、q=(2/3,-1/5)，精确核对 G_T=K_s+k6 v_K v_K^T 及 (M) 余项恒等式。

这些是抽象接口检查，不是 source counterexample、完整公式的机器证明、Lean receipt
或矩阵 enclosure。一般式由前述纸面代数给出；没有做数值扫描/全回归。

## 8. 本 lane 的最小交付包与 obstruction

保留当前 principal 选择时，只需先补：同 Omega、同 DH/controller/regularizer 的
actual rows4/5、完整 f_pr+epsilon_B、actual a6/remote quantities 的合法包络，
以及选定 A 的 determinant、signed numerator、固定 observable 身份。
不存在“必须先消元 joint6 才能完成两行接口”的数学要求。

若后来选择 Schur，则增加实际 row6、d≠0（统一 enclosure 还需分母控制）、
effective RHS/defect 与 v 恢复式，并为选定 S 重新绑定 numerator/determinant。
如还使用 residual budget，须按 P_T K P_T^T 运输 metric，或给出明确 comparison。

消费的 actual-three-row 与 source-semantics reviews 均仍列出 actual row/defect、
det/numerator/observable witness 缺失。本轮不重新读取外部源，不断言所有仓库都不存在
这些证据，也不制造 delta、R、A_cap 或 authenticated source packet。
现有 symbolic correction equation 不是缺失的实际 joint6 force row；
preconditioned 两行也不在没有 row-space recovery 身份时变成未预条件的三行。

pending / missing-witness obstruction。无 source admission、无 registry promotion、
无 actual trajectory/closure 结论。本轮没有更改已选 source route 或既有 artifacts。
