---
kind: review_result
review_id: review-GH-MATH-P4-ROWSPACE-RECOVERY-MINIMAL-LOCAL-20260908T102010
task_id: GH-MATH-P4-ROWSPACE-RECOVERY-MINIMAL
source_agent: Codex-rowspace-minimality-lane
created_at: "2026-09-08T10:20:10-06:00"
inspected_commit: 30c0c0a151f8aa2fa8f1ce1a081350f66592460c
inspected_paths:
  - agent_review_inbox/review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-LOCAL-20260908T101508.md
  - C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json
integration_status: pending
admission: pending
admission_label: pending
proof_status: EXACT_RATIONAL_ROWSPACE_AUDIT_AND_ABSTRACT_PROOF
source_binding_proven: false
actual_source_rows_recovered: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
requested_action: retain the exact dual-row witnesses and distinguish six original rows from two additional weighted constraints; supply same-source evidence before recovery
---

# Minimal physical row recovery for the current rational X

## Result

For the **current stored rational candidate X**, recovery of physical residual
rows 4 and 5 from the available preconditioned rows 4 and 5 fails the necessary
AND sufficient dual-row-span condition.

The exact minimality is sharper than “need more rows”:

- Physical row 4 alone requires original preconditioned rows {1,4,6}.
- Physical row 5 alone requires original preconditioned rows {1,2,3,5}.
- Both together require all six original preconditioned rows; starting with
  {4,5}, every one of {1,2,3,6} must be added if only original rows are allowed.
- If arbitrary new scalar linear constraints may be certified instead,
  exactly TWO additional independent weighted combinations suffice and are
  necessary. Their formulas are explicit below. This does not supply their
  actual source proofs.

This is finite-dimensional mathematical/rational candidate evidence, not
recovery of any actual runtime residual or a physical trajectory counterexample.
No new Cramer or dynamics proof, source admission, Lean/Julia run or full regression.

## 1. Necessary and sufficient abstract interface

Use one field F (here Q or R), finite dimensions, a measurement matrix
Y:F^n→F^m and a desired physical projection P:F^n→F^k.

The following statements are equivalent:

1. For every residual z, Yz=0 implies Pz=0.
2. ker(Y) is contained in ker(P).
3. Every row of P belongs to the linear span of the rows of Y.
4. There exists a dual recovery matrix L:F^m→F^k with **L Y=P**.
5. rank([Y;P])=rank(Y), where stacking is vertical.
6. For every z,z', Yz=Yz' implies Pz=Pz'.

Consequently the same L gives exact recovery Pz=L(Yz), not merely a
zero-residual implication. No determinant, SPD or inverse premise on Y is needed.
Full row rank of Y alone is insufficient.

Proof of the nontrivial direction: assuming kernel inclusion, define on im(Y)
the map Yz↦Pz. It is well-defined by applying the kernel condition to z−z'.
It is linear. Extend it to the full measurement space using a basis, obtaining L.
Conversely L Y=P immediately gives kernel inclusion.
The row-span formulation says each output coordinate is a linear combination
of measurement rows; the rank criterion is exactly “adding P adds no row direction.”
Equality of measurements reduces to a zero measurement of the difference.

For rational Y,P, a rational recovery L exists whenever this rank test passes;
Gaussian elimination over Q suffices. Real solvability of a rational system
does not require introducing irrational recovery coefficients.

A minimal source-independent Lean-prep statement, NOT an implemented theorem:

    RowRecovery(Y,P) := exists L, L*Y=P
    RowRecovery(Y,P) iff forall z, Y*z=0 -> P*z=0
    RowRecovery(Y,P) -> forall z, P*z=L*(Y*z)  -- with chosen witness L

Concrete source application adds the separate hypotheses
z=residual_source(x), Y=measurement_source(x), and measured row equations/bounds.
Naming these matrices does not produce those source identities.

## 2. Specialization to row selection from invertible X

Let y=Xz, Y=S_I X for an ordered row selection I, and P=P_B select physical
rows B. If X is invertible, put C=P X^-1. Then:

    RowRecovery(S_I X,P)
      iff every row of C has support contained in I.

Proof: if L S_I X=P, multiplication by X^-1 gives L S_I=C; the left side is
zero outside I. Conversely, if C has this support, choose L by restricting C
to I, yielding L S_I=C and hence L S_I X=P.

Thus the union of supports of rows of P X^-1 is the unique inclusion-minimal
original-row subset that recovers all desired outputs. This is not a heuristic
based on small coefficients: any nonzero rational coefficient makes that
measurement necessary for unrestricted residuals.

For each omitted required row j, z=X^-1 e_j is an exact abstract obstruction:
all selected measurements vanish while Pz=(P X^-1)e_j≠0.
This construction is not asserted to lie in the physical source residual set.

## 3. Exact current X calculation and explicit dual rows

The inspected file is

C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/robot_formal_v1/interval_bounds/half_active_vanis2_domain_probe.json

SHA-256:
28710E24C1528F98B3E0B54B388836824B11E6DE8E19491737B6C85BF6FF2D1E

X is its 6x6 rational preconditioner. All indices below are one-based.
A targeted exact Fraction Gauss–Jordan calculation gave rank(X)=6 and checked
BOTH X*V=I and V*X=I for the computed rational V.

The following rows of V=X^-1 are the complete exact recovery covectors:

    row4(V) = [alpha, 0, 0, beta, 0, gamma]
    alpha = 41762158574623343465791/384000000000000000000000
    beta  = 448027162654999/3840000000000000
    gamma = 12877/800000

    row5(V) = [eta, theta, iota, 0, kappa, 0]
    eta   = -366870171535679301/1600000000000000000000
    theta = 80475217491279639/1600000000000000000
    iota  = 3944154584391/80000000000000
    kappa = 200739/4000000

All seven displayed nonzero coefficients are genuinely nonzero; in particular,
eta retains its negative sign. With y=Xz this means exactly:

    z4 = alpha*y1 + beta*y4 + gamma*y6
    z5 = eta*y1 + theta*y2 + iota*y3 + kappa*y5.

For I={4,5}, P=P_{4,5}, the exact ranks are

    rank(Y)=2,
    rank([Y;P])=4.

Therefore current failure is not invertibility of X and not rank(Y)<2.
It is the rank INCREASE by 2 when the desired physical rows are appended,
equivalently their absence from the measured dual row span.

The prior negative 2x2 minor X[{4,5},{1,2}] was rechecked nonzero.
It implies that no nonzero combination of the two measured rows can cancel
both remote columns 1 and 2, consistent with the rank defect above.

As a focused cross-check, all 63 nonempty original-row subsets were tested
until the first successful cardinality; the only minimal successful subset
for both physical rows was {1,2,3,4,5,6}. This is a tiny exact matrix audit,
not project regression. Minimality already follows from the support theorem.

## 4. Exactly two arbitrary additional constraints, not four

The number of additional arbitrary scalar linear measurements needed in general is

    d = rank([Y;P]) − rank(Y).

Necessity: each new scalar row increases the available row-span dimension
by at most one, while d independent desired directions are missing.
Sufficiency: append a basis of the image of row(P) in the quotient by row(Y).
Here d=2.

With the current measured y4,y5, a useful choice is:

    w4 = alpha*y1 + gamma*y6
    w5 = eta*y1 + theta*y2 + iota*y3.

Equivalently these are two residual covectors
w4=(alpha*row1(X)+gamma*row6(X))*z and
w5=(eta*row1(X)+theta*row2(X)+iota*row3(X))*z.

Then exactly

    z4=beta*y4+w4,
    z5=kappa*y5+w5.

If a source witness proves y4=y5=w4=w5=0 at the same point, physical rows4/5
are recovered. The two added rows are independent modulo row(Y); the missing
inverse covectors restricted to indices {1,2,3,6} also have rank2.

This route can retain signed cancellation (especially eta*y1 in w5) without
proving y1=y2=y3=y6=0 individually. However w4=w5=0 are NEW source obligations,
not consequences of the old two-row payload and not established by defining w.
Taking the two desired physical rows themselves as extra constraints is another
trivial sufficient choice, but supplies no shortcut to source proof.

For nonzero measured defects, preserve the exact identities above. If separately
certified bounds are available, e.g. |y4|≤b4 and |w4|≤c4, then
|z4|≤|beta|b4+c4; similarly for row5.
A signed correlated bound on w can be tighter than separate absolute boxes.
Zero, bounded and unknown residual statements must not be interchanged.

## 5. Relative recovery when extra SOURCE constraints exist

The universal test above quantifies over all z. If actual residuals are known
to lie in a linear subspace U, the necessary and sufficient condition weakens to

    ker(Y) intersect U subset ker(P).

Equivalently P=L Y on U. If U=ker(Z), this becomes

    exists L,K,  P=L Y+K Z,

or rank([Y;Z;P])=rank([Y;Z]).
Thus Yz=0 and Zz=0 imply Pz=0. This is the precise way that additional
source restrictions might eliminate the earlier algebraic z obstruction.

For affine constraints Zz=c, exact recovery is Pz=L(Yz)+Kc; the offset must
be retained. A zero physical residual requires the corresponding output sum
to vanish, not just the measurement part.

For a nonlinear physical residual set R, the exact condition is that equal
measurements on R have equal P outputs (or its zero-fiber restriction if only
zero recovery is requested). A global linear factor L is sufficient but need
not be necessary on such a nonlinear set. Do not replace an unproved physical
constraint by an invented linear U just to pass the rank test.

There is no supplied U/Z/actual-source restriction in the inspected packet
that proves the missing condition. The previous z remains only an algebraic
counterexample to unrestricted recovery, never a physical trajectory witness.

## 6. Optional single signed observable: a smaller target is a different interface

For one desired covector p, the original-row minimum is supp(p X^-1).
For p=ell4*e4^T+ell5*e5^T, the current covector is

    [ell4*alpha+ell5*eta, ell5*theta, ell5*iota,
     ell4*beta, ell5*kappa, ell4*gamma].

Hence cancellation in the first coefficient can remove original row1 for
that ONE output. If both ell components are nonzero and
ell4*alpha+ell5*eta=0, its support is exactly {2,3,4,5,6};
otherwise both nonzero components require all six. With only ell4 nonzero
the support is {1,4,6}; with only ell5 nonzero it is {1,2,3,5}; zero output
requires no rows.

This signed sparsity is not recovery of both physical rows, and it does not
instantiate the existing adjugate SameCellEvidence, which demands two rows.
A direct projected-source consumer would need its own actual scalar identity
and observable/denominator bindings. In particular the covector arising after
adjugate contraction can depend on state even when the original observable ell
is fixed; all support/cancellation conditions then require appropriate pointwise
or uniform domain witnesses.

## 7. Evidence and action boundary

This turn used read-only JSON/text/hash inspection and in-memory exact rational
elimination/rank/inverse tests. No Lean file or executable checker was created.
No Lean/Lake, Julia, producer, solver, broad regression, state/registry change
or source admission occurred. All numeric statements describe the hash-pinned
candidate X, not authenticated loaded/runtime preconditioner semantics.

Predecessor:
C:/Users/z5242/Desktop/重构版/工作流/agent_review_inbox/review-GH-MIXED-FLOWCHUANFENG-ADJUGATE-LOCAL-20260908T101508.md

SHA-256:
26FEE83738B6F8CCAA8FD3DFC88535E5002E936DDBD08F39D15DAB779DC37F59

Both hashes above were recomputed this turn.
No state was read for proof evidence; existing unrelated .olean files were untouched.

Next minimal choice for the source lane:
either supply all four missing ORIGINAL preconditioned rows {1,2,3,6},
or supply the TWO weighted identities w4=w5=0 (or their certified defect bounds),
or provide a justified source subspace/constraint witness passing the relative
rank test. In each route actual existing y4/y5 equations must also be proved,
not merely exported as polynomial expressions. This review supplies the dual
algebra only; actual_source_rows_recovered=false and admission=pending.

