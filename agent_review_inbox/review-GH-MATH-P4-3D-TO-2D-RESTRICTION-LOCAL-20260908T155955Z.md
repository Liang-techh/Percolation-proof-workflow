---
kind: review_result
review_id: review-GH-MATH-P4-3D-TO-2D-RESTRICTION-LOCAL-20260908T155955Z
task_id: GH-MATH-P4-3D-TO-2D-RESTRICTION
source_agent: codex-restriction-math-lane
created_at: 2026-09-08T15:59:55Z
integration_status: pending
admission_label: pending
status: CONDITIONAL_RESTRICTION_IDENTITIES_MISSING_ACTUAL_WITNESSES
proof_status: paper_exact_algebra_not_kernel_verified
source_binding_proven: false
actual_same_cell_evidence_constructed: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTUAL-CELL-PACKET-LOCAL-20260908T155615Z.md
predecessor_sha256: 422def58079888605e681a219fda11ad2b24995fac6af229b913d6a4b43ba62f
requested_action: choose retained-coupling restriction or exact Schur elimination and supply same-cell actual row and observable witnesses
---

# Block456 to B=(4,5): exact conditional interface, no actual packet

This consumes the supplied revision-784 actual-cell obstruction via the
predecessor artifact, without reading or changing state. Only this new review
is written. Mathematical identities below are paper derivations, not compiled
theorems or new source certificates. No q6 or target-cap example is repeated.

## 1. Source object before dimensional reduction

Fix one full source state x and one cell Omega in that SAME state space.
Set C=(4,5,6), E=(1,2,3), B=(4,5), j=6. Use one symmetric regularized
matrix M and actual acceleration a, with the explicit sign convention

```text
M a = F + e.
```

F, e and M must have a specified common interpretation: analytic ideal model,
exact-real FD model or decoded runtime with balance defect. The symbol e is
not automatically zero. A source-to-model matrix difference must also be
charged if replacing M by a nominal/model matrix.

Two legitimate starting three-dimensional descriptors are:

```text
Retain E: T=M_CC,
          g=F_C+e_C-M_CE a_E,                T a_C=g.

Eliminate E (J_E=M_EE^-1):
          T=M_CC-M_CE J_E M_EC,
          g=F_C+e_C-M_CE J_E(F_E+e_E),       T a_C=g.
```

Inverse identities, symmetry and the full balance are premises. The first
descriptor is not the second; neither is automatically the constant nominal
K=M0CC456 appearing in the existing residual-budget producer.
All arguments remain functions of x, including retained remote accelerations.
Reducing the matrix dimension does not project Omega down to two angles or
discard the source variables on which g depends.

## 2. Two legal 3-to-2 routes

Write the selected T and its complete g, in order (4,5;6), as

```text
T = [[A,h],[h^T,d]],   a_C=(u,v),   g=(p,s).
```

A is symmetric 2x2, h is 2x1, u=(a4,a5), v=a6.

| Route | 2x2 matrix S | Effective RHS f | Additional premise |
|---|---|---|---|
| Principal-row restriction | A | p-h*v | First two actual rows |
| Eliminate joint6 | A-h*h^T/d | p-h*s/d | Third actual row and d!=0 |

In the first route starting from retained E, this is exactly
`M_BB a_B = F_B+e_B-M_BE a_E-M_B6 a6`.
Thus the old remote order D=(1,2,3,6) includes joint6; M_BD*a_D must include
all four columns. It is invalid to take the principal block and retain p as
its RHS unless h*v=0 has been separately proved.

In the Schur route, with g=g0+epsilon, the new defect is
`epsilon_B-h*epsilon_6/d`; taking only epsilon_B loses a source term.
When E was already eliminated, this is the sequential elimination of
D=(1,2,3,6). Its equality to direct four-coordinate elimination follows only
with the relevant inverse identities (e.g. full SPD suffices). The retained-E
route followed by joint6 elimination still retains E acceleration in its RHS;
do not identify it with complete D elimination.

These operations do not permit imposing v=0 because the angle cell evaluates
q6=0. A configuration slice is not an acceleration or trajectory constraint.

## 3. Same-source determinant and signed numerator

For either route write S=[[a,b],[b,c]] and use the corresponding complete f.
The exact objects required by the current adjugate consumer are

```text
D2 = a*c-b*b,
Ntheta = ell1*(c*f1-b*f2) + ell2*(a*f2-b*f1).
```

ell here is a fixed observable covector, NOT the producer's nominal residual
vector lBase. Preserve the whole signed expression before enclosure.
The cell evidence must supply positive rational delta<=D2 and |Ntheta|<=R,
with the same packet gate R<=delta*A_cap. No such numbers are generated here.

For the Schur route, det(T)=d*det(S). Positive d and a det(T) lower bound
alone do not give a numeric det(S) lower bound without an upper bound on d;
if det(T)>=Delta>0 and 0<d<=d_upper, then Delta/d_upper is a conditional
lower bound. A principal determinant det(A), a constant origin determinant,
or an M_EE Cholesky pivot is not det(S).

A division-free alternative is the symmetric scaled descriptor

```text
S_tilde=d*A-h*h^T,  f_tilde=d*p-h*s,
det(S_tilde)=d^2*det(S)=d*det(T),
Ntheta_tilde=d^2*Ntheta.
```

This follows by multiplying BOTH sides of the reduced descriptor by d.
Its determinant/numerator bounds must be established for these scaled objects
on the same cell; no unscaled field may be reused by name. d!=0 remains
required for equivalence with the eliminated system. Positive definiteness
would provide d>0 but is not supplied by arbitrary descriptor syntax.

## 4. Metric transport: what H does and does not mean

The inspected three-dimensional producer intends H=K^-1 for constant
K=M0CC456, while T above may depend on x and may already be a Schur matrix.
H is a force-residual budget metric, not an acceleration descriptor. The
adjugate consumer itself takes no H field. Its acceleration observable bound
and a residual H-budget need an explicit bridge if combined.

For the SAME SPD K, partition K=[[K_B,k],[k^T,k6]], set
K_s=K_B-k*k^T/k6 and write a residual z=(y,t). Exact identities are

```text
z^T K^-1 z
 = (y-k*t/k6)^T K_s^-1 (y-k*t/k6) + t^2/k6
 = y^T K_B^-1 y
   + (t-k^T K_B^-1 y)^2/(k6-k^T K_B^-1 k).
```

Consequently a proved three-dimensional upper budget Q3<=W can transport to
either `y^T K_B^-1 y<=W` for the plain projection, or
`(y-k*t/k6)^T K_s^-1(y-k*t/k6)<=W` for the corrected projection.
These are different residual maps. The principal block (K^-1)_BB equals
K_s^-1, NOT K_B^-1; merely slicing H is the zero-extension metric and does
not justify a bound on arbitrary y with the discarded component unspecified.

Apply any chosen linear residual map to BOTH lBase and port, including actual
defect, to preserve total-residual identity. The K-based correction above is
not the T-based RHS correction unless the needed block ratios/matrices match.
If the map depends on x it is still a pointwise force identity, but it is not
a fixed affine observable derivative without additional derivative terms.

The existing producer's Q3 bound is nominal port-only and uses an acceleration
quadratic form including a6. Dropping the a6 contribution from its upper bound
is not licensed by the projection inequalities. Actual defect and final beta
allocation remain separate obligations even after valid metric transport.

## 5. Exact obstruction in the actual source interface

Freshly inspected external source directory:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

`routeB_compact_block456_descriptor_structure_audit.jl` lines 43-71 defines
MDD456, DeltaMDC456, constant M0CC456, lBase456, remote correction constraints,
port constraints and total constraints. Its equations include

```text
MDD456*vD456 + DeltaMDC456*aC456 = 0,
rC456=MCD456*vD456,
lT456=diag(IVAL_C)*fC456-K*aC456+rC456.
```

They do NOT by themselves establish the actual three-row balance T*a_C=g.
One could rearrange the last equality as
`K*a_C=diag(IVAL_C)*fC456+rC456-lT456`, but an unbound lT456 leaves this
RHS unconstrained. This tautological rearrangement cannot create numerator
enclosures or physical source rows.

The minimal exact obstruction to the naive principal restriction is the
unproved term h*a6 (and any retained M_BE*a_E). The obstruction to elimination
is the absent third ACTUAL force row/inverse premise. The existing correction
row involving vD456 is not that missing joint6 force row.

For each of the five current SameCellEvidence fields:

| Field | Condition still missing for cell (5.6,3,83) |
|---|---|
| row1 | Actual three-row source balance plus selected route's complete RHS |
| row2 | Same balance, coordinate order and defect interpretation as row1 |
| determinant_lower | Bound for the selected A, Schur S or scaled S_tilde, not another mass object |
| numerator_upper | Bound for the selected matrix, complete RHS and fixed ell, retaining signed correlation |
| observable_binding | theta''=ell1*a4+ell2*a5 from the actual observable and trajectory semantics |

No existing row/CSV inspected supplies this common packet. The predecessor
cell remains a partial nominal port candidate; this is a missing-witness
obstruction, not a proof that a valid packet cannot exist. The next useful
artifact is one authenticated full-state cell with actual force rows, followed
by ONE chosen restriction/reduction and its bound/observable witnesses.

## Current byte bindings and validation boundary

SHA256 was freshly recomputed for these inputs:

| Input | SHA256 |
|---|---|
| Predecessor actual-cell review | 422def58079888605e681a219fda11ad2b24995fac6af229b913d6a4b43ba62f |
| Workspace NEW_P4_032_AdjugateAcceleration.lean | a39485adea19ffd31a2f46a9b6cf0160d888d08ca36c64f4d0e9461fb406b616 |
| External routeB_compact_block456_descriptor_structure_audit.jl | 9e67520934801c87d0bbe14c550f755afe80ffd6eacd1b6572fc65c52fc6cd79 |
| External routeB_compact_block456_port_bi_partition_probe.csv | 1af8d59bf7253f992f13ad9318ea16ad5adb8cfa387dc5866b2f41ca4836dce4 |

The matching-metric producer excerpt at lines 169-184 was reread, not executed.
The cell geometry and broader missing-artifact inventory are consumed from
the hashed predecessor; this turn does not repeat their producer audit.
No source admission, compiled theorem, authenticated historical run or new
constant enclosure is claimed. State, registry and existing artifacts untouched.
