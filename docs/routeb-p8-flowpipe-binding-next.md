# Route-B P8 independent reachability：source contract 与 flowpipe binding next

日期：2026-09-06。范围是只读审计 `docs/routeb-m4-next-obligations.md`、
P8 Picard/receipt examples，以及外部 `routeB_export_traj` 与真实 RHS 文件。
本轮不运行长仿真，不修改 source、state、registry；只新增本文档。

## 当前状态

结论：`P8 independent true-DH reachability` 仍为 `OPEN`。

已有 Lean 叶的确切边界是：

- `RouteBP8PicardStep.fullX0_subset_initialBox`：把全 12 个机械坐标的
  `9/400` 初始能量约束及 `c^2 <= 3` 放入显式 14 坐标初始盒；
- `RouteBP8PicardStep.picard_image_inclusion`：在给定 `hbox` 后证明一次
  Picard image 的坐标区间包含；
- `RouteBP8PicardStep.picard_image_ramp_coordinates`：在给定
  `RampRhsPremise` 后暴露 `w`、`c` 的 Picard 更新；
- `RouteBP8PicardStep.fullX0_ramp_picard_step_decomposition`：组合以上三者，
  但仍把真实 RHS、区间 enclosure、Picard image existence 都作为前提；
- `RouteBP8RhsReceipt.receipt_to_routeBP8PicardStep_hbox` 与
  `receipt_usable_for_routeBP8PicardStep`：只把 receipt 的
  `Contains` 命题转成 parent 的 `hbox`，不绑定 Julia RHS。

`RhsReceipt.fullRhsBinding` 的唯一构造子仍是 `open`。`receipt.template.json`
仍是 `pending_endpoint_payload`：12 个动态端点为空，`w` 仅记录 source literal
`du[13]=0`，`c` 仍为 sidecar/open。故当前结果是 conditional interface，
不是 true-DH flowpipe theorem。

## 当前第一阻塞点：13-state source 与 14-state ramp contract 不相容

### Lean parent 的要求

`RouteBP8PicardStep` 固定坐标为

```text
Fin 14: q1..q6, dq1..dq6, w, c
qSlot i  = i       (0..5)
dqSlot i = 6+i    (6..11)
wSlot    = 12
cSlot    = 13
```

其 `RampRhsPremise F` 要求对所有状态 `z`：

```text
F z wSlot = z cSlot
F z cSlot = 0
```

这正是 `w'=c, c'=0`，而不是只把 `c` 放在 receipt 的尾部。

### 当前真实 RHS 的事实

外部 `robot_final/cross_validation/routeB_reachability_full_dh_probe.jl` 的
`full_rhs!`（lines 131--166）读取 `q=u[1:6]`、`dq=u[7:12]`、`w=u[13]`，
写入 `du[1:6]=dq`、`du[7:12]=acc`，并明确写入 `du[13]=z0`。文件没有
`c=u[14]`，也没有 `du[13]=c`；其 ReachabilityAnalysis problem 是
`dim:13`（lines 171--178）。因此它是 13-state、constant-`w` RHS。

`routeB_export_traj.jl` 也没有提供 14-state RHS：`sim_traj` 在 lines 89--109
用固定 `dt=0.005` 离散更新 `q,dq`，并在 line 100 直接计算
`wv=cw*tk`；批量 exporter 在 line 149 从外部采样 `cw`。这只能记录离散
Monte-Carlo trajectory，不能把 `c` 变成 ODE state。

### 精确的不可实例化见证

对当前 source 作自然 lift：

```text
F14(z)[0..11] = full_rhs!(z[0..12])[0..11]
F14(z)[12]   = 0
F14(z)[13]   = 0.
```

取 `z*` 的 `q=dq=w=0,c=1`。则 `FullX0 z*` 成立，因为机械能为 0、
`w=0`、`c^2=1<=3`。但 parent 的 ramp premise 同时要求

```text
F14(z*)[12] = z*[13] = 1,
```

而 source lift 给出 `F14(z*)[12]=0`。所以当前 source 下
`RampRhsPremise F14` 直接矛盾；这比补齐 14 个 RHS endpoint 更早。
只有 `c=0` 的退化子族可以绕过该矛盾，不能覆盖原始 `c^2<=3` 扰动族。

因此第一 child 不是 interval arithmetic，而是必须二选一的语义修复：

1. 提供真正的 14-state RHS，证明 `w'=c,c'=0`；或
2. 把 P8 contract 改成显式时间的 13-state RHS `F13(t)`，证明
   `w(t)=c*t`，并另建对应 parent/flowpipe adapter。

本轮不修改现有 parent，故当前 P8 链在 `RampRhsPremise` 处停止。

## source hash 与 coordinate map

### 当前 payload generator 选中的 source

`examples/routeb_p8_rhs_payload_generator/SOURCE_METADATA.json` 声明的
candidate 是 `robot_final/full_dh_probe+dhport_lib`，只 hash 以下两个文件：

| 角色 | 外部路径 | SHA-256 | 关键语义 |
|---|---|---|---|
| true-RHS probe | `6dof_sos_optimized/6dof_sos_optimized/robot_final/cross_validation/routeB_reachability_full_dh_probe.jl` | `12292f8841ef79cfa58d07facbec4ca739e27346b11b6ec57e290638b7d8b93a` | 13-state `full_rhs!`; `du[13]=0` |
| DH source anchor | `6dof_sos_optimized/6dof_sos_optimized/robot_final/dhport_lib.jl` | `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936` | DH `M`; `10^-6 I`; central FD `C/G`, `h=10^-5` |
| exporter | `6dof_sos_optimized/6dof_sos_optimized/robot_final/routeB_export_traj.jl` | `35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf` | 固定步长 trajectory exporter；manifest 标为 empirical |

`routeB_export_traj.jl` 与 `routeB_dense_Mq/routeB_export_traj.jl` 及 source
audit snapshot 同 hash，但它没有被当前 P8 receipt 的 `source_hashes` 声明。
这不是本轮修复项；未来若 exporter 仍属于 source contract，必须显式加入
provenance manifest。

另有同名旧副本
`C:\Users\z5242\Desktop\重构版\李导数\robot_final\routeB_export_traj.jl`
的 hash 为 `fc69514fb659c7f0d1702c3670e35a06d5a299965e5cd41823707409ee3c63b8`，
其同目录 `dhport_lib.jl` 为
`38f89aa0b18cbd24930e4112b8eb4f2b025c4145172783f280bed4f8848b81bc`。
不得把此旧副本与当前 P8 generator 选中的两个 source 静默混用。

### 14 坐标的逐项映射

| payload / Lean one-based | 名称 | Julia input | Julia output | 当前状态 |
|---:|---|---|---|---|
| 1..6 | `q1..q6` | `u[1]..u[6]` | `du[1]..du[6]` | source text only; `du[i]=dq[i]` |
| 7..12 | `v1..v6`（source 名 `dq`） | `u[7]..u[12]` | `du[7]..du[12]` | source text only; `du[i+6]=acc[i]` |
| 13 | `w` | `u[13]` | `du[13]` | source text only; **`0`，不是 `c`** |
| 14 | `c` | none | none | OPEN sidecar; `full_rhs!` 不消费 |

因此 receipt 的 14 维只是 endpoint shape；它不等于 14-state source binding。
当前局部 box 是 `q,v,w∈[-0.01,0.01]`、`c∈[-2,2]`，且只是一盒，不能
推出 full-X0、全 ramp family 或 `[0,1]` coverage。

## 从 conditional receipt 到 true-DH flowpipe 的最短 child theorem chain

以下是“source contract 已先修复为一致的 14-state ramp RHS”之后的最短链；
括号内是现有可复用 theorem，`NEW` 表示尚不存在的具体 child。

```text
S0  source_hash_and_coordinate_manifest              (metadata/checker only)
 |
 v
S1  NEW source13_or_source14_semantic_binding
     exact q/dq/w/c map; DH/FD/regularizer/solve semantics
 |
 v
S2  NEW ramp_binding
     ∀ z, F14 z wSlot = z cSlot ∧ F14 z cSlot = 0
 |
 v
S3  NEW outward_rhs_interval_contains
     ∀ cells B, ∀ y∈B, ∀ i: Fin 14,
       lower_B i ≤ F14 y i ≤ upper_B i
 |
 v
S4  receipt_to_routeBP8PicardStep_hbox
     (existing adapter; receipt Contains -> hbox)
 |
 v
S5  fullX0_subset_initialBox
     + fullX0_ramp_picard_step_decomposition
     (existing structural one-step theorem)
 |
 v
S6  NEW picard_image_exists_and_is_solution_step
     actual ODE/AC solution, not merely an assumed picardImage witness
 |
 v
S7  NEW local_flowpipe_step
     each cell's solution segment lies in its propagated interval/tube
 |
 v
S8  NEW cell_continuation_and_partition_coverage
     next-cell compatibility, no unresolved leaf, time coverage to T=1
 |
 v
S9  p8_firstExit_domain_continuation_assembly
     (existing conditional theorem, if first-exit route is used)
 |
 v
S10 NEW true_dh_flowpipe_T1
     ∀ x0 in full 12-ball, ∀ c with c²≤3,
     ∀ t∈[0,1], trajectory(t)∈ certified full-state tube(t)
```

`RouteBFirstExitBridge.p8_firstExit_domain_continuation_assembly` can provide
the logical composition at S9, but it still requires concrete
`FirstExitAttainment`, `PrefixLimitMargin`, `BoundarySeparated`,
`LocalCertificate` and `ContinuationCriterion`. It does not turn a finite list
of reachsets into coverage. The existing `RouteBTerminalFlowpipe` leaf is a
12-state conditional terminal-transfer skeleton, not a substitute for S1--S8.

For the shortest *pure flowpipe* closure, the M4 C1--C5 energy/residual chain is
not needed. For the original terminal theorem it is downstream: after S10 one
still needs the source residual/energy budget and terminal comparison described
in `docs/routeb-m4-next-obligations.md` (especially C4 and C5).

## Why the current receipts/probes cannot discharge the chain

1. `RhsReceipt.Contains` is a proposition over an abstract `F`; metadata and
   source hash are not proof of containment.
2. All dynamic endpoint entries in `receipt.template.json` are `null`; the
   `w=[0,0]` entry is only a source-text fact and is semantically incompatible
   with nonzero-ramp `w'=c`.
3. The full-DH probe's default artifact is `PASS_FULL_DH_ADAPTER_SMOKE` with
   `t_end=0`; narrow artifacts at `T=10^-3` are explicitly marked
   `full_dh_validated=false` and `coverage_complete=false`.
4. The exporter manifest says `evidence_level="empirical"`,
   `coverage_kind="trajectory_monte_carlo_only"`, and
   `global_box_coverage=false`; it skips failed/out-of-limit samples and uses a
   discrete `dt=0.005` rollout.
5. The full-DH probe has its own generic `mass_generic` and no-pivot solve,
   whereas the exporter calls `dhport_lib.jl`/Float64 `arm_MCG` and `\`. A
   future source comparator must bind these semantics if both files are claimed
   to describe one deployed RHS.

## Admission boundary

Current P8 status should remain:

```text
source_binding       = OPEN
ramp_binding         = OPEN / inconsistent with current 13-state source
rhs_endpoint_receipt = PENDING
flowpipe_coverage    = OPEN
full_dh_validated    = false
coverage_complete    = false
registry             = unchanged
```

The first actionable child is therefore `S1/S2` (a coherent 14-state ramp
source binding), not a longer simulation and not a wider local interval box.
