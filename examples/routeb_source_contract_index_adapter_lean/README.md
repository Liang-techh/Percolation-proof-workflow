# Route-B source-contract index adapter

This isolated sidecar transports the already compiled seven-slot
`SourceContractAdapter` into the indexing conventions of `BodySemanticCore`.
It fixes the intended zero-based interpretation:

- human body 4 is `Fin 6` index 3, with COM origin slots 3 and 4;
- human body 5 is `Fin 6` index 4, with COM origin slots 4 and 5;
- human joint 5 is inactive for body 4 and active for body 5;
- when active, joint `j` reads the z-axis of parent frame slot `j`.

The proofs reuse the abstract origin/axis slot bridge and ancestor cutoff. They
do not unfold DH matrix entries, introduce axioms, parse CSV data, or claim a
Julia `Float64` comparator result. This sidecar is intentionally not wired into
the main theorem DAG or persistent state.
