# Derivation and evidence boundary

## Mathematical payload

For a Fourier term with integer frequency `nu`, its value at the zero vector is
`exp(i * nu · 0) = 1`.  Therefore the q=0 value of each mass entry is the
finite sum of the 610 CSV real coefficients for that row and column.  The
frozen matrix `csvQ0Mass` is:

```text
[[4711/6000, -1481/80000, -103/16000, 7/60, -21/80000, 1/60],
 [-1481/80000, 1397297/2400000, 677771/2400000, 0, 41827/800000, 0],
 [-103/16000, 677771/2400000, 612881/2400000, 0, 8189/160000, 0],
 [7/60, 0, 0, 7/60, 0, 1/60],
 [-21/80000, 41827/800000, 8189/160000, 0, 40147/800000, 0],
 [1/60, 0, 0, 1/60, 0, 1/60]]
```

Adding `1/1000000` on the diagonal gives exactly the existing literal `M0`.
The theorem `csv_q0_plus_regularizer_eq_M0` checks this arithmetic in the
pinned Lean kernel using exact rationals.

## Provenance boundary

The CSV is not imported into Lean.  The external checker reads the frozen
snapshot, verifies its exact SHA-256 and 610 data rows, recomputes the above
matrix with rational arithmetic, and compares it to the payload.  This is an
audited extraction/provenance fact, not a kernel theorem about file I/O.

The source snapshot is the existing source-audit copy of the original target
CSV.  The original target directory is not modified.

## Non-claims

This leaf does not establish equality for arbitrary `q`, equality with the
deployed Julia `Float64` function, or physical DH source binding.  It also does
not promote `M0` or the CSV payload to the verified theorem registry by itself.
