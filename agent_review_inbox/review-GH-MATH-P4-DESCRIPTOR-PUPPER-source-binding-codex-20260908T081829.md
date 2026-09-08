---
kind: review_result
review_id: review-GH-MATH-P4-DESCRIPTOR-PUPPER-source-binding-codex-20260908T081829
task_id: GH-MATH-P4-DESCRIPTOR-PUPPER
source_agent: Codex-P4-math-lane
agent: Codex-P4-math-lane
created_at: 2026-09-08T08:18:29-06:00
inspected_commit: 1f7592f29f9bec8e29b689db30c416b6655dcff6
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GrowthEnvelopeBinding.lean
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/dhport_lib.jl
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_full_dh_growth_bound.py
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.same_cell_full_descriptor_P_upper.source_binding
requested_action: retain the sourced conditional mu/H/K interface; prove target-cell component bounds and exact-real DH semantic equalities before using it; do not admit a numerical P_upper or promote the registry
---

# A sourced growth envelope exists; its target-cell binding remains open

This round locates concrete rational mass/RHS evidence that the preceding descriptor-interface review had not consumed. It also resolves the zero-gravity-offset seam for the exported exact-real Fourier model. It does not establish a target-cell P_upper.

All external filenames below are relative to `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`. Source inspection, coefficient arithmetic and mathematical implications are distinguished from source authentication and Lean compilation.

## 1. Mass lower bound has a specific structural source

`dhport_lib.jl:44-60` sums positive translational Gram terms and isotropic rotational terms with weights

`I_j/3 = (1/3, 1/5, 7/60, 1/15, 1/30, 1/60)`,

then adds the default regularizer `1/1000000`. `routeB_compact_rotational_mass_lower_certificate.py` forms the scalar prefix Gram `G=R' diag(I_j/3) R`, where `R_ij=1` for j<=i. It records six positive leading minors for `G-(47/5000)I`, hence the candidate full-mass constant is **mu=9401/1000000**.

The geometric transfer is explicit: put u_j=z_j*a_j in R^3 and apply the scalar Gram inequality to each Cartesian component. Since every exact DH axis is unit, sum_j ||u_j||²=sum_j a_j². Exact rotation orthogonality makes the isotropic world inertia equal to `(I_j/3)I`. Dropping the nonnegative translational terms and adding the regularizer gives the full six-row coercivity premise. This argument uses neither axis alignment nor a Schur inverse. It applies to the exact-real default regularized model; it does not certify rounding in the Float64 Gram construction or an unregularized invocation. The recorded determinant result was read, not rerun or kernel-verified this round.

## 2. RHS coefficients and a resolved G(0) seam

`routeB_compact_full_dh_growth_bound.py` uses the same decimal-rational controller coefficients as the exact-real interpretation of `dhport_lib.jl:14-17,102-110`: Kp, Kd+b_fr, and `(gw_coef*I_val)`. It bounds the FULL force

`rhs=-Kp*q-(Kd+b_fr)*v+G_h(0)+GW*w-C_h(q,v)*v-G_h(q)`

for h=1/100000, default regularization, and component restrictions **|q_j|<=5/2, |v_j|<=15, |w|<=2**. The script advertises these restrictions on the physical-energy domain V<=1. It reads analytic Fourier C/G coefficient sums and adds the exported central-FD derivative errors; these are not Float64 roundoff bounds.

There was a potential offset seam: Julia uses G_h(0), while the growth script uses analytic G(0). Inspection and exact coefficient arithmetic found that the potential CSV has **17 terms**, all coefficients real and satisfying a(-nu)=a(nu). Thus its exact potential U satisfies U(-q)=U(q), so U(h e_j)=U(-h e_j) and G_h(0)=0 for every h!=0. Its analytic gradient at zero is also zero, consistent with the gravity CSV. Consequently no extra zero-offset error is needed for THIS exact-real Fourier potential. This does not show bitwise/roundoff equality for the deployed Julia potential; the latter still needs a source/roundoff bridge. It also does not justify deleting a nonzero offset in a different controller.

Using exact Fraction addition on the recorded C/G/FD rows, with

`dc_ijk=(dm_ijk+dm_ikj+dm_jki)/2`,

`R_j=Kp_j*(5/2)+d_j*15+GW_j*2+|G_j(0)|+225*(sum_kl |C_jkl|+sum_kl dc_jkl)+|G_j|_coeff+dg_j`,

gives the following component envelope candidates. Fourier coefficient modulus is relaxed to |Re|+|Im|, matching the producer.

| j | R_j |
|---|---|
| 1 | 73439445001755279/320000000000000 |
| 2 | 911524590020108399/6400000000000000 |
| 3 | 3285221030062038663/32000000000000000 |
| 4 | 7555186660118404261/64000000000000000 |
| 5 | 1453164205023427893/16000000000000000 |
| 6 | 214400000003/4000000000 |

Their maximum is **R=73439445001755279/320000000000000**, at component 1, exactly matching the stored growth CSV. This is a maximum of componentwise SUMS; maxima of C, G and torque occur at different components and must not be confused with that calculation.

## 3. Concrete conditional H/K values, with the missing hypotheses exposed

If the target cell supplies the SAME rhs and all six bounds |rhs_j|<=R, choose the uniform cell envelope

`H_i=H=6 R²=16180056246497515293490173013103523/51200000000000000000000000000`.

With Bmax=1402217/12000000 and the sourced candidate mu, set

`K_i=K=Bmax*H/mu²=7562649976598335467430636643971660903497/18099978444800000000000000000000`.

These are exact algebraic consequences of the sourced candidates, not measured acceleration maxima. In particular Bmax*H=mu²*K. The independent uncompiled `NEW_P4_032_GrowthEnvelopeBinding.lean` defines those rationals, proves a six-component sum interface, and feeds the existing descriptor theorem with **explicit** coercivity, full descriptor equality, RHS component bounds and a4/a5 projection equalities. It does not populate those hypotheses from CSV filenames. A tighter H=sum_j R_j² is possible but is not needed to resolve the semantic bottleneck.

Once the hypotheses are proved on each source cell, the earlier `same_cell_P_upper` theorem can consume these H/K values and a SAME-cell relative-port inequality with `rhoSq_i*K<=P_i`. No rhoSq from a different ledger/branch/metric is inserted here. K>100000000 by exact arithmetic; this continuation envelope therefore does not by itself demonstrate a usable positive-margin allocation. No concrete P_i or D_lower is submitted.

## 4. Exact remaining obstruction and smallest binding contract

The producer geometry and p45 bound do not imply the growth-domain restrictions. In the state model restricted only by the four-angle producer geometry and p45<=28/5, take q=(s,0,0,0,0,0), v=0, w=0. Both restrictions hold for every s. The exported exact potential is independent of q1, so G_h,1(q)=G_h,1(0)=0, and the velocity-quadratic Coriolis term vanishes. The exact controller then has **rhs_1=-s**. Choosing s=R+1 defeats |rhs_1|<=R. This is a force/domain counterexample to the sufficiency of those two restrictions, not proof that this state lies in the full physical target domain, and not an unbounded-port claim.

For target source D and cell_i, the next obligation can be weaker than V<=1: prove directly

`D(x) and cell_i(x) => (forall j, |q_j(x)|<=5/2 and |v_j(x)|<=15) and |w(x)|<=2`.

Alternatively prove inclusion in a specifically defined physical-energy sublevel AND its coordinate lower-bound theorems. An intersection with V<=1 only proves a result on that intersection; it does not recover the original cover. Existing block/angle constraints leave q1 and remote velocities uncontrolled. A trajectory/barrier argument is unnecessary for this pointwise transfer if these component caps can be established independently.

The remaining SAME-source obligations are: equality of target mass with the exact-real structural/Fourier mass plus this regularizer; equality of target C/G with the central-FD model at this h (or an explicitly absorbed defect); equality of controller/disturbance coefficients and gravity offset; the full six-row descriptor and a4/a5 projections; and the relative port inequality in the same metric/domain. If Float64 execution remains authoritative, add roundoff and descriptor-solve residual bounds, or explicitly select the exact-real model as authoritative. Reading matching parameter text and matching rational arithmetic is not a proof of these identities. Scalar normalization nu remains distinct from coercivity mu.

## Evidence and disposition

Read-only `Get-Content`, `rg`, `Get-FileHash`, `git rev-parse HEAD` and the inline Python Fraction/CSV arithmetic returned exit code 0. The arithmetic check only read existing CSVs, checked potential coefficient parity, added six component envelopes and evaluated H/K. No external producer or verifier was imported/executed. No Lean/Lake, solver, Julia, sampling, regression, intake, integration or registry mutation was run. The added Lean file remains OPEN_UNCOMPILED; import/elaboration and kernel verification are outstanding.

| Source/artifact | SHA-256 |
|---|---|
| NEW_P4_032_GrowthEnvelopeBinding.lean | 09b872b69472379fbfc8afd9f933011e95630827d71bc25b9515d3432cafb82e |
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| rotational mass lower producer | 5f7ba3e31f7f2dc99ad1e28fbf2d5218c7cd81ef51a5469a7b493e5f379512e1 |
| rotational mass lower CSV | e5386990995f592b1d31a36664addb7dd22157a65db10b1b370ef59e20c8c481 |
| full DH growth producer | 49bd543e4754ffae7d54764cdb4b6a39a0bf637ec0b0891dfe46885c9d8a1288 |
| full DH growth CSV | 97ef9ec67360738da0125bf738e06da28a8e9ea7aa15c99b6e6d69fe496f954d |
| Fourier Coriolis CSV | 2a3004c1459c28a5e93a243d47d22ab4f18c115aeaf72cf436336a7b6c0abdd3 |
| Fourier gravity CSV | 660dda32da0dd98fe99fd86440f2fae782f0ee109839090720c4c9965e06bea4 |
| Fourier potential CSV | 4ebbb10e32639f54b18f259cbb762c04f2be842a856cae85e1fe94dad5478b6c |
| Fourier FD error CSV | 58c706d5abc8565f61cf50c1958317d04174a5def93cb15a23232d9d9b082f63 |
| analytic Fourier dynamics producer | a340d353f326b12a43564e5f0d45723a433611914038219e9e92d57fe177a9ce |
| rational Fourier structural producer | 9460181770e47be0ecbde43a8a29ef285da1168c3121fab18d5378c671401a7b |

Disposition: pending. Concrete mu/H/K candidates now have a source chain and an explicit conditional consumer. Target-cell domain and semantic binding remain open; there is no admitted P_upper.
