---
kind: review_result
review_id: review-GH-MIXED-ADJUGATE-REASSIGNED-20260908T165153Z
task_id: GH-MIXED-ADJUGATE-REASSIGNED
source_agent: codex-adjugate-reassigned-source-lane
created_at: 2026-09-08T16:51:53Z
integration_status: pending
admission_label: pending
status: CONDITIONAL_RECOVERY_TO_NUMERATOR_SEAM_ACTUAL_ROWS_MISSING
actual_source_leaf_closed: false
source_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
rank_audit_repeated: false
state_mutation: false
registry_mutation: false
requested_action: authenticate complete measurements and recovered physical defects before either adjugate route
---

# Reassigned adjugate lane: physical recovery must precede numerator admission

Only this new inbox review is written. No old artifact, state, registry or
other agent file is modified. No Lean/Lake, builder, solver, numerical
experiment or regression is run. No VERIFIED label or actual source witness
is claimed. An additional uncompiled Lean duplicate is unnecessary: existing
recovery and adjugate consumers already expose the needed conditional seams.

## 1. Current concrete obstruction, freshly checked

External root P:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.

The current `robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py`
still exports only rows4/5 (line52). Its lines69-70 use q/dq key i+1 and
coefficient X[i][a]*gain[a] only when a==i. Reading the current JSON confirms
row4 has q/dq support only at joint4, and row5 only at joint5.

The previous weighted-source review identified the resulting missing terms.
This turn verifies the present builder/support pattern, without repeating its
coefficient counts, inverse or rank calculations. The missing signed expression
in a complete residual row i is

```text
m_i(x)=sum_(j!=i) X_ij*(kp_j*q_j+damp_j*v_j).
```

With z=M_A*a-F_A and y=X*z, and assuming all other channels are interpreted
correctly, the stored builder expression b_i is y_i-m_i, not y_i. This is an
expression-level condition, not a claim that either expression has actually
been observed. Complete controller metadata does not restore missing support.
The centered neighboring bridge's fuller controller expression likewise does
not prove actual physical rows4/5 or joint6.

No concrete exact rational identity in the inspected artifacts closes the
actual physical-row leaf. Existing rational recovery identities are useful
algebraic inputs only. The precise remaining obstruction is missing corrected
actual measurements/defect bounds for the same residual, not rank arithmetic.

## 2. One provenance envelope and residual convention

Keep one source/configuration K, full-state domain Omega (the existing
half_active_vanis2 candidate, not a new box), same analytic/runtime chart,
state/lift and units, matrix M, force F and actual acceleration a. Let

```text
z=M*a-F=e,   y=X*z.
```

X is the same pinned preconditioner as the measurement payload. It is not
the state-space type or the kinetic/force metric H. Let J select the actually
supplied complete preconditioned observations and Y=J*X. A rational recovery
matrix L_B is useful only together with the explicit factorization
`L_B*Y=P_B`, where P_B selects physical residual rows(4,5).
Same-X basis order, scaling and input identities are required.

If actual observations satisfy Y*z=b+eta, the existing minimal consumer gives

```text
e_B=P_B*z=L_B*b+L_B*eta.
```

The needed error is L_B*eta, not eta. For the incomplete stored row expression
with evaluation noise nu, complete measurements would satisfy
`y_i=bhat_i+m_i-nu_i`. The deterministic omission, observation error and
actual physical/model residual are different objects. Do not count m twice
inside physical source discrepancy or assume y_i=0 after textual repair.

The actual e must account for the selected controller, analytic-versus-FD,
mass-model/regularizer, force assembly and solve semantics. Defining e as a
residual is not a certified bound on it. This review does not reverify the
upstream source discrepancy or provide observation data.

## 3. Principal restriction: signed recovered defect enters the numerator

For B=(4,5), D=(1,2,3,6), retain all remote accelerations and define

```text
S_B=M_BB,  f0=F_B-M_BD*a_D,
S_B*a_B=f0+e_B.
```

No joint6 elimination or new determinant is hidden in this route. For fixed
observable covector ell and k_B(x)=ell^T adj(S_B(x)), the exact conditional
composition is

```text
N_actual = k_B*f0 + k_B*L_B*b + k_B*L_B*eta.
```

This uses linearity of the numerator in its RHS and the supplied recovery
factorization. It neither recovers missing observations nor proves a bound.
Keep the combined signed expression if correlated enclosure evidence exists;
taking absolute values of each physical defect component first is a separate,
potentially more conservative sufficient estimate.

The actual packet requires det(S_B) on this Omega, not det(M), det(X), an
origin minor or a port Cholesky pivot. Its numerator must use f0+e_B; a bound
for f0 alone omits the recovered defect. Even a fixed ell gives a generally
state-dependent k_B, so cancellation/support arguments for one rational row
cannot be reused uniformly without their own domain witness.

## 4. Joint6 Schur elimination: an additional physical-row obligation

Start from the SAME retained-E physical three-row balance, E=(1,2,3), and
partition in order (4,5;6):

```text
T=M_CC=[[A,h],[h^T,d]],
g0=F_C-M_CE*a_E,
T*a_C=g0+e_C.
```

With d!=0 and the actual joint6 row, the reduced objects are

```text
S_B=A-h*h^T/d,
f0=g0_B-h*g0_6/d,
e_reduced=e_B-h*e6/d.
```

Recovery for this route needs P_C*z, not just P_B*z. If L_C*Y=P_C and
Y*z=b+eta, set T6=[I_2,-h/d]. The full signed numerator is

```text
N_actual=ell^T adj(S_B)*(f0+T6*L_C*b+T6*L_C*eta).
```

The current two-physical-row recovery consumer does not supply e6 or the
actual third balance by dimension-changing notation. A separately certified
joint6 defect/value is also a legitimate input; no such input is provided.

Here det(T)=d*det(S_B). This is an exact conditional algebraic relation,
not a usable positive lower bound by itself. If denominator clearing is used,
both matrix and RHS must be multiplied by d; both the 2x2 determinant and
signed numerator then scale by d^2. Unscaled/scaled or principal/Schur bounds
cannot be mixed. No determinant/numerator constants are computed.

## 5. Five-field handoff and exact stopping point

| SameCellEvidence obligation | Principal route | Joint6 elimination route |
|---|---|---|
| row1,row2 | Actual rows4/5 with full M_BD*a_D and e_B | Same actual rows plus actual joint6 equation and inverse premise |
| determinant_lower | Same M_BB determinant on Omega | Same Schur determinant on Omega; control d consistently |
| numerator_upper | Signed ell-adjugate of complete restricted RHS | Signed ell-adjugate of complete reduced RHS including e6 correction |
| observable_binding | Fixed physical ell, coordinate/time units, actual theta''=ell dot a_B | Same; eliminating a6 does not define theta or its units |

The consumer's rational gate and nonempty-domain/source semantics are additional
bindings. No rank test, generic source-independent Cramer identity, metadata
hash or derivative label supplies any missing actual premise.

Preserve source bytes/configuration, Omega identity, X/measurement/recovery
matrix identities, row ordering, actual acceleration/lift, observable and
units in one packet. H, if used for a residual budget, needs an independent
same-source metric binding and is not inferred from X or S_B.

Conclusion: both routes are conditionally valid, but the current payload
does not provide complete actual measurements or physical row witnesses.
No concrete source leaf is closed. Next evidence should supply corrected
actual observations plus the requisite signed recovery constraints/defect
bounds (and row6 for elimination), then the matching determinant/numerator
and observable witnesses. Status remains pending.

## Fresh byte bindings

External paths relative to P:

| Input | SHA256 |
|---|---|
| robot_formal_v1/exact_checks/build_preconditioned_force_balance_identity_dh.py | 925f3818146e7e4154bff07ef16cc6c93db8609ae15be20a8551b4f15dca1c5f |
| robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48 |
| robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |

Workspace consumers:

| Input | SHA256 |
|---|---|
| examples/routeb_p4_rowspace_recovery_lean/NEW_ROWSPACE_MINIMAL_CONSUMER_20260908.lean | 8aa876e70e620c3d0640e3e2536e2b2c36270c133558c8f20236eb57bd5923e6 |
| examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean | a39485adea19ffd31a2f46a9b6cf0160d888d08ca36c64f4d0e9461fb406b616 |

Prior weighted-source and corrected-actual-rows reviews supplied routing and
conditional contracts; current builder/payload support was independently
reread. No prior compile, full coefficient, inverse/rank or runtime evidence
is represented as newly verified.
