# Prospective bounded LP screen, explicitly requested by the coordinator

This supersedes the signed acceleration-storage direction as the preferred
candidate. The earlier single exact calculation is retained, without rerun.

Use W0 = .5 v'Mv + Rpotential + (7/75)q4^2, and
V = sum_{j=1}^8 (1-t)^j [a_j W0 + sum_i p_ji q_i^2 + c_j c^2],
with all 64 coefficients nonnegative. One additional beta bounds the shared
initial ball. Minimize 9 beta/400 + 3 sum(a_j)/10000 + 3 sum(c_j).
No SDP, ODE solve, trajectory, sampled certificate claim, or installation.

ONE scipy.linprog call, HiGHS, 30-second limit, default presolve. Analytic
source only (eta=0), source mass/potential CSVs, exact reference coefficients
converted to floats. The frozen-Z=I scalar source cost is assembled with its
signed cross term intact. Positive powers only ensure terminal zero.

Predetermined collocation set: all 24 signed initial coordinate-ball axis
points with c=0; four initial mixed q2/v2 and q4/v4 points with c=+/-sqrt(3);
eight templates at each of t=1/4,1/2,3/4,1 (32 points); and both zero-state
ramp signs at t=0,1/4,1/2,3/4,1 (10 points). Total 70 points.
The noninitial templates are uniformly shrunk in q,v if necessary to fit
90 percent of all 97 published J<=1 support bounds and the block quadratic
domain. This is deterministic construction of static test points, not a
trajectory or adaptive search. c and w=tc are never shrunk.

All source evaluations, point coordinates, source cost, W0 and W0dot, LP
rows, returned coefficients, objective, solver status, and diagnostic residuals
will be saved. A successful status is only numerical candidate evidence.
If a finite candidate returns, scale its coefficients by 1+10^-5 and round
to a 10^-12 rational grid once, then report (do not hide) every residual.
No repeated solve, changing degree, adding points, or fitting to a new ODE.

The full-T=1 actual J<=1 goal stays open unless the uniform source scalar
inequality, original-domain first-exit/continuation, and eta gates are proved.
