# One exact initial-state obstruction, planned before evaluation

Inspect only the second LP's immutable coefficients, exact M0/H0/K/D and
source Fourier CSVs. No third LP, time sweep, trajectory or broad test.

The selected coefficient vector has no q6 position storage. Test the single
predeclared allowed initial state q6=1/100, v6=-1/400, other coordinates zero,
c=w=eta=0, t=0. Check by exact grouping that M66 on this source line is the
constant M0_66 and the potential is U0. Then compute W0 and W0dot using the
actual-energy cancellation identity, and the candidate Vdot exactly.

A strictly positive Vdot at this initial state refutes uniform zero-supply
dissipation since delta'Ldelta>=0. It does not refute the physical target,
the entire storage family, or a positive-supply alternative. The physical
implementation binding and the analytic derivative theorem are separate.

Also record the precise local 2x2 quadratic obstruction: zero q6 diagonal
but nonzero q6-v6 off-diagonal. This is a necessary origin gate, not a
floating eigenvalue test.
