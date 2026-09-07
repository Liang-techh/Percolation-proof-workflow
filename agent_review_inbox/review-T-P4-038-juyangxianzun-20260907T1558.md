---
kind: review_result
review_id: review-T-P4-038-juyangxianzun-20260907T1558
task_id: T-P4-038
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-07T15:58:00-06:00
upstream_review: review-T-P4-038-guyuefangyuan-20260907T1521
scope: formalization_only
admission_label: compiled_candidate
integration_status: pending
final_integration: false
---

# T-P4-038 Lean formalization / CI repair result

## 1. Formalized artifact

新增 portable sidecar：

- `examples/routeb_p4_young_feasibility_lean/P4YoungFeasibility.lean`
- `examples/routeb_p4_young_feasibility_lean/README.md`
- `examples/routeb_p4_young_feasibility_lean/verify.sh`
- `examples/routeb_p4_young_feasibility_lean/lean-toolchain`

`lean-toolchain` 固定为 `leanprover/lean4:v4.32.0`；`verify.sh` 从 `PATH` 查找 `lake/lean`，默认复用仓库 `examples/local_fkg` 的 pinned Lake 环境，并包含 `CI_PORTABLE=1`，可由 `.github/workflows/lean-agent-sidecars.yml` 独立执行。

## 2. Kernel-facing theorem decomposition

本轮把古月方源的单标量 sign-robust Young feasibility 拆成 11 个公开 theorem：

1. `young_gap_mul_identity`：精确冻结
   `theta * (D - youngCost theta A P) = (D-A-P)*theta - A*theta^2 - P`。
2. `young_scalar_budget_mul_iff`：在 `theta>0` 下，将带除法的 Young budget 精确等价为 division-free quadratic
   `A*theta^2 - (D-A-P)*theta + P <= 0`。
3. `young_scalar_discriminant_necessary`：若 `A>0, P>=0, theta>0` 且 budget 可行，则
   `D-A-P>0` 且 `4*A*P <= (D-A-P)^2`。
4. `young_theta_gap_identity`：构造 `theta=G/(2A)` 时的精确 reserve
   `(G^2-4*A*P)/(2G)`。
5. `young_scalar_discriminant_constructive`：`A>0, G>0, 4AP<=G^2` 直接构造正 `theta` 并证明 budget。
6. `young_lambda_gap_identity`：历史参数 `lambda=1+2A/G` 的精确同一 reserve identity。
7. `young_scalar_lambda_constructive`：构造 `lambda>1` 并闭合 combined-Schur scalar budget。
8. `young_scalar_strict_margin_constructive`：以 `Gm=D-m-A-P` 冻结 strict-reserve consumer。
9. `young_scalar_strict_extra_reserve`：严格 discriminant `4AP<Gm^2` 推出严格正的剩余 reserve。
10. `rational_example_sharp_vs_theta_one`：精确核验上游例子 `A=1, P=1/100, D=5/4, theta=3/25`，cost=`91/75<5/4`，而 `theta=1` cost=`101/50>5/4`。
11. `obstruction_example_no_theta`：精确核验 `A=P=1,D=3` 不存在任何正 `theta` 满足 budget。

接口收缩：constructive sufficiency 在已经显式给出 `A>0`、`G>0` 和 discriminant gate 后，不再需要冗余的 `P>=0` hypothesis；但 necessity theorem 保留 `P>=0`，因为它用于从任意 feasible row 推出 `G>0`。

## 3. Real GitHub Actions failure -> repair -> pass

首轮真实 Actions：

- run: `34164346834`
- job: `101872318926`
- head: `e1def56e90790c7a640a724d6739976dff6af8ae`

真实日志暴露了本 sidecar 的 Lean 4.32 问题：

- `field_simp [youngCost,...]` 没有展开 `youngCost`，导致两个 gap identity 留下未闭合 polynomial goal；
- 使用了不匹配当前 mathlib API 的 `(mul_le_mul_right htheta2).mp ...`；
- `field_simp ... <;> ring` 触发 `warningAsError` 下的 `linter.unnecessarySeqFocus`；
- 对 `1 < 1 + 2*A/G` 直接使用 `positivity` 报 `not a positivity goal`；
- 因这些错误，下游依赖 theorem 的 `#print axioms` 暂时出现 `sorryAx`。

修复 commit：

- `1265eb36b0c562814baaeec4fe5d49e09b0bad85`

修复内容：

- 在两个 `youngCost` gap identity 中先 `unfold youngCost`，再 `field_simp` / `ring`；
- 改用正乘子下的严格反证取消 `theta^2`，避免依赖变动的 `mul_le_mul_right` iff API；
- 将不必要的 `<;>` 改成顺序 tactic；
- 先证明 `0 < 2*A/G`，再由 `linarith` 得到 `lambda>1`。

修复后的真实 Actions：

- run: `34164675665`
- job: `101873260800`
- head: `1265eb36b0c562814baaeec4fe5d49e09b0bad85`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 日志明确输出：

```text
AXIOM_AUDIT=PASS
P4_YOUNG_FEASIBILITY_FOCUSED_CHECK=PASS
P4_CONCRETE_A_P_D_M_SOURCE_BINDING=OPEN
P4_SHARED_LAMBDA_MULTIROW=OPEN
TRUE_DH_FLOAT64_SEMANTICS=OPEN
P8_DOMAIN_TRAJECTORY_COVERAGE=OPEN
P4_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_young_feasibility_lean/verify.sh
```

11 个公开 theorem 的 `#print axioms` 全部只有
`[propext, Classical.choice, Quot.sound]`，没有 `sorryAx`。

注意：shared workflow 整体 conclusion 仍为 `failure`，但与本 sidecar 无关；同一真实日志中仍有其他独立 lane 的 FLT quotient path、M4 cross-branch、P5 componentwise/parameter-tube/weighted-dual、P7 tail Schur、P8 ramp reconstruction 等失败。本轮未抢占这些 Agent 的 lane。

## 4. Remaining boundary

本轮只证明 source-independent scalar algebra。仍未形式化/未绑定：

- P4 各真实 row/cell 的 concrete `A,P,D,m`；
- `T-P4-039` 的 same-cell common-`theta` / common-`lambda` 多行交集；
- true-DH / Float64 evaluator semantics；
- 同一 P8 domain 的 trajectory / flowpipe coverage；
- source provenance/admission；
- P4/M4 final closure 与 registry mutation。

因此本结果只标记为 `compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
