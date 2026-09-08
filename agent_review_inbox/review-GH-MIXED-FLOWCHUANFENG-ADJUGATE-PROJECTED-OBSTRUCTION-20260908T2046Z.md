---
kind: review_result
review_id: review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-PROJECTED-OBSTRUCTION-20260908T2046Z
task_id: GH-MIXED-FLOWCHUANFENG-ADJUGATE
source_agent: Codex-adjugate-takeover
created_at: "2026-09-08T20:46:00Z"
inspected_commit: f75237a764fee61cb88b3bd99ae2386142cc5647
integration_status: pending
admission_label: pending
proof_status: EXACT_STORED_X_PROJECTED_OBSTRUCTION_NOT_SOURCE_THEOREM
source_binding_proven: false
actual_same_cell_packet_found: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
proposed_integration_target: P4.signed_projected_adjugate_source_witness_obstruction
requested_action: retain immutable obstruction; require independent same-source projected residual and determinant/observable witnesses before applying a source-bound acceleration cap
---

# Adjugate takeover: even one nonzero projection needs new source evidence

## Result and increment over the historical lane

No complete authenticated block-(4,5) descriptor/determinant/numerator/observable
packet was located in the bounded search below. Source admission remains pending.

The new exact obstruction is stronger than the historical failure to recover
both physical rows: **the two currently exported preconditioned rows cannot, on
their own, determine or finitely bound ANY nonzero physical residual projection
supported on coordinates (4,5)**. This includes the state-dependent covector
ell^T adj(S) whenever det(S)>0 and ell is nonzero. Thus reducing the goal to one
signed adjugate projection does not eliminate the missing-source obligation.

A single independently certified scalar residual projection can suffice for a
direct projected consumer; that is less evidence than recovering both rows,
but it is NEW evidence, not a consequence of their current two-row expressions.
No synthetic identity is promoted to a source theorem here.

## 1. Current source join: what is actually present

Use W=`C:/Users/z5242/Desktop/重构版/工作流` and
P=`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.
Source hashes at the end bind exact inspected bytes, not semantic authenticity.

| Object | Present content | Missing source premise |
|---|---|---|
| P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | Stored 6x6 rational preconditioner X; analytic first-slab candidate; formal=false | Actual runtime valuation, authenticated same-cell determinant or observable |
| force_balance_bridge_dh_v1.json in that directory | Rows [4,5], centered substitution a=A*x+delta_a, symbolic preconditioned expression | Actual acceleration substitution and equality-ideal bridge explicitly remain unresolved |
| preconditioned_force_balance_identity_dh_v1.json | Two row records for X*((M+epsilon I)*a-tau_DH+C*dq+G)=0; formal=false | Unpreconditioned actual rows; no complete SameCellEvidence |
| W/examples/routeb_p4_3d_to_2d_restriction_lean/NEW_PRINCIPAL_RESTRICTION_20260908.lean | principal_rows consumes heq and retains joint6 coupling | An actual heq inhabitant and physical coordinate map |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean | Algebraic identities and SameCellEvidence with row1,row2,determinant_lower,numerator_upper,observable_binding | A bound source instance of those five fields |
| NEW_P4_032_DHProducerBaseBridge.lean and NEW_P4_032_DHAnalyticAUpper.lean in that directory | Compact source transcription and a residual estimate containing producerMetric(acceleration) | Authenticated physical B-row equations and an acceleration-independent numerator enclosure |

The external dhport_lib.jl was read in full. Lines 58/60 distinguish accumulated
mass and regularized mass; lines 76-102 construct central-FD C/G; lines 105-113
form the controller RHS and return a floating solve. A token or file hash cannot
identify its decoded solve with the analytic Fourier descriptor. This review
does not execute that file or attest its deployed method/environment.

Both DH force payloads' direct references to the domain JSON and dhport source
match fresh SHA256. Their other producer dependencies and polynomial terms were
not reverified. A scoped search for SameCellEvidence, observable_binding,
projected_adjugate and projectedNumerator in workspace examples/artifacts and
the two external directories found only the generic adjugate Lean interface.
This is not a claim that no differently encoded witness exists anywhere.

The later 19:57Z ADJUGATE-SOURCE-WITNESS review was also checked against its
referenced definitions. Its diagonal transcription is a valid algebraic
rearrangement, not an updated physical principal-block witness. In particular,
dhLBase=g-D0*u makes g-dhLBase=D0*u by definition. Its positive constant det(D0)
cannot be substituted for det of the selected physical principal block S.
Bounding the resulting numerator by first assuming the same target acceleration
cap only returns that assumption. No such substitution is made here.

## 2. Freeze the physical block and the residual sign

Keep the principal block B=(4,5), not a newly selected Schur reduction. Let
J=(1,2,3,6), so ALL excluded-coordinate couplings, including joint6, are retained.
Fix the same source/configuration, full state/cell, and real interpretation:

```text
M_A : chosen analytic regularized 6x6 mass, regularizer counted once;
F_A : chosen corrected analytic DH forcing;
ahat: acceleration whose source semantics are to be certified;
r   := M_A*ahat - F_A;
S   := (M_A)_BB;
u   := ahat_B;
f0  := (F_A)_B - (M_A)_BJ*ahat_J.
```

Then, as a definitional residual decomposition, S*u=f0+r_B. This is NOT the
physical zero-residual assertion r=0. It also supplies no bound on r or ahat.
An actual source use must bind all four objects, including the complete FD,
controller, mass-evaluation, RHS-assembly and solve discrepancies as applicable.

Write S=[[a,b],[b,c]], D=a*c-b^2, ell=(ell1,ell2) for the independently fixed
observable covector, and

```text
lambda := ell^T adj(S) = (c*ell1-b*ell2, a*ell2-b*ell1);
N0     := lambda*f0;
Csrc   := lambda*r_B.
```

The exact defect-aware projected identity is

```text
D*(ell*u) = N0 + Csrc.                                      (1)
```

The plus sign follows from r=M_A*ahat-F_A. A residual defined with the opposite
sign must reverse it explicitly. With this convention all correlated signed
terms, including retained couplings and Csrc, must be formed BEFORE taking an
absolute enclosure. An old cancellation in N0 is not a bound on N0+Csrc.

Even granting that the candidate expressions provide the actual measurements
y4=y5=0 for y=X*r is insufficient to set Csrc=0. The following algebra proves
that statement without any test state, trajectory, numerical solve or invented S.

## 3. Exact obstruction for the current stored X

All indices are physical one-based. Let Y consist of rows 4 and 5 of X and let
P_B select residual coordinates 4 and 5. Define the two small submatrices

```text
A = X[{4,5},{1,2}],     C = X[{4,5},{4,5}],
m = det(A) = X41*X52-X42*X51.
```

The focused exact Fraction calculation from the CURRENT domain JSON gives

```text
m = -559156839227989655975571536103807900439816646872206471148558242754560000000000000000000000000000000000000000000000
    /1122038947870973702745619935334275743313470649790397615504547463978478091901812264530645937672041117648162226641221
  < 0.
```

Consequently A is invertible. Define a 6x2 rational matrix Z by its rows:

```text
Z[{1,2},:] = -A^-1*C;
Z[3,:] = Z[6,:] = 0;
Z[{4,5},:] = I2.
```

No full 6x6 inverse is needed. A division-free verification of the construction
can use A*adj(A)=m*I and m!=0; the actual check used exact reduced fractions.
It confirmed exactly

```text
Y*Z = 0_(2x2),                P_B*Z = I2.                    (2)
```

Thus P_B restricted to ker(Y) is SURJECTIVE: for every t in R^2, z=Z*t has
Y*z=0 and z_B=t. This strengthens the old single-vector obstruction.

For any nonzero real covector lambda choose t=lambda^T. Then

```text
Y*z=0,
lambda*z_B=lambda1^2+lambda2^2>0.
```

Scaling z by an arbitrary real k leaves Y*z=0 but scales that projection by k.
Therefore no finite bound for |lambda*z_B| can follow from these two zero rows
alone, even when lambda is fixed. Equivalently there is no recovery covector L
with L*Y=lambda*P_B for any nonzero lambda.

For the adjugate covector in (1), det(S)>0 makes adj(S) invertible. Hence
ell!=0 implies lambda!=0, and the obstruction applies at every such frozen S.
The degenerate ell=0 case is only the zero projection and supplies no nontrivial
observable bound. Allowing S and therefore lambda to vary with state cannot
repair this pointwise obstruction without additional source restrictions.

This z is an ALGEBRAIC residual vector, not a physically attainable residual.
No conclusion of unbounded actual acceleration, failed dynamics or nonexistent
source certificate follows. Actual residual constraints could exclude z; they
must be provided and proved, not inferred from the two-row payload labels.

## 4. Smallest additional signed evidence for ONE output

For a fixed state and fixed nonzero lambda, the missing dual-row direction is
exactly one-dimensional:

```text
rank([Y;lambda*P_B]) - rank(Y) = 1.
```

Necessity follows from (2); sufficiency follows by adjoining the single scalar
measurement lambda*r_B itself, or an equivalent measurement modulo row(Y).
This is a statement about independent scalar information, not a claim that
proving that new measurement is easy. With state-dependent lambda the source
must establish the corresponding scalar FUNCTION identity/enclosure on the
whole claimed cell, not a frozen coefficient at the origin.

The previous ROWSPACE-RECOVERY-MINIMAL review provides a useful optional dual
description. With its exact inverse-row coefficients and y=X*r,

```text
r4 = beta*y4 + w4,     w4=alpha*y1+gamma*y6;
r5 = kappa*y5 + w5,    w5=eta*y1+theta*y2+iota*y3;
Csrc = lambda1*beta*y4 + lambda2*kappa*y5
         + (lambda1*w4+lambda2*w5).
```

These prior coefficient values were not re-inverted in this turn; the new
obstruction (2) is independent of that inverse calculation. The formulas show
the possible source task: enclose the ONE correlated weighted scalar in
parentheses, keeping signs and the current lambda. Do not replace this with
assumptions w4=w5=0 or arbitrary small budgets. Nor does one projected witness
populate both row fields of the existing SameCellEvidence.

For a direct projected route, the existing source-independent
abs_bound_of_positive_multiplier already accepts the abstract scalar identity.
The actual required same-cell interface is:

```text
observableAcceleration = ell*u;
D*observableAcceleration = N0+Csrc;
0 < delta <= D;
|N0+Csrc| <= R;                  independently proved on this source cell
R <= delta*Aupper.
```

Then |observableAcceleration|<=Aupper follows. A separated fallback with
|N0|<=R0 and |Csrc|<=E is valid if R0+E<=delta*Aupper, but loses cancellation
between the two terms. It must not be advertised as the same correlated bound.

Defining Csrc using ahat does not supply its enclosure: substituting (1) into
the proposed bound can merely restate the desired acceleration cap. A valid
producer needs independent source error/control/geometry evidence or an
explicit noncircular absorption argument. No new delta,R,E,Aupper is proposed.

Alternatively, retain the existing two-row SameCellEvidence route: prove actual
rows for S*u=f0+r_B and enclose its complete projected numerator. The single-
scalar path is only a smaller proof interface for the SAME block/observable,
not a claim that this record has been instantiated, nor a switch to Schur data.

## 5. Reopen conditions and admission boundary

At minimum a later source packet must identify:

1. One nonempty cell/full-state domain and one source/configuration/coordinate
   valuation; analytic, exact-real FD and decoded runtime targets stay distinct.
2. The actual principal S with its symmetry and regularizer convention, full
   RHS/couplings, and row equations OR the independently verified projected
   scalar identity with its complete source defect.
3. A positive determinant lower bound for THIS S on THIS cell. A diagonal
   transcription determinant, origin matrix, Schur pivot or mass metric bound
   is not that witness without a proved bridge.
4. The deployed observable, fixed ell and coordinate/time units, and equality
   of its actual acceleration with ell*u. Non-affine/time-varying observables
   need the additional chain-rule terms; choosing a new function by definition
   does not bind the existing downstream consumer.
5. A noncircular signed enclosure of the full numerator and the rational gate,
   all bound to the same source/cell. Global use separately requires coverage
   and actual path inclusion.

The current evidence does not discharge these conditions. This immutable review
can be retained as a narrower obstruction and source-work request, but is not
eligible for source binding, a formal certificate or registry promotion.

## 6. Fresh hashes and targeted check provenance

Each path below is relative to W or P as defined in section 1.

| Prefix/path | SHA256 |
|---|---|
| P/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json | 28710e24c1528f98b3e0b54b388836824b11e6de8e19491737b6c85bf6ff2d1e |
| P/robot_formal_v1/interval_bounds/force_balance_bridge_dh_v1.json | 3045ea1923148c90c8473c8402c7522e99eeda2c1590a494322ca3950d76a107 |
| P/robot_formal_v1/interval_bounds/preconditioned_force_balance_identity_dh_v1.json | e0969aade062fe7c7648a655ea95282e8fd27f9eb7d47c3ffc1b38e33c920f48 |
| P/routeB_dense_Mq/dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean | a39485adea19ffd31a2f46a9b6cf0160d888d08ca36c64f4d0e9461fb406b616 |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHProducerBaseBridge.lean | 94cc1f34d87d376309b750e95811fe0d13a4386fea872dba9b967b0421f73e94 |
| W/examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHAnalyticAUpper.lean | 6b1db125678b95ed08bf19f94f350b9c227681bc72a3d16fa3b8aacb4664d6cc |
| W/examples/routeb_p4_3d_to_2d_restriction_lean/NEW_PRINCIPAL_RESTRICTION_20260908.lean | 1d93e5db2ea613b1f2aaacb6d84aa9613374c62cf3a147cd1b61d8a15a106dc4 |
| W/agent_review_inbox/review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-LOCAL-20260908T101508.md | 26fee83738b6f8ccaa8fd3dfc88535e5002e936ddbd08f39d15dab779dc37f59 |
| W/agent_review_inbox/review-GH-MATH-P4-ROWSPACE-RECOVERY-MINIMAL-LOCAL-20260908T102010.md | 55f000e5f6cf85a9159e5e230a19101caa9d40b00078ff00461cf3b479a08835 |
| W/agent_review_inbox/review-GH-MATH-P4-ADJUGATE-SOURCE-WITNESS-honglianmozun-20260908T1957Z.md | 1abf56945e32edf7295acbdadc268164ff19f623d62ec28afad3e6fdcff4f857 |
| W/agent_review_inbox/review-GH-MATH-P4-CORRECTED-ACTUAL-ROWS-LOCAL-codex-20260908T104515.md | 671076df787d72b460dcb6d154e46238cd6b0be1ea638ac592fb34dcbc170007 |

One focused `python -B -` inspection, exit 0, parsed the actual rational X,
checked its shape, computed m<0 and the two exact products (2), and verified
the four direct hash references described in section 1. JSON duplicate keys
were rejected. Only Python integers/Fraction were used for matrix arithmetic;
no floating-point approximation, full inverse, subset sweep or solver was used.

The exact two-column construction checked, using Python zero-based indices:

```python
a, b = X[3][0:2]
c, d = X[4][0:2]
minor = a*d-b*c
assert minor < 0
Z = [[Fraction(0) for _ in range(2)] for _ in range(6)]
for k, j in enumerate([3, 4]):
    Z[0][k] = (b*X[4][j]-d*X[3][j])/minor
    Z[1][k] = (c*X[3][j]-a*X[4][j])/minor
    Z[j][k] = 1
assert all(sum(X[i][j]*Z[j][k] for j in range(6)) == 0
           for i in [3, 4] for k in range(2))
assert [Z[3], Z[4]] == [[1, 0], [0, 1]]
```

The general surjectivity/projection conclusions are the written algebraic proof
above, not a Lean/kernel result. Source files were read-only; no source exporter,
producer, runtime/interval witness, broad regression, ingestion or admission
tool was run. Initial broad metadata output was truncated; only subsequent
explicit fields, raw hashes and the small exact matrix computation support the
source-status findings. Large polynomial support arrays were not audited.
Only this new immutable review is written for this delegated task; state,
registry, shared scripts and old agent artifacts remain outside its write scope.
