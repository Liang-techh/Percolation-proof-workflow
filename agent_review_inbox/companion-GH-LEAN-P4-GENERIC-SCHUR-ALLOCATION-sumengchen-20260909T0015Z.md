---
kind: companion_log
task_id: GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION
source_agent: 苏梦辰
created_at: 2026-09-09T00:15:00Z
integration_status: pending
admission_label: pending
registry_mutation: false
---

# GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION — Lean 4.32 repair companion

本轮优先处理上一轮 sidecar 的真实 GitHub Actions 失败，没有转去重复做新的数学探索。

## 真实 blocker

上一轮 `Lean agent sidecars`：

- run: `34285443768`
- job: `102259873472`
- checkout: `f3feb6ec6ee663e733126f2049ba85d26c5a1a22`
- pinned Lean: `4.32.0`

本 sidecar `examples/routeb_p4_generic_schur_allocation_lean/verify.sh` 的 focused compile 暴露两处真实 Lean 4.32 blocker：

1. `P4GenericSchurAllocation.lean:53:14`：`sq_sub_smul` 中一次把 `Finset.sum_sub_distrib` 与 `Finset.sum_add_distrib` 连续作用到三项和式，rewrite 找不到期望的 sum-of-difference 形状；
2. `P4GenericSchurAllocation.lean:118:2`：`zero_radius_boundary_not_finite_witness` 的 `norm_num` 已关闭目标，尾随 `ring` 触发 `No goals to be solved`。

因此该失败编译中的 `sq_sub_smul` 及其 downstream theorem axiom report 出现 `sorryAx`；不能把上一轮标成 compiled candidate。

## 最小 repair

repair commit：`6426af1f007c6360bb90d11d8a53fb3a90d6ea38`。

修改仅限 proof implementation：

- `sq_sub_smul` 先显式把三项表达式固定为 `((x^2 - cross) + a^2 y^2)`，再分两步使用 `Finset.sum_add_distrib`、`Finset.sum_sub_distrib`，最后只把两类标量乘法提出有限和；
- `zero_radius_boundary_not_finite_witness` 删除已经无目标后的多余 `ring`。

没有修改 8 个 theorem statement、hypotheses、常数、有限维 `Vec n := Fin n → ℝ` 接口或 Euclidean/no-double-charge 数学强度。

## 再 Lean 状态

repair 已触发新的 `Lean agent sidecars`：

- run: `34294059656`
- job: `102286686583`
- checkout head: `6426af1f007c6360bb90d11d8a53fb3a90d6ea38`

本 companion 写回时，checkout、pinned formal-math、Elan 已完成，job 正在 bootstrap pinned local-FKG；`Run portable agent sidecars` 尚未结束。因此当前仍只写 `pending`，不虚报 compile PASS 或 axiom PASS。下一轮继续优先读取该真实 job；若 focused path 仍失败，仅按其诊断继续最小修复。

## OPEN 边界保持不变

- dense `M0_CC⁻¹` metric transport / weighted-square reification；
- deployed DH/source expression binding for `ell` / `r`；
- matching-metric port cap；
- source/domain/path coverage；
- Float64 / FD / controller / solve；
- P8 ODE / flowpipe coverage；
- parent admission、registry mutation、最终 integration。

**当前：pending；待封不觉独立验证 / 待梁智炜最终整合。**
