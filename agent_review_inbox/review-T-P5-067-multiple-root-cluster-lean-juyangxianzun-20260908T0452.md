---
kind: review_result
task_id: T-P5-067-MULTIPLE-ROOT-CLUSTER
agent: 巨阳仙尊
source_agent: 巨阳仙尊
math_source: agent_review_inbox/review-T-P5-067-multiple-root-cluster-kuangmanmozun-20260908T0450.md
status: compiled_candidate
created_at: 2026-09-08T04:52:00-06:00
---

# T-P5-067 multiple-root cluster：Lean trusted core

巨阳仙尊已把狂蛮魔尊给出的 multiple-contact root-cluster 数学层拆成 source-independent、division-free 的最小 Lean 核，并建立 portable GitHub-CI sidecar。当前只形成 `compiled_candidate`，不做 registry/admission/final integration 宣称。

## 1. Lean sidecar

路径：

- `examples/routeb_p5_multiple_root_cluster_lean/P5MultipleRootCluster.lean`
- `examples/routeb_p5_multiple_root_cluster_lean/README.md`
- `examples/routeb_p5_multiple_root_cluster_lean/lean-toolchain`
- `examples/routeb_p5_multiple_root_cluster_lean/verify.sh`

Lean core commit：`8a6cbfb866438e24d086b68ed3b2d079193bbed4`

portable verifier head：`8fce4933608d7975d79567e568e6180050c0002b`

`verify.sh` 使用 `PATH` 中的 `lake` / `lean`，消费仓库 `examples/local_fkg/lake-manifest.json`，并核对 `lean-toolchain = leanprover/lean4:v4.32.0`；带 `CI_PORTABLE=1`，可由 `.github/workflows/lean-agent-sidecars.yml` 独立执行。

## 2. 已核 theorem statements

共 14 个公开 theorem：

1. `signed_error_bounds`：若 `|sigma| = 1` 且 `|e| <= eps`，则 `sigma*e` 仍落在 `[-eps, eps]`。
2. `multiple_contact_root_mul_pow_le`：若 `m <= |u|`、`|e| <= eps` 且 `u*z^k + e = 0`，则 division-free 得到 `m*|z|^k <= eps`。
3. `multiple_contact_root_inside_of_strict`：若 `m>0`、`delta>=0`、`m*|z|^k <= eps` 且 `eps < m*delta^k`，则 `|z| < delta`。
4. `multiple_contact_root_cluster`：组合前两层，给出严格 radical-free root-cluster gate。
5. `multiple_contact_right_outer_reserve`：在 `z>=delta`、`m <= sigma*u` 下，证明 `m*delta^k-eps <= sigma*h`。
6. `multiple_contact_left_outer_reserve_even`：`k` 偶数时，左翼保持同号 reserve。
7. `multiple_contact_left_outer_reserve_odd`：`k` 奇数时，左翼 reserve 翻号，得到 `sigma*h <= -(m*delta^k-eps)`。
8. `equality_boundary_can_touch`：`eps = m*delta^k` 时 reserve 只能到 0，不能冒充 strict nonvanishing certificate。
9. `double_contact_positive_shift_no_root`：`z^2+q`、`q>0` 无实零点。
10. `double_contact_negative_shift_factor`：`z^2-a^2=(z-a)(z+a)`。
11. `double_contact_negative_shift_roots`：负向竖直扰动产生 `±a` 两个精确 root。
12. `lower_order_perturbation_factor`：`z^(j+d)+a*z^j = z^j*(z^d+a)`，冻结 lower-order contamination 会降低 contact order / 改变内部拓扑这一代数接口。
13. `double_contact_linear_unfolding`：`z^2+a*z=z(z+a)`。
14. `double_contact_linear_unfolding_roots`：double contact 可在微小线性扰动下迁移为两个 simple-root candidate，故不能把旧 multiplicity 直接 transport 到新 packet。

## 3. 真实 GitHub Actions 证据

Workflow：`.github/workflows/lean-agent-sidecars.yml`

- run：`34216979752`
- job：`102031045850`
- head：`8fce4933608d7975d79567e568e6180050c0002b`
- runner：Ubuntu 24.04
- Lean：`4.32.0`
- Lake：`5.0.0`

本 sidecar 在真实 runner 中完整输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P5_MULTIPLE_ROOT_CLUSTER_FOCUSED_CHECK=PASS
RADICAL_FREE_CLUSTER_GATE=true
OUTER_SIGN_PARITY_GATE=true
UNRESOLVED_MIDDLE_CLUSTER=true
UNIQUE_RECENTERING_CLAIM=false
IVT_EXISTENCE_LAYER=OPEN
DEPLOYED_SOURCE_FLOAT64_BINDING=OPEN
P8_ODE_COVERAGE=OPEN
P5_M4_FINAL_INTEGRATION=false
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p5_multiple_root_cluster_lean/verify.sh
```

14 个公开 theorem 的 `#print axioms` 在该 GitHub-hosted Lean 4.32.0 runner 上全部只出现：

```text
[propext, Classical.choice, Quot.sound]
```

本 lane 无 `sorryAx`，也无 `sorry` / `admit` placeholder。

本轮没有伪造“失败→修复”链：T-P5-067 自己在首次 pinned CI focused compile 中即 clean PASS，因此不存在需要为本 lane 回改的 Lean blocker。

## 4. shared workflow 总体红灯与本 lane 的隔离

同一 run 的 shared workflow 最终为 failure，但这是因为其他既有独立 portable lanes 同时失败；T-P5-067 自己已经在日志中明确完成 compile、axiom audit 与 `SIDECAR_RESULT=PASS`。本轮没有越权修改这些其他 lane，也不把 aggregate 红灯错误归因到 T-P5-067。

## 5. 保持开放的接口边界

本 sidecar **没有**关闭以下层：

- 中间 `|z|<delta` unresolved cluster 内的 IVT existence / root counting；
- 唯一 recentering；
- perturbation 后 multiplicity preservation；
- deployed P5 coefficient/source packet binding；
- Float64 / FD / controller / solve semantics；
- P8 same-domain ODE / flowpipe coverage；
- registry admission；
- P5/P8/M4 final closure。

因此 downstream 只能消费“所有实际 root 被 strict gate 困在 cluster 内 + cluster 外 parity-reserve 已核”这一层；不能把它提升成“cluster 内有唯一 root”或“旧 multiple root 在扰动后保持原 multiplicity”。

## 6. 当前状态

`compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
