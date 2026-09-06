# Coupled finite-horizon gain bridge

**Final scalar compilation passed**, Lean 4.33.1, both exit codes 0.
Import `GainBridge` from `output/run-HgoUb4qX` to use
`RouteBCoupledGainBridge.original_outputs_under_J_one` and the optional
`RouteBCoupledGainBridge.final_reference_cost_under_J_cap`.
The complete [terminal log](output/run-HgoUb4qX/terminal.log), source snapshots
and three hashed gain receipts are preserved. Only standard axioms were
reported. The nonlinear source-J and analytic convolution premises are not
discharged by this scalar compilation.

## PRIMARY result: original outputs directly from J<=1

The final direct-output receipt
`routeb_coupled_finite_gain/output/run-20260905T194943Z-9ad8ada4/results.json`
supplies, for the SAME full initial ball and ramp input family,

```
NP<=183423/1000000,       KP²<=3233741/1000000,
NT<=41957/100000,         KT²<=3907007/500000.
```

The direct L2-to-pointwise bridge derived below has NO Ddelta endpoint term.
The rational rounds sqrt(NP)<=43/100, KP<=9/5, sqrt(NT)<=13/20, KT<=14/5 give,
under the still-open nonlinear premise J<=1,

```
P_actual(t) <= (223/100)² = 4.9729 < 5.6,  all t in [0,1],
Qterminal_actual(1) <= (69/20)² = 11.9025 < 12.
```

The paired scalar Lean gate is **`original_outputs_under_J_one`**, combining
`original_domain_under_J_one` (apply at every t) and
`original_terminal_under_J_one`. It concludes P<28/5 and T<12; T here means the
terminal output, not the time parameter. These gates retain the respective analytic
bridge, nominal output bounds, squared kernel-gain bounds, and J<=1 as explicit
premises. `direct_original_output_arithmetic` checks all numerical rounds.
The main's kernel-square bounds use Frobenius norms as outward bounds for the
operator norms needed here; this is valid in this direction.

**Ractual<=.1 is NOT required for this primary route.** Its .04/.05 scalar
gates remain below as valid optional/historical intermediates, not changes to
the original target or input set. No source J<=1 proof or original-output proof
has been established by this scalar admission alone. The main's E1 stored-path
values Jdelta~.0602 and integral Q(r)~.3612 are below 1 but remain unenclosed
diagnostics, not proof of the uniform nonlinear premise or domain closure.

## Scope and notation

The main task supplies rigorous nominal-flow and kernel bounds N,H; none is
invented here. Its FINAL refined receipt supplies N<=2877/200000 and
H<=403089/500000. The first receipt and its conditional .04 gate are retained
as history below. The matrix coefficient seam is the previous exact coupled
reference audit. This leaf derives the analytic finite-horizon bridge and a
small scalar Lean admission interface. The convolution theorem itself is
derived below, not claimed Lean-verified. There is no nominal stability premise,
independent-sigma relaxation, matrix re-audit, trajectory or gain computation.

Use x=(q1,...,q6,v1,...,v6), with the exact A12,B12,E2x12,F2x1 already exported.
To avoid confusing damping D with the new direct channel, write

```
Gamma = [0_6x6; I_6],
Ddelta = [0,0,0,350003/3000000,0,0;
          0,0,0,0,200739/4000000,0],
W=diag(5/8,10/13),
Qrot=diag(3,8,95/7,165/7,45,90) with Qrot_23=Qrot_32=-5,
L=Qrot^-1.
```

Thus Q(r)=r' Qrot r, including the -10 r2*r3 term, and L is the full
anisotropic metric, not the inverse of its diagonal. The (2,3) determinant is
585/7>0 and all remaining diagonal entries are positive, so the symmetric
positive-definite square roots Qrot^(1/2),L^(1/2) exist and are inverse.

## Same initial state/input; two distinct reference outputs

The affine nominal acceleration a0(x,w) is the exact coefficient map from the
previous leaf. Define the defect along the ACTUAL path by

```
delta(t)=a_actual(t)-a0(x_actual(t),w(t)).
```

It is NOT a_actual minus a0 evaluated along the nominal flow. Let xbar solve

```
xbar'=A xbar+B w,       xbar(0)=x_actual(0),
x_actual'=A x_actual+B w+Gamma delta.
```

For the actual reference residual and the nominal-flow residual,

```
e_actual=E x_actual+F w+Ddelta delta,
ebar=E xbar+F w.
```

The pointwise nominal formula on the actual path is `e0(x_actual,w)=E x_actual+Fw`.
In general it is NOT ebar. Its difference from ebar is E(x_actual-xbar), which
must be retained. No bound on nominal-flow cost alone controls that difference.

Assume x_actual,xbar are absolutely continuous on [0,1], the equations hold
almost everywhere, w is integrable, and delta is square-integrable in L. All
matrices are constant finite real matrices. Then y=x_actual-xbar is absolutely
continuous, y(0)=0, y'=Ay+Gamma delta, and variation of constants gives

```
y(t)=int_0^t exp(A(t-s)) Gamma delta(s) ds,
e_actual(t)=ebar(t)+Ddelta delta(t)
               +int_0^t E exp(A(t-s)) Gamma delta(s) ds.
```

One proof multiplies y by exp(-At), applies the product rule almost everywhere,
and integrates. Matrix exponentials are bounded on this compact interval even
when A has an unstable mode. No infinite-horizon limit is taken.

For the ramp w=ct, the same formula can be written using A14/E2x14 and
Gamma14=[0;I;0;0]. The actual and nominal augmented states share w(0)=0 and c;
their last two differences are zero. Hence their augmented kernel equals
E12 exp(A12 t) Gamma12 exactly. Do not add an independent Fw disturbance to the
error bridge: the common input cancels, and its effect is already in ebar/N.
The nominal N must cover the full original 12-state initial ball of radius
3/20 and the same ramp family c²<=3, not selected initial directions.

## Finite-horizon L2 convolution estimate

Put z=L^(1/2)delta, so delta=Qrot^(1/2)z and

```
J=int_0^1 delta' L delta = ||z||_L2(0,1)^2,
K(t)=W^(1/2) E exp(At) Gamma Qrot^(1/2),
d0=||W^(1/2) Ddelta Qrot^(1/2)||_2,
Hstar=d0+int_0^1 ||K(t)||_2 dt.
```

Here matrix norms are induced Euclidean operator norms, not Frobenius norms
unless an explicit outward conversion is supplied. Extend z by zero outside
[0,1], and K by zero outside [0,1]. On [0,1] the error convolution equals this
whole-line convolution. Minkowski's integral inequality and translation
invariance give the finite-kernel Young bound

```
||K*z||_L2(0,1) <= ||K*z||_L2(R)
 <= (int_0^1 ||K(u)||_2 du) ||z||_L2(R).
```

The direct part has norm at most d0 sqrt(J). Applying the L2 triangle inequality
to the nominal output, direct part and convolution, if

```
int_0^1 ebar' W ebar <= N,     Hstar<=H,
```

with N,H>=0, yields the requested noncircular implication

```
sqrt(Ractual) <= sqrt(N)+H sqrt(J),
Ractual=int_0^1 e_actual' W e_actual
       <= (sqrt(N)+H sqrt(J))².
```

Delta may depend nonlinearly on the actual trajectory and input: the argument
is pathwise and requires no independence assumption. The triangle/Young bound
can be conservative, but does not replace an endogenous signal by an assumed
independent source when asserting the identity.

The main task separately supplies `M delta=r` and its anisotropic implication
`delta' L delta<=Q(r)`. Integrating gives `J<=int Q(r)`, with r built from the
SAME a0(x_actual,w) and actual path. Any finite outward bound Jbar on that
integral can replace J above. This leaf does not assume the old R<=.1 budget,
derive r again, or assert a source/Float64 bound on it.

## Admission and noncircular closure

A convenient all-rational interface is to certify n,h,j>=0 with
`N<=n²`, `H<=h`, `J<=j²`. Then

```
Ractual <= (n+h*j)².
```

The explicit scalar gate `(n+h*j)²<=1/10` admits the previously proposed
residualCost budget. The Lean file proves this implication with the bridge as
an explicit premise; it does not supply N,H,J or claim that the gate passes.
Directly accepting a J estimate that already assumes the desired R bound
would be circular.

### Initial outward gains: retained historical admission

The read-only receipt
`routeb_coupled_finite_gain/output/run-20260905T194015Z-49c2839c/results.json`
provides N<=9289/500000=.018578, H<=422703/500000=.845406, for the full initial
ball and ramp family. Its nominal-only P and terminal bounds are .183423 and
.419570 rounded upward; these are NOT actual-flow bounds.

With the still-open nonlinear premise `J<=1/25`, use the exact rational
envelopes n=137/1000 and j=1/5. The scalar calculation is

```
9289/500000 < (137/1000)²,
n+h*j = 765203/2500000 = .3060812,
Ractual <= (765203/2500000)² < 1/10.
```

`actual_reference_cost_under_J_cap` formalizes the last implication, retaining
the convolution bridge, supplied N,H bounds, and J<=1/25 as explicit premises.
`supplied_gain_arithmetic` checks the exact constants. The gain receipt is
snapshotted and hashed before compilation, but this scalar proof does not
recheck its interval matrix computation. The nonlinear J bound and any
first-exit closure remain OPEN; a postprocessed trajectory is not such a proof.

### FINAL refined gains: conditional J<=1/20 admission

The final read-only gain receipt is
`routeb_coupled_finite_gain/output/run-20260905T194507Z-c3a3498d/results.json`:

```
N <= 2877/200000 = .014385,
H <= 403089/500000 = .806178.
```

The main's gain computation uses an integrated Gram bound with an exact
positive-integer Sylvester check and cellwise 2x2 spectral-norm kernel bounds.
This leaf does not repeat that audit. The nominal-only P and terminal bounds
remain .183423 and .419570 rounded upward, not actual-flow guarantees.

For the still-unproved nonlinear premise J<=1/20, take

```
n=3/25, j=9/40,
2877/200000 < n²,       1/20 < j²,
n+(403089/500000)*j = 6027801/20000000 = .30139005,
Ractual <= (6027801/20000000)² < 1/10.
```

The current endpoint theorem is
`RouteBCoupledGainBridge.final_reference_cost_under_J_cap`; its hypotheses
explicitly include the analytic bridge, N,H bounds and J<=1/20.
`final_gain_arithmetic` checks the precise rational gate. J<=1/16 is not admitted
by the final supplied N,H scalar expression. The old J<=1/25 theorem remains
valid conditional arithmetic at the earlier constants, not the current target.

**No source J bound has been proved.** The main's E1 postprocessing of ONE
stored path reports delta'Ldelta integral about .0602, outside the sufficient
.05 gate, and Q(r) integral about .36121; actual cost is about .01002. These are
unenclosed diagnostics, not a rigorous refutation of J<=.05, the gain bridge,
or the original goal. They suggest that norm-only gain estimates may require
improvement or signed/correlated nonlinear terms; no such improvement is claimed
here. In particular, J<=.05 is neither asserted achieved nor presented as
currently supported by that trajectory diagnostic.

If the eventual source estimate instead has genuine feedback form
`J<=a²+b² Ractual`, with a,b>=0, then sqrt(J)<=a+b sqrt(Ractual). An independently
proved N<=n² and H<=h gives

```
(1-h*b) sqrt(Ractual) <= n+h*a.
```

Only if h*b<1 can this be closed as
`Ractual <= ((n+h*a)/(1-h*b))²`. The Lean file verifies the scalar amplitude
rearrangement under that strict loop condition. The estimate for J must still
be valid on the path/domain in question, not assumed from the conclusion.

## Parameter-specific direct channel

Qrot_45=0, so the two squared singular values of the direct channel are exactly

```
d4²=(5/8)*(350003/3000000)²*(165/7),
d5²=(10/13)*(200739/4000000)²*45.
```

The small Lean arithmetic check verifies 0<=d5²<=d4² and
`(447/1000)²<=d4²<=(56/125)²`. Hence d0=sqrt(d4²) lies in [.447,.448].
This is a sanity check on the direct contribution in H, not a bound on the
convolution tail. No arbitrary scalar inverse-mass replacement of Qrot is used.

## Primary all-time P and terminal output bridges

Let CP select q4,q5,v4,v5 with weights sqrt(3/2),sqrt(3/2),sqrt(4/5),sqrt(4/5),
so P(x)=||CP x||² and the ORIGINAL domain threshold is 5.6, not 45. Let CT use
weights sqrt(3),sqrt(3),sqrt(2),sqrt(2), so Qterminal(x)=||CT x||². Define

```
KC²=int_0^1 ||C exp(Au) Gamma Qrot^(1/2)||_2² du.
```

For each t<=1, Cauchy-Schwarz in the variation-of-constants integral yields
`||C y(t)||<=KC sqrt(J_t)`, where J_t=int_0^t delta'Ldelta<=J. Therefore

```
P(x_actual(t)) <= (sqrt(NP)+KP sqrt(J))²   for every t<=1,
Qterminal(x_actual(1)) <= (sqrt(NT)+KT sqrt(J))²,
```

provided P(xbar(t))<=NP for all t and Qterminal(xbar(1))<=NT. These are L2-to-
pointwise gains; do not substitute the L1 kernel constant H without proving
the needed comparison. There is no Ddelta feedthrough for these state outputs:
their velocity coordinates are components of x, whose difference is the
integral of delta. No endpoint pointwise bound on delta is required.

If source bounds hold only before exit, apply the same estimates to every
prefix [0,t]. A nominal total cost N and full-horizon kernel constants also
bound every prefix. Actual continuation through t=1 then requires a separate
strict first-exit closure for EVERY domain premise used in the source bound.
A P<5.6 output bound alone cannot certify an unrelated remote-coordinate box.

## Verification boundary

The only planned compilation is this directory's small scalar GainBridge.lean,
using cached Lean 4.33.1 and pinned mathlib commit
0df444a360eaa60ab8c11dca51a86af692955474. Each attempt saves sources before
compilation and logs both the Lean exit and wrapper exit synchronously.
The matrix coefficient audit and future rational N,H calculations remain with
their original sidecars (the supplied first N,H receipt is used only through
its explicit scalar constants, followed by the final refined receipt).
No original target theorem or .1 budget is admitted
without their premises and the scalar gate.
