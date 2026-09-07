# Route-B P5 component-relative decay Lean sidecar

This portable sidecar formalizes `T-P5-006`, using the mathematical result in
`agent_review_inbox/review-T-P5-005-kuangmanmozun-20260906T2307.md`.

It proves:

- `component_power_le`: `|r_i| <= rho_i |v_i|` implies
  `r_i v_i <= rho_i v_i^2`;
- `component_relative_decay_raw`: summing the six channels retains the exact
  diagonal damping `d_i-rho_i`;
- `admissible_relative_margin`: `0 <= rho_i < d_i` makes every retained margin
  strictly positive;
- `component_relative_residual_decay`: the combined source-independent theorem;
- `routeB_component_relative_residual_decay`: the same theorem specialized to
  the exact rational Route-B damping vector
  `[13/10,11/10,19/20,4/5,13/20,1/2]`.

The local copy of the damping vector is an exact-rational interface copy of
`examples/routeb_supply_core/RouteBSupplyCore.lean`; it is not a new source
binding.  This sidecar deliberately does **not** derive `rho` from the current
FD envelopes, samples, Float64 execution, controller/solve residuals, or true-DH
semantics, and it makes no P5/M4 admission claim.

Run from the repository checkout with the pinned local-FKG Lake environment:

```bash
CI_PORTABLE=1 bash examples/routeb_p5_component_relative_decay_lean/verify.sh
```

`verify.sh` requires `lake` and `lean` on `PATH`, checks the pinned toolchain,
compiles with `-DwarningAsError=true`, requires an axiom report for every
exported theorem, and fails if `sorryAx` appears.
