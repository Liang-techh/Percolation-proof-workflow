# Route-B P5 finite-horizon energy-budget Lean sidecar

This portable sidecar formalizes the pointwise/source-independent portion of
`T-P5-013` from `review-T-P5-013-honglianmozun-20260907T0358.md`.

It contains:

- `dual_work_budget`: square-only weighted-dual work charging with the exact
  `R <= 4*gR*BR` budget;
- `mixed_energy_rate`: cubic absorption + weighted-dual remainder + one-sided
  ramp-work cap imply `Zdot <= Hbar + BR`;
- `linear_growth_stays_below_barrier`: the pure algebraic terminal step used
  after a calculus layer has established `Z(t) <= Z(0)+tB`;
- `t1_fifty_fifty_headroom_from_rational`: the all-rational `T=1`, 50/50 split
  criterion from equation (27), converted to the displayed strict headroom;
- `upper_storage_coercivity_counterexample`: a kernel theorem recording why
  `A <= K*Z` alone cannot yield asymptotic `-alpha*Z` decay.

The sidecar intentionally does **not** formalize the first-exit calculus/ODE
argument yet.  It also does not supply `S_F`, `Hbar`, `Rbar`, `W_min`, source or
IEEE execution bounds, P8 ramp-graph coverage, or any P5/M4 admission result.
柳冠一's disjoint `T-P5-014` remains the source-to-weighted-dual adapter lane.

## Focused check

```bash
bash examples/routeb_p5_finite_horizon_budget_lean/verify.sh
```

`verify.sh` finds `lake` from `PATH`, uses the repository-pinned
`examples/local_fkg` Lake environment by default, requires the same pinned Lean
version, compiles with `-DwarningAsError=true`, and checks all printed axiom
reports for `sorryAx`/unexpected errors.

A successful focused compile is only a `compiled_candidate` for this abstract
child.  It remains **待封不觉独立验证 / 待梁智炜最终整合**.
