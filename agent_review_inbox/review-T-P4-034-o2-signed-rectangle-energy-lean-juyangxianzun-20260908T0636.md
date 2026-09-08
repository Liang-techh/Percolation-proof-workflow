# Review result — T-P4-034 O2 signed-rectangle energy Lean sidecar

- task_id: `T-P4-034`
- agent: `巨阳仙尊`
- source_agent: `巨阳仙尊`
- math_source: `agent_review_inbox/review-T-P4-034-honglianmozun-20260908T0558.md`
- status: `compiled_candidate`
- final_integration: `false`
- registry_mutation: `false`

## 本轮形式化范围

新增 portable sidecar：

- `examples/routeb_p4_o2_signed_rectangle_energy_lean/O2SignedRectangleEnergyConsumer.lean`
- `examples/routeb_p4_o2_signed_rectangle_energy_lean/README.md`
- `examples/routeb_p4_o2_signed_rectangle_energy_lean/verify.sh`
- `examples/routeb_p4_o2_signed_rectangle_energy_lean/lean-toolchain`

实现的是红莲魔尊 T-P4-034 数学结果中的 **source-independent exact-real consumer**，不重做 dhport/Float64/source provenance。核心定义为

`D_H(x,y)=p x^2+2qxy+s y^2`

与 adjugate charge

`N_H(e4,e5)=s e4^2-2q e4 e5+p e5^2`。

在 `p>0`、`Δ=ps-q^2>0` 下，Lean kernel 验证 division-free completion：

`4*theta*Δ*(-theta*D_H(x,y)-(e4*x+e5*y)) <= N_H(e4,e5)`。

因此，只要实际 evaluator error 已经是与 energy pairing 相同的 **force/residual coordinates**，且其 signed rectangle 四角全部满足

`N_H(corner) <= 4*theta*Δ*kappa`，

则得到

`-D_H + errorPower <= -(1-theta)*D_H + kappa`。

另有 first-exit seam：若 `theta<=1` 且 `kappa < c*Vstar-beta`，则在 `V=Vstar` 的 ledger 上推出 `Vdot<0`。

## theorem decomposition

本 sidecar 公开 15 个 theorem：

1. `second_diagonal_pos`
2. `energy_sos_identity`
3. `energy_quadratic_nonnegative`
4. `dual_sos_identity`
5. `dual_quadratic_nonnegative`
6. `retained_dissipation_completion_identity`
7. `o2_error_power_retained_dissipation_completion_2x2`
8. `quadratic_interval_le_endpoints`
9. `dual_quadratic_rectangle_le_corners`
10. `o2_signed_rectangle_energy_consumer`
11. `o2_signed_rectangle_first_exit_with_reserve`
12. `global_sign_dual_invariant`
13. `global_sign_rectangle_transport`
14. `absolute_bias_small_scale_identity`
15. `absolute_evaluator_bias_blocks_homogeneous_decay`

其中 `dual_quadratic_rectangle_le_corners` 保留 signed interval correlation：不先把 `e4,e5` 各自粗化为 absolute maxima，而是直接核四个有符号角。

同时建立了 `AccelerationError2` 与 `ForceResidualError2` 两个不同 wrapper，且**故意不提供 coercion**。因此 solve/acceleration error 不能静默喂给 O2 energy consumer；source lane 必须先给 same-box acceleration→force/residual bridge。

`absolute_evaluator_bias_blocks_homogeneous_decay` 只接受显式 small-scale gap `t*D_H(e)<|e|^2`；它核验固定 affine bias 在缩放状态上可以压过二次耗散，防止把 state-independent nonzero error rectangle 错报为穿过原点的 homogeneous decay certificate。

## 数学 → Lean → CI → 修复 → 再 Lean

### 初始实现

初始 sidecar commit：

`386af4afa98643e34d23aadbf1fd9b02b834bae9`

真实 GitHub Actions：

- run: `34225256143`
- job: `102057774283`
- Lean: `4.32.0`
- Lake: `5.0.0`

该 run 在本 lane 暴露了真实 Lean blocker：`dual_quadratic_rectangle_le_corners` 中直接 `apply quadratic_interval_le_endpoints` 时，opaque `dualQuadratic` 目标无法与展开后的 scalar polynomial conclusion unification；同一轮 `-DwarningAsError=true` 还报告 obstruction theorem 的两个多余 hypothesis `hD/hnorm`。因此依赖该 rectangle theorem 的三个公开 theorem 当时出现 `sorryAx`，本 lane 正确失败，没有把失败包装成 PASS。

### 修复

main 修复 commit：

`20f7c18520148b16f4e9223fc029b38ff60de534`

修复内容：

- 不弱化 four-corner theorem；把每个单变量 convex-quadratic transport 先落到显式 polynomial helper，再 `simp only [dualQuadratic]` + `nlinarith` 回到抽象定义；
- 删除 obstruction theorem 中确实不参与 proof term 的冗余 `hD/hnorm`，保留真正需要的 `ht` 与 `hsmall`；
- 未改变 O2 energy charge、signed rectangle gate、first-exit reserve 或 typed coordinate boundary。

为避免 main 上其他 Agent 高频 push 造成 concurrency cancellation，另在隔离 CI branch `ci/juyangxianzun-t-p4-034` 上复现同一修复；repaired branch head：

`5072faeb068e9e94eb11ac98b45a76932ed3ae64`

真实 GitHub Actions：

- run: `34226369435`
- job: `102061381647`
- checkout head: `5072faeb068e9e94eb11ac98b45a76932ed3ae64`
- Lean: `4.32.0`
- Lake: `5.0.0`

本 lane 在该 runner 上于后续 branch push 导致整个 shared job 被取消**之前已经完整执行结束**，明确输出：

- `PLACEHOLDER_SCAN=PASS`
- `AXIOM_AUDIT=PASS`
- `P4_O2_SIGNED_RECTANGLE_ENERGY_FOCUSED_CHECK=PASS`
- `FOUR_CORNER_DIVISION_FREE_GATE=true`
- `SIGNED_INTERVAL_CORRELATION_PRESERVED=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p4_o2_signed_rectangle_energy_lean/verify.sh`

15 个公开 theorem 的 `#print axioms` 在该 pinned runner 上全部只显示：

`[propext, Classical.choice, Quot.sound]`

本 lane **无 `sorryAx`**。

shared workflow 中仍存在其他历史独立 sidecar 的 compile failure；本轮没有越权修改那些 lane，也不将 shared job 的整体颜色用于替代 T-P4-034 自身的 focused evidence。

## Portable CI contract

`verify.sh`：

- 带 `CI_PORTABLE=1`；
- 从 `PATH` 查找 `lake`/`lean`，不含本机专属绝对路径；
- 要求 `examples/local_fkg/lake-manifest.json`；
- sidecar `lean-toolchain` 固定 `leanprover/lean4:v4.32.0` 并与 local_fkg pin 比较；
- 使用 `lake env lean -DwarningAsError=true`；
- placeholder scan + 15 theorem `#print axioms` + `sorryAx` audit。

## 仍然开放 / 不得误报关闭

- deployed `dhport_lib.jl` 最终 evaluator residual signed rectangle source binding；
- Float64/libm/central-FD/regularizer/linear solve semantics；
- solve/acceleration error → force/residual coordinate 的 same-box bridge；
- singular-rank / kernel compatibility branch；
- P8 same-domain ODE/flowpipe coverage；
- concrete P4 coefficient/hash/orientation binding；
- P4/M4 final closure；
- registry/admission/provenance mutation。

因此当前结论严格仅为 `compiled_candidate`，不是最终集成结果。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
