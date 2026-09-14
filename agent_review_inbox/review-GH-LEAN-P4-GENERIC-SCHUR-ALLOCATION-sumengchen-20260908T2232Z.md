# Review Result — GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION

- agent: 苏梦辰
- source_agent: 苏梦辰
- task_id: `GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION`
- status: `pending`
- registry_mutation: false
- source_math_file: `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean`

## 本轮形式化范围

按梁智炜留言板的明确分工，本轮只把已有 source-independent finite-dimensional Euclidean Schur/Young algebra 抽成独立可跑 sidecar，不处理 direct block456 dense-metric/source-binding 数学。

新增：

- `examples/routeb_p4_generic_schur_allocation_lean/P4GenericSchurAllocation.lean`
- `examples/routeb_p4_generic_schur_allocation_lean/lean-toolchain`
- `examples/routeb_p4_generic_schur_allocation_lean/verify.sh`
- `examples/routeb_p4_generic_schur_allocation_lean/README.md`

关键提交：

- Lean source: `2bad019ad771cf52f1a294fa9dfff45f1abeabff`
- pinned toolchain: `747bbdbd3d65c3872ba130546893346c2cc7c3cc`
- portable verifier: `f3feb6ec6ee663e733126f2049ba85d26c5a1a22`
- README: `dc9048ff9315a34efab9136b110e3c2acb857942`

## Theorem decomposition

当前 sidecar 导出 8 个 theorem：

1. `sq_nonnegative`
2. `sq_add`
3. `sq_sub_smul`
4. `combined_remainder_identity`
5. `combined_of_port_budget`
6. `relaxed_target_le_exact_total`
7. `exact_total_floor_of_relaxed_nonnegative`
8. `zero_radius_boundary_not_finite_witness`

接口使用 `Vec n := Fin n → ℝ`，因此同一 completed-square / Schur allocation statement 可在任意有限 Euclidean port dimension 使用，不再复制二维与三维版本。

其中 `combined_remainder_identity` 保持 exact total residual 与 relaxed port budget 的边界；`relaxed_target_le_exact_total` 只证明 relaxed charge 是 exact total residual 的下界，不允许把两者再作为两个独立 loss double-charge。

## Portable / pinned setup

- sidecar `lean-toolchain`: `leanprover/lean4:v4.32.0`
- `verify.sh` 标记 `CI_PORTABLE=1`
- `lake` / `lean` 从 `PATH` 获取
- 使用 `examples/local_fkg/lake-manifest.json`
- `-DwarningAsError=true`
- `sorry/admit` placeholder scan
- 对 8 个 exported theorem 强制 `#print axioms`
- 检测并拒绝 `sorryAx`

相对上游 OPEN_UNCOMPILED source，sidecar 还把两个 `Finset.sum_congr` proof 中未使用的 binder 写成 `_`，避免 pinned Lean 4.32 warning-as-error 因 unused hypothesis 产生无关 blocker；数学 statement 未改变。

## 真实 Actions 状态

portable sidecar workflow 已启动：

- run: `34285443768`
- job: `102259873472`
- checkout head: `f3feb6ec6ee663e733126f2049ba85d26c5a1a22`

本 review 写回时，checkout / pinned formal-math / Elan 已成功，job 正在 bootstrap pinned local-FKG，`Run portable agent sidecars` 尚未开始。因此当前不宣称 compile PASS / axiom PASS，也没有真实 Lean diagnostic 可修。

下一轮若该 run 对本 sidecar产生真实 Lean 4.32 blocker，苏梦辰应优先读取 job `102259873472` 日志并最小修复；若 focused path 通过，再写新的 compiled receipt。

## 明确保留 OPEN

- dense `M0_CC⁻¹` metric transport / weighted-square reification；
- deployed DH/source expression binding for `ell` / `r`；
- matching-metric port cap；
- source/domain/path coverage；
- Float64 / FD / controller / solve；
- P8 ODE / flowpipe coverage；
- parent admission / registry mutation / final integration。

当前只允许 `pending`。

**待封不觉独立验证 / 待梁智炜最终整合**。
