---
kind: review_result
review_id: review-GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE-codex-20260908T1100
task_id: GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE
source_agent: codex-half-active-invocation-semantics-lane
created_at: 2026-09-08
integration_status: pending
admission_label: pending
proof_status: INVOCATION_EVIDENCE_NOT_SAME_CONFIGURATION_ACTUAL_PACKET
source_binding_proven: false
actual_valuation_supplied: false
runtime_defect_refinement_supplied: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: bind the actual invocation values and full-domain runtime refinement to the vanis2 chart; do not substitute a mu-zero finite-sample log or Monte Carlo bracket for the actual semantic packet
---

# Half-active vanis2：runtime invocation 的新核对与最小 semantic obstruction

## 1. 本轮新增发现

在已知 corrected-chart/actual-row 缺口之外，本轮找到并审阅了已有 runtime 调用线索：
`verify_dynamics_semantics.jl`、其 CSV/report/短日志，以及使用默认 exact_ddq 的
`debug_11_gains.jl`。**没有找到可直接消费的同一 vanis2 configuration/domain 的
actual valuation + defect refinement packet。**

最关键的区别：semantics verifier 中唯一计算并报告 acceleration 的 exact_ddq 调用
显式使用 `mass_regularization=0.0`，不是 vanis2 analytic chart 的 1/1000000。
记录的结果只是该 strict 调用的 finite flag 和最大绝对分量，不是完整 solve receipt。
default/explicit 的另外几项检查是 mass/C/G 比较，不是 regularized acceleration 行方程。

本轮不重复 controller omission 算术或 rank，不运行任何脚本/Julia/Lean/Lake/回归。
只读定位、查看现有日志及做一个精确 token 域归属检查；只新增本 review。
禁止目标之外的 source/payload/旧 review/state/registry 均未修改。

## 2. 固定本任务的 semantic key

采用已有 half_active_vanis2_domain_probe.json，SHA
`28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`。
域记录为完整六维 angle radii
`(9/20,19/50,37/100,19/50,37/100,9/20)`、所有 |dq_i|<=3、|w|<=2。
initial radius=3/20、step=1/512 是其 analytic first-slab 记录，不作为本轮 trajectory 认证。

同源 packet 至少需同时固定

```text
(Omega, coordinate/time units, actual input valuation,
 controller gains and G0 semantics, mu, FD step,
 analytic M/C/G chart, reference mass, X,
 runtime source/dependencies/configuration, returned acceleration).
```

current dhport 默认 mu=1e-6、FD step=1e-5，M/C/G 为 Float64 DH/central-difference 计算；
corrected DH chart 是同一完整 signed controller 规范的 analytic 表达式候选。
十进制 gains 的实数 rational chart 与运行中的二进制常数/乘除仍需 refinement。
source 文件 hash 也不独自绑定 include 后全局参数的实际值、调用 kwargs 或运行环境。

## 3. 已有 invocation artifacts 的可消费边界

### A. verify_dynamics_semantics

源码固定测试点
`q=(.21,-.13,.08,.31,-.27,.17)`、
`dq=(.12,-.05,.07,-.16,.11,-.09)`、w=.4。
精确十进制 token 检查确认这个点处在记录的 vanis2 box 内；
这只是点的包含，不认证 box 覆盖或调用结果。

源码依次比较 default/explicit regularized mass 和 default/explicit C/G，
另算 strict unregularized mass eigenvalue，最后调用

```julia
ddq_strict = exact_ddq(q, dq, w; mass_regularization = 0.0,
                     fd_step = CG_FINITE_DIFF_STEP)
```

现有 CSV 记录 default mass/C/G 差为 0、regularizer delta 约 1e-6、strict minimum
eigenvalue 约 0.01413、strict acceleration max abs 约 2.46255，均 pass=true；
短日志仅 `DYNAMICS_SEMANTICS_OK`。report 自己也限定为单点 sanity check。

这些记录没有返回值六个分量、同次 assembled M/RHS、精确 residual、actual lift、Xy
或 weighted constraints。没有 authentication 信息证明当前源码与历史运行逐字一致。
即使把历史 run 按其描述接受，它也不是目标 mu 的 actual solve packet。

对不同 mu 的调用，不能因为 regularizer 很小就静默沿用 ahat。
若要运输一个相同 ahat 的 source equation，至少保留
`(M_target-M_strict)ahat` 与 forcing 的相应差项；若两次调用返回不同加速度，
还需实际 returned-value/equation 绑定。有限性或 sample eigenvalue 不提供这些界。

### B. debug_11_gains 默认调用

这个脚本确实 include dhport 并在 validate_bracket 中调用默认 `exact_ddq(q,dq,w)`。
但它在 eta=2.7/5.6 的随机 weighted state ball、|w|<=sqrt(3) 下测量/验证 bracket，
不是 vanis2 全状态域的认证遍历。源码中的辅助 f 还含 mgl 与 kc 耦合的 storage/reference
表达式，不能把它无说明地改名为 corrected DH physical forcing。
它打印 aggregate violation/ratio，不输出本任务的 actual balance/solve receipt。
本轮只读代码，不运行、不移植其域或 empirical gains。

### C. vanis2 的 analytic downstream references

定向搜索找到 builders 对该 domain 的引用，以及 dynamic_descriptor_l2_chain.py
将 vanis2 与已有 endpoint/bound records 组成 analytic descriptor chain。
这说明 analytic payload 在后续被使用，不构成 runtime acceleration valuation。
该脚本检查/组合 analytic contraction/descriptor quantities，没有在所读部分调用
dhport exact_ddq 或认证 Float64 solve residual。未执行或验证整条 chain。

## 4. 最小实际语义 refinement

令 ahat 为目标运行返回的 acceleration，M_R/F_R 为同次调用的实际 assembled values
按实数解码，M_A/F_A 为选定 corrected analytic chart。需要

```text
e_solve=M_R ahat-F_R,
z_A=M_A ahat-F_A
   =e_solve+(M_A-M_R)ahat+(F_R-F_A),
y=Xz_A.                                               (R)
```

这些是 exact conditional identities；定义 e_solve 不等于证明其为零或给出 enclosure。
F_R 必须明确是实际存储 RHS，还是带 assembly error 的另一个表达式，不能混用。
FD/G0、decoded controller constants、mass regularization、rounding/solve 差异均需保留。

一个可消费的 pointwise packet 应至少给同次 input/config、M_R/F_R/ahat 的 bit-level
身份、非有限值检查、exact-dyadic residual 或可靠外包、source/model refinement 与 hashes。
若要覆盖整个 Omega，则还需统一算法误差/模型差异界或有覆盖证明的局部 receipts。
一个在 Omega 内的成功样本不满足这个全域量词。
本轮不要求/执行额外 runtime invocation，也不伪造上述 fields。

## 5. Corrected chart、physical lift 与 joint6 必须共用 (R)

消费前轮已核对的 physical acceleration bridge：它只给 raw_from_lift 的有理变换。
设 lift 为 eta_acc，centered map 为 A_lin，则 actual 接线应是

```text
ahat=T_lift eta_acc,
delta_a=ahat-A_lin chi,
E_ctr=X[M_A(A_lin chi+delta_a)-F_A]=y.
```

只有实际 valuation 身份成立才可使用最后等式；corrected expression 本身不证明 y=0。
若 substitution 有误差 r_sub，必须加 `X M_A r_sub`。
physical bridge 第六行只表示 ahat6=eta_acc,3（在 actual 代入成立时），不代表 ahat6=0。

joint6 的实际 defect 是
`z_A,6=e_solve,6+(M_A-M_R)6,*ahat+(F_R-F_A)6`；
preconditioned row6 是 `y6=sum_j X6j*z_A,j`，二者不同。
weighted constraints w4/w5 必须由这个同一个 y 构造，不从 nominal port 或不完整旧 payload
抽取同名项。即使 y456 已有值，缺失 weighted 源方向仍需真正的值/界，不能由行数产生。

最终物理 principal rows 应保留

```text
(M_A)_BB ahat_B=F_A,B+z_A,B-(M_A)_BE ahat_E-(M_A)_B6 ahat6.
```

不得把选择 vanis2 angle box 当作对 acceleration/defect 的约束。
corrected source expression、actual solve、metric、det/numerator 与 observable 必须共享
同一 semantic key；旧 nominal H-budget 与新的 runtime residual 不能仅按维数拼接。

## 6. 最小 conditional obstruction 与下一项可收割证据

当前可以固定一个 analytic domain、X、corrected controller 规格和 symbolic lift。
但现有 invocation 记录没有把该 domain/chart 与同次 returned acceleration/solve defect
连接起来；其 strict sample 又使用不同 mu。故 actual z_A、y456、w4/w5 的值/统一界
均未由这些 artifacts 决定。

最小缺失包不是再一份 controller/rank/Schur 推导，而是：

1. **Invocation identity**：同一 runtime target/config、实际输入和返回值；
2. **Refinement**：同一 (R) 的有效 solve/model defect，含 joint6 及远端项；
3. **Valuation/domain**：实际 acceleration/lift、X 与 Omega 的共同绑定；
4. **Consumption**：physical rows 或 signed weighted measurements 的实际值/界，
   之后才是 metric、完整 signed numerator/determinant 与 observable 的同域 packet。

若改选 ideal analytic model，可独立证明其方程并只声明该模型结果；
不能将这种模型选择悄悄当成 runtime actual refinement。
本结论是有限检查范围内的 missing-witness obstruction，不是物理反例或不可实现性定理。
pending，无 VERIFIED、source admission、registry/trajectory closure。

## 7. 检查边界

本轮直接读取现有脚本、report、CSV、短日志，计算 SHA，并用 Fraction 检查测试点 token
在 box 内；没有重放任何 runtime/producer 或读取日志为 formal receipt。
外部文件和既有 review/state/registry 均未写入；只新增本指定前缀 review_result。
