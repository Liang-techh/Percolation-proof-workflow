---
kind: review_result
review_id: T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE-sumengchen-20260908T2048Z
task_id: T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE
source_agent: 苏梦辰
created_at: "2026-09-08T20:48:00Z"
inspected_commit: "190b98044bd5effd691b6c4a577283adad7741e8"
admission_label: compiled_candidate
formal_certificate_allowed: false
registry_eligible: false
---

# T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE — Lean 4.32 CI repair closeout

## 1. Scope

本轮只处理苏梦辰上一轮已经认领并提交的 `T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE` Lean sidecar，不重新展开大规模数学探索，也不修改 registry / admission / 最终结论。

数学输入来自柳冠一 `GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL`：principal compact joint6 的 residual mismatch 保留 signed cross product

`Q = N_a D_c - N_c D_a`

并要求 numerator / denominator 证据必须来自同一 cell、同一 observable/source。Lean 侧因此继续使用 dependent-indexed

`ResidualCSE α CellKey SourceKey cell source`

作为接口边界，避免跨 cell/source 错拼证据。

## 2. 上一轮真实 CI blocker

上一轮候选在 GitHub Actions run `34273996737` / job `102222499532` 中真实执行并失败。focused 日志给出的 Lean 4.32 blocker 包括：

- `residualValue` 使用实数除法但定义未标 `noncomputable`；
- `rational_residual_sub_eq_cross_mul_div` 中 `field_simp` 已闭合目标，后续 `ring` 被判为 unreachable tactic；
- `abs_den_product_lower` 的 `hdeltaA` 未显式使用，触发 unused-variable linter；
- `quotient_difference_split` 使用 `<;>` 触发 `unnecessarySeqFocus`；
- Lipschitz triangle step 使用了当前环境不存在的 identifier `abs_add`；
- 最后 coefficient identity 中 `field_simp` 后的尾随 tactic 再次触发 unreachable-tactic；
- 受上述失败影响，相关 theorem 的 `#print axioms` 出现 `sorryAx`，因此上一轮不能视为 compiled candidate。

## 3. Lean 4.32 最小修复

修复 commit：

`190b98044bd5effd691b6c4a577283adad7741e8`

修改路径：

`examples/routeb_p4_joint6_rational_residual_bridge_lean/P4Joint6RationalResidualBridge.lean`

修复只针对 elaboration/linter compatibility，没有改变 theorem statement、hypotheses、常数、same-cell/source typing 或数学强度：

1. `residualValue` 改为 `noncomputable def`；
2. 两处 `field_simp` 后删除已经 unreachable 的尾随 tactic；
3. 未使用但为保持 theorem 接口保留的 `hdeltaA` 改名为 `_hdeltaA`；
4. `quotient_difference_split` 改为显式 sequential `field_simp` / `ring`，移除 `<;>`；
5. triangle inequality 改用 Lean 4.32/mathlib 当前可用的 `abs_add_le _ _`；
6. 其余 theorem / typed adapter / division-free gate 均保持原 statement。

## 4. Real GitHub Actions focused compile / axiom status

修复后 GitHub Actions：

- run: `34275549271`
- job: `102227551482`
- checkout SHA: `190b98044bd5effd691b6c4a577283adad7741e8`
- toolchain: Lean `4.32.0`

该 job 后续因为仓库出现更新的 sidecar push，被 workflow 的 cancel-in-progress 机制整体取消；但在取消发生之前，`examples/routeb_p4_joint6_rational_residual_bridge_lean/verify.sh` 已经完整执行结束并明确输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_JOINT6_RATIONAL_RESIDUAL_BRIDGE_FOCUSED_CHECK=PASS
SIGNED_CROSS_MISMATCH_BEFORE_ENCLOSURE=true
SAME_CELL_SOURCE_KEY_TYPED=true
DIVISION_FREE_SUP_GATE=true
DIVISION_FREE_LIPSCHITZ_GATE=true
PRINCIPAL_COMPACT_JOINT6_SOURCE_PACKET=OPEN
DEPLOYED_SOURCE_BINDING=OPEN
FLOAT64_FD_CONTROLLER_SOLVE=OPEN
P8_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_joint6_rational_residual_bridge_lean/verify.sh
```

因此整体 run 的最终 `cancelled` 不属于本 sidecar compile blocker；本 sidecar 的 focused compile 与 axiom scan 已在同一真实 job 中先行完成并 PASS。

## 5. Exported theorem / axiom status

本 sidecar 当前 12 个 exported theorem：

1. `ne_zero_of_pos_le_abs`
2. `rational_residual_sub_eq_cross_mul_div`
3. `rational_residual_eq_of_cross_mul`
4. `abs_div_le_of_abs_num_le`
5. `abs_den_product_lower`
6. `rational_residual_sup_le_of_cross_mul_bound`
7. `division_free_residual_sup_gate`
8. `same_cell_source_residual_eq`
9. `same_cell_source_division_free_sup_gate`
10. `quotient_difference_split`
11. `rational_residual_pair_lipschitz_of_cross_mul_packet`
12. `division_free_residual_lipschitz_gate`

真实 CI `#print axioms` 对以上 theorem 均只报告：

`[propext, Classical.choice, Quot.sound]`

无 `sorryAx`。

## 6. Formalized boundary vs remaining OPEN

已核化的只是 exact-real rational-residual algebra/interface seam：signed cross-mismatch、denominator lower bound、same-cell/source typed adapter、division-free sup gate 与 pairwise Lipschitz gate。

仍明确保持：

- `PRINCIPAL_COMPACT_JOINT6_SOURCE_PACKET=OPEN`：实际 `Joint6_GetStarTheta/zd6` 的 `N_a,D_a,N_c,D_c` 同 cell/source CSE packet 尚未绑定；
- `DEPLOYED_SOURCE_BINDING=OPEN`：actual observable / evaluator / source expression 尚未接入；
- `FLOAT64_FD_CONTROLLER_SOLVE=OPEN`：运行时 Float64、FD、controller、solve 误差语义尚未接入；
- `P8_ODE_COVERAGE=OPEN`：P8 same-domain / trajectory coverage 尚未接入；
- `REGISTRY_MUTATION=false`。

这些 OPEN 项不能由本 algebra sidecar 的 compile PASS 自动提升。

## 7. Coordination note

同轮新到的 `P5-099-TARGET-DOMAIN-DECISION` 数学结果已经被另一形式化 Agent（巨阳仙尊）认领 Lean seam，因此苏梦辰未重复认领，避免三形式化 Agent 之间重复实现。

当前仅为 `compiled_candidate`：**待封不觉独立验证 / 待梁智炜最终整合**。
