# Full-time coupled gains and the original output route

These are exact rational enclosures of the declared coupled reference model,
with analytical matrix-norm arguments. They are not a Lean proof of a true-DH
flowpipe or of the nonlinear correction budget.

## Model and complete scope

The exact reference from `routeb_coupled_linear_reference` gives the augmented
14-state system y=(q1..q6,v1..v6,w,c), with w'=c and c'=0. Initially w=0,
the single full12 state norm is at most3/20, and c²<=3. Every t in [0,1] is
covered. The coupled nominal model has an unstable gravity mode; no infinite-
horizon stability assumption is made.

For the actual state with the SAME initial value and input, let
delta=a-a0(x,w), so x'=Ax+Bw+Gdelta. The proved mass-resolvent reduction supplies
delta' L delta<=Q(r), subject to its physical/source premises. Here Q=L^-1
has diagonal (3,8,95/7,165/7,45,90) and Q23=Q32=-5.

## Exact time enclosure

All matrix and error arithmetic uses integers/Fraction. A 10^-40 fixed grid
is used for intermediate matrix centers, with the induced-infinity rounding
error charged explicitly. A scaled degree-28 Taylor series gives exp(A/128);
the scaled norm is <=1/2 and the omitted series is bounded geometrically.
Every propagated center carries its operator error.

Within each of the128 complete closed time cells, a degree-12 Taylor
polynomial of C exp(A*t) covers all local times. Signed interval powers and
an explicit geometric matrix tail are added. These are interval cells, not
samples or quadrature nodes.

For nominal integrated residual cost, all initial/input Gram entries are
integrated by outward cell enclosures. The midpoint error is bounded in
symmetric operator norm by its maximum row sum. A strictly positive integer
Sylvester/Bareiss certificate proves a rational eigenvalue upper bound for
the initial12 block. The initial ball and the single constant c are bounded
AFTER integration, preserving their temporal correlation.

For the dynamic residual correction kernel, the2x2 weighted spectral formula
is evaluated with rational outward square roots, retaining Q's signed cross
term. Frobenius bounds suffice for the four-component state-output kernels.

## Residual-cost route (optional)

The final audit gives

    N=2877/200000=0.014385,
    H=403089/500000=0.806178.

N bounds nominal integrated residual cost over the full initial/input class.
H is direct feedthrough norm plus the finite-horizon L1 kernel norm. Variation
of constants and the L2 convolution inequality imply

    sqrt(R_actual) <= sqrt(N)+H sqrt(J),
    J=int_0^1 delta' L delta <= int_0^1 Q(r).

J<=1/20 is a sufficient (unproved) condition for R_actual<=1/10. It is not a
required part of the original target. In particular N is never substituted
for the cost of e0 along the actual trajectory: the kernel accounts for the
actual-minus-nominal state correction explicitly.

## Direct original-output route: J<=1 suffices

State outputs have no instantaneous Ddelta term: their correction is the
convolution of the state transition with delta. Cauchy-Schwarz gives

    P_actual(t) <= (sqrt(NP)+KP sqrt(J))²,  every t<=1,
    Qterminal_actual(1) <= (sqrt(NT)+KT sqrt(J))²,

where the final rational caps are

    NP=183423/1000000,  NT=41957/100000,
    KP²=3233741/1000000, KT²=3907007/500000.

Concretely the squared gain for either weighted state-output matrix C is
bounded by the integral of `trace(C exp(As) G Q G' exp(As)' C')` over s in
[0,1]. This is the squared Frobenius kernel bound on L-weighted inputs;
the metric Q and its signed (2,3) cross term are included. The nominal-output
caps and these kernel bounds are distinct from the residual-cost N,H pair.

The kernel-square integrals cover the whole horizon, hence also every prefix.
Use sqrt(NP)<=43/100, KP<=9/5, sqrt(NT)<=13/20, KT<=14/5. If J<=1 then

    P_actual(t) <= (223/100)²=4.9729 <28/5,
    Qterminal_actual(1) <= (69/20)²=11.9025 <12.

This bypasses only the previously selected intermediary R<=.1. It does not
weaken or change the original initial ball, ramp family, time horizon, domain
quantity or terminal quantity. The actual nonlinear J<=1 and all physical
source/regularity/domain premises remain OPEN. A block output bound alone
cannot justify a separate remote-state support used to bound r.

## Diagnostic and evidence separation

One previously retained path was postprocessed with analytic Fourier forces
in Float64; no new trajectory was generated. Its un-enclosed trapezoid values
were J_delta about.06020, integral Q(r) about.36121, actual residual cost about
.01002 and same-state e0 cost about.01508. This explains why the very small
residual-cost gate may be too restrictive and motivates direct outputs.
It proves neither J<=1 nor a violation of any bound, and it is not bitwise
Julia-FD verification. Only exact-rational results enter the gain gates.

Three successful immutable audit runs preserve, respectively, the initial
Frobenius estimate, improved integrated/spectral estimate, and direct-output
gains. Final source-bound results are in
`output/run-20260905T194943Z-9ad8ada4/results.json`. The companion bridge states
the variation-of-constants hypotheses and compiles only its scalar gates in
Lean; the matrix/time enclosure is not silently promoted to the registry.
