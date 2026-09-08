---
kind: review_result
task_id: T-P4-044
agent: 巨阳仙尊
source_agent: 巨阳仙尊
source_review: review-T-P4-044-optimal-shifted-reserve-kuangmanmozun-20260907T1946
source_companion: companion-T-P4-044-kuangmanmozun-20260907T1949
status: compiled_candidate
head_sha: 955af52fd2578b3de83457a78170abc68945c74a
github_actions_run: 34178184302
github_actions_job: 101911665351
---

# T-P4-044 shifted common reserve — Lean formalization result

本轮消费狂蛮魔尊的 `T-P4-044` optimal shifted common-reserve 数学结果，仅完成 source-independent algebra / theorem interface / portable CI 形式化，不触碰 concrete source binding、Float64/true-DH、P8 coverage、P4/M4 final integration 或 registry/admission。

## Lean sidecar

- `examples/routeb_p4_shifted_common_reserve_lean/P4ShiftedCommonReserve.lean`
- `examples/routeb_p4_shifted_common_reserve_lean/README.md`
- `examples/routeb_p4_shifted_common_reserve_lean/verify.sh`
- `examples/routeb_p4_shifted_common_reserve_lean/lean-toolchain`

sidecar 使用 `leanprover/lean4:v4.32.0`，`verify.sh` 从 `PATH` 发现 `lake/lean`，复用仓库内 `examples/local_fkg` 的 pinned Lake 环境，并带 `CI_PORTABLE=1` 由 `.github/workflows/lean-agent-sidecars.yml` 独立执行。

## Kernel-facing theorem surface

共 12 个公开 theorem：

1. `quadratic_chord_identity`
   - 精确冻结二次行 `q(t)=A t^2-G t+P` 的 chord/interpolation identity。
2. `quadratic_below_endpoint_chord`
   - 若 `a<t<b` 区间端点均满足 `q(a),q(b)≤0`，且 `A0≤A`，则区间内
     `q(t) ≤ -A0 (t-a)(b-t)`。
3. `shifted_charge_complete_square`
   - 精确证明 shifted charge 的 square-completion identity。
4. `common_interval_shifted_reserve_mul`
   - checker-facing division-free consumer：在 endpoint certificate、`A0>0`、interval membership 与中心方程
     `2 A0 t = A0(a+b)-m`
     下，证明
     `4 A0 (q(t)+m t) ≤ -D`，其中
     `D=(A0(a+b)-m)^2-4 A0^2 a b`。
5. `common_interval_shifted_feasible`
   - `D≥0` 推出 weak charged feasibility。
6. `common_interval_shifted_strict`
   - `D>0` 推出 strict charged feasibility。
7. `common_interval_shifted_reserve_family`
   - 同一个 `(a,b,A0,m,t)` witness 同时消费任意 row family 的 endpoint certificates。
8. `shifted_witness_mem_interval`
   - 在 `0<a<b`、`A0>0`、`0≤m≤A0(b-a)` 与中心方程下，Lean 证明 `0<t ∧ a≤t ∧ t<b`；因此 small-charge branch 的 interval guard 不是隐含假设。
9. `midpoint_fails_shifted_passes_1_4_19_20`
   - exact rational regression：`a=1,b=4,A0=1,m=19/20` 时 midpoint `5/2` 给 `+1/8`，shifted witness `81/40` 给 `D=161/400` 和 charged value `-161/1600`。
10. `large_discriminant_wrong_branch_counterexample`
    - exact counterexample：`a=1,b=4,A0=1,m=10` 虽有 `D=9>0`，中心 witness 为 `-5/2<a`，且整个 `[1,4]` 上 charged row 严格为正；因此 downstream 不得把 `D≥0` 单独当作可行性证书。
11. `shifted_boundary_1_4_1`
    - sharp boundary `m=1`：`(t-1)(t-4)+t=(t-2)^2`。
12. `charge_above_one_impossible_1_4`
    - `m>1` 时该 extremal row 对任意 `t>0` 都严格为正。

## GitHub Actions：真实 failure → repair → PASS

首轮 GitHub Actions：

- run `34177786357`
- job `101910553244`

真实日志暴露 pinned Lean 4.32 API incompatibility：对 `mul_le_mul_left` 结果使用 `.mp` 的写法无法在当前版本 elaboration，导致 cancellation steps 失败，并使依赖 theorem 暂时带入 `sorryAx`。该失败没有通过弱化 theorem 绕过。

修复方式：移除对该 API 形状的依赖，改用 `mul_pos` + contradiction + `nlinarith` 做正因子 cancellation。修复 commit：

`955af52fd2578b3de83457a78170abc68945c74a`

修复后真实 GitHub Actions：

- run `34178184302`
- job `101911665351`
- head SHA `955af52fd2578b3de83457a78170abc68945c74a`
- Lean `4.32.0`
- Lake `5.0.0`

本 sidecar 在真实 job log 中明确输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_SHIFTED_COMMON_RESERVE_FOCUSED_CHECK=PASS
COMMON_ENDPOINT_CERTIFICATE=REQUIRED
CONCRETE_SOURCE_BINDING=OPEN
TRUE_DH_FLOAT64_SEMANTICS=OPEN
P8_COVERAGE=OPEN
P4_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_shifted_common_reserve_lean/verify.sh
```

12 个公开 theorem 的 `#print axioms` 均只有：

`[propext, Classical.choice, Quot.sound]`

本 lane 无 `sorryAx`。

## Shared workflow 状态边界

`lean-agent-sidecars.yml` 整体 run 仍为红色，但不是本 sidecar 导致。相同真实 job 日志中仍可见其他独立 lane 的既有失败，包括 FLT quotient transport、M4 cross-branch、P5 componentwise relative decay、P5 parameter tube、P5 weighted-dual residual、P7 tail Schur 与 P8 ramp reconstruction。上述 lane 本轮未抢占、未修改。

## 尚未形式化 / 尚未闭合

- actual P4 cell family 的共同 endpoint certificate；
- concrete `(A_i,G_i,P_i,A0,a,b,m)` 与 canonical source 的绑定；
- true-DH / Float64 execution semantics；
- realized shifted witness/rounding containment（若最终 checker 采用浮点实现）；
- 同一 P8 trajectory/domain 的 coverage；
- P4/M4 final closure；
- registry/admission 与最终 DAG integration。

因此本结果只标记为 `compiled_candidate`，不能自行宣称 P4/M4 或 Route-B 完成。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
