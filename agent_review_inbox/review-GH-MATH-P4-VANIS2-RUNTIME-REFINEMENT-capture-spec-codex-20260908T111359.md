---
kind: review_result
review_id: review-GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT-capture-spec-codex-20260908T111359
task_id: GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT
source_agent: codex-single-call-capture-spec
created_at: 2026-09-08T11:13:59-06:00
integration_status: pending
admission_label: pending
proof_status: ISOLATED_CAPTURE_SPEC_NOT_EXECUTED
runtime_executed: false
receipt_generated: false
actual_source_rows_supplied: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
requested_action: implement and review a new isolated instrumented-call harness only under separate execution scope; preserve exact source order and capture one backslash result, then check dyadic algebra and analytic refinement separately
---

# Vanis2 single-call capture：隔离实现规格，不是 receipt

## 1. 固定输入身份

- `dhport_lib.jl` SHA-256：
  `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`。
- `half_active_vanis2_domain_probe.json` SHA-256：
  `28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e`。
- X：从这个 domain 的 `preconditioner` 按精确 rational 解析；禁止另用 mass inverse。
  receipt 必须包含完整 rational X 或可解析的该 hash-bound 文件；额外 X hash 采用明确
  编码规则，例如逐行 num/positive-den 字符串的 canonical JSON，不靠未定义 serializer。
- 设计 mu=1/1000000、h=1/100000。实际 binary64 目标 bit pattern 分别为
  `3eb0c6f7a0b5ed8d`、`3ee4f8b588e368f1`；本轮只用标准库编码核对这些常数。
  设计分数与 decoded dyadic 的差异保留给 refinement，不能声明实数完全相等。

当前未指定可认证的 actual invocation/input receipt；不把旧 mu=0 sanity 样本挑作结果。
域信息不是一组完整的运行输入，也不是 runtime trajectory containment。

## 2. 唯一 solve 的 capture boundary

现有 exact_ddq 只返回 acceleration，不暴露实际 M/RHS；先调用它再重算 M/RHS 会违反
同次捕获要求。禁止通过第二次 arm_MCG 调用伪装第一次 solve 的输入。

最短未来实现是在新隔离目录中放置 versioned instrumented function，逐句保持目标
exact_ddq 的原控制流/求值顺序、相同 arm_MCG 和 effective globals；旧文件不改。
instrumented-vs-original 的 equivalence 属于需要审查的源映射，不由命名保证。
该 harness 不是“未修改原 exact_ddq 的运行 receipt”，必须如实标识为 instrumented invocation。

概念顺序如下（伪码；本轮不生成可执行脚本、不运行）：

```text
load pinned source into an isolated namespace
freeze/hash effective globals, runtime/dependency configuration
decode supplied input bits q,dq,w; check finite and point in Omega
mu=bits(3eb0c6f7a0b5ed8d); h=bits(3ee4f8b588e368f1)
M,Cdq,Gq = arm_MCG(q,dq; mass_regularization=mu,fd_step=h)
_,_,G0   = arm_MCG(zeros(6),zeros(6); same explicit knobs)
tau      = ORIGINAL exact_ddq tau expression, unchanged broadcast/order
F        = ORIGINAL parenthesized RHS expression tau-Cdq-Gq
snapshot input M,F and source intermediates without modifying them
ahat     = M backslash F             # exactly one solve
snapshot ahat; snapshot/hash effective configuration after call
serialize raw bits + provenance only after capture
```

原点 arm_MCG 是原调用本身的 G0 步骤，不是额外重算 solve 输入。
禁止为了记录方便换成 inverse(M)*F、修改 broadcast、预先 fuse 表达式或更换 solve API。
快照必须在任何可能原地改写前完成；不要将记录的副本误换为另一条待求解路径。
在无同进程外部参数修改的隔离运行中冻结 global arrays；before/after hash 仅作检查，
不能独自证明期间没有瞬时变动。源文件、依赖与 capture implementation 都要单独 pin。

## 3. 字段级最小 receipt

这张表是实现规格，当前值缺失的字段不能填占位 PASS。

| 字段 | 内容与要求 |
|---|---|
| schema/scope | `vanis2.same_call.v1` / `pointwise_instrumented_capture` |
| call identity | 唯一 call_id、UTC、实际命令、退出码、capture/source/dependency hashes |
| runtime | Julia、平台/架构、BLAS/LAPACK、线程/rounding 等实际环境；有效 globals manifest |
| domain/config | 上述 domain/X/source pins、mu/h 的设计 tokens 与 actual bits、单位/coordinate order |
| input | q_bits[6]、dq_bits[6]、w_bits；实际 decoded 点的 Omega membership |
| solve input | M_R_bits[6][6]、F_R_bits[6]，同一次 solve 前的 snapshot |
| source intermediates | tau_bits[6]、Cdq_bits[6]、Gq_bits[6]、G0_bits[6]，同次调用来源 |
| returned output | ahat_bits[6]，该唯一 backslash 的返回值 |
| provenance | log/raw-capture SHA、before/after source/config checks、instrumentation mapping review |

所有 binary64 用固定 16 位 hex bit patterns，矩阵明确按 i 行 j 列编码（Julia 一基语义，
serialized 数组逐行）；不是原内存 column-major 字节流的未说明拼接。
拒绝 NaN/Inf/缺字段/shape 错误。原始 signed zero bits 保留，exact algebra 中其值为零。

## 4. 最短可执行 checker 与输出分级

独立 checker 只需 standard-library bit decoding 与 exact rationals，无 Lean/Julia 需求：

1. 核对 pins、shape、finite、配置 bits、point membership 和同次 provenance。
2. 将 M_R/F_R/ahat 解码为 exact dyadic，逐分量计算
   `e_solve=M_R*ahat-F_R`，输出六个 reduced fractions。
3. 用同一个 rational X 计算 `y_solve=X*e_solve`，输出六分量以及显式 rows456 selection。
4. 可按同 X 的已给 signed covectors输出 w_solve4/w_solve5；标识只属于 solve residual。
5. 核对/保存 assembly discrepancy `F_R-(tau-Cdq-Gq)` 的 exact dyadic 值。
   不要求该差为零，不以第二次浮点评价替代第一次 assembled RHS。

输出状态最多为 `decoded_pointwise_solve_algebra_checked`。这表示捕获数据之间的
精确算术核对，不表示原运行可信、solve exact、physical rows zero 或 source admission。
同次 provenance 和 instrumented-source 对应必须独立通过；自洽 JSON 可被伪造，
因此纯算术不是运行真实性证据。

## 5. 从 y_solve 到真正 y=Xz：不能省掉 refinement

选定 corrected analytic chart 后实际需要的是

```text
z_A=e_solve+(M_A-M_R)*ahat+(F_R-F_A),
y_A=X*z_A.
```

若没有同输入的 M_A/F_A valid enclosure 或 exact source identities，checker 必须输出
`analytic_refinement=pending; y_A_rows456=unavailable`，不能把 y_solve 改名为 y_A。
FD/G0、mu、controller decoding、assembly 与 mass/model terms 分开定位但只计入一次。

refinement attachment 可提供同 decoded input 的 rational interval matrices/vectors、
其 source/evaluator/proof hashes和正确性证据；独立 interval 计算才能生成 z_A/y_A bounds。
两条 actual weighted constraints必须消费 y_A，保留其 signed correlation 与 error。

physical lift attachment 另给 T_lift 与其 reference hash、eta_acc、A_lin/delta_a 身份，
验证 ahat=T_lift*eta_acc 和 ahat=A_lin*chi+delta_a，或保留残差 r_sub。
lift 的 ahat6=eta_acc,3 不表示 joint6 defect 为零。principal RHS 仍保留
`-M_A,BE*ahat_E-M_A,B6*ahat6`；physical z_A6 与 preconditioned y_A6 不同。

## 6. 当前 blocker / 最短 handoff

| blocker | 当前状态 | 最短解除动作（未执行） |
|---|---|---|
| actual input/call | 没有本任务同次 capture | 提供/授权确定输入的 isolated instrumented run |
| original function 返回内部量不足 | 只返回 ahat | 新 harness 捕获原运算路径内部值；先审查 instrumentation mapping |
| full M_R/F_R/ahat bits | 缺失 | 单次 solve 前后 snapshot；禁止事后重算补齐 |
| decoded residual | 无数据可检查 | 对 capture 做 exact-dyadic checker |
| y_A rows456 | solve residual 不够 | 同输入 analytic/model refinement attachment |
| physical lift | 只有 nominal transform | actual valuation 或明确 substitution defect |
| 全 Omega | 单点 run 本来不足 | 独立 uniform refinement/有覆盖证明的 cell 证据，不做样本升级 |

当前授权写入范围只有新 review/隔离 specification；本轮未创建或执行 capture harness，
也没有可消费的历史同次 tuple。这里是执行/证据边界，不声称机器不能运行 Julia。
mu=0 sanity 的输入 configuration 错误且只保存 aggregate finite 信息，不能填入本 schema。

最短交接：实现并审查新的同次 capture -> 指定点执行并保存 bits -> 独立 dyadic 核对
-> 再交 analytic/lift refinement；按实际完成层级标记，不伪造 receipt。
本轮只创建此 review，state/registry/旧 artifacts/其他 agent 文件未修改；无 VERIFIED。
