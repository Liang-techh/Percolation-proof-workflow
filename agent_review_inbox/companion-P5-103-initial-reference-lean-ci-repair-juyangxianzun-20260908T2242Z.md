---
kind: companion_log
task_id: P5-103-INITIAL-REFERENCE-LEAN
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-08T22:42:00Z
status: CI_REPAIR_PUSHED_RECHECK_RUNNING
integration_status: pending
registry_mutation: false
---

# P5-103 initial-reference Lean — real CI blocker and repair

本轮优先处理上一轮 `examples/routeb_p5_initial_reference_bridge_lean/` 的真实 GitHub Actions 失败，不做新的大规模数学探索。

## 真实失败证据

上一轮 sidecar head：

- commit: `db591c3215895a6d6b6b2a733eb3e46dd90f5b52`
- Actions run: `34282284703`
- job: `102249648557` (`portable-sidecars`)
- pinned runner: Lean `4.32.0`, Lake `5.0.0`, repository pinned `examples/local_fkg/lake-manifest.json`

`P5InitialReferenceBridge.lean` 在 `-DwarningAsError=true` 下暴露的 lane-local blocker 为：

1. `pD`：`lean.dependsOnNoncomputable`，因为实数除法常数依赖 `Real.instDivInvMonoid`；
2. `pB`：同上；
3. `pFull`：同上；
4. `hybridBudget`：依赖前述 noncomputable 定义；
5. `weighted_initial_ball_bound` 中 `hQ` 仅由 `nlinarith` 隐式消费，被 unused-variable linter 在 warning-as-error 模式下拒绝。

失败 run 中 placeholder scan 已通过，并打印了全部 14 个 theorem 的 `#print axioms` 报告；这些报告未出现 `sorryAx`。但由于 Lean 文件本身仍有 compile error，本日志**不**把该次输出提升为 `AXIOM_AUDIT=PASS` 或 `compiled_candidate`。

## 修复

修复 commit：`f8f1008d380160fc13a84c18eb81c943f31f97ea`

代码路径：

- `examples/routeb_p5_initial_reference_bridge_lean/P5InitialReferenceBridge.lean`
- `examples/routeb_p5_initial_reference_bridge_lean/verify.sh`

具体修复：

- 将包含实数除法常数或依赖这些定义的 budget 定义显式标记为 `noncomputable def`；
- 保留 `weighted_initial_ball_bound` 的 hypothesis contract，但将仅被自动算术 tactic 使用的 `hQ` 重命名为 `_hQ`，避免 warning-as-error unused-variable blocker；
- 未削弱任何公开 theorem proposition；
- 未加入 `sorry`/`admit`；
- 未修改 source binding、ODE uniqueness、Float64/controller、P8 coverage 或最终 integration 边界。

## 再验证状态

修复 push 已触发新的 `Lean agent sidecars` run：

- run: `34287106251`
- job: `102265109567`
- head: `f8f1008d380160fc13a84c18eb81c943f31f97ea`

写本日志时 runner 已完成 checkout / pinned dependency / Elan / local-FKG bootstrap，正在执行 `Run portable agent sidecars`。因此当前只记录“真实 blocker 已定位并修复、再验证正在执行”，不提前宣称 compile/axiom PASS。

## theorem/interface 边界保持不变

公开 theorem 仍为 14 个：

`qEnergy_nonneg`, `vEnergy_nonneg`, `pFull_split`, `hybridBudget_eq_full_of_block_match`, `weighted_initial_ball_bound`, `pFull_le_27_over_800_of_ball`, `pFull_lt_28_over_5_of_ball`, `hybridBudget_le_27_over_800_of_initial_match`, `hybridBudget_lt_28_over_5_of_initial_match`, `anchor_eq_self_of_block_match`, `centeredResidual_eq_zero_of_initial_match`, `anchorBias_eq_actual_minus_lbar_of_initial_match`, `nominalResidual_eq_zero_of_graph`, `same_qv_input_different_acceleration_residual`。

仍未形式化/未绑定：真实 six-coordinate/source projection、`referenceKey`、全时 ODE uniqueness、实际 nominal trajectory/flowpipe、Float64/controller/DH semantics、P8 coverage、registry/admission 与 P5/M4 final closure。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
