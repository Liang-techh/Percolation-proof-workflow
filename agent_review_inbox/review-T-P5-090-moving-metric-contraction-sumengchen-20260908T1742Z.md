# review_result — T-P5-090 moving-metric contraction

- task: `T-P5-090`
- agent: `苏梦辰`
- source_agent: `苏梦辰`
- math_source_agent: `古月方源 (Fang Yuan Gu)`
- math_source_commit: `8a3e0f3909e82f359131945aa845b033053f28b2`
- initial_sidecar_commit: `a5c9020bfe61aeac237cf331359476f3bc730ea2`
- lean_fix_commit: `bc652b46d32fd7d65d0956f64c9bf928a2c87a70`
- sidecar: `examples/routeb_p5_moving_metric_contraction_lean/`
- status: `compiled_candidate`
- registry_mutation: `false`

## 本轮形式化边界

本轮只形式化古月方源已经给出的 moving-metric / moving-affine-chart 数学结构，不重新做大规模数学探索，也不做 provenance / receipt / admission / re-audit。Lean child 被拆成 exact-real 2×2 最小接口，重点保留 moving metric 的 material derivative 与 moving frame connection，避免把移动坐标误当成 frozen metric。

已核化的 exported theorem 共 7 个：

1. `RouteBP5MovingMetricContraction.pullback_quadratic_eq_bilinear`
   - 2×2 对称二次型在 affine chart pullback 下与对应 bilinear 表达严格一致。
2. `RouteBP5MovingMetricContraction.physical_variation_rate_identity`
   - physical variation rate 显式包含 metric material derivative；将其整理成 contraction tensor 的负号形式。
3. `RouteBP5MovingMetricContraction.moving_metric_contraction_tensor_congruence`
   - moving-chart contraction tensor 与 physical contraction tensor 的 exact congruence。
4. `RouteBP5MovingMetricContraction.contraction_rate_pullback`
   - exact coordinate pullback 下 contraction numerator/rate 传输。
5. `RouteBP5MovingMetricContraction.normalized_rate_of_congruence`
   - 不依赖矩阵求逆的 forward normalized-rate transport；保留同一 contraction rate。
6. `RouteBP5MovingMetricContraction.dropping_material_metric_derivative_counterexample`
   - 显式反例：若漏掉 `dot W` / material metric derivative，会改变 contraction 判定，因此该项不能被 checker 静默删除。
7. `RouteBP5MovingMetricContraction.moving_affine_chart_material_cancellation`
   - moving affine chart 的 material/connection 项按数学输入中的结构进行精确抵消，防止 frozen-chart 误用。

形式化 statement 只承诺 exact-real 2×2 algebra 与 forward transport；没有把尚未完成的 differential covariance 推导、deployed source execution 或 ODE coverage 偷渡成 hypothesis-free theorem。

## 真实 Lean / CI 闭环

### 第一次 Actions：真实 blocker

- run: `34255966264`
- job: `102161727581`
- head: `a5c9020bfe61aeac237cf331359476f3bc730ea2`
- 环境：Lean `4.32.0`，Lake `5.0.0-src+8c9756b`，使用仓库 pinned `lean-toolchain` / `lake-manifest.json` 路径。

本 sidecar 真实失败点为：

```text
examples/routeb_p5_moving_metric_contraction_lean/P5MovingMetricContraction.lean:100:2:
error: No goals to be solved
```

原因是 `physical_variation_rate_identity` 中 `rw [hdV]; simp [...]; ring` 在 Lean 4.32 下前一步已经关闭目标，后续 tactic sequencing 被判为错误。这是 proof sequencing / normalization blocker，不是数学 statement 失败。

### 修复

commit `bc652b46d32fd7d65d0956f64c9bf928a2c87a70` 将该处改为显式 `calc` transport：先使用 `hdV`，再用 ring 整理负号，最后通过 definitional equality 回到 `physicalContractionQ2`。没有修改 theorem statement、hypotheses、数学常数或结论强度。

### 第二次 Actions：focused PASS

- run: `34257095178`
- job: `102165539112`
- head: `bc652b46d32fd7d65d0956f64c9bf928a2c87a70`

本 sidecar 在真实 GitHub Actions 中明确输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_MOVING_METRIC_CONTRACTION_FOCUSED_CHECK=PASS
EXACT_REAL_2X2_ALGEBRA=true
MATERIAL_METRIC_TERM_RETAINED=true
MOVING_FRAME_CONNECTION_RETAINED=true
SAME_CONTRACTION_RATE=true
DIVISION_FREE_FORWARD_TRANSPORT=true
DIFFERENTIAL_COVARIANCE_DERIVATION=OPEN
DEPLOYED_SOURCE_BINDING=OPEN
FLOAT64_FD_CONTROLLER_SOLVE=OPEN
P8_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_moving_metric_contraction_lean/verify.sh
```

## axiom 状态

7 个 exported theorem 的 `#print axioms` 均只出现：

```text
[propext, Classical.choice, Quot.sound]
```

本 sidecar 当前无 `sorryAx`。

## 依赖与接口边界

数学依赖是 T-P5-090 给出的 moving metric `W(q)`、affine chart `J(q)`、material derivative packet 与 moving-frame connection identity；与此前 similarity-normalization / moving-frame transport 层接口相容，但本 sidecar 没有擅自把它们升级为 deployed source certificate。

仍保持 OPEN：

- `DIFFERENTIAL_COVARIANCE_DERIVATION=OPEN`：从实际 differentiable `J(q), W(q)` 与 vector field 自动推出本轮 algebra packet 的微分层桥接；
- `DEPLOYED_SOURCE_BINDING=OPEN`：真实 source/Jacobian/metric packet 的同域绑定；
- `FLOAT64_FD_CONTROLLER_SOLVE=OPEN`：Float64、finite-difference、controller、solve execution semantics；
- `P8_ODE_COVERAGE=OPEN`：同域 ODE continuation / flowpipe coverage。

聚合 `portable-sidecars` workflow 仍为红色，但真实日志显示本 T-P5-090 focused path 已独立通过；聚合失败来自其他既有未认领 sidecar，本轮未越权抢修，也未据此修改整体 DAG / registry / 最终结论。

**当前仅标记 `compiled_candidate`：待封不觉独立验证 / 待梁智炜最终整合。**
