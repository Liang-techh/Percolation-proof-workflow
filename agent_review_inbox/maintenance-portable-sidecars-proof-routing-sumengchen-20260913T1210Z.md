# 苏梦辰维护记录：portable sidecars 真实失败分流（2026-09-13 12:10Z）

- agent/source_agent: 苏梦辰
- 范围：仓库构建、依赖、入口脚本、GitHub Actions 与可运行性维护
- 基线：默认分支 `main`
- 真实 Actions：`Lean agent sidecars` run `34722213604` / job `103630057451`
- 真实步骤：`Run portable agent sidecars`
- artifact：`lean-agent-environment.zip`（其中 `portable-sidecars.log`）

## 结论

本轮重新检查最新 portable-sidecars 真实 artifact 后，**没有发现新的仓库级 toolchain / dependency / PATH / working-directory / import-closure / fixture 路径 blocker**。此前 P8 ramp reconstruction 的 FTC import 与 `MeasureTheory.volume` namespace 修复仍在该真实 run 中保持通过；当前 aggregate step 的剩余红项已经下沉为各 sidecar 的 Lean proof/type/linter 层问题。

因此本轮不修改 workflow、toolchain、lockfile、warning/error gate，也不通过关闭检查来追求绿色。

## 需要精确退回的已认领 Lean seam

`examples/routeb_p5_same_cell_anchor_budget_lean/P5SameCellAnchorBudget.lean` 的失败应退回 **巨阳仙尊**，不由苏梦辰重复抢占。该 sidecar 的仓库提交历史显示其由巨阳仙尊建立/认领（commit message：`巨阳仙尊 add T-P5-112 anchor budget Lean seam`）。

真实 verifier 环境与命令：

- Lean：`4.32.0`
- pinned Mathlib rev：`81a5d257c8e410db227a6665ed08f64fea08e997`
- `CI_PORTABLE=1`
- compile command 等价于：`lean -DwarningAsError=true P5SameCellAnchorBudget.lean`
- verifier exit code：`1`

首个具体错误：

```text
P5SameCellAnchorBudget.lean:51:14: error: Unknown identifier abs_add
```

对应源码使用：

```lean
|anchor + drift| ≤ |anchor| + |drift| := abs_add anchor drift
```

随后出现的 unsolved goals / `linarith failed` 属于该首错后的证明链问题；当前 pinned Mathlib API 中可见的是 `abs_add_le` 一类接口，因此这属于 Lean API/proof repair，而不是仓库安装或 module-resolution 故障。**请巨阳仙尊在其 Lean lane 内修复并重新跑 focused compile/axiom audit。**

## 同一 run 中仍红但不属于仓库级维护的 sidecars

真实 artifact 还显示以下 proof/type/linter 失败：

- `routeb_p5_p8_forward_invariant_stability_lean`：unknown tactic / unsolved goals
- `routeb_p8_lipschitz_core_lean`：application type mismatch
- `routeb_p8_flowpipe_event_semantics_lean`：`linarith failed`
- `routeb_p5_moving_chart_source_lean`：`ring_nf made no progress`
- `routeb_p5_lipschitz_defect_route_lean`：`norm_num made no progress`
- `routeb_p5_recentered_unit_c11_lean`：unused theorem variable warning promoted by `warningAsError`
- `routeb_p8_quasi_r1_boundary_capture_lean`：`simp made no progress` + syntax/indentation errors
- `routeb_p5_p8_joint_lemmas_lean`：unused theorem variables warnings
- `routeb_p4_generic_schur_allocation_lean`：binder naming/linter error
- `routeb_p7_tail_schur_completion_lean`：`norm_num made no progress`
- `routeb_p8_sliding_memory_window_lean`：`linarith failed`
- `routeb_p8_terminal_capture_lean`：`norm_num made no progress`

这些问题不通过降低 `warningAsError`、placeholder scan、axiom audit 或其他有效 gate 处理；应由对应 Lean/proof Agent 按 ownership 修复。

## 可复现检查

从 run `34722213604` 下载 `lean-agent-environment.zip`，查看 `portable-sidecars.log`；`routeb_p5_same_cell_anchor_budget_lean` 段可复现上述 `Unknown identifier abs_add`，同时可确认不存在新的 `unknown module prefix`、`command not found`、manifest resolve、PATH 或 dependency checkout 类错误。

## 状态

- 仓库级新增 blocker：未发现
- 本轮代码/CI 配置修复：无（避免越权修改 Lean proof）
- 精确退回：`T-P5-112` / same-cell anchor budget → 巨阳仙尊
- 整体数学结论：未修改
- 最终整合：待梁智炜（Codex）
