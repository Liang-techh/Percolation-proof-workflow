---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-TARGET-DEFINITION-LOCAL-20260908T162002Z
task_id: GH-MATH-P4-ACTIVE-V-TARGET-DEFINITION
source_agent: codex-active-v-definition-source-lane
created_at: 2026-09-08T16:20:02Z
integration_status: pending
admission_label: pending
status: EXPLICIT_CANDIDATE_VALUES_FOUND_ACTIVE_SELECTION_UNBOUND
explicit_candidate_definition_found: true
actual_active_target_binding_found: false
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
generated_constants: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-T-P4-ACTIVE-ENERGY-ORIGIN-LOCAL-20260908T161455Z.md
predecessor_sha256: 9542842c3260413777573e341ad9ccadcf83faf43c64a499a31576df07eebd14
requested_action: explicitly bind the active V to one existing value-level storage and its configuration, offset and threshold
---

# Active V: explicit full-energy definitions found, active consumer selection missing

## New evidence and narrower conclusion

This read-only continuation found two explicit value-level source definitions,
not merely derivative expressions. It refines the earlier scoped absence
finding: an actual candidate expression exists, but its identification with
the active barrier's V remains absent. No existing review is edited.

External source directory E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.
Only this new inbox review is written. No source or CSV producer was run;
no new constants, origin values, bounds, solver evidence or Lean claims were
generated. Existing status flags are reported contents, not newly verified proofs.

## 1. Concrete value-level candidate and configuration chain

`routeB_compact_dh_full_energy_supply_split_audit.jl:19-21` explicitly assigns

```text
Uctrl_DH = (1/2) sum_i Kp_DH[i]*q[i]^2 + sum_i g0[i]*q[i]
Vfull_DH = Kfull_DH + Ugrav_DH + Uctrl_DH.
```

This fixes one candidate value including its additive convention: no extra
offset or cross term is present in this assignment. The import chain is

```text
dh_full_energy_supply_split
  -> dh_gain_descriptor_regeneration
  -> fourier_lifted_descriptor_model.
```

The inspected dependencies make the following fields explicit:

| Field | Located definition | Boundary |
|---|---|---|
| State | q[1..6], dq[1..6], c/s lift for joints2..5 | Need c/s=sin/cos(q) and actual state map |
| Mass | Fourier model loads analytic mass CSV then adds its declared regularizer once at lines127-130 | Not decoded dhport mass by name |
| Kinetic term | regeneration: Kfull_DH=(1/2) sum M[i,j]*dq[i]*dq[j] | Uses that same regularized analytic M |
| Gains | regeneration declares Kp_DH, d_DH and GwI_DH; repairs damping in descriptor_DH | Ideal coefficient branch; actual loaded values remain separate |
| Potential | regeneration: Ugrav_DH is an explicitly assigned c/s polynomial | No subtraction of Ugrav_DH(0) in Vfull_DH |
| Linear compensation | +g0 dot q in this Vfull_DH definition | Must preserve the source sign or justify its vanishing |
| Cross term | Absent in Vfull_DH | Cannot substitute the targeted cross-term storage |
| Additional offset | Absent in Vfull_DH | Raw potential's existing constant convention is retained |
| Time | No explicit time variable in this Vfull_DH assignment | Different from the saved time-dependent four-coordinate V |

The named dhport source is used for gain provenance; M/C/G remain the imported
analytic polynomial model. The regeneration source fingerprints dhport and
records its declared regularizer, but this does not establish real/machine
function equality.

## 2. A second explicit candidate: additive shifted storage

`routeB_compact_dh_storage_shift_audit.jl:14-28` explicitly assigns

```text
GRAVITY_SHIFT_DH = A0_grav_DH + Agrav_DH + 2*Bgrav_DH
controller_linear_shift = sum_i g0_constants[i]^2/(2*Kp_DH[i])
Vshift_DH = Vfull_DH + GRAVITY_SHIFT_DH + controller_linear_shift.
```

These are existing symbolic assignments. This turn does not evaluate or
generate any numeric shift. This shift is a lower-bound construction, NOT
origin subtraction. There is no source assignment here choosing the normalized
candidate `Vfull_DH-Vfull_DH(0,0)` as the active V.

The shift CSV reports g0_exact_zero and decomposition flags true, with
formal_certificate_allowed=false. The script also sets
`kinetic_factorization_available=true` directly; that boolean is not itself
a mass-factorization proof. No recorded flag is used here as admission evidence.

### Linear compensation sign must not be generalized silently

The full-energy source uses +g0 dot q while tau_DH contains +g0. The earlier
closed-loop audit uses -g0 dot q. With a nonzero common g0, cancellation against
the +g0 torque requires the negative linear storage term. The shift source
asserts its analytic g0 is zero, so these two expressions can coincide only
after that source-specific zero identity is established. Do not extend this
to loaded FD G0 without a separate witness. This review neither recomputes g0
nor declares the historical energy-identity flags false.

## 3. Active barrier does not select either candidate

Fresh reading of `routeB_compact_block_energy_barrier_audit.py:16-54` shows
the actual inputs remain the FD remainder CSV, Schur CSV, targeted
storage-to-block CSV and OLD closed-loop-energy CSV. It reads
`closed_power_raw_identity`, `initial_storage_upper` and fixed thresholds.
It does not import or reference the DH full-energy/shift artifacts, serialize
a storage function, or declare a value-level equality to either candidate.
A targeted search in this script and its output CSV found no reference to
Vfull_DH, dh_full_energy_supply_split or dh_storage_shift.

Thus neither candidate is justified as the active target merely because its
name includes DH/full energy. The active consumer's identity/normalization
link is still missing. Replacing the input chain is an implementation change
outside this read-only task, and would itself require proofs of transferred
initial/derivative/domain bounds.

## 4. Other existing V names do not resolve the selection

- The targeted strictification source explicitly describes
  `V_eps=K+U_g+U_ctrl_target+eps*q'*M(q)*dq`, with modified gains and cross
  term. This is a different storage even before choosing an additive offset.
- The old closed-loop-energy source defines its controller potential and a
  positive Vshift, but active consumption of its derivative flag does not
  choose raw, shifted or normalized values.
- The saved certificate reconstructed by routeB_export_traj.jl is a
  four-coordinate polynomial with explicit t and Float64 coefficients;
  it is not the above six-coordinate analytic expression by definition.

The dhport midpoint-height potential and Ugrav_DH have different declared
value conventions. A proof of their anchored differences can transport the
potential contribution to normalized energy, but does not identify raw Vfull_DH
or positive-shift Vshift_DH with active V. No derivative identity supplies
that value-level choice.

## 5. Minimal missing binding, now with concrete candidates available

The next artifact should identify which existing expression the active
consumer means and provide a pointwise equality on its exact domain:

```text
V_active(state,time) = chosen_value_expression(mapped_state,time).
```

The binding must include the mass/source/configuration, regularizer, actual
gain branch, c/s lift, potential anchoring, compensation sign, cross term,
time map and additive offset. It must bind initial upper bound, derivative
budget and target threshold to this SAME expression. A constant offset must
move the threshold/initial bound consistently; a nonconstant gain/cross-term
difference requires an actual comparison theorem, not a constant adjustment.

For origin-only use, a source-bound value inequality for the selected V is
enough. This task supplies neither that inequality nor a new offset value.
The minimal obstruction is now selection-and-transfer binding, not absence
of all value-level energy definitions. Integration remains pending.

## Fresh SHA256 anchors (relative to E)

| Source/artifact | SHA256 |
|---|---|
| routeB_compact_dh_full_energy_supply_split_audit.jl | d6d9bd3131d73fddf946f8652458b04c628f76471d497b2a52a49f0335b30632 |
| routeB_compact_dh_storage_shift_audit.jl | aa3957f714f86c631a55fb8e7cc190fc98918a9cc04d148adcd7a28141cb9fec |
| routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9 |
| routeB_fourier_lifted_descriptor_model.jl | 0fcf733144b3d7b1b08f328fe4ad24477057c56976f0ef53633c450d8fc4729d |
| routeB_compact_block_energy_barrier_audit.py | 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927 |
| routeB_compact_dh_storage_shift_audit.csv | 9a357d70638cc37496400da23adc7df8e25d2c012cd5c6d6dd576fb83ee0be3b |
| routeB_compact_dh_full_energy_supply_split_audit.csv | a812b9aa37a6366c40d6890591fbdc0819bce9b7d3c4df58ea077765d540f25c |

These bind current inspected bytes only; no dependency rerun, historical
execution authentication, Lean verification or source admission is claimed.
