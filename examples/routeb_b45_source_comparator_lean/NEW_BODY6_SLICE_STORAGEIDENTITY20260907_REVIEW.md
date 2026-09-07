# BODY6 storage-identity transfer review

Status: `OPEN_UNCOMPILED`; fail-closed source-binding contract.

The sidecar separates three obligations that were previously easy to conflate:
same-storage equality on a domain, an initial-set upper bound, and a future
sublevel barrier along a path. `initial_bound_transfer_attempt` transfers an
initial bound only after `V` and `W` are equal on the initial domain. The
barrier transfer additionally requires the whole path to remain in the same
identity domain.

`RouteBInitialTransfer` records the exact missing bridge for the current
Route-B branch: `V_eps` must equal `Vfull_DH` on the comparison domain, the
block-only initial set must lie in that domain, and the recorded initial bound
must be proved for the same `V_eps`. The scalar value
`492033745203/25600000000000 < 1` is only a budget fact; it is not a source
identity.

The counterexamples show that equal initial bounds do not imply a future
barrier, and equal derivatives do not fix an additive constant at a fixed
threshold. Therefore the targeted-gain `V_eps` ledger cannot be silently used
as a full-DH `V≤1` barrier. The actual storage formula, normalization,
domain/path inclusion, and dynamics remain separate obligations.

No claim is made about DH source correctness, flowpipe existence, coverage,
residual absorption, terminal transfer, pinned Lean compilation, or registry
promotion.
