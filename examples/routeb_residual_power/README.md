# Residual power: a proved budget and a precise obstruction

These lemmas were compiled with Lean 4.33.1 and the existing pinned Mathlib
cache. They are not yet comparator-accepted or registered as VERIFIED.

Let P(v,w) be the exact rational six-channel supply in RouteBSupplyCore,
and let e be a vector of additive forces. The new principal theorem proves

    P(v,w) + sum_i e_i*v_i
      <= (631227/1086800)*w^2 + sum_i e_i^2/(2*D_i).

This holds for every real v,w,e. It spends half the damping on the disturbance
channel and half on the force error. The additive error term is retained at
w=0. It can therefore support a finite-time energy estimate with an explicit
integrated defect, rather than pretending the defect is homogeneous in w.
The sharper unsplit bound `sum_i (G_i*w+e_i)^2/(4*D_i)` is also proved.

The exact one-channel budget theorem states that, for d>0,

    (forall v, -d*v^2+e*v <= B) iff e^2/(4*d) <= B.

In particular e!=0 gives a positive value at v=e/(2*d). This only excludes
a uniform zero-budget argument with a fixed nonzero velocity-linear force
defect. It is NOT a demonstrated counterexample to the DH certificate or
to a state-dependent residual model.

## Actual proof/repair history

- `output/run-cwI9TzoS/`: failed strict compilation; two tactic sequencing
  warnings and an unfinished finite-vector coefficient simplification.
- The proof script was repaired without weakening any theorem statement.
- `output/run-LstptWRG/`: compilation exit 0. All ten printed theorem axiom
  reports contain only propext, Classical.choice and Quot.sound. The reused
  supply core was freshly compiled in the same run.
- Source SHA-256:
  `0f74bf60dbe7473f4b7f7d78c759a6fbff03ae984bb932f203a31c8c8de7de3d`.
- Compiled object SHA-256:
  `3301afdef1bf669f4cabc1d1be741854e745feaff54735df8a4d71d349f6af82`.

Reproduce offline with `bash examples/routeb_residual_power/verify.sh` in WSL.
No dependency installation or broad regression suite is involved.

## Next mathematical bottleneck

Bind e to the actual DH force residual, including finite-difference C/G,
parameter rounding, any mass-model difference and linear-solve residual.
Then bound the weighted squared error on the proven domain and integrate it
with the actual storage and disturbance budget. Neither this source nor the
supply core proves that dynamics binding or the domain-containment premise.

The historical `routeB_compact_fd_remainder_energy_audit.csv` uses supply
coefficient 23089373/99590400, whereas the current DH-specialized supply core
uses 631227/2173600. Its numerical ledger must not be transplanted as a theorem
for the new coefficients without checking the controller/model assumptions.
The existing ledger already recognizes that raw additive error less than a
unit-supply margin does not establish homogeneous absorption.
