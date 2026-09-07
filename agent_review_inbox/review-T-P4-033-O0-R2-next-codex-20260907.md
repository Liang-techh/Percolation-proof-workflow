# T-P4-033 O0-R2 next — exact Fourier tuple to weighted metric / Schur margin

Scope is only the next consumer of the already-ingested exact-Fourier
one-cell tuple. The tuple values are intentionally not repeated here.

## Key result

The tuple already carries the required exact `source_key`, `state_key`, cell,
fixed `B=(4,5)`, `D=(1,2,3,6)`, and block orientation
`M_BD[B,D], DeltaM_DB[D,B]`. Its norm is `induced_infinity`. The arithmetic
tuple therefore cannot yet be consumed by the canonical weighted O0-R2 or
Schur-margin O0-R3 target, because the receipt has neither the metric lower
bound nor the weighted norm conversion.

## Smallest weighted child

The preferred Lean-facing target should be stated directly in the output
Euclidean norm:

```lean
theorem exact_fourier_weighted_perturbation
    (E : Matrix (Fin 2) (Fin 2) ℝ)
    (B_up : Matrix (Fin 2) (Fin 2) ℝ)
    (U2 s : ℝ)
    (hE : ∀ a : Fin 2 → ℝ,
      ‖E *ᵥ a‖₂ ≤ U2 * ‖a‖₂)
    (hs : 0 < s)
    (hmetric : ∀ a : Fin 2 → ℝ,
      s * ‖a‖₂ ≤ Real.sqrt (dot a (B_up *ᵥ a))) :
    ∀ a : Fin 2 → ℝ,
      ‖E *ᵥ a‖₂ ≤ (U2 / s) *
        Real.sqrt (dot a (B_up *ᵥ a)) := by
  sorry
```

The receipt-friendly equivalent of `hmetric` is the exact triple:

```text
B_up >= beta I,   s > 0,   s^2 <= beta
```

with `B_up` in the canonical left-output orientation. If the existing tuple
is retained as an induced-∞ bound, an additional exact finite-dimensional norm
adapter is required before using this target, for example a proved
`induced_infinity -> induced_2` operator bound on the same `Fin 2` port. The
cleaner child is to supply `U2` directly under `induced_2`; merely relabeling
the existing induced-∞ bound as an induced-2 bound is invalid.

The same-key fields for this child are:

```text
metric.source_key = tuple.source_key
metric.state_key  = tuple.state_key
metric.norm       = induced_2
metric.orientation = left_output
metric.B_up, metric.beta, metric.s
metric.s_positive = true
metric.s_sq_le_beta = true
metric.B_up_ge_beta_I_proved = true
```

The current tuple supplies the first two keys and the block orientation, but
not the metric fields or the norm-conversion proof.

## Schur-margin child after weighted conversion

Only after a same-key weighted baseline and perturbation are available should
the margin consumer be called. Its minimum scalar target is:

```lean
theorem exact_fourier_schur_margin_consumer
    (rho_r epsilon_R theta m_r : ℝ)
    (h_rho : 0 ≤ rho_r)
    (h_eps : 0 ≤ epsilon_R)
    (h_theta : 0 < theta)
    (h_margin :
      (1 + 1 / theta) * ((rho_r + epsilon_R)^2 - rho_r^2) < m_r) :
    0 < m_r -
      (1 + 1 / theta) * ((rho_r + epsilon_R)^2 - rho_r^2) := by
  linarith
```

This is only the budget arithmetic. Its input receipts must prove, under the
same source/state/metric key:

```text
weighted baseline:     ||R_r a||_2 <= rho_r * sqrt(a^T B_up a)
weighted perturbation: ||(R_f-R_r)a||_2 <= epsilon_R * sqrt(a^T B_up a)
theta > 0
remaining baseline margin m_r > 0
strict budget inequality above
```

The existing exact-Fourier child has no `rho_r`, no positive `m_r`, and no
weighted `epsilon_R`; its recorded perturbation is still under the
induced-∞ source contract. Therefore it cannot be passed directly to the
Schur consumer.

## Exact remaining gap

The next consumable child must supply one of these two routes:

1. **Weighted route:** same-key exact `B_up >= beta I`, an exact positive
   lower root `s` with `s^2 <= beta`, and either a direct induced-2 port bound
   or a proved induced-∞ to induced-2 adapter; or
2. **Direct Schur route:** same-key weighted `rho_r`, weighted `epsilon_R`,
   `theta > 0`, `m_r > 0`, and the strict remaining-margin inequality.

No tuple arithmetic is missing. The unique mathematical obstruction is the
absence of the exact metric lower-root/norm-conversion witness; if attempting
O0-R3 directly, the corresponding missing premise set is the weighted
baseline plus positive remaining margin and `theta`. Keep
`weighted_metric_conversion=false` and `schur_margin_consumed=false` until
one route is supplied under the tuple's exact `source_key` and `state_key`.
