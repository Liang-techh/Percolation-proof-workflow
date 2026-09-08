---
kind: review_result
review_id: review-GH-MATH-P4-SOURCE-ELLIPSOID-BINDING-codex-20260908T084123
task_id: GH-MATH-P4-SOURCE-ELLIPSOID-BINDING
source_agent: Codex-P4-target-cell-inclusion
agent: Codex-P4-target-cell-inclusion
created_at: 2026-09-08T08:41:23-06:00
inspected_commit: 154a11ebc578c93d4e4f670d2d4c414b00ac6eb7
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCellInclusion20260908.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCaps.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GrowthEnvelopeBinding.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.lean
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_interval_bounds.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/dhport_lib.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_certificate_manifest.toml
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_full_dh_growth_bound.py
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_composed_interval_probe.py
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/half_centered_bound_v1.json
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
source_binding_status: pending
coverage_status: pending
parsed: false
elaborated: false
kernel_checked: false
axioms_checked: false
verified: false
final_integration: false
registry_promoted: false
comparator_accepted: false
formal_certificate_allowed: false
proposed_integration_target: P4.same_source_target_cell_and_FD_stencil_inclusion
requested_action: consume the exact inclusion candidates only after authoritative target/coordinate binding; retain evaluation-stencil enlargement, a proved target cover, and the explicit source-model/FD/solve obligations; do not infer coverage from saved V or JSON labels
---

# P4 target-cell inclusion: exact slack, stencil enlargement, and missing source cover

The new file contains nine source-independent mathematical theorem candidates. It advances the geometry of the intended inclusion; it does not identify the actual P4 source domain with that geometry. No Lean/Lake, Julia, producer, solver, comparator, intake/integration command or registry operation was run. All Lean proof bodies remain uncompiled.

The inspected commit records the workspace snapshot at the check. External sources are separately identified by paths and hashes below; that workspace commit does not authenticate the external Julia/Python files or the deployed dynamics. Existing TargetCaps, shared adapters, source drivers and state/registry files were not edited in this task. Deliverables are the new Lean sidecar and this review_result.

## 1. Exact positive inclusions

Write E for the full-state region

```text
p_full(q,v) = (3/2) sum_{j=1}^6 q_j^2 + (4/5) sum_{j=1}^6 v_j^2 <= 28/5.
```

Nonnegativity gives q_j^2<=56/15<4 and v_j^2<=7<9. Thus `full_ellipsoid_tight_caps` supplies |q_j|<=2 and |v_j|<=3. This retains useful slack that is lost if one immediately relaxes to the old GrowthCaps bounds 5/2 and 15.

For any perturbation delta with |delta_j|<=1/2, triangle inequality gives

```text
|q_j+delta_j| <= 2+1/2 = 5/2;
|v_j| <= 3 <= 15;
w^2<=3 implies |w|<=2.
```

`full_ellipsoid_stencil_caps` encodes this implication. In particular it covers every exact FD segment q+s*e_k with |s|<=h=1/100000. It preserves velocity, disturbance and time. It does not claim that the perturbed state remains in E or that it is physically reachable.

For a centered local box the sufficient conditions are instead

```text
|q_j-qc_j|<=qr_j,  |v_j-vc_j|<=vr_j,
|qc_j|+qr_j+h<=5/2,  |vc_j|+vr_j<=15,
|delta_j|<=h,  |w|<=2.
```

`centered_coordinate_cap` and `centered_box_stencil_caps` prove the corresponding algebraic implications. Checking just the radius silently assumes a zero center. The exact condition above also accounts for the FD halo; merely checking the original box is insufficient when a coordinate saturates 5/2.

Live reading of the ten JSON slab files referenced by the two banks gives the same five angle/velocity radius pairs in each bank: (4/25,3/10), (1/5,3/5), (1/4,9/10), (3/10,6/5), (7/20,3/2). Half-domain files also list all six angle radii explicitly. For these origin-centered modeled boxes, even the largest angle radius plus 1/100000 is below 5/2. The bounds are sufficient conditional on actual box membership and correct interpretation of the JSON domain; no membership or physical evolution follows from this text extraction. Their step fields are 1/256 and 1/512, respectively; they are not a demonstrated time partition covering [0,1].

## 2. Same-coordinate ramp and cover interface

`RampCoordinates X` contains explicit q, velocity, amplitude and time accessors. `rampState` uses precisely those accessors and sets disturbance=amplitude*time. This prevents independent choices of w in the inclusion proof, but it does not authenticate the accessors against an external source.

`covered_ramp_target_caps` requires all of the following on the original D:

- A cover proof: for every x in D there is a cell i containing x.
- For that same x and every applicable cell, p_full(rampState x)<=28/5.
- The same amplitude satisfies c(x)^2<=3, and the same time satisfies 0<=t(x)<=1.

It returns a containing cell, GrowthCaps for the original state, and GrowthCaps for every perturbation with coordinate size <=1/2. Neither D nor the cover is constructed by this theorem. Defining new cells as old cells intersected with E proves a cover only of D intersected with E unless D subset E is separately proved. This is the exact remaining source-domain obligation.

The cover interface only requires existence of a containing cell. Disjointness is not needed for this pointwise use or for `SameSourceCharges.cover`; a later counting or additive decomposition may impose separate partition obligations. If a bound depends on saved storage/time, the same cell bounds must also be valid for the intended time values; a q/v/w-only spatial table does not certify a time-dependent base inequality.

## 3. Strict stencil non-closure counterexample

`ellipsoid_not_stencil_closed` uses an entirely rational boundary point:

```text
q = (0,0,0,0,0,0), v = (2,1,1,1,0,0), w=t=0.
sum v_j^2 = 7, so p_full = 28/5.
p_full(q+s*e_1,v) = 28/5 + (3/2)s^2 > 28/5 whenever s != 0.
```

Consequently no positive FD step makes E closed under all its required coordinate perturbations. Source equations established only on E cannot automatically be used for mass/potential at the shifted endpoints. The new positive theorem places those endpoints in the larger GrowthCaps box, not back in E. This obstruction is about evaluation domains, not an ODE trajectory or failure of the physical target.

The required analytic evaluation domain can be written

```text
Omega contains { q(x)+s*e_k : x in the target cell, |s|<=h, k=1..6 },
and contains { s*e_k : |s|<=h, k=1..6 } for G_h(0).
```

For centered mean-value/Taylor enclosures, the entire expanded segment/box must be in Omega, not only q+h*e_k and q-h*e_k. The source at `routeB_interval_bounds.jl:478,532,584` explicitly constructs such expanded boxes. If the DH/Fourier identity and derivative/error bounds are proved globally in q, Omega can be all R^6 and no physical joint-limit extension is needed for those analytic evaluations. A periodic coefficient bound is not itself that global source identity.

## 4. Strict coverage obstruction for the local bank

`small_boxes_do_not_cover_full_ellipsoid` takes q=(1,0,0,0,0,0), v=w=t=0. Its p_full=3/2<=28/5. Every box with |q_1|<=7/20 excludes it. Hence the ten inspected modeled boxes cannot cover the entire E, even though each box individually has ample GrowthCaps slack.

This does not refute inclusion of a smaller reachable set in their union. Such a result requires an independent all-initial-conditions flowpipe/barrier argument and valid transitions/time coverage for the same vector field. It cannot be supplied by a bank's status, source_hashes, radius values or formal=false/true labels.

There is also a pre-existing target mismatch that this file deliberately leaves open. The authoritative-candidate manifest at `routeB_dense_Mq/routeB_certificate_manifest.toml:25` describes p45, using only q4,q5,v4,v5. In contrast, the coverage driver `p_bounds` at lines 57-68 sums all six q and all six v. At q=(2,0,0,0,0,0), v=0, p45=0 but p_full=6>28/5, within the recorded q1 joint limits. Thus p45 plus joint limits does not imply E. Remote velocity can likewise violate GrowthCaps while p45 is zero. These are domain counterexamples, not claims that these points arise from the original small initial ball.

E does imply the compact producer's four-angle quadratic restriction by dropping the other nonnegative squares. The projection must be exactly angles=(q2,q3,q4,q5); its joint-3 interval follows from the actual joint limits (or the tighter coordinate bound and a bound on pi). The converse fails. A four-angle operator table must additionally be identified with the full-source operator under that projection; omitted-coordinate invariance must be proved, not inferred from table shape.

## 5. Disturbance endpoints and arithmetic interpretation

The exact ramp premises c^2<=3 and 0<=t<=1 imply w^2=(ct)^2<=3. `ramp_outer_interval` shows that any nonnegative rational u with u^2>=3 encloses every such w. For example u=7/4 gives an exact outer endpoint smaller than the GrowthCaps limit 2, without computing sqrt(3).

The inspected `routeB_dense_Mq/routeB_interval_branch_bound.jl:198` constructs its root with `bi(-sqrt(3.0),sqrt(3.0))`. `bi` at `routeB_interval_bounds.jl:95` outward-converts its already-computed inputs to BigFloat; that conversion does not establish outward rounding of the earlier Float64 square root. This must be reified separately.

The new `undersized_disturbance_root` provides a conditional exact diagnostic:

```text
u = 3900231685776981 / 2251799813685248,
c = 31201853486215849 / 18014398509481984.
c > u, c^2 < 3.
```

The last inequality reduces to the positive integer

```text
3*(18014398509481984)^2 - (31201853486215849)^2 = 50407222242937967.
```

Thus a root ending at this exact u misses an allowed ramp value already at t=1. This task did not execute Julia or bind an actual sqrt return value to u; the theorem does not assert that runtime identity. The source inspection establishes the missing outward-root obligation, and the dyadic example demonstrates its mathematical consequence. A separate `robot_final/routeB_interval_branch_bound.jl` currently uses a different construction and has a different hash; that file cannot silently repair or authenticate the selected `routeB_dense_Mq` source.

A simple exact replacement specification for an E-cover root is [-2,2]^6 for q, [-3,3]^6 for v and [-7/4,7/4] for w, with [0,1] for time if needed. This is a specification only; no driver was edited. Finite subdivisions must preserve this outer cover and justify every discarded child with a sound exact/outward exclusion test, including boundary points. The root rectangle itself is not contained in E; bounds may be proved on its intersection with the original target domain.

## 6. Required next true-DH/source binding

The minimal next result must instantiate the coordinate map and original D, rather than add another abstract cap premise. It needs the following exact hypotheses or explicit defect bounds:

1. Target identity and quantifiers. Select the intended p45 region, full E region, or reachable-state domain without silently replacing one by another. Bind all 12 state coordinates, zero/one-based projections, time and ramp amplitude to the source. For a reachable-domain route, preserve the full 12-dimensional initial ball of radius 3/20 and all allowed inputs; supply the all-time inclusion/first-exit argument and continuation. Saved block V<=1 or V<=t^2 does not supply full-state coercivity or this cover.
2. One DH mass/potential source on Omega. Identify the full six-body M and U with the exact-real structural/Fourier objects, with regularizer 1/1000000 and the same DH parameters, COM convention and inertia normalization. An equality known only at cell centers, or only inside E, does not bind FD endpoints outside E.
3. One FD semantics. Bind h=1/100000, the endpoint maps q+/-h*e_k, and the common denominator 2h to C_h and G_h; supply the analytic derivative/remainder hypotheses on their full segments when using mean-value/Taylor bounds. `dhport_lib.jl:73-99` converts its step to Float64, while the interval file sets HFD from a BigFloat decimal string. Neither is definitionally the rational real h. If Float64 execution remains the target, enclose the actual step, rounded endpoint additions, denominator, trigonometry and accumulation errors explicitly. The available 1/2 geometric slack does not prove those error bounds.
4. Same controller/input and solve. Bind Kp, Kd+b_fr, GW, G_h(0), and w=ct, then prove the full six-row descriptor M*a=rhs or account for its solve residual. Source `exact_ddq` is implemented with floating-point linear solve; its name is not an exact descriptor theorem. Bind a4/a5 projections to the same acceleration used in the producer metric. Coercivity mu remains distinct from P4 normalization nu.
5. Actual covering cells and local certificates. Prove D subset union_i cell_i for the same interpreted endpoints and source. Then supply RHS component bounds, operator/port bounds and the time-dependent A/P/D envelopes on those same cells. `GrowthEnvelopeBinding.source_metric_cap` still requires hR, hcoercive, heq and both projections. Geometric GrowthCaps alone fills none of these semantic equalities or certified bounds.

If the target really is E and the exact-real source identity holds globally, the shortest path is: reify a rational root and cover, instantiate `RampCoordinates`, apply `covered_ramp_target_caps`, and separately transfer the global Fourier/FD RHS bounds. If the target is the manifest's p45 or saved-storage domain, the missing all-coordinate inclusion is a genuine additional obligation, not a notation repair.

## 7. Evidence and disposition

Performed only source reads, targeted text searches, hash inspection, the ten-box JSON field extraction and exact BigInteger arithmetic for the dyadic diagnostic. No broad regression or sampled numerical verification was run. One JSON display command initially had a PowerShell pipeline syntax error; it was corrected by collecting rows before formatting. Two text-search invocations had path/flag syntax errors and were replaced with explicit paths. These diagnostics did not execute any source producer or alter its inputs.

The new Lean file has nine theorem declarations and no sorry/admit/axiom/native_decide/unsafe/implemented_by tokens or trailing whitespace in the inspected text. This is not a parser, import, tactic or axiom audit. The file imports existing TargetCaps and its uncompiled source chain, so import resolution and all inherited/current proof bodies remain outstanding. In particular `nlinarith`, finite-sum reduction and large-rational `norm_num` have not run.

| Artifact | SHA-256 at inspection |
|---|---|
| NEW_P4_032_TargetCellInclusion20260908.lean | dfb06443abc4cdf90296c8de7b4ccfdbdba914011480f780a9eae942cf5920ee |
| NEW_P4_032_TargetCaps.lean | 342b69f8103d4140a869e67d730bf6a6a765b15541428690d040cb5b9de6480f |
| routeB_dense_Mq/routeB_interval_branch_bound.jl | a2bd89c923ab646bcb138372e4c74a5980afe5d5906f21080b6781e03051869c |
| routeB_dense_Mq/routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_dense_Mq/routeB_certificate_manifest.toml | d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495 |
| routeB_dense_Mq/routeB_compact_full_dh_growth_bound.py | 49bd543e4754ffae7d54764cdb4b6a39a0bf637ec0b0891dfe46885c9d8a1288 |
| routeB_dense_Mq/routeB_compact_composed_interval_probe.py | ab6a4e34ecb391247eef796496f57b28407587b366c360f4e0ad441fedd04ba6 |

Disposition: pending / OPEN_UNCOMPILED. Exact inclusion and obstruction candidates are available for review. True-DH target identity, evaluation-domain identity, finite cover, source bounds, Lean compilation and admission are not supplied by this result.
