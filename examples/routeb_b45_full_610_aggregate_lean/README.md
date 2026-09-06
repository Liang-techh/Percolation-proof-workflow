# B45-1 full 610-row aggregate comparator seam

This sidecar is a minimal exact-real contract for the full mass CSV.  It
models all 610 rows as Fourier atoms of 6x6 entries, sums them into a matrix,
and proves that the source six-body mass sum plus the exact `1/1000000`
diagonal regularizer equals that aggregate, conditional on two explicit
premises:

1. the CSV aggregate equals the sum of six body Fourier evaluators;
2. each body evaluator equals the exact-real source body contribution.

The file does not claim either premise.  The original CSV schema contains
`row,col,nu1..nu6,real_num,real_den,imag_num,imag_den` but no body identifier,
so the missing body-level provenance cannot be reconstructed from the 610-row
payload alone.  It also does not identify Julia `Float64` execution with the
exact-real definitions.

The 17-row potential table is intentionally absent: it is a different scalar
potential artifact and cannot discharge this mass comparator.
