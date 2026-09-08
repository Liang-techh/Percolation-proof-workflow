---
kind: review_result
review_id: GH-LEAN-BODY6-PATHDOMAIN-REPAIR-JYXZ-20260908T0824
task_id: GH-LEAN-BODY6-PATHDOMAIN-REPAIR
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-08T08:24:00-06:00
inspected_commits:
  - 3cddaef8f351a27ba30e0cfdd2df0638c21493a9
  - bd5d1cd2b34b170e7ad0fa918d24ce397ec8d9c4
  - 1f7592f29f9bec8e29b689db30c416b6655dcff6
integration_status: pending
admission_label: compiled_candidate
requested_action: 封不觉独立验证；梁智炜（Codex）收割与最终整合
---

# GH-LEAN-BODY6-PATHDOMAIN-REPAIR：pinned Lean / Actions 验证结果

本轮按 task_queue 指派，只验证 `examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.lean` 中已经提交的 `cap + B` / `B + cap` 修复，不扩大数学 claim，也不做 provenance / receipt / admission 重审。

## 1. 被验证的具体修复

协调层 commit `3cddaef8f351a27ba30e0cfdd2df0638c21493a9` 保持 theorem 输入契约

```lean
hBudget : cap + B ≤ bar
```

不变，只在 `projected_shift_cap_transfer_attempt` 中先显式换序：

```lean
have hBudget' : B + cap ≤ bar := by
  simpa [add_comm] using hBudget
exact (add_le_add_right (hCap t ht) B).trans hBudget'
```

因此这是纯 arithmetic/order repair：先从 `hCap t ht : w t ≤ cap` 得到 `B + w t ≤ B + cap`，再与 commuted budget 拼接。没有改变 theorem statement，也没有把初始时刻包含偷换成 whole-path inclusion。

## 2. portable focused audit 工件

新增：

- `examples/routeb_body6_pathdomain_projection_audit/lean-toolchain`
- `examples/routeb_body6_pathdomain_projection_audit/verify.sh`
- `examples/routeb_body6_pathdomain_projection_audit/README.md`

其中 verifier 使用仓库 `examples/local_fkg/lake-manifest.json` 和同一 pinned toolchain；`lake` / `lean` 均从 `PATH` 查找，没有硬编码本机路径，并带 `CI_PORTABLE=1` 标记供 `.github/workflows/lean-agent-sidecars.yml` 自动执行。

人工等价的 focused command 为：

```bash
CI_PORTABLE=1 bash examples/routeb_body6_pathdomain_projection_audit/verify.sh
```

verifier 内部 pinned compile 路径为：

```bash
cd examples/local_fkg
lake env lean -DwarningAsError=true "$TMP"
```

其中 `$TMP` 是当前 target 的临时副本，并追加七个公开 theorem 的 `#print axioms`。

## 3. 真实 GitHub Actions receipt

真实 GitHub-hosted runner：

- workflow: `Lean agent sidecars`
- run: `34237227667`
- job: `102098140421`
- checked head: `1f7592f29f9bec8e29b689db30c416b6655dcff6`
- OS: Ubuntu 24.04
- Lean: `4.32.0` (`8c9756b28d64dab099da31a4c09229a9e6a2ef35`)
- Lake: `5.0.0-src+8c9756b`
- local_fkg toolchain: `leanprover/lean4:v4.32.0`

本 focused verifier 的实际 wrapper exit code 为 **0**，runner 原样输出：

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
BODY6_PATHDOMAIN_REPAIR_FOCUSED_CHECK=PASS
CAP_PLUS_SHIFT_ORDER_REPAIR=true
WHOLE_PATH_INCLUSION_PROVED=false
PHYSICAL_DH_SOURCE_BINDING=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_body6_pathdomain_projection_audit/verify.sh
```

## 4. `#print axioms`

下列七个 theorem 在 pinned runner 上全部只依赖：

```text
[propext, Classical.choice, Quot.sound]
```

没有 `sorryAx`：

1. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.whole_path_has_initial_attempt`
2. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.project_whole_path_attempt`
3. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.project_initial_only_attempt`
4. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.projected_shift_cap_transfer_attempt`
5. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.already_shifted_cap_transfer_attempt`
6. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.initial_does_not_give_whole_path_attempt`
7. `NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907.shift_accounting_counterexample_attempt`

placeholder scan 同样 PASS；target 内没有 `sorry` / `admit`。

## 5. shared workflow 为什么仍是红色

同一个 shared job 最终整体 exit 1，但不是本 lane 导致。wrapper 共扫描 75 个 portable sidecar，只要任意一个失败就把 `PORTABLE_SIDECARS_FAILED=1` 并退出 1。本 run 中其它独立历史 lane 仍有真实问题，例如 FLT sidecar 的 portable 相对路径、M4 cross-branch 的 noncomputable/unused-variable、P5 componentwise/direct-two-channel/parameter-tube/recentered-unit/square-only/weighted-dual-residual、P7 tail Schur、P8 ramp reconstruction 等。它们均发生在本 BODY6 focused lane PASS 之后或之外，本轮没有越权修改。

## 6. 尚未关闭的边界

本结果只支持 `compiled_candidate`：

- whole-path inclusion：**未证明**；
- physical DH/source projection：**OPEN**；
- storage identity / concrete source binding：**OPEN**；
- ODE continuation / same-domain coverage：**OPEN**；
- registry/admission mutation：**false**；
- 不宣称 P4/P5/P8/M4 或 BODY6 最终 integration。

结论：`cap + B` / `B + cap` 的 Lean compile blocker 已在仓库 pinned Lean 4.32.0 / Lake 5.0.0 下真实消除，七个公开 theorem 的 axiom audit clean，本 focused lane 可标记为 `compiled_candidate`。

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**。
