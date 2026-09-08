---
kind: review_result
review_id: NEW_REVIEW_P5_EXACT_RATIONAL_PSD_SCHEMA_ADDITIVE_HCAP_20260908
task_id: P5-EXACT-RATIONAL-PSD-SCHEMA-ADDITIVE-HCAP
agent: Sartre
status: CERTIFICATE_SCHEMA_AND_MINIMAL_METRIC_ADAPTER_PENDING_INSTANCE
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
lean_compile_status: not_run
---

# Exact rational PSD schema：graph H-cap → additive allocation

本轮只新增schema/math review。没有制造Q、Delta或alpha/Y数值，没有改任何
consumer/source/state/registry，没有运行Lean、提取器、SDP或回归。
以下是可由真实证书填充并逐字段核验的schema，不是已有可行实例。

## 1. 直接读取的 consumer 与 artifact 边界

已读取 `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean`：

```
combined_of_port_budget (base target lam W : Real) (ell r : Vec n)
  (hlam : 1 < lam) (hport : sq r <= W)
  (halloc : 0 <= (lam-1)*(base-target-lam*W)-lam*sq ell)
  : target <= base-sq(ell+r)
```

cap W是标量，接受additive Delta；没有要求cap与a_B齐次或rho<1。
文件注释为source-independent/open-uncompiled；本轮不覆盖其编译历史。
James additive-port review给出的source decomposition、metric transport、allocation
三项调用者义务与上述原声明一致。

外部 `routeB_compact_block456_residual_schur_interface_audit.jl:17–36` 实际使用
H=M0_CC^-1、C=(4,5,6)，并保持稠密metric。其RHO2_456/BUP456是symbolic diagnostic
的homogeneous port envelope，不是本轮G0实际remote-port的additive Delta witness。
旧 `routeB_compact_bi_m0_metric_ledger.csv` 有eta/resolved_boxes/rho2/theta/lambda/
margin/admissible列，但属另一个block45 port metric账本，不能填block456同cell Delta。
不重新优化或比较这些常数。

## 2. Schema 的基本对象、维度和符号

固定z=(q,v,w)∈R13，物理lift c_i=cos q_i、s_i=sin q_i；alpha∈R6。
graph G0=M alpha-R=0，G1的78行及total/unique/regularity证据沿用前轮contract。
本H-cap不需要Y；若证书引入Y或alpha范围，须另外证明范围覆盖真实graph。

| object | dimension | required exact fields / meaning |
|---|---|---|
| M,R | 6x6, 6 | 同source coefficient IDs；regularized mass与完整DH RHS |
| L,d0 | m x6, m | actual d=L alpha+d0；m=3用于block456，m=2不能静默替代 |
| H | m x m | symmetric PSD实际metric，metric ID；nominal inverse须绑定M0与inverse identity |
| Q | 6x6 | symmetric polynomial/rational-function multiplier；不要求Q PSD |
| Delta | scalar | actual port squared cap的候选表达式，不是其已证明bound |
| K | 7x7 | 按下式构造；维数7来自alpha6+常量1，与m不同 |
| v_ref,beta,target,lambda | m, scalar, scalar, scalar | 同点consumer字段；lambda>1单独证书 |

```
K00=M^T Q M-L^T H L
K01=-L^T H d0
K10=-d0^T H L
K11=Delta-R^T Q R-d0^T H d0
```

Q和H必须对称。两个off-diagonal块符号为负，常数块有两个减项。
不能将d0丢掉、将R替成某个名义remote RHS，或用不匹配metric的norm替代H。
精确identity为：

```
Delta-(L alpha+d0)^T H(L alpha+d0)
 = [alpha;1]^T K[alpha;1] - G0^T Q(M alpha+R).
```

因此同cell K PSD + 实际G0=0给H-cap。Q/K是certificate未知量，不是本轮已找到数据。
这个7x7路线只是充分schema；未能找到某阶Q或K证书，不证明真实graph cap不可能。

## 3. Rational representation 与 clearing-denominator

每个scalar entry用稀疏多项式或分式表示：固定variable_order、monomial exponent
非负整数tuple、规范化整数num/positive den；禁止Float64与未解释decimal。
输入文件的稀疏零约定、重复monomial合并、matrix index_order必须明确。

若所有entry都是有理系数多项式，取统一正整数d清系数分母即可。
若存在随z变化的denominator，字段须给：

- 每个entry的numerator/denominator及nonzero-domain witness；
- 公共polynomial scale s_K(z)，以及Ω上s_K>0的exact witness；
- polynomial matrix Khat 与恒等式 Khat=s_K*K 的交叉相乘核验；
- 对应的source域不穿denominator零点的证据。

可以从所有denominator的适当偶数幂乘积构造正scale，但仍须证明每个factor非零、
幂次足以清掉全部分母。仅“乘平方”不能让零点合法。
s_K>0时Khat PSD才与K PSD等价；s_K>=0而允许零会丢失零点处信息。
negative/unknown-sign scale禁止；不要分别缩放各块破坏统一矩阵关系。
若用正对角congruence清分母，则明确D及D可逆，并核验Khat=D^T K D，不能混同scalar scaling。

allocation另用正scale s_A清分母并记录identity，不能借用未证正的lambda-1。
lambda>1仍作为单独strict gate；lambda=1只可能得到边界式，不能进入此consumer。

## 4. 可核验的 exact PSD certificate 字段

常量有理Khat可交 exact factor/LDL：permutation P、rational L、diagonal D≥0，
并逐entry核验 P*Khat*P^T=L*D*L^T。允许零pivot，但不能仅看非负pivot列表而不验证
完整factor identity。不存在矩阵的数值特征值tolerance或抽样PSD通行证。

随z变化的Khat，需要uniform cell certificate。例如Ω的lifted超集由g_j≥0、h_l=0定义：

```
Khat(z)=S0(z)+sum_j g_j(z)*Sj(z)+sum_l h_l(z)*Al(z)
Sj(z)=Vj(z)^T Gj Vj(z),  Gj rational PSD
```

其中Vj=v_j⊗I7，若v_j有Nj个monomials，则Vj为(7Nj)x7，Gj为(7Nj)x(7Nj)。
Al为对称polynomial矩阵，无PSD要求；所有polynomial matrix identities逐系数核验。
Gj用上述exact factor/LDL或另一已核验PSD证书证明，不接受浮点Gram直接判正。
circle equations属于h_l，box/nonzero guards属于所选域证据。
必须证明真实(q,v,w,lift(q))的cell落入该semialgebraic域；超集positivity足够，
未证明的缩域不足。该quadratic-module形式是可选充分证书，不保证固定degree完备。

实际payload应列：domain constraint IDs、Vj monomial order、Gj bytes/hash与factor、
Al coefficients、identity residual=exact zero的检查证据、clearing scale、source/evaluator
绑定。不能只给“PSD=true”“solver feasible”或“same hash”。

## 5. Consumer allocation 和最小 metric adapter

需要actual source等式 l_actual=v_ref+d，P_actual=beta-l_actual^T H l_actual。
定义q_H(u)=u^T H u和：

`A=(lambda-1)*(beta-target-lambda*Delta)-lambda*q_H(v_ref)`。

同cell需要lambda>1与A≥0，后者可给scalar SOS/interval证书；若A依赖alpha，须在
同一已证明total graph上核验，不能把自由alpha换成假bound。positive target若由
物理目标要求，再另行检查；generic theorem自身并未要求target>0。

现有consumer可直接用的条件是提供真实线性T:R^m→R^n，
q_H(u)=sq(Tu)。n不必等于m，所有baseline/port/total使用同一T。
有理LDL可认证H PSD，但diagonal的平方根未必有理，所以不能把rational LDL
直接当作一个同维rational T。若只给H PSD而没有T，原欧氏声明不能直接统一类型。

最小新增adapter可以完全避免平方根（本轮只给目标，不修改consumer）：

```
weighted_combined_of_port_budget
  (H=H^T) (forall u, q_H(u)>=0)
  (lambda>1) (q_H(d)<=Delta) (A>=0)
  : target <= beta-q_H(v_ref+d)
```

其同源无inverse的精确proof identity是：

```
(lambda-1)*(beta-target-q_H(v_ref+d))
 = A + q_H(v_ref-(lambda-1)*d)
     + lambda*(lambda-1)*(Delta-q_H(d)).
```

只需H对称、PSD、实数顺序；不要求H正定。这样 rational PSD certificate直接消费，
不需要计算H平方根或转换default Pi/sup norm。该adapter仍是待实现/待验证数学目标，
本轮未提供Lean inhabitant。也可沿原consumer加已证明的real T，不是接口no-go。

## 6. Payload source/hash schema（必填，不是有效实例）

每份真实candidate certificate应包含：

```
schema_version, certificate_id, source_semantics_id
jet: extractor_path/hash, six_input_hashes, coefficient_table_hash, variable_order
cell: path/hash, Omega_ref, time_interval, input_law_ref, lift_inclusion_witness
graph: G0/G1_definition_hash, total_unique_witness, invertibility_ref, regularity_ref
port: block_order, actual_residual_identity_ref, L_ref, d0_ref, v_ref_ref
metric: H_ref/hash, nominal_reference_hash, symmetry_ref, PSD_ref, optional_T_ref
cap: Q_coefficients_ref/hash, Q_symmetry_ref, Delta_ref/hash, K_identity_ref
clearing: denominator_refs, nonzero_refs, sK_positive_ref, Khat_ref, identity_ref
PSD: domain_constraints_refs, SOS_Gram/factor_refs, exact_identity_check_ref
allocation: beta/target/lambda_refs, lambda_gt_one_ref, A_ref, positivity_ref
consumer: exact_module_hash, theorem_name, source_target_identity_ref
validation: checker_hash, argv, exit_code, log_hash, scope, independent_audit_ref
admission=pending, registry_promoted=false, formal_certificate_allowed=false
```

如果actual model有Malpha=R+z_defect，graph与cap的R字段必须同步改为真实R+z_defect
并带其hash/语义/域；G1还要Dz_defect。不能使用零defect版K证书通过非零defect graph。
定义packet时缺失字段可以null标出pending；校验阶段不可把null当zero/identity。
receipt自身用最终bytes的detached hash，不制造自引用self-hash。

## 7. 现有artifact不能填的字段与明确结论

当前读到的block456 H有真实nominal metric来源，但只是symbolic interface中的定义；
尚未给与本轮full-state cell/actual port绑定的H证书。Delta的homogeneous diagnostic
与旧block45 metric ledger不能提供本schema的actual additive cap。没有找到实际Q、
Khat/SOS Gram、clearing域证书或same-cell allocation实例。

因此最短路线是先固定真实L/d0/H/source target，再交Q/Delta+K证书及allocation。
consumer不需要重写为homogeneous形式；缺T时用上述直接H adapter即可。
这不是“consumer算法不支持additive”，也不是已证明当前source可满足PSD schema。

本轮重算的文件SHA：

- GenericSchurAllocation20260908.lean：
  A76375770D563F86F7DE80FDEA970E8D0D0FADD1ED917C262B725C7A8BA47648。
- 外部routeB_compact_block456_residual_schur_interface_audit.jl：
  3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98。
- 外部routeB_compact_bi_m0_metric_ledger.csv：
  23058051FC66A39EF91ADA952CAD210A716480AF5BA3EC04B5BD3DDCA0BF2E0F。

哈希只固定读取身份，非编译/语义证据。保持pending；无registry/formal gate变更。
