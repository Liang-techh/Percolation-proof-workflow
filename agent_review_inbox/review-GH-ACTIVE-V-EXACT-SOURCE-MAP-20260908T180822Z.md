---
kind: review_result
review_id: review-GH-ACTIVE-V-EXACT-SOURCE-MAP-20260908T180822Z
task_id: GH-ACTIVE-V-FUNCTION-IDENTITY
source_agent: Godel the 6th
created_at: 2026-09-08T18:08:22Z
integration_status: pending
admission_label: pending
status: CERTIFICATE_RUNTIME_CHAIN_LOCATED_ENERGY_FUNCTION_IDENTITY_INCOMPATIBLE
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
ideal_obstruction_recomputed: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: select the actual consumer function and supply its function-indexed initial witness; do not identify certificate polynomial with raw or centered mechanical energy
---

# Bounded source map: actual certificate V is a separate function

Scope: read-only inspection of the current external 6DOF source files and
literal certificate table. Only this review is written. No solver, producer,
Julia, Lean/Lake, state operation or prior ideal-envelope audit was run.

Source root E is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## 1. Located definition chain

| Source location under E | Exact role | What the edge does NOT prove |
|---|---|---|
| routeB_pmi_certificate.jl:254-265 | build_cert makes degree-4 V0(qa,qb,t), degree-1 A1/A2 and scalar Q11/Q12/Q22 decision variables | No assignment from Vfull_DH or Vshift_DH |
| same:399-415,449-455 | scalar solve, numpoly/value conversion; Vn=V0n+A1n*dqa+A2n*dqb+(Q11v*dqa^2+2*Q12v*dqa*dqb+Q22v*dqb^2)/2 | Separate scalar solve is not identity to the separately solved PMI candidate |
| same:698-712 | writes Float64 coefficients of Vn and exponents to routeB_certificate_V.csv | Decimal serialization is not an exact source theorem or Gram verification |
| routeB_export_traj.jl:66-78 | reads THAT CSV; coefficients parse as Float64, exponent tokens parse as Float64 then round/Int; stores V_coeffs and V_exps | No centering, energy substitution or coefficient cleanup occurs |
| same:114-123 | evalV_fast uses q4,q5,v4,v5,t and accumulates the stored monomials | The evaluator is not Vfull_DH, Vshift_DH or a mass-metric cross assignment |
| same:168-181 | Vv from evalV_fast is logged beside tk^2 and a bracket ratio | The neighboring tube/bracket columns do not prove a function identity |
| routeB_compact_energy_storage_to_block_audit.py:17-24,44-51,78 | independently declares mass/Hessian/eps/radius scalars and exports initial_energy_upper as initial_storage_upper | Does not read routeB_certificate_V.csv or certify its polynomial |
| routeB_compact_block_energy_barrier_audit.py:47-54,63-65 | sets V_BAR=1, reads that initial_storage_upper, forms V_TUBE=V0+gamma_eff+gravity_defect | Contains no actual V evaluator or function-selection witness |

The located read/write chain identifies which coefficient file the trajectory
exporter consumes. It does not identify that plotted V as the energy barrier's
intended V. Two unrelated meanings of V0 must also remain separate: the
certificate's polynomial decision variable V0 and the barrier's scalar V0.

## 2. Current artifact binding is real but only a byte binding

Fresh SHA256 checks found that the certificate manifest's source/export/V/DH
hashes all match the current files. The export manifest's exporter/V hashes
also match. Thus this is NOT a discovered stale-hash mismatch.

```text
routeB_pmi_certificate.jl
235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77
routeB_export_traj.jl
35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf
routeB_certificate_V.csv
cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
routeB_certificate_manifest.toml
d9ae90af1860364eae950649b3ffbf1810d78583383781ec9fa6949fdd24f495
routeB_export_manifest.toml
5b61d624f4f6060da8c33a51fa7982bef8206d2c3924babb512440defad89187
dhport_lib.jl
aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
```

The manifests themselves label evidence empirical/numerical candidate and
trajectory_monte_carlo_only, with global_box_coverage=false. Matching hashes
authenticate neither an execution nor an exact identity between functions.
No manifest timestamp or recorded Julia version is claimed as a new run.

## 3. Exact function discriminator on the SAME X0, not an envelope rerun

The 46-row CSV has one q4^4 coefficient token
`0.060398529511233624` at exponent tuple (4,0,0,0,0). All exponent tokens were
checked to be nonnegative integers. This coefficient is nonzero both as its
literal decimal rational and as the represented finite binary64 coefficient.
It is not a near-zero coefficient that the reader suppresses.

Consider the whole one-dimensional subset of the fixed X0:
q4=s, q5=v4=v5=0, all remote coordinates zero, t=0, |s|<=3/20.
The certificate polynomial restricted to this interval has a NONZERO quartic
coefficient. In contrast, the pinned current energy definitions restrict to:

```text
Vfull_DH = (A0+A+B) + (3/10)*s^2
Vshift_DH = (A0+A+B) + gravity_shift + controller_shift + (3/10)*s^2
Vcross = Vfull_DH                 on this subset
centered variants = the corresponding expression minus their constant anchor.
```

Reason: q2=q3=q5=0 fixes the potential to A0+A+B; velocities vanish, so kinetic
and q^T Mv vanish; the targeted gain increment is on joints 2/3; the same
analytic g0 is zero. This is source-expression specialization, not numerical
sampling or the previous raw lower-bound calculation.

A polynomial with nonzero quartic coefficient cannot equal a degree-at-most-2
polynomial throughout a nontrivial interval. Therefore the literal/decoded
IDEAL certificate polynomial is not any of these mechanical-energy conventions
on X0, even after constant anchoring. Nonzero time coefficients independently
exclude whole-time identity to the autonomous energy expressions.

This is an exact expression nonidentity, not a claim that the rounded runtime
evaluation has been formally interpreted. That latter bridge remains absent.
No origin-only comparison, initial-bound value or obstruction arithmetic was
recomputed. To compare rather than identify these functions would require a
new signed function-difference bound, not a sameStorage equality field.

## 4. The two initial contracts differ

Certificate source line 104 defines
r0=qa^2+qb^2+dqa^2+dqb^2-R_init^2. Its line-290 pinit is
`-V(qa,qb,dqa,dqb,0)+s4p*r0`. IF both pinit>=0 and s4p>=0 are genuinely proved
on the stated constrained initial domain, then r0<=0 implies V(0)<=0.
That conditional obligation is not the energy producer's recorded u bound;
this review does not validate the numerical certificate/multipliers.

The polynomial initial variables are exactly the block coordinates, so they
can be embedded in the fixed block-only X0. The runtime Monte Carlo generator
at export_traj:143-150 instead samples a full twelve-dimensional ball. That
sampling is neither universal proof nor a reason to change X0. Certificate
storage ignores remote coordinates, but the physical dynamics need not.

The energy producer separately computes
`[max(hessian_upper/2,mass_upper/2)+eps*mass_upper/2]*radius^2`.
Its cross allowance is already present. There is no input field binding this
scalar to the certificate CSV, and source syntax alone does not establish a
bound for any selected mechanical convention. The barrier keeps threshold 1;
the trajectory display's t^2 column is not a replacement for that contract.

## 5. Minimal missing fields / next decision

No single same-K/X0 exact identity across these branches exists as currently
defined. A complete contract must FIRST distinguish:

- `active_function_id` and `consumer_source_hash`: certificate polynomial,
  explicit energy convention, or another specifically defined storage;
- `coefficient_artifact_hash`, `coefficient_semantics`, `evaluator_hash`,
  exponent order and evaluation/refinement witness for the certificate branch;
- `K`: potential value/anchor, original or targeted gains, regularizer, linear
  sign, cross inclusion, analytic versus FD/runtime interpretation;
- `X0/state_map/time0`: retain block-only initial embedding, not sampled states;
- `initial_function_witness`: either checked certificate pinit/multiplier
  proof for that exact decoded polynomial, or a source-bound energy theorem;
- `comparison_witness`: if transferring between these different functions,
  a proved same-domain signed inequality with its budget, NOT identity;
- `consumer_binding`: the unchanged initial scalar and threshold attached to
  that same selected function. No threshold or selection was changed here.

Pinned energy-side hashes checked in this inspection:

```text
routeB_compact_energy_storage_to_block_audit.py
80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9
routeB_compact_energy_storage_to_block_audit.csv
8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1
routeB_compact_block_energy_barrier_audit.py
62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927
routeB_compact_dh_full_energy_supply_split_audit.jl
d6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632
routeB_compact_dh_storage_shift_audit.jl
aa3957f714f86c631a55fb8e7cc190fc98918a9cc04d148adcd7a28141cb9fec
routeB_compact_dh_gain_descriptor_regeneration_audit.jl
04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9
routeB_compact_targeted_nonlinear_strictification_audit.jl
41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1
```

Validation was limited to read-only hashes, manifest comparisons and literal
CSV shape/coefficient inspection with Python -B, exit 0. The mathematical
nonidentity is the paper polynomial argument above, not kernel verification.
No deployed active-V selection or source/initial theorem is asserted.
