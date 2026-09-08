---
kind: review_result
review_id: review-T-P4-041-strict-boundary-lean-juyangxianzun-20260907T1752
task_id: T-P4-041-STRICT-COMMON-LAMBDA-BOUNDARY-LEAN
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-07T17:52:00-06:00
source_review: review-T-P4-041-strict-common-lambda-boundary-kuangmanmozun-20260907T1742
parent_task: T-P4-041-STRICT-COMMON-LAMBDA-BOUNDARY
integration_status: compiled_candidate
admission_label: pending
inspected_math_commit: 4e644acd61eaa79841dcabc9ef8890e36ba8aecd
lean_head_sha: 321a68cae4cba7d3fb8e1fff8ed163cf59b630aa
lean_run_id: 34171049476
lean_job_id: 101891269760
lean_toolchain: leanprover/lean4:v4.32.0
lake_version: 5.0.0-src+8c9756b
sidecar_path: examples/routeb_p4_strict_lambda_boundary_lean/
---

# T-P4-041 — strict common-lambda boundary Lean result

## 1. Scope actually formalized

巨阳仙尊消费狂蛮魔尊的 `T-P4-041` 数学 review，仅形式化 source-independent / checker-facing 的 strict-vs-weak boundary algebra 与精确有理反例，不重做大规模数学探索，也不触碰 source/provenance/admission/final integration。

新增 portable sidecar：

```text
examples/routeb_p4_strict_lambda_boundary_lean/
  P4StrictLambdaBoundary.lean
  lean-toolchain
  verify.sh
  README.md
```

`verify.sh` 带 `CI_PORTABLE=1`，从 `PATH` 查找 `lake/lean`，复用仓库内 `examples/local_fkg` pinned Lake 环境，并显式检查 sidecar toolchain 与 Lake root toolchain 一致；未硬编码本机专属路径。

## 2. Kernel-facing definitions

定义三个平方根自由 predicate：

```text
weakPair C U V :=
  C <= U+V OR (C-U-V)^2 <= 4UV

strictPair C U V :=
  C < U+V OR (C-U-V)^2 < 4UV

boundaryPair C U V :=
  U+V <= C AND (C-U-V)^2 = 4UV
```

在 `U,V >= 0` 下，Lean 已证明 exact fail-closed seam：

```text
weakPair C U V ∧ ¬ strictPair C U V
  <-> boundaryPair C U V.
```

因此 downstream 若需要正 reserve、非零 rounding interval 或 source widening tolerance，不能把 weak equality PASS 当成 strict PASS。

## 3. Public theorem set

本 sidecar 共有 15 个公开 theorem：

```text
strictPair_implies_weakPair
boundaryPair_implies_weakPair
boundaryPair_not_strict
weak_not_strict_iff_boundary

touching_pair_is_boundary
touching_pair_weak_not_strict

touching_rows_common_weak_forces_two
touching_rows_at_two
touching_rows_no_positive_common_reserve

perturb_gap_identity
positive_perturbation_strict
zero_perturbation_boundary
negative_perturbation_not_weak
perturbation_discriminant_identity
positive_tenth_exact_reserve
```

其中精确 touching example 已 kernel 化：两行

```text
q1(t)=t^2-3t+2,
q2(t)=t^2-5t+6
```

若同时弱可行，则 Lean 直接推出唯一共同 witness `t=2`；并证明两行在 `t=2` 都恰好等于 0，所以不存在任何 `m>0` 的共同正 reserve。

对应 pair data `(C,U,V)=(4,1,1)` 被证明满足 `boundaryPair`，因此 weak PASS 而 strict FAIL。

## 4. Rational perturbation phase transition

定义

```text
C(e)=(2-e)^2,
U=1,
V(e)=(1+e)^2.
```

Lean 精确证明

```text
4 U V(e) - (C(e)-U-V(e))^2 = 32 e (1-e).
```

由此形式化了三个区间：

```text
0 < e < 1  -> strictPair
    e = 0  -> boundaryPair
    e < 0  -> ¬ weakPair
```

同时冻结 review 中的 rational interior witness：`e=1/10, t=39/20` 时

```text
q1(39/20) = -19/400,
q2_(1/10)(39/20) = -21/400.
```

因此 strict overlap 一侧确实存在正 reserve，而该 reserve 在触碰边界 `e -> 0+` 时归零。

## 5. GitHub Actions / focused compile

真实 GitHub-hosted runner：

```text
workflow: Lean agent sidecars
run_id:   34171049476
job_id:   101891269760
head_sha: 321a68cae4cba7d3fb8e1fff8ed163cf59b630aa
Lean:     4.32.0
Lake:     5.0.0-src+8c9756b
```

本 sidecar 的真实日志明确输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_STRICT_LAMBDA_BOUNDARY_FOCUSED_CHECK=PASS
FINITE_FAMILY_OPEN_INTERVAL_HELLY=OPEN
CONCRETE_P4_SOURCE_FLOAT64_BINDING=OPEN
P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN
P4_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_strict_lambda_boundary_lean/verify.sh
```

15 个 theorem 的 `#print axioms` 全部只有：

```text
[propext, Classical.choice, Quot.sound]
```

本 sidecar 没有 `sorryAx`。

## 6. Shared workflow red status is unrelated

整个 `portable-sidecars` job 仍为 `failure`，但本 lane 自身已经 PASS。真实日志显示红灯来自其他既有独立 lane，包括：

- `anthropic_flt_quotient_transport_sidecar` 的旧 `../local_fkg` 路径；
- `routeb_m4_cross_branch_budget_lean` 的 noncomputable / unused hypothesis；
- P4 weighted-three-term 旧 syntax / sorry / missing root toolchain；
- P5 componentwise / parameter-tube / weighted-dual residual 的既有 Lean 错误；
- P7 tail Schur 的 nonneg/absorption 证明缺口；
- P8 ramp reconstruction 的 interval-integral import/API 缺口。

本轮没有越权修改或抢占这些 lane。

## 7. Intentionally still open

本轮没有宣称完成以下层：

```text
finite-family open-interval Helly/max-lower-min-upper theorem,
finite strict family <-> uniform positive reserve 的 Finset min' 层,
sqrt/root-based interval equivalence（checker 不需要，暂未形式化），
actual P4 cell-family C/U/V 或 A/P/G coefficient binding,
true-DH / Float64 realized-lambda containment,
P8 same-domain trajectory coverage,
P4/M4 closure,
registry/admission/final integration.
```

因此最小可靠结论是：`T-P4-041` 的 **pairwise strict/weak/boundary checker algebra + exact boundary counterexample + rational perturbation transition** 已成为 compiled candidate；finite-family strict-common-witness 聚合层与 source/physical 层继续开放。

**状态：compiled_candidate。待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
