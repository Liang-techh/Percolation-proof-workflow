# Correlation-preserving source bounds and a rejected relaxation

These are exact rational audits and analytical error enclosures, not Lean
kernel theorems or a physical DH trajectory certificate. The original M4
claim and total residual integral <=0.1 remain open.

## 1. Actual coefficient bounds on a candidate support

The candidate pre-exit support is |q4|,|q5|<=2/5 and

    (|v1|,|v2|,|v2+v3|,|v4|,|v5|,|v6|) <= (3/5,5/2,2,4/5,4/5,2/5).

The entire original full12 initial ball fits this support; we do not replace
that ball with block-only or zero-remote initial data. Neither invariance of
this support nor any remote/joint-limit continuation is proved.

`bounds.py` substitutes v3=V-v2 into the exact source T4,T5 coefficient
payload and combines equal monomials before taking absolute values. It then
groups Fourier modes by the remote frequencies and expands only the block
phase around q4=q5=0. For a grouped coefficient c, the variation bound uses
|exp(i theta)-1|<=min(2,|theta|) and |c|<=|Re c|+|Im c|. All ledger arithmetic
is rational; no remote angle is fixed and no sampled trig extrema are used.

The compact mass formulas yield bounds on sigma=p_B-Mref*v_B. The complete
results, excluding implementation defects, are:

| Quantity | Joint 4 | Joint 5 |
|---|---:|---:|
| abs(sigma) | 11730139/150000000 | 2361653/20000000 |
| abs(T) after preserving V | 52039753/600000000 | 20197663/400000000 |
| abs(T-G) | 56983993/600000000 | 40798663/400000000 |
| Naive abs(T) before preserving V | 527021987/2400000000 | 172514789/1200000000 |

Numerically the T bounds decrease from about (0.21959,0.14376) to
(0.08673,0.05049). These decimals are display only. The bounds concern the
encoded analytic coefficients; ideal-FD/Float64 differences and computed G0
are not silently set to zero in a physical application.

## 2. Why arbitrary bounded sigma is not an adequate abstraction

For the actual joint-5 constants m=200739/4000000, k=1/2, d=13/20, consider
the *relaxed* filter

    q'=(p-sigma)/m,
    p'=-k*q-(d/m)*p+(d/m)*sigma,

with initial q=p=sigma=0 and w=h=0. Take S=59/500, strictly less than the
source's conditional sigma5 cap. Prescribe continuous piecewise-linear sigma:

- on [0,1/100], ramp from 0 to -S;
- on [1/100,99/100], hold -S;
- on [99/100,1], ramp from -S to +S.

The zero initial physical velocity is respected. Both q and p solve the
first-order filter with continuous input, so this is not a spurious endpoint
jump. The other block coordinates may be zero in this *auxiliary* model.

`relaxation_counterexample.py` encloses the three exact linear propagators
using rational Taylor polynomials. For ||B||_infinity<=1/2, the omitted tail
after degree n is at most 2||B||^(n+1)/(n+1)!. Under squaring, an operator error
epsilon grows by at most 2||P||epsilon+epsilon^2. Matrix entries are rounded
on a rational 10^-40 grid and their exact induced-norm rounding error is
charged explicitly. Scalar error bounds are rounded upward. Multiplication
by the approximate state propagates both matrix and state errors. Known
sigma and constant coordinates are reset to their exact prescribed values.

No floating-point value participates in any enclosure or acceptance check.
The resulting exact interval assertions are

    0 < q(1) < 1/10,   -5 < v(1) < -4.

Therefore terminal 3q²+2v²>32>12, and domain (3/2)q²+(4/5)v²>64/5>28/5.
This rejects an unconditional output theorem for the relaxed filter with only
these amplitude caps. It also cannot establish the proposed smaller block
velocity support by an amplitude-only bootstrap.

**It does not refute the actual DH theorem.** The artificial sigma need not
equal the actual mass-coupling momentum along any full-six-axis trajectory,
and the trajectory leaves the candidate support used for the source bounds.
The conclusion is that those bounds alone, after discarding physical
correlation, are insufficient to close the bootstrap; not that the source
bounds or target are false.

## 3. Consequence for the proof frontier

Keep p/sigma and remote-state dynamic correlations, or prove a sufficiently
tight derivative/cumulative estimate. The coupled momentum equations, source
column cancellation and the earlier actual-force budget remain useful.
Do not continue searching for a positive amplitude-only filter certificate at
the displayed caps: the relaxed model itself violates the desired outputs.
Do not infer a bound on sigma' from a bound on sigma.

The two failed enclosure-program attempts and their exact source snapshots
are retained in `history/`. The first failed while serializing an oversized
rational; the second rejected a guessed readable q interval. The repaired
program changed neither dynamics nor the input. This is not a Lean proof of
the matrix-exponential enclosure theorem; comparator and registry admission
are intentionally not claimed.
