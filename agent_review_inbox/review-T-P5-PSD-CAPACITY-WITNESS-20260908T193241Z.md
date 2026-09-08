---
kind: review_result
review_id: R-P5-PSD-CAPACITY-WITNESS-20260908T193241Z
task_id: T-P5-PSD-CAPACITY-WITNESS
source_agent: Poincare
harvested_by: 梁智炜
created_at: 2026-09-08T19:32:41Z
status: EXACT_TOY_WITNESS_SOURCE_INDEPENDENT
integration_status: pending
admission_label: pending
concrete_K_path_bound: false
source_binding: false
P5_closed: false
registry_eligible: false
registry_promoted: false
lean_run: false
lake_run: false
kernel_checked: false
axioms_checked: false
requested_action: preserve exact toy capacity witness; require actual source packet before Route-B consumption
---

# P5 PSD-slack capacity：exact toy witness

本回合运行新建的
`examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_KPATH_PACKET_PSDCapacity20260908.py`，
只针对已冻结的 source-independent toy fixture 做 targeted arithmetic；没有运行整仓
回归、Julia、Lean/Lake，也没有修改 state、registry 或任何外部项目文件。

## Exact result

脚本在 18 个 representative certificate 上逐项构造
`S_r - C_r(tD)`，为每个 shifted `S` 生成 exact rational LDL/PSD factor，并检查
所有 72 条（18×4）容量行。对全一非负方向 `D`，得到：

```text
t_cap = 32553/4000000
t     = 1/1000
active_cone = [2, 4]
active_row  = 2
shifted_psd_factors = 18
capacity_inequalities = 72
```

更新后的 toy gain 为两行均为 `1/500` 的 2×4 矩阵；baseline geometry、updated
legacy checker 和 updated geometry checker 均报告 `certificate_arithmetic_valid=true`
且 18 个 representative/36 个含 flip labels 保持通过。该结果证明固定 `N` 扣减
障碍可以由 PSD slack 的小正增量绕开；它不是 actual physical `K_path` 的数值结论。

## Frozen provenance and output boundary

输入代码 hashes：

```text
check_exact.py       d887aade11edf9adf1e7f532d8b173a089ac9e2fadba2e25fbc2f169e1e4211
NEW_exact_geometry_spn.py
                      263fac727c1c3068043c02a63dade5995a22e1e7e9a879682ac3e69bafd54f42
NEW_KPATH_PACKET_PSDCapacity20260908.py
                      6874c582ffad59463a18fc92e676e66d2b393f0604e8c8868658745d6c40df07
```

输出文件的当前 hashes：

```text
NEW_KPATH_PACKET_PSDCapacityWitness20260908.json
                      9dbd0ac2b785b3aa8546dbc3c30c73b531ff139f80eaa1d0ab7e211efa35b93f
NEW_KPATH_PACKET_UpdatedToySPN20260908.json
                      962b97fd8b9cb70c850face843a15ae20ee3166dee272f504ba0086998a1218b
```

输出显式保留 `scope=source-independent-unbound`、`concrete_K_path_bound=false`、
`source_binding=false`、`P5_closed=false` 和 `registry_eligible=false`。它不绑定
真实 DH residual、domain、force/source map、runtime Float64、flowpipe 或 terminal
transfer；`K`、`Q`、`L`、18 张证书和 `t` 只属于 toy fixture。

## Mathematical reuse and next gate

可复用的数学内容是：若实际每个 representative 有 exact `S_r ⪰ δ_r I`，则
`C_r(tD)` 的行和给出有理容量多面体，任何满足 `t≤min δ_r/c_ri` 的非零方向都可
消耗 PSD slack；这为未来 actual certificate-indexed `K_path` 提供了明确的
有限维构造模板。不能把本 toy 的 `t` 或证书矩阵迁移到真实 source。

进入 Route-B 前必须另交：actual `PathBinding`、同一 domain 的 `K_path`、chart/state
与 source hashes、真实 `μ/Q` normalization、18 个 source-indexed rational
certificates，以及目标-pinned Lean/import/axiom/comparator receipts。当前只登记
pending exact toy evidence，formal gate 保持关闭。
