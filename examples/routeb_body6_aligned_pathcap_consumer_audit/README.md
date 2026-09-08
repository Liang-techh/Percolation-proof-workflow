# GH-LEAN-BODY6-ALIGNED-CONSUMER

Agent/source_agent: **巨阳仙尊**.

This sidecar is a focused portable Lean compilation and axiom audit for
`examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean`.
It verifies the two public theorem leaves without changing their statements:

- `RouteBAlignedPathcapConsumerProof.actualStorageEqualsBRplusB_at_aligned_pathcap`
- `RouteBAlignedPathcapConsumerProof.actualStorageDefect_nonneg_at_aligned_pathcap`

The interface is deliberately narrow.  Given an `InitialPathCapState` explicitly
bound to `mkInitialPathCapState`, a projected coefficient identity
`projected2A345Term ... = PathCapB + state.B_hat`, and the storage alignment
`twoA2StorageActual = PathCapB`, the first theorem transports the actual storage
plus the typed path-cap shift to the projected term.  The second theorem consumes
that exact identity to certify a zero, hence nonnegative, local storage defect.

This does **not** prove whole-path inclusion, physical DH/source projection,
coefficient/source binding, ODE continuation/coverage, or registry/admission.

Run with:

```bash
CI_PORTABLE=1 bash verify.sh
```

A green receipt is only `compiled_candidate`: **待封不觉独立验证 / 待梁智炜（Codex）收割与最终整合**.
