# T-P4-033 O0-R3 — minimal canonical receipt contract

Date: 2026-09-07  
State snapshot: revision 502  
Scope: define the smallest receipt that can later feed O0-R1/R2/R3.  This
review deliberately does not consume any existing ledger or claim O0 closure.

## Current disposition

No same-key physical `(rho_r, remaining_margin)` is available.  The port leaf
has only an unverified `rho_F^2` candidate; the physical Schur ledger lacks the
same-domain `A > mu` and physical coupling receipts; and the adapter still
lacks the typed identity `R_port a_B = r_B`.  The exact-real inverse flag is
also fail-closed: a numeric `K` is unusable unless
`proves_exact_real_bound=true` is attached to an authoritative receipt.

## Minimal canonical receipt

The interval/Lean agent should emit one receipt per canonical cell, or one
uniform-domain receipt whose `domain` explicitly covers every cell:

```json
{
  "schema": "routeb.o0.canonical_source_metric_schur_receipt.v1",
  "status": "PENDING",
  "receipt_id": "<content-addressed-id>",
  "source_key": "<canonical-sha256-K>",
  "state_key": "<canonical-sha256-cell-and-evaluator-state>",
  "domain": {
    "cell_id": "<canonical-cell-id>",
    "q_lo": ["..."],
    "q_hi": ["..."],
    "axis_order": ["q1", "q2", "q3", "q4", "q5", "q6"],
    "coverage": "<complete-for-this-receipt-or-explicit-cell-only>"
  },
  "semantics": {
    "exact_real_mu": "1/1000000",
    "deployed_mu_literal": "1e-6",
    "fd_step": "<exact-rational-h>",
    "force_scale": "<canonical-scale-id>",
    "coefficient_version": "<id>",
    "rounding_or_interval_mode": "<outward-mode>"
  },
  "metric": {
    "orientation": "left_output",
    "norm": "induced_2",
    "B_up_identity": "B_up = S^T S",
    "beta": "<exact-rational-beta>",
    "s": "<exact-rational-s>",
    "s_positive": true,
    "s_sq_le_beta": true,
    "B_up_ge_beta_I_proved": true
  },
  "inverse": {
    "matrix": "M_DD(mu_exact)",
    "K": "<exact-rational-K>",
    "norm": "induced_2-or-induced_infinity",
    "proves_exact_real_bound": true,
    "proof_receipt": "<pinned-theorem-or-interval-receipt-id>",
    "epsilon_A": "<exact-rational-or-null>",
    "epsilon_A_times_K_lt_one": true
  },
  "weighted_baseline": {
    "map": "R_r",
    "rho_r": "<exact-rational-rho_r>",
    "rho_r_nonnegative": true,
    "statement": "forall a_B, ||R_r a_B||_2^2 <= rho_r^2 * (a_B^T B_up a_B)",
    "proof_receipt": "<pinned-theorem-or-interval-receipt-id>"
  },
  "weighted_perturbation": {
    "map": "R_f - R_r",
    "epsilon_R": "<exact-rational-epsilon_R>",
    "statement": "||(R_f-R_r)a_B||_2 <= epsilon_R*sqrt(a_B^T B_up a_B)",
    "proof_receipt": "<pinned-theorem-or-interval-receipt-id>"
  },
  "schur_baseline": {
    "theta": "<fixed-exact-rational-theta>",
    "lambda": "1 + 1/theta",
    "remaining_margin_m_r": "<exact-rational-m_r>",
    "m_r_positive": true,
    "same_normalization_as_metric": true,
    "proof_receipt": "<physical-schur-receipt-id>"
  },
  "physical_binding": {
    "statement": "R_port a_B = r_B",
    "proof_receipt": "<typed-source-binding-receipt-id>"
  },
  "admission": {
    "all_source_keys_equal": true,
    "all_state_keys_equal": true,
    "registry_promoted": false,
    "formal_certificate_allowed": false
  }
}
```

The canonical key `K` must hash the normalized semantics, source hashes,
coordinate order, metric convention, exact `mu`, FD/force scales, coefficient
version, and rounding mode.  `state_key` must additionally bind the cell/domain
and evaluator state.  Artifact hashes alone are insufficient if they are not
joined by these normalized fields.

## Exact child obligations

The smallest executable decomposition is:

1. **O0-R1 inverse child.** Supply exact-real `K >= 0` with
   `proves_exact_real_bound=true`; prove `epsilon_A*K < 1`; emit
   `K_f = K/(1-epsilon_A*K)` and
   `DeltaK = epsilon_A*K^2/(1-epsilon_A*K)` under `source_key=K`.
2. **O0-R1 port perturbation child.** Bind the same-key B/C bounds and derive
   an exact unweighted perturbation, then either attach the O0-R2 metric
   witness `(s,beta)` above or directly prove the weighted `epsilon_R` line.
3. **O0-R2 baseline child.** Do not treat the existing `rho_F^2` as `rho_r`.
   Provide an exact rational `rho_r`, or provide `g_r` plus a rational witness
   `g_r <= rho_r^2`, in the same `B_up` metric.
4. **O0-R3 margin child.** Provide exact `m_r > 0` after the baseline charge,
   with the same fixed `theta`/`lambda`, `l_base`, `A_up`, cell, and source/state
   keys.
5. **Join child.** Check only the exact scalar condition

   ```text
   lambda*((rho_r+epsilon_R)^2-rho_r^2) < m_r
   ```

   and return `m_f = m_r - lambda*((rho_r+epsilon_R)^2-rho_r^2) > 0`.
   This is the only O0-R3 arithmetic consumption step.

## Fail-closed rules

- `proves_exact_real_bound=false` or missing is an O0-R1 obstruction, even if
  `K` is rational and numerically plausible.
- A squared baseline field without an exact rational root witness is not a
  `rho_r` input.
- An unweighted bound divided by `s` is not weighted evidence unless the same
  key includes the proved `B_up >= beta I`, `s > 0`, and `s^2 <= beta` facts.
- A candidate `margin`, a physical `rho_reg`, or an unrelated Schur ledger
  cannot be renamed `m_r` without the same metric, normalization, cell, and
  source/state binding.
- `R_port a_B = r_B` remains a prerequisite to call the result physical; the
  canonical receipt must remain `PENDING` until that typed identity is present.
