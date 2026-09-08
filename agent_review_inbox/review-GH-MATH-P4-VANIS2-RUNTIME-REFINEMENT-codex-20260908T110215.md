---
kind: review_result
review_id: review-GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT-codex-20260908T110215
task_id: GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT
source_agent: codex-vanis2-runtime-receipt-lane
created_at: 2026-09-08T11:02:15-06:00
handoff_revision: 804
handoff_revision_source: coordinator_message_not_state_read
integration_status: pending
admission_label: pending
proof_status: MISSING_SAME_CALL_CAPTURE_WITH_EXECUTABLE_RECEIPT_SPEC
runtime_capture_found: false
runtime_capture_executed: false
analytic_refinement_proven: false
physical_rows_recovered: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: authorize a separate same-call instrumented capture at explicit target knobs and check exact decoded algebra; require analytic/lift and full-domain refinement separately
---

# Vanis2 runtime refinement：最短可执行 receipt 规格

## 结果

接收 coordinator revision 804，不读取 state。定向搜索既有 robot_formal_v1 与
routeB_dense_Mq 的 receipt/invocation/runtime-refinement/decoded/solve-residual 文件名，
以及 interval_bounds JSON 的 M_R/F_R/e_solve/bit-capture 字段，没有找到目标同次调用 packet。
这是有限范围缺失结果，不是全机器不存在证明。本轮未运行任何 source、Lean/Lake 或回归。

当前仍缺明确 `mu=1e-6, h=1e-5` 的同次 M_R/F_R/ahat、decoded residual、physical lift
与 X-projected actual rows456。以下只给未来捕获/检查规格，不创建脚本或伪造 receipt。

## 1. 固定身份与配置

域文件 half_active_vanis2_domain_probe.json 当前 SHA：
`28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`。
dhport_lib.jl 当前 SHA：
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`。
候选 X 必须取同一个域文件中的完整 rational matrix，不由运行 mass inverse 临时替换。

配置需同时保留设计实数 token `1/1000000`、`1/100000` 与实际传入的 binary64 bits。
两种表示不完全相等；checker 应验证实际 bits 等于约定的正确 binary64 转换，
而不是错误要求 decoded dyadic 等于设计分数。差异归入 model/runtime refinement。
调用应显式传 kwargs，不只依赖默认值；effective gains、G0、全局参数和代码环境也须冻结。

## 2. 最小 core JSON schema（占位类型，不是实际 receipt）

```text
schema: "vanis2.same_call.v1"
scope: "pointwise_runtime_capture"
run:
  id, utc, command, exit_code, julia_version, platform, blas_lapack_identity
  source_bundle_sha256, capture_code_sha256, dependency_lock_sha256
  environment_and_effective_globals_manifest_sha256
domain:
  file_sha256, preconditioner_X_rational_sha256
config:
  mu_design: "1/1000000"
  h_design: "1/100000"
  mu_bits, h_bits
  effective_config_sha256
input:
  q_bits[6], dq_bits[6], w_bits
call:
  call_id
  M_R_bits[6][6]
  tau_bits[6], Cdq_bits[6], Gq_bits[6], G0_bits[6]
  F_R_bits[6]
  ahat_bits[6]
provenance:
  capture_log_sha256, raw_capture_sha256
```

每个 bits 值使用固定 16 位 hexadecimal 的 IEEE754 binary64 bit-pattern，不是
`show`/JSON decimal rounding。F_R 是真正送进 backslash 的 assembled RHS。
36+6+6 个 M_R/F_R/ahat 数已经足够核对 decoded solve algebra；tau/C/G/G0 是
把该 solve 与本任务 controller/FD invocation 连接所需的最小额外源中间量。
不要求通过输出某个总体 norm 反推缺失向量。

这些值必须在**同一次目标函数执行、同一次 solve** 前后捕获；不能先调用 exact_ddq，
再另跑 arm_MCG 拼一份 M_R/F_R。当库可能原地修改数据时记录 solve 输入快照。
capture 的代码/运行 provenance 仍需审查；JSON 数学自洽本身不能证明没有人工拼接。
本轮不修改现有 exact_ddq；任何 instrumented wrapper/new source capture 需另行授权，
并说明与原调用的 control flow/求值顺序一致性。

## 3. 不运行 Lean 的最短 deterministic checker 步骤

1. 拒绝缺字段、错误 shape、非有限 bits、错误 source/config/domain/X 身份；
   用 exact decoded input 检查单点属于记录的 Omega，不以打印小数替代实际 bits。
2. binary64 解码为精确 dyadic rational。对正常数用
   `(-1)^s*(2^52+fraction)*2^(exponent-1023-52)`；subnormal 用
   `(-1)^s*fraction*2^(-1074)`；零保留 raw bits 身份但代数值为零。
3. 精确有理求
   `e_solve[i]=sum_j M_R[i,j]*ahat[j]-F_R[i]`，保存六个 reduced fractions。
   不用 binary64 residual 再求 norm，也不默认 e_solve=0。
4. 从 hash-bound domain 读取 X，精确计算完整 `y_solve=X*e_solve`，导出 rows4/5/6
   与相同 X 的两条 signed weighted combinations；保留负号。
5. 输出 input/outputs/driver hashes、每项检查结果与完整日志。缺失源身份 -> pending；
   已提供但矛盾的 capture -> reject；通过仅标记 decoded_pointwise_algebra_checked。

F_R 的实际浮点组装可以另以严格相同 rounding/operation-order 的模拟核对；
不能要求 exact rational `F_R=tau-Cdq-Gq`，因为减法舍入一般使它不成立。
若不模拟，保留精确 assembly discrepancy `F_R-(tau-Cdq-Gq)` 并作为语义项处理。
这些 core 检查不认证 FD/model、区间包络、整个 Omega 或 physical rows 为零。

## 4. Actual analytic rows 与 physical lift 的最小附加模块

核心 receipt 只给 e_solve。要得到 corrected analytic chart 的实际残差，必须另有

```text
z_A = e_solve+(M_A-M_R)ahat+(F_R-F_A),
y_A = X z_A.
```

可执行的点态 refinement attachment 至少包括：analytic chart/source/config hashes、
针对同一 decoded q/dq/w 的 M_A/F_A 有理 interval enclosures、生成与独立检查证据。
用 exact ahat/dyadic values 做 interval arithmetic，即可导出 z_A 与 y_A456 enclosure。
包络包含性本身需要可信 evaluator/数学证明；写两个端点不成为 enclosure 证据。
G0、mu、FD、gain decoding、组装与求解差异必须在同一 convention 下完整计入。

由 y_A 而非 y_solve 构造
`w4=alpha*y_A1+gamma*y_A6`、
`w5=eta*y_A1+theta*y_A2+iota*y_A3`，再恢复 physical rows4/5。
仅 y_solve 的 weighted constraints 不控制 analytic z_A，除非 model terms 已证明为零。

physical lift attachment 至少给 T_lift/reference hash、同次 eta_acc 的 exact rational
值或认证 enclosure，以及 `ahat=T_lift*eta_acc` 的实际检查结果。
若只有近似等式，输出 r_lift；centered delta_a 同理给 A_lin/hash 和
`r_sub=ahat-(A_lin*chi+delta_a)`，保留 X M_A r_sub。
通过定义 lift/delta_a 可以建立代数身份，不会自动认证其旧 bounds 或动态方程。

joint6 必须保留物理 z_A6、actual ahat6 和预条件 y_A6 的区别；
principal RHS 仍是 `F_A,B+z_A,B-M_A,BE*ahat_E-M_A,B6*ahat6`。
receipt 不自动产生 det/numerator/metric/observable packet；任何后续消费者必须绑定同一对象。

## 5. 旧证据不兼容的精确理由

| 旧对象 | 不能替代本 schema 的原因 |
|---|---|
| semantics sanity CSV/log | 唯一 reported acceleration 来自显式 mu=0；只有最大分量/finite flag，没有同次 M_R/F_R/ahat bits 或 residual |
| default/explicit match | 比较 mass/C/G，不提供目标 regularized solve 的实际行方程；单点比较也不覆盖 Omega |
| Monte Carlo default exact_ddq | 输入域/聚合输出不是 vanis2 full-state receipt，无逐调用 capture/refinement |
| physical acceleration bridge | nominal rational coordinate/energy transform，没有实际 returned acceleration 的 valuation |
| centered corrected chart | expression/substitution 规格不证明实际取零，也不提供 solve/model defect |
| vanis2 analytic intervals | 前提是 analytic 方程；runtime actual 多出 Xz_A，不能用原 radius 消除其来源 |

本轮重新核对旧 sanity CSV SHA 为
`838eba3367e76e9c05528d72577a2624279045cec7bf045af02738a2fd67779f`；没有重跑 sanity。
测试点即使在 Omega 内，也不能修复 mu/config 不匹配与缺失的完整捕获。

## 6. 最短 handoff 与量词边界

下一步最短可执行工作是：另行授权 isolated same-call capture -> exact-dyadic core checker
-> 同输入 analytic enclosure/refinement -> physical lift/row recovery attachments。
本轮只交规格，不执行上述步骤，不生成 source artifact。

一份 pointwise receipt 至多覆盖一个 decoded input。要声称所有 x∈Omega 的 refinement，
需要独立全域算法误差界或带覆盖证明的域 partition；不把有限样本视为 universal witness。
这也是本轮最小 conditional obstruction：现有证据既缺 core capture，又缺全域 refinement。

pending / no actual witness；无 VERIFIED、source admission、state/registry 写入或旧 artifact 改动。
