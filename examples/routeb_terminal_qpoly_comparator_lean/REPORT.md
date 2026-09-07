# F4 report

Status: `PASS_CONDITIONAL_ARITHMETIC_ONLY`

The compiled leaf proves an exact direct qpoly comparator.  Its only terminal
input is the semantic inequality
`qpoly(1) <= (3/2)L + 3*g*D`; monotonicity in `D`, positivity of `g`, and the
exact rational margin prove strict `< 12` whenever `D <= 4483/2000`.

The equality threshold is `D_max = (4-L/2)/g`, with
`D_gate < D_max`.  This is an exact threshold calculation, not a decimal
floating-point comparison.

The old `p <= 28/5` route is not used.  It is insufficient because the sharp
coefficient relation only gives `qpoly <= (5/2)p <= 14`.

The real deployed-DH proof of the premise `D <= D_gate`, including full
trajectory coverage and FD/rounding/solve semantics, remains **OPEN**.  Thus
this artifact is not a deployed-DH theorem and must not be promoted as one.
