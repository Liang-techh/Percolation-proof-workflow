# review_result — GH-LEAN-P3-CENTRAL-FD-REMAINDER

- task_id: `GH-LEAN-P3-CENTRAL-FD-REMAINDER`
- agent: `苏梦辰`
- source_agent: `苏梦辰`
- math_source_agent: `红莲魔尊`
- math_source: `agent_review_inbox/review-GH-MATH-P3-FD-REMAINDER-honglianmozun-20260908T1507Z.md`
- status: `compiled_candidate`
- registry_mutation: `false`
- admission_mutation: `false`
- final_integration: `false`

## 本轮形式化内容

新增/修复 portable Lean sidecar：

`examples/routeb_p3_central_fd_remainder_lean/`

主文件：`P3CentralFDRemainder.lean`。该 sidecar 把数学 handoff 中的 centered finite-difference remainder 拆成最小 algebraic/Taylor packet 接口，明确不把尚未提供的 analytic `C^3 -> TaylorPair` 桥伪装成已证明内容。

当前 exported theorem 共 12 个：

1. `rawDefect_eq_remainder_diff`：对称 Taylor 展开中零阶、二阶项精确消去，raw defect 等于 `rplus-rminus`。
2. `rawDefect_abs_le_third`：由两侧 `M*h^3/6` remainder 界推出 sharp `|rawDefect| <= M*h^3/3`。
3. `central_fd_raw_defect_le_of_taylor_pair`：checker-facing 无除法形式 `3*|rawDefect| <= M*h^3`。
4. `centralFD_error_eq_raw_div`：在 `h>0` 下把 normalized centered-FD error 精确化为 `rawDefect/(2*h)`。
5. `central_fd_error_le_sixth_third_deriv`：sharp normalized 常数 `|D_h f-d| <= M*h^2/6`。
6. `shifted_stencil_contained`：`x∈[a,b]` 且 `h<=hmax` 时，`x-h` 与 `x+h` 落在 `[a-hmax,b+hmax]`。
7. `central_fd_error_uniform_of_step_cap`：由 `h<=hmax` 得统一 `M*hmax^2/6` 界。
8. `central_fd_x_cube_sharp`：`x^3` centered-FD error 精确为 `h^2`，验证 `1/6` 常数可达。
9. `raw_defect_x_cube_sharp`：同一 cubic regression 的无除法 raw defect 为 `2*h^3`。
10. `cubic_family_same_center_two_jet`：`A*(t-x0)^3` 在中心共享同一 value/一阶/二阶 jet 的代数回归。
11. `cubic_family_center_fd_error`：该族 centered-FD error 精确为 `A*h^2`，冻结“仅 pointwise C2 数据不足以给 uniform remainder budget”的信息边界。
12. `central_fd_two_term_linear_residual_budget`：最小二项线性 residual handoff；只在 caller 已 source-bind `e=e1+e2` 后传播两项误差预算，不改 residual normalization。

## typed state / interface 边界

`TaylorPair` 显式携带 `fplus,fminus,f0,d,d2,h,M,rplus,rminus`、`h_pos`、`M_nonneg`、两侧精确 Taylor identity 与两侧 absolute remainder bound。analytic 层仍必须单独证明：在完整 shifted stencil region 上的 `C^3` / third-derivative bound 如何构造该 packet。本 sidecar 没有把该 analytic bridge 设为 axiom，也没有假装 deployed evaluator 已满足它。

## 真实 CI 闭环

前一轮真实 GitHub Actions：

- run `34245119527`
- job `102125328170`

暴露 Lean 4.32 `warningAsError` blocker：`P3CentralFDRemainder.lean` 两处 proof sequencing 使用了 `<;>`，触发 `linter.unnecessarySeqFocus`。当时 theorem 的 `#print axioms` 已经只有 `[propext, Classical.choice, Quot.sound]`，问题属于 portability/linter，不是数学缺口。

本轮在 commit：

`a6909c96a7493836108e95842d648ac0d92cde79`

中把相关 sequencing 改成显式 proof bullets；没有修改 theorem statement、hypotheses、常数或数学语义。

修复后的真实 GitHub Actions：

- run `34246573961`
- job `102129982512`
- Lean `4.32.0`
- Lake `5.0.0`
- formal-math pin `795efb86f191735c5481675763537cfb4ff37e55`

本 sidecar 明确输出：

- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P3_CENTRAL_FD_REMAINDER_FOCUSED_CHECK=PASS`
- `TAYLOR_PACKET_ALGEBRA=true`
- `SHARP_ONE_SIXTH_CONSTANT=true`
- `SHIFTED_STENCIL_CONTAINMENT=true`
- `X3_SHARPNESS_REGRESSION=true`
- `POINTWISE_C2_OBSTRUCTION_FAMILY=true`
- `TWO_TERM_LINEAR_RESIDUAL_HANDOFF=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p3_central_fd_remainder_lean/verify.sh`

12 个 exported theorem 的 axiom 集均只含 `[propext, Classical.choice, Quot.sound]`；本 sidecar 无 `sorryAx`。

聚合 `portable-sidecars` workflow 仍为红色，但本任务 focused sidecar 已 PASS。聚合失败来自其他既有/未认领 sidecar（例如 FLT quotient 路径、M4 cross-branch、若干旧 P5/P7/P8 工件）；本轮未越权抢修这些任务。

## 依赖

- `Mathlib`
- 仓库固定 Lean `4.32.0`
- `examples/local_fkg/lake-manifest.json` 所固定依赖
- upstream formal-math commit `795efb86f191735c5481675763537cfb4ff37e55`
- `verify.sh` 从 `PATH` 解析 `lake/lean`，portable 路径由 `CI_PORTABLE=1` 接入 `.github/workflows/lean-agent-sidecars.yml`

## 仍 OPEN 的形式化接口

- analytic `C^3` / third-derivative uniform bound → `TaylorPair` 的正式构造；
- deployed evaluator / actual source function 与 `fplus,fminus,d,d2` 的 source binding；
- Float64/libm/outward-rounding 与真实 centered-FD execution semantics；
- 实际 residual 各项系数、单位与本 sidecar 的 linear handoff 的同一 normalization/source-key 绑定；
- downstream P4/P5/P8 的 same-domain coverage、ODE continuation / flowpipe coverage。

本结果仅为 `compiled_candidate`，未修改主 DAG/registry/admission/整体结论。

**待封不觉独立验证 / 待梁智炜最终整合。**
