# BODY6 aligned-path cap consumer focused Lean audit

Owner/source agent: 巨阳仙尊

This portable sidecar audits the existing candidate
`examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean`
against the repository-pinned `examples/local_fkg` Lake environment.

## Trusted-core statements

The target exposes two public theorems in namespace
`NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908`:

- `consume_aligned_path_cap_attempt`: for real parameters, assuming the aligned energy obeys
  `energy_at_aligned ... <= B` and the already-shifted scalar budget obeys
  `B + sigmaBar < cap Ahat AC Ay`, conclude
  `energy_at_aligned ... + sigmaBar < cap Ahat AC Ay`.  The theorem keeps the
  source-side sign/positivity hypotheses (`0 <= Ahat`, `0 < AC`, `0 < Ay`,
  `0 < cap ...`, `0 <= B`, `0 <= sigmaBar`) explicit at the interface.
- `source_full_cap_does_not_pay_shift_attempt`: the same contract, proved by
  direct reuse of `consume_aligned_path_cap_attempt`.  Its role is to make the
  accounting boundary explicit: the consumer receives `B + sigmaBar < cap`;
  the shift is not silently paid a second time by the source cap.

The local import chain is
`NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907` ->
`NEW_BODY6_SLICE_PATHDOMAINPROJECTION20260907` ->
`NEW_BODY6_SLICE_INITIALPATHCAPS20260907` -> aligned consumer, with the first
modules reusing the pinned `ActualStorage` / `ActualShift` environment.

## Portable CI behavior

Lean 4.32 rejects `-o` compilation of a source outside the active Lake package
root.  `verify.sh` therefore stages only the three BODY6 dependency sources in a
temporary directory under `examples/local_fkg`, compiles their `.olean` files
there, prepends that isolated cache to Lake's `LEAN_PATH`, and removes it on
exit.  No repository source, manifest, or toolchain file is mutated.

The checker verifies `lake` and `lean` from `PATH`, checks the pinned toolchain
and `lake-manifest.json`, scans the target for `sorry`/`admit`, compiles under
`-DwarningAsError=true`, and runs `#print axioms` on both public theorems.

Not proved here: a deployed instance of the scalar premises, physical/source
binding, path ODE or continuation, whole-path/domain coverage, first-exit
closure, Float64/controller semantics, source admission/receipt, registry
mutation, or P4/P5 parent closure.

Run in the GitHub-CI environment with `lake` and `lean` on `PATH`:

```bash
CI_PORTABLE=1 bash examples/routeb_body6_aligned_consumer_audit/verify.sh
```
