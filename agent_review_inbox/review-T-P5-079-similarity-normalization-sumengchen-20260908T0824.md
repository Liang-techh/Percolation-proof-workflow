---
kind: review_result
task_id: T-P5-079-SIMILARITY-NORMALIZATION
agent: 苏梦辰
source_agent: 苏梦辰
math_source_agent: 柳冠一
created_at: 2026-09-08T08:24:00-06:00
status: compiled_candidate
integration_owner: 梁智炜
independent_verifier: 封不觉
---

# 苏梦辰 review — T-P5-079 similarity normalization Lean child

## 结论

已把柳冠一 `T-P5-079-SIMILARITY-NORMALIZATION` 中已有实质数学推导拆成一个 source-independent、2×2 real symmetric metric + diagonal affine chart 的最小 Lean sidecar，并在仓库 pinned Lean 4.32 / `examples/local_fkg/lake-manifest.json` 环境中取得真实 GitHub Actions focused compile + axiom PASS。

本结果仅为 `compiled_candidate`。**待封不觉独立验证 / 待梁智炜最终整合**。不修改 parent 状态、DAG/registry/admission 或整体结论。

## 数学输入

来源：柳冠一 `agent_review_inbox/review-T-P5-079-similarity-normalization-liuguanyi-20260908T0806.md`。

本轮只消费其已经给出的 affine/diagonal similarity algebra，不重新做 source/provenance 数学探索。形式化边界固定为：

- affine chart 的平移项只在 corrector conjugacy 中出现并精确消去；
- linear scaling 取 `S = diag(s1,s2)`；
- metric 是一般 symmetric 2×2 weight，允许非零 cross entry；
- residual/state difference 采用同一个 covariant transport；
- Jacobian 只要求 multiplication-only action intertwining `J_x S v = S J_z v`，不在首个 receipt 中引入矩阵逆、导数 API 或 set-image API。

## Lean sidecar

路径：`examples/routeb_p5_similarity_normalization_lean/`

文件：

- `P5SimilarityNormalization.lean`
- `README.md`
- `verify.sh`
- `lean-toolchain`

相关提交：

- claim: `8dbc4a18df37cea150aac42191ffb2837e8ba6d1`
- Lean core: `0ff1b59ea2c45a59a09a61462add73f4cc5493c6`
- toolchain pin: `ae27ea34b7e5b3ddd082678469597db408481250`
- README: `242a7957a363b987bb7d7887bfe1f14c61760f63`
- portable verifier: `d4b4550b468d16baea8681fbc1a383828df66083`

`verify.sh` 从 `PATH` 查找 `lake` / `lean`，默认复用仓库 `examples/local_fkg` 的 pinned Lake environment，检查 toolchain 一致、`lake-manifest.json` 存在、placeholder scan、warnings-as-errors compile 以及 exported theorem 的 `#print axioms`，并拒绝 `sorryAx`。脚本带 `CI_PORTABLE=1` seam，可被 `.github/workflows/lean-agent-sidecars.yml` 自动发现。

## Kernel theorem decomposition

当前导出 10 个 theorem：

1. `quadraticForm_congruence`
   - 对一般 symmetric 2×2 metric 精确核化 diagonal congruence `W_z = Sᵀ W_x S` 的 quadratic-form identity。

2. `bilinear_congruence`
   - 上述 congruence 的 bilinear companion。

3. `strongMonotone_similarity_iff`
   - 若 state/residual differences 共同按同一 diagonal chart covariantly transport，则 pointwise strong-monotonicity inequality 在两个坐标系严格等价，数值常数 `mu` 不变。

4. `sqLipschitz_similarity_iff`
   - 同样严格 transport squared-Lipschitz gate，数值常数 `Lambda` 不变。

5. `corrector_step_similarity`
   - 精确证明 affine damped-corrector conjugacy；平移项消去，scalar step `h` 不重标定。

6. `jacobian_sym_congruence`
   - 在 source-facing multiplication-only premise `J_x S v = S J_z v` 下，T-P5-074 型 symmetric Jacobian quadratic packet 按同一 congruence transport。

7. `jacobian_gram_congruence`
   - 同 premise 下，T-P5-076 型 weighted Jacobian Gram quadratic packet 按同一 congruence transport。

8. `frozen_metric_monotonicity_counterexample`
   - 核化柳冠一的 exact rational obstruction：`J_x=[[1,1],[-1,1]]`, `S=diag(3,1)` 时，若归一化后错误冻结 metric 为 Euclidean `I`，方向 `(1,1)` 的 symmetric quadratic 精确等于 `-4/3`。

9. `transported_metric_sym_regression`
   - 使用正确 transported metric `diag(9,1)` 时，上述 normalized Jacobian 的 symmetric packet 精确恢复为 `2 * qform`。

10. `transported_metric_gram_regression`
    - 同一例子 weighted Gram packet 也精确恢复为 `2 * qform`。

这些 theorem 明确防止 checker 把“状态缩放了但 metric/Jacobian contract 没有一起缩放”的错误实现当作等价 normalization。

## 真实 GitHub Actions / focused compile

首个真正跑完本 sidecar 的 Actions：

- workflow run: `34237227667`
- job: `102098140421`
- checked-out head: `1f7592f29f9bec8e29b689db30c416b6655dcff6`
- runner: Ubuntu 24.04
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 的真实日志明确输出：

```text
Running examples/routeb_p5_similarity_normalization_lean/verify.sh
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_SIMILARITY_NORMALIZATION_FOCUSED_CHECK=PASS
GENERAL_SYMMETRIC_METRIC_2X2=true
DIAGONAL_AFFINE_CHART=true
SAME_MU_LAMBDA=true
SAME_CORRECTOR_STEP=true
JACOBIAN_ACTION_INTERTWINING=true
WRONG_METRIC_COUNTEREXAMPLE=true
ARBITRARY_MATRIX_GENERALIZATION=OPEN
DEPLOYED_SOURCE_CHART_BINDING=OPEN
FLOAT64_FD_CONTROLLER_SOLVE=OPEN
P8_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_similarity_normalization_lean/verify.sh
```

10 个 exported theorem 的 `#print axioms` 均只有：

```text
[propext, Classical.choice, Quot.sound]
```

无 `sorryAx`。

本轮在该 sidecar 上没有出现 theorem-level compile failure，因此无需弱化 statement 或做数学修补。此前若干 workflow run 因 repository concurrency 的 `cancel-in-progress: true` 被后续 push 取消，那是调度取消，不是 Lean compile blocker；上述 run/job 已真实完成本 sidecar focused path。

## 聚合 workflow 红色边界

`portable-sidecars` aggregate job 仍为 failure，但真实日志显示本 sidecar 自身已 PASS；红色来自其他既有/未认领 sidecar，例如 FLT quotient path、M4 cross-branch、旧 P5 componentwise/direct-two-channel/parameter-tube/weighted-dual、P7 tail-Schur、旧 P8 ramp-reconstruction 等。本轮没有越权抢修，也不把 aggregate red 归因于 T-P5-079。

## 依赖与剩余形式化问题

当前 Lean child 只证明 source-independent local algebra。仍需由后续 source/coverage 层提供：

- deployed concrete affine chart `c,S`（若 checker 真正需要 inverse，则另给 pinned `S⁻¹` / nonzero-scale certificate）；
- physical source residual covariance，与 normalized residual 的同 key / 同 cell binding；
- concrete Jacobian action intertwining `J_x S v = S J_z v`，不能只凭矩阵名字假定；
- forward/backward domain mapping、source box / tube / flowpipe 的同域 coverage；
- 若未来需要 arbitrary invertible non-diagonal `S`，可另拆 general Matrix child，本轮不为未使用接口增加依赖；
- true-DH / Float64 / FD / controller / solve execution semantics；
- P8 ODE continuation / same-domain trajectory coverage。

因此本轮没有 source admission、receipt registration、DAG/registry mutation 或 parent closure。

## 状态

`compiled_candidate` — **待封不觉独立验证 / 待梁智炜最终整合**。
