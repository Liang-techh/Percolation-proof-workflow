---
kind: review_result
review_id: NEW_REVIEW_P5_K7_REAL_BLOCK456_INSTANTIATION_20260908
task_id: P5-K7-REAL-BLOCK456-INSTANTIATION
agent: Sartre
status: REAL_FIELD_MAPPING_DEFINED_SOURCE_JOIN_AND_PSD_INSTANCE_PENDING
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# K7 schema 的真实 block456 字段实例化

本轮补真实source代入，不重复上一轮通用PSD schema全文。
直接读取block456 descriptor、residual Schur interface和GenericSchurAllocation原声明。
只新增本immutable review，不造Q/Delta/alpha数值，不改state/registry或旧文件，
未运行Lean、外部producer或回归。

## 1. 真实source字段与最先需要阻止的误接

外部根D：`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`。
`routeB_compact_block456_descriptor_structure_audit.jl` 给出：

- DIDX456=[1,2,3]，CIDX456=[4,5,6]；mu=1/1000000。
- MDD456、MDC456、MCD456来自Mdirect；M0DC456/M0CC456为origin substitution，
  M0CC456含同一regularizer；DeltaMDC456=MDC456-M0DC456。
- fC456含factorized-model Kp/Kd/Bfr/GwI、MGL_C456和4/5交叉项。
- lBase456=diag(IVAL_C)*fC456-M0CC456*aC456。
- nominal_eq456=MDD456*vD456+DeltaMDC456*aC456。
- rC456=MCD456*vD456；lT456=lBase456+rC456是descriptor约束。

实际同cell graph提取器的未知量alpha却是完整六维analytic acceleration，满足Malpha=R_DH。
不能设vD456=alpha_D：前者是nominal-subtracted remote difference，不是完整remote acceleration。
同样，Mdirect与CSV M的多项式同一性、factorized fC与DH-gain source的nominal定义
都需要证明，不能由block名称或mass origin值相同直接替代。

## 2. 两条合法的7x7实例化路线（都仍有source前提）

### A. Direct actual remote port

用E_D/E_C作为6维acceleration的3行selection matrices。
若actual target允许带符号分解为d=sigma*MCD*E_D*alpha+d_local，
则K7取 L=sigma*MCD*E_D（3x6）、d0=d_local（3-vector）。
但必须重新证明与该direct port匹配的v_ref和l_actual；不能直接借用旧lBase456，
也不能把完整remote contribution和旧nominal residual重复加一次。

### B. 保留旧 nominal-subtracted rC 的 polynomial-cleared 路线

记A=MDD，B0=M0DC，B=MDC，C=MCD，R_D=E_D R_DH。
定义nominal remote eta为唯一解：

`A*eta=R_D-B0*alpha_C`。

如果真实full graph给A*alpha_D+B*alpha_C=R_D，则v=alpha_D-eta满足
A*v+(B-B0)*alpha_C=0，与nominal_eq456的符号一致。
这一步要求A可逆及上述同源等式；M可逆本身不保证任意principal block A可逆。

不必显式导出A^-1。令δ=det A、J=adj(A)，提供exact identities
A*J=J*A=δI以及同cell δ≠0。于是：

```
δ*rC = Ls*alpha+d0s
Ls = C*(δ*E_D + J*B0*E_C)       (3x6)
d0s = -C*J*R_D                  (3-vector)
```

这里d0s保留完整remote forcing，不能删为0。Ls/d0s是从已选source可生成的
polynomial表达式，本轮没有生成其系数或认证它与actual target相同。
若actual signed d=sigma*rC+d_local，则对应Ls乘sigma，
d0s改为sigma*d0s+δ*d_local，仍需d_local的真实表达式。

采用scaled port ds=δ*d和scaled cap Delta_s=δ²*Delta。
用Ls/d0s/Delta_s构造相同7x7 K_s，不增加未知alpha维数；K_s PSD给
δ²*d^THd≤δ²*Delta。由δ≠0、δ²>0才恢复unscaled hport。
δ可为负，无须强加δ>0；不能在δ=0点约去δ²。
这给出保持旧nominal port的最小polynomial adapter，避免把vD当actual alpha_D。
若不做该elimination而直接加eta三个未知量，原7x7模板要扩成10x10，
不能隐瞒未知量增加却仍把证书标成K7。

## 3. Q/K/metric/Delta 的统一schema

无论A或B路线，graph mass/RHS仍是完整同source M6x6、R6；Q为symmetric6x6。
对于所选port coefficients Lt,d0t和cap Dt（A路线不scaled，B路线scaled）：

```
K=[M^TQM-Lt^THLt,                -Lt^THd0t;
   -d0t^THLt,          Dt-R^TQR-d0t^THd0t]   (7x7)
```

H必须是同target的symmetric3x3 metric。当前residual_schur_interface实际取
H=M0CC456INV，即origin regularized M0CC的稠密inverse；不能对角化替换。
可以给rational H entries及M0CC*H=H*M0CC=I的exact检查、M0CC正定证书，
无需运行数值求逆。本轮只识别来源，不声称已有完整H/source/cell证书。

Q仅需对称，K需PSD。Dt包含additive forcing；不能直接用旧RHO2_456*Aup456
homogeneous diagnostic填实际Dt。没有现成Q/Delta/PSD实例被本轮认定有效。

## 4. 最小证书字段与clearing/coverage

| gate | 必填数据与证据 |
|---|---|
| coefficient/source join | M/DM/R/DR digest、CSV/model/controller哈希；Mdirect=CSV M的exact pullback equality；nominal fC/实际target身份 |
| graph | variable_order、G0/G1、同cell total/unique、M可逆与正则性证据 |
| route selection | direct或nominal-subtracted；E_C/E_D、sigma、d_local、v_ref、l_actual与P_actual等式；禁止两route混用 |
| B路线额外 | A/B/B0/C/R_D身份、δ/J coefficients、adjugate identities、δ非零、scaled-port identity |
| metric/cap | H/reference hash、symmetric/PSD/inverse identity；Q对称；Dt及unscaled Delta定义；K exact assembly |
| denominator clearing | rational entries规范num/positive-den；公共positive scale s与Khat=sK identity；变量denominator非零与s>0证据 |
| PSD witness | constant exact LDL/factor或cell matrix-SOS；rational Gram及其exact PSD factor、monomial order、逐entry polynomial identity |
| cell/lift | Ω/time/input law、实际q→c/s、box/circle constraints、真实域包含性；缩域必须证明覆盖真实graph |
| allocation | 同点beta/v_ref/target/lambda、lambda>1、Aalloc≥0；B路线最终用unscaled Delta，不把Delta_s直接交consumer |
| validation | checker/source/schema/log hashes、真实exit码、proof/axiom receipt如适用；缺字段= pending，不是zero |

Q/H等为rational functions时，所有denominator先列出；采用足够偶数幂乘积清分母
可以保证非零处scale正，但仍须证明domain上每个factor非零。s≥0允许零不足以
反推K PSD。不能分别缩放K四个块；congruence-clearing须另给可逆congruence identity。

matrix-SOS可采用Khat=S0+Σg_j Sj+Σh_l Al，g_j≥0、h_l=0，
Sj=Vj^T Gj Vj，Vj=v_j⊗I7、Gj为7Nj阶有理PSD矩阵。
Al对称无需PSD。须exact coefficient equality及rational Gram factor，不能用
浮点eigenvalue、solver flag或采样。它只是充分certificate格式，不承诺固定degree可行。
若域加alpha/Y bound，另证包含实际唯一graph，防止vacuous cap。

## 5. Allocation 与 consumer join

已确认 GenericSchurAllocation20260908.combined_of_port_budget 接受：
lambda>1，sq(r)≤Wcap，(lambda-1)*(base-target-lambda*Wcap)-lambda*sq(ell)≥0。
用统一real linear metric map T使sq(Tu)=u^THu，取：

`ell=T v_ref, r=T d, Wcap=Delta, base=beta`。

同cell allocation必须是
`(lambda-1)*(beta-target-lambda*Delta)-lambda*v_ref^THv_ref≥0`。
由actual target identity才能把结论改写成target≤P_actual。
不存在“cap PSD通过就自动allocation通过”的推论。

如果只有rational H PSD证书但没有T，最小adapter是直接H-quadratic版本，利用：

```
(lambda-1)*(beta-target-qH(v_ref+d))
= Aalloc+qH(v_ref-(lambda-1)*d)
  +lambda*(lambda-1)*(Delta-qH(d)).
```

它只需H symmetric PSD，不要求H square root有理。原consumer支持additive；
这里是metric representation接缝，不是算法不支持。该adapter本轮仅设计未编译。

## 6. 本轮锁定身份与未完成项

- D/routeB_compact_block456_descriptor_structure_audit.jl：
  9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79。
- D/routeB_compact_block456_residual_schur_interface_audit.jl：
  3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98。
- examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean：
  A76375770D563F86F7DE80FDEA970E8D0D0FADD1ED917C262B725C7A8BA47648。

source hash只是身份字段；factorized versus DH-gain的source equality、实际signed
target、同cell A/M可逆、Q/Delta/K证书、allocation/coverage均未被本轮填成已完成。
最小下一步应先选A或B实际port route并交coefficient/source join，再交PSD实例。
pending、registry/formal gate不变。
