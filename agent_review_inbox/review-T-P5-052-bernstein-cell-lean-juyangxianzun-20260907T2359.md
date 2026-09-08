---
kind: review_result
task_id: T-P5-052
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source_agent: 古月方源
created_at: 2026-09-07T23:59:00-06:00
status: compiled_candidate
integration_status: pending
admission_label: pending
---

# Review — T-P5-052 correlated Bernstein cell gate Lean

## 1. 本轮消费的数学输入

消费古月方源 `review-T-P5-052-guyuefangyuan-20260907T2334.md` / companion 中的 source-independent Bernstein cell gate：把同一个 cell 参数上的低次相关 remainder 保持为 exact polynomial，使用 Bernstein 控制点证明整段非负；若 coarse control 出现负值则只允许 `SUBDIVIDE/UNDECIDED`，不能把它当成数学反例。

本轮没有重新做 P5 大规模数学搜索，也没有做 provenance/admission/re-audit。

## 2. Claim 与实现路径

Claim：

- `agent_review_inbox/claim-T-P5-052-bernstein-lean-juyangxianzun-20260907T2342.md`

Portable sidecar：

- `examples/routeb_p5_bernstein_cell_lean/P5BernsteinCell.lean`
- `examples/routeb_p5_bernstein_cell_lean/README.md`
- `examples/routeb_p5_bernstein_cell_lean/lean-toolchain`
- `examples/routeb_p5_bernstein_cell_lean/verify.sh`

Pinned toolchain：`leanprover/lean4:v4.32.0`。`verify.sh` 从 `PATH` 使用 `lake/lean`，并复用仓库 `examples/local_fkg/lake-manifest.json`；无本机专属绝对路径。

最终代码 commit：`e450973911e8a0a1fbff9c08bc48096d4add247d`。

## 3. Lean theorem decomposition

本轮公开 theorem 共 21 个：

1. `quad_bernstein_identity`
2. `cubic_bernstein_identity`
3. `quad_bernstein_weights_sum`
4. `cubic_bernstein_weights_sum`
5. `quadBern_nonneg_of_controls`
6. `cubicBern_nonneg_of_controls`
7. `quadPoly_nonneg_of_controls`
8. `cubicPoly_nonneg_of_controls`
9. `quad_decasteljau_left_half`
10. `quad_decasteljau_right_half`
11. `cubic_decasteljau_left_half`
12. `cubic_decasteljau_right_half`
13. `quad_left_controls_nonneg`
14. `quad_right_controls_nonneg`
15. `cubic_left_controls_nonneg`
16. `cubic_right_controls_nonneg`
17. `endpoint_only_unsound_regression`
18. `negative_control_positive_polynomial_identity`
19. `negative_control_positive_polynomial_lower_bound`
20. `negative_control_positive_polynomial_middle_control`
21. `cubic_packets_feed_two_remainder_consumer`

形式化核心包括：

- degree-2 exact conversion
  `a0+a1 t+a2 t^2 = b0(1-t)^2+2 b1 t(1-t)+b2 t^2`
  with `b0=a0`, `b1=a0+a1/2`, `b2=a0+a1+a2`；
- degree-3 exact conversion
  `g0=c0`, `g1=c0+c1/3`, `g2=c0+2c1/3+c2/3`, `g3=c0+c1+c2+c3`；
- `[0,1]` 上 Bernstein 权重非负，因此所有 control `>=0` 推出整个 cell polynomial `>=0`；
- quadratic/cubic dyadic de Casteljau left/right half 的 exact identity；
- 非负 controls 在 dyadic half subdivision 下保持非负；
- typed adapter：两个已经由 Bernstein packet 证明非负的 `Rtr/Rdet` 可以直接喂给已有的 branch-free two-remainder consumer，不重复证明 2x2 affine completion。

## 4. 防误用 regression

Lean 固化两个关键边界：

### endpoint-only 不安全

`p(t)=1-5t+5t^2` 满足

- `p(0)=1`
- `p(1)=1`
- `p(1/2)=-1/4`

因此只查 cell 两端不能替代 Bernstein/full-cell gate。

### negative coarse control 不能当 rejection

Lean 精确证明

`7/20 - t + t^2 = (t-1/2)^2 + 1/10 >= 1/10`

但其 quadratic middle Bernstein control 为

`7/20 - 1/2 = -3/20 < 0`。

因此 coarse negative control 的正确语义是 `SUBDIVIDE/UNDECIDED`，不能报告 polynomial negativity。

## 5. Lean / CI 修复过程

初稿提交后，在最终 Actions 前自检发现 cubic left/right nonnegative-control theorem 的 nested conjunction 使用 `constructor <;> nlinarith` 过宽，可能把 `nlinarith` 应用到尚未拆开的 conjunction goal。没有弱化 theorem statement，改成显式逐层 `constructor`，得到最终修复 commit：

`e450973911e8a0a1fbff9c08bc48096d4add247d`。

这是 pre-CI proof-structure repair；本轮不伪造“本 sidecar 先在 CI 失败再修复”的记录。最终 head 的第一次完整可观察 CI 已直接通过本 lane。

## 6. 真实 GitHub Actions 结果

Workflow：`.github/workflows/lean-agent-sidecars.yml`

- run: `34192313841`
- job: `101952704738`
- runner: GitHub-hosted Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0`
- head: `e450973911e8a0a1fbff9c08bc48096d4add247d`

本 sidecar 日志明确输出：

- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P5_BERNSTEIN_CELL_FOCUSED_CHECK=PASS`
- `BERNSTEIN_QUAD_CUBIC_CORE=true`
- `DYADIC_DECASTELJAU_HALF=true`
- `NEGATIVE_CONTROL_IS_NOT_REJECTION=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_bernstein_cell_lean/verify.sh`

21 个公开 theorem 的 `#print axioms` 均只出现：

`[propext, Classical.choice, Quot.sound]`

本 lane 无 `sorryAx`。

同一 run 中既有的 `examples/routeb_p5_branchfree_affine_majorant_lean/verify.sh` 也独立输出 `P5_BRANCHFREE_AFFINE_MAJORANT_FOCUSED_CHECK=PASS`，所以本轮 typed Bernstein packet adapter 所指向的 downstream branch-free consumer 在同一 pinned CI 环境中是健康的。

Shared workflow 最终仍为红色，但原因是其他已存在的独立 sidecar（如 FLT quotient transport、M4 cross-branch、P5 componentwise/direct-two-channel/parameter-tube/weighted-dual、P7 tail Schur、P8 ramp reconstruction 等）失败。本轮没有抢占或修改这些 lane；不能用 shared 红灯否定本 T-P5-052 focused PASS，也不能用本 focused PASS 宣称 shared workflow 全绿。

## 7. 尚未形式化 / 不得越界解释

当前仍明确 OPEN：

- `EVENTUAL_STRICT_POSITIVITY_SUBDIVISION_THEOREM=OPEN`：严格正 cubic 在足够细 dyadic subdivision 后所有 controls 变正的 eventual theorem 未纳入 trusted core；
- deployed source 中 `Rtr/Rdet` 对 cell parameter 的 exact polynomiality / degree provenance；
- concrete cell affine parameterization 与同一 source-key binding；
- exact/rational source coefficient exporter；
- `DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN`：Float64、FD、controller/solve semantics；
- `P8_ODE_COVERAGE=OPEN`；
- `P5_M4_FINAL_INTEGRATION=false`；
- `REGISTRY_MUTATION=false`。

因此本结果只能标为 `compiled_candidate`，不能宣称 P5 parent、P8 coverage、M4 closure 或 registry admission 已完成。

## 8. 建议的下游接口

数学/source Agent 下一步应优先给出每个真实 P5 cell 的 exact packet：

`cell_key + affine_parameter_map + monomial_coefficients(Rtr,Rdet) + exact/rational provenance`

checker 只需执行：monomial→Bernstein exact conversion → controls 检查 → 若失败则 dyadic de Casteljau subdivision → control 全非负时调用已经形式化的 branch-free two-remainder consumer。coarse negative control 只能触发 subdivision/undecided，不得触发 rejection。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
