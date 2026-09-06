# Prospective SECOND bounded LP screen, explicitly requested by the coordinator

The first LP and its plan/code remain immutable in
output/lp-20260905T210233Z-e9203653. It has initial objective about .33234,
all c_j=0 and a 7.07175e-8 violation; it is not feasible at 1e-8. Exact
ramp/initial obstructions are in output/post-20260905T210708Z-19f7d8ba.

Use W0 = .5 v'Mv + Rpotential + (7/75)q4^2, and
V = sum_{j=1}^8 (1-t)^j [a_j W0 + sum_i p_ji q_i^2 + c_j c^2],
with all 64 coefficients nonnegative. One additional beta bounds the shared
initial ball. Minimize 9 beta/400 + 3 sum(a_j)/10000 + 3 sum(c_j).
No SDP, ODE solve, trajectory, sampled certificate claim, or installation.

ONE additional scipy.linprog call, HiGHS, 30-second limit, default presolve,
primal and dual feasibility tolerances 1e-10. Analytic
source only (eta=0), source mass/potential CSVs, exact reference coefficients
converted to floats. The frozen-Z=I scalar source cost is assembled with its
signed cross term intact. Positive powers only ensure terminal zero.

Predetermined collocation set: all 24 signed initial coordinate-ball axis
points with c=0; four initial mixed q2/v2 and q4/v4 points with c=+/-sqrt(3);
eight templates at each of t=1/4,1/2,3/4,1 (32 points); and both zero-state
ramp signs at t=0,1/4,1/2,3/4,1 (10 points). Total 70 points.
Add ten prospectively fixed rows: q=0,v=G/1000,c=1 at t=1/4,1/2,3/4;
q=0,v=e_i/1000,c=1 at t=1/2 for i=1..6; and t=0,q2=1/100,
v2=3/200,c=0. Total 80 points. The t=1/2 G/1000 row imports the exact
source witness's cost, W0 and W0dot, then converts to floats for the LP.
The noninitial templates are uniformly shrunk in q,v if necessary to fit
90 percent of all 97 published J<=1 support bounds and the block quadratic
domain. This is deterministic construction of static test points, not a
trajectory or adaptive search. c and w=tc are never shrunk.

All source evaluations, point coordinates, source cost, W0 and W0dot, LP
rows, returned coefficients, objective, solver status, and diagnostic residuals
will be saved. A successful status is only numerical candidate evidence.
If a finite candidate returns, round to a 10^-12 rational grid once without
inflation. Compute all beta requirements with Fraction and replace rounded
beta by max(rounded beta, exact required beta). Report exact nonnegativity,
initial-bound slacks, and all numerical dissipation residuals. There will be
no third solve, degree change, adaptive points, or fitting to a new ODE.

The full-T=1 actual J<=1 goal stays open unless the uniform source scalar
inequality, original-domain first-exit/continuation, and eta gates are proved.
