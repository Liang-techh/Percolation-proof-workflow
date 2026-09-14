# 苏梦辰 — P8 ramp interval-FTC import maintenance

- agent: 苏梦辰
- role: repository build/dependency/entrypoint/GitHub Actions maintenance
- status: repair committed; real CI revalidation in progress
- final integration: 待梁智炜（Codex）最终整合

## 触发的真实失败

默认分支此前 `Lean agent sidecars` run `34642161155`, job `103404664335`, step `Run portable agent sidecars` 中，`examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh` 以 `exit_code=1` 失败。artifact `portable-sidecars.log` 的实际诊断包括：

- `P8RampReconstruction.lean:127:20: error: expected token`
- `P8RampReconstruction.lean:123:13: error(lean.unknownIdentifier): Unknown identifier IntervalIntegrable`
- `P8RampReconstruction.lean:125:16: error(lean.unknownIdentifier): Unknown identifier intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le`
- `P8RampReconstruction.lean:147:20: error: expected token`

对应 focused command 由 verifier 实际执行：

```bash
cd examples/local_fkg
lake env lean -DwarningAsError=true ../routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean
```

仓库 pinned `examples/local_fkg/lake-manifest.json` 固定 Mathlib 为 `81a5d257c8e410db227a6665ed08f64fea08e997`。该版本中 `intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le` 定义于 `Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus`；旧 sidecar 仅导入 `Mathlib.Analysis.Calculus.MeanValue` 与 `Mathlib.Tactic`，因此 interval-integral API 与 notation 未进入环境。这是 import/dependency-closure 问题，不是数学 theorem statement 失败。

## 最小修复

修改路径：

- `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`

只新增：

```lean
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
```

未修改 theorem statement、hypotheses、proof gate、`warningAsError`、axiom audit、`sorry/admit` policy 或数学语义。

修复 commit：`1deae47ae56a97299d8752481a55f2dbdca92b81` (`fix(ci): import interval FTC for P8 ramp sidecar`).

## 真实 CI 再验证

该 commit 已触发：

- `Lean agent sidecars` run `34707536760`
- job `103590202954` (`portable-sidecars`)
- 当前 setup、repository checkout、formal-math checkout、Anthropic FLT checkout、Mathlib compatibility checkout、Elan、pinned local-FKG bootstrap、FLT provenance validation、Mathlib compatibility bootstrap 均已真实 PASS。
- step 10 `Run portable agent sidecars` 当前正在执行；因此本记录不宣称 focused compile/axiom PASS。

同时触发：

- `Workflow tests, Harris replay, and local-FKG verification` run `34707536598`，当前执行中。

## 仍失败/不越权项

旧 aggregate log 中 BODY6 `hBudget : cap + shiftB ≤ bar` vs `shiftB + cap ≤ ...`、以及其他 sidecar 的 Lean proof/type/linter failures 仍属于各自 theorem/Lean lane；本维护没有通过降低 gate 或删除检查来掩盖它们。

下一轮优先读取 run `34707536760` 的真实 artifact/job log：若 P8 ramp focused verifier PASS，则将本 import-closure blocker 标为已闭环；若出现新的具体 compile 诊断，则只做最小兼容修复。

结论：仓库级 import fix 已提交，真实 CI 尚在运行；仓库能编译该 seam 不等于 P8/Route-B 证明完成。待梁智炜（Codex）最终整合。
