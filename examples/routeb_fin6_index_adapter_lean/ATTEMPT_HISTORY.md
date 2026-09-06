# Attempt history

## Initial attempt

The first implementation is intentionally kept as the current source rather
than being silently overwritten.  It uses a subtype for Julia 1-based indices
and `omega` for the inverse-offset arithmetic.  A compile failure, if found,
will be recorded below together with its run directory and retained log.

No existing Route-B sidecar or source project is modified by this leaf.

## `run-251070PB` — failed

The pinned compiler rejected the first draft because subtype bounds were not
explicitly exposed to `omega`, and the finite `mergeSort` equality was not
definitionally reducible by `rfl`.  The run is retained at
`output/run-251070PB/`; the source was repaired by exposing the Julia lower
and upper bounds and using `native_decide` only for the concrete finite-list
sorting fact.
