---
kind: review_result
task_id: T-P4-036.2
review_id: review-T-P4-036.2-juyangxianzun-20260907T1458
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source_agent: 古月方源
status: compiled_candidate
created_at: 2026-09-07T14:58:00-06:00
math_review: agent_review_inbox/review-T-P4-036.2-guyuefangyuan-robust-phase-cells-20260907T1434.md
sidecar: examples/routeb_p4_robust_phase_cells_lean/
final_code_commit: debe2356d31b2751d735f967fefbae80ee387ffa
ci_run_id: 34161058928
ci_job_id: 101862832446
ci_toolchain: leanprover/lean4:v4.32.0
---

# T-P4-036.2 — robust all-12 phase cells Lean sidecar

本轮只消费古月方源新提交的 `T-P4-036.2` robust phase-cell 数学推导；没有重新做大规模数学探索，也没有处理 Float64/libm/source execution、receipt/provenance/admission、coverage 或最终 integration。

## 落地工件

新增 portable sidecar：

- `examples/routeb_p4_robust_phase_cells_lean/P4RobustPhaseCells.lean`
- `examples/routeb_p4_robust_phase_cells_lean/README.md`
- `examples/routeb_p4_robust_phase_cells_lean/verify.sh`
- `examples/routeb_p4_robust_phase_cells_lean/lean-toolchain`

`verify.sh` 从 `PATH` 解析 `lake/lean`，固定 Lean `v4.32.0`，复用仓库 `examples/local_fkg/lake-manifest.json` 并检查 mathlib revision `81a5d257c8e410db227a6665ed08f64fea08e997`，包含 `CI_PORTABLE=1`，由 `.github/workflows/lean-agent-sidecars.yml` 真实执行。

## Lean theorem decomposition

公开 theorem 共 12 个：

1. `base_trig_cell_of_abs_le`
   - hypotheses: `0 ≤ b`, `|r| ≤ b`
   - conclusion: `-b ≤ sin r ≤ b` 且 `1-b^2/2 ≤ cos r ≤ 1`。
2. `formed_angle_error_to_reduced_radius`
   - `|xhat-(q+center)|≤eps`、`|q|≤a` 推出 `|xhat-center|≤a+eps`。
3. `phase_neg_quarter_cell`
4. `phase_zero_cell`
5. `phase_pos_quarter_cell`
6. `quarter_phase_cell`
   - 用 finite typed phase `QuarterPhase = neg | zero | pos` 统一 `-π/2,0,+π/2` 三类，而不是引入当前 source 不需要的 generic integer range reduction。
7. `theta_cos_lower_constant`
   - exact rational identity `1-(3/20)^2/2 = 791/800`。
8. `theta_all6_exact_cells_from_qbox`
   - 从 `∀i, |q i|≤3/20` 与冻结的 theta phase table `(0,-1,+1,0,0,0)` 一次性得到全部 6 个 exact-real theta cell。
9. `alpha_all6_exact_cells`
   - 从冻结的 alpha phase table `(-1,0,+1,-1,+1,0)` 得到全部 6 个 exact-real alpha cell。
10. `robust_phase_cell_of_formed_angle_error`
    - 上游 formed-angle absolute error 只把 reduced radius 从 `a` 扩大到 `a+eps`。
11. `robust_theta_cell_of_formed_angle_error`
12. `robust_alpha_cell_of_formed_angle_error`

另外冻结了 typed source-facing definitions：`QuarterPhase`、`phaseShift`、`phaseAngle`、四个 phase-cell endpoint function、`phaseTheta`、`phaseAlpha`。

## 真实 Lean → CI → 修复 → 再 Lean 闭环

首次 Actions run `34160647204` / job `101861684083` 暴露了本 sidecar 的两个真实问题：

- `base_trig_cell_of_abs_le` 中 `hb : 0 ≤ b` 在最初证明脚本没有显式使用，`-DwarningAsError=true` 将 unused-variable linter 提升为错误；
- pinned Lean/mathlib 中三角不等式 theorem 名为 `abs_add_le`，最初误写成不存在的 `abs_add`，导致 `formed_angle_error_to_reduced_radius` 及其 robust consumers 带入 `sorryAx`。

修复 commit `debe2356d31b2751d735f967fefbae80ee387ffa`：

- 用 `(sq_le_sq₀ (abs_nonneg r) hb).2 hr` 显式消费 `hb` 并形成平方界；
- 改用 `abs_add_le`。

随后 GitHub-hosted runner 在 Actions run `34161058928` / job `101862832446`、Lean `4.32.0` / Lake `5.0.0` 上对本 sidecar 明确输出：

```text
AXIOM_AUDIT=PASS
P4_ROBUST_PHASE_CELLS_FOCUSED_CHECK=PASS
ANGLE_FORMATION_FLOAT64_BINDING=OPEN
LIBM_OUTPUT_INCLUSION=OPEN
D1_D2_D3_PROPAGATION=OPEN
P8_COVERAGE=OPEN
REGISTRY_MUTATION=false
FINAL_INTEGRATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_robust_phase_cells_lean/verify.sh
```

全部 12 个公开 theorem 的 `#print axioms` 均为：

```text
[propext, Classical.choice, Quot.sound]
```

本 sidecar 无 `sorryAx`。

## shared workflow 状态边界

run `34161058928` 的 shared `portable-sidecars` job 整体仍为 failure，但本 sidecar focused lane 已独立 PASS。该 run 中剩余失败来自其他已有独立 lane，例如：

- `anthropic_flt_quotient_transport_sidecar` 的 `../local_fkg` 路径；
- `routeb_m4_cross_branch_budget_lean` 的 noncomputable/unused hypothesis；
- `routeb_p5_componentwise_relative_decay_lean` 的 abs-square / finite-sum proof；
- `routeb_p5_parameter_tube_gain_lean` 的 typeclass/linter/unsolved goal；
- `routeb_p5_weighted_dual_residual_lean` 的 unused `hκ1` / disjunction projection；
- `routeb_p7_tail_schur_completion_lean` 的 nonneg/linarith；
- `routeb_p8_ramp_reconstruction_sidecar` 的 interval-integral/import/API 问题。

这些不是本轮认领范围，本轮未越权修改。

## 尚未形式化 / 精确退回 source 层

本 sidecar现在只证明 exact-real trig consumer。要把 `T-P4-036.2` 接入真实 Route-B checker，仍需 source/physical 层提供：

- Julia/Float64 中 `q + phase` 或等价 formed-angle 的逐分量 real decoding 与 absolute formation error `eps_i`；
- `sin/cos` libm 输出相对 exact-real `Real.sin/Real.cos` 的 enclosure，包含 non-finite/overflow/rounding fail-closed 语义；
- 由 robust trig cells 到 D1/D2/D3 的 outward propagation；
- 同一 P8/目标 domain 的 source coverage / flowpipe binding。

因此当前结果只标为 **`compiled_candidate`**，不得据此宣称 Route-B/P4 最终闭合。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
