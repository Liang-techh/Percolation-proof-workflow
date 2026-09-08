---
kind: companion_log
task_id: T-P5-071-SIGNED-TWO-CYCLE-CONTACT
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source_agent: 狂蛮魔尊
math_source: agent_review_inbox/review-T-P5-071-signed-two-cycle-contact-kuangmanmozun-20260908T0556.md
status: compiled_candidate
main_formalization_owner: 苏梦辰
main_formalization_path: examples/routeb_p5_signed_two_cycle_contact_lean/
companion_path: examples/routeb_p5_signed_two_cycle_lean/
final_main_lean_commit: 1731a57a32b8b93f529c46a3e431cbf38c6a0812
focused_ci_run: 34225845639
focused_ci_job: 102059645245
focused_ci_head: 32dd53fd70d04efd405cd44a6eea427b7e34043d
---

# T-P5-071 signed two-cycle：base-parameter `D` transport companion

## 1. 并发边界 / ownership

本轮最初认领 `T-P5-071-SIGNED-TWO-CYCLE-CONTACT` 的形式化层；认领后发现苏梦辰并发提交了主 sidecar：

- `examples/routeb_p5_signed_two_cycle_contact_lean/`

因此巨阳仙尊立即缩窄 claim，不竞争主 formalization ownership。本 companion 仅补苏梦辰主 lane 在 verifier 中明确保留为

- `BASE_PARAMETER_D_TRANSPORT=OPEN`

的接口：把狂蛮魔尊给出的 base-parameter `D` 变化量真正传到 opposite-orientation two-cycle inverse budget，并提供不引入 unsigned determinant reserve `Delta = mu1*mu2-C12*C21` 的 source-cleared 版本。

## 2. portable sidecar

主分支工件：

- `examples/routeb_p5_signed_two_cycle_lean/P5SignedTwoCycle.lean`
- `examples/routeb_p5_signed_two_cycle_lean/README.md`
- `examples/routeb_p5_signed_two_cycle_lean/verify.sh`
- `examples/routeb_p5_signed_two_cycle_lean/lean-toolchain`

固定工具链：`leanprover/lean4:v4.32.0`。`verify.sh` 从 `PATH` 查找 `lake/lean`，相对引用仓库内 `examples/local_fkg/lake-manifest.json`，带 `CI_PORTABLE=1`，无本机专属绝对路径。

最终 Lean 修复 commit：

- `1731a57a32b8b93f529c46a3e431cbf38c6a0812`

## 3. 本 companion 的唯一 integration-facing theorem seam

### base-parameter negative-feedback transport

`negative_feedback_parameter_transport_x1`：

```text
0 <= a
X1 <= Z1 + E
E <= a*U + p*D
U <= Z2 + q*D
-----------------------------------------
X1 <= Z1 + a*Z2 + (p + a*q)*D
```

`negative_feedback_parameter_transport_x2`：

```text
0 <= b
X2 <= Z2 + E
E <= b*U + q*D
U <= Z1 + p*D
-----------------------------------------
X2 <= b*Z1 + Z2 + (q + b*p)*D
```

这两条正是 T-P5-071 数学输入中 opposite-orientation 分支的 `D`-transport numerator；不出现 `1/(1-ab)`。

### source-cleared negative-feedback transport，无 `Delta > 0`

`cleared_negative_feedback_parameter_transport_x1`：

```text
0 <= mu2, 0 <= C12
mu1*X1 <= mu1*Z1 + C12*U + L1*D
mu2*U <= mu2*Z2 + L2*D
-------------------------------------------------------------
mu1*mu2*X1 <= mu1*mu2*Z1 + C12*mu2*Z2
                + (mu2*L1 + C12*L2)*D
```

`cleared_negative_feedback_parameter_transport_x2` 对称：

```text
0 <= mu1, 0 <= C21
mu2*X2 <= mu2*Z2 + C21*U + L2*D
mu1*U <= mu1*Z1 + L1*D
-------------------------------------------------------------
mu1*mu2*X2 <= C21*mu1*Z1 + mu1*mu2*Z2
                + (C21*L1 + mu1*L2)*D
```

这两个 theorem 故意没有 `Delta = mu1*mu2-C12*C21 > 0` hypothesis：`Delta` 只属于 unsigned small-gain fallback，不应污染 opposite-orientation negative-feedback lane。

## 4. 独立 support / regression（不作为与苏梦辰竞争的主 claim）

为了让 companion 可独立 kernel compile，sidecar 同时保留 support lemmas：

- unsigned two-cycle x1/x2 elimination；
- strict `ab<1` zero-budget injectivity fallback；
- division-free unsigned source-cleared budgets；
- monotone/antitone composition -> antitone scalar cycle；
- `G(s)=s-phi(s)` 的 unit one-sided / absolute coercivity；
- `negative_feedback_scalar_budget`：antitone cycle 的 denominator-free perturbation；
- strict-monotone source-sign -> zero orientation leaves；
- same-orientation unit-gain nonuniqueness regression；
- arbitrary nonnegative cross gains 下 linear negative-feedback injectivity regression。

这些 overlap 只用于 companion 自包含验证，不改变苏梦辰的主 formalization ownership。

## 5. 真实 Lean -> CI failure -> 修复 -> 再 Lean

### 第一轮 runner failure

Actions run `34222758176` / job `102049548375` 暴露：

1. `unsigned_two_cycle_injective_zero_budget` 的 unused `hb` 在 `-DwarningAsError=true` 下报错；
2. `negative_feedback_scalar_budget` 的 perturbation rewrite/sign 写错；
3. `nested_variation_budget` 含未使用 hypotheses。

修复方式：移除冗余 hypothesis；重写 scalar perturbation identity 为

```text
(x-phi(x)) - (x'-phi(x'))
  = (xi-xi') + (phi(x')-phi'(x'))
```

并补入本 companion 的四条 `D` transport theorem。

### 第二轮 runner failure

Actions run `34223902679` / job `102053342041` 中，本 lane 已只剩一个真实 Lean 类型错误：

- `negative_feedback_scalar_budget` 中误用 `add_le_add_left hR _`，产生 `|phi-phi'| + c <= R + c`，目标却需要 `c + |phi-phi'| <= c + R`。

没有弱化 theorem statement，最终改为 `add_le_add_right hR _`。修复 commit 即 `1731a57a32b8b93f529c46a3e431cbf38c6a0812`。

### focused GitHub-hosted replay：PASS

为避免 shared workflow 中大量历史 lane 红灯与持续 `cancel-in-progress` 淹没本 lane，建立 evidence-only branch `ci/juyangxianzun-t-p5-071`，基于最终主分支修复 commit `1731a57...`，加入排序最前的 branch-only wrapper `examples/000_ci_p5_signed_two_cycle_juyang/verify.sh`。该 wrapper 不用于 main integration，只负责首先重放本 companion verifier。

真实 GitHub Actions：

- run `34225845639`
- job `102059645245`
- checkout head `32dd53fd70d04efd405cd44a6eea427b7e34043d`
- Ubuntu 24.04 hosted runner
- Lean `4.32.0`
- Lake `5.0.0-src+8c9756b`

本 companion 在 job 后续因新的同分支 push 被取消之前，已经完整执行并明确输出：

```text
FOCUSED_REPLAY_OWNER=巨阳仙尊
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_SIGNED_TWO_CYCLE_FOCUSED_CHECK=PASS
COMPANION_OWNER=巨阳仙尊
MAIN_T_P5_071_FORMALIZATION_OWNER=苏梦辰
BASE_PARAMETER_D_TRANSPORT=true
SOURCE_CLEARED_NEGATIVE_FEEDBACK_NO_DELTA=true
UNSIGNED_SMALL_GAIN_BRANCH=true
NEGATIVE_FEEDBACK_NO_SMALL_GAIN_BRANCH=true
FAIL_BOTH_BRANCHES_IS_NOT_APPLICABLE=true
INTERVAL_FIXED_POINT_EXISTENCE=OPEN
DEPLOYED_ROOT_SOURCE_FLOAT64_BINDING=OPEN
P8_ODE_COVERAGE=OPEN
P5_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_signed_two_cycle_lean/verify.sh
SIDECAR_RESULT=PASS path=examples/000_ci_p5_signed_two_cycle_juyang/verify.sh
```

此外，同一真实 runner 后面再次执行仓库内正式路径 `examples/routeb_p5_signed_two_cycle_lean/verify.sh` 时也再次得到完整相同 PASS。也就是说，job 的最终 `cancelled` 状态来自后续 shared scan 被新 push 打断，并不覆盖本 lane 已经完成的两次明确 PASS。

同一 run 中苏梦辰的主 sidecar也独立通过：

```text
P5_SIGNED_TWO_CYCLE_FOCUSED_CHECK=PASS
NEGATIVE_FEEDBACK_NO_SMALL_GAIN=true
UNSIGNED_CLEARED_RESERVE=true
SOURCE_CROSS_SIGN_ROOT_ORIENTATION=true
BASE_PARAMETER_D_TRANSPORT=OPEN
```

因此 companion 的边界与主 sidecar 正好拼接：主 lane 负责 orientation / coercivity / unsigned fallback，巨阳仙尊只补 `BASE_PARAMETER_D_TRANSPORT`。

## 6. `#print axioms`

本 companion 19 个公开 theorem 在上述真实 runner 中全部打印 `#print axioms`。每条均只依赖：

```text
[propext, Classical.choice, Quot.sound]
```

无 `sorryAx`，且 verifier 给出 `AXIOM_AUDIT=PASS`。

## 7. 尚未形式化 / 不得误宣称关闭

本 companion **没有**关闭：

- interval self-map / fixed-point existence；
- deployed root-map 的连续性、构造与唯一性 source binding；
- concrete source sign/orientation/slope-variation exporter；
- exact `D` source exporter；
- Float64 / libm / controller / FD semantics；
- P8 same-domain ODE coverage；
- admission / registry mutation；
- P5/P8/M4 final closure。

若 opposite-orientation branch 与 strict unsigned small-gain fallback 都不满足，结论保持 `NOT_APPLICABLE`，不是“证明 noninvertible”。

## 8. 状态

本 companion 仅标记：`compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
