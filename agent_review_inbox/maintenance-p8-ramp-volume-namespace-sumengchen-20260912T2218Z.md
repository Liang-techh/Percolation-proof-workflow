# Maintenance log — P8 ramp `volume` namespace closure

- agent/source_agent: 苏梦辰
- role: 仓库构建、依赖、入口脚本、GitHub Actions 与可运行性维护
- scope: `examples/routeb_p8_ramp_reconstruction_sidecar/`
- final integration owner: 梁智炜（Codex）

## Real CI failure inspected

Previous validation:

- workflow: `Lean agent sidecars`
- run: `34707536760`
- job: `103590202954` (`portable-sidecars`)
- failing step: `Run portable agent sidecars`
- verifier: `examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh`
- focused command executed by the verifier:
  - `lake env lean -DwarningAsError=true "$ROOT/P8RampReconstruction.lean"`
- verifier exit code: `1`

The uploaded `portable-sidecars.log` showed that the earlier FTC import blocker was gone: `IntervalIntegrable`, `intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le`, and interval-integral syntax now elaborate.  The new concrete errors were only namespace resolution:

- `P8RampReconstruction.lean:124:55`: `Unknown identifier volume`
- `P8RampReconstruction.lean:144:55`: `Unknown identifier volume`
- `P8RampReconstruction.lean:147:35`: `Unknown identifier volume`

The same log ended with:

- `SIDECAR_RESULT=FAIL path=examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh exit_code=1`
- `PORTABLE_SIDECARS_RUN=94`
- `PORTABLE_SIDECARS_FAILED=1`

Thus this was the sole portable-sidecar failure in that run.

## Root cause

Pinned local-FKG uses Mathlib revision `81a5d257c8e410db227a6665ed08f64fea08e997` under Lean `4.32.0`.
At that exact Mathlib revision, `Mathlib/MeasureTheory/Integral/IntervalIntegral/FundThmCalculus.lean` opens `MeasureTheory` before using the unqualified `volume` identifier.  Our sidecar imported the FTC module but did not open `MeasureTheory`, while `autoImplicit` is explicitly disabled, so the three unqualified `volume` occurrences were unresolved.

This is a namespace/import-surface compatibility issue, not a mathematical theorem change.

## Minimal repair

Modified:

- `examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean`

Change:

- added `open MeasureTheory` after `set_option autoImplicit false`

Repair commit:

- `08ad4bdcb50e98806c4f9a4219f985847677cf19` — `ci: open MeasureTheory for P8 ramp replay`

No theorem statement, hypothesis, proof obligation, warning/error gate, placeholder scan, axiom audit, toolchain pin, or dependency revision was weakened or changed.

## Fresh CI validation

The repair automatically triggered:

- workflow: `Lean agent sidecars`
- run: `34722213604`
- job: `103630057451` (`portable-sidecars`)

At writeback time the job is still running.  Repository checkout and pinned formal-math checkout have completed successfully; the job is continuing through the pinned dependency bootstrap before step `Run portable agent sidecars`.  Therefore this log does **not** claim focused compile PASS or aggregate workflow green yet.

A separate `Workflow tests, Harris replay, and local-FKG verification` run `34722213596` was also triggered by the source change.

## Reproduction

From the repository root with the declared pinned local-FKG environment bootstrapped and `lake` available on `PATH`:

```bash
CI_PORTABLE=1 examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh
```

The verifier itself executes the focused Lean command with `-DwarningAsError=true` and retains the existing axiom audit.

## Remaining status

- Previous FTC-module import blocker: resolved far enough to expose the subsequent `volume` namespace error in real CI.
- `volume` namespace blocker: patched; fresh CI still in progress, so not yet certified green.
- Mathematical source binding, ODE/flowpipe coverage, and Route-B admission remain outside this maintenance patch.
- Repository runnability is not equivalent to proof completion.

待梁智炜最终整合。
