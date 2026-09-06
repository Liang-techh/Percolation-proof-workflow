# Full source signed-gap audit

This leaf owns only `examples/routeb_signed_gap_source/`. Its evidence concerns
the exact rational Fourier source, all six axes, and conditional all-state
endpoint inequalities. It does not prove the physical DH/FD/Float64 binding,
full-horizon J<=1, or feasibility of a dissipation matrix. No trajectories,
prefix force-budget search, broad regressions, browser, registry or state
writes are used. Every audit executes a saved copy after its inputs, code and
this report have been snapshotted and hashed. All attempts remain in `output/`.

Run `python -B examples/routeb_signed_gap_source/verify.py` from the workspace.
The wrapper creates a unique attempt, opens its terminal log before launching
the audit, waits synchronously, and saves an exit receipt and output hashes.
Only copied modules are imported, with bytecode disabled; their main functions
are not called. `before_run.json` identifies every original path and SHA256.
The wrapper's post-run receipt checks every code/input snapshot for changes.

The first audit, `run-20260905T203002Z-f4b7c48a`, passed before the coordinator's
new global gravity inequality was added. It is preserved without alteration.
Later attempts add that inequality and the affine residual multiplier check;
each attempt's own report/code snapshot defines its exact scope. See the
latest successful attempt's `RESULTS.md`, `audit_results.json`, and `receipt.json`
for the final values and execution evidence. No failed audit has been erased.

## Exact source and conventions

The input mass ledger has 610 Gaussian-rational rows, the potential 17 rows,
and the complete Coriolis ledger 2,852 rows. They are read directly from the
original `routeB_dense_Mq` CSVs into the pre-run snapshot. Write

    M(q) = mu I + sum_nu M_nu exp(i nu.q),   mu=1/1000000.
    U(q) = sum_nu U_nu exp(i nu.q).

All fractions and complex real/imaginary parts are exact. Both conjugates are
present in the CSV. The mass is symmetric and real by coefficient comparison;
q1 and q6 are cyclic configuration coordinates, but their velocities and
their force rows are fully retained. The audit reconstructs M0=M(0),
H0=Hessian U(0), gradient U(0)=0, both M0 inverse products, the entire nominal
acceleration map and A14 from the saved coupled reference. Mu is also checked
against the Julia source token. It cancels exactly from M0-M(q); its derivative
is zero. This is exact-real intended-source semantics, not identification of
floating point or finite-difference computations.

The coefficient audit is independent of the old block restriction. For EVERY
ordered i,j,k in 1..6, it compares the stored CSV entry with

    Gamma_ijk = (partial_k M_ij + partial_j M_ik - partial_i M_jk)/2.
    C_i(q,v) = sum_jk Gamma_ijk(q) v_j v_k.

Empty polynomials are checked too. It checks Gamma_ijk=Gamma_ikj and all 216
identities Gamma_ijk+Gamma_jik=partial_k M_ij. For Cmat_ij=sum_k Gamma_ijk v_k,
the latter is the coefficientwise statement that dot M-2 Cmat is skew.

For the requested power identity, BOTH sides are assembled independently from
the stored Gamma and differentiated mass, collecting ordered triples into
each of the 56 unordered degree-three velocity monomials. They agree at all
141 Fourier frequencies in the union, including zeros: 7,896 COMPLEX slots
(15,792 rational scalar comparisons). Thus, for all real q,v,

    sum_i v_i C_i(q,v) = (1/2) sum_ijk partial_k M_ij(q) v_i v_j v_k.

No parity assumption or missing factor of two for mixed velocity monomials
is allowed. This proves the analytic all-six-axis work cancellation from
these CSV coefficients. It does not assert that a numerical C routine has
exactly the same work at machine precision.

## Complete Sgap coefficients and gravity

Put u=q2, s=q2+q3, x=q4, y=q5 and

    A=762237/200000, B=242307/200000, Cg=20601/400000.
    U=10791/4000 + A cos(u)+B cos(s)+Cg cos(s+y)
                    + Cg sin(s)(1-cos(x))sin(y).
    Psi(z)=z^2/2+cos(z)-1.
    p=sin(s)(1-cos(x))sin(y).
    R=U-U(0)-(1/2)q'H0 q = A Psi(u)+B Psi(s)+Cg Psi(s+y)+Cg p.
    Sgap=(1/2)v'(M0-M(q))v-R.

The entire potential Fourier polynomial, its twist gradient, and its twist
square identity are compared exactly with the source. In particular

    p_s=cos(s)(1-cos(x))sin(y),
    p_x=sin(s)sin(x)sin(y),
    p_y=sin(s)(1-cos(x))cos(y),
    h=H0 q-grad U
      =-A(u-sin(u))e2-B(s-sin(s))(e2+e3)
       -Cg(s+y-sin(s+y))(e2+e3+e5)
       -Cg[p_s(e2+e3)+p_x e4+p_y e5].

`Sgap_fourier_coefficients.json` exports the FULL Fourier-polynomial Sgap in
original coordinates: scalar Fourier terms U(0)-U, all unordered v_i v_j
coefficients of half the mass gap, and all q_i q_j coefficients of half H0.
Mixed factors are already included. There is no hidden quadratic q term or
omitted constant. `r0_fourier_coefficients.json` also exports all six complete
signed forces r0=(M0-M)a0+h-C, combining the mass columns with a0 BEFORE export.
It uses Y=(q1..q6,v1..v6,w,c) for linear terms and original v for quadratic
terms. Eta is excluded and must be added once by the consumer.

The differentiated kinetic cubic coefficients are checked against -v'C,
and the potential coefficients against -grad U. With q'=v, v'=a this gives

    dot Sgap = v'[(M0-M)a+h-C].

If delta=a-a0 and M delta=r0+eta, then

    dot Sgap = v'M0 delta-v'eta.

This last substitution requires the stated actual-force equation and enough
regularity for the chain rule. It requires no mass positivity or independent
absolute Coriolis component estimate. Along absolutely continuous solutions
where that chain rule holds, the identity holds almost everywhere and

    integral k v'M0 delta
      = [k Sgap]_0^T - integral k' Sgap + integral k v'eta.

## Source-specific signed squares, not component norms

Choose one representative nu of each nonzero conjugate pair by its first
nonzero component being positive. There are 70 such mass modes. With
z=(v1,v2,v2+v3,v4,v5,v6) and v=S z (S32=-1, other diagonal entries one), set

    A_nu=S' Re(M_nu) S,   B_nu=S' Im(M_nu) S, theta=nu.q.
    Kgap=(1/2)v'(M0-M)v
        =sum_nu [(1-cos(theta)) z'A_nu z + sin(theta) z'B_nu z].

The sine sign is PLUS: M_nu exp(i theta)+conjugate equals
2 Re(M_nu)cos(theta)-2 Im(M_nu)sin(theta). The audit reconstructs half dM
from this real representation, including the constant Fourier mode.

Each A_nu and B_nu has an exact rational square completion

    z'A_nu z = sum_l alpha_nu,l (a_nu,l'z)^2 = Aplus-Aminus,
    z'B_nu z = sum_l beta_nu,l  (b_nu,l'z)^2 = Bplus-Bminus,

where plus/minus sums contain positive weights and nonnegative squares.
All 227 factors and their signs are exported; 5,040 rational matrix-entry
comparisons reconstruct the 140 transformed matrices. Indefinite matrices
are retained: if the residual has zero diagonal, its cross entries use
2bij zi zj=bij/2[(zi+zj)^2-(zi-zj)^2]. No numerical eigenvalue or tolerance
classifies a sign. The transformed metric is not substituted into a physical
force expression: only the velocity variables of these quadratic forms change.

Let t=1-cos(theta)>=0 and sigma=sin(theta), sigma+/-=(|sigma|+/-sigma)/2.
The exact nonnegative positive/negative kinetic decomposition is

    Kplus =sum [t Aplus + sigma+ Bplus + sigma- Bminus],
    Kminus=sum [t Aminus+ sigma+ Bminus+ sigma- Bplus].

For gravity, writing rho=1-cos(x), the exact identity

    -Cg p = (Cg/4)rho(sin(s)-sin(y))^2
            -(Cg/4)rho(sin(s)+sin(y))^2

gives Sgap=Splus-Sminus with

    Splus =Kplus +(Cg/4)rho(sin(s)-sin(y))^2,
    Sminus=Kminus+A Psi(u)+B Psi(s)+Cg Psi(s+y)
                     +(Cg/4)rho(sin(s)+sin(y))^2.

Both parts are globally nonnegative. Their difference is signed. Source
Taylor witnesses at v=0 prove both signs even in the original full12 ball:
q=t(0,0,1,2,-1,0) has Sgap>0, while q=t e2 has Sgap<0, for
0<|t|<=1/20. Exact quartic coefficients and sixth-order remainder constants
are in `audit_results.json`; these are state witnesses, not trajectories.

## Independent check of the coordinator's global gravity bound

The claimed bound is valid globally with a STRICT rational constant margin.
The coordinator's simpler quarter-angle proof needs no Taylor expansion or
angle split. Put t=z/4. Double-angle identities give

    Psi(z)=8t^2-8sin(t)^2 cos(t)^2
           =8sin(t)^4+8(t^2-sin(t)^2) >=8sin(t)^4,
    sin(z)=4sin(t)cos(t)cos(2t),
    sin(z)^4<=256sin(t)^4.

Here |sin(t)|<=|t| and |cos|<=1 hold globally. Therefore
Psi(z)>=sin(z)^4/32 for every real z. The reduced polynomial identity and
8/256=1/32 are checked exactly; the trigonometric identities and inequalities
are justified by this analytic proof. No local-angle premise enters.

Let a=|sin(s)|, b=|sin(s+y)| and rho=1-cos(x). The sine addition formula
sin(y)=sin(s+y)cos(s)-cos(s+y)sin(s) yields |sin(y)|<=a+b. Also
a^2+ab<=2a^2+b^2/4 because (a-b/2)^2>=0. Since A Psi(u)>=0,

    R >= B a^4/32+Cg b^4/32-Cg rho(2a^2+b^2/4)
      = B/32 (a^2-32Cg rho/B)^2
        +Cg/32 (b^2-4rho)^2-kappa rho^2,
    kappa=32Cg^2/B+Cg/2 < 1/10.

The complete polynomial identity in a^2,b^2,rho and the strict last gate are
checked as rational coefficients in `polynomial_gates.json`, which gives the
exact kappa and margin. Consequently

    R >= -kappa rho^2 >= -rho^2/10 >= -x^4/40,
    Sgap <= Kgap+kappa rho^2 <= Kgap+x^4/40.

The last step uses 0<=rho<=x^2/2. On |x|<=X the strongest bound used here is
kappa*min(2,X^2/2)^2, intersected with the signed twist bound. This improves
the upper endpoint without ever assuming R>=0. Python proves the finite
polynomial gates; the trigonometric proof is the mathematical argument above.
No Lean status is claimed for this leaf or for another agent's unfinished work.

## Rigorous all-state endpoint bounds on the existing conditional enclosures

For every exported phase and every signed-square velocity row, the audit
constructs the SAME nominal-plus-J functional support inequality as the
existing prefix audit:

    |ell Y(t)| <= N_ell,j + K_ell,j sqrt(b),  t in [j/128,(j+1)/128],
    K_ell,j^2 >= integral_0^((j+1)/128)
                  ell exp(A14 tau) Bdelta Q Bdelta' exp(A14' tau) ell',
    Q=L^-1, diag Q=(3,8,95/7,165/7,45,90), Q23=Q32=-5.

This is scalar Cauchy-Schwarz after variation of constants for the SAME
initial state and input, conditional on J(t)<=b. N uses one full12 ball of
radius 3/20 and the single ramp parameter c^2<=3, w(0)=0. The entire signed
linear row is combined before taking its initial support or kernel bound.
All 97 functionals are exported. Functionals share the same state; multiplying
their valid upper bounds relaxes correlations but does not assert independent
initial balls or a new trajectory set.

The copied finite-gain helpers enclose exp(A14 t) on 128 CLOSED time cells:
scaled degree-28 step exponential, degree-12 local expansion, explicit Taylor
remainders, and charged integer-grid rounding. Kernel upper bounds integrate
ALL preceding lag cells. The negative Q23 contribution is kept in the scalar
kernel expression before its interval enclosure. Fractions and integers
determine every gate; floating values are printed only for display.

Only the new 97 functional enclosures and signed endpoint expressions are
evaluated. The force residual envelope, preconditioner search and J-prefix
bootstrap are NOT rerun. Two fixed diagnostic conditionals are J=0 and J<=1
over the original horizon. For the 72 already established conditional cells
through 9/16, the exact published strict barrier is used, and each new row cap
is intersected with the published coordinate enclosure. Those published caps
are imported premises, not reverified nonlinear prefix certificates. Their
ordered times and strict derived-J/barrier inequalities are checked.

For phase cap Theta and square-row caps H_l, let

    Aplus_cap=sum_(alpha>0) alpha H_l^2,
    Aminus_cap=sum_(alpha<0) (-alpha) H_l^2,

and analogously for B. The mass contribution of ONE mode lies in

    [-c Aminus_cap-s max(Bplus_cap,Bminus_cap),
       c Aplus_cap+s max(Bplus_cap,Bminus_cap)],
    c=min(2,Theta^2/2), s=min(1,Theta).

This retains the nonnegative centered cosine and signed velocity forms. The
single common sine multiplies the entire quadratic: its cost uses max of
positive/negative bounds, not their sum. It never bounds |C_i|, |dM_ij| or
independent acceleration components.

Globally 0<=Psi(z)<=min(z^4/24,z^2/2). The twist square phases are bounded
through |sin(s)+/-sin(y)|<=2 min(1,|s+/-y|/2), retaining s+y and s-y as combined
functionals. A second valid twist bound is Cg rho min(1,|s|)min(1,|y|); each
endpoint takes the tighter valid bound. The upper endpoint also uses the
global R lower bound just proved. The restoring sectors contribute only to
the lower endpoint. `endpoint_bounds.json` exports lower and upper values,
their signed kinetic/gravity contributions, and every mode's interval, for
every closed time cell and case.

The initial endpoint gets an additional shared-ball refinement. If a=||q||,
b=||v|| and a^2+b^2<=r^2, then a^2 b^2<=r^4/4 and
a b^2<=2r^3/(3sqrt(3)). These sharpen the centered-cosine/sine mass terms at
r=3/20. All roots are rounded outward by integer arithmetic. This initial
bound covers the entire original full12 ball, not a coordinate box alone.

The endpoints are uniform at EVERY time in a cell, so they apply at any
possible first-exit endpoint on a covered prefix. The conditional J<=1
values on [0,1] do not establish J<=1. The nominal J=0 case is an enclosure
of the reference family, not a claim that actual nonlinear delta vanishes.

## Affine 7x7 handoff

Use V=Y'P Y+k Sgap, with P symmetric and

    d=Y'(P'+A14'P+P A14)Y+k' Sgap-k v'eta,
    g=Bdelta'P Y+(k/2)M0 v,
    dot V=d+2g'delta,  M delta=r=r0+eta.

The coordinator's affine multiplier 2(z+Z delta)'(M delta-r) gives

    H = [ b-d-2z'r,               -(g+Z'r-Mz)';
          -(g+Z'r-Mz),             Z'M+MZ-L ].

The polynomial checker verifies all coefficients of

    (1,delta)'H(1,delta)
      =b-d-2g'delta-delta'Ldelta+2(z+Zdelta)'(Mdelta-r)

for symbolic symmetric M,L, arbitrary Z and arbitrary z,g,r. Thus H>=0
suffices for delta'Ldelta+dot V<=b on the actual residual constraint. Unlike
the older homogeneous multiplier, this does not impose b-d>=0: its top-left
entry is b-d-2z'r. z and Z may be chosen pointwise; they are algebraic
multipliers and are not differentiated in this identity.

For exact symmetric N=M^-1, choose Z=N L and z=N g. Let a*=N r. The reduced
matrix is

    [ b-d-2g'a*,   -a*'L;
      -La*,         L ],

and its quadratic form is

    margin+(delta-a*)'L(delta-a*),
    margin=b-d-2g'a*-a*'L a*.

The reduced congruence is independently checked as a symbolic polynomial.
When L>0, H>=0 iff margin>=0. This is a lossless pointwise identity conditional
on the inverse equations, not a constructed rational cellwise multiplier or
an inverse approximation certificate. The exact-rational source M0 inverse
alone cannot be substituted for N(q).

For a finite implementation, use the exported full r0, regularized source M,
Sgap coefficients, M0/H0/A14 and signed square factors to form b-d-2z'r and
g+Z'r-Mz BEFORE interval bounding. Do not split cancelling summands into
absolute component estimates. The new global R bound is especially useful
when the sign of k or k' requests an upper bound on Sgap.

If Slo<=Sgap<=Shi and k+=max(k,0), k-=max(-k,0), then

    k+ Slo-k- Shi <= k Sgap <= k+ Shi-k- Slo.

Neither endpoint is silently made positive. To close a budget still requires
V(0)<=v0, a uniform covered-prefix V(T)>=vT(T), the PSD inequalities, and the
appropriate strict integral supply/storage margin. Work cancellation and
endpoint control alone do not bound integral delta'Ldelta.

## Open certificate premises

- Source/DH identification and all represented-parameter, FD, trigonometric
  evaluation and solve defects in a single eta remain open.
- The force equation, regularity, identical actual/reference initial/input,
  variation of constants, existence and continuation must be supplied.
- Imported strict-prefix coverage retains its original analytic eta=0 and
  mass-lower-bound premises. This leaf does not transfer it to the implementation.
- The full-horizon J<=1 enclosure is conditional, not a bootstrap conclusion.
- No P,k,z,Z,b, full cellwise 7x7 PSD certificate, or integrated storage/supply
  budget has been found or certified here. General affine multipliers improve
  the admissible certificate class but do not supply feasibility.
- Python exact arithmetic is an auditable finite computation, not Lean
  compilation. No formal certificate, registry admission or state transition
  is authorized by these results.
