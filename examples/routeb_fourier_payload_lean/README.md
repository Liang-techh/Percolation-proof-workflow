# Route-B P3 Fourier payload — first Lean instantiation seam

This example is the first concrete Lean data instantiation for the P3 Fourier
table. `PayloadRows.lean` contains 610 literal rows with rational coefficients,
generated from the frozen CSV
`examples/routeb_source_binding_audit/snapshots/current_exact/routeB_fourier_mass_full_rational.csv`.
The CSV hash is checked by `generate_payload.py` before generation.

The generated file is data only. `Payload.lean` constructs a
`FiniteCoefficientTable` and proves in Lean:

- the 610 `(entry, frequency)` keys are unique;
- the declared finite support is exactly the support of those rows;
- the table has 610 rows and 32 nonempty matrix entries;
- `FullEntries = Fin 6 × Fin 6` has cardinality 36, and the four omitted
  matrix entries have empty support;
- a kernel-defined CSV lookup returns exactly each row coefficient.

The 36-entry statement intentionally allows structurally zero entries. The
source CSV has no rows for `(4,5)`, `(5,4)`, `(5,6)`, or `(6,5)`, so adding
fabricated zero rows would no longer be a 610-row reification of the CSV.

Run the focused check from WSL:

```text
bash examples/routeb_fourier_payload_lean/verify.sh
```

The pinned environment is Lean `v4.33.1` with Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474`; `verify.sh` checks both pins and
compiles only this sidecar.

This does not define or prove an `exactizedDHSourceCoeff` map. The theorem
`conditional_source_csv_equality_on_support` remains conditional on a caller
providing per-row equality for an external source map. Exactized DH map
equality is therefore still OPEN, and no `LEAN_VERIFIED` or physical
certificate claim is made.
