# Momentum filter: exact storage, conditional bounds, and failed cap closure

## Outcome

The momentum reformulation is exact and stable, and does **not** need a
sigma-derivative hypothesis. But the actual supplied amplitude caps do not
close the proposed block box or terminal target. This is not merely a loose
upper-bound issue: the main task has enclosed a continuous cap-admissible
relaxed-filter counterexample. It is **not an actual DH path**, and does not
refute the original theorem. The missing information is the coupled dependence
of momentum p and sigma on the same six-axis motion.

Only this new folder was written. No Lean compilation, trajectory integration,
download, target edit, state edit, or registry change was performed. Run
`python -B examples/routeb_momentum_filter/verify.py` from the workspace to
reproduce the exact-rational interval audit. It preserves a new source snapshot,
pre-run manifest, results and a synchronous terminal log with exit trailer.
See ATTEMPT_HISTORY.md for attempt history and discovery-command errors.

## Exact state change; no sigma derivative

For each block axis assume the same momentum identity and balance as the
inertial sidecar:

```
p=m v+sigma,       q'=v,
p'=-k q-d v+g w+h,       h=T-G+g0+eta.
```

Here p is momentum, not the polynomial domain quantity P below. Substitution
alone gives the requested stable filter

```
q'=(p-sigma)/m,
p'=-k q-(d/m)p+(d/m)sigma+g w+h.
```

Use absolutely continuous q,p, measurable locally integrable sigma,h,w, and
the equations almost everywhere; v=(p-sigma)/m almost everywhere. For pointwise
endpoint velocity statements one additionally uses this algebraic relation
at that endpoint, e.g. continuous sigma and interpreted physical velocity.
No bound or existence assertion for sigma' is used in the filter estimates.
The actual parameters, including the nominal regularizer, are

| Axis | m | k | d | g |
|---|---|---|---|---|
| 4 | 350003/3000000 | 3/5 | 4/5 | 1/5 |
| 5 | 200739/4000000 | 1/2 | 13/20 | 1/10 |

## Parameter-specific rational quadratic storage

Put r=p/m, a=k/m, b=d/m, u=g w+h, and x=(q,r). The homogeneous matrix is
`A=[[0,1],[-a,-b]]`. Both k,d,m are positive, and d²-4mk>0; the two decay rates
are approximately (0.85714408,5.99994000) and (0.82131111,12.13083073).

Define V=x' L x using the following exact matrices:

```
L4 = [ 5350003/4800000          350003/3600000;
       350003/3600000          752507500009/8640000000000 ],
L5 = [ 5580739/5200000          200739/4000000;
       200739/4000000          441774146121/10400000000000 ].
```

The audit checks positive leading entry and determinant, and exactly checks
`A' L+L A=-I` for both actual axes. In terms of their actual m,k,d, let

```
Lq = -(k+m)/(d*m) sigma + u/k,
Lr = sigma/m + (k+m)/(k*d) u.
```

The concrete input coefficients are also rationally checked. Along the filter,

```
V' = -q²-r²+q Lq+r Lr,
V' + (q²+r²)/2 - (Lq²+Lr²)/2
   = -((q-Lq)²+(r-Lr)²)/2 <= 0.
```

The first identity preserves sigma/u correlations; the second is an optional
dissipation inequality. Summing axes is immediate. This storage controls q,r,
not directly v: replacing r by v without the sigma feedthrough would be wrong.
We use sharper finite-time impulse estimates below rather than inflate this
storage comparison into a large all-time induced gain.

## T=1 impulse formulas and full initial ball

Let alpha<beta be the positive roots of m lambda²-d lambda+k=0. Define

```
B(t)=(exp(-alpha*t)-exp(-beta*t))/(beta-alpha),
A(t)=(beta*exp(-alpha*t)-alpha*exp(-beta*t))/(beta-alpha).
```

Then A=B'+bB and A'=-aB. Variation of constants, with the *actual* initial
velocity v0 and p0=m v0+sigma0, gives

```
q(t)=A(t)q0+B(t)v0+B(t)sigma0/m
       -(B' * sigma)(t)/m+(B * (g w+h))(t)/m,
v(t)=-a B(t)q0+B'(t)v0+B'(t)sigma0/m
       -(B'' * sigma)(t)/m+(B' * (g w+h))(t)/m-sigma(t)/m.
```

The second formula follows from the r-state solution and v=r-sigma/m, **not**
by differentiating sigma. `*` denotes causal convolution. It explicitly shows
both the initial sigma and terminal feedthrough; they cannot silently be
discarded or treated as independent physical source freedoms.

Write I0=int_0^t B, I1=int_0^t |B'|, I2=int_0^t |B''| and
J0=int_0^t (t-s)B(s) ds. B is nonnegative. It has a unique peak at
tau=log(beta/alpha)/(beta-alpha), and B' has its minimum at 2tau. Thus

```
I0=(1-A)/a,   J0=(t-B-b I0)/a,
I1=B(t)                         if t<=tau,
I1=2 B(tau)-B(t)                if t>=tau,
I2=1-B'(t)                      if t<=2tau,
I2=1+B'(t)-2 B'(2tau)           if t>=2tau.
```

No quadrature or time-stepping approximation is used. Assume |sigma0|<=S0,
|sigma(t)|<=S, |h(t)|<=H and w=ct with c²<=3. The nonnegative input envelopes
for q,v have coefficients `(S0,S,H,|c|)`:

```
bq=(|B| S0+I1 S+I0 H+g J0 |c|)/m,
bv=(|B'| S0+(1+I2) S+I1 H+g I0 |c|)/m.
```

At t=1, the following displayed coefficients are rounded UP; the JSON retains
the full outward rational endpoints:

| Axis/output | S0 | S | H | abs(c) |
|---|---:|---:|---:|---:|
| 4/q | .703159 | 1.362612 | .842186 | .081406 |
| 4/v | .581461 | 17.841472 | 1.362612 | .168438 |
| 5/q | .774976 | 1.926778 | 1.056407 | .054889 |
| 5/v | .636389 | 41.041224 | 1.926778 | .105641 |

The full initial set is `sum_{i=1}^6(q_i(0)^2+v_i(0)^2)<=9/400`. It implies a
single four-dimensional block ball of radius 3/20, not four independent balls.
The estimates retain its joint Euclidean norm. For W=diag(wq,wv) on each axis,
F_i=[[A,B],[-aB,B']], and lambda=max_i lambda_max(F_i' W F_i),

```
sqrt(sum_i [wq q_i(t)²+wv v_i(t)²])
 <= (3/20) sqrt(lambda)+sqrt(sum_i [wq bq_i²+wv bv_i²]).
```

All twelve initial coordinates remain allowed. Their effects on sigma0 are
relaxed to S0, conservatively; we do not set the remote entries to zero for an
upper bound. The separate individual-coordinate estimates use the corresponding
row norm times 3/20 and need not be simultaneously attained.

## Actual supplied caps: quantitative failure of box closure

Read from `routeb_momentum_source_bounds/bounds.json`:

```
S=(11730139/150000000,2361653/20000000),
H=(56983993/600000000,40798663/400000000),
```

where H excludes eta. This evaluation sets eta=0, an explicit simplifying
assumption, NOT an implementation-error certificate. For nonzero eta caps,
replace H_i by H_i+E_i. We use S0=S; improved source initial bounds can replace
S0 without changing the formulas, but do not remove the terminal feedthrough.

Source caps hold only before exit from the proposed box
`|q4|,|q5|<=.4`, `( |v1|,|v2|,|v2+v3|,|v4|,|v5|,|v6| )`
`<=(.6,2.5,2,.8,.8,.4)`, with unrestricted remote angles. This filter supplies
no remote-coordinate invariance argument. Its computed upper bounds are:

| Quantity | Rigorous upper bound, rounded up |
|---|---:|
| P(t)=(3/2)(q4²+q5²)+(4/5)(v4²+v5²), all 0<=t<=1 | 27.011 |
| Qterminal=3(q4²+q5²)+2(v4²+v5²), t=1 | 66.961 |
| all-time abs(q4), abs(v4) | .458623, 1.926693 |
| all-time abs(q5), abs(v5) | .593907, 5.360083 |

Therefore the candidate block box is **not self-consistently certified**.
The original domain target is **P<5.6 only**, and the terminal target is
Qterminal<12. Neither is certified at these caps. Since the caps are only
pre-exit, these estimates also do not establish their continued validity.
The earlier P<45 comparison was unrelated to the original domain target and
is withdrawn. Preserved run JSON files retain `certifies_P_lt_45` solely as
obsolete historical output; it is not a target certificate. That field has
been removed from the current audit script without another audit run.

For context, the same calculation gives the following conditional terminal
bounds (always S0=S, eta=0, full initial ball, c²<=3):

| Hypothetical S4,S5 | Hypothetical H4,H5 | P all-time upper | Qterminal upper |
|---|---|---:|---:|
| 0,0 | 0,0 | .232 | .530 |
| .01,.01 | .05,.05 | .932 | 2.226 |
| .03,.02 | .10,.10 | 2.494 | 6.046 |
| .05,.04 | .25,.25 | 7.507 | 18.310 |

These are filter-cap implications, not claimed actual source bounds. Failure
of an upper estimate alone would not prove non-feasibility.

## Genuine cap-only obstruction; keep the source correlation

Our interval audit also evaluates a limiting relaxed input: sigma(0)=0,
sigma=S on (0,1), then sigma(1)=-S, with zero physical initial q,v and h=w=0.
Its endpoint is `q=-S B(1)/m`, `v=S(2-B'(1))/m`. Continuous transition inputs
converge to this endpoint by the explicit convolution formula. At the actual
S caps the limiting magnitudes are about
`(|q4|,|v4|)=(.054988,1.386047)` and
`(|q5|,|v5|)=(.091512,4.781065)`; the combined terminal quantity exceeds 49.59.
This limit is not presented as a directly audited finite-ramp trajectory.
It has sigma0=0, so tightening only the initial sigma cap does not fix it.

For an amplitude-only class to guarantee |v_i(1)|<=4/5, this family already
imposes the necessary (not sufficient) gate

```
S_i <= (4/5) m_i/(2-B_i'(1)),
```

whose values are approximately .04513610 and .01975839. The actual caps exceed
both. No formal Lean claim is made for this analytical limiting argument.

More decisively, the main task's separately saved
`routeb_momentum_source_bounds/relaxation_counterexample.json` records a
continuous piecewise-affine axis-5 input with S=59/500 below the source cap,
zero q,p,sigma initially, h=w=0: ramp 0 to -S on [0,.01], hold until .99,
then ramp to +S at 1. Its rational Taylor/remainder enclosure gives
`0<q5(1)<.1`, `-5<v5(1)<-4`, hence Qterminal>32 and P(1)>64/5.
We inspected this receipt; its finite-ramp computation belongs to the main
task and was not rerun or independently duplicated here. It disproves the
desired terminal and velocity-box implications for the arbitrary bounded-sigma
filter class, including the original P<5.6 target, and **not any original DH theorem**.

The next premise must retain information such as the actual identity
sigma=M_BD v_D+(M_BB-R)v_B jointly with p=M_B* v, a coupled reachable set in
(p,sigma), or controlled variation/derivative budget for sigma. These are
alternative ways to retain temporal structure; none is established here.
Stability of the filter alone cannot restore correlation discarded at its
input. No further positive-certificate search is warranted for these caps.

## Exact computation boundary

The audit uses Fraction arithmetic with outward interval rounding on a 10^-24
grid. Square roots use integer square-root enclosures. For exp(-x), x in [0,32],
odd/even Taylor sums of orders 25/24 bracket exp(-x/32), then five outward
squarings restore exp(-x). Peak times are rational sign-bracketed. The complete
interval [0,1] is covered by 128 closed interval cells, not merely sampled;
cumulative impulse integrals are monotone and evaluated at each right endpoint.
The 2x2 operator bound uses its exact eigenvalue formula with outward roots.

JSON results are authoritative rational enclosures; decimal displays are only
readable summaries. This is executable exact arithmetic plus the derivation
above, not a Lean-verified reachability theorem or Float64 solver guarantee.
The previous total residualCost integral <=.1 is neither used nor proved.
