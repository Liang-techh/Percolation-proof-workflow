---
kind: review_result
task_id: T-P5-059
agent: 巨阳仙尊
source_agent: 巨阳仙尊
reviewed_math_source: 狂蛮魔尊
status: compiled_candidate
integration_status: pending
admission_label: compiled_candidate
lean_sidecar: examples/routeb_p5_quadratic_form_parity_lean/
lean_commit: 0600b5114ad4cf45943c11f81a6611c7603697f1
actions_run: 34200654118
actions_job: 101978509951
---

# T-P5-059 review — quadratic-form parity Lean trusted core

本轮读取了 `README.md`、`task_queue.md`、`collaboration_board.md`，并消费狂蛮魔尊新提交的 `T-P5-059` 数学 review / companion（主 review commit `66c23f3876ad086ff695ea610389deab786f7a0f`，companion commit `8c7f303658fbf7be8a3cb4f142a6ed8682474907`）。认领前未发现苏梦辰或臭屁猪认领该数学结果；苏梦辰随后认领的是独立的 `T-P5-058`，因此本轮保持任务边界不重叠。

## Lean sidecar

路径：`examples/routeb_p5_quadratic_form_parity_lean/`

- `P5QuadraticFormParity.lean`
- `README.md`
- `verify.sh`
- `lean-toolchain`

claim commit：`ba8b6e51dc2cdbf373fa82f32b2252cf016786d0`。Lean 源文件 commit：`b72a091acb55d86f64fe4ced398635579d8aa3c5`。完整 portable sidecar head：`0600b5114ad4cf45943c11f81a6611c7603697f1`。

sidecar 使用仓库 `examples/local_fkg/lake-manifest.json` 与同版本 `leanprover/lean4:v4.32.0`；`verify.sh` 只从 `PATH` 解析 `lake` / `lean`，没有本机专属绝对路径，并注册 `CI_PORTABLE=1`。

本轮落成 14 个公开 theorem：

1. `balanced_pair_same_parity_cancel`
2. `balanced_pair_opposite_parity_flip`
3. `positive_excess_pair_vanishes_at_zero`
4. `opposite_parity_quadratic_jump`
5. `opposite_parity_cross_zero_invariant`
6. `particular_contact_invariance_iff`
7. `opposite_parity_gate_iff_universal_invariant`
8. `all_odd_quadratic_invariant`
9. `diagonal_squares_ignore_sign`
10. `counterexample_matrix_coercive`
11. `quadratic_form_parity_counterexample`
12. `square_only_pass_does_not_imply_mixed_invariance`
13. `accidental_contact_cancellation_not_structural`
14. `mixed_quadratic_consumer_of_parity_gate`

### 最小 kernel-facing decomposition

两通道对称二次型冻结为

`qform2 a b c x y = a*x^2 + 2*c*x*y + b*y^2`。

对 balanced even/odd 两通道，只翻转一个奇通道时，Lean 精确证明 jump

`qform2 a b c x y - qform2 a b c x (-y) = 4*c*x*y`。

因此本轮把两个不同强度的接口严格分开：

- **particular contact**：固定 `(x,y)` 时，左右值相等当且仅当 `c*x*y=0`；这允许偶然的零坐标 cancellation。
- **structural / universal gate**：要求所有 contact data 都可跨符号延拓，当且仅当 `c=0`，封装为 `OppositeParityGate c`。

这避免把一次偶然 contact cancellation 错升格为结构性 cross-block 消失。`all_odd_quadratic_invariant` 还证明两个奇通道同时翻转时任意内部 quadratic coupling 都不变，因此禁止把“所有 balanced odd block 必须对角化”作为错误的额外条件。

对 square-only 风险，本轮 formalize 了 exact counterexample：`a=b=1, c=1/2` 的二次型满足统一 coercivity

`(1/2)*(x^2+y^2) ≤ qform2 1 1 (1/2) x y`，

但在 `(1,1)` 与 `(1,-1)` 两侧取值分别为 `3` 与 `1`。与此同时两个 diagonal squares 完全相同。因此“逐通道平方已可延拓”不能推出 mixed quadratic energy 可延拓；mixed consumer 必须显式接收 opposite-parity cross gate。

另有 `positive_excess_pair_vanishes_at_zero` 把至少一侧含正 excess power 的 pair 在共同零点消失作为最小可复用 seam；没有在本轮重新做 factor/root discovery。

## 真实 GitHub Actions / focused compile

真实 Actions 证据来自 sidecar 完整 head `0600b5114ad4cf45943c11f81a6611c7603697f1`：

- workflow run: `34200654118`
- job: `101978509951`
- environment: Lean `4.32.0`, Lake `5.0.0`
- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P5_QUADRATIC_FORM_PARITY_FOCUSED_CHECK=PASS`
- `TWO_CHANNEL_STRUCTURAL_IFF=true`
- `MIXED_CROSS_TERM_GATE_EXPLICIT=true`
- `DIAGONAL_SQUARE_LIFT_UNSOUND_WITHOUT_GATE=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_quadratic_form_parity_lean/verify.sh`

14 个公开 theorem 的 `#print axioms` 均只出现 `[propext, Classical.choice, Quot.sound]`，本 lane 无 `sorryAx`。

该 workflow job 在 **本 T-P5-059 lane 已完整执行并打印 PASS 之后**，因主分支上另一 Agent 的后续 push 触发 workflow concurrency `cancel-in-progress` 而被整体标记为 `cancelled`；取消发生在后续 P8 lane 执行期间，不影响此前已经真实完成的 T-P5-059 focused compile / axiom audit。不得把 run 的整体 cancelled 误写成 T-P5-059 compile failure，也不得反过来把本 lane PASS 误写成 shared workflow 全绿。

同一日志中已有多个历史独立 lane 真实失败，例如 FLT quotient portable path、M4 cross-branch、P5 componentwise/direct-two-channel/parameter-tube/weighted-dual、P7 tail Schur 与旧 P8 ramp reconstruction；本轮未越权修复这些不属于 `T-P5-059` 的 lane。

## 仍开放的接口边界

- 狂蛮魔尊提出的 finite-index parity conjugation / `K_EO=0` 全矩阵 theorem 尚未形式化；当前只锁定最小两通道必要充分结构 gate。
- quantitative pair Lipschitz / Hölder transport 尚未形式化。
- factor/root discovery 与 normalized primitive 的 deployed construction 不在本 trusted core。
- actual P5 `K`、balanced parity partition、source coefficient binding 未做。
- Float64 / FD / controller / solve / libm semantics 未做。
- P8 same-domain ODE / flowpipe coverage 未做。
- square-only certificate 不能替代 mixed quadratic gate；particular-contact cancellation 也不能替代 structural universal gate。
- P5/P8/M4 final closure 与 registry/admission mutation 均未做。

当前严格状态：`compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
