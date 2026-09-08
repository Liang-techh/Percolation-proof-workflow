---
kind: review_result
review_id: review-GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS-LOCAL-codex-20260908T102742
task_id: GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS
source_agent: codex-joint6-weighted-source-lane
created_at: 2026-09-08T10:27:42-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_SIGNED_WEIGHTED_CONSTRAINT_PACKET
source_binding_proven: false
actual_source_constraints_supplied: false
actual_same_cell_evidence_constructed: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: certify the two signed weighted source measurements together with existing measurements on the same residual; retain full principal RHS and construct matching determinant/numerator/observable witnesses
---

# 两条 signed weighted source constraints 接入 principal residual packet

## 1. 已有 rank 结果的准确用途

消费 `review-GH-MATH-P4-ROWSPACE-RECOVERY-MINIMAL-LOCAL-20260908T102010.md`
对候选 rational X 的结果：rank(X)=6，Y 为 X 的 rows4/5，目标物理投影为 P_B，
rank(Y)=2、rank([Y;P_B])=4。因此在全空间 residual 的线性恢复接口中，
恰需两个额外独立 scalar measurements。仅允许追加原始 rows 时则需要 {1,2,3,6}
四行。这不是实际非线性 source 集合上的无条件最小性结论。

本轮不重算 X 的逆或全部 row subsets，不认证 X 的 runtime 来源；
固定系数来自该 review 对 domain JSON SHA
`28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`
的精确有理审查。另消费现有 rowspace Lean REVIEW 的 source 边界以及
`review-GH-MATH-P4-JOINT6-DEFECT-ELIMINATION-LOCAL-codex-20260908T102031.md`。
本轮只新增本 review，不重复 threshold/Schur 标量代数，不做 Lean/source admission。

## 2. 固定同一 z，不能用不同模型的行拼接

对一个完整 source state x∈Omega，选定同一规范

```text
z=M(x) a_actual(x)-F(x),   y=X z,
B=(4,5), E=(1,2,3), physical joint j=6.
```

z 是 force-balance residual/defect，不是 a、nominal port、lBase 或预条件 residual y。
M、F 包含明确 controller、regularizer、单位及 analytic/FD/runtime 语义。
z 不自动为零；若定义 z:=M a-F，只得到恒等式，不得到任何 source bound。

从已审查的 C=P_B X^-1，系数为

```text
alpha = 41762158574623343465791/384000000000000000000000
beta  = 448027162654999/3840000000000000
gamma = 12877/800000
eta   = -366870171535679301/1600000000000000000000
theta = 80475217491279639/1600000000000000000
iota  = 3944154584391/80000000000000
kappa = 200739/4000000
```

定义两个测量泛函（这些定义不是新 source 证明）：

```text
w4=alpha*y1+gamma*y6,
w5=eta*y1+theta*y2+iota*y3,
z4=beta*y4+w4,
z5=kappa*y5+w5.                                        (R)
```

注意 eta<0。保留 signed w5 可允许抵消；用绝对值换掉 eta 会改变源方程。
y6 是 Xz 的第六行，可混合全部 physical residual 坐标，不是 z6。
恢复 z4/z5 不等于证明物理 row6，也不自动允许 joint6 消元。

令 Dm=diag(beta,kappa)，m=(y4,y5,w4,w5)，J=[Dm,I_2]。
若 Qm 是从六维 z 产生 m 的四行矩阵，则精确 dual identity 为

```text
J Qm=P_B,   z_B=J m.
```

weighted rows 还可写成 `w4=(e4^T-beta*row4(X))z`、
`w5=(e5^T-kappa*row5(X))z`。这说明它们正是已有两行缺少的物理信息方向，
不是从两个旧多项式展开中免费多出两条 source 定理。

## 3. 待 source lane 提供的两条 signed constraints

一般带非零值/defect 的合法 packet 应给

```text
y4=b4+dy4,   y5=b5+dy5,
alpha*y1+gamma*y6=c4+dw4,
eta*y1+theta*y2+iota*y3=c5+dw5.                        (W)
```

b=(b4,b5)、c=(c4,c5) 是同源已知函数/offset，dy、dw 是实际剩余缺陷，需有认证包络。
定义

```text
e0=Dm b+c,   e_delta=Dm dy+dw,
z_B=e0+e_delta.                                        (D)
```

零值特例需要真正证明 y4=y5=w4=w5=0，才推出 z_B=0。
若只有有界 measurement，就只能得到有界 z_B，不能宣称零 source rows。
已存在的 y4/y5 payload 也仍需 actual witness；不能只证明 w4/w5 就假定旧行已获认证。

如果 observable 只需一个 scalar，可能另外设计更少方向的接口；本任务是恢复两条
physical rows 供现有两行 packet 使用，不能用单一投影 bound 冒充两行恢复。

## 4. 接入保留 joint6 的 principal RHS

直接展开 z_B=(M a-F)_B，使用 (D)：

```text
S=M_BB,   u=a_B,
f0=F_B-M_BE a_E-M_B6 a6+e0,
S u=f0+e_delta.                                        (P)
```

这个 exact principal packet 保留四个远端 acceleration：a1,a2,a3,a6。
不需要 row6 或 d≠0；也不允许从 q6=0 推 a6=0。
两条 weighted constraints 恢复的是 z_B，而不是把 M_B6 a6 消成零。
measurement 中含 y6 和 RHS 中含 a6 是不同作用，不是重复计费。

符号以 z=M a-F 为准，故 e0/e_delta 加到 RHS。若输入使用 F-M a，其所有测量值和
defect 必须一起反号，不能仅翻转 w5 某项。
若 F 由另一 controller 修正而来，force correction 必须进入同一 F 或 z 一次；
不能在 weighted witness 中使用旧 F，又在 f0 中换成新 F 而漏掉桥接项。

## 5. Measurement/source mismatch 的必要余项

(R) 依赖精确 y=Xz。若存储/运行测量为 yhat=Xz+xi，且 what 也由同一个 yhat
按上述权重计算，则

```text
P_B z=Dm*yhat_B+what-C xi,   C=P_B X^-1.
```

遗漏 -C xi 会把预条件/组装误差当成 source 方程。
若 source 实际用 X_actual 而系数来自 X0，C0 X0=P_B 给
`C0 y_actual=P_B z+C0(X_actual-X0)z`；额外项需消除或预算。
其依赖未知 z 时不能无证明地拿当前目标 bound 循环补齐。
因此最小接口首选明确交付同一 rational X 的 exact measurement identity，
或完整携带这些 mismatch terms；哈希字符串相等本身不证明执行语义。

## 6. Metric：恢复矩阵与预算的相容接线

有 coordinate bounds 时可保守得到
`|e_delta,4|<=|beta|*b_dy4+b_dw4`，
`|e_delta,5|<=|kappa|*b_dy5+b_dw5`。
这不自动是给定 H 的二次型预算；相关性丢失必须明示。

一种保留联合相关性的接口：eta_m=(dy4,dy5,dw4,dw5)，提供同源 SPD Sigma 和
`eta_m^T Sigma^-1 eta_m<=B_m`，则因 J 满行秩，G=J Sigma J^T 为 SPD，并有

```text
e_delta^T G^-1 e_delta <= B_m.
```

若需要另一目标 residual metric H_B，必须另给 `H_B<=kappa_m G^-1`，才能推出
`e_delta^T H_B e_delta<=kappa_m B_m`。不暗设 kappa_m=1。
此处 Sigma 必须控制整个四维 joint measurement error，不能把四个独立 scalar bounds
未经组合就声明成这个 ellipsoid。未知 correlation 可另给保守有证明的组合。

另一可选路线：若已认证同源六维 z^T K^-1 z<=W，plain physical projection 给
`z_B^T (K_BB)^-1 z_B<=W`；不是简单截取 K^-1 的 principal block。
这需要真正的 full balance residual cap，不是 nominal port-only cap。

不要把 e_delta 与任意 force residual ell+r 混为同一对象；如需连接那个消费者，
再交同源 residual decomposition/action map。应用线性 map 时 nominal、port、
weighted error 和 mismatch 必须一起运输，同一缺陷不重复扣除。

## 7. Det 与完整 signed numerator：packet 的最后接点

同一 S=M_BB(x)，固定 observable covector nu（不是上述常数 eta，也不是 lBase）：

```text
D2=det(S),  b_obs=adj(S)^T nu,
N=nu^T adj(S)(f0+e_delta),
D2*(nu^T u)=N.                                         (N)
```

weighted-error 的 exact contribution 为

```text
Nerr = b_obs,1*(beta*dy4+dw4)
     + b_obs,2*(kappa*dy5+dw5).
```

若存在 measurement mismatch，还须加入 `-b_obs^T C xi`。
b_obs(x) 随 S(x) 变化，即使 nu 固定也不能拿别的 cell 的系数或 cancellation 使用。
首选同域包住完整 signed N，保留 eta*y1 与其他项的相关性；
fallback 才分别包 nominal 与 error 并明确损失。
若采用第 6 节 metric cap，可用
`|Nerr|²<=(b_obs^T G b_obs)*B_m`，仍须同域包住这个系数。

现有 SameCellEvidence 的接线位置是：

| 字段 | 本 lane 能提供的条件结构 | 尚需实际证据 |
|---|---|---|
| row1/row2 | (W)+(R) 代入 (P) | 同一 source z、X 和四条实际 signed measurement 值/defects |
| determinant_lower | D2=det(M_BB) | 同 Omega 的正有理下界 delta，不是 det(X) 或 origin determinant |
| numerator_upper | 完整 (N)，含 actual a6/remote 与 weighted/mismatch terms | 同 Omega 的 |N|<=R，不能用 port rho 替代 |
| observable_binding | nu^T u | 实际 observable、单位和 theta''=nu4*a4+nu5*a5 的轨迹语义 |

最后仍需 R<=delta*A_cap 等 gate。没有在本轮生成 delta/R/A_cap。
某个 metric cap 即使成立也不产生 determinant positivity 或 observable identity。

## 8. 最小性与 signed cancellation 的定向边界

在 unrestricted residual 接口中，取 y=e6，则旧 y4=y5=0 且 w5=0，但
z4=w4=gamma!=0；取 y=e2，则旧行与 w4=0，但 z5=w5=theta!=0。
因为 X 可逆，均有抽象 z=X^-1 y。这是两条独立信息方向，非物理可达反例。

反向说明 weighted constraints 可以弱于补四个原始零行：取
`y1=theta, y2=-eta, y3=y4=y5=0, y6=-alpha*theta/gamma`，则 w4=w5=0，
所以 z4=z5=0，但 y1,y2,y6 均非零。只需两个 signed source identities，
不必证明四个缺失原始测量都为零；然而两个新 identities 本身仍未获得。

本轮只用一次标准库 Fraction stdin 检查最后这个 cancellation 和 gamma/theta 非零，
未重跑 X 审计、Lean、Julia、source producer 或全回归。

## 9. 最终 obstruction

所需的新源约束已具体化为 (W)，恢复误差已具体化为 (D)，principal RHS、metric 与
signed numerator 已给出一致接线。它们是待填的证明义务，不是 source 已提供的约束。
尤其当已有 y4/y5 只是 symbolic/preconditioned payload 时，新增 w 的定义不产生
actual row evidence。还须固定同一 Omega、模型、加速度、X、force 和全部 defect。

pending / missing-source-constraints。只新增此 review，无 actual source rows recovered、
无 Lean/source admission、无 state/registry 修改或物理 closure。
