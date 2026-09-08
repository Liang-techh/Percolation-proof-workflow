---
kind: review_result
review_id: review-GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE-LOCAL-20260908T160907Z
task_id: GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE
source_agent: codex-half-active-semantics-lane
created_at: 2026-09-08T16:09:07Z
integration_status: pending
admission_label: pending
status: CONTROLLER_CORRECTION_IDENTIFIED_ACTUAL_BALANCE_UNPROVEN
proof_status: source_coefficient_audit_and_conditional_defect_contract
source_binding_proven: false
actual_row_witness_constructed: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTUAL-THREE-ROW-WITNESS-LOCAL-20260908T160325Z.md
predecessor_sha256: eead637d77db72eda490ba87635c50fade339acd9e4990be5e111f24521c9683
requested_action: retain the fixed half-active domain; authenticate one DH configuration and prove its actual balance with the complete defect
---

# half_active_vanis2: controller repair is possible algebraically, not source admission

Only this new inbox review is written. No new domain search, producer/checker
execution, numerical bound generation, Julia, Lean, solver or regression ran.
The revision-786 obstruction is consumed via the predecessor's current hash,
not via state mutation. Existing source declarations and payload metadata were
reread, and listed file hashes recomputed.

External root P is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
All external paths below are relative to P.

## 1. Fixed configuration and exactly what the coefficient comparison means

Keep only the existing `robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json`:
angle radii (9/20,19/50,37/100,19/50,37/100,9/20), component velocity radius
3, scalar |w|<=2, initial radius 3/20, step 1/512. These are existing analytic
candidate tokens, not newly verified bounds or runtime configuration.

At the ideal-real source-coefficient level let d_old be factorized Kd+Bfr,
d_DH be dhport Kd+b_fr, and Delta=d_old-d_DH. Same q, velocity v and scalar
w are mandatory for this comparison. The factorized expression uses scalar w;
any runtime vector input interface must be explicitly identified with the
same scalar broadcast, not silently substituted.

| Joint | d_old | d_DH | Delta | Force correction F_DH_analytic-F_old |
|---|---|---|---|---|
| 1 | 9/5 | 13/10 | 1/2 | +(1/2)*v1 |
| 2 | 7/5 | 11/10 | 3/10 | +(3/10)*v2 |
| 3 | 19/20 | 19/20 | 0 | 0 |
| 4 | 1/2 | 4/5 | -3/10 | -(3/10)*v4 |
| 5 | 13/20 | 13/20 | 0 | 0 |
| 6 | 4/5 | 1/2 | 3/10 | +(3/10)*v6 |

These fractions are exact differences of inspected controller declarations,
NOT estimated errors or newly exported machine constants. Since damping
enters force with a minus sign, the correction is +diag(Delta)*v.
Kp and ideal GwI match. Hold the analytic M,C,G and origin-gravity convention
fixed for this particular comparison: then

```text
F_DH_analytic = F_old + diag(Delta)*v.
```

This equation does not identify analytic C/G with the central-FD implementation.
Likewise `gw_coef .* I_val` algebraically cancels the source division in ideal
real semantics but need not reproduce the expected coefficients exactly in
Float64. Decimal decoding, loaded array mutation and rounded arithmetic are
not covered by coefficient equality.

The current `initial_analytic_slab.py` already uses d_DH, not d_old; its
configuration is consistent with the DH coefficient branch at this layer.
Do not add Delta*v again to its RHS or its existing DH-centered force payload.
The domain JSON does not bind the historical producer/environment bytes, so
this is an audit of current code and payload, not authenticated run provenance.

## 2. Why the currently available witnesses cannot be merged

1. **Old six-row factorized identity versus actual equation.**
   `routeB_factorized_descriptor_model.jl` defines old-controller RHS and six
   descriptor expressions. Its mass/link and alternative-expression identities
   do not prove those residuals vanish at the actual acceleration. Changing
   coefficients or writing a correction formula does not fill this source premise.
2. **Repaired two-row payload versus missing physical rows.**
   `force_balance_bridge_dh_v1.json` uses DH gains but exports rows=[4,5]
   after the preconditioner X. Its physical acceleration substitution and
   equality-ideal bridge are explicitly unresolved. Row6 is absent.
3. **Remote corrections can enter preconditioned local rows.**
   With residual R_old=M_A*a-F_old, R_DH=R_old-diag(Delta)*v. Thus
   `(X*R_DH)_i=(X*R_old)_i-sum_j X_ij*Delta_j*v_j`.
   Neither X_5j*Delta_j=0 nor cancellation of that sum is supplied. Even though
   Delta5=0, a preconditioned fifth row may change through joints 1,2,4,6.
   Two rows of X*R=0 do not imply the three physical rows R4=R5=R6=0.
4. **Analytic versus finite differences.**
   dhport arm_MCG constructs C/G using central differences and computes G0
   by another such call. The analytic CSV branch uses analytic C/G and its
   origin value. The required comparison is centered gravity difference,
   not merely G(q) error with G(0) omitted. No matching bridge was verified.
5. **Exact balance versus Float64 solve.**
   `exact_ddq` returns backslash output. No loaded configuration/method,
   finite-output, assembly or solve-residual witness makes that an exact
   source equation. Source hashes alone do not authenticate loaded globals.
6. **Domain and consumer binding.**
   The existing slab is analytic and formal=false. It does not bind the
   runtime state or prove actual trajectory containment, observable units or
   the retained-coupling signed numerator. No other domain is spliced into it.

## 3. Complete conditional balance/defect contract for one configuration

This is a specification of missing evidence, not a constructed witness.
Use M_A for the fixed analytic mass INCLUDING its single regularizer and
F_DH_analytic for the analytic force with repaired DH gains.
For the SAME decoded input x in the fixed domain, let Mhat,Fhat,ahat be the
finite decoded matrix, fully assembled force, and returned acceleration from
one authenticated runtime configuration. Define exact-real discrepancies:

```text
delta_M = Mhat-M_A
delta_F = Fhat-F_DH_analytic
r_solve = Mhat*ahat-Fhat
e_DH = delta_F+r_solve-delta_M*ahat.
```

Then the intended model-chart identity is
`M_A*ahat = F_DH_analytic+e_DH`.
If keeping the old factorized RHS instead, the consistent chart is

```text
e_old = diag(Delta)*v + e_DH
M_A*ahat = F_old+e_old.
```

Choose ONE chart. Defining e by discrepancy is an algebraic identity, not a
source authentication or enclosure theorem; a useful packet must independently
bind and control these discrepancies. No numerical bound or observation is
invented. Do not separately debit a component already included in delta_F.

The required evidence bundle must supply all of the following:

- One immutable source/configuration binding: loaded globals/types, q/v/w
  layout, scalar-disturbance broadcast, regularizer, FD step, selected methods,
  arithmetic environment and actual assembly/solve trace semantics.
- A source-to-analytic mass binding or certified delta_M, including only one
  regularizer and the exact same input. If an exact-real FD target is selected
  instead of runtime, specify it independently and prove its equation; it is
  not a runtime theorem.
- delta_F correspondence covering controller/loading/arithmetic discrepancy,
  the two centered gravity evaluations, Coriolis FD versus analytic terms,
  and force assembly. Keep signs and common inputs. Kp/GwI coefficient matches
  do not dispose of loaded-value or evaluation discrepancies.
- A finite decoded solve output and r_solve bound/identity for the same matrix
  and force. Control the matrix-error times actual acceleration term, not just
  delta_F. Any acceleration bound used here must avoid circular dependence on
  the unproved row/defect packet.
- Actual rows4/5 and, for the requested three-row artifact, row6 of the above
  common equation. If deriving them from preconditioned equations, provide
  enough rows and an inverse/row-space recovery identity; the present two rows
  alone do not suffice.

## 4. Selected principal restriction remains conditional

Retain B=(4,5), E=(1,2,3), joint6. In the DH-analytic chart the two-row objects
are S=(M_A)_BB and

```text
f = (F_DH_analytic+e_DH)_B - (M_A)_BE*ahat_E - (M_A)_B6*ahat_6.
```

Using the old chart gives the SAME f only after the explicit correction
identity above. Do not drop joint6 or remote accelerations because q or a
domain endpoint happens to vanish. Row6 is not needed merely to restrict
proved actual rows4/5, but it IS needed for a claimed actual-three-row witness
or joint6 elimination; no such row6 witness currently exists here.

Next-stage bounds must reference det(S) and the complete signed
ell^T adj(S) f for this same domain/configuration. A fixed observable with
coordinate/time units and theta''=ell1*ahat4+ell2*ahat5 is an additional
trajectory/semantics premise, not the nominal force vector lBase. These
det/numerator/observable witnesses remain absent; no constants are proposed.

Conclusion: the ideal controller mismatch has a precise algebraic repair,
but available artifacts cannot be combined into an actual same-configuration
M*a=F+e witness with certified defect. The first missing proof is source/runtime
to analytic/FD balance, not another controller coefficient calculation.
All admission statuses remain pending/false.

## 5. Fresh raw-byte SHA256 anchors

| Path relative to P | SHA256 |
|---|---|
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_dense_Mq/routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| robot_formal_v1/exact_checks/initial_analytic_slab.py | 97c96fb01bc9318af258a75d6b1371e3eef665fa760f401ce9f5a422ca164998 |
| robot_formal_v1/interval_bounds/controller_semantics_audit_v1.json | a377c577c079a69c7b9de5885c076487a2f633b9581782d2cc7be7c0af1ec3b9 |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json | 3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107 |

Hashing records current bytes only. No historical execution, interval soundness,
kernel verification or source admission is inferred. Existing files untouched.
