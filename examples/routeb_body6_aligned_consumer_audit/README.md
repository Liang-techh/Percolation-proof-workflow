# BODY6 aligned-path cap consumer focused Lean audit

Owner/source agent: 巨阳仙尊

This portable sidecar compiles the existing candidate
`examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean`
inside the repository-pinned `examples/local_fkg` Lake environment.

Trusted-core scope:

- `consume_aligned_path_cap_attempt`: from typed `ConsumerPremises` (actual/encoded storage alignment, initial source cap, path start, integrated and uniform growth, domain projection, whole-path membership, and one shifted budget), derive `FullPathCap (target m) path bar`.
- `source_full_cap_does_not_pay_shift_attempt`: exact origin regression showing a source full cap of `0` does not by itself pay the encoded shift needed for a target full cap of `1`.

The checker also performs a placeholder scan and `#print axioms` audit under `-DwarningAsError=true`.

Not proved here: existence of a Route-B instance of `ConsumerPremises`, physical/source binding, path ODE or continuation, positivity/coercivity, domain coverage, first-exit closure, source admission/receipt, registry mutation, or P4/P5 parent closure.

Run from a GitHub-CI environment with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_body6_aligned_consumer_audit/verify.sh
```
