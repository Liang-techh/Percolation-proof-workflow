# Source-resolved prefix energy: a conditional enclosure, not M4

The original initial set, ramp family, horizon and two physical outputs are
unchanged. This leaf tests a sufficient route toward the actual
`J(t)=integral_0^t delta' L delta <= 1`. It does not substitute a shorter
horizon for the requested T=1 certificate. All calculations here set the
implementation defect eta to zero; physical/FD/Float64 binding is OPEN.

## Exact same-state source identity

Use the saved rational coupled reference, including mu=1/1000000 in M0 and
the Fourier mass. With a0 evaluated at the actual state and actual input,

    r0 = (M0-M(q)) a0 + H0 q - G(q) - C(q,v),
    M(q) delta = r0 + eta,    delta=a-a0(q,v,w).

The earlier rotational dual supplies the conditional analytic premise M>=L,
where Q=L^-1 has diagonal (3,8,95/7,165/7,45,90) and Q23=Q32=-5. Hence
delta' L delta <= (r0+eta)' Q (r0+eta). Taking eta=0 in an audit is NOT
proof that eta vanishes in the original implementation.

## Whole-time nominal and state-error functionals

Let ybar=(xbar,w,c), ybar'=A14 ybar, w'=c, c'=0, w(0)=0. The single
initial x0 has Euclidean norm <=3/20 and c^2<=3. Actual and nominal x share
that same x0 and same w. For any real linear functional ell of y,

    ell(y(t)) = ell(ybar(t))
              + integral_0^t ell exp(A14(t-s)) Gdelta delta(s) ds.

The initial/input enclosure is the support bound

    |ell exp(A14 t)y0| <= (3/20)||row_initial12||2
                         + sqrt(3)|row_c|.

There are not twelve independent radius-3/20 initial conditions. A single
ball is used in each functional. Independence between different functionals
is still relaxed when their subsequent absolute bounds are multiplied.

For a cell [tj,tj+1], bound each squared scalar kernel in the Q metric and
integrate its nonnegative upper bounds from lag 0 to tj+1. If J(t)<=b on
the prefix, Cauchy-Schwarz gives

    |ell(y(t))| <= N_ell,j + K_ell,j sqrt(b),  t in [tj,tj+1].

This is why the K bound must integrate over all preceding lags, not merely
the current time cell. It also explains why nominal bounds alone cannot be
substituted for the same-state a0 along the actual trajectory.

The matrix transition is enclosed with the existing exact-rational, charged
rounding method: scaled degree-28 exponential step, degree-12 local Taylor
polynomials on 128 complete closed cells, and explicit operator remainders.
No samples, numerical eigenvalues, floating safety factors or ODE solves are
used. Linear rows are rounded to a rational grid with their l1 error charged
against the maximum absolute enclosed transition entry. Every final upward
rounding of a candidate prefix cap is rechecked in the nonlinear inequality.

## Source cancellations retained before bounds

The code checks dM=M0-M is zero at the origin and H0 equals the exact
potential Hessian. For every Fourier mode nu and force row i, it combines
all six dM columns with the full a0 coefficient matrix before taking a norm.
Consequently the mass contribution is represented as a sum of

    (cos(nu.q)-1) * A_real,nu y - sin(nu.q) * A_imag,nu y.

The phase nu.q and the combined linear functional A_nu y each receive a
time-dependent support/kernel bound. This is sharper than first bounding
all six independent accelerations and multiplying six mass-entry boxes.

Coriolis velocity monomials are combined after v3=(v2+v3)-v2. The coordinates
are (q1,q2,q2+q3,q4,q5,q6) and their velocities, but phase functionals still
use the exact original Fourier frequencies. Conjugate symmetry and zero
imaginary center permit centered cosine enclosures. The entire real
Christoffel polynomial is used, including diagonal and off-diagonal factors.

The gravity remainder is grouped by potential mode, using the global bounds

    |cos(theta)-1| <= min(2,theta^2/2),
    |sin(theta)| <= min(1,|theta|),
    |sin(theta)-theta| <= min(|theta|^3/6,|theta|+1).

The final original force envelope retains Q's negative cross term in the
formula but upper-bounds it by +10 cap(r2) cap(r3). This loss of sign is
explicit. A resulting large upper bound is not a lower bound or counterexample.

## Exact inertia preconditioning

The second audit adds a valid alternative, not an unproved frozen-inverse
substitution. Let T be identity except T23=7/19 and

    W=diag(1/3,19/117,7/95,7/165,1/45,1/90).

The code checks exactly T'WT=L and LQ=I, as well as the full rational
M0 inverse. Set S=T M0^-1 and B=S(M0-M). The actual equation with eta=0 is

    T delta = S r0 + B delta.

If epsilon bounds the operator from the L norm to the W norm of B, then

    ||delta||L <= ||S r0||W + epsilon ||delta||L,
    delta'Ldelta <= ||S r0||W^2/(1-epsilon)^2, when epsilon<1.

The sufficient operator bound is the weighted Frobenius expression
||B||op^2 <= trace(W B Q B') <= epsilon^2. Each B entry is enclosed directly from its
centered Fourier polynomial. Its interval products retain the signed Q23
term. All force components are combined with S before bounding mass, C and
gravity; T square completion avoids discarding L's correlation afterward.

The minimum of this bound and the original Q(r0) bound is a bound on
delta'Ldelta. It is NOT necessarily a bound on Q(r0). The first
preconditioned run accidentally kept the older JSON field name
Q_r_integral_upper for this minimum. The immutable original is retained;
normalize_receipt.py records a field-name-only correction, with hashes and
no recalculation. Current audit.py uses delta_energy_integral_upper.

## Strict per-cell induction and its limitations

Suppose J(tj)<=bj. On a hypothetical pre-exit prefix of the cell with J<=b,
the preceding source estimate gives J'<=Fj(b) almost everywhere. Thus

    J(t) <= bj + (t-tj) Fj(b).

The strict gate bj+h Fj(b)<b excludes the first hitting time J=b by
continuity. It yields the next bound bj+1=bj+h Fj(b) without assuming the
whole next cell already satisfies J<=b. The companion small-gain leaf now
formalizes both scalar gates and the ContinuousOn first-hit argument, including
a strict-prefix version that never evaluates a source bound on the exit
boundary. Its final run-90JWgVCt compiled successfully. Variation of constants,
integration and source identification remain explicit analytic premises.

A monotone finite search proposes b<=1 and checks strict gates. It does not
claim exhaustive optimization over every cap. The second source revision
also tests b=1 if geometric proposals skip past it. Failure means no tested
sufficient scalar enclosure closed, not that the physical J exceeds 1.

The first immutable audit closes 66 cells, through t=33/64, with the
conditional ideal-model cap J<=21783090379/100000000000. It does not cover
the original T=1 target. A fixed whole-horizon envelope is already 1.9287
at hypothetical J=0 and grows to 778.6365 at J=1; these are upper bounds,
not realized forces. Preconditioning in the second retained audit extends
the conditional analytic prefix to 9/16 with J<=26281199249/200000000000.
It improves the fixed hypothetical J=0 and J=1 bounds only to 1.86868 and
777.318 respectively, not to an admissible whole-horizon budget.
Signed/channel correlations, implementation errors, full continuation
and final theorem/statement binding remain future obligations.
