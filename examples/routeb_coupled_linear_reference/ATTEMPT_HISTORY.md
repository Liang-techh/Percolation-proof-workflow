# Attempt history

The initial source and report are saved before the first audit. Every attempt's
`before_run.json`, `terminal.log`, input snapshots and source copies are
authoritative; no success status is assumed before the subprocess completes.
There is no Lean compilation or numerical flow/eigenvalue experiment in this leaf.

## Observed first run

`output/run-20260905T192654Z-3dbe159f` completed with
`EXACT_COUPLED_NOMINAL_REFERENCE_PASS` and `AUDIT_EXIT_CODE=0`.
No audit assertion failed and no mathematical repair was required.

It checked 610 mass rows, 17 potential rows, 72 entries in the two inverse
products, 78 nominal-balance coefficients, and 26 residual coefficients.
All six LDL pivots are positive and the factorization reconstructs M0 exactly.
The earlier saved rational M0,H0 comparison also passed.

After completion, only the root documentation was updated with observed
results. One documentation patch initially failed because its expected text
did not match DERIVATION.md; no files from that failed patch were changed,
as confirmed by a subsequent read. The corrected documentation patch succeeded.
That editor failure is visible in tool history, not a mathematical audit failure.
The pre-run snapshots and terminal log remain unchanged. No second audit was
needed or performed.
