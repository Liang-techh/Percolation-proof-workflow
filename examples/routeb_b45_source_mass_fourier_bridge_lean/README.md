# B45-1 source-table to regularized Fourier bridge candidate

This Mathlib-only sidecar proves the low-dependency aggregation seam:

```text
sum_body sourceBodyContribution(body)
  = sum_body fourierBody(body)
```

under an explicit per-body comparator premise, and then adds the exact
`1/1000000` diagonal regularizer.  The exact source mass and `I_val/3` tables
are present in the definition of `bodyContribution`.

The theorem does **not** prove the comparator premise.  In particular, it does
not identify Julia `Float64` execution, the 610-row aggregate CSV, or the
physical DH recursion with the abstract `fourierBody` evaluator.

The 17-row artifact is a separate potential Fourier table: the generator
accumulates `P += m_i * 9.81 * pcom_i[3]`, whereas the mass table accumulates
the 6x6 Gram contributions.  Therefore the 17 rows cannot discharge the
per-body mass comparator or serve as a slice of the full six-body mass sum.
