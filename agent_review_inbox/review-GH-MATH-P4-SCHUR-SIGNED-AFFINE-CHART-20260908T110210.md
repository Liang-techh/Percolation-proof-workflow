---
kind: review_result
review_id: review-GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART-20260908T110210
task_id: GH-MATH-P4-SCHUR-SIGNED-AFFINE-CHART
source_agent: Codex-signed-affine-source-audit
created_at: "2026-09-08T11:02:10-06:00"
inspected_commit: c7ab49a3c55c002076ae18f325eedc8a146ac9bd
integration_status: pending
admission: pending
admission_label: pending
status: ACTUAL_AFFINE_CHART_AND_DUAL_BOUNDS_MISSING
affine_chart_source_witness_found: false
dual_interval_bounds_found: false
quadratic_defect_bound_found: false
source_binding_proven: false
merge_decision: refuse_completed_source_packet
lean_compile_status: not_run
state_mutation: false
registry_mutation: false
formal_certificate_allowed: false
requested_action: authenticate z_A and its signed enclosure, then prove the same-source port map and metric/target identity; do not splice incompatible old domains
---

# Signed affine chart: new invocation evidence still does not fill the packet

## 1. Result

No inspected source artifact supplies the complete same-(kappa,x,Omega) chain
d=A*y+b together with signed u/s bounds, a quadratic D bound, H=M0_CC^-1,
and the intended beta/t. All three witness flags remain false.

This continuation uses the revision804-related budget-closure review and the
new source-semantics split. It does not repeat generic Young, row rank,
fixed-ball thresholds or their counterexamples. Those remain earlier
conditional algebra, not physical claims.

Only this new review is written. No sidecar, external source, payload,
state/registry or older agent file is modified; no Lean/Lake, Julia,
numerical experiment, producer or full regression ran.

## 2. What the new source split actually adds

The fresh SOURCE-SEMANTICS-HALF-ACTIVE review identifies runtime invocation
evidence but explicitly reports actual_valuation_supplied=false and
runtime_defect_refinement_supplied=false.

A targeted read of current verify_dynamics_semantics.jl confirms:
- mass and C/G are compared at default versus explicit regularized settings;
- its acceleration call is exact_ddq(...;mass_regularization=0.0,...);
- the output records finite status and maximum absolute component;
- the script itself calls this a sanity check, not proof over the full domain.

Thus the acceleration call is not the mu=1/1000000 chart invocation, and its
aggregate record is not a same-call tuple (M_R,F_R,ahat) or solve-defect enclosure.
This review did not replay the call or authenticate historical execution.

The new semantic split must be preserved:
an independently defined ideal analytic/FD model equation is one target;
decoded runtime acceleration with model/assembly/solve refinement is another.
Choosing the former cannot establish the latter. The current packet request
cannot silently switch from “actual runtime residual” to a nominal model.

## 3. Minimal missing source chain, with dimensions and identities fixed

Retain full-state half_active vanis2 Omega and a single configuration kappa.
Let chi=(q,dq,w), actual returned acceleration ahat in R6, fixed chart mass
M_A including one mu, and corrected chart force F_A. For decoded runtime
M_R,F_R, the source split requests

    z_A=M_A*ahat-F_A
       =(M_R*ahat-F_R)+(M_A-M_R)*ahat+(F_R-F_A),
    y=X*z_A in R6.

Even this z_A/y valuation and an effective same-domain enclosure are missing.
Merely defining these discrepancies is not an error bound.

To reach block456 actual port defect d in R3, a further SOURCE statement is
needed, e.g.

    d=K*z_A+b,   K:R6->R3, b in R3,
    A=K*X^-1,   d=A*y+b.

This is a requested chart, not a verified formula for the current source.
K and b must follow the actual/reference residual definitions and sign convention.
In particular d is not necessarily the projection of the solve residual:
reference/controller differences, retained distal terms or a changed nominal
acceleration may contribute through K or b. Do not set b=0 without proof.
X^-1 is a chart transport here, not H and not a new rank claim.

The bound consumer also needs, at the SAME x:
ell,r0,d in R3, r_actual=r0+d, l_actual=ell+r_actual,
H:R3x3=M0_CC^-1 for C=(4,5,6) in that order,
E_A from the same chosen a_C/energy chart, beta from the actual intended
budget evaluator, and t with the same units/normalization.
The source mapping for H must preserve its origin/reference and one mu.

Defining y:=d, A:=I, b:=0 would give a tautological chart of the wrong intended
measurement semantics and no new enclosure. It is not a substitute witness.

## 4. Required dual and quadratic bounds: no producer currently fills them

For a proved same-source affine chart, the exact requested quantities are

    u=ell^T H(Ay+b),
    s=(ell+r0)^T H(Ay+b),
    D=(Ay+b)^T H(Ay+b).

The two dual coefficient vectors are A^T H ell and A^T H(ell+r0).
The previous budget-closure review already provides the signed interval
support-function consumer; no new derivation is needed.

A usable actual witness must certify a signed enclosure of that SAME y,
the offsets involving b, and all source-dependent coefficients on Omega.
If A,H,ell,r0,b vary across the cell, a fixed interval bound must quantify over
that variation; one evaluated coefficient vector is not a cell certificate.

For D, a matrix/affine quadratic bound must use this same A,b,H,y.
A six-component acceleration radius, |X| comparison output or unrelated metric
cap is not D. One may instead certify the combined target defect 2s+D directly.
No current artifact binds either option.

This task located no authenticated actual affine K/b map, no actual signed
y interval payload, and no matching quadratic bound. Therefore the dual-bound
formulas are only an exact interface specification, not source evidence.

## 5. Artifacts and domains that cannot be spliced

Fresh inspection of the two bound JSON domain lists confirms both enumerate:

    initial_analytic_slab_v1.json
    expanded_analytic_slab_v1.json
    adaptive_domain_0_v1.json
    adaptive_domain_1_v1.json
    adaptive_domain_2_v1.json

Neither lists half_active_vanis2_domain_probe.json.
These are the old domains of combined_descriptor_remainder_v1.json and
descriptor_defect_contribution_audit_v1.json. They may only transfer through
proved domain inclusion AND model/chart/quantity identities; no such witness
was supplied here.

The predecessor's inspected decomposition producer uses (I-C)^-1|X| to split
nonnegative acceleration-remainder bounds. That comparison operator is not
M0_CC^-1, and those arrays do not determine signed u/s. An absolute enclosure
could become a conservative signed enclosure after legitimate source transport,
but that missing transport cannot be replaced by naming conventions.

The older block456 q-box/eta port budget is nominal, not a vanis2 runtime
defect chart. Its B_up/Aup and betaC expressions cannot be joined to the
half-active runtime discrepancy solely because both contain three-dimensional
or six-dimensional arrays.

The current symbolic block456 Schur source has H=inv(M0CC456Q) and betaC,
but this does not establish the same corrected source/reference ell, actual d
or same-domain cap. beta and t must be reidentified in the final packet;
t is a specified target level, not a number inferred from a defect JSON.

Finally, the new source-semantics review reports default debug Monte Carlo
invocations on eta-domain samples and a mu-zero verifier sample. Neither is
the uniform vanis2 actual invocation/defect packet. This review does not
re-evaluate those logs or import their numerical results.

## 6. Shortest obstruction and reopen order

The shortest missing chain is:

1. **Actual valuation/refinement:** one kappa,x,Omega with z_A and signed y=Xz_A
   enclosed for the intended actual semantics.
2. **Actual port chart:** prove how that same z_A produces d=Kz_A+b and identify
   the corresponding ell,r0,l_actual. Do not confuse actual defect with nominal port.
3. **Common metric and target:** identify H=M0_CC^-1, E_A,beta,t under the same
   reference, order, regularizer, units and domain.
4. **Projected evidence:** two dual interval bounds and D (or 2s+D) under the
   same chart, followed by the predecessor's explicit signed allocation gates.

A complete artifact for item1 was not found in the bounded sources inspected.
Items2–4 are not supplied by the existing symbolic equations or old bound lists.
The obstruction is missing compatible source evidence, not a new algebraic
impossibility or physical trajectory counterexample.

Disposition: pending, source packet refused as complete.
No claims of Lean compilation, verification or registry admission.

## 7. Exact paths and current hashes

W=C:/Users/z5242/Desktop/重构版/工作流.
P=C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized.

| Path | SHA-256 |
|---|---|
| W/agent_review_inbox/review-GH-MATH-P4-SOURCE-SEMANTICS-HALF-ACTIVE-codex-20260908T1100.md | F04AA854206A046B5429C9381CA69B8775BD6ECCFEC6E82417CB10077620D408 |
| W/agent_review_inbox/review-GH-MATH-P4-SCHUR-BUDGET-CLOSURE-20260908T105720.md | 4A7B5D054F53BEF37D920D70682B3769D97AB19076622A0BDD5A0A4C19FE476F |
| P/routeB_dense_Mq/verify_dynamics_semantics.jl | 9EF1AD949DD929E6DCBC03FF566BB84ADE28D923393541330E37244051720A07 |
| P/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E |
| P/robot_formal_v1/interval_bounds/descriptor_defect_contribution_audit_v1.json | 65A4D583913E8CC7402A22B3AD5A09676FEC74E7251B48E491F9F82F13CBBFD9 |
| P/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json | 68596F1557AA709D86BC8711ED7985552684DFFE7FDE290ABF03B511F6BD9805 |

Fresh checks comprised targeted review/source reading, JSON domain-list reads,
filename/field searches for actual/affine/signed witness candidates, and hashes.
Field search covered P/robot_formal_v1/interval_bounds and P/routeB_dense_Mq
JSON/receipt candidates; absence is limited to this search, not the whole machine.
No matching *force*dh*v2* filename was found under interval_bounds.
No large bound arrays, runtime execution or interval soundness were authenticated.

