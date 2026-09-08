---
kind: review_result
review_id: review-GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS-LOCAL-20260908T160325Z
task_id: GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS
source_agent: codex-actual-three-row-source-lane
created_at: 2026-09-08T16:03:25Z
integration_status: pending
status: ACTUAL_THREE_ROW_WITNESS_ABSENT
admission_label: pending
selected_route: principal_restriction_retaining_joint6_and_remote_coupling
source_binding_proven: false
actual_same_cell_evidence_constructed: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-3D-TO-2D-RESTRICTION-LOCAL-20260908T155955Z.md
predecessor_sha256: 30cd6edd6a283dd875531420b6edba4c0d6810ef429ed5edb9cdc609b0ec666e
requested_action: bind actual DH force rows on the existing full-state slab and then provide retained-coupling numerator and observable witnesses
---

# Actual three-row search: full-state analytic slab located, actual witness missing

Only this new review is written. The revision-785 restriction handoff is
consumed through the predecessor above; no state file was read or changed.
This turn reads existing JSON, source and producer code and computes hashes.
No producer/checker, Julia, Lean, solver, full regression or numeric test ran.
No earlier counterexample or restriction proof is repeated.

External root P:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
All external paths below are relative to P.

## 1. A fixed full-state candidate domain, not a q-box/velocity splice

The existing `robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json`
has status RATIONAL_FIRST_NONLINEAR_SLAB, formal=false, and scope
Imported analytic model / full initial Euclidean ball radius 0.15 /
measurable |w|<=2 / first slab only. It records:

```text
angle_radii = (9/20,19/50,37/100,19/50,37/100,9/20)
velocity_radius = 3/1
initial_radius = 3/20
step = 1/512
```

These are existing payload tokens, not newly certified or generated bounds.
The matching candidate full-state box is
Omega={ |q_i|<=angle_radii_i, |dq_i|<=3 for every i, |w|<=2 }.
`initial_analytic_slab.py` lines 12-50 confirms this interpretation: six
individual angle radii, interval velocity products, scalar disturbance,
full 6x6 mass/RHS enclosures and a component acceleration supersolution.
The initial ball and time step have separate reachability roles; they do not
turn this review into a trajectory-containment certificate.

This is a different existing domain from (eta=5.6,depth=3,box_id=83). No port
row or H-budget from that earlier cell is imported. The domain JSON records
mass/gravity/Coriolis hashes, but not a historical producer/environment hash;
reading today's producer does not authenticate the historic execution.

The current slab producer's damping is
(13/10,11/10,19/20,4/5,13/20,1/2), matching the current DH controller coefficients.
Its M/C/G are still analytic CSV expressions. Thus the obstacle is not an
assumed damping mismatch for this slab: the analytic-to-FD/runtime bridge
and proof of the actual source row equations remain missing.

## 2. Existing force outputs: what is and is not a row witness

| Artifact | Observed content | Missing actual three-row link |
|---|---|---|
| force_balance_bridge_dh_v1.json | rows=[4,5], a=A*x+delta_a, centered preconditioned force split; references this exact domain hash | No row6 export; physical acceleration substitution and equality-ideal bridge explicitly unresolved |
| preconditioned_force_balance_identity_dh_v1.json | rows 4,5 support data for X*((M+epsilon I)*a-tau_DH+C*dq+G)=0 | These are rows of X times the full residual, not unpreconditioned physical rows 4,5,6 |
| routeB_factorized_descriptor_model.jl | Six analytic descriptor expressions, including complete RHS and mass-link identities | Equality of symbolic expressions is not a witness that actual acceleration makes each expression zero; controller branch differs |
| half_active_vanis2_domain_probe.json | Full-state analytic interval M/RHS and acceleration supersolution | Does not encode actual source balance, projected numerator or observable identity |

The DH centered bridge explicitly lists these unresolved obligations:
substitute physical acceleration lift into A*x and delta_a; prove the
Fourier equality-ideal bridge; certify DH energy/port-IQC positivity and flowpipe.
Its status is EXACT_CENTERED_FORCE_BALANCE_BRIDGE_DH_GAINS and formal=false.

The factorized source was inspected at lines 187-200 and 253-287.
`force_balance_aux` is a mass-side sum plus regularizer, NOT the zero residual.
The full descriptor is formed only after subtracting rhs. The identity test
compares alternative mass/descriptor representations after link substitution;
it does not establish a source trajectory satisfies descriptor=0.

Furthermore, its Kd+Bfr differs from dhport at joints 1,2,4,6. In the chosen
C=(4,5,6), the fourth and sixth force rows therefore differ already at their
damping terms. `controller_semantics_audit_v1.json` independently reports those
indices; this turn also reread both coefficient declarations. The repaired DH
two-row artifact cannot authenticate the un-repaired factorized sixth row.
No corrective force term has been numerically generated or silently set zero.

## 3. Selected route and exact requested packet objects

Choose principal restriction, not joint6 elimination. Keep the full-state x
throughout. Fix B=(4,5), E=(1,2,3), C=(4,5,6), D=(1,2,3,6), with the
same regularizer and selected actual DH force semantics.

The missing starting witness is the actual three-row statement

```text
M_CC(x)*a_C(x) = F_C(x)+e_C(x)-M_CE(x)*a_E(x),  x in Omega.
```

With convention M*a=F+e, the intended two-dimensional consumer takes

```text
S = M_BB
f = F_B+e_B-M_BE*a_E-M_B6*a6
u = (a4,a5).
```

The effective RHS retains a6 and all E accelerations. This route does not
need row6 for its two algebraic row equalities if actual rows4/5 are supplied
directly; the requested three-row source witness is nevertheless absent,
and a6 remains an actual coupled source quantity in the RHS enclosure.
No remote acceleration is set to zero from an angle or time-slab restriction.

Required determinant is det(M_BB(x)); required signed numerator is
ell^T adj(M_BB(x))*f(x), for a FIXED observable covector ell and one force
normalization. Neither det of a preconditioner/origin matrix nor an existing
port norm radius supplies these two bounds. No delta/R/cap is proposed.

The current `dhport_lib.jl` returns a Float64 backslash solve of its
regularized mass and finite-difference force. Calling it exact_ddq does not
establish e=0. One must either bind the exact-real FD equation as the target
with a source semantics witness, or include the actual solve/assembly defect
for decoded runtime. If using analytic matrices/force, include the additional
analytic-to-FD and model-matrix discrepancy consistently, once. Existing
analytic slab enclosures do not certify that combined actual defect.

Observable must be a physical quantity with fixed ell, offset, coordinate/time
units and theta''=ell1*a4+ell2*a5. No inspected output declares that binding.
The producer's nominal force lBase and its comparison preconditioner are not
an observable or its units. Any later residual H-budget needs its own same
Omega metric binding; this review imports none from the earlier q-box.

## 4. Minimal missing-witness obstruction

The first unresolved item is NOT the availability of a full-state box:
such an existing analytic candidate was located. It is the actual DH
three-row balance on that box, with authenticated source semantics and defect.

| Required component | Result of this bounded search |
|---|---|
| Fixed full-state domain | Located analytic candidate Omega; historic provenance and source/trajectory bridge unverified |
| Actual rows4,5,6 | Missing; repaired artifact only has preconditioned rows4/5, six-row source is symbolic and has different damping |
| Same descriptor/effective RHS | Formula fixed above, but no actual source witness instantiates it |
| Actual defect | No matching FD/controller/assembly/solve bound or exact source refinement found |
| det / signed numerator | No bounds for this M_BB, this complete f and this Omega found |
| Observable/units | No fixed observable coefficients and derivative/unit binding found |

Next useful evidence is a source-bound balance artifact for Omega with
the chosen DH configuration and actual acceleration valuation. Then obtain
the principal-row det and correlated numerator witnesses and freeze the
observable. The two-row consumer additionally needs its rational gate and
all five SameCellEvidence fields; source admission cannot precede these.
Failure to locate them is a bounded missing-evidence result, not proof that
such a packet cannot exist. Status remains pending, registry eligibility false.

## 5. Fresh SHA256 anchors

| Path relative to P | SHA256 |
|---|---|
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json | 3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107 |
| robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48 |
| robot_formal_v1/interval_bounds/controller_semantics_audit_v1.json | a377c577c079a69c7b9de5885c076487a2f633b9581782d2cc7be7c0af1ec3b9 |
| routeB_dense_Mq/routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |

The domain hash matches the value recorded in the DH centered bridge.
This is one direct content-binding check, not recursive proof validation.
No source artifacts, candidate packets, shared scripts, state or registry were modified.
