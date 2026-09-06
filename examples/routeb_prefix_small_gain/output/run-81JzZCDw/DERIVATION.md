# Conditional prefix small gain for the same-state RouteB defect

This leaf proves a conditional mathematical bootstrap and compiles scalar
algebra only. It supplies no numerical nonlinear-source certificate, registry
entry, state update, physical-source binding, or completed RouteB goal. The
current source work remains with the main agent. Compile outcomes and immutable
snapshots are recorded in ATTEMPT_HISTORY.md and output/run-*/terminal.log.

## 1. Exact prefix statement and proof

Let T be finite, T>=0, and X:[0,T]->R continuous, X(0)=0. Let b>=0,
0<=k<1 and b+k<1 be constants, uniform in time. Assume the following
**prefix implication**, not merely a bound at selected sample times:

    for every t in [0,T],
    [X(s)<1 for every s in [0,t]] ==> X(t)<=b+k X(t).        (P)

Then, with c=b/(1-k),

    X(t)<=c<1 for every t in [0,T].                         (B)

Nonnegativity or monotonicity of X is not needed for this topological claim.
For its energy interpretation below, X is of course nonnegative and monotone.
The premise (P) does NOT assume its inequality at the exit endpoint.

Proof: c>=0 and c<1 because 1-k>0 and b<1-k. If some X(t)>=1, the
intermediate value theorem and X(0)=0 give a hit of 1. The set of hits in
[0,t] is nonempty and compact, hence has a smallest member tau. Continuity
at 0 implies tau>0. There is no earlier value >=1: equality contradicts
minimality, and a value >1 would give an earlier hit by the intermediate
value theorem. Thus for each u<tau, (P) applies and

    (1-k)X(u)<=b, hence X(u)<=c.

Taking u_n=tau*(1-1/(n+2)) and continuity gives X(tau)<=c<1, contradicting
X(tau)=1. Therefore no value >=1 occurs. Now (P) applies at EVERY t,
including T, yielding (B). For T=0 this is immediate. This is a complete
first-hit argument, with no assumption that the estimate already holds after
exit. The stronger premise using all s<t also suffices.

For J(t)=int_0^t delta(s)' L delta(s) ds, assume L is fixed symmetric positive
definite and delta is measurable and in L2_L on every compact subinterval of
the solution's existence interval. Then J is finite and absolutely continuous
on each such interval, J(0)=0, J>=0, and X=sqrt(J) is continuous. Apply (B):

    J(t)<=c^2<1.                                           (E)

The square-root need not be differentiable at 0; no differential inequality
for sqrt(J) is used. This theorem on an already existing compact interval
does not prove that a maximal solution exists up to T.

## 2. Domains, other exits, and continuation

If (P) is only known while x(s) lies in a source domain D_s, conclusion (B)
holds only up to the first exit from that domain. It excludes J hitting 1
before that exit; it does not exclude a different domain exit.

A sufficient application on [0,1] is as follows. The actual system has a
local absolutely continuous solution, all original initial states are strictly
inside the allowed source domain, and all equations and estimates below hold
on every compact prefix before the first exit of either J<1 or D_s. For each
additional domain boundary there must be an independently justified strict
bound, valid on these same prefixes, that persists at a proposed exit by
continuity. Assume the regularity and extension criterion needed for the
actual ODE: e.g. a Caratheodory vector field, locally integrable time bounds,
local Lipschitz dependence on state, and the solution staying in a compact
subset of its domain through finite times. These conditions exclude a finite
maximal-time obstruction and permit continuation to 1. Discrete Float64
samples alone do not supply such a continuous solution or extension criterion.

A convenient sufficient source-domain construction uses a convex nominal
tube. For a fixed invertible full-state weight S and kernel G_S below, set

    d_S(t) = (int_0^t ||G_S(u)||_op^2 du)^(1/2).

Variation of constants gives ||S(x(t)-xbar(t))||<=d_S(t)X(t). A source region
containing, with strict margin, every closed tube
{z: ||S(z-xbar(t))||<=d_S(t)} for the entire initial/input family therefore
contains every pre-J-exit actual state and its segment to the nominal state.
This justifies a Lipschitz estimate on that tube without assuming future J<=1.
Computing/enclosing such tubes is a new obligation, not done here. If using
an independently chosen box instead, every box face needs its own closure.
An initial ball merely fitting a box is insufficient if it touches a face.

## 3. Same-state force identity and error convention

All equations in this section concern the SAME actual full-six-axis path.
Write x=(q,v), Gamma=[0;I_6], and a0(x,w)=M0^-1(drive-H0 q), where
drive=-Kq-Dv+Gw. For the chosen analytic source M,C,Gforce assume almost
everywhere

    M(q) a + C(q,v) + Gforce(q) = drive + eta,
    M0 a0(x,w) + H0 q = drive.

Here eta is one combined force error, including any source, finite-difference,
floating-point and solve defects that have been defined and bounded. It is
not silently zero. Define

    r0(x,w) = (M0-M(q))a0(x,w) + H0 q-Gforce(q)-C(q,v),
    delta = a-a0(x,w),        r=r0(x,w)+eta.

Subtraction gives M(q)delta=r and

    x'=A x+B w+Gamma delta.

This is exactly the identity in the current coupled-resolvent source; a0 is
not evaluated on xbar in this identity. Let xbar solve xbar'=A xbar+B w
with the SAME initial state and input, so

    y=x-xbar=int_0^t exp(A(t-s)) Gamma delta(s) ds.           (V)

Assume a locally integrable common input (the current target is w=ct,
c^2<=3), absolutely continuous states solving the equations a.e., and local
L2_L integrability of delta. There is no independent nominal-input error in
(V). The full original initial ball is ||x(0)||<=3/20; no coordinate is fixed.

Use the source's full matrix

    Q=diag(3,8,95/7,165/7,45,90), Q23=Q32=-5;  L=Q^-1.

The (2,3) principal determinant is 585/7>0, so Q is positive definite.
Write ||f||_Q=(f'Qf)^(1/2), ||d||_L=(d'Ld)^(1/2); their time norms below
are L2 norms on [0,t]. Assume on the source domain the physical coercivity
premises needed for

    ||M(q)^-1 f||_L <= ||f||_Q for every f,                 (M)

or simply the corresponding actual-path inequality ||delta||_L<=||r||_Q
if only the pathwise closure below is wanted. A sufficient matrix premise
for (M) is symmetric M(q)>=L>0: congruence gives
||L^(1/2)M(q)^-1 L^(1/2)||_op<=1. This does not prove that premise for the
physical source. The current Lean resolvent requires explicit dual and balance
hypotheses; its existence alone is not a uniform physical inverse-mass audit.

## 4. A sufficient noncircular L2 small-gain estimate

Fix an invertible 12x12 weight S, preserving all state coordinates. Suppose
uniformly for all original initial states/inputs and every admissible prefix:

(a) Nominal-path NONLINEAR force: ||r0(xbar,w)||_{L2_Q(0,t)}<=b0, b0>=0.
This is not the nominal residual output ebar used in the current gain receipt.

(b) Incremental source bound along the actual/nominal pair:

    ||r0(x,w)-r0(xbar,w)||_{L2_Q(0,t)}
        <=ell ||S(x-xbar)||_{L2(0,t)},       ell>=0.         (LIP)

One sufficient proof is a pointwise bound
||Q^(1/2) D_x r0(z,w(s)) S^-1||_op<=ell on every segment from xbar(s)
to x(s). With r0 continuously differentiable there, the fundamental theorem
of calculus on that segment proves (LIP) by squaring and integrating. All
segments, inputs and times need coverage. A general causal incremental L2
estimate can replace this pointwise sufficient condition.

(c) State response: ||S(x-xbar)||_{L2(0,t)}<=g X(t), g>=0. In fact let

    G_S(u)=S exp(Au) Gamma Q^(1/2),
    g >= int_0^1 ||G_S(u)||_op du.                         (G)

Since delta=Q^(1/2)z with z=L^(1/2)delta, (V), zero extension, the triangle
inequality for integrals and translation invariance give
||G_S*z||_L2<=||G_S||_L1 ||z||_L2. Full-horizon (G) bounds every prefix.
This is a finite-horizon statement; the coupled A need not be stable.

(d) Error: ||eta||_{L2_Q(0,t)}<=eps, eps>=0, independently justified on
the same admissible prefixes. Sufficiently, int_0^t eta'Qeta<=Eeta<=eps^2.

By (M) on the actual path and the L2 triangle inequality,

    X(t) <= ||r0(x,w)+eta||_L2_Q
         <= b0 + ell ||S(x-xbar)||_L2 + eps
         <= b0+eps + (ell*g)X(t).                         (SG)

Set b=b0+eps and k=ell*g. If k<1 and b0+eps+k<1, Section 1 applies on
every justified prefix, with

    c=(b0+eps)/(1-k),     J(t)<=c^2<1.                    (C)

There is no circularity in deriving a uniform local bound on the hypothetical
region X<1, then improving it to c<1 and using a first-exit contradiction.
There IS a gap if a future full-horizon J<=1 or an unclosed state box is used
to justify (a)-(d). Local square integrability up to every t before exit is
enough for (SG); never assume the desired full-horizon finite energy first.

The available error margin is eps<1-b0-k, requiring b0+k<1. In energy units
a sufficient strict budget is 0<=Eeta<(1-b0-k)^2, taking eps=sqrt(Eeta).
With multiple force errors eta=sum eta_i and separate energy bounds E_i,
eps=sum sqrt(E_i) is safe. Summing their energies without cross terms is not
safe unless an orthogonality/correlation estimate is supplied. If an error
bound itself is eps0+k_eta X, include k_eta in the loop coefficient; it
cannot be counted as an independent constant error budget.

## 5. What a Lipschitz map from r to delta does and does not prove

For fixed q, (M) is a Lipschitz constant at most 1 for f -> M(q)^-1 f in
the Q-to-L norms. That fact alone says X<=||r||_L2_Q, which does not bound r
and gives no small-gain loop. Here r is endogenous to x, and x is driven by
delta. The feedback to estimate is delta -> xbar+Vdelta -> r0 -> delta.
The sufficient estimate (SG) controls that loop while retaining the same state.
It is a pathwise bound and does not require constructing a Banach fixed point.

If a contraction-mapping formulation is desired, for each admissible delta
define x_delta=xbar+Vdelta and

    F(delta)(t)=M(q_delta(t))^-1 r0(x_delta(t),w(t)).

The actual equation is delta=F(delta)+M(q_actual)^-1 eta. A sufficient
incremental bound is ||F(d1)-F(d2)||_L2_L<=k_F||d1-d2||_L2_L on an
admissible ball, with ||F(0)||<=b_F and error<=eps. This yields
X<=(b_F+eps)/(1-k_F) when k_F<1. To use Banach existence additionally prove
the total mapping is defined on, and maps into, a closed complete ball and
is a contraction there. A mere bound on an endogenous eta supplies no
incremental Lipschitz estimate for the total mapping or uniqueness theorem.
None of those existence claims is required for the pathwise bootstrap.

Do not infer the F Lipschitz constant by multiplying the force Lipschitz
constant by a frozen inverse-mass norm. With f(x,w)=M(q)^-1 r0(x,w),

    D_x f[h] = M^-1 D_x r0[h] - M^-1 (D_q M[h_q]) f.

The second term is required. Equivalently the difference at x1,x2 contains
(M(q1)^-1-M(q2)^-1)r0(x2,w). A weighted bound on D_x f gives a valid k_F
after the state gain (G), but must include that term. Section 4 avoids
derivatives of M^-1 altogether by applying (M) to the actual total force
before splitting r0 into nominal and incremental parts. It may be conservative
but is sufficient and logically noncircular when its domain is justified.

## 6. Source-grounded assessment at this checkpoint

Read-only inputs are copied and SHA256-hashed by verify.sh. Paths here are
relative to the workspace root; saved copies are under each run's inputs/.

* artifacts/routeb_gain_checkpoint_20260905/REPORT.md: the primary current
  route requires J<=1, with original P<28/5 and terminal Qterminal<12.
  It explicitly leaves source/FD/Float64 errors, prefix domains and extension
  open. This leaf changes no target, initial set or input family.
* examples/routeb_coupled_gain_bridge/{DERIVATION.md,GainBridge.lean,verify.sh}:
  N<=2877/200000 and H<=403089/500000 concern the two-component residual
  output e, not r0 or the full-state source Jacobian. Consequently sqrt(N)
  cannot be inserted as b0 and H cannot be inserted as g or k in (SG).
* examples/routeb_coupled_resolvent/{CoupledResolvent.lean,source_bounds.py}:
  acceleration_free_resolvent subtracts actual and same-state reference force
  balances with eta explicit. The source script forms (M0-M)*a0 using every
  one of the 13 (q,v,w) columns and combines q2+q3, v2+v3 correlations before
  norms. It checks r0 and its linearization vanish at the joint origin and
  gravity remainder is cubic. Smoothness and zero linearization suggest local
  small gains near the joint origin, but do not supply uniform ell on a tube
  containing the full original ball and ramp family through time 1. In
  particular the ramp is not fixed at w=0, and the nominal flow is coupled.
* The source audit's output/bounds-20260905T193103Z-725e99c7/source_bounds.json
  declares box_invariance_proved=false and physical_FK_FD_Float64_binding=false.
  Its static Q(r0) upper bound is about 754.868 before eta. This is neither a
  small incremental Lipschitz constant nor a closed prefix integral bound.
  It does not refute a tighter nominal-tube estimate or the actual target.
* examples/routeb_coupled_finite_gain/DERIVATION.md and its final direct-output
  receipt run-20260905T194943Z-9ad8ada4/results.json provide two state-output
  kernel-square gains, not the full-state L2 gain (G). The block output P
  controls q4,q5,v4,v5; it cannot certify every remote coordinate used in a
  source support. The reported old-path J~.0602 and integral Q(r)~.3612 are
  unenclosed single-path diagnostics and cannot choose certified b0 or k.

Thus a same-state L2 small-gain route is a valid CONDITIONAL continuation
strategy. The current checkpoint does not supply its numerical small-gain
premises. The main agent needs a uniform nominal nonlinear-force budget b0,
a compatible weighted incremental force bound ell and state gain g (or a
direct composite gain k), error eps, and every required domain/continuation
certificate. This leaf does not guess numbers or rerun source bounds.

## 7. Output and formal handoff

Under (C), the current bridge's rounded direct-output estimates give

    P(x(t)) <= (43/100 + (9/5)c)^2 <= (223/100)^2 < 28/5,
    Qterminal(x(1)) <= (13/20 + (14/5)c)^2 <= (69/20)^2 < 12.

The terminal statement presumes continuation to 1. The P bridge can be used
on pre-exit prefixes for its own boundary as described in Section 2. If useful,
the optional residual-output bridge also yields

    Ractual <= (3/25 + (403089/500000)c)^2.

This expression need not be <=1/10 when c<1; that optional budget is not
required for the current direct-output target.

PrefixSmallGain.lean proves amplitude_bound, strict_margin,
prefix_scalar_gate, first_exit_value_excluded, sqrt_energy_gate,
compose_source_state_loop, forcing_amplitude_gate, forcing_energy_gate and
original_output_envelopes. The prefix topological proof, L2/matrix analysis,
source data, domain closure and physical implementation remain outside this
scalar formalization. No sorry, admit or new axiom is used. The Lean file
imports cached mathlib only, not sibling candidate modules. It explicitly
assumes each analytic inequality and proves its scalar consequences.

Reproduce in WSL with bash examples/routeb_prefix_small_gain/verify.sh from
the workspace root. The wrapper checks mathlib commit
0df444a360eaa60ab8c11dca51a86af692955474 and invokes installed Lean 4.33.1
directly against cached dependencies, with warnings treated as errors. Only
this directory is written. Every compile run retains its complete terminal
log, exact inputs, hashes, source snapshots, and any produced object file.
