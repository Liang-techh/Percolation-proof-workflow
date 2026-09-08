---
kind: review_result
task_id: T-P5-039
review_id: review-T-P5-039-sumengchen-20260907T1955
agent: 苏梦辰
source_agent: 苏梦辰
upstream_review: review-T-P5-039-guyuefangyuan-20260907T1931
status: compiled_candidate
created_at: 2026-09-07T19:55:00-06:00
---

# T-P5-039 — exact Pareto optimizer Lean formalization

## Scope

Formalization-only follow-up to 古月方源's exact optimizer for the T-P5-038 Pareto quarter-barrier family. This review does not repeat the T-P5-038 first-exit proof, does not claim any deployed source/Float64/ODE binding, and does not mutate registry/admission/parent status.

The mathematical gate is

`300000 * E4 + 1200 * (250 + 53*r) * E5 < (109-r) * (250 + 53*r)`, with `0 ≤ r ≤ 1`.

Writing

- `A = 27250 - 300000*(E4+E5)`
- `B = 5527 - 63600*E5`
- `margin A B r = A + B*r - 53*r^2`

reduces the search over the entire convex family to an exact concave quadratic optimizer.

## Lean sidecar

Portable sidecar:

- `examples/routeb_p5_pareto_optimizer_lean/P5ParetoOptimizer.lean`
- `examples/routeb_p5_pareto_optimizer_lean/lean-toolchain`
- `examples/routeb_p5_pareto_optimizer_lean/README.md`
- `examples/routeb_p5_pareto_optimizer_lean/verify.sh`

Pinned toolchain: `leanprover/lean4:v4.32.0`. `verify.sh` resolves `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg`, runs with `-DwarningAsError=true`, is registered with `CI_PORTABLE=1`, checks every exported theorem's `#print axioms`, and rejects `sorryAx`.

Source commits from this formalization pass:

- claim: `f386d53e28e92d3650a6143faff6c5fdfa2250fa`
- Lean file: `0e378ba3e2ba9b1e02c41bfe9ada039f70e00e9b`
- pinned toolchain: `805f7cce97c09f31a0e54fdd2cf2b52a93b864a3`
- README: `50903eef0601a874a2b7120f76b357ce0399c8af`
- portable verifier: `f0714487c46f119369ec040e26990c86de29e861`

## Kernel theorem surface

The sidecar exports 17 focused theorems under `RouteBP5ParetoOptimizer`:

1. `pareto_margin_expand` — exact expansion from the source-facing gate to `A + B*r - 53*r^2`.
2. `pareto_margin_left_max` — if `B ≤ 0`, `r=0` is maximal on `r≥0`.
3. `pareto_margin_right_max` — if `B ≥ 106`, `r=1` is maximal on `r≤1`.
4. `pareto_margin_vertex_gap` — exact square-completion gap at `r=B/106`.
5. `pareto_margin_vertex_max` — the unconstrained vertex is the global quadratic maximum.
6. `pareto_margin_vertex_value` — exact value `A + B^2/212`.
7. `pareto_vertex_mem_Ioo` — `0 < B < 106` implies `B/106 ∈ (0,1)`.
8. `paretoOpt_mem_Icc` — the piecewise rational optimizer always lies in `[0,1]`.
9. `pareto_optimal_selector` — every admissible `r` is dominated by `paretoOpt B`.
10. `pareto_vertex_positive_iff` — interior positivity iff the division-free check `0 < 212*A + B^2`.
11. `pareto_gate_exists_iff` — exact necessary-and-sufficient feasibility theorem for the whole one-parameter family.
12. `pareto_gate_impossible_of_branch_nonpositive` — branchwise nonpositive maxima imply no admissible parameter can pass.
13. `pareto_interior_strict_gain_over_left` — positive interior slope gives strict gain over `r=0`.
14. `pareto_interior_strict_gain_over_right` — `B<106` gives strict gain over `r=1`.
15. `pareto_selector_right_threshold` — `B≥106 ↔ E5≤1807/21200`.
16. `pareto_selector_left_threshold` — `B≤0 ↔ 5527/63600≤E5`.
17. `pareto_interior_endpoint_failure_witness` — exact rational regression witness where both endpoint certificates fail but the interior optimizer succeeds.

The exact optimizer represented by `paretoOpt` is therefore:

- `r*=0` if `B≤0`,
- `r*=1` if `B≥106`,
- `r*=B/106` if `0<B<106`.

The corresponding exact maximum margins are `A`, `A+B-53`, and `A+B^2/212` respectively. In the interior branch the search has been eliminated completely by the polynomial check `212*A+B^2>0`.

The regression witness is frozen exactly as

- `E5 = 2737/31800`,
- `E4 = 75803/15900000`,
- hence `A=-1`, `B=53`,
- endpoint margins are both `-1`,
- while `r=1/2` has margin `49/4 > 0`.

This prevents later checker code from silently reducing the family back to endpoint-only search.

## Real CI result

A later main-branch Actions run containing this sidecar executed it under the pinned environment:

- workflow run: `34177786357`
- job: `101910553244`
- Lean: `4.32.0`
- Lake: `5.0.0`

The focused log for `examples/routeb_p5_pareto_optimizer_lean/verify.sh` reports:

- `AXIOM_AUDIT=PASS`
- `P5_PARETO_OPTIMIZER_FOCUSED_CHECK=PASS`
- `T_P5_038_FIRST_EXIT_REUSED_NOT_DUPLICATED=true`
- `SIDECAR_RESULT=PASS path=examples/routeb_p5_pareto_optimizer_lean/verify.sh`

All 17 exported theorem reports contain only `[propext, Classical.choice, Quot.sound]`; this sidecar has no `sorryAx`.

The aggregate `portable-sidecars` job is still red, but the failures are outside T-P5-039. The same real log shows unrelated pre-existing failures in the FLT quotient path, M4 cross-branch, P4 shifted-common-reserve, P5 componentwise/parameter-tube/weighted-dual-residual, P7 tail-Schur, and old P8 ramp-reconstruction sidecars. I did not claim or modify those tasks.

## Dependencies and interface boundary

Mathematical/formal dependencies are the P5 Pareto endpoint family and first-exit consumer already developed in `T-P5-036`, `T-P5-037`, and `T-P5-038`; this sidecar only solves the exact parameter-selection layer and deliberately reuses rather than duplicates the T-P5-038 first-exit theorem.

Still open upstream/downstream obligations:

- same-domain source certificates for the actual componentwise `E4` and `E5` bounds;
- typed/deployed source identity for those bounds;
- true-DH plus Float64/FD/controller/solve execution-remainder binding;
- P8 same-domain ODE existence/continuation and flowpipe coverage;
- final P5/P8/M4 composition, conflict handling, DAG/registry update and admission decision.

No provenance/receipt/admission work was performed. No parent status, global conclusion, DAG, or registry was mutated.

**Status: compiled_candidate — 待封不觉独立验证 / 待梁智炜最终整合。**
