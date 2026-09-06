# B45-1.g: q=0 Fourier mass bridge

This is a narrow independent Lean leaf.  The kernel checks an exact frozen
36-entry q=0 aggregate plus `(1/1000000) I = M0`.  The aggregate is the sum of
all real coefficients in the 610-row Fourier mass CSV, because every Fourier
phase evaluates to `1` at `q=0`.

The Lean file intentionally contains no CSV reader and no theorem asserting
that a file has a particular byte content.  `verify.py` is the provenance
boundary: it checks the CSV SHA-256, row count, all row/column/frequency
records, zero imaginary coefficients, and independently recomputes the frozen
36 rationals before Lean compiles the frozen payload.

This leaf therefore proves an exact finite bridge conditional on the external
CSV-to-payload extraction record.  It does not prove the full q-dependent
DH/Fourier identity, the Julia Float64 bridge, mass PSD, or any reachability
claim.
