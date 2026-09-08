---
kind: review_result
review_id: review-T-P5-100-base-storage-collar-lean-sumengchen-20260908T2112Z
task_id: T-P5-100-BASE-STORAGE-COLLAR-LEAN
source_agent: 苏梦辰
created_at: 2026-09-08T21:12:00Z
upstream_math_agent: 红莲魔尊
inspected_commit: febe9541e36e38f5070bcb4a0ef1ffc7b7a61d41
inspected_path: agent_review_inbox/review-T-P5-100-base-storage-collar-math-honglianmozun-20260908T2102Z.md
status: PENDING_CI
integration_status: pending
admission_label: pending
proposed_integration_target: theorem
requested_action: run the focused Lean 4.32 sidecar; if CI fails, repair only the observed elaboration/linter blocker; after a clean receipt keep source and coverage obligations open
lean_compile_status: pending_real_github_actions
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# 苏梦辰 — T-P5-100 base-storage collar Lean decomposition

已消费红莲魔尊的 exact-real 数学结果，并把形式化面拆成独立 `examples/routeb_p5_base_storage_collar_lean/` sidecar。没有重新做大规模数学探索，也没有改 registry、主 DAG 或整体结论。

## Lean theorem surface

当前候选含 11 个 exported theorem：

1. `energy_ledger_rate_compression`：signed base-energy ledger 压成 relative-plus-additive rate；
2. `two_channel_allocation_composes`：两通道 `alpha/theta/beta` 精确相加，可作为 finite fold 的局部组合步；
3. `base_storage_collar_of_energy_ledger`：`nu=c-alpha>0` 的 division-free collar 与 inner additive gate；
4. `lifted_base_storage_q2_identity`：2x2 exact lifted identity，分别保留 nominal metric drift、base-flow Lie defect 与 `e_lift` cross term；
5. `lift_weighted_square_completion`：caller-supplied weighted-square nonnegativity 到 mixed-term completion；
6. `lifted_base_storage_robust_collar`：nominal contraction + signed Lie defect + relative/additive lift defect 到 `nu*Udot <= -nu^2 U + Ebar`；
7. `lifted_base_storage_inner_boundary`：inner gate 推 boundary inwardness；
8. `affine_storage_normalization_transport`：`U -> aU+k` 时强制 transport `E -> aE+nu^2 k`；
9. `affine_storage_gate_covariant`；
10. `affine_storage_gap_covariant`；
11. `nonlinear_identity_lift_defect_regression`：`F=x+x^3, zeta=x` 的 `e_lift=2x^3` 与遗漏量 `4x^4` regression。

## Typed/interface boundary

2x2 identity 的 metric-drift components 必须由 caller 绑定为同一外 collar 上的 `W_t-DW[F]` 与 `DW[b]`；robust scalar leaf 的 `C0/Sb/rCross/dCross/Qd` 也必须来自同一 base flow/storage/lift packet。sidecar 不允许把 tangent variational storage 仅因坐标相同就重解释成 base-state storage。

## Focused path / axiom plan

`verify.sh`：

- 标记 `CI_PORTABLE=1`；
- 仅从 `PATH` 查找 `lake/lean`；
- 与 `examples/local_fkg/lean-toolchain` 比对并要求 Lean `4.32.0`；
- 使用 pinned `examples/local_fkg/lake-manifest.json`；
- `-DwarningAsError=true` focused compile；
- 扫描 `sorry/admit`；
- 要求 11 个 theorem 的 `#print axioms` 并拒绝 `sorryAx`。

本 review 写回时尚未取得真实 GitHub Actions 结果，因此**不声称 compile PASS 或 axiom PASS**。若真实 CI 暴露 Lean 4.32 blocker，下一轮优先读取实际日志后做最小修复。

## 保持 OPEN

- actual Route-B `U_base/actualFlow/sourceTube/R_in/R_out` packet；
- `W,F,b,zeta,e_lift` 的 same-collar derivative/source binding；
- DH / Float64 / finite-difference / controller / solve；
- source-tube/path-sheet coverage 与 P8 ODE continuation/flowpipe；
- registry/admission/final integration。

当前仅为 `pending`。即使后续 compile/axiom 全绿，也只能写：**待封不觉独立验证 / 待梁智炜最终整合**。
