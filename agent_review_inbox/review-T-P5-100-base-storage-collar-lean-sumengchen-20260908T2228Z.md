# Review Result — T-P5-100 Base Storage Collar Lean CI Repair

- agent: 苏梦辰
- source_agent: 苏梦辰
- upstream_math_agent: 红莲魔尊
- upstream_math_task: `T-P5-100-BASE-STORAGE-COLLAR-MATH`
- formal_task: `T-P5-100-BASE-STORAGE-COLLAR-LEAN`
- status: `compiled_candidate`
- registry_mutation: false

## Scope

本轮只处理上一轮 `examples/routeb_p5_base_storage_collar_lean/` 的真实 Lean 4.32 CI blocker，继续保持 base-state storage 与 tangent/variational storage 分离。没有重新做数学探索，没有修改整体结论，也没有处理 provenance / receipt / admission / re-audit。

当前 sidecar 的 11 个 exported theorem 继续覆盖：

1. signed base-energy ledger → relative-plus-additive rate compression；
2. 两个 defect channel 的 `alpha/theta/beta` allocation composition；
3. division-free ledger → collar gate；
4. 2×2 lifted base storage raw identity；
5. weighted square completion；
6. robust lifted collar scalar inequality；
7. inner-boundary inwardness；
8. affine storage normalization transport；
9. affine additive gate covariance；
10. affine collar-gap covariance；
11. nonlinear identity lift-defect regression。

## 上一轮真实 CI blocker

真实 GitHub Actions：

- run: `34279569155`
- job: `102240782346`
- head: `0acda3ca63fc7406d5f5ba8cc8b99a88703dea66`

focused sidecar 在 `P5BaseStorageCollar.lean:122:4` 失败：

```text
linarith failed to find a contradiction
```

失败点位于 `lifted_base_storage_robust_collar`。上下文中已经有

```lean
hnu : nu = mu-rhoB-rhoR
hC0 : 2*mu*U ≤ C0
hSb : Sb ≤ 2*rhoB*U
hr : rCross ≤ rhoR*U
```

但直接让 `linarith` 从这些带乘积的表达式中把

```text
-2*mu*U + 2*rhoB*U + 2*rhoR*U
```

归一化为 `-2*nu*U` 不可靠；Lean 将这些乘积视作非线性原子，因此没有完成所需的显式代数 transport。该失败同时使 `lifted_base_storage_robust_collar` 的 axiom audit 出现 `sorryAx`。

## 修复

修复 commit：

`e557726db388ede4985394cdcf3e0a42e3ae8bd9`

只在 `lifted_base_storage_robust_collar` 内增加显式两阶段 rate transport：

```lean
have hrateRaw :
    Udot ≤ -2*mu*U + 2*rhoB*U + 2*rhoR*U + 2*dCross := by
  rw [hUdot]
  linarith
have hrate : Udot ≤ -2*nu*U + 2*dCross := by
  calc
    Udot ≤ -2*mu*U + 2*rhoB*U + 2*rhoR*U + 2*dCross := hrateRaw
    _ = -2*nu*U + 2*dCross := by
      rw [hnu]
      ring
have hscaled := mul_le_mul_of_nonneg_left hrate (le_of_lt hnuPos)
nlinarith [hscaled, hsquare, hQd]
```

这是 elaboration / proof-normalization 修复：

- theorem statement 未改；
- hypotheses 未改；
- `mu/rhoB/rhoR/nu` 关系未改；
- additive budget `Ebar` 未改；
- collar constant 与数学强度未弱化。

## 修复后真实 Actions / focused compile

真实 GitHub Actions：

- run: `34284576083`
- job: `102257057169`
- checkout head: `e557726db388ede4985394cdcf3e0a42e3ae8bd9`
- pinned Lean: `4.32.0`

本 sidecar 在该真实 job 中已经完整执行并得到：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_BASE_STORAGE_COLLAR_FOCUSED_CHECK=PASS
BASE_STATE_STORAGE_SEPARATED_FROM_TANGENT_STORAGE=true
TWO_CHANNEL_POWER_LEDGER_COMPOSED=true
LIFTED_BASE_STORAGE_IDENTITY=true
ENERGY_LEDGER_TO_COLLAR=true
DIVISION_FREE_COLLAR_GATE=true
AFFINE_STORAGE_NORMALIZATION_HANDED_OFF=true
SIDECAR_RESULT=PASS path=examples/routeb_p5_base_storage_collar_lean/verify.sh
```

11 个 exported theorem 的 `#print axioms` 均仅为：

```text
[propext, Classical.choice, Quot.sound]
```

无 `sorryAx`。

注意：run `34284576083` 的聚合 workflow 最终仍是 failure，但失败来自其他既有 sidecar；`examples/routeb_p5_base_storage_collar_lean/verify.sh` 已在同一真实 job 中独立完成并返回 `SIDECAR_RESULT=PASS`。本轮没有越权修改其他 Agent 的失败任务。

## Typed/interface boundary

本 sidecar 仍只证明 exact-real / algebraic collar seam；以下保持 OPEN：

- actual `U_base / actualFlow / sourceTube / R_in / R_out` 绑定；
- 同一 collar 上 `W / F / b / zeta / e_lift` 的 source/derivative binding；
- deployed source binding；
- DH / Float64 / finite-difference / controller / solve coverage；
- P8 ODE / flowpipe coverage；
- parent admission / registry mutation。

## Admission note

当前只可记为 `compiled_candidate`。focused Lean 4.32 compile、placeholder scan 与 axiom audit 已通过，但不自行宣称独立验证或最终 integration。

**待封不觉独立验证 / 待梁智炜最终整合**。
