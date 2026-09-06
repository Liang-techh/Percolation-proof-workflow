# Coupled acceleration-free residual reduction

This continues the original full-six-axis target after rejecting the independent
bounded-sigma filter abstraction. All coordinates and the same physical state
are retained. No original assumptions or output thresholds are changed.

## Exact identity and interpretation

Choose the exact regularized reference M0=M(0), H0=Hessian U(0), and

    drive=-Kq-Dv+Gw,
    M0*a0+H0*q=drive,
    M(q)*a+C+G=drive+eta.

Here eta is the single combined source/FD/Float64/solve defect for the chosen
analytic mass and forces. The reference a0 is evaluated at the CURRENT
actual (q,v,w), not on a separately evolved nominal solution. Subtraction gives

    r=(M0-M(q))*a0+H0*q-G-C+eta,
    M(q)*(a-a0)=r.

Thus r contains no unknown actual acceleration a. Its dependence on the state,
mass, gravity and Coriolis is explicit; no independently selectable sigma or
remote-acceleration input has been introduced.

`acceleration_free_resolvent` and the residual energy identity are proved in
Lean. All force-balance/source meanings are explicit hypotheses rather than
an assertion that the Float64 backslash solve is exact.

## Six-dimensional correction bound

Let delta=a-a0 and E=delta' M delta=r.delta. The previously compiled rotational
dual bound gives, with its DH-axis/mass hypotheses still to be instantiated,

    delta' L delta <= E <= Q(r),

where L=Q^-1 is the full anisotropic six-dimensional metric. In particular,
delta4²<=(165/7)E and delta5²<=45E. With the ACTUAL reference masses and
residualCost weights, Lean proves

    residualCost(m44*delta4,m55*delta5) <= (3/10) Q(r).

Writing e0=Mref*a0_B+K_Bq_B+D_Bv_B-G_Bw gives the exact e=e0+Mref*delta_B
and the convenient, non-sharp conditional inequality

    residualCost(e) <= (3/2) residualCost(e0)+(9/10) Q(r).

This is not a cumulative bound. In particular the old nominal-trajectory
linearized screen (~0.014) CANNOT be substituted for the integral of
residualCost(e0) along the actual trajectory. Both e0 and r share that actual
state. The coupled state equation is x'=A12*x+B12*w+(0,delta), with
delta' L delta<=Q(r(x,w)), not two unrelated state histories.

## Exact coefficient reference

The companion `routeb_coupled_linear_reference` audits rational M0,H0,M0^-1,
A12,B12 and the complete 2x13 e0 map. Both e0 rows depend on all 13 coordinates
(q,v,w); all 78 cost cross terms are retained. The stiffness has the exact
negative direction e2'(K+H0)e2=-1709689/400000. The full coupled nominal model
must not be treated as the stable decoupled momentum filter.

## Source envelope and what it did not achieve

`source_bounds.py` constructs the acceleration-free mass coefficients from
the actual Fourier M and exact nominal acceleration map. Before any norm,
it changes coordinates to (q1,q2,q2+q3,q4,q5,q6) and velocities
(v1,v2,v2+v3,v4,v5,v6). Christoffel velocity monomials are likewise combined
before bounding. The constant and first derivatives of the analytic r at
(q,v,w)=0 vanish; the G-H0q remainder is cubic because the potential has real
Fourier coefficients. These are exact coefficient identities, not a proof of
the FD/Float64 Jacobian or execution errors.

The diagnostic candidate box has position radii (.4,1,1.2,.4,.4,.4), velocity
radii (.6,2.5,2,.8,.8,.4), and |w|<=7/4 (which contains the entire original
ramp range). It covers the original initial ball but is not proved invariant.
Centered Fourier inequalities preserve cos cancellation and use global
|cos(theta)-1|<=min(2,theta²/2), |sin(theta)|<=min(1,|theta|) and
|sin(theta)-theta|<=|theta|³/6. All arithmetic in the ledger is rational.

Even so, componentwise bounding on this whole box yields a Q(r) bound about
754.868 before eta. This is much too loose for the current budget argument.
**It is not a counterexample or a proof that the coupled route is impossible.**
It shows that discarding time/state correlations into a static component box
does not finish the certificate with this estimate. Next work needs a tighter
time-dependent correlated state enclosure, a directional residual estimate,
or a coupled dissipation certificate; merely inserting this box number into
the compiled conditional inequality does not close M4.

## Evidence boundary

The Lean module compiled once successfully with pinned Lean 4.33.1 and only
standard axioms; source snapshots and complete synchronous exit logs are in
`output/run-HTi4uZSF`. The source envelope audit and its input snapshots are in
`output/bounds-20260905T193103Z-725e99c7`. No full regression, nominal simulation,
large solver, browser, external-project edit or toolchain rebuild was run.
Physical source binding, actual integrated budgets, complete domain/trajectory
coverage, comparator and registry admission remain open.
