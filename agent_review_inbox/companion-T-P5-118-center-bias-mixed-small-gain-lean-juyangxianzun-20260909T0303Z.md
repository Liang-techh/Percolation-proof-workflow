---
kind: companion_log
task_id: T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN
agent: 巨阳仙尊
source_agent: 巨阳仙尊
created_at: 2026-09-09T03:03:00Z
upstream_review: agent_review_inbox/review-T-P5-118-CENTER-BIAS-MIXED-SMALL-GAIN-guyuefangyuan-20260909T0224Z.md
upstream_review_commit: d74f645aefcd7e485cd3b6df03d20b39e4e03826
implementation_head: d72cee4e29fa88d97e595d266022280dc0e58a00
status: lean_implemented_ci_running
integration_status: pending
admission_label: pending
source_binding_proven: false
coverage_proven: false
registry_eligible: false
formal_certificate_allowed: false
---

# 巨阳仙尊 — T-P5-118 Lean sidecar implementation

## Implemented portable sidecar

- Lean: `examples/routeb_p5_center_bias_mixed_small_gain_lean/P5CenterBiasMixedSmallGain.lean`
- boundary README: `examples/routeb_p5_center_bias_mixed_small_gain_lean/README.md`
- pinned toolchain: `examples/routeb_p5_center_bias_mixed_small_gain_lean/lean-toolchain` = `leanprover/lean4:v4.32.0`
- portable verifier: `examples/routeb_p5_center_bias_mixed_small_gain_lean/verify.sh`
- focused dispatch: `examples/000_juyang_formal_focus/verify.sh`

`verify.sh` uses `lake`/`lean` from `PATH`, checks the sidecar toolchain against `examples/local_fkg/lean-toolchain`, requires `examples/local_fkg/lake-manifest.json`, runs `lake env lean -DwarningAsError=true`, scans `sorry/admit`, and requires a `#print axioms` report for every public theorem.

## Public theorem decomposition

1. `weighted_quadratic_bias_identity`: exact `(r+s)(sQx+rQb)-rsQ(x+b)=Q(sx-rb)` identity for an explicitly typed real-module PSD quadratic kernel.
2. `quadratic_add_weighted`: root-free weighted PSD split.
3. `biased_displacement_linear_le`: `m Q(x) <= V` and `Q(b) <= B` feed the cross-multiplied biased displacement bound.
4. `biased_displacement_sq_le`: on `0 <= V <= R`, squares the packet and consumes only `V^2 <= R V`.
5. `mixed_power_square_bound`: uncancelled relative/additive coefficient gates imply the mixed power-square bound without division by the positive common scale.
6. `square_completion_power_absorption`: exact square-completion consumer converts the power-square packet into `pA <= alpha V + beta + theta Qd`.
7. `biased_anchor_power_absorption`: composed mixed absorption theorem.
8. `biased_anchor_mixed_small_gain`: substitutes the absorbed power bound into the Lyapunov ledger.
9. `mixed_small_gain_strict_reserves`: `alpha<c`, `theta<1` preserve strict storage and dissipation coefficients.
10. `mixed_small_gain_boundary_inward`: division-free `beta <= (c-alpha)R0` gate gives inward derivative at `V=R0` when `theta<=1`.
11. `nonzero_bias_zero_floor_counterexample`: exact scalar saturated packet showing a genuine nonzero-bias premise set can permit outward derivative at zero storage, so positive zero-floor dissipation reserve is not derivable from these premises alone.

The quadratic theorem uses a deliberately explicit `PSDQuadraticModuleKernel` interface (`Q`, polarization `B`, add/sub expansion, scalar-square law, scalar bilinearity) rather than assuming the weighted split as an opaque premise.

## Current GitHub Actions evidence

Implementation/focused head: `d72cee4e29fa88d97e595d266022280dc0e58a00`.

Real workflow currently running:

- workflow: `Lean agent sidecars`
- run: `34305224255`
- job: `102320401805` (`portable-sidecars`)
- bootstrap `examples/local_fkg` step: completed successfully
- `Run portable agent sidecars`: still in progress at this writeback

Therefore this companion log does **not** claim compile success, `AXIOM_AUDIT=PASS`, absence of `sorryAx`, or `compiled_candidate` yet. The next 巨阳仙尊 round should read the completed job log first; if this sidecar has a Lean/type/tactic/linter failure, repair that exact failure before taking new math work. If it passes, record the lane-local `PLACEHOLDER_SCAN`, focused marker, and all 11 `#print axioms` reports in a new review/companion result.

## Deliberately open boundaries

Still outside this sidecar: deployed `storageKey`/`anchorKey`, actual center offset and `Q_Z(b)<=B` source proof, actual centered comparator, deployed `h/gamma/d`, signed-correlation refinement, same-segment/same-storage-domain coverage, concrete `(alpha,beta,theta,R0)` margin selection, Float64/FD/controller/runtime semantics, P8 flowpipe, independent verification, admission and registry.

**待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合。**
