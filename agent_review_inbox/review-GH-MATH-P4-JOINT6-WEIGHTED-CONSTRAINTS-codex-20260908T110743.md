---
kind: review_result
review_id: review-GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS-codex-20260908T110743
task_id: GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS
source_agent: codex-actual-weighted-consumption-audit
created_at: 2026-09-08T11:07:43-06:00
integration_status: pending
admission_label: pending
proof_status: CONDITIONAL_WEIGHTED_RECOVERY_ACTUAL_INPUT_MISSING
actual_y_bound: false
actual_weighted_constraints_supplied: false
physical_rows_recovered: false
lean_compile_status: not_run
registry_eligible: false
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: supply one actual y=Xz with model/solve/measurement defects and same-domain signed values; propagate those values once into principal RHS and matching numerator/metric
---

# Weighted constraints 消费审查：actual y 尚未供应

## 1. 结论与本轮证据范围

signed weighted constraints **可以条件性消费同一个 actual y=Xz** 并恢复 physical
rows4/5；但当前 runtime-refinement artifact 仍是 receipt schema，明确记录
runtime_capture_found=false、analytic_refinement_proven=false。因此本轮没有可实例化的
actual y、weighted 值或对应 physical row packet。

仅消费/核对本 lane 既有 weighted 数学、最新 joint6/actual-numerator review 及 runtime
schema；不重新扫描外部 artifacts，也不将前轮 bounded search 扩大成全仓库不存在结论。
只新增本 review；不需要 sidecar，不重复 rank 或泛型 Young，不执行 Lean/Julia/回归。

## 2. 必须统一的三层 residual

对同一配置、full-state x 与 actual ahat：

```text
e_solve=M_R ahat-F_R,
e_model=(M_A-M_R)ahat+(F_R-F_A),
z_A=e_solve+e_model,
y_A=Xz_A=y_solve+y_model.
```

weighted input 应是 y_A，而不是只包含 solve error 的 y_solve，也不是物理 lift 的
同名坐标 y1/y2/y3。相同维度不提供相同 residual。
若有实际 y_solve 的零值，只能消掉该部分，仍需保留 y_model；analytic/FD/controller、
regularizer、G0、assembly 差异均不能隐含置零。

若测量存储为 yhat=y_A+xi，则真正恢复必须减去 xi 的对应 dual 组合。
corrected-builder omission 若已经在表达式层修正，不再重复计入；若仍消费旧表达式，
须先补回已知 signed omission，才能讨论这里的 actual measurement mismatch。

## 3. Exact weighted 恢复与 joint6 的保留

沿用前轮同一 rational X 的精确系数，不做新 rank/inverse 算术。令 C=P_B X^-1，
其两行支持对应

```text
w4=alpha*y_A1+gamma*y_A6,
w5=eta*y_A1+theta*y_A2+iota*y_A3, eta<0,
z_A,4=beta*y_A4+w4,
z_A,5=kappa*y_A5+w5.
```

若 source 给 y_A,B=b+db、w=c+dw，则 D=diag(beta,kappa) 给

```text
z_A,B=e0+de,   e0=D b+c,   de=D db+dw.                 (W)
```

零 constraints 需要实际证明四个输入为零，非零 offset/defect 必须原样保留。
若 yhat 有误差且 what 由同一 yhat 构造，则 `(W)` 的恢复值还需减 `C xi`。
不能用独立来源的 y_A4 与 yhat6 拼接；X_actual 与系数绑定的 X 不同时亦需 mismatch correction。

y_A6 是混合的 preconditioned row6，不等于物理 z_A6；lift 的 eta_acc,3 只是
在 actual lift 身份成立时等于 ahat6。两条 weighted constraints 既不证明 z_A6=0，
也不消去 actual ahat6。

physical principal rows 随后是

```text
S=(M_A)_BB, u=ahat_B,
f0=F_A,B-(M_A)_BE ahat_E-(M_A)_B6 ahat6+e0,
S u=f0+de,   E=(1,2,3), B=(4,5).                     (P)
```

joint6/远端 solve/model defects 已经通过 z_A→y_A→(W) 进入 de/e0，
而实际 acceleration coupling 留在 f0；它们是不同作用，不得删掉 coupling，也不得
再把已经计入的同一 defect 追加一次。principal 路线不需要假设 row6 为零或作 Schur 消元。

## 4. Metric 与 numerator 的同源消费边界

令 eta_m=(db4,db5,dw4,dw5)，J=[D,I]，无 measurement mismatch 时 de=J eta_m。
若同域 joint error budget 为 eta_m^T Sigma^-1 eta_m<=B_m，Sigma SPD，
则 G=J Sigma J^T 给 de^T G^-1 de<=B_m。若含 -Cxi，则须将 xi 及相关性一起
放入扩大 measurement vector/map 或另证有效组合预算，不能仍用原四维 cap。
目标 H 不同需独立 comparison；nominal port cap 不自动控制这里的 de。

同一固定 observable covector nu 下，packet 使用

```text
D2=det(S),
N=nu^T adj(S)*(f0+de),
D2*(nu^T u)=N.
```

令 b_obs=adj(S)^T nu，则 signed error contribution 是
`b_obs1*(beta*db4+dw4)+b_obs2*(kappa*db5+dw5)`，有 mismatch 时再减 b_obs^T Cxi。
eta 的负号、controller/refinement 项与 actual joint6 coupling 必须在整个 N 中保留。
可用同源 metric 推 `|b_obs^T de|²<=(b_obs^T G b_obs)B_m`，但不凭此产生
det(S)>0 或 frozen observable/导数身份。

不允许将 det(X)、origin mass determinant、其他块的 Schur determinant 与这个 N 配对。
若 fixed nu 被改变成 state-dependent projection，原 observable 二阶导数绑定不能原样沿用。

## 5. 当前可交付与缺失项

| 层 | 可交付 | 尚缺 |
|---|---|---|
| dual algebra | 已有同 rational X 的精确 weighted recovery | actual loaded X/valuation 同一性 |
| actual measurements | (W) 的带 offset/defect 接口 | y_A 与 w4/w5 的同源实际值或 certified bounds |
| joint6/远端 | (P) 明确保留 coupling、full defect | actual ahat 与 solve/model refinement |
| metric | J/Sigma 的条件运输 | 同域 joint error enclosure 与目标 metric comparison |
| numerator/det | 完整 signed N 公式 | 选定 S 的正下界、同域 N 上界及 rational gate |
| observable | nu^T u 的代数对象 | 同单位 physical observable 与 acceleration derivative 身份 |

最小下一步是供应 actual runtime/refinement packet，或明确改选并证明 ideal-model 方程。
仅编写 weighted constraints 定义、给 correction spec 或重复 generic theorem 不填这些字段。
当前仍是 pending / missing-actual-input；不作物理反例或 source admission。

## 6. 本轮输入 anchors

下列文件均位于 agent_review_inbox，SHA 仅固定消费版本，不是编译/执行证据：

- `review-GH-MATH-P4-JOINT6-WEIGHTED-CONSTRAINTS-LOCAL-codex-20260908T102742.md`：
  `792c6cc3839a82afc4f12ecf0d63e137567e4b464cd1b0762ae15c3696f22e42`。
- `review-GH-MATH-P4-JOINT6-DEFECT-ELIMINATION-codex-20260908T110434.md`：
  `a276d3247bac7c8833fc238b1b90c238f8f2ae7ef0c3e2b7e0b881a28af97a6a`。
- `review-GH-MATH-P4-VANIS2-RUNTIME-REFINEMENT-codex-20260908T110215.md`：
  `ddf425345cc97a58ba1ae5f5fa24cabfd0b7f72f64dcb7353d27216f77841286`。

本轮无 VERIFIED、Lean/Julia 执行、source/registry promotion；未修改任何旧文件。
