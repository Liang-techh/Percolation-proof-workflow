# External catalog receipt

`percolation_workflow.catalog_receipt` wraps the external-catalog validator in
a deterministic provenance receipt. It records the catalog hash, upstream
commit, license/attribution markers, classification histogram, and the
candidate paths that are eligible for further Route-B review.

The receipt is advisory only. `registry_promoted` and
`formal_certificate_allowed` are always `false`; no catalog entry is a Lean
theorem and no candidate is admitted without an independent current-pin
compile, exact statement comparator, and the normal zero-sorry kernel gates.
