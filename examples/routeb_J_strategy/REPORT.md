# A source-inverse and signed-sector route for the actual J budget

This is a read-only mathematical study of the current full6/full12 problem.
Only this new `examples/routeb_J_strategy/` directory was created. No source,
certificate, registry, state, or other sidecar was edited. There were no new
trajectories, sweeps, browser calls, or broad tests.

**Result:** a precise sufficient inequality for the J=1 bootstrap is given
below. It preserves the source inverse and signed force correlations. Two
tempting stronger symmetry assertions are rigorously false, including inside
the original initial ball. This study does **not** establish J<=1, nor show
that the whole J=1 bootstrap is impossible.

**Latest handoff:** the main agent's source-resolved prefix audit and subsequent
preconditioner still leave the norm bootstrap unclosed. See `SIGNED_WORK.md`
for the updated figures, scrutiny of the preconditioner, and the separate
signed-work identity and explicit 7x7 dissipation condition. No successful
mass/Coriolis cancellation certificate is claimed. The older norm lemmas in
this report are valid sufficient alternatives, not a prediction of closure.

## Current checkpoint and scope

The gain checkpoint and final finite-gain results give the direct-output
implications, conditional on the actual correction budget J<=1:

    P_actual(t) <= 4.9729 < 5.6,
    Qterminal_actual(1) <= 11.9025 < 12.

Here x0 is in the full12 ball of radius 3/20, w(t)=c*t, c^2<=3, t in [0,1],
and a0=M0^-1[-(K+H0)q-Dv+G_in*w] is evaluated at the actual state. Define

    delta=a-a0,
    r0=(M0-M(q))*a0 + H0*q-grad U(q)-C(q,v),
    M(q)*delta=r0+eta,
    J(t)=integral_0^t delta^T L delta.

The exact-real regularized mass is the full Fourier source mass plus 10^-6 I.
The existing source/physical premises are needed to identify it with the true
DH model. Analytic-minus-FD, represented-parameter, rounding and solve defects
belong in the single eta; none is discharged here.

The metric is L=Q^-1, where Q has diagonal (3,8,95/7,165/7,45,90),
Q23=Q32=-5, and all other off-diagonal entries zero. The existing rotational
mass premise is M(q)>=L>0. The stored path figures J~.0602 and integral Q(r)
~.3612 remain E1 only; they are not used in any calculation here.

Inputs inspected: the gain checkpoint REPORT, coupled_resolvent DERIVATION
and source_bounds.py, inertial_structure DERIVATION/audit.py/audit_results.json,
block_potential DERIVATION, coupled_linear_reference DERIVATION/reference.json,
rotational_dual DERIVATION, and the final finite_gain DERIVATION/results.json.
The algebra audit directly reads the potential and mass CSVs used by the
inertial audit and checks their M(0), Hessian U(0), and inverse against the
saved rational reference.

## 1. Exact gravity decomposition: three scalar sectors plus a small twist term

Use u=q2, s=q2+q3, x=q4, y=q5; do not constrain any of these coordinates.
Write n=e2+e3, m=n+e5, and

    A=762237/200000, B=242307/200000, Cg=20601/400000,
    p(s,x,y)=sin(s)*(1-cos(x))*sin(y),
    f(z)=z-sin(z).

An exact rearrangement of all 17 source Fourier rows is

    U=10791/4000 + A*cos(u) + B*cos(s) + Cg*cos(s+y) + Cg*p(s,x,y).

Because p has zero Hessian at the origin, the complete gravity remainder is

    h := H0*q-grad U
       = -A*f(u)*e2 - B*f(s)*n - Cg*f(s+y)*m
         - Cg*[p_s*n + p_x*e4 + p_y*e5],                  (1)

    p_s=cos(s)*(1-cos(x))*sin(y),
    p_x=sin(s)*sin(x)*sin(y),
    p_y=sin(s)*(1-cos(x))*cos(y).

This reduces the gravity norm evaluation to fixed force directions and scalar
nonlinearities. The s+y angle must remain combined. For example, the fifth
gravity component is exactly -Cg*[f(s+y)+p_y]; it is not separately bounded
using f(s), f(y), and their absolute values.

For all real z, f(z)=kappa(z)*z with

    0 <= kappa(z) <= min(z^2/6, 2), kappa(0)=0.           (2)

Thus the first three terms are -S(q)q, where

    S(q)=A*kappa(u)*e2 e2^T + B*kappa(s)*n n^T
         + Cg*kappa(s+y)*m m^T >= 0.                   (3)

This is the valid restoring sector. On an enclosure |z|<=Z it also gives
f(z)*(kbar*z-f(z))>=0 with kbar=min(Z^2/6,2), a polynomial sector inequality
for a lifted scalar f(z). Its validity does not require fixing the sign of z.

The remaining twist vector has the explicit all-real bounds

    |p_s| <= min(2,x^2/2)*min(1,|y|),
    |p_x| <= min(1,|s|)*min(1,|x|)*min(1,|y|),
    |p_y| <= min(1,|s|)*min(2,x^2/2).                  (4)

These can be used directly on time cells. Their products preserve the small
block coordinates; they avoid replacing the twist remainder by a cube of
|s|+|x|+|y|. Prefer evaluating the signed p derivatives in (1) whenever the
enclosure supports that; (4) is only a fallback for this vector's norm.

### A rigorous obstruction to making the entire gravity remainder restoring

One cannot extend (3) to all of h. Let

    d=(0,0,1,2,-1,0), q=t*d, v=0, w=0.

The exact Fourier coefficients and the global sine Taylor remainder give

    q^T h(q) = (84039/400000)*t^4 + R6,
    |R6| <= (3816417/8000000)*|t|^6.

Consequently, for 0<|t|<=1/20,

    q^T h(q) >= (668495583/3200000000)*t^4 > 0.          (5)

These states are in the original initial ball: ||(q,v)||^2=6*t^2<=.015<.0225.
There is no neighborhood of the origin on which h(q)=-S_full(q)q with
S_full(q)>=0. In particular, subtracting the complete gravity remainder as
a universally dissipative term is invalid. The twist term in (1) must stay.
This is a sector counterexample, not a dynamical counterexample to J<=1.

Proof of the remainder certificate: for each real Fourier coefficient a_nu,
q^T h contains a_nu*(nu.q)*(sin(nu.q)-nu.q). Its quartic coefficient is
-sum a_nu*(nu.d)^4/6 and its sixth-order remainder is bounded by
sum |a_nu|*|nu.d|^6/120. Both sums are evaluated as exact fractions by the audit.

## 2. Source-inverse defect lemma: bound the requested correction energy directly

Let M>=L>0 be symmetric, Q=L^-1, r0 and eta be arbitrary, and M*delta=r0+eta.
For **any** matrix P (a rational approximate inverse is convenient), put

    E=I-MP.

Then

    ||delta||_L <= ||P*r0||_L + ||E*r0||_Q + ||eta||_Q. (6)

Proof: delta=P*r0+M^-1(E*r0+eta). The mass premise implies
M^-1 L M^-1 <= M^-1 <= Q. Apply the triangle inequality. No closeness condition,
stability assertion, series convergence, or independently selectable physical
acceleration is assumed.

The same lemma can be sharpened by a finite algebraic correction. For n>=0,

    P_n=P*(I+E+...+E^n),
    I-M*P_n=E^(n+1),
    ||delta||_L <= ||P_n*r0||_L + ||E^(n+1)*r0||_Q + ||eta||_Q. (7)

This is a finite identity, valid even when ||E||>=1. Improvement with n is
not asserted in that case. Degree zero or one is the practical starting point.

On each time/configuration cell choose a rational P from the full 6x6 source
mass near the cell center. Approximation errors enter E automatically. Form
P*r0 and (I-MP)*r0 as complete expressions **before** absolute values. The
second expression is a solve defect of the same force, not a new independent
forcing function. Mass dependence only uses u,s,x,y because q1,q6 are cyclic;
all six force and acceleration coordinates are still present.

For a fixed rational theta>0, another sufficient version is

    W_P(q)=(1+theta)*P^T L P +(1+1/theta)*E^T Q E,
    ||delta||_L <= sqrt(r0^T W_P(q) r0)+||eta||_Q.       (8)

A rational matrix W_cell satisfying W_cell-W_P(q)>=0 on the cell is a valid
source-specific force metric there. This needs only a symmetric 6x6 positivity
check. For example, if D_center is its rational center and the symmetric
interval radius matrix is R_entry, then
D_center-rho*I>=0 and rho>=max_i sum_j R_entry[i,j] suffice. Interval/Taylor
bounds for M(q) make this a finite rational certificate. Cell enclosure and
this positivity check are obligations, not results of the present audit.

The original Q estimate remains available pointwise:

    ||delta||_L <= min(sqrt(r0^T Q r0),
                       ||P*r0||_L+||E*r0||_Q) + ||eta||_Q. (9)

Thus the new option cannot worsen the best retained bound. Unlike replacing
M^-1 L M^-1 everywhere by Q, it becomes exact for eta=0 when P=M(q)^-1.

### Concrete source-inverse information at M0

Let W0=M0^-1 L M0^-1. The exact rational audit computes the complete Gram
N^T W0 N for N=(e2,n,m,e4,e5). Display values are:

| force direction | d^T W0 d | d^T Q d |
|---|---:|---:|
| e2 | 2.06210440 | 8 |
| n=e2+e3 | 3.14891965 | 11.57142857 |
| m=e2+e3+e5 | 8.90602893 | 56.57142857 |
| e4 | 7.46662140 | 23.57142857 |
| e5 | 16.61923506 | 45 |

The crucial signed cross term is e2^T W0 n=-1.184242283..., whereas
e2^T Q n=3. Also n^T W0 m=-2.282143238.... Therefore even preserving Q's
original negative (2,3) entry does not preserve the source inverse's directional
cancellation. If f(u) and f(s) have the same sign, their cross term in (1)
decreases the source-inverse cost at M0. Such signs cannot be assumed for the
whole initial ball; they must be retained as variables or justified on a cell.

These M0 values are exact-rational computations displayed as decimals. They
are **not uniform bounds away from the origin**. Equations (6)-(9) supply the
required variation correction. The audit prints all exact Gram fractions.

## 3. Preserve the symmetric velocity quadratic forms

There is no valid all-cubic bound for the complete r0. An exact local witness
from the source Christoffel coefficients is

    q=0, v=t*(e4+e5), w=0:
    C(0,v)=(21/25000)*t^2*e1,
    r0=-(21/25000)*t^2*e1,
    delta=-(21/25000)*t^2*M0^-1*e1                 (eta=0). (10)

Hence r0 is not O(||(q,v,w)||^3). Small nonzero first derivatives of M cannot
be discarded on parity grounds. This witness is an admissible initial-state
slice for sufficiently small t; it involves no trajectory computation.

The useful symmetry is instead C_i(q,v)=v^T Gamma_i(q)v with Gamma_i symmetric.
Let Tq=(q1,u,s,x,y,q6), so original q=S*Tq with S=T^-1, and similarly
v=S*z, z=(v1,v2,V,v4,v5,v6). Then use Gamma_tilde_i=S^T Gamma_i S.
This exactly combines v2,v3 before bounding. In acceleration coordinates the
metric becomes L_tilde=S^T L S and Q_tilde=T Q T^T; its (u,s) block is

    [8, 3; 3, 81/7].

Do not keep the original Q matrix after changing acceleration coordinates.
If only substituting velocity variables in the physical force r0, no output
metric transformation is needed: its force components remain physical ones.

Here is a small finite certificate for a correlated velocity enclosure. For
fixed q,w suppose z=z_c+R*zeta, ||zeta||_2<=1, with rational R. This must be an
outer enclosure of the actual velocities; it is not an extra initial condition.
Let A_v=-M0^-1 D, DeltaM=M0-M, v_c=S*z_c, and

    r_c=DeltaM*a0(q,v_c,w)+h(q)-C(q,v_c),
    Bv_i,*=(DeltaM*A_v*S*R)_i,* - 2*v_c^T Gamma_i*S*R,
    H_i=R^T S^T Gamma_i S R.

The full residual has the exact expansion

    r0=r_c+Bv*zeta-[zeta^T H_i zeta]_(i=1..6).         (11)

This preserves cancellation between the mass-mismatch velocity term and the
Coriolis linear-in-zeta term. Bounding these terms separately is unnecessary.

For any positive definite force metric W, define the rational 6x6 matrix

    G_H[i,j]=trace(H_i H_j).

The certificate

    sigma^2*W^-1 - G_H >= 0                           (12)

implies

    ||[zeta^T H_i zeta]_i||_W <= sigma*||zeta||^2.

Proof: the linear map X -> [trace(H_i X)] has Euclidean-to-W squared operator
norm bounded by sigma^2 under (12). Set X=zeta*zeta^T, whose Frobenius norm
is ||zeta||^2. This is a six-dimensional check despite the symmetric quadratic
monomials. It is sufficient; rank-one information can make the exact bound
smaller. Do not describe the Frobenius relaxation as a sharp tensor norm.

The affine part in (11) is certified by another small matrix. With
Fv=[r_c Bv], beta>=0, lambda>=0, require

    diag(beta^2-lambda, lambda*I_6) - Fv^T W Fv >= 0.   (13)

Then ||r_c+Bv*zeta||_W<=beta on the unit ball, and (11)-(13) give

    sqrt(r0^T W r0) <= beta+sigma.                    (14)

The constant/linear correlations survive in the 7x7 matrix (13). Conditions
(12)-(13) can be enclosed uniformly in the four active position coordinates
and the permitted ramp variable on a time cell. A velocity box can always be
enclosed by an ellipsoid, but paying a sqrt(6) dilation may lose the benefit;
use a proved correlated kernel ellipsoid when available.

For (6), the same construction can be applied after the output maps P and E,
using L and Q respectively, or use a positive definite W_cell from (8) once.
It introduces no free actual acceleration and requires no trajectory sweep.

## 4. Precise interface to the main agent's time-dependent J=1 bootstrap

Let I_k=[t_k,t_(k+1)] cover [0,1]. On every actual solution prefix with
J(t)<=1, suppose the main audit proves membership in cells D_k and supplies
rational nonnegative numbers alpha_k, beta_k, eps_k such that

    sup_Dk ||P_k*r0||_L <= alpha_k,
    sup_Dk ||(I-M*P_k)*r0||_Q <= beta_k,
    ||eta||_Q <= eps_k throughout I_k.

Then a concrete sufficient closure test is

    SUM_k |I_k|*(alpha_k+beta_k+eps_k)^2 < 1.           (15)

Use (1), (11)-(13), or direct signed interval/Taylor assembly to establish the
two source-force bounds. The bounds may also depend on time and be integrated
as polynomials rather than frozen to a cell supremum. Equation (9) allows the
minimum with the existing Q envelope. If using W_cell and (14), substitute
the single bound beta+sigma for alpha_k+beta_k.

Proof of closure: at a first hitting time J(t*)=1, all preceding states satisfy
the assumed conditional enclosure. Integrating (6) squared up to t* is bounded
by the full nonnegative sum in (15), giving 1<1. Continuity excludes such a
first hit. Existence/continuation and enclosure coverage through every earlier
domain exit must also be proved; a block-only enclosure cannot supply the
remote coordinates needed here. A strict margin in (15) is the useful gate;
a conditional upper bound equal to one alone is not a first-hit contradiction.

There is also an integrated error option: if the analytic part of (6) has
L2 norm <=b and integral eta^T Q eta<=e^2, Minkowski gives J(1)<= (b+e)^2.
The source error must be included once, with an explicit remaining margin.

This is a tractable route beyond independent box Q(r)<=754.868: four active
mass coordinates, exact 6x6 preconditioning, three signed scalar gravity
sectors, an explicit small twist term, and 6x6/7x7 rational positivity checks.
The present study establishes the identities and sufficient lemmas, not the
uniform cell estimates required to pass (15).

## Evidence and reproduction

Run `python -B examples/routeb_J_strategy/algebra_audit.py`. It only prints
its result; importing the existing algebra module does not call its main or
write its audit outputs. The successful targeted audit checks the exact
potential rearrangement, the radial obstruction coefficients and strict bound,
the origin Coriolis witness, the source/reference M0 and H0 identities, both
M0 inverse products, metric inversion, and the complete directional Gram.
It also prints source hashes. No Lean verification is claimed for this study.

RETROSPECTIVE DEVELOPMENT NOTE (not a reconstructed execution receipt): the
initial run rejected an incorrect provisional radial
direction/sign combination by an assertion failure. The corrected direction
d=(0,0,1,2,-1,0) passed the Fourier coefficient check and the explicit Taylor
remainder bound. Those earlier development executions had no immutable input
snapshots or terminal.log files; no such receipts are invented here. Only the
final formulas above are asserted. `verify_snapshot.py` performs one new run
from copied inputs, writes before_run.json and input hashes before execution,
opens terminal.log before launching the child, and records its synchronous
exit code plus source-bound audit_results.json and receipt.json. The new
receipt also covers the added reference/provenance identities.
