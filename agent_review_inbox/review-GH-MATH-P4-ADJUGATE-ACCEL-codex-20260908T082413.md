---
kind: review_result
review_id: review-GH-MATH-P4-ADJUGATE-ACCEL-codex-20260908T082413
task_id: GH-MATH-P4-ADJUGATE-ACCEL
source_agent: Codex-P4-math-lane
agent: Codex-P4-math-lane
created_at: 2026-09-08T08:24:13-06:00
inspected_commit: ef85d45a4cdf3b62de723fd3a8e2fc646749d0fc
inspected_paths:
  - agent_review_inbox/review-T-P4-DESCRIPTOR-ACCEL-BRIDGE-liuguanyi-20260908T1212.md
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/half_centered_bound_v1.json
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.signed_projected_adjugate_acceleration_interface
requested_action: retain the independent theorem attempt and the two JSONs as scoped audit inputs only; obtain same-cell descriptor/determinant/projected-numerator witnesses and independent compilation before application; no source binding, P_upper or registry promotion
---

# Signed projected-adjugate sidecar and the precise role of two analytic JSONs

Implemented the source-independent 2x2 bridge requested from the remote T-P4-DESCRIPTOR-ACCEL-BRIDGE review. The sidecar is `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean`, namespace `RouteBP4032AdjugateAcceleration`. It imports Mathlib directly and has no dependency on DH files, growth constants, source keys, receipt or admission code. It remains OPEN_UNCOMPILED.

## Exact theorem and rational packet

For symmetric M=[[a,b],[b,c]], write D=a*c-b², N1=c*f1-b*f2 and N2=a*f2-b*f1. `cramer_identity` consumes both exact descriptor rows and derives D*u1=N1 and D*u2=N2 without an inverse. `projected_identity` contracts them with fixed real ell1,ell2 to obtain

`D*(ell1*u1+ell2*u2) = Ntheta = ell1*(c*f1-b*f2)+ell2*(a*f2-b*f1)`.

The contraction remains signed. `projected_accel_bound` needs precisely the two rows, **0<delta**, **delta<=D**, **|Ntheta|<=R**, and **R<=delta*upper**. The reusable scalar order leaf shows

`delta*|u| <= D*|u| = |N| <= R <= delta*upper`,

then cancels the positive factor delta. No positive-definiteness, eigenvalue, square-root or matrix-inverse premise is added. `coordinate_accel_bounds` gives optional independent coordinate caps from the two signed numerators; it is not used to replace the direct projection.

`RationalPacket` stores rational delta, numeratorUpper and accelerationUpper, positive delta, nonnegative accelerationUpper, and the exact multiplication gate. The scalar theorem itself can derive nonnegativity of upper from its nonempty pointwise premises, so it does not require that redundant premise; the packet keeps it as an explicit standalone data constraint. Rational-to-real order transport is written with `exact_mod_cast`.

`DescriptorFields` carries one domain and all scalar fields, plus fixed ell1,ell2. `SameCellEvidence` quantifies all of the following over that SAME domain and cell: row1, row2, determinant lower bound, projected numerator upper bound, and

`observableAcceleration = ell1*acceleration1+ell2*acceleration2`.

`same_cell_observable_cap` then concludes the absolute observable acceleration bound on that cell. It asserts no domain cover. For an affine observable ell1*q1+ell2*q2+theta0, a source-side derivative theorem must supply the last equality; the constant offset has no algebraic role. The sidecar does not pretend to prove a chain rule by naming a field. State/time-dependent ell or a nonlinear observable would require additional derivative terms, so the binding cannot be omitted.

The exact cancellation family M(t)=[[1,t],[t,1+t²]], f(t)=(t,1+t²), u=(0,1) is encoded with determinant one and Ntheta=0 for ell=(1,0). `positive_box_loss` records 2*T*(1+T²)>0 for T>0, the independent-box fallback loss from the remote review. No fallback enclosure replaces the signed numerator in the packet.

## The two external JSONs are useful audit inputs, not these witnesses

External root here is `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/`.

Both `robot_formal_v1/interval_bounds/combined_descriptor_remainder_v1.json` and `half_centered_bound_v1.json` currently have status COMBINED_POLYNOMIAL_DESCRIPTOR_BOUND, **formal:false**, and scope **Analytic CSV model; same symmetric domains and |w|<=2. Not a flowpipe.** Each has five domain records and six entries in each of preconditioned_gravity, preconditioned_coriolis, preconditioned_mass, preconditioned_defect, acceleration_remainder_abs. The half-step artifact also records centered_cosine:true and coefficient-bound arrays.

The first names initial_analytic_slab, expanded_analytic_slab and adaptive_domain_0/1/2; the second names half_domain_0 through half_domain_4. They are not a shared cell merely because their schemas match. For example, the inspected initial/half-domain-0 angle and velocity radii are 4/25 and 3/10, whereas half-domain-4 has angle radii 7/20 and velocity radius 3/2. These local boxes do not imply coverage of the current P4 source domain.

Read-only hashing found **14/14 direct source_hashes match current files for each JSON**. This establishes current byte consistency of their listed dependencies only. It neither authenticates the mathematical exporter nor recursively verifies all dependent proofs. No independent checker was run. The current producer is not itself authenticated by those dependency hashes, and its extra coefficient-output fields are not present in the older combined JSON; no byte-for-byte reproduction claim is made.

Reading `exact_checks/combined_descriptor_remainder.py` clarifies what the arrays mean. It combines signed polynomials with the slab preconditioner X, merges symmetric v_j*v_k Coriolis coefficients, and only then takes rational interval bounds. Its mass term combines X*(M-M0) with the linear acceleration map A applied to z=(q,v,w). Its gravity contribution uses a second-derivative Taylor remainder. Thus the fields are **preconditioned nonlinear descriptor defect bounds relative to a linear model**, not raw force component bounds. The producer forms r=gd+cd+md and an acceleration-remainder candidate E=(I-C)^(-1)r, checking E>=0 and E=r+C*E in exact rational arithmetic when it is run. Here that code was only read.

This approach does retain signed cancellation within those expressions and is worth auditing. However, the fields preconditioned_gravity/mass are not the full G/M, and acceleration_remainder_abs is not an absolute acceleration cap. None of these arrays is automatically |f|, det(M), or |ell^T adj(M)f| for a 2x2 block. Their names must not be mapped directly to the new packet.

## Minimal equations and obligations needed before reuse

For the existing six-dimensional analytic remainder route, define aLin=A*z, e=a-aLin and d=f-M*aLin. The source must prove the exact full equations **M*a=f**, hence **M*e=d**, with the same controller, gravity constant, Coriolis and regularizer. It must then prove that the JSON r actually bounds |X*d| on its stated box; this includes the correct gravity linearization and mass-linear term. The preconditioned identity is

`e=(I-X*M)*e+X*d`.

To turn this into |e|<=E, bind a nonnegative matrix C to |I-X*M|, prove a contraction (for example positive weights with C*w<=kappa*w and kappa<1), and prove r+C*E<=E with E>=0. **The supersolution equality alone is insufficient without contraction/order control.** The sibling check_initial_analytic_slab source reads C, weights and kappa and checks these forms, but its existence is not a theorem or an execution receipt.

Only after this route is source-bound may a separately proved linear bound L_j>=|(A*z)_j| yield |a_j|<=L_j+E_j. A raw RHS envelope would still require, for example, bounds B_ij>=|M_ij| and |f_i|<=sum_j B_ij*(L_j+E_j), or independent direct RHS intervals. The slab files do contain candidate rhs_intervals, but their source/domain proofs were not established here. This is an explicit possible audit path; no value is promoted to growthR/H/K or P_upper.

For the NEW 2x2 adjugate lane, the smaller direct input is different: a SAME-cell exact symmetric two-row descriptor, a positive rational determinant lower bound, and an outward bound for its **signed projected numerator**. Extracting rows 4/5 of a coupled 6x6 descriptor is not enough: retain the remote acceleration coupling in effective f, or prove the exact reduced/Schur descriptor. A bound for the full six-dimensional preconditioned remainder cannot be relabeled as that reduced numerator. Observable coefficients, coordinate projection, force units and any baseline/affine offset must be bound to the same model.

Finally, prove target-cell inclusion in the selected angle/velocity/disturbance box (and a cover if a global result is claimed). Trajectory invariance is needed only if the claimed result is along a trajectory; these JSONs explicitly supply no flowpipe. The analytic CSV model must be connected to the intended DH model. If the target uses central-FD C/G, its FD defect must be bounded and absorbed; if Float64 remains authoritative, roundoff, parameter interpretation and solve residuals also need enclosure. Rational endpoints encode numbers exactly but do not by themselves establish outward enclosure of deployed evaluations.

Disposition of these JSONs: **retain as pending analytic remainder audit inputs with useful provenance and cancellation structure; do not accept them as a proved same-source RHS envelope or instantiate the adjugate packet.** Missing deployed delta/Rtheta and descriptor/coverage/rounding witnesses remain explicit.

## Checks and source fingerprints

PowerShell text/schema/hash inspection exited 0. The new sidecar has 142 lines, zero `sorry`/`admit` placeholders and zero trailing-whitespace lines. Manual review checked the ring identities, positive-factor cancellation and quantifier alignment. This is not Lean verification: imports, elaboration, casts and kernel acceptance remain open. No Lean/Lake, Julia, producer/checker execution, solver, sampling, broad regression, external message, intake or registry action occurred.

| Artifact | SHA-256 |
|---|---|
| NEW_P4_032_AdjugateAcceleration.lean | a39485adea19ffd31a2f46a9b6cf0160d888d08ca36c64f4d0e9461fb406b616 |
| remote T-P4-DESCRIPTOR-ACCEL-BRIDGE review | e3b5741ef359bfd850e5d4d86bf4ba654b9a2a4f7eb252547603abaf1bcd6e3d |
| combined_descriptor_remainder_v1.json | 68596f1557aa709d86bc8711ed7985552684dffe7fde290abf03b511f6bd9805 |
| half_centered_bound_v1.json | 225dac3905b873b1fc4b8e2f4f5333cd985b909643c651cd63146a506f2e9dfc |
| exact_checks/combined_descriptor_remainder.py | babaebf0cd5e7f0cf3a68c116d24e0f67dfea547ee906846a2f4da5633c4fb5f |
| exact_checks/check_combined_descriptor_remainder.py | 5f16afadaa1291da81c37e8bab98bd396b6f07e853436e3ce11e9aa0d53c3d0a |
| exact_checks/check_initial_analytic_slab.py | efa9f57d42e6cd70bd0cc5afdeef68a35673a880f5c53e992a2a182c4ca36340 |
| exact_checks/affine_initial_endpoint.py | f8056410ea423dc8568c9efbc9c550c14f22ebf3c509edb56a47a1cc82d9b193 |

Related completed handoff: `review-GH-MATH-P4-DESCRIPTOR-PUPPER-source-binding-codex-20260908T081829.md` separately documents the conditional growthMu/growthR/growthH/growthK values and the component_to_full/source_metric_cap hypotheses. Neither sidecar establishes physical source binding, an admitted P_upper, a scalar residual A_upper charge, or a final positive target.
