---
kind: review_result
review_id: review-GH-MATH-P4-TARGET-CAPS-codex-20260908T083041
task_id: GH-MATH-P4-TARGET-CAPS
source_agent: Codex-P4-math-lane
agent: Codex-P4-math-lane
created_at: 2026-09-08T08:30:41-06:00
inspected_commit: 82b257d62178940d024708570dc66f6e953919ae
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_TargetCaps.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GrowthEnvelopeBinding.lean
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_interval_branch_bound.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_certificate_V.csv
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.target_cell_to_growth_component_caps
requested_action: bind the target cell explicitly to the full ellipsoid or selected local box; retain the coercive-energy alternative and saved-storage counterexample; do not identify block storage with full energy or admit a source RHS/P_upper
---

# Full-ellipsoid and local-box inclusions succeed; saved V<=1 does not

The bounded source inspection found three distinct domains. There is a direct exact inclusion for the FULL ellipsoid used by the interval coverage driver, and also for each of the ten JSON slab boxes. Neither proves that the compact P4 target cell belongs to one of those domains. The saved four-coordinate storage sublevel does not provide the full-coordinate bounds, even when strengthened to its t² tube.

External filenames below are relative to `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/`.

## 1. Actual driver formula supplies a positive route without energy

`routeB_dense_Mq/routeB_interval_branch_bound.jl:37-43` declares proof-facing weights 3/2 and 4/5. Crucially, `p_bounds` at lines 57-68 loops over EVERY element of q and dq, not just components 4/5. `global_root` at lines 187-198 builds six-coordinate boxes using these weights. Thus its intended exact mathematical domain is

`p_full=(3/2)*sum_{j=1}^6 q_j²+(4/5)*sum_{j=1}^6 v_j² <= 28/5`.

It follows separately for every j that q_j²<=56/15<25/4 and v_j²<=7<225. With the intended disturbance condition w²<=3, this yields **|q_j|<=5/2, |v_j|<=15, |w|<=2**. Additional joint limits only restrict the domain. The stale prose calling this a block domain does not change the six-coordinate loop.

`NEW_P4_032_TargetCaps.lean::full_ellipsoid_caps` formalizes that exact implication. `target_cell_caps` requires, for one source embedding, explicit hypotheses `D(x) and cell_i(x) => p_full(embed x)<=28/5` and `w(embed x)²<=3`. It then supplies the caps on precisely that source cell. No V premise is needed. This is the minimal inclusion route if the target really is the driver's full ellipsoid.

The driver uses BigFloat arithmetic and constructs the root disturbance endpoints with `sqrt(3.0)`. This review does not equate that machine root with an exact endpoint or certify its coverage of the mathematical disturbance set. The exact theorem consumes the stated rational inequality w²<=3; arithmetic/coverage reification remains separate. Nor is p_full<=28/5 inferred from the compact producer's four-angle geometry or p45<=28/5.

## 2. The two JSON banks also fit, provided membership is proved

Exact Fraction parsing of the slab references in `combined_descriptor_remainder_v1.json` and `half_centered_bound_v1.json` gives the same five radius pairs in each bank:

| Slab index | max angle radius | max velocity radius |
|---|---|---|
| initial / half 0 | 4/25 | 3/10 |
| expanded / half 1 | 1/5 | 3/5 |
| adaptive 0 / half 2 | 1/4 | 9/10 |
| adaptive 1 / half 3 | 3/10 | 6/5 |
| adaptive 2 / half 4 | 7/20 | 3/2 |

All ten boxes therefore fit the requested component caps by exact rational comparison; their declared disturbance scope is |w|<=2. `box_caps` gives the generic pointwise inclusion from coordinate radii. These results do not assert that a target cell, full ellipsoid, initial set or trajectory is covered by these local slabs. The two banks and their controller/analytic semantics must retain their distinct provenance.

## 3. Physical V<=1 is sufficient only with its actual lower bounds

`coercive_energy_caps` explicitly consumes

`V<=1`, `(1/5)*sum q_j²<=V`, `(9401/2000000)*sum v_j²<=V`, and `w²<=3`.

The velocity comparison is exact: 9401*225=2115225>2000000. For q, (1/5)*(25/4)=5/4>1. The energy inequalities thus suffice independently of the driver ellipsoid. Energy alone does not constrain an external disturbance; `ramp_disturbance_cap` separately derives (c*t)²<=3 from c²<=3 and 0<=t<=1.

The source path for these lower bounds is a specifically shifted FULL energy: K(q,v)+(Ug(q)+Cg)+(1/2)*sum Kp_j*q_j², with zero origin gravity compensation, min Kp=2/5, nonnegative shifted gravity and the regularized full-mass coercivity 9401/1000000. `routeB_compact_closed_loop_energy_audit.jl:16-19` and `routeB_compact_energy_power_rewrite_audit.jl:105-110` record the controller/shift expressions; `routeB_compact_block_energy_barrier_audit.py:48-52,92-103` advertises their full-energy use. The target must be identified with that shifted energy and those same coordinates/mass. The sidecar does not prove those source identities. An unshifted, block-only or cross-term storage cannot inherit these lower bounds by its name.

## 4. Exact saved-storage obstruction

`routeB_export_traj.jl:66-77` loads `routeB_certificate_V.csv` with exponents only in (qa,qb,dqa,dqb,t), corresponding to physical coordinates (q4,q5,v4,v5,t). Exact decimal-rational evaluation at the zero block and t=0 gives

`V_saved(0,0,0,0,0)=-5852960231758441/50000000000000000 < 0`.

Take the six-coordinate state q=(3,0,0,0,0,0), v=(16,0,0,0,0,0), t=0, w=0. The saved storage has that same negative value: both V_saved<=1 and V_saved<=t² hold. The block p45 and the four-angle producer quadratic form are zero. Yet |q1|=3>5/2 and |v1|=16>15. The q1 value also lies inside the recorded (-pi,pi) joint limits. This gives a precise failure of the block-sublevel/tube/geometry premises to supply growth caps. It is not a claim of initial-set inclusion or an actual reachable trajectory. Its p_full=2183/10 is outside the full driver ellipsoid, so it does not contradict the positive inclusion above.

`saved_storage_counterexample` encodes the obstruction conditional on the exact CSV origin-value binding. That binding was checked by Fraction parsing, not by a Lean CSV importer; the source file contains no fake reification proof. Even at the full origin, the negative saved value prevents its identification with a globally nonnegative shifted mechanical energy without an additional shift/change of storage.

## Consequence for the growth envelope

The domain obstruction is now localized: **full-ellipsoid target cells or proved local-box members have enough coordinate restrictions; saved-block-V target cells do not.** The current generic source/ProducerChain interfaces still leave D abstract, so neither a target-cell inclusion nor a complete cover has been filled automatically. Once such an inclusion is supplied, these caps support the analytic coefficient-sum RHS proof; the equalities for the intended full DH mass/controller/C/G/FD/disturbance and descriptor remain outstanding. Caps alone do not discharge `GrowthEnvelopeBinding.source_metric_cap`'s RHS, coercivity, descriptor or projection hypotheses. No P_upper is admitted.

## Evidence

Read-only source/hash inspection and an inline Python Fraction CSV/JSON check returned exit code 0. The arithmetic check evaluated only the saved origin coefficient and compared the ten radius pairs. No Lean/Lake, Julia, producer/verifier, solver, sampling, regression or registry operation was run. The new 119-line Lean attempt contains no `sorry`/`admit`; compilation and kernel verification remain open.

| Artifact | SHA-256 |
|---|---|
| NEW_P4_032_TargetCaps.lean | 342b69f8103d4140a869e67d730bf6a6a765b15541428690d040cb5b9de6480f |
| routeB_interval_branch_bound.jl | a2bd89c923ab646bcb138372e4c74a5980afe5d5906f21080b6781e03051869c |
| routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| routeB_certificate_V.csv | cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601 |
| routeB_compact_block_energy_barrier_audit.py | 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927 |
| routeB_compact_closed_loop_energy_audit.jl | 9631e727a76ea32651ba7ca8e175e632d1ded6cda98bba2fd81e33d24f959c09 |
| routeB_compact_energy_power_rewrite_audit.jl | 7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf |
| combined_descriptor_remainder_v1.json | 68596f1557aa709d86bc8711ed7985552684dffe7fde290abf03b511f6bd9805 |
| half_centered_bound_v1.json | 225dac3905b873b1fc4b8e2f4f5333cd985b909643c651cd63146a506f2e9dfc |

Disposition: pending / OPEN_UNCOMPILED, final_integration:false.
