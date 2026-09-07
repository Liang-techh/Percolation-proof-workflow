---
kind: review_result
review_id: review-T-P5-032-juyangxianzun-20260907T1306
task_id: T-P5-032
source_agent: 巨阳仙尊
agent: 巨阳仙尊
created_at: 2026-09-07T13:06:00-06:00
status: compiled_candidate
admission_label: compiled_candidate
claim: agent_review_inbox/claim-T-P5-032-juyangxianzun-20260907T1255.md
math_input:
  - agent_review_inbox/review-T-P5-032-honglianmozun-20260907T1253.md
sidecar: examples/routeb_p5_eight_ninths_coercivity_lean/
lean_source_blob: ab345720f96cf55d573a82d780af21dfa14af34b
verify_blob: fc71ed40b43ffb7890c6aafdb222cd4533ac2e55
toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
ci_head: 8f69f4a7dd6bacb42d501405b8f8966b8e048f87
ci_run: 34153791079
ci_job: 101841342031
---

# T-P5-032：exact `8/9` hypocoercive coercivity 的 Lean 子闭环

本轮只形式化红莲魔尊 `review-T-P5-032-honglianmozun-20260907T1253.md` 中 **source-independent** 的数学层，不重新探索大规模数学，不接管 source gain table、Float64/solve 语义、P8 coverage、ODE first-exit/continuation、provenance/admission、registry 或最终整合。

## 1. 新增 portable sidecar

路径：

- `examples/routeb_p5_eight_ninths_coercivity_lean/P5EightNinthsCoercivity.lean`
- `examples/routeb_p5_eight_ninths_coercivity_lean/README.md`
- `examples/routeb_p5_eight_ninths_coercivity_lean/verify.sh`
- `examples/routeb_p5_eight_ninths_coercivity_lean/lean-toolchain`

`lean-toolchain` 固定 `leanprover/lean4:v4.32.0`。`verify.sh` 带 `CI_PORTABLE=1`，从 `PATH` 查找 `lake/lean`，复用仓库 sibling `examples/local_fkg` 的 pinned Lake manifest/toolchain，并以 `-DwarningAsError=true` focused compile；没有硬编码任何本机专属路径。

## 2. theorem decomposition

本 sidecar 将 T-P5-032 数学输入压成 14 个公开 theorem：

1. `nine_square_gap_identity`
   - 冻结当前 block-(4,5) 的 exact `eps=1` storage `V` 与 dissipation `Q`；
   - kernel 逐项证明
     `Q-(8/9)V` 等于 9 个正有理系数平方项之和。

2. `nine_square_coefficients_positive`
   - 对 9-square certificate 中出现的 8 个不同 rational coefficient 做 exact positivity sanity check。

3. `q_ge_eight_ninths_storage`
   - 主 coercivity consumer：
     `8/9 * V <= Q`。

4. `improved_iss_refinement`
   - 输入不变的 half-`Q` residual absorption：
     `Vdot <= -(1/2)Q + (17/10)R2`；
   - 联合新 coercivity 输出：
     `Vdot <= -(4/9)V + (17/10)R2`。

5. `ultimate_gain_constant`
   - exact arithmetic：`(17/10)/(4/9)=153/40`。

6. `decay_improvement_factor`
   - exact comparison：
     `(4/9)/(457/1344)=1792/1371 > 1`。

7. `improved_barrier_inward`
   - generic division-free gate：
     `153*L2 < 40*Vstar`
     配合新的 derivative bound 推出 `Vdot<0`。

8. `quarter_barrier_inward`
   - `Vstar=1/4` specialization：`153*L2<10`。

9. `initial_coefficient_lt_one_twelfth`
   - kernel 冻结 T-P5-030 的 exact initial coefficient：
     `474733828336525417 / 5726342542105201000 < 1/12`。

10. `parameter_tube_boundary_inward`
    - generic first-exit arithmetic seam：
      `153*nu < (40-153*mu)*Kc`
      加上 boundary derivative premise 推出 `Vdot<0`。
    - **Lean 显式要求 `0 < dc^2`。** 这是 typed interface 中应保留的真实边界：若 parameter-cell diameter `dc=0`，把 strict gate 乘上 `dc^2` 后不能推出严格 inwardness；zero-diameter 情形必须单独退化处理，不能偷偷从该 theorem 消费。

11. `one_twelfth_parameter_tube_gate`
    - 对 `Kc=1/12`：
      `153*mu + 1836*nu < 40`
      推出 generic gate。

12. `physical_slack_to_one_twelfth_gate`
    - 对 T-P5-031 的 `mu=U+p`, `nu=W+q` 直接给出下游 typed gate：
      `153*(U+p)+1836*(W+q)<40`。

13. `slack_feasibility_necessity`
    - 若 `p,q>=0`、`U*W<=p*q` 且 `153p+1836q<R`，则必须
      `R>0` 且 `1123632*U*W<R^2`；
    - 只作为 fail-closed **necessity diagnostic**，没有把它误写成 sufficiency。

14. `exact_feasibility_factor`
    - integer kernel check：`4*153*1836=1123632`。

## 3. exact storage / dissipation 接口

Lean 中直接冻结：

- `m4=350003/3000000`
- `m5=200739/4000000`
- `d4=4/5`
- `d5=13/20`
- `k44=3/4`
- `k55=29/50`
- `k45=-3/400`。

`vStorage` 对应当前 `eps=1` hypocoercive storage；`qDissipation` 对应
`yᵀ(D-M)y + xᵀKx - yᵀAx`，并显式保留 skew coupling
`+(1/400)x4*y5 -(1/400)x5*y4`。

九平方恒等式被直接作为 polynomial equality 由 `simp` + `ring` 核验；主 coercivity 再仅消费平方非负性，不依赖矩阵求逆、特征值、平方根或数值 eigensolver。

## 4. GitHub Actions / focused compile

最终 head：

`8f69f4a7dd6bacb42d501405b8f8966b8e048f87`

真实 GitHub Actions：

- run: `34153791079`
- job: `101841342031`
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 的真实日志明确输出：

```text
AXIOM_AUDIT=PASS
P5_EIGHT_NINTHS_COERCIVITY_FOCUSED_CHECK=PASS
SOURCE_RESIDUAL_GAIN_TABLE=OPEN
SOURCE_FLOAT64_INCREMENTAL_SEMANTICS=OPEN
P8_SAME_DOMAIN_COVERAGE=OPEN
ODE_FIRST_EXIT_CONTINUATION=OPEN
P5_P8_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_eight_ninths_coercivity_lean/verify.sh
```

本 sidecar 在最终 CI head 上没有 Lean 类型错误、linter error 或 `sorryAx`。在正式运行前我将 `q_ge_eight_ninths_storage` 的证明接口收窄为显式 `have hid := nine_square_gap_identity ...` + `positivity` + `linarith`，避免依赖对全局 context 的脆弱 rewrite；最终 real Actions 直接通过。

shared workflow 整体仍为 failure，但真实日志确认**不是本 sidecar 导致**。同一 run 中仍有若干其他独立 lane 报错，例如：

- `anthropic_flt_quotient_transport_sidecar` 的错误 `../local_fkg` 相对路径；
- `routeb_m4_cross_branch_budget_lean` 的 noncomputable/unused-hypothesis 问题；
- `routeb_p5_componentwise_relative_decay_lean` 的 finite-sum/rewrite 问题；
- `routeb_p5_parameter_tube_gain_lean` 的 `AddLeftMono` metavariable、rewrite/linter 与 `sorryAx`；
- `routeb_p5_weighted_dual_residual_lean` 的 unused `hκ1` / disjunction projection / `sorryAx`；
- `routeb_p7_tail_schur_completion_lean` 与 `routeb_p8_ramp_reconstruction_sidecar` 的各自 Lean 错误。

这些均属其他 lane，本轮没有越权抢占。

## 5. `#print axioms`

14 个公开 theorem 均完成 axiom report：

- 实数代数 theorem：`[propext, Classical.choice, Quot.sound]`
- `exact_feasibility_factor`：`[propext]`
- 本 sidecar 无 `sorryAx`。

## 6. 对 downstream 的可核升级

本 sidecar 已经把旧的 `Q -> V` Euclidean detour 替换为 direct coercivity：

```text
Q >= (8/9)V
```

因此在不改变 `17/10` residual consumer 的情况下，可把 downstream energy ledger 统一升级为：

```text
Vdot <= -(4/9)V + (17/10)R2.
```

对应 checker-facing gate：

```text
one-trajectory generic:  153 L2 < 40 Vstar
quarter barrier:          153 L2 < 10
Kc=1/12 parameter tube:   153 mu + 1836 nu < 40
T-P5-031 downstream:      153(U+p) + 1836(W+q) < 40
```

所以 T-P5-031 的 physical-gain → `mu/nu` bridge 本身不需要重写，只需由梁智炜（Codex）决定是否在最终 DAG 中把其旧 `11424/137088/2285` consumer 替换为该 stronger gate。

## 7. 仍未形式化 / 应退回 source 与 ODE 层

本轮没有提供且不能由当前纯代数 sidecar 替代的 premise：

- 同一 P8/first-exit domain 上真实的 block-(4,5) source residual / physical incremental gain table；
- Julia/DH/Float64/controller/solve 的 centered incremental semantics 与 enclosure；
- `R2` 或 T-P5-031 `U/W` 数值界的 source binding；
- P8 same-domain coverage；
- initial-state/source-state semantic binding；
- ODE existence、first-exit 与 continuation；
- P5/P8/M4 的最终组合、registry/admission 与整体结论。

`parameter_tube_boundary_inward` 还明确暴露了一个需要 downstream 正确分支处理的 typed boundary：**strict tube argument仅在 `dc^2>0` 时直接消费；`dc=0` 必须单独处理。**

## 8. 状态边界

当前仅为 `compiled_candidate`。本 review 不宣称 registry admission、P5 closure、P8 closure、M4 closure 或最终整合。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
