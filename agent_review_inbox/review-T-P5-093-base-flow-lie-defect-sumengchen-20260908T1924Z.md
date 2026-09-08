# review_result — T-P5-093 BASE-FLOW-LIE-DEFECT（苏梦辰 CI 修复闭环）

- source_agent: 苏梦辰
- task: `T-P5-093-BASE-FLOW-LIE-DEFECT`
- status: `compiled_candidate`
- upstream_math_agent: 红莲魔尊
- upstream_math_commit: `b1dbffc478d465b77e847468fa7527557b3bf4d0`
- sidecar: `examples/routeb_p5_base_flow_lie_defect_lean/`
- original_lean_commit: `96dc056533db218b0a99499b6c9a5888867c86fc`
- focused_verifier_commit: `73fcc3738dcd9893b791166c0ea3a4377f2a85e4`
- repair_commit: `9bad432167a2717543694846ce796a725d58f9d6`
- verified_checkout: `e77a4e7d54d58c871bc7633f1f1b1c3b7727c69b`
- registry_mutation: `false`

## 本轮真实 CI blocker 与修复

上一轮真实 GitHub Actions `34261723058 / 102181545777` 在
`examples/routeb_p5_base_flow_lie_defect_lean/P5BaseFlowLieDefect.lean:104`
失败。Lean 4.32 对

```lean
exact (mul_le_mul_left hnu_pos).mp hmul
```

的字段/API 推断没有得到预期的正标量乘法消去等价，报出：

```text
error(lean.invalidField): Invalid field mp: environment does not contain Function.mp
```

该错误导致 `base_flow_mixed_defect_invariant_boundary` 当轮未成功核验并出现 `sorryAx`。这是 Lean 4.32 proof transport blocker，不是数学 statement blocker。

修复 commit `9bad432167a2717543694846ce796a725d58f9d6` 只把最后一步改成显式反证：若 `dV>0`，由 `nu>0` 得 `0 < nu*dV`，与已得 `nu*dV ≤ 0` 矛盾。没有修改 theorem statement、hypotheses、常数、符号约定或数学强度。

## 当前 Lean theorem surface

本 sidecar 保持 8 个 exported theorem：

1. `base_flow_lie_defect_q2_identity`
2. `base_flow_lie_defect_rate_loss`
3. `base_flow_plus_variational_defect_rate`
4. `weighted_square_completion`
5. `base_flow_mixed_defect_energy`
6. `base_flow_mixed_defect_invariant_boundary`
7. `constant_metric_skew_base_defect_zero`
8. `dropping_metric_transport_of_base_defect_counterexample`

形式化边界仍是 exact-real / 2×2 algebraic-energy layer：整体 signed Lie-defect packet、`mu → mu-rho` rate loss、额外 variational defect 单独计费、weighted square completion、division-free mixed tube gate、skew/Killing 零代价，以及 `Db=0` 但 metric transport 不可省略的反例。

## 修复后的真实 focused CI

修复后真实 GitHub Actions：

- run: `34267716864`
- job: `102201324366`
- checkout: `e77a4e7d54d58c871bc7633f1f1b1c3b7727c69b`（包含 repair commit）

本 sidecar 的 focused 输出明确为：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_BASE_FLOW_LIE_DEFECT_FOCUSED_CHECK=PASS
SIGNED_LIE_DEFECT_ASSEMBLED=true
DOUBLE_COUNTING_AVOIDED=true
DIVISION_FREE_TUBE_GATE=true
DEPLOYED_SOURCE_BINDING=OPEN
FLOAT64_FD_CONTROLLER_SOLVE=OPEN
P8_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_base_flow_lie_defect_lean/verify.sh
```

8 个 exported theorem 的 `#print axioms` 均只含：

```text
[propext, Classical.choice, Quot.sound]
```

修复后本 sidecar 无 `sorryAx`。

运行依赖与固定版本来自仓库 pinned toolchain / manifest；本次 Actions 使用 Lean `4.32.0`、Lake `5.0.0-src+8c9756b`，mathlib revision `81a5d257c8e410db227a6665ed08f64fea08e997`，formal-math revision `795efb86f191735c5481675763537cfb4ff37e55`。`verify.sh` 继续从 PATH 获取 `lake/lean`，并支持 `CI_PORTABLE=1`。

## 聚合 workflow 与未覆盖接口

`portable-sidecars` 聚合 job 最终仍为红色，但失败来自其他既有、未由苏梦辰认领的 sidecar；T-P5-093 自身已在同一真实 job 中明确 `SIDECAR_RESULT=PASS`。本轮没有越权修改 FLT、M4、其他 P5、P7/P8 sidecar，也没有接手巨阳仙尊正在处理的 moving-chart Lie-defect child。

仍保持 OPEN：

- deployed source / same-domain binding；
- Float64 / finite-difference / controller / solve execution semantics；
- moving-chart naturality 的下游接口（由独立 child 处理）；
- P8 ODE continuation / flowpipe coverage。

不修改 theorem registry、主 DAG、整体状态或最终结论。

## 结论

`T-P5-093-BASE-FLOW-LIE-DEFECT` 现为 `compiled_candidate`。

**待封不觉独立验证 / 待梁智炜最终整合。**
