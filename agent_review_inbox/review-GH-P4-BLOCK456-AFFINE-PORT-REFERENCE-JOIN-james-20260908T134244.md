---
kind: review_result
review_id: review-GH-P4-BLOCK456-AFFINE-PORT-REFERENCE-JOIN-james-20260908T134244
task_id: GH-P4-BLOCK456-AFFINE-PORT-REFERENCE-JOIN
source_agent: James
created_at: 2026-09-08T13:42:44-06:00
inspected_commit: 9e6c4bc04cbcbfc7a2a213a642d7ac615218a671
status: pending
integration_status: pending
admission_label: pending
proof_status: REDUCED_AFFINE_IDENTITY_LOCATED_EXACT_REFERENCE_JOIN_OBSTRUCTED
actual_same_cell_packet_found: false
source_binding_proven: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
---

# Block456 affine port / dense metric / scalar cap: exact join boundaries

## Decision and scope

Located: actual source formulas for an affine reduced-descriptor residual,
the intended dense nominal H, and a scalar-valued homogeneous port cap formula.
Not located: a same-cell actual-flow valuation and a verified affine-defect
cap that instantiate the generic additive consumer together.

New discriminating finding: the symbolic reference uses rational 1/1000000,
whereas the interval port producer adds the inherited binary64 literal 1e-6.
These are NOT the same mass/reference. One stored B_up entry is strictly below
the symbolic model's corresponding mass diagonal. This refutes a proposed
exact reference/upper-mass join, not every possible port inequality.

Only this immutable review was added. No producer, Julia, Lean, solver, full
regression or trajectory check was run. Read-only source/hash inspection and
decoding the existing regularizer literal were used. No synthetic Q/Delta,
actual-state witness, cap, state/registry update or admission was produced.
This task does not reconstruct the other lane's y/d/u/s/D Schur packet.

Read the matching-metric budget/provenance reviews, metric-transport/reference
reviews, actual-cell review at 155615Z, and liuchuanafeng's same-source consumer
review. Their historical producer reconstruction, inverse factorization and
rounding/provenance concerns remain prior evidence, not re-executed findings.

External root E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
Prefix Q below means E/routeB_dense_Mq.

## 1. Which affine identity is actually in the source?

`routeB_compact_block456_descriptor_structure_audit.jl:16-70` fixes
C=(4,5,6), D=(1,2,3), alpha=aC456 and the equations

```text
A v + E alpha = 0,       A=MDD, E=MDC-M0DC
rC=MCD v
lBase=iC-M0CC alpha,     iC=diag(IVAL_C) fC
lT=lBase+rC.
```

On this reduced descriptor and provided A is nonsingular, define
`R=-MCD A^-1 E`. The following source-derived choices are valid, but distinct:

| Named d | L | d0 | Baseline for the generic total |
|---|---|---|---|
| reduced port rC | R | 0 | lBase |
| reduced total lT | R-M0CC | iC | 0, if the entire total is being capped |

The first zero is justified by the displayed reduced equation, not an
assumption that physical forcing vanishes. The second offset is a function
of q_C,dq_C,w, with the actual nominal fC and IVAL scaling from the source;
it is not a fixed numerical bias. The q4/q5 cross-couplings are included in fC.
The inherited `factorized_descriptor_model.jl:192-199` uses its Fourier gains;
the fC6 extension has no added cross coupling. An actual DH-controller residual
cannot be substituted without a separate semantic identity.

In particular vD456 is an auxiliary reduced acceleration variable. The source
does not assert it is the full physical a_D. `nominal_factorized_identity456`
only checks two representations of the reduced equations. No actual trajectory
valuation is constructed by that equality check. This review does not re-derive
the remote forcing alternative or set its contribution to zero.

Thus d=L alpha+d0 IS constructible on the named ideal, but the exact identity
`d_actual=lT` or `d_actual=rC` is an independent missing field. Identifying d
only by its dimension, or by a force/acceleration variable name, is insufficient.

## 2. The real dense H, and a newly explicit reference mismatch

The symbolic Schur interface uses H_Q=inv(M0CC456Q), with

```text
M0_Q = [[350003/3000000,0,1/60],
        [0,200739/4000000,0],
        [1/60,0,50003/3000000]].
```

It retains the 4/6 off-diagonal coupling. The previous factor review supplies
the mathematical transport; this turn neither reconstructs its proof nor
equates this nominal metric with a current-q or remote energy metric.

The interval producer's dependency chain, freshly inspected, is:

```text
port_bi_partition_probe.jl -> routeB_interval_bounds.jl -> dhport_lib.jl
dhport_lib.jl:27                    MASS_REGULARIZER = 1e-6 (Float64)
routeB_interval_bounds.jl:89        BI(x::Real)=BI(BF(x),BF(x))
routeB_interval_bounds.jl:105       BI + Real converts through BI(Real)
block456 probe:analytic_cs_mass_iv  diagonal += MASS_REGULARIZER
```

BigFloat conversion retains the binary64 value; it does not reinterpret the
token as the rational 1/1000000. The literal's binary64 bits, decoded read-only
with .NET from the actual source token, are `3EB0C6F7A0B5ED8D`, namely

```text
mu_F = 4722366482869645 / 4722366482869645213696
epsilon = 1/1000000 - mu_F > 0.
```

This is a source-semantics check, not a Julia execution receipt. For the ideal
analytic raw mass shared by both formulas,
`M_Q=M_F+epsilon*I` and `M0_Q=M0_F+epsilon*I`. The probe recomputes Mzero
through its analytic evaluator; do not attribute its block456 reference to
the raw decimal M0 file just because the included library also reads that file.

There is a direct stored-token discriminator, without an interval rerun.
The actual row `(eta=5.6,depth=3,box_id=83)` has bdiag2_upper exactly

```text
0.05018474999999999999995474811182588625868561393872369080781936645507812500000043
```

The sole M55 analytic CSV record (line289) is 40147/800000; hence the symbolic
regularized M55 is exactly 200739/4000000 = 0.05018475 for every q.
The stored token is STRICTLY smaller. Consequently that P_k cannot satisfy
`P_k-M_CC,Q(q) >= 0`: its second diagonal is negative. This falsifies the
claimed Gershgorin-upper-mass predicate for this exact symbolic model.
It does NOT falsify `R^T H R <= gamma P_k`, which is a different predicate;
a positive input normalization need not upper-bound M_CC to define that norm.

Assuming SPD for the same ideal references, inverse monotonicity gives
`H_Q <= H_F`. Thus an authenticated bound for a fixed vector in H_F can safely
bound that same vector in H_Q. But the actual reduced operator also changes:

```text
R_Q-R_F = epsilon*MCD*A_F^-1*A_Q^-1*E.
```

So output-metric monotonicity alone does not transport the old bound from
R_F alpha to R_Q alpha. A same-cell operator comparison or an explicit bound
for this source-derived difference remains required. No numerical epsilon
budget or new Delta is fabricated here. The prior historical sign-only
producer reconstruction does not remove this dependency-level reference issue.

## 3. What scalar cap has actually been exported?

The matching column is `gamma_k=rho2_m0_upper[k]`, with input
`P_k=diag(bdiag1_upper,bdiag2_upper,bdiag3_upper)` and intended inequality

```text
(R alpha)^T H (R alpha) <= gamma_k*alpha^T P_k alpha.
```

`routeB_compact_block456_residual_schur_interface_audit.jl:18-33` uses the
existing diagnostic constants gamma=589578/1000000 and
BUP=(133374,50185,33335)/1000000. They are literal source fields, not newly
chosen constants, and its scalar charge is gamma*Aup456. That source explicitly
calls them global diagnostics rather than certified per-cell physical data.

Two necessary distinctions for the requested Delta:

- A scalar-valued function `Delta(x)=gamma_k*alpha(x)^T P_k alpha(x)` is a
  valid consumer *shape*. No constant acceleration bound is needed for this
  shape, but its operator and actual-residual identities are still required.
- A numerical cap uniform on the q-cell needs an acceleration/offset domain.
  The cover records only q2..q5, with producer q1=q6=0, no velocity/input/
  acceleration bounds. If L has a nonzero direction at an admitted q and H
  is SPD, the affine norm along free alpha=t*v is unbounded. Thus q-only
  membership cannot generally provide such a constant Delta. This is a
  conditional obstruction, not a claim about accelerations on the true graph.

The located homogeneous cap applies to rC, not to lT=(R-M0)alpha+iC or an
affine actual defect containing controller/FD/solve remainders. A cap for
L alpha alone does not cap L alpha+d0. A source-bound affine quadratic
certificate or separate justified offset/cross-term control is missing.
Neither AFD in the stacked diagnostic nor its free uq/uv symbols are an
instantiated same-cell H-metric affine cap. No Schur packet is reconstructed here.

## 4. Minimal source/hash/units/normalization join

The current algebraic consumer remains
`RouteBP4032GenericSchurAllocation20260908.combined_of_port_budget`, n=3.
Its input r is Euclidean after transport, not a raw generalized-force vector.
The minimum actual attachment is:

| Field | Located / obligation |
|---|---|
| cell_key | Exact cover hash plus eta/depth/box_id, q-coordinate order and slice; full valuation/domain evidence still absent. |
| source_key | Mass CSV, regularizer as exact rational or explicit binary64 value, loader/probe dependencies, nominal controller, and actual-source refinement. |
| affine_identity | Name d and alpha; prove actual d=L alpha+d0. Reduced identities exist; actual source valuation missing. |
| units | alpha is C-acceleration; R/M0 act mass-like to give C generalized-force coordinates; d0=iC for total residual. Do not substitute unscaled fC. |
| metric_key | H inverse of the SAME ordered nominal mass; resolve section2 mismatch rather than matching the string M0. |
| cap_key | Scalar Delta in d^T H d units, squared convention explicit; gamma is already rho squared. Per-state versus uniform cap explicitly tagged. |
| sign_key | Current reduced R is negative; baseline remains lBase and total=lBase+rC. Isolated-square sign invariance does not license changing the combined total. |
| transport_key | A real linear T with sq(Tu)=u^T H u, applied to both baseline and d; preserve coordinate order. |
| consumer_key | r=T d, ell=T baseline, W=Delta, base=actual beta, lambda>1 and actual allocation evidence. Exact target identity uses the same total. |

The quadratic has generalized-force-squared divided by generalized inertia
units (for rotational acceleration, energy/time-squared), not kinetic energy
itself. The precise nondimensionalization must come from the actual model/ledger.
A matching array shape is not a units proof.
Do not add a second debit for d after using this consumer's total-square bound.
Missing fields stay pending; a contradicted exact reference join must be rejected
or replaced by a proved comparison. No consumer change is required by this audit.

## 5. Fresh byte pins

All rows except the last are under Q.

| File | SHA-256 |
|---|---|
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_compact_block456_residual_schur_interface_audit.jl | 3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98 |
| routeB_compact_block456_port_bi_partition_probe.jl | 62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129 |
| routeB_compact_block456_port_bi_partition_probe.csv | 1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4 |
| routeB_compact_qbox_cover_depth3.csv | 85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf |
| routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648 |

Historical CSV source hash remains 29710d03c34b8ef7362132a062888b84b17bb92a16a79e37a44818addbe9c90f;
its already-reviewed reconstruction and admission are not rerun here. The
specific source/reference mismatch above is fresh and can be addressed without
claiming a universal impossibility or inventing a successful additive cap.
