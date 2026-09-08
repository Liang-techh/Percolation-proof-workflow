---
kind: review_result
review_id: NEW_REVIEW_P5_SAME_CELL_GRAPH_JET_ADDITIVE_CONTRACT_20260908
task_id: P5-SAME-CELL-GRAPH-JET-ADDITIVE-CONTRACT
agent: Sartre
status: CONDITIONAL_GRAPH_CONTRACT_DESIGNED_WITNESSES_PENDING
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# 同 cell graph jet 与 additive-port 最小闭环

本轮只设计 source/math contract 与只读 checker 的证据门，不生成 alpha/Y 数值，
不运行提取器、全回归或 Lean。仅新增本 immutable review_result；未来修正另命名。

## 1. 固定系数、状态与未知量

输入沿用 `examples/routeb_p5_source_jet/NEW_EXACT_DH_CELL_JET_20260908.py`，
当前读取 SHA-256 为
`3BD8AC1D468B6F73A5FF230F031CE3D38315B608C90AB0381762054BF0C5A6AE`。
该提取器锁定的六个 source/cell 哈希是本 contract 的输入身份，不能换成仅同名文件。
上轮生成的 coefficient-table digest 为
`c1cee2bc333ead4211842a086e68fae4f52fc95400c78e729935abba19dec139`；
本轮未重跑提取，后续 checker 必须重新计算并匹配该 digest。

令 z=(q,v,w)∈R13；x=(q,v)∈R12，w 暂作独立输入参数。
M:R6→R6x6，R:R13→R6；物理角度导数 DM 已包含 c/s pullback 链式法则。
固定 cell Ω⊂R13 及包含它的开集 U。时间/输入律单独绑定，不能仅由 |w|≤2推出。

每一点 z 的未知量：

- alpha∈R6：实际选定的 exact analytic model acceleration。
- Y∈R6x13：alpha 对 z 的完整 Jacobian，列序 q1..q6,v1..v6,w。
- 定义 M_k=DM[:,:,k]（k<6）；其余七个方向 M_k=0，因为现有 M 仅依赖 q。

所有方程均在同一 z、同一 q/c/s valuation、同一 source key 上：

```
G0_i(z,alpha) = sum_j M_ij(q)*alpha_j - R_i(z) = 0               (6 rows)
G1_ik(z,alpha,Y) = sum_j M_ij(q)*Y_jk
                  - DR_ik(z) + sum_j (M_k)_ij(q)*alpha_j = 0    (78 rows)
```

这是84个 graph 等式，不是84条从数据中已经证明成立的事实。
可导出为 exact polynomial constraints；不需要导出任何 inverse entries。
对 h∈R13，Yh 满足 M(Yh)=DR[h]-DM[h_q]alpha。

## 2. 数学闭环：存在唯一与 Y=Dalpha

所需条件是：M、R 在 U 上 C1，且每个 z∈U 的 M(q) nonsingular。
则每个 z 的 G0 有唯一 alpha；固定 alpha 后，每列 G1 有唯一解 Y[:,k]。
对 G0 的 alpha-Jacobian 恰为 M；隐函数定理给出局部 C1 解，唯一性使局部解一致，
从而形成 U 上的单值 C1 alpha。对 G0 求导即得到 G1，由唯一性确认 Y=Dalpha。

因此不用提供数值 alpha/Y，也能在条件定理层面证明 graph 非空且唯一。
这消除了“在空 graph 上普遍不等式真”的漏洞；只有 graph 等式、没有存在/可逆证据
时不能使用这个闭环。此处是数学论证设计，未给 Lean/kernel inhabitant。

若仅在闭 cell Ω 上有 det≠0，连续性可在每一点选取邻域；必须记录邻域处理及
M/R的延拓，不能把箱内点态 bounds 当作自动提供整个开集正则性。
若还要统一导数界，宜给覆盖Ω的有限开邻域或稍大的同源 cell U0⊂U。
当前 finite Fourier/多项式 pullback 在 q/v/w 上是光滑的；这一事实也需与实际
CSV evaluator 的函数身份接线，不来自 Float64 source 的函数名。

## 3. exact certificate 字段：可逆与正则性

每份未来 packet 至少包含以下字段及实际 evidence_ref/hash：

| 字段 | 要求 |
|---|---|
| source_key | M/C/G CSV、DH-gain/model代码、extractor版本、cell哈希、coefficient digest；regularizer与g0/controller语义 |
| state_map | q/v/w顺序、物理角度到c/s映射、block embeddings；全程使用同一 valuation |
| domain | Ω及U/U0精确定义、time/input参数域、source函数在开邻域定义的证明 |
| coefficient_binding | M/DM/R/DR 表与实际 source evaluator、导数的 equality；不是哈希本身 |
| invertibility | 以下任一 exact witness，且覆盖同一Ω/所需邻域 |
| regularity | C1与derivative equality；物理q导数不是独立c/s偏导；边界延拓/邻域证据 |
| graph_total_unique | 从invertibility推出每点唯一(alpha,Y)，或等价的已证明graph定理 |
| coverage | 若声称沿轨迹消费，真实初始集、输入律、轨迹存在/continuation及 stay-in-Ω；否则只允许点态条件结论 |

可逆 certificate 的可选形式（不要求全部）：

1. exact determinant expression d(q)=det M(q) 及同域 d(q)^2≥δ，δ>0。
   determinant identity 必须核验；无须显式求逆。
2. 若采用机械SPD路径，先给 M=M^T，再给 ∀u, u^T M u≥m||u||²、m>0 的 exact
   quadratic/SOS/interval witness。不能只凭正对角、抽样正定或已加入regularizer推断。
3. exact pivot/factor certificate，附所有相关 denominator/pivot 非零或正性证明。

允许 rational interval或SOS证书，但必须交实际可核验对象而非名称：
box endpoints、函数包含证明、outward arithmetic规则，或多项式恒等式、Gram矩阵
与exact PSD分解。若利用 circles c_i²+s_i²=1，记录 ideal multipliers 和 real pullback。
在覆盖真实lift域的超集证明 positivity足够；只列circle ideal却遗漏q/c/s关系的
不适当缩小域，不足以证明真实Ω上的结论。下游 graph positivity 中人为加入的
alpha/Y box约束，必须另证包含实际唯一graph，不能靠限制未知量避开坏点。

## 4. 图上的 additive port，不把 bound 当 graph

先固定分块，推荐与当前 block456 additive consumer 对齐：B=(4,5,6)、D=(1,2,3)。
不得换用旧2+4 contract。令 E_B/E_D 是固定坐标提取矩阵。
直接实际 remote port可定义在graph上：

```
p(z,alpha)=M_BD(q)*(E_D alpha)
d(z,alpha)=sigma*p(z,alpha)+d_local(z,alpha), sigma∈{+1,-1}
l_actual=v_ref+d
P_actual=beta-l_actual^T H l_actual
```

sigma、v_ref、d_local 和 P_actual 的实际目标身份必须由 source 残差定义证明；
graph只能绑定 alpha，不能替调用者挑符号或默认 d_local=0。
若p已包含完整remote acceleration贡献，不再添加nominal remote项。
若使用forced-defect port，则另给nominal subtraction与force/acceleration转换，
并将名义部分完整保留在v_ref，不能从直接port分支跳过去。

在唯一graph上交同域 additive cap：

`d(z,alpha)^T H(z) d(z,alpha) ≤ Delta(z)`。

可用无显式逆的 polynomial graph certificate 检查此界：证明 Delta-d^THd 在
Ω、lift关系与G0=0上非负。若证书含Y而实际cap不需要Y，可不引入G1，缩小证明规模。
该graph不等式配合total_unique才给出真实alpha上的界。
已有acceleration cap可以辅助，但必须与同源G0以及H、d的实际定义绑定。

## 5. 接入已有 additive consumer 的准确参数

已直接读取
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean:74`。
`combined_of_port_budget` 实际接受 lam>1、sq r≤W、schurNumerator≥0，结论为
target≤base-sq(ell+r)。这里参数 W 是标量cap，不是P5 moving metric W(t,x)。

还需真实线性metric transport T：∀u, sq(Tu)=u^THu。统一设置：

```
ell = T(v_ref), r = T(d), scalar W = Delta, base = beta
(lam-1)*(beta-target-lam*Delta) - lam*(v_ref^T H v_ref) >= 0
```

由graph cap得到hport，由allocation得到halloc，结论才是 target≤P_actual。
没有额外要求Delta随a_B为零；这就是允许additive而非homogeneous的接点。
T也不要求矩阵显式求逆，但必须交同H的factor/isometry证据或另用直接metric定理；
不能将Pi/sup norm、Euclidean norm、current mass metric与nominal H混用。
allocation、positive target若consumer要求、P_actual到physical PMI的身份仍独立。
本轮不编译/修改该consumer，不声称一次algebra调用关闭P5/physical source。

## 6. Y 的下游用途及 actual defect 边界

direct additive-port幅值consumer本身不需要Y。Y服务于后续DF与port derivative：

`Dp[h]=DM_BD[h_q]*(E_D alpha)+M_BD*(E_D Yh)`。

这让base residual导数可能复用同一个graph jet，但不是自动得到b或Db。
只有实际选定的 nominal F 与actual field f_actual绑定后，才定义
`b=f_actual+F`、`Db=Df_actual+DF`。
W/Wt/DW仍来自实际metric；additional variational e按实际变分方程定义，排除Db*xi。

若实际 acceleration满足 M*alpha_actual=R+z_defect 而不是G0=0，则必须新增同源
z_defect及Dz_defect字段：

```
M*alpha_actual=R+z_defect
M*Dalpha_actual[h]=DR[h]+Dz_defect[h]-DM[h_q]*alpha_actual
```

这不是允许本轮设z_defect=0。幅值界不能替Dz，runtime不光滑时也不能自动套C1 graph。
本contract的当前系数仅指明exact analytic branch；实际refinement需另行见证。

## 7. 最小只读 checker 设计与剩余交付

按以下门序检查，任何缺失保留pending，不写registry：

1. INPUT_IDENTITY：重算六文件/extractor/coefficients/domain hashes及变量序。
2. DERIVATIVE_BINDING：exact polynomial比较DM/DR与物理方向导数；检查R转录语义。
3. INVERTIBILITY_REGULARITY：核验所选certificate及domain/邻域，不能只读claimed=true。
4. GRAPH_TOTAL_UNIQUE：消费已证明通用线性解/IFT接口；不要求样本alpha/Y。
5. SOURCE_PORT：实际signed decomposition、block索引、H/T身份。
6. GRAPH_CAP：exact graph positivity证书，若有未知量bounds先证明包含性。
7. CONSUMER_ALLOCATION：检查同点Delta/base/target/lam，不重复收费。
8. COVERAGE：仅当声称轨迹/不变性时强制；缺失只能给条件点态结果。

当前已有：M/DM/R/DR exact提取器和哈希绑定的cell数据。
当前缺失的最小新对象：同域invertibility+regularity认证、实际source graph身份、
真实signed port/H定义及graph additive cap与allocation。alpha/Y数值不是必须的新文件。
实际W/Wt/DW、b/Db/e与trajectory coverage仍未提供，不能由graph唯一性推断。
本轮将这些缺口压成明确字段，不伪造解/界，不改变formal或registry gate。
