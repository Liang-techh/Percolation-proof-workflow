---
kind: review_result
review_id: review-T-P5-031-juyangxianzun-20260907T1251
task_id: T-P5-031
source_agent: 巨阳仙尊
agent: 巨阳仙尊
created_at: 2026-09-07T12:51:00-06:00
status: compiled_candidate
admission_label: compiled_candidate
claim: agent_review_inbox/claim-T-P5-031-juyangxianzun-20260907T1228.md
math_input:
  - agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md
sidecar: examples/routeb_p5_physical_gain_parameter_tube_lean/
lean_source_blob: d0dddc11fea89b991980d200605fc65c7fb03adb
verify_blob: b799e9a546e1f3bcdd0156e5158c93174d44c9b5
toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
ci_head: 1c129fd3d7d6860c324f32734dd7d384a2154feb
ci_run: 34152839072
ci_job: 101838555450
---

# T-P5-031：physical gain → parameter tube 的 Lean 子闭环

本轮只形式化古月方源 `review-T-P5-031-guyuefangyuan-20260907T1224.md` 中 **source-independent** 的数学桥，不重新探索大规模数学，也不接管 source gain table、Float64 语义、P8 coverage、ODE first-exit、provenance/admission、registry 或最终整合。

## 1. 新增 portable sidecar

路径：

- `examples/routeb_p5_physical_gain_parameter_tube_lean/P5PhysicalGainParameterTube.lean`
- `examples/routeb_p5_physical_gain_parameter_tube_lean/README.md`
- `examples/routeb_p5_physical_gain_parameter_tube_lean/verify.sh`
- `examples/routeb_p5_physical_gain_parameter_tube_lean/lean-toolchain`

`verify.sh` 通过 `PATH` 查找 `lake`，读取 sibling `examples/local_fkg/lake-manifest.json`，校验 toolchain 一致性，并以 `-DwarningAsError=true` focused compile；已登记 `CI_PORTABLE=1`，由 `.github/workflows/lean-agent-sidecars.yml` 自动执行，没有硬编码本机专属路径。

## 2. theorem decomposition

本 sidecar 将数学输入压成以下最小 theorem/interface：

1. `moving_frame_a4_endpoint_bound`
   - hypotheses: `0 ≤ t`, `t ≤ 1`
   - conclusion: `|h4*t+r4| ≤ A4`
   - exact constants:
     - `h4 = 2340/8699`
     - `r4 = -21912800/75672601`
     - `A4 = 21912800/75672601`。

2. `moving_frame_a5_endpoint_bound`
   - 同样在 `0 ≤ t ≤ 1`
   - `h5 = 1520/8699`
   - `r5 = -15007200/75672601`
   - `A5 = 15007200/75672601`。

3. `moving_frame_time_abs_bound`
   - `0 ≤ t ≤ 1 ⇒ |t| ≤ 1`。

4. `four_term_square`
   - division-free 四项 Cauchy：
   - `(u1+u2+u3+u4)^2 ≤ 4*(u1^2+u2^2+u3^2+u4^2)`。

5. `four_term_component_budget`
   - 将四个 typed component square budget `ui^2 ≤ ci*V` 聚合为 centered scalar budget。

6. `component_physical_gain_transport`
   - 输入 generalized-force component physical contract
     `|Dl| ≤ kq4|dq4|+kq5|dq5|+kv4|dv4|+kv5|dv5|+kw|dw|+kc*d`
   - 与 moving-frame component bounds
   - 输出
     `|Dl| ≤ centeredPart + parameterGain*d`。
   - CI 首轮证明了 `kc≥0` 对这个 consumer 实际不需要，因此修复后从 theorem interface 中删除该冗余 hypothesis；`parameterGain_nonneg` 仍保留真正需要的 `kc≥0`。

7. `parameterGain_nonneg`
   - 非负 physical gains 推出 deterministic parameter gain 非负。

8. `two_channel_cauchy`
   - `(S4*G4+S5*G5)^2 ≤ (S4^2+S5^2)(G4^2+G5^2)`。

9. `square_le_square_of_abs_le`
   - `|x|≤r ⇒ x^2≤r^2`，不用 `sqrt`。

10. `product_slack_cross_bound`
    - square-only Young/product-slack consumer：
    - 若 `C^2 ≤ U*W*V`、`UW≤pq`、相关量非负，则
      `2*d*C ≤ p*V+q*d^2`。

11. `physical_gain_to_mu_nu_envelope`
    - 主 source-independent bridge：若
      `|Dl4|≤S4+G4*d`, `|Dl5|≤S5+G5*d`,
      `S4^2+S5^2≤U*V`, `U*(G4^2+G5^2)≤p*q`, `p,q≥0`,
      则
      `Dl4^2+Dl5^2 ≤ (U+p)*V + ((G4^2+G5^2)+q)*d^2`。
    - 因而 checker-facing 可取 `mu=U+p`, `nu=W+q`，其中 `W=G4^2+G5^2`。

12. `parameter_tube_gain_gate`
    - 冻结现有 parameter-tube ledger 的 rational gate：
      `11424*(U+p)+137088*(W+q)<2285`。

13. `slack_feasibility_necessity`
    - 对任意非负 slack `p,q`，若 `UW≤pq` 且
      `11424p+137088q<R`，则必须
      `R>0` 且 `6264373248*U*W<R^2`。
    - 这是 fail-closed feasibility diagnostic，不把 necessity 误写成 sufficiency。

14. `exact_feasibility_factor`
    - kernel 冻结：`4*11424*137088 = 6264373248`。

## 3. 真实 Lean → CI → 修复 → 再 Lean

首轮 workflow `run 34152433689 / job 101837315243` 的真实日志在本 sidecar 报：

`P5PhysicalGainParameterTube.lean:94:20: Variable name hkc is not explicitly referenced.`

这是 `-DwarningAsError=true` 捕获的最小 theorem interface 冗余，不是数学失败。首轮的各个 `#print axioms` 已经没有 `sorryAx`；我没有关闭 linter，而是直接删除 `component_physical_gain_transport` 中不需要的 `hkc : 0 ≤ kc` hypothesis。修复 commit：

`1c129fd3d7d6860c324f32734dd7d384a2154feb`

修复后的真实 Actions：

- run: `34152839072`
- job: `101838555450`
- Lean: `4.32.0`
- Lake: `5.0.0-src+8c9756b`

本 sidecar 日志明确输出：

```text
AXIOM_AUDIT=PASS
P5_PHYSICAL_GAIN_PARAMETER_TUBE_FOCUSED_CHECK=PASS
SOURCE_PHYSICAL_GAIN_TABLE=OPEN
SOURCE_FLOAT64_INCREMENTAL_SEMANTICS=OPEN
P8_SAME_DOMAIN_COVERAGE=OPEN
ODE_FIRST_EXIT_CONTINUATION=OPEN
P5_P8_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_physical_gain_parameter_tube_lean/verify.sh
```

shared workflow 整体仍为 failure，但真实日志确认该红灯来自其他独立 lane，例如 FLT quotient 路径、M4 cross-branch、P5 componentwise/parameter-tube/weighted-dual、P7 tail Schur 与 P8 ramp reconstruction；本轮没有越权修改这些 lane。

## 4. `#print axioms`

修复后的 14 个公开 theorem 均完成 axiom report：

- 实数代数 theorem：`[propext, Classical.choice, Quot.sound]`
- `exact_feasibility_factor`：`[propext]`
- 本 sidecar 无 `sorryAx`。

## 5. 仍未形式化 / 应退回 source 层的输入

Lean 代数桥已闭合，但 `T-P5-031` 不能因此升级为最终物理证书。下一层必须由 source/checker 提供：

- 同一 P8 / first-exit domain 上的真实、force-normalized physical gain table `k[a,*]`；
- raw Julia/DH/Float64/controller/linear-solve 的 centered incremental/Lipschitz execution semantics；
- 由 component state budgets 生成真实 `U`，由 parameter gains 生成真实 `G4,G5,W`；
- 选择并验证非负 `p,q`，同时满足 `UW≤pq` 与 `11424(U+p)+137088(W+q)<2285`；
- P8 same-domain center trajectory / coverage、initial binding、ODE first-exit continuation；
- 最终与 P5/P8/M4 的组合仍由梁智炜（Codex）决定。

若 source 数字一旦给出，建议 checker 先算
`R = 2285 - 11424U - 137088W`，并先用 kernel 化 necessity gate `R>0`、`6264373248UW<R^2` 快速 fail-closed；通过后再寻找/冻结具体 `p,q` witness。

## 6. 状态边界

当前仅为 **`compiled_candidate`**。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
