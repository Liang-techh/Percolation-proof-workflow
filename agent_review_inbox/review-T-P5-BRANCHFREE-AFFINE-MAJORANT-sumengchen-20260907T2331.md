---
kind: review_result
task_id: T-P5-BRANCHFREE-AFFINE-MAJORANT
agent: 苏梦辰
source_agent: 苏梦辰
math_source_agent: 柳冠一
inspected_math_commit: 0af72cfaa1a9fbaa31d47cda05f152fb5579ce32
sidecar_fix_commit: 3bd5802cce6ced38aba8a37a215567ffada6d352
integration_status: compiled_candidate
admission_label: pending
registry_mutation: false
final_integration: false
---

# T-P5-BRANCHFREE-AFFINE-MAJORANT — Lean review result

苏梦辰本轮按柳冠一已经完成的数学推导做最小 theorem decomposition，没有重新做大规模数学探索。新增独立 portable sidecar：

- `examples/routeb_p5_branchfree_affine_majorant_lean/P5BranchFreeAffineMajorant.lean`
- `examples/routeb_p5_branchfree_affine_majorant_lean/README.md`
- `examples/routeb_p5_branchfree_affine_majorant_lean/verify.sh`
- `examples/routeb_p5_branchfree_affine_majorant_lean/lean-toolchain`

`verify.sh` 使用 `CI_PORTABLE=1`，从 `PATH` 查找 `lake` / `lean`，默认借用仓库 `examples/local_fkg` 的 pinned Lake 环境，检查 `lake-manifest.json` 与 toolchain 一致性，不硬编码本机绝对路径。

## 1. Formal statement / typed interface

在同一 signed coordinate convention 下定义

```text
Q(x,y) = p*x^2 + sigma*x*y + s*y^2,
d(x,y) = b4*x + b5*y,
D4      = 4*p*s - sigma^2,
B2      = b4^2 + b5^2,
Nsig    = s*b4^2 - sigma*b4*b5 + p*b5^2.
```

主 forward theorem：对固定 `kappa > 0`，若同一 `(p,s,sigma,b4,b5)` 上同时有

```text
B2   <= 4*kappa*(p+s),
Nsig <= kappa*D4,
```

则对任意 `x,y : ℝ`，Lean 核化

```text
-Q(x,y) - d(x,y) <= kappa.
```

实现刻意保持 division-free / inverse-free / sqrt-free / eigenvalue-free，也不按 `det(H)` 做 PD/PSD 分支。

为避免 source/checker 把不同 cell/key 的界错误拼接，还提供 `source_family_affine_energy_le`：两个 remainder certificate 必须在同一 typed `z`、同一 domain predicate `D z`、同一 signed `sigma` convention 上消费。

## 2. Exported theorem decomposition

当前导出并做 `#print axioms` 的 11 个 theorem：

1. `sym2_scaled_qf_completion_identity`
2. `sym2_scaled_qf_nonneg_of_trace_det4`
3. `majorant_trace_identity`
4. `majorant_det4_identity`
5. `affine_majorant_scaled_identity`
6. `affine_energy_le_of_two_invariant_gates`
7. `affine_energy_le_of_nonnegative_remainders`
8. `affine_energy_lt_of_two_invariant_gates`
9. `source_family_affine_energy_le`
10. `degenerate_family_joint_gates`
11. `degenerate_family_affine_bound`

其中核心 exact identities 为

```text
4*a*(a*x^2 + m*x*y + c*y^2)
 = (2*a*x + m*y)^2 + (4*a*c-m^2)*y^2,
```

以及

```text
4*(4*kappa*p-b4^2)*(4*kappa*s-b5^2)
 - (4*kappa*sigma-2*b4*b5)^2
 = 16*kappa*(kappa*D4-Nsig),
```

和 branch-free affine completion

```text
4*kappa*(Q+d+kappa)
 = Gkappa_quadratic(x,y) + (d+2*kappa)^2.
```

因此二维 PSD consumer 只需 scaled trace + scaled determinant 非负即可推出全局 affine-energy budget。

## 3. Near-singular regression

同时核化柳冠一给出的 exact family

```text
p=t^2, s=1, sigma=0, b4=2*t, b5=0, kappa=1.
```

Lean 证明两条 joint gate 对任意 `t : ℝ` 都成立，并直接推出

```text
-quad (t^2) 1 0 x y - bias (2*t) 0 x y <= 1
```

对所有 `x,y` 成立，包含 `t=0` singular endpoint。该 regression 保留了数学层强调的接口边界：`D4` 与 `Nsig` 应作为相关量/同 key remainder 处理；不能默认把它们各自做互不相关的最坏区间后再相减。

## 4. Real Actions: math → Lean → CI → fix → Lean

### First run: real blocker

初始 sidecar 在真实 GitHub Actions

- run `34189982906`
- job `101945896639`
- head `2122d3a8d0ba2e5bcbe8d549abc47e5243f1e8b0`

上暴露 Lean 4.32 normalization blocker。`sym2_scaled_qf_nonneg_of_trace_det4` 的 `a=0,m=0` 分支中，证明项

```text
mul_nonneg hc (sq_nonneg y)
```

类型为 `0 <= c*y^2`，而目标仍打印为

```text
0 <= 0*x^2 + 0*x*y + c*y^2.
```

因此第一轮该 theorem 及其 downstream consumers 暂时出现 transitive `sorryAx`。这是 proof normalization 问题，不是数学 statement 或常数问题。

### Fix

commit

`3bd5802cce6ced38aba8a37a215567ffada6d352`

仅把该 branch 改为

```lean
simpa using (mul_nonneg hc (sq_nonneg y))
```

没有改变 theorem statement、hypotheses、常数或数学接口。

### Second run: focused PASS

真实 Actions：

- run `34190535718`
- job `101947506956`
- head `3bd5802cce6ced38aba8a37a215567ffada6d352`
- Lean `4.32.0`
- Lake `5.0.0`

本 sidecar 明确输出：

```text
AXIOM_AUDIT=PASS
P5_BRANCHFREE_AFFINE_MAJORANT_FOCUSED_CHECK=PASS
BRANCH_FREE_TWO_GATE_FORWARD_CONSUMER=true
SIGNED_SIGMA_SAME_KEY_REQUIRED=true
JOINT_RTRACE_RDET_ENCLOSURE_REQUIRED=true
OPTIONAL_GLOBAL_IFF_CONVERSE=OPEN
SOURCE_FLOAT64_BINDING=OPEN
P8_ODE_COVERAGE=OPEN
P5_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_branchfree_affine_majorant_lean/verify.sh
```

11 个 exported theorem 的 `#print axioms` 均仅为

```text
[propext, Classical.choice, Quot.sound]
```

当前本 sidecar **无 `sorryAx`**。

聚合 `portable-sidecars` job 仍为 failure，但真实日志显示与本任务无关；本轮未抢占这些旧工件。该 run 中仍失败的包括 FLT quotient 路径、M4 cross-branch、旧 P5 componentwise/direct-two-channel/parameter-tube/weighted-dual-residual、P7 tail-Schur 和旧 P8 ramp-reconstruction 等。

## 5. Dependencies / remaining formalization boundary

依赖：`Mathlib` + 仓库 pinned `examples/local_fkg/lake-manifest.json` / Lean 4.32.0；数学输入来自柳冠一 `T-P5-BRANCHFREE-AFFINE-MAJORANT` review/companion。

尚未形式化/绑定：

- 数学 review 中的完整 global `iff` converse（当前 forward checker 已闭合；若 downstream classifier 真正需要 iff，可另拆最小 child）；
- source/Float64 对 `R_trace = 4*kappa*(p+s)-B2` 与 `R_det = kappa*D4-Nsig` 的同 cell / 同 key / 同 signed-sigma correlated enclosure；
- true-DH、controller、FD、solve remainder 的 execution semantics；
- P8 ODE continuation / same-domain trajectory / flowpipe coverage；
- registry/admission/final parent-state mutation。

本结果只记为 `compiled_candidate`，不修改 P5/M4 总体结论，不自行做 integration/admission。

**待封不觉独立验证 / 待梁智炜最终整合。**
