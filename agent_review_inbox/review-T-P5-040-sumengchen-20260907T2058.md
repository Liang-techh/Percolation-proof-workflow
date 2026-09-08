---
kind: review_result
task_id: T-P5-040
review_id: review-T-P5-040-sumengchen-20260907T2058
agent: 苏梦辰
source_agent: 苏梦辰
upstream_review: review-T-P5-040-honglianmozun-20260907T1950
status: compiled_candidate
created_at: 2026-09-07T20:58:00-06:00
---

# T-P5-040 — mixed relative-plus-additive Pareto closure Lean formalization

## Scope

本轮只做红莲魔尊 `T-P5-040` 已有数学推导的 Lean theorem decomposition 与 portable sidecar 修复闭环，不重新做大规模数学探索，不做 provenance / receipt / admission / re-audit，也不修改 P5/M4/P8 父状态、DAG、registry 或整体结论。

上游数学 review：`review-T-P5-040-honglianmozun-20260907T1950.md`，数学提交 commit `06ef9ccc4aa6055a6a3bd7d6f0a5bb9055220f47`。本 Agent 的认领 commit 为 `4ac6429bf7cd3db42096847966bafe2dc59347c5`。

该 sidecar 固定以下 P5 block-(4,5) Pareto 数据：

- `c(r) = (109-r)/200`
- `a4(r) = (250+53r)/1500`
- `a5 = 1/6`
- `reserve4 = a4(r)-rho4`
- `reserve5 = a5-rho5`
- `A4 = 250+53r-1500rho4`
- `A5 = 1-6rho5`

输入接口保持为数学层已有的 mixed residual contract：

- `Q >= c(r)V + a4(r)u4^2 + a5 u5^2`
- `Vdot = -Q - u4*l4 - u5*l5`
- `|l4| <= rho4|u4| + b4`
- `|l5| <= rho5|u5| + b5`
- `reserve4 > 0`, `reserve5 > 0`

不在 Lean 中虚构实际 deployed residual/source/runtime/trajectory binding。

## Portable Lean sidecar

目录：`examples/routeb_p5_mixed_relative_additive_lean/`

- `P5MixedRelativeAdditive.lean`
- `lean-toolchain`
- `README.md`
- `verify.sh`

`lean-toolchain` 固定为 `leanprover/lean4:v4.32.0`。`verify.sh` 标记 `CI_PORTABLE=1`，从 `PATH` 解析 `lake` / `lean`，检查 `examples/local_fkg/lake-manifest.json` 与 toolchain 一致，再用 `lake env lean -DwarningAsError=true` 做 focused compile；随后逐 theorem 检查 `#print axioms` 并拒绝 `sorryAx`。

本轮修复链上的相关 commits：

- `47a4fc8863bc829116a786f37eed10f1ce9383d0` — 加入 focused verifier
- `30386cf953f8e05c3ae2e628be1bd1a6cb4b5505` — Lean 4.32 focused proof 修复
- `fd04b486f0e393c599c308a2a0de1a68b6e08367` — abs-square transport 修复
- `3104fe39902bbb65a11b5d0b53b419a1ab31da87` — 最终 residual sign normalization 修复

## Kernel theorem surface

namespace：`RouteBP5MixedRelativeAdditive`。当前导出并做 axiom audit 的 11 个 theorem：

1. `abs_sq_eq`：`|x|^2 = x^2`，作为后续纯代数 absolute-value transport 的最小 lemma。
2. `residual_power_bound`：从 `|l| <= rho|u|+b` 推出 `-u*l <= rho*u^2+b|u|`。
3. `mixed_square_completion_cleared`：无除法 sharp completion，`4t(-tu^2+b|u|) <= b^2`。
4. `mixed_square_completion`：`t>0` 时得到 sharp charge `-tu^2+b|u| <= b^2/(4t)`。
5. `reserve4_pos_iff`：`reserve4>0 <-> A4>0`。
6. `reserve5_pos_iff`：`reserve5>0 <-> A5>0`。
7. `block45_pareto_mixed_residual_decay`：完成两通道 relative-plus-additive absorption，得到
   `Vdot <= -c(r)V + b4^2/(4 reserve4) + b5^2/(4 reserve5)`。
8. `block45_pareto_quarter_gate_cross`：把 quarter-barrier 的 integer checker gate 精确重写到 reserve-variable cross inequality。
9. `block45_pareto_bias_first_exit_gate`：在 `V=1/4`、`b4^2<=B4`、`b5^2<=B5` 与正 reserve 下，由 division-free checker gate推出 `Vdot<0`。
10. `block45_zero_relative_gate_reduces`：`rho4=rho5=0` 时精确退化回 T-P5-039 additive Pareto gate。
11. `block45_pareto_incremental_gate_cross`：冻结 incremental `dc^2` tube 的 exact cross-multiplied arithmetic gate。

quarter-barrier checker gate 为：

`300000*B4*A5 + 1200*B5*A4 < (109-r)*A4*A5`。

零 relative charge 时精确退化为：

`300000*B4 + 1200*(250+53r)*B5 < (109-r)*(250+53r)`。

incremental tube gate 为：

`900000*G4*A5 + 3600*G5*A4 < (109-r)*A4*A5`。

T-P5-039 的 exact Pareto optimizer 层明确复用，没有在本 sidecar 重复实现参数优化器。

## Real Actions repair loop

本轮按要求读取了真实 GitHub Actions 日志并做修复闭环。

### 失败轮

commit `fd04b486f0e393c599c308a2a0de1a68b6e08367` 对应：

- workflow run `34180671679`
- job `101918968240`

真实 Lean 4.32 日志在 `residual_power_bound` 暴露了 normalization 类型不匹配：已有 hypothesis 是 `-(u*l) <= |u*l|`，目标写成 `-u*l <= |u||l|`，Lean 没有自动把两种乘法/负号语法正规化。因此失败 run 中依赖 theorem 暂时出现 `sorryAx`。这不是数学假设或常数问题。

最终在 commit `3104fe39902bbb65a11b5d0b53b419a1ab31da87` 中改为显式 `simpa only [neg_mul] using hsign`，没有削弱任何 theorem statement、常数或 interface。

### 最终 focused PASS

最终 commit `3104fe39902bbb65a11b5d0b53b419a1ab31da87` 对应真实 Actions：

- workflow run `34181527795`
- job `101921468341`
- Lean `4.32.0`
- Lake `5.0.0-src+8c9756b`

本 sidecar 的真实日志明确输出：

- `AXIOM_AUDIT=PASS`
- `P5_MIXED_RELATIVE_ADDITIVE_FOCUSED_CHECK=PASS`
- `T_P5_039_OPTIMIZER_LAYER_REUSED_NOT_DUPLICATED=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_mixed_relative_additive_lean/verify.sh`

11 个 exported theorem 的 `#print axioms` 均只有 `[propext, Classical.choice, Quot.sound]`，当前 sidecar 无 `sorryAx`。

聚合 `portable-sidecars` job 仍为红色，但真实同一日志确认与 T-P5-040 无关。失败来自其他未认领工件，包括：

- `anthropic_flt_quotient_transport_sidecar` 的 `../local_fkg` 路径
- `routeb_m4_cross_branch_budget_lean`
- `routeb_p5_componentwise_relative_decay_lean`
- `routeb_p5_direct_two_channel_gate_lean`
- `routeb_p5_parameter_tube_gain_lean`
- `routeb_p5_weighted_dual_residual_lean`
- `routeb_p7_tail_schur_completion_lean`
- `routeb_p8_ramp_reconstruction_sidecar`

本轮没有抢占或修改这些其他 Agent 的 sidecar。

## Dependencies / remaining formal interfaces

直接上游数学依赖：T-P5-040；T-P5-039 的 exact Pareto optimizer 已复用。柳冠一 T-P5-041 的 coordinate/source bridge 已给出后续把真实 source 压成 `(rho_i, B_i)` mixed contract 的路线，并允许 `b_i` 保持 pointwise/state-dependent，只要求 checker 获得统一 square budget `b_i^2 <= B_i`；但实际 deployed source binding 仍未由本 sidecar声称。

仍需上游/下游提供：

- 同一 domain 上真实 residual component contract `|li| <= rhoi|ui|+bi`；
- `A4>0`、`A5>0` 的实际 reserve certificate；
- quarter consumer 的统一 `B4,B5` square budgets；
- incremental consumer 的统一 `G4,G5` square budgets；
- true-DH / Float64 / finite-difference / controller / matrix-solve execution remainder 的实数 reification 与 containment；
- P8 ODE existence / continuation / same-domain flowpipe coverage；
- P5/P8/M4 最终 composition、冲突处理、DAG/registry/admission 决策。

本 review 不宣称上述接口已闭合，也不修改整体结论。

**Status: compiled_candidate — 待封不觉独立验证 / 待梁智炜最终整合。**
