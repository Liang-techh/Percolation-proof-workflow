---
kind: review_result
review_id: review-GH-MIXED-schur-absorption-reassigned-20260908T105121
task_id: GH-MIXED-schur-absorption-reassigned
source_agent: Codex-actual-defect-schur-lane
created_at: "2026-09-08T10:51:21-06:00"
inspected_commit: 335ac7556da34fc9084c82c6261bda381af7738a
integration_status: pending
admission: pending
admission_label: pending
status: ACTUAL_SOURCE_BINDING_BLOCKED_CONDITIONAL_GATES_SUPPLIED
proof_status: OPEN_UNCOMPILED_CONDITIONAL
source_binding_proven: false
actual_residual_cap_proven: false
lean_compile_status: not_run
state_mutation: false
registry_mutation: false
candidate_path: examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean
candidate_sha256: 91A3A598BA6C6FB0278A127C8B94A34839F74EB3CD88D46B6D2CA4D4169C5BA7
requested_action: retain signed actual-defect gates; supply common source residual/metric/projection witnesses before using SchurPMIBinding
---

# Reassigned Schur absorption: nominal-to-actual signed defect gates

## 1. Result and three evidence layers

The bottleneck is not another generic Young proof. Under the requested
E_A<=beta-L-2 ell^T H r contract, the exact extra condition introduced by an
actual residual defect is a SIGNED projection bound. It is different from the
extra condition for the direct target. This review gives both gates, their
sharp full-ball robust form, and a strict conditional obstruction.

- **Pure Real algebra:** the new candidate proves four scalar gate statements
  conditional on explicitly supplied identities. No norm, source or matrix
  is manufactured. It is UNCOMPILED.
- **Source binding:** same-state identities for ell, nominal r0, defect d,
  actual r, metric H, beta and E_A remain open.
- **Actual residual:** no same-source actual defect/metric cap or physical
  trajectory bound was established. Status is pending; source handoff blocked.

Only the named new Lean-prep and this new review were written.
No local/remote Lean/Lake, Julia, solver, producer, sampling or full regression.
No state/registry/old artifact/shared adapter edits.

## 2. Exact actual-defect interface

Fix one state x, common real SPD metric H and source-bound vectors:

    r_actual = r0 + d,
    l_actual = ell + r_actual,
    L=||ell||_H², Q0=||r0||_H², c0=<ell,r0>_H,
    u=<ell,d>_H, s=<ell+r0,d>_H, D=||d||_H²,
    Qactual=||r_actual||_H²,
    P0=beta-||ell+r0||_H²,
    Pactual=beta-||l_actual||_H².

Then the needed common identities are

    Pactual = beta-L-2(c0+u)-Qactual,
    Pactual = P0-2s-D.

These identities must come from the SAME actual residual and H. Two unrelated
scalar equalities from different configurations cannot populate this packet.

The exact pointwise joint condition is

    [E_A-Qactual <= Pactual AND t<=Pactual]
      iff
    [2u <= beta-L-2c0-E_A AND 2s+D <= P0-t].

The Qactual deduction cancels in the first comparison, leaving a linear
ell-defect projection. It does NOT cancel in the target. Hence a nominal
Q0 cap cannot substitute for either actual identity or for the second gate.

The Lean-prep directly states these equivalences and a consumer of supplied
u<=U, s<=S, D<=Dcap with
2U<=beta-L-2c0-E_A and 2S+Dcap<=P0-t.
These are signed upper comparisons, not compulsory absolute-value bounds.
Keeping correlation can improve them. The structure does not require first
inflating the entire nominal port ball or bounding every defect component.

## 3. Sharp robust threshold for a fixed nominal center

Assume a real SPD inner-product space of dimension at least1 and epsilon>=0.
Hold ell,r0,E_A,beta,t FIXED and allow every d with ||d||_H<=epsilon.
Set S0=||ell+r0||_H²=L+2c0+Q0>=0.

The two desired inequalities hold for ALL such d iff

    beta >= max(
      E_A + L + 2c0 + 2*sqrt(L)*epsilon,
      t + (sqrt(S0)+epsilon)^2
    ).                                                     (R)

Proof: the first gate maximizes 2<ell,d> over the ball, with maximum
2||ell|| epsilon. The second maximizes ||ell+r0+d||², with maximum
(||ell+r0||+epsilon)². Both follow from inner-product Cauchy/triangle,
and equality is attained in the corresponding aligned direction.
If ell=0 the first projection is identically zero; if ell+r0=0 choose any
unit direction for the second. epsilon=0 is immediate.
For simultaneous universal validity, take the maximum of the two maxima;
they need not have the SAME maximizing direction.

This is a sharp statement for the full defect-ball enlargement, not a
necessary condition on a smaller actual source graph. It is not encoded as
a compiled Lean theorem in this task. It preserves nominal c0 rather than
replacing it by worst-case independent alignment.

Equivalently let g_bind=beta-L-2c0-E_A and g_target=P0-t.
The robust gates are
g_bind>=2sqrt(L)epsilon and
g_target>=2sqrt(S0)epsilon+epsilon².
For epsilon>0 and nonzero ell, a zero nominal binding gap cannot survive all
defect directions. That is a specific obstruction, not mere lack of a solver.

If ell or beta changes when d changes on the actual graph, (R) is applied
pointwise with source-bound parameters or requires a separately proved uniform
enclosure; it cannot silently freeze varying quantities.

## 4. Strict counterexample: actual cap and positive target do not give binding

Pure one-dimensional exact-real interface example:

    H=1, ell=1, r0=0, d=1/4, E_A=1, beta=2, t=0.
    Qactual=1/16, Pactual=7/16, E_A-Qactual=15/16.

The actual metric cap Qactual<=(1/16)E_A has rho=1/16, B=0 and strict
slack delta=15/16. The direct target t<=Pactual holds, yet the binding fails:
15/16>7/16. Nominal d=0 had binding equality and P0=1.

Thus even an actual cap with strict slack and a positive direct target does
not imply E_A<=beta-L-2 ell^T H r_actual. Using the absorption floor here
would be invalid because its separate SchurPMIBinding premise is false.
This example is abstract Real algebra, NOT a claim about reachable robot
states or the actual deployed metric. No numerical experiment was run.

## 5. How a same-source actual cap may enter, without double charging

For the block456 convention read from the existing descriptor interface, a
possible source packet would prove, at the same point and configuration,

    M_DD v + DeltaM_DC a_C = e_D,
    J M_DD = I,
    r_actual = M_CD v + e_C.

Then r0=R a_C, R=-M_CD J DeltaM_DC and d=M_CD J e_D+e_C.
This sign is tied to these exact equations; it is not a universal sign rule
for other condensed-force conventions.

The mandatory source part also fixes ell and l_actual=ell+r_actual.
Any controller/reference/local defect placed in ell instead of d changes
c0/u/s and must be reflected consistently. Do not add a second copy of a
controller/FD/solve defect already included in d.

With same-H witnesses Q0<=W0 and D<=Dcap, an actual cap may be
Wactual=(sqrt(W0)+sqrt(Dcap))², or for eta>0,

    Qactual <= (1+eta)W0 + (1+1/eta)Dcap.

If W0<=rho0 E_A+B0 and Dcap<=rhoD E_A+BD, this yields
rhoActual=(1+eta)rho0+(1+1/eta)rhoD and
BActual=(1+eta)B0+(1+1/eta)BD.
A strict absorption gate needs rhoActual+delta<=1, delta>0, E_A>=0.
It still needs the binding gate from section2 and target allocation
t+BActual<=delta E_A if using only that absorption floor.
A direct target proof via section2 need not also pass this more conservative
floor. FeedbackBinding is a separate energy-upper relation and is not implied.

Neither nominal nor actual cap establishes beta's allocation. The current
Julia diagnostic rho/BUP constants and lambda=2 are not a completed source
witness; generic Young only supplies a conditional lower bound on Pactual
once all actual inputs/caps have been bound.

## 6. Current source obstacles, not resolved by this candidate

Fresh source reads confirm block456 lBase, rC and lT are separate symbolic
objects linked by total_eq456=lT-lBase-rC; writing this expression does not
prove it vanishes at actual acceleration. The nominal port equation is
defect-free, whereas actual FD/assembly/solve/reference defects need explicit
allocation. E_A=Aup, betaC, the inverse M0_CC metric and any H-whitening must
retain the same order C=(4,5,6), reference origin and one regularizer.

The recent CORRECTED-ACTUAL-ROWS review explicitly has
corrected_source_written=false, source_binding_proven=false and
physical_rows_recovered=false. Even a hypothetically corrected controller
chart leaves actual substitution, full defect and row-recovery obligations.
It must not be read as evidence that a corrected builder or actual cap exists.
The earlier controller omission review is not repaired by the present algebra.

Old two-dimensional typed force/accel absorption inputs cannot directly produce
the three-dimensional actual packet. Likewise a half-active analytic slab,
a different q-box port ledger and a runtime force computation cannot be spliced
without domain, source and metric identities.

Smallest useful next source evidence:
1. One source/config/domain and actual acceleration/residual valuation.
2. Same-H ell,r0,d,l_actual identities, preserving all signed contributions.
3. Signed projections u,s and D bounds (or a same-H defect radius), not merely
   an unrelated nominal port cap.
4. The two allocations in section2 or the robust threshold (R).
5. If the legacy absorption route is retained, its actual relative/additive
   cap and strict slack; physical margin comparison/coverage remain separate.

Without this packet, source closure remains blocked. Repeating scalar Young,
changing beta's name, or promoting the Lean candidate cannot close it.

## 7. Candidate and input identities

Workspace W=C:/Users/z5242/Desktop/重构版/工作流.
External P=C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized.

| Exact path relative to root | SHA-256 |
|---|---|
| W/examples/routeb_p4_schur_joint_threshold_lean/NEW_REASSIGNED_20260908_ACTUAL_DEFECT_GATES.lean | 91A3A598BA6C6FB0278A127C8B94A34839F74EB3CD88D46B6D2CA4D4169C5BA7 |
| W/examples/routeb_p4_schur_joint_threshold_lean/NEW_JOINT_THRESHOLD_20260908.lean | 48DE2FC9D83BEA893405DD2D5A1B39ED5AF265CB6AEF1BA64678F56FD17BC8DF |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_SchurPMIAbsorption.lean | F18F9FB180AEAFAAD0DC3CD5149894D03EE111DB5C45ABFB86CAA927DF4050E3 |
| W/agent_review_inbox/review-GH-MATH-P4-CORRECTED-ACTUAL-ROWS-LOCAL-codex-20260908T104515.md | 671076DF787D72B460DCB6D154E46238CD6B0BE1EA638AC592FB34DCBC170007 |
| P/routeB_dense_Mq/routeB_compact_block456_residual_schur_interface_audit.jl | 3D68FFF2E71E3C912D45463CE1166E4381A98CEFB049478B989CC279520D4D98 |
| P/routeB_dense_Mq/routeB_compact_block456_descriptor_structure_audit.jl | 9E67520934801C87D0BBE14C550F755AFE80FFD6EACD1B6572FC65C52FC6CD79 |

Also read the existing 20260908T101432 Schur takeover review to avoid repeating
its nominal robust threshold. New contribution is the fixed-center actual-defect
joint gate and its two distinct signed projections.

Validation is static source inspection and paper algebra only; candidate
#print axioms commands are prospective and unexecuted. No elaboration/kernel
receipt exists from this turn. Input hashes bind bytes, not source correctness.
Other agents changed shared files during work; none was written or restored here.

