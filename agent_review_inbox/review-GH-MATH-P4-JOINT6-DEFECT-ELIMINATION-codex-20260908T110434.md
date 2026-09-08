---
kind: review_result
review_id: review-GH-MATH-P4-JOINT6-DEFECT-ELIMINATION-codex-20260908T110434
task_id: GH-MATH-P4-JOINT6-DEFECT-ELIMINATION
source_agent: codex-joint6-actual-numerator-audit
created_at: 2026-09-08T11:04:34-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_DEFECT_IDENTITIES_NO_ACTUAL_NUMERATOR_PACKET
source_binding_proven: false
actual_elimination_witness: false
same_source_numerator_bound: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: retain joint6 in the principal RHS; supply same-configuration actual residual and the selected matrix's determinant/signed numerator bounds before any elimination or packet admission
---

# Joint6 defect / numerator refresh：不将三种第六分量混为一谈

## 1. 结果与范围

本轮没有找到可消费的同一 source/configuration 的 actual elimination 或 Schur numerator
packet。新的 runtime-refinement review 仍是 receipt 规格而非 actual capture。
当前 joint6/adjugate 材料给出条件恒等式，不给实际源绑定或 det/numerator 包络。

读取/消费前轮 joint6 defect review、actual/runtime-refinement reviews，并本轮直接核对
`NEW_P4_032_AdjugateAcceleration.lean` 的 descriptor/packet 接口以及
`review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-LOCAL-20260908T101508.md` 的同源要求。
对 robot_formal_v1/interval_bounds 的 numerator/adjugate/Schur/joint6/actual/runtime
文件名做了定向查询，没有发现新的候选 packet。不是全仓库不存在证明。

仅新增本 review；无需再写 algebra sidecar。无 rank/Young 审计、Lean、Julia、solver、
全回归；不修改 source、旧 artifacts、其他 agent 文件、state 或 registry。

## 2. Physical row6、preconditioned row6、lift coordinate

固定完整 x=(q,dq,w)∈同一个 Omega、actual ahat、corrected chart M_A/F_A：

| 对象 | 精确定义/条件 | 不能替代什么 |
|---|---|---|
| physical row6 defect | z6=(M_A)6,*ahat-(F_A)6 | 不等于预条件第六行，未证明为零 |
| preconditioned row6 | y6=(Xz)6=sum_j X6j*zj | y6=0 不单独给 z6=0；含其他物理行 defect |
| lift 第三坐标 | 在 ahat=T_lift eta_acc 的实际代入成立时，现有 transform 给 ahat6=eta_acc,3 | 不给 force row6；不蕴含 ahat6=0 或 defect bound |

current nominal correction vector v_D 也不是 joint6 actual acceleration。
文件名/局部槽号不提供物理索引、单位或 source valuation。
只有同配置同次调用的 solve/model refinement 才能解释 z；当前缺少它。

## 3. Principal exact defect interface：无需 row6 消元

记 B=(4,5)、E=(1,2,3)，取

```text
A=(M_A)_BB, h=(M_A)_B6, u=ahat_B, v=ahat6,
p=(F_A)_B-(M_A)_BE*ahat_E,
Au+hv=p+z_B.
```

actual rows4/5 一旦成立，就有 `Au=f_pr`，其中 `f_pr=p+z_B-hv`。
不用假设 d≠0、row6=0 或完整矩阵可逆。principal packet 必须保留 actual v 与远端 ahat_E。
如果定义 z=M_A ahat-F_A，行等式按定义可成立，但未知 z 使 RHS 仍未受控；
这是 residual 记账，不是取得独立源约束或可用 numerator 上界。

若调用模型是 runtime M_R/F_R，则必须携带

```text
z=e_solve+(M_A-M_R)ahat+(F_R-F_A),
e_solve=M_R ahat-F_R.
```

nominal port 的 norm cap 不控制此 full force defect。误把 q6=0 当 v=0、或把
preconditioned y6=0 当 z6=0，都不合法。

## 4. 只有实际第三行与 d≠0 才能走 Schur

另有同一对称 source 矩阵的 actual row6：

```text
h^T u+d v=s+z6,
d=(M_A)66,
s=(F_A)6-(M_A)6E*ahat_E.
```

d≠0 时等价的 reduced equation 和恢复式是

```text
S=A-hh^T/d,
f_sc=p-hs/d+z_B-h*z6/d,
S u=f_sc,
v=(s+z6-h^T u)/d.
```

必须同时保留 z_B-h*z6/d。若用近似 inverse j，还需保留
`-h(1-jd)v` 的 inverse defect，不能由求解成功声明它为零。
现有 lift 或 y6 的 measurement 不能填充这条未预条件 actual row6。
把域上的 d 非零变成数值 quotient cap 还需分母控制；没有本轮认证的 d_min。

## 5. 两个 numerator 必须与自己的 determinant 配对

固定 observable covector nu，注意它不是 nominal force lBase。principal 路线取

```text
D_pr=det(A),
N_pr=nu^T adj(A)*(p+z_B-hv),
D_pr*(nu^T u)=N_pr.
```

相对于误删 joint6 与 defect 的 nominal `N0=nu^T adj(A)p`，实际遗漏正是

```text
N_pr-N0=nu^T adj(A)z_B-(nu^T adj(A)h)*v.
```

就算旧 N0 恰为零，也不能推出新 numerator=0。独立 defect 与 v bounds 可给保守
上界，但不能谎称保留 signed correlation。应在完整 RHS 上先收缩整个 signed numerator。

Schur 路线须另用
`D_sc=det(S)`、`N_sc=nu^T adj(S)f_sc`。若两条路线都由同一个完整 actual 方程得到，
则代数上 `D_sc*N_pr=D_pr*N_sc`；若两分母非零才可解释为相同 observable ratio。
这不允许把 N_pr 的包络配 D_sc 的下界，也不自动给任何正 denominator gate。
换路线改变了矩阵、RHS 和 defect，不能按字段名复用旧 bounds。

若用 scaled Schur，需同时 `S_tilde=dA-hh^T`、`f_tilde=d(p+z_B)-h(s+z6)`，
相应 determinant 和 numerator 都是未缩放对象的 d² 倍；d≠0 仍是等价性前提。
这些是 paper identities，不是本轮编译或 source enclosure。

metric 若用于界 z 或 projected defect，须与同一个 reference K 配对。
例如 Schur residual projection P=[I,-h/d] 的自然 reduced metric 是
`(P K P^T)^-1`，除非块比值恰好匹配，不能自动取 nominal K 的 Schur inverse。
这个条件沿用前轮 exact interface，不重做 scalar allocation。

## 6. 对现有 SameCellEvidence 的逐项缺口

当前 adjugate consumer 的实际接口要求对同一 domain/cell 给 row1、row2、
determinant_lower、numerator_upper、observable_binding；packet 另有正有理 delta 与 gate。
本轮只读其源码，不声称其编译状态有新证据。

| 字段/前提 | 当前缺口 |
|---|---|
| actual source/refinement | 无目标配置同次 M_R/F_R/ahat 与 solve/model-defect packet；runtime schema 不是 receipt |
| principal row1/row2 | 需物理 rows 或合法 weighted recovery，并保留完整 z_B、远端与 joint6；现有 two-X-row 标签不够 |
| Schur extra row6 | 缺同 source 实际第三行与可用 pivot 条件；不能以 lift/y6 代用 |
| determinant_lower | 缺所选 A 或 S 在同 Omega 的正有理下界；origin determinant、det(X)、其他 Cholesky pivot 不等价 |
| numerator_upper | 缺完整 N_pr 或 N_sc 的同域 signed enclosure，包含 actual defects/acceleration coupling |
| observable_binding | 缺固定 physical observable、坐标/时间单位及其二阶导数与 nu^T u 的关系 |
| metric/gate | 无新 matching-defect cap，亦无同对象的 delta/R/A_cap gate |

principal restriction 是当前最少额外前提的路线；不应为了两行 consumer 强迫消元 joint6。
如没有可认证的 actual v/远端项或 signed numerator，principal 也不能跳过其 enclosure。
先从已授权同次调用/refinement 取得真实 residual，再选择一条路线完整交付 packet。

结论：conditional identity / missing-actual-det-numerator evidence，保持 pending。
本轮不提供物理反例、不声称 VERIFIED、source admission 或 P4/P5 closure。
