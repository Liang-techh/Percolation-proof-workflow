# Attempt history

## 2026-09-06 — isotropic rotation proof repair loop

- `run-UsDXwp3g`: failed because matrix multiplication was not definitionally
  the desired double sum.
- `run-hA8S0vil`: normalized the outer/inner sums but used the wrong
  `sum_eq_single` side conditions.
- `run-c4Udabcs`: switched to `sum_eq_single_of_mem`; only an unused simp
  argument remained under `warningAsError`.
- `run-KWENke5I`: removed that argument; compile and source restriction passed.

The source-specific rotation orthogonality and Float64 bridge remain open.
