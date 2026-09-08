---
kind: review_result
review_id: T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE-sumengchen-20260908T2022Z
task_id: T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE
source_agent: 苏梦辰
created_at: 2026-09-08T20:22:00Z
upstream_task: GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL
upstream_review: agent_review_inbox/review-GH-MATH-P4-JOINT6-ACTUAL-RESIDUAL-liuguanyi-20260908T2010Z.md
inspected_upstream_commit: 196aa849e029c84327b6acfcba19c945a74753c9
candidate_commit: b813a84ceba49c9a16aff51053e9189004327b7e
candidate_path: examples/routeb_p4_joint6_rational_residual_bridge_lean/
admission: pending
status: pending-real-github-actions
registry_mutation: false
---

# T-P4-JOINT6-RATIONAL-RESIDUAL-BRIDGE — Lean decomposition / portable sidecar

## Mathematical input consumed

柳冠一 isolated the source-independent rational residual bridge for the principal compact joint6 branch.  For actual/contract residuals `N_a/D_a` and `N_c/D_c`, the signed cross mismatch is formed first,

`Q = N_a D_c - N_c D_a`,

and denominator evidence is kept separately.  The deployed principal-branch CSE/source packet is still missing, so this child deliberately formalizes only the exact algebraic adapter and cannot instantiate a physical joint6 residual claim.

## Lean sidecar

Created `examples/routeb_p4_joint6_rational_residual_bridge_lean/` with:

- `P4Joint6RationalResidualBridge.lean`
- `README.md`
- `lean-toolchain` = `leanprover/lean4:v4.32.0`
- `verify.sh` marked `CI_PORTABLE=1`, resolving `lake` and `lean` from `PATH` and consuming the repository `examples/local_fkg/lake-manifest.json` environment.

The interface type

`ResidualCSE α CellKey SourceKey cell source`

is dependently indexed by both `cell` and `source`.  The typed adapter theorems therefore cannot directly combine actual/contract CSE objects carrying different cell or observable/source keys.

## Exported theorem decomposition

1. `ne_zero_of_pos_le_abs`
2. `rational_residual_sub_eq_cross_mul_div`
3. `rational_residual_eq_of_cross_mul`
4. `abs_div_le_of_abs_num_le`
5. `abs_den_product_lower`
6. `rational_residual_sup_le_of_cross_mul_bound`
7. `division_free_residual_sup_gate`
8. `same_cell_source_residual_eq`
9. `same_cell_source_division_free_sup_gate`
10. `quotient_difference_split`
11. `rational_residual_pair_lipschitz_of_cross_mul_packet`
12. `division_free_residual_lipschitz_gate`

This realizes the source-independent leaves requested by the mathematical review: exact cross-multiplication equality, same-cell sup containment, the division-free gate `E <= B delta_a delta_c`, the signed quotient-difference split, pairwise Lipschitz containment, and the division-free Lipschitz gate `delta L_Q + E L_P <= L delta^2`.

## Real Actions state at writeback

Workflow: `.github/workflows/lean-agent-sidecars.yml`

- run: `34273996737`
- job: `102222499532` (`portable-sidecars`)
- candidate head: `b813a84ceba49c9a16aff51053e9189004327b7e`
- checkout / pinned formal-math / checksum-verified Elan: completed successfully
- pinned local-FKG bootstrap: completed successfully
- `Run portable agent sidecars`: **in progress** at this review writeback

Therefore this review does **not** claim compile success, axiom success, or failure.  `#print axioms` and placeholder status are enforced by `verify.sh`, but their real CI result remains pending until the job reaches this sidecar and completes.  If the real job reports a Lean 4.32 error, the next 苏梦辰 pass must read that exact job log before making the minimal repair.

## Dependency / interface boundary

Closed here only at the source-independent exact-real algebra layer:

- same cell/source-key typed rational CSE interface;
- denominator nonvanishing from positive absolute lower bounds;
- signed cross mismatch before absolute-value enclosure;
- division-free sup and pairwise Lipschitz gates.

Still OPEN and intentionally external:

- principal compact `Joint6_GetStarTheta`/`zd6` actual numerator/denominator CSE;
- exact contract numerator/denominator on the same marker cell;
- same-observable/sign-convention source binding;
- exact rational `delta_a,delta_c,E` and, if needed, `L_Q,L_P` from that deployed source;
- Float64/FD/controller/solve semantics;
- P4 parent residual/source admission and comparator;
- path/domain/ODE/P8 coverage;
- any registry mutation or final workflow conclusion.

Current status is **pending**.  Even after a clean focused compile this child may only become `compiled_candidate`: **待封不觉独立验证 / 待梁智炜最终整合**.
