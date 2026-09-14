# 苏梦辰 — BODY6 consumer audit import-closure maintenance

- agent/source_agent: 苏梦辰
- scope: 仓库级构建/入口脚本/GitHub Actions 可运行性维护；未修改数学 theorem statement、hypotheses 或整体结论。
- status: repair 已提交；最终 focused CI 仍待真实 Actions 完成，本文不宣称 PASS。

## 真实失败链

1. `Lean agent sidecars` run `34524301934`, job `103029713632`, `Run portable agent sidecars`：
   - `NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean:1:0`: `unknown module prefix 'ActualStorage'`
   - 同文件 line 2: `unknown module prefix 'ActualShift'`
   - 两个 BODY6 consumer audit 在有效 theorem audit 前退出，随后 `AXIOM_AUDIT=FAIL` / `SIDECAR_RESULT=FAIL`。
   - 根因属于 verifier staging：临时 `LEAN_PATH` 只含 consumer，没有 repository-local transitive imports 的已编译模块。

2. 首轮递归 staging 后，run `34638549103`, job `103392618905` 暴露两个脚本级问题：
   - `ReferenceMass.lean` authoritative source 与 `snapshots/.../ReferenceMass.lean` 被同时发现；ambiguity 状态又被误当 external import。
   - pathcap verifier 用 `-o="$olean"`，Lean 把输出路径解析为以 `=` 开头的文件，报 `failed to write '=...olean': No such file or directory`，exit 2。

3. 修正 snapshot/output pruning、ambiguity status propagation 与 `lean -o "$olean"` 后，run `34640170667`, job `103398057730` 继续深入真实 import closure，新的仓库级 blocker 为：
   - `ambiguous repository module source for ChristoffelPower`
   - candidates:
     - `examples/routeb_christoffel_power/ChristoffelPower.lean`
     - `examples/routeb_p5_christoffel_power_sidecar/ChristoffelPower.lean`
   - `SignedGap.lean` 实际消费 `RouteBChristoffelPower.christoffelTwoChannelBound`，因此这一 closure 语义上要求前者；P5 文件使用独立 namespace `RouteBP5ChristoffelPower`。

## 本轮维护修改

- `examples/routeb_body6_aligned_consumer_audit/verify.sh`
  - commit `cce19212a9973ff62730fcd5325e34d7f2b03b70`
  - 为 `ChristoffelPower` 增加唯一、注释明确的 authoritative source override：`examples/routeb_christoffel_power/ChristoffelPower.lean`。
  - 其它 duplicate module name 继续 hard-fail，不做任意选择。

- `examples/routeb_body6_aligned_pathcap_consumer_audit/verify.sh`
  - commit `88533c339fdc5e74959326852f22b16763b162fd`
  - 同样加入 exact `ChristoffelPower` source binding。
  - 保持实际目标 theorem：
    - `NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.consume_aligned_path_cap_attempt`
    - `NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.source_full_cap_does_not_pay_shift_attempt`

保留所有 `-DwarningAsError=true`、placeholder scan、`#print axioms` 与 `sorryAx` gate；未关闭测试、未降级 warning/error gate、未加入 `sorry/admit`、未伪造 PASS。

## 当前真实 CI

最终脚本 head `88533c339fdc5e74959326852f22b16763b162fd` 已触发 `Lean agent sidecars` run `34642161155`, job `103404664335`。截至本文写回时：repository checkout、formal-math、Anthropic FLT、Mathlib compatibility checkout、Elan、pinned local-FKG bootstrap 与 FLT provenance 已真实成功；当前停在 `Bootstrap pinned Mathlib compatibility environment`，`Run portable agent sidecars` 尚未开始。因此 BODY6 focused compile/axiom 状态仍为 **pending**，不得写作成功。

同一 head 的主 workflow `Workflow tests, Harris replay, and local-FKG verification` 也已触发；最终结论待真实 run 完成。

## 可复现入口

```bash
CI_PORTABLE=1 examples/routeb_body6_aligned_consumer_audit/verify.sh
CI_PORTABLE=1 examples/routeb_body6_aligned_pathcap_consumer_audit/verify.sh
```

## 剩余边界

aggregate portable-sidecars 中仍有多个独立 Lean proof/type/`sorryAx` failure（P5 center-bias/base-gradient/observable-tail，P4 rational bridges/product-domain/fraction wiring，P8 interval-flow/forward-invariant 等）。这些不通过削弱仓库 gate 掩盖；若属于已认领 Lean proof seam，则留给对应形式化 Agent。

仓库能跑不等于证明完成；不宣称最终整合，不修改整体数学结论。待梁智炜最终整合。
