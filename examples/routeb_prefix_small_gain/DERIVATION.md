# Conditional prefix small gain for the same-state RouteB defect

The topology extension compiled successfully in output/run-90JWgVCt:
Lean 4.33.1, compiler and wrapper exit codes both 0, nineteen theorem axiom
reports containing only propext, Classical.choice and Quot.sound. The actual
ContinuousOn first-hit and prefix bootstrap arguments are now formalized,
together with whole-interval small-gain and cell corollaries. This removes the
previous topology formalization gap; it does not discharge any source premise.
The source and complete log are retained there. Both earlier scalar runs remain
intact; no Lean attempt failed. Final report/history annotations postdate the
immutable compile snapshots, and the current Lean source matches the final run.

This leaf formalizes conditional topology and scalar mathematics. It supplies
no numerical nonlinear-source certificate, registry
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

## 1a. Per-cell integrated energy bootstrap (no Lipschitz premise)

Let t0<=t1, J:[t0,t1]->R continuous, J(t0)<=b, and F>=0. Assume the
strict cell gate

    Bcell := b+(t1-t0)F < cap.                             (CG)

Suppose on EVERY pre-exit prefix [t0,t] contained in J<cap,

    J(t)<=b+(t-t0)F.                                      (CP)

It suffices if the source estimate is valid under the weaker condition J<=cap;
the argument uses it only on strict pre-exit prefixes. Then

    J(t)<=b+(t-t0)F<=Bcell<cap, for every t in [t0,t1].     (CB)

Proof: F>=0 and t1>=t0 imply b<=Bcell<cap, so J(t0)<cap. If J ever
reaches or exceeds cap, continuity gives a first hitting time tau>t0. For
every u<tau, (CP) applies, so J(u)<=b+(u-t0)F<=Bcell<cap. Passing to
tau from below by continuity gives J(tau)<=b+(tau-t0)F<=Bcell<cap,
contradicting the hit. Therefore the whole cell stays below cap, and (CP)
can be applied at every t, including t1, to get (CB). A degenerate cell
t0=t1 is covered by J(t0)<=b<cap. Nonnegativity of J or b is not needed
for this abstract statement, though it holds for actual energy. The source
estimate need not hold at the proposed hit itself; continuity is assumed.

For the actual cumulative energy, sufficient analytic premises for (CP) are
absolute continuity and

    J(t)=J(t0)+int_t0^t delta' L delta,
    delta' L delta<=F a.e. on every pre-exit part,
    J(t0)<=b.

If delta' L delta<=Q(r), a uniform pre-exit cap Q(r)<=F suffices. F is
an energy-density upper bound, not a force amplitude; do not square it again.
The same argument permits an integrated estimate directly without a pointwise
F. For a continuous nondecreasing envelope A(t) with J(t)<=b+A(t)
on pre-exit prefixes, b+A(t1)<cap suffices (and ensures J(t0)<cap if
the initial value is bounded by b+A(t0)).

Finite induction over adjacent cells uses the established previous bound b_i,
an independently certified F_i(cap_i) on the hypothetical pre-exit region,
and b_i+h_i F_i(cap_i)<cap_i. The improved endpoint value is
b_{i+1}=b_i+h_i F_i(cap_i), or a certified outward rounding of it. No
small-gain Lipschitz constant is required. If the trial cap changes, its source
envelope F_i must be reevaluated, including after rounding. Failure of this
sufficient gate stops THIS induction and does not prove an actual violation.
The gate does not close any unrelated source-domain exit; Section 2 still
applies. It also cannot restart beyond an unclosed gap using only diagnostics.

For the current source audit, the state-response bounds use the entire history
[0,t], even when the induction step concerns only [t0,t1]. This is compatible
with the cell argument because cumulative energy J is nondecreasing: the
previous history obeys J(s)<=J(t0)<=b<cap, and a pre-exit current history
also obeys J(s)<cap. Thus the hypothetical cap is valid for the whole history
needed in variation of constants, without resetting J to zero at t0.

If the source audit bounds Q(r0)<=F0 while omitting eta, error can be
restored conservatively as follows. A pointwise ||eta||_Q<=e gives

    F=(sqrt(F0)+e)^2.

Alternatively, if int_cell eta'Qeta<=Ecell and h=t1-t0, the L2 triangle
inequality gives the total cell energy increment at most

    (sqrt(h F0)+sqrt(Ecell))^2.

Thus b+(sqrt(h F0)+sqrt(Ecell))^2<cap is sufficient on every prefix,
provided the error budget holds uniformly on those prefixes and F0>=0,
Ecell>=0. It is not legitimate to reuse a gate computed at eta=0 as a
physical-source error certificate.

## 1b. Formal ContinuousOn first-hit and bootstrap theorems

All five new declarations below compiled in the namespace RouteBPrefixSmallGain.
No global continuity, monotonicity, differentiability or nonnegativity of the
function is needed. The interval is closed and nonempty (a<=b); degenerate
intervals are included. The mathematical equations/source estimates used by
the corollaries are explicit hypotheses, not introduced axioms.

The exact requested interface is:

```lean
theorem continuousOn_prefix_bootstrap {f : ℝ → ℝ} {a b c cap : ℝ}
    (hab : a ≤ b) (hf : ContinuousOn f (Set.Icc a b))
    (hstart : f a < cap) (hmargin : c < cap)
    (hprefix : ∀ t ∈ Set.Icc a b,
      (∀ s ∈ Set.Icc a t, f s ≤ cap) → f t ≤ c) :
    ∀ t ∈ Set.Icc a b, f t < cap
```

continuousOn_exists_first_hit proves that a continuous function with
f(a)<cap<=f(b) has tau in (a,b], f(tau)=cap, and f(s)<cap for every
s in [a,tau). It first obtains a hit using intermediate_value_Icc, proves
that [a,b] intersect f^-1({cap}) is compact using ContinuousOn on the closed
interval, and takes its least element. If an earlier value were >=cap, IVT
would supply an earlier member of that level set, contradicting minimality.
Thus the first hitting time and its prehistory are proved inside Lean.

continuousOn_strict_prefix_bootstrap is stronger than the displayed
interface: hprefix is needed only under all f(s)<cap on [a,t]. To avoid
assuming the estimate at a hit of cap, it uses a first hit of the intermediate
level d=(c+cap)/2. The singleton prefix at a gives f(a)<=c<d. A purported
value >=cap implies a first hit of d. Its entire closed prefix lies below
cap, so hprefix applies at that hit and gives d<=c, contradicting c<d.
This fully formal proof handles the strict-prefix formulation in Section 1
without leaving a continuity-to-the-limit obligation to the caller.

The displayed closed-prefix theorem follows by weakening f(s)<cap to
f(s)<=cap. Its initial strictness and uniform strict margin are essential
parts of the stated sufficient conditions.

continuousOn_small_gain_bootstrap combines the strict-prefix theorem with
amplitude_bound and strict_margin. Its hypotheses include ContinuousOn X,
X(a)<1, b>=0, k<1, b+k<1 and the pre-exit inequality X(t)<=b+k X(t).
Its conclusion is X(t)<=b/(1-k) AND X(t)<1 on the entire interval.
It allows X(a)=0 as a special case and does not need the optional k>=0
restriction. An application X=sqrt(J) must still supply continuity of that
concrete function from integrability/regularity; no actual J is fabricated.

continuousOn_cell_bootstrap formalizes Section 1a directly. Given
ContinuousOn J on [t0,t1], J(t0)<=b, F>=0, the strict cell gate, and
J(t)<=b+(t-t0)F on every strict pre-exit prefix, it proves

    for every t in [t0,t1], J(t)<=b+(t-t0)F AND J(t)<cap.

The theorem calls the already compiled scalar cell gates and the new topology
theorem. It requires no first-hit or limiting inequality from the caller.
A source estimate valid on closed prefixes J<=cap supplies its strict-prefix
premise by weakening each strict inequality. All existing scalar gates and
the old receipt's numeric gate remain unchanged; no new numeric gates were
added for this extension.

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

Read-only source inputs and receipts are copied and SHA256-hashed by verify.sh.
The main audit's terminal log is also copied (logs are excluded from the
pre-run source hash manifest). Paths here are relative to the workspace root;
saved copies are under each run's inputs/.

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

The main agent's subsequent exact receipt is
examples/routeb_prefix_budget/output/run-20260905T200606Z-34dbb987/results.json,
read together with its audit.py and terminal.log, and saved by the second
compile wrapper. It supplies conditional scalar per-cell progress of 66/128
cells through t=33/64, with an outward J upper bound
21783090379/100000000000 = 0.21783090379. The last passed cell is index 65,
[65/128,33/64], with

    b    = 32377921103/250000000000,
    F    = 11304860080329/1000000000000,
    cap  = 108921350211/500000000000,
    b+F/128 = 5576471137013/25600000000000 < cap,
    b+F/128 <= 21783090379/100000000000 < 1.

supplied_last_cell_arithmetic checks these exact rational relations in Lean;
it assumes no actual trajectory bound and does not replay the source audit.
The new generic cell gates give the precise scalar/continuity interface for
using such receipts. The next unclosed cell is index 66, [33/64,67/128].
The recorded search stopped with a candidate above 1 and the reason "no tested
strict scalar enclosure below J=1"; this is not a proof that every possible
candidate fails. The whole-horizon hypothetical J<=1 source envelope is
99665469473184597/128000000000000 (about 778.63648), so that particular
global envelope also does not close. This latest time-dependent bound and
the earlier static box's 754.868 are different estimates on different assumed
supports, not conflicting claims about the actual energy.

The new audit explicitly sets eta_assumed_zero_for_this_analytic_audit=true,
actual_DH_J_proved=false, physical_FD_Float64_binding=false and
full_horizon_analytic_budget_closed=false. Its per-cell source bound is
cap-dependent and supplies no incremental Lipschitz estimate. It advances
the conditional analytic prefix, without discharging the small-gain constants,
full-horizon source budget or physical trajectory premises in this leaf.

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

PrefixSmallGain.lean proves continuousOn_exists_first_hit,
continuousOn_strict_prefix_bootstrap, continuousOn_prefix_bootstrap,
continuousOn_small_gain_bootstrap, continuousOn_cell_bootstrap,
amplitude_bound, strict_margin,
prefix_scalar_gate, first_exit_value_excluded, sqrt_energy_gate,
compose_source_state_loop, forcing_amplitude_gate, forcing_energy_gate,
cell_initial_strict_gate, cell_prefix_strict_gate, cell_integral_strict_gate,
cell_first_exit_excluded, supplied_last_cell_arithmetic and
original_output_envelopes. First-hit topology and the conditional interval
bootstraps are now formalized, as detailed in Section 1b. L2/matrix analysis,
source data, actual-domain closure and physical implementation remain outside
this formalization. No sorry, admit or new axiom is used. The Lean file
imports cached mathlib only, not sibling candidate modules. It explicitly
assumes each analytic inequality and proves its scalar and topological
consequences. Abstract topology does not establish that any particular source
estimate holds on the required prefixes or that an actual solution continues.

Reproduce in WSL with bash examples/routeb_prefix_small_gain/verify.sh from
the workspace root. The wrapper checks mathlib commit
0df444a360eaa60ab8c11dca51a86af692955474 and invokes installed Lean 4.33.1
directly against cached dependencies, with warnings treated as errors. Only
this directory is written. Every compile run retains its complete terminal
log, exact inputs, hashes, source snapshots, and any produced object file.
