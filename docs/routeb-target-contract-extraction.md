# Route-B target contract: source extraction, not a theorem

Read-only source inspection on 2026-09-05; no simulations or regressions run.
The target root is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized`.

## Concrete definitions recovered

`routeB_dense_Mq/routeB_export_traj.jl` declares `T=1`, `R_init=0.15`,
`eta_star=5.6`, `pw=[1.5,0.8]` at lines 40-46. Lines 139-148 sample a
**12-dimensional** Euclidean ball, not a ball in only the controlled block:

    X0 = { (q,v) : sum_i q_i^2 + sum_i v_i^2 <= (3/20)^2 }

with the declared joint-limit filter. The limits are q1,q2,q4,q5 in [-pi,pi],
q3 in [-5pi/6,5pi/6], q6 in [-2pi,2pi]. This small initial ball lies inside
these limits; retaining all 12 coordinates matters for subsequent dynamics.

The state-region quantity, also declared verbatim in
`routeB_certificate_manifest.toml`, is

    p45(q,v) = (3/2)*(q4^2+q5^2) + (4/5)*(v4^2+v5^2).

The full Monte-Carlo disturbance group uses `w(t)=c*t`, `|c|<=sqrt(3)`.
The manifest records precisely that ramp family. The new `EnergyTube.lean`
uses the equivalent real premise `c^2<=3`. This matches that family but does
not automatically prove any claim elsewhere quantified over arbitrary
measurable inputs with an integral budget.

The dynamics source evaluates

    tau = -Kp*q - (Kd+b_fr)*v + G0_ref + (gw_coef*I_val)*w
    a = Mq \ (tau-Cdq-Gq)

with regularizer 1e-6 and central-difference step 1e-5. Here the implementation
uses Float64 evaluation. The exporter advances a fixed 0.005-step second-order
position / first-order velocity update, holding w at the step's left endpoint.
These sampled trajectories are not exact continuous ODE solutions or rigorous
reachsets. Formalizing an exact-real ODE with implementation-defined force
errors is a separate semantic obligation, as is any discrete rollout claim.

## Distinctions the final theorem must preserve

- `routeB_pmi_certificate.jl:104` uses a four-variable block initial polynomial
  `qa^2+qb^2+dqa^2+dqb^2-R_init^2`; this is not a definition of the other eight
  initial coordinates. The trajectory exporter samples the full 12-ball.
- The saved polynomial certificate V, reconstructed at exporter lines 66-79,
  is evaluated on `(q4,q5,v4,v5,t)` and plotted against `t^2`. It is **not** the
  mechanical energy `E=kinetic+U-U0+controllerPotential` used in the new lemmas.
  Replacing V by an E comparison requires a proof of the original block/terminal
  goal; the negativity obstruction concerns this candidate E, not saved V.
- Exporter lines 152-162 skip simulation failures and out-of-limit trajectories.
  A proof must cover every allowed initial condition and input, including
  first-exit cases; it must not inherit this plotting filter as a domain proof.
- The block quantity does not bound remote velocities. An all-coordinate
  bootstrap must be proved independently before using the FD envelope cap.

These definitions resolve source ambiguities but do not close `target_contract`
or bind the original final statement through a comparator. Retain the original
joint-limit/domain and terminal quantifiers when that statement is formalized.

Source SHA-256 (checked in this turn):

- exporter: `35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf`
- certificate source: `235f4876ed1a3343f6d84f83c0079b4d279886585dc36aeb55b9fc0289177a77`
- DH library: `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`
