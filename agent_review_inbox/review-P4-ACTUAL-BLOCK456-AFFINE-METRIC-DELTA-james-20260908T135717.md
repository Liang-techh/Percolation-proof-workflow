---
kind: review_result
review_id: review-P4-ACTUAL-BLOCK456-AFFINE-METRIC-DELTA-james-20260908T135717
task_id: P4-ACTUAL-BLOCK456-AFFINE-METRIC-DELTA-20260908
source_agent: James
created_at: 2026-09-08T13:57:17-06:00
inspected_commit: ad5f9de1593dedac3b969cd6ab4f3eb8bdad3e78
status: pending
integration_status: pending
admission_label: pending
proof_status: EXACT_SOURCE_POINT_REJECTS_OLD_DIRECT_CAP_AND_FIXED_BETA_ALLOCATION
source_binding_proven: false
runtime_verified: false
lean_compile_status: not_run
registry_eligible: false
formal_certificate_allowed: false
state_mutation: false
registry_mutation: false
---

# Actual block456: regularizer repair does not close direct or cleared intake

## 1. Outcome

Two specific proposed reuses have exact arithmetic no-go results:

- The existing homogeneous nominal-subtracted port ledger is NOT a cap for
  the direct actual remote port. This fails at an actual source-graph point
  in a named existing q-cell, for both rational mu and binary64-mu ideal models.
- On that same point, the nominal-subtracted port is zero, but the existing
  fixed-beta total target is negative. Even a perfect zero port cap cannot
  make the existing lambda=2 allocation prove target>=0 there.

These are no-go statements for the named cap/target on a stated algebraic
domain, not for every alternative Delta/beta/storage, nor for a reachable
trajectory. No complete corrected Q/Delta/K7 instance was found or invented.
The regularizer can be corrected at the formula level as in section5; changing
only the metric, determinant or a stored scalar is not a valid comparator.

Only this immutable review was written. No state, registry, shared script,
source, old negative result or Lean file was changed. No Julia, producer, Lean,
solver or regression was run. Read-only Python stdin used csv/Fraction and
exact Gaussian elimination on a source-derived matrix; this is a focused
arithmetic check, not a source/kernel/runtime admission receipt.

## 2. Actual source and cell used by the exact comparison

External root E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
Q below denotes E/routeB_dense_Mq. All relevant byte hashes are in section7.

From `routeB_compact_qbox_cover_depth3.csv:5853`, select the existing key
`(eta=5.6, depth=3, box_id=1756)`, status INTERSECTS:

```text
q2,q3,q4,q5 in [-1932183566159/4000000000000, 0]
q1=q6=0 as in the port producer's evaluation slice.
```

The exact boundary point q=0 lies in this closed cell. Take dq=0,w=1. This also
satisfies the existing analytic slab's q/dq box and measurable |w|<=2 scope.
The q-cell itself does not assert a time/input law or trajectory reachability.
In particular this is not a claim that q=dq=0,w=1 occurs on a w=ct trajectory.

The full nominal matrix M_Q is evaluated directly from
`routeB_analytic_mass_full_cs_polynomial.csv`: retain exactly the terms with
zero sine exponents, set all cosine powers to one, sum rational coefficients,
then add mu_Q=1/1000000 once on the six diagonal entries. The RHS at q=dq=0 is
exactly the `GwI_DH` list parsed from the regeneration source:

```text
RDH = (1,1/2,3/10,1/5,1/10,1/20).
```

This follows from g0-G(0)=0, zero damping/proportional terms and zero quadratic
Coriolis. No finite-difference runtime cancellation is assumed. Solve M_Q*alpha
=RDH with exact rational elimination, and recheck all six equations exactly.
Both det(M_Q)>0 and det(M0_CC,Q)>0 were checked in this arithmetic evaluation.

The resulting full six-coordinate alpha has common denominator
D=55045306919641125471053338193373 and numerator vector

```text
(67072620432254444407085508000000,
 38059699292563014591671526000000,
 12771373085954591625310118400000,
 15496010610460899685191174600000,
 57359628436617187133182572800000,
 82562335976049469352722168650000).
```

This is a computed point on the selected ideal analytic graph, not a fabricated
generic matrix example, sampled interval certificate or measured runtime solve.

## 3. Direct-port route: actual cap reuse fails on cell1756

Use the K7 review's direct source choice, C=(4,5,6), D=(1,2,3):

```text
p=MCD*alpha_D,    L=MCD*E_D,    d0=0,    H_Q=M0_CC,Q^-1.
```

Here d0=0 describes this isolated direct port, not the full actual defect;
other signed/local terms still need their own source identity. Global sign
reversal of p does not change the following square.

The actual ledger row is
`routeB_compact_block456_port_bi_partition_probe.csv:1043`. Its gamma token is

```text
rho2_m0_upper = 0.02763877883827984077234081186821188530465357191822595529996629922178292124871019
```

Use all THREE exact bdiag*_upper decimal tokens from that SAME row to form
P1756. Exact Fraction comparisons returned

```text
p^T H_Q p > 1/5
gamma1756 * alpha_C^T P1756 alpha_C < 1/100.
```

So the proposed direct-port reuse fails by more than 19/100 at this point.
The larger existing global diagnostic is insufficient too:

```text
gammaGlobal=589578/1000000
BUPGlobal=diag(133374,50185,33335)/1000000
gammaGlobal * alpha_C^T BUPGlobal alpha_C < 9/100.
```

No new Delta is chosen by these comparisons: both candidate cap expressions
are the existing file data. The simple fractions above are exact comparison
thresholds, not replacement certified caps.

Replacing ONLY mu_Q by the exact binary64 literal's rational value in the
ideal analytic matrix and its own nominal H, and solving its own full graph,
gave the SAME strict comparisons (>1/5, <1/100, global <9/100). Thus this
direct-port failure is not repaired by the tiny regularizer change. This
second model is exact arithmetic on a decoded constant, NOT Float64 dynamics.

For reproducibility the exact evaluation digests of compact JSON
`[alpha_strings, p_strings, qH_string, cell_cap_string]` are:

```text
mu_Q: 409bfca8a2aef526a369f99c329f15d35fab56f325758475e6358a5ecc3e1d07
mu_F: 3ad5509a5454f178164df0e0db1d293d520dc77622f7646fd299a6f7955d3fd8
```

This does not contradict the intended old ledger: its operator is
`-MCD*MDD^-1*(MDC-M0DC)`, not MCD applied to full remote acceleration.
No output from the old producer was authenticated as a rigorous enclosure here.

## 4. Adjugate-cleared route: zero port still cannot close fixed beta

The relevant route is section2B of the actual K7 review, NOT the old
2+4 rational-elimination degree audit or the unrelated 2x2 observable kernel.
Its source definitions are A=MDD, B=MDC, B0=M0DC, C=MCD and R_D=E_D RDH.
With eta defined by A*eta=R_D-B0*alpha_C,

```text
v=alpha_D-eta, rC=C*v
delta=det A, J=adj A
delta*rC=C*(delta*E_D+J*B0*E_C)*alpha-C*J*R_D.
```

At the actual q=0 point B=B0. The exact six-row solve gives eta=alpha_D and
rC=0. This was rechecked with a separate exact A solve, not by relabeling vD.
Hence the cleared port is zero for every nonzero delta. Clearing cannot create
a positive reserve which the unscaled target lacks.

The source `lBase456=diag(IVAL_C)*fC456-M0CC456*alpha_C` equals p at this point:
both the factorized and DH nominal controller have the same GwI here, and all
q/dq terms vanish. With rC=0, lT=lBase=p. The ACTUAL frozen beta expression in
the residual Schur source is

```text
betaC456=(1/100)*||alpha_C||^2+(1/10)*(||q_C||^2+||dq_C||^2)+(1/20)*w^2.
```

Exact results for mu_Q:

```text
betaC456 =
5099344342087165633918034487837130517573418633273043860041117129 /
60599716277549823384336998880341537569705479047404765910822342580
< 9/100

direct_total456 = betaC456-lT^T H_Q lT =
-908496145006016245606224697730990370520062591844085847627884168761717525947223 /
6758722017363098327650876161130774484190251396262627754497272897204629481055540
< -11/100.
```

The source fixes lambda=2. For target=0, ANY valid nonnegative unscaled port
cap Delta therefore satisfies

```text
Aalloc = betaC456-2*Delta-2*lBase^T H_Q lBase < -31/100.
```

This is an allocation no-go for that fixed target/beta, even if an ideal K7
certificate supplied Delta=0. It is not an impossibility of all K7 certificates:
cap positivity and allocation are independent. Do not spend a new Q search
claiming it will fix this specific negative allocation.

Because at q=dq=0 the ideal solution is linear in w, the rational-model target
scales as w^2. The same negative coefficient persists for any nonzero smaller w
on the algebraic slice, subject to the stated domain. No time evolution or
full source/runtime admission follows from this slice calculation.

## 5. Corrected exact formula comparator for the regularizer seam

The source-dependent exact discrepancy is

```text
mu_Q=1/1000000
mu_F=4722366482869645/4722366482869645213696
epsilon=mu_Q-mu_F=3339/73786976294838206464000000 > 0.
```

The prior bdiag2/reference negative result remains valid. A corrected comparator
must compare TWO models rather than assert equality of their references.
For both routes M_Q=M_F+epsilon*I6 and M0CC_Q=M0CC_F+epsilon*I3. With SPD,
H_Q<=H_F for the same force vector. This is not a bound on a changed vector.

For the direct isolated port, C and E_D are unchanged, so L is unchanged,
but alpha changes with M. The exact model transition obeys
`M_Q*(alpha_Q-alpha_F)=-epsilon*alpha_F` for the same RHS. A concrete direct
cap must bind the chosen graph; it cannot mix alpha_F with H_Q and call that
the actual corrected point. No current Delta/allocation instance meets that gate.

For the cleared route, A_Q=A_F+epsilon*I3, while B,B0,C,R_D stay fixed under
this regularizer-only change. The exact three-dimensional corrections are

```text
delta_Q = delta_F + epsilon*tr(adj A_F)
                     + epsilon^2*tr(A_F) + epsilon^3
J_Q = J_F + epsilon*((tr A_F)*I3-A_F) + epsilon^2*I3
Ls_Q = C*(delta_Q*E_D + J_Q*B0*E_C)
d0s_Q = -C*J_Q*R_D.
```

These are exact polynomial identities specifying a constructible comparator,
not a newly compiled/source-reified coefficient table. Both det and adjugate
must change. The nonzero denominator obligation remains on the same cell.

K7 must then be assembled with the SAME M_Q,RDH,H_Q,Ls_Q,d0s_Q and
`Delta_s,Q=delta_Q^2*Delta_Q`. Keeping the old cleared cap while only replacing
delta changes the implied unscaled Delta. Recover unscaled hport only after
delta_Q!=0; pass Delta_Q, not Delta_s,Q, into the generic allocation.
No actual Q, Delta_s, matrix-SOS/PSD factor or positive allocation is present
in the inspected jet output or K7 review. The latter is an interface, not a
coefficient/PSD artifact. Source identity for the selected signed total and
controller split remains necessary beyond these polynomial corrections.

## 6. Historical negatives and next hop

Preserved unchanged:

- previous cell83 B_up-vs-rational-M55/reference mismatch;
- historical producer-byte/sign provenance and missing interval admission;
- the origin beta audit's free-acceleration necessary-condition failure;
- prior q6-ray graph exclusion and its runtime/reachability qualifications;
- prior adjugate physical-row recovery, missing joint6 and scaling obligations.

The new point is a full ideal mechanical graph solve, not the free-acceleration
axis used by the old beta screen. The new direct-cap rejection and fixed-beta
allocation rejection do not supersede those older results.

Next hop: first identify whether the intended physical domain contains this
algebraic slice. If it does, redesign the actual beta/storage/target before
attempting positive allocation. If a smaller trajectory-linked domain excludes
it, supply that inclusion/exclusion proof rather than deleting the point.
For direct port obtain its own full-graph affine cap; for cleared port keep the
actual nominal-subtraction and regenerate/reify delta,J,Ls,d0s under ONE mu.
Only after those choices should a same-cell Q/Delta PSD witness be sought.
No state/registry/formal gate changes are proposed by this review.

## 7. Fresh hash pins

Except paths starting examples/ or agent_review_inbox/, rows are relative to Q.

| File | SHA-256 |
|---|---|
| routeB_analytic_mass_full_cs_polynomial.csv | 1a1db0b737abac58afae06e95766d2da91c12425fe1be388364f1dca7db59451 |
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_interval_bounds.jl | 7c7b7254a00b5ce21f6b9f512d5de7145ca8386e0420ecf71e92a5aeb5ca789f |
| routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| routeB_compact_block456_residual_schur_interface_audit.jl | 3d68fff2e71e3c912d45463ce1166e4381a98cefb049478b989cc279520d4d98 |
| routeB_compact_block456_port_bi_partition_probe.jl | 62df8b89f8025081dba985c35863c6f427dde71c225f50e1dba949f0f60bf129 |
| routeB_compact_block456_port_bi_partition_probe.csv | 1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4 |
| routeB_compact_qbox_cover_depth3.csv | 85b907bf8d12f46ee003731c5518a00a9a106c8f5a12e492037ae8fc52b04fdf |
| routeB_compact_dh_gain_descriptor_regeneration_audit.jl | 04b764434601dd0c11b2a6554156fd4d948cf742dbf33472b960e0d54e8235c9 |
| routeB_factorized_descriptor_model.jl | c3007d5e30feeb963a86b9589ade3ca7d95b16316e753e8d18b007aa044cd427 |
| routeB_compact_block456_direct_target_origin_beta_audit.csv | d6260d4a02b1fb32074bd036296c96929b614b6baa2fa4398bd78026d7bf174a |
| agent_review_inbox/NEW_REVIEW_P5_K7_REAL_BLOCK456_INSTANTIATION_20260908.md | 962a2a711342a93f716578d625ea022ae8cf1e5a8f0314c8be8b4afd21b768a1 |
| examples/routeb_p5_source_jet/NEW_EXACT_DH_CELL_JET_20260908.py | 3bd8ac1d468b6f73a5ff230f031ce3d38315b608c90ab0381762054bf0c5a6ae |
| examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_GenericSchurAllocation20260908.lean | a76375770d563f86f7de80fdea970e8d0d0fadd1ed917c262b725c7a8ba47648 |
