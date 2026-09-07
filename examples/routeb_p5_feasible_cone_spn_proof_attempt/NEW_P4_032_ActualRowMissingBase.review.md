# Actual-row external slack and the missing base allocation

**OPEN_UNCOMPILED.** New independent sidecar after the revision-723 same-row audit. Existing files/state/registry remain unchanged. Read-only source/CSV inspection and four exact integer arithmetic checks only; no Lean, Julia, solver or regression execution.

There is now a concrete **same-row external coefficient slack**, but still no complete same-instance P4 front/loss/target packet. The new result isolates why a positive external ledger row cannot close that packet.

## The selected row

External base: `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

`routeB_compact_external_budget_ledger.csv`, physical line **9**, is the sole numerical row used in the sidecar:

| Field | Printed token |
|---|---|
| mass_regularizer / eta / theta | `1e-6` / `5.6` / `1.0` |
| bound_metric | `operator_pmi_gamma_lower_bound` |
| external_candidate_gamma | `0.2` |
| young_external_gamma | `0.15698624457194343` |
| max_port_pmi_gamma | `0.07849312228597172` |
| candidate_margin | `0.04301375542805658` |
| boxes / resolved / unknown / outside | `337 / 321 / 0 / 16` |
| subproblem_coverage_complete / routeB_global_gate | `True / False` |

It has no sf, prescribed scalar target, or front-floor/offset/scale product. The bounds-column name is preserved verbatim; its physical inequality direction requires checking the upstream interval contract, not interpreting the name alone.

Hashes frozen in this inspection:

- CSV: `a00383cb7ff547979028047c4489d7a4328d60b582b808efb65b19c2bba3c2c6`.
- `routeB_compact_external_budget_ledger.py`: `c36fe1f3c6b62bad7121458481b63f58dac130f251d413c68ed1a4f9430e7da9`.
- `routeB_compact_combined_schur_interface.py`: `c6d2af78691325991d6b91c163cd01ac8cfc8ee8b455fc963920a9e3fdf3529c` (read to corroborate the expression; no constants imported from its output).

## What the positive row actually gives

Treating the two printed coefficient tokens as exact rational numbers gives

`gamma - charge = 4301375542805657 / 10^17 > 0`.

This is exact **decimal-token arithmetic**, not exact replay of the floating-point computation. The generator uses `float`, computes `(1+1/theta)*rho2`, then subtracts it from gamma (`.py:67-69`). The printed `candidate_margin` exceeds the exact token difference by `1/10^17`; twice the printed rho2 likewise exceeds printed charge by `1/10^17`. These discrepancies do not change this coefficient sign, but prevent pretending that all printed tokens satisfy the rational identities simultaneously. No outward-rounding or source-reification proof was supplied.

The generator's actual consumer condition (`.py:114-117`) is

`b_base - (1+theta)*||l_base||^2 - charge*A_up >= 0`.

At theta=1, the missing target allocation is exactly

`target + 2*||l_base||^2 + charge*A_up <= b_base`.

The external gamma/charge slack neither supplies `b_base`, bounds `||l_base||^2`, nor proves a lower bound for `A_up`. It is not the P4 `F-L`. For a term `2*a_B' r_B`, the same generator explicitly requires a different two-sided energy column; this raw Young coefficient cannot be reused without a normalization proof.

## Consumable exact counterexample

Keep the selected row's gamma, charge and theta=1. Choose the **abstract interface assignment**, not an asserted physical trajectory state,

`b_base=gamma=1/5`, `||l_base||=1`, `A_up=1`.

The external coefficient slack remains positive, yet

`b_base - 2*||l_base||^2 - charge*A_up = -195698624457194343 / 10^17 < 0`.

Thus every positive target fails for this interface assignment. This refutes the inference “positive external row slack implies full positive budget”; it does not refute the physical candidate, because descriptor admissibility of this assignment is not established.

More sharply, hold every selected coefficient, `||l_base||=1`, `A_up=1` and the illustrative target `1/100` fixed. With `b_base=1/5` that target fails; with `b_base=11/5` it succeeds. Only the unrecorded base term changes. `same_coefficients_opposite_target_results` makes this pair directly consumable. The target `1/100` is chosen for the counterexample and is not present in the CSV. Even setting an abstract scalar margin equal to the full expression cannot rescue the first assignment; connecting it to the actual source is a separate obligation.

The sidecar exposes `row_slack_does_not_close_full_budget` and `row_counterexample_blocks_every_positive_target`. It also supplies `target_iff_base_allocation`, a sufficient `consume_base_allocation` lemma using gamma≥charge, and a same-domain functional consumer requiring the missing base allocation plus the external margin comparison. All remain uncompiled.

Even if a stronger base argument yields `(gamma-charge)*A_up≥0`, a state with `A_up=0` still defeats a strictly positive constant target unless an independent positive baseline is supplied. `zero_metric_no_positive_floor` isolates that additional obstruction.

## Smallest next obligations

1. Freeze this exact row's instance key and establish source/rounding/metric meaning, including eta/sf/domain/stage binding. No other row may fill missing fields.
2. Supply the same-state functions `b_base`, `l_base`, `A_up` and the exact inequality identifying their expression with the intended scalar margin. For the P4 adapter, also bind its energy/residual/remainder/front/alpha/beta/gain/offset/nominal objects; coefficient names do not perform that mapping.
3. Supply a prescribed target and prove `target + 2*||l_base||² + charge*A_up≤b_base` uniformly on that domain. For constant positivity, prove the required baseline or exclude zero metric states with a justified lower bound.

Other inspected budget records do not fill these gaps: the supply-allocated DH interface has its own exact theta_B/gamma_B coefficients, the block456 ledger uses a different M0 metric/component, and the beta tension audit compares free axes across coupled stages subject to descriptor admissibility. None was spliced into the selected row. No current physical F≤L/F>L verdict, PSD result, coverage closure or admission follows.
