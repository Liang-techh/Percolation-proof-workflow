# P3 finite-table reification seam

`FiniteTableReification.lean` adds an independent, kernel-checkable interface
for a future explicit Fourier payload. `ExactCoefficientBridge.lean` is not
modified.

The interface requires, as proof fields:

- unique `(matrix-entry, frequency)` keys;
- exact finite-support equality between the rows and the declared support;
- exact entry coverage;
- caller-supplied row count and entry count via `HasShape`.

`rows_give_map_equality_on_support` and
`finite_table_checker_sound` prove that two coefficient maps equal to every
finite row are equal on the represented support. `full_entries_card` kernel
checks the 36-entry cardinality. A one-row smoke table is included only to
compile-check the interface; it is not Route-B data.

## Focused verification

Run from WSL:

```text
bash examples/routeb_fourier_source_binding_lean/verify_finite_table.sh
```

The script compiles only the new seam plus its unchanged bridge dependency,
with warnings treated as errors, and prints the resulting Lean exit code and
hashes.

## Explicit open obligation

The first unclosed instantiation is the construction of a concrete
`FiniteCoefficientTable` whose `rows.length = 610`, whose keys/support are
proved complete and unambiguous, and whose row coefficients are proved equal
to both the exactized DH map and the frozen CSV map. The theorem
`routeB_610_payload_obligation` is conditional on precisely those hypotheses;
it does not claim that the Python checker has been re-proved by the Lean
kernel, and no source data are fabricated here.
