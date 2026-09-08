# Review result — GH-LEAN-P4-032-relative-additive

- task_id: `GH-LEAN-P4-032-relative-additive`
- agent: `巨阳仙尊`
- source_agent: `巨阳仙尊`
- status: `compiled_candidate`
- integration_authority: `梁智炜（Codex）`
- independent_gate: `封不觉`

## Scope

本轮只处理 task queue 明确分配的 P4-032 relative-plus-additive Lean 编译闭环；没有重新做数学探索，也没有修改 provenance / receipt / admission / registry。

数学/Lean 依赖链：

1. `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_BlockDefects.lean`
2. `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DefectNormBudget.lean`
3. `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_WeightedThreeTerm.lean`
4. `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_RelativeAdditive.lean`

新增 portable focused sidecar：

- `examples/routeb_p4_relative_additive_focused/verify.sh`
- `CI_PORTABLE=1`
- `lake` / `lean` 仅从 `PATH` 查找
- 固定使用 `examples/local_fkg/lean-toolchain` 与 `examples/local_fkg/lake-manifest.json`
- `-DwarningAsError=true`
- 对 target 做 placeholder scan 与 `sorryAx` audit

## Kernel-facing theorem boundary

目标文件当前公开并被 focused sidecar 审计的 theorem：

- `effective_coefficients_nonnegative`
- `affine_budget_identity`
- `weighted_budget_le_relative_additive`
- `relative_additive_budget_nonnegative`
- `consume_weighted_budget`
- `force_relative_additive`
- `accel_relative_additive`
- `zero_bias_corollary`

核心 typed seam 是：对同一 compatible budget packet `p : Parameters` 与同一点 `energy, ED, EB`，若

- `ED ≤ p.kappaD * energy + p.biasD`,
- `EB ≤ p.kappaB * energy + p.biasB`,
- 三项 weighted budget 已由上游 `NEW_P4_032_WeightedThreeTerm.lean` 给出，

则将其核内收缩到

`rhoEff p * energy + biasEff p`,

其中 `tau` 只平方一次；force 分支继续要求 `ActionBound (MBD * J) p.tau`，acceleration 分支继续要求 `ActionBound MBD p.tau`，没有把两个 typed defect convention 混并。

`zero_bias_corollary` 只在显式 `biasD = 0` 与 `biasB = 0` 下删除 additive load；没有从小能量、正权重或 source-independent 条件中偷推零 bias。

## Lean → CI → fix → Lean

### 首轮真实失败

新增 focused sidecar 的首轮 Actions：

- run: `34174347540`
- job: `101900674942`
- head: `f2aec2e41e07123c17e4942fcdc01125e644741f`

真实 Lean 4.32.0 日志定位到 `NEW_P4_032_RelativeAdditive.lean` 的 addition-order type mismatch：原证明使用

`add_le_add_left hd (p.weights.value 0 * (p.rhoA * energy))`

得到的是 `D + A ≤ D' + A`，而 `weightedBudget` 需要 `A + D ≤ A + D'`。该失败进一步让依赖 theorem 的 axiom report 临时出现 `sorryAx`。

同时 focused sidecar 暴露 target 缺少 `relative_additive_budget_nonnegative` 的 `#print axioms` 行，因此即使类型错误单独消失，原 audit 仍不会完整通过。

### 修复

修复 commit：

- `6c2ce166369319a73e70876020f4a175e08eaa71`

具体修复：

1. 将该步改为 `add_le_add_right hd (...)`，使加法顺序与 `weightedBudget` 的 AST 直接一致；
2. 增加 `#print axioms relative_additive_budget_nonnegative`；
3. 删除文件头已失真的 `UNCOMPILED / No Lean run` 描述，但没有添加 source/coverage/admission 成功声明。

## GitHub Actions result

修复后的真实 Actions：

- workflow: `.github/workflows/lean-agent-sidecars.yml`
- run: `34174702246`
- job: `101901701564`
- head: `6c2ce166369319a73e70876020f4a175e08eaa71`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 明确输出：

- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P4_RELATIVE_ADDITIVE_FOCUSED_CHECK=PASS`
- `RHO_EFF_BIAS_EFF_TYPED=CHECKED`
- `SQRT_DEPENDENCE=false`
- `SOURCE_BINDING=OPEN`
- `COVERAGE=OPEN`
- `ADMISSION_MUTATION=false`
- `P4_M4_FINAL_INTEGRATION=false`
- `SIDECAR_RESULT=PASS path=examples/routeb_p4_relative_additive_focused/verify.sh`

8 个 target theorem 的 `#print axioms` 均只有：

`[propext, Classical.choice, Quot.sound]`

本 target lane 无 `sorryAx`。

shared workflow 整体仍为 failure，但失败来自其他独立 portable lanes（例如 FLT quotient path、M4 cross-branch、P5 componentwise / parameter-tube / weighted-dual、P7 tail Schur、P8 ramp reconstruction）；这些不属于本 task，本轮未修改。

## Remaining boundary

本轮只关闭 source-independent algebra / typed-consumer 层。仍未形式化或未绑定：

- concrete P4 source coefficient / defect-envelope binding；
- Float64 / true-DH / solve / controller 语义到 `ED, EB, rhoA, tau, kappaD, kappaB, biasD, biasB` 的可信桥；
- 与同一 P8 trajectory/domain 的 coverage；
- downstream P4/M4 最终 closure；
- registry / admission promotion。

因此当前只能记为 `compiled_candidate`，不能自行宣称最终整合。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
