# Bounded comparator handoff — 2026-09-05

**Compiled mathematics and dependency audit passed. Statement comparator and
nanoda acceptance remain blocked by exporter/toolchain incompatibility.
Nothing was ingested into a verified registry.**

## New targets

- `Challenge.lean` imports only Mathlib modules and directly spells out all
  six damping and disturbance coefficients, quantified over arbitrary
  `v : Fin 6 → ℝ` and `w : ℝ`, with bound `631227/2173600 * w²`.
  It has an independent elementary proof, so even the Challenge has no holes.
- `Solution.lean` separately declares the same explicit statement, proving it
  from `RouteBSupplyCore.pointwise_supply_bound`. Neither side imports the other.
- The comparator target name on both sides is
  `RouteBSupplyComparison.explicit_supply_bound`.
- `comparator.json` sets `definition_names=[]` and `enable_nanoda=true`, and
  permits only `propext`, `Quot.sound`, and `Classical.choice`.
- `DependencyAudit.lean` inspects the compiled Solution's transitive imports
  and declaration closure, traversing types, definition/opaque bodies,
  inductive constructors, and recursor rules. It forbids importing Challenge,
  rejects nonstandard axioms, and requires the intended supply-bound and
  vector-completion proof dependencies.

The existing upstream comparator's `Compare.loop` and `runForUsedConsts`
also compare non-hole definitions and inspect opaque bodies. No custom
definition hides coefficients in this explicit target. Those upstream
comparison checks are configured but **were not reached** in this run.

## Actual final attempt

`output/comparator-cached-exporter-ec0FOjSk/` contains:

- `compile-RouteBSupplyCore.log`, `compile-Challenge.log`,
  `compile-Solution.log`, `compile-DependencyAudit.log`: all strict direct
  Lean 4.33.1 compilations passed (`-DwarningAsError=true`).
- `lake-prebuild.log`: real Lake build of Challenge and Solution succeeded.
- Dependency audit: **8,699 declarations, 12 opaque bodies**, reachable
  axioms `[propext, Quot.sound, Classical.choice]`, and
  `ROUTEB_DEPENDENCY_AUDIT_OK`. This audit ran on the clean direct compilation
  before Lake prepared its own build artifacts; these phases have separate logs.
- `comparator.log`: real upstream comparator replayed the Challenge build,
  then the cached exporter failed reading `Challenge.olean` with
  **`incompatible header`**. Comparator exit code **1**. Neither the statement
  match nor the nanoda/default-kernel replay was reached. There is no comparator
  success run or acceptance claim.
- `inputs.sha256`, `manifests.sha256`, `tools.sha256`, `compiled.sha256`,
  `input-stability.log`: frozen inputs, actual binary/object hashes, and
  successful post-attempt input stability checks.
- `project/`: the exact frozen sources and generated pinned Lake manifest.
  Its package link points to the existing WSL Mathlib cache.

Input SHA-256 values:

```text
Challenge.lean  cc4c4b531b9ac42d0be8b7152ec7dfa85e7dcc89f7cc6ecbfa4d965375a6f09d
Solution.lean   43835aa7aaeb5cb6f18e53527097d4dcab2d2f8137ac9762a3c36a34cfe685ae
DependencyAudit.lean  f774bc637296c6942bccbeca9161c7505536b02f6a5a515dc81875acb3560540
RouteBSupplyCore.lean 646c1052c10c1d8606342010c4303c0c25e40e008664ce7f1c1b1649c51f6971
comparator.json a16b29b152312bf3a094e1af62363e49bac56e3d98fd71c1e51c5de01ee134ea
```

## Exact environment gap

The project uses installed Lean **4.33.1**, with Mathlib commit
`0df444a360eaa60ab8c11dca51a86af692955474` in `/home/z5242/sos_lean`.
The available exporter in `/home/z5242/.cache/lean-ci-tools/lean4export/`
declares **Lean 4.32.0**, source commit
`4e7915201d3f9f04470d9eae002fa695f7cdc589`. Its actual binary hash is
`e57369980b0b81228580ce08066fb9bd738e717e002673a143f4956d217266b0`.
It cannot read this project's 4.33.1 `.olean` header.

Actual comparator source pin: `575674928e239f5bc452aab72d1dd7b0f1326494`;
nanoda pin: `68d5ca9db226849b41a6fff59d796ff19d0a8840`;
landrun pin: `811cfff51ceaf3d9843708aa6d22e9b84ccac8b4`.
These are the pins from the existing upstream formal-math acceptance script.
The comparator binary itself was built with its own 4.34.0-rc1 toolchain;
the observed failure is in the separate 4.32.0 exporter reading a 4.33.1 object.

The remaining infrastructure requirement is an actual exporter compatible
with Lean 4.33.1. No such exporter was built or downloaded, following the
user's instruction to prioritize mathematics and stop rebuilding tools.

## Reproduction and retained failures

```powershell
wsl -d Ubuntu -- bash /mnt/c/Users/z5242/Desktop/重构版/工作流/examples/routeb_supply_core/verify_comparator.sh
```

The final script creates a fresh sidecar-only run, performs clean compilation
and the audit, prepares Lake traces, and invokes the actual comparator.
With the current default cached exporter it is expected to fail as above.
`ROUTEB_LEAN4EXPORT` can point to an existing compatible binary if the main
task later provides one. It does not rebuild or download tools. After the
user's stop instruction, the optional rebuild branch was removed; that
script-only simplification received a shell syntax check, not another
comparator run. The final attempt preserves its exact earlier script snapshot.

Earlier runs remain separate and are not presented as successes:

- `comparator-cached-exporter-zmerjF2E`: early preflight stopped at unavailable
  `jq`, before input freezing; the script now uses standard-library JSON.
- `comparator-cached-exporter-PF7Ms4p7`: frozen inputs and successful theorem
  compiles; dependency-audit counter required an explicit `Nat` annotation.
- `comparator-cached-exporter-LBe5kCWE`: clean compilation/audit passed;
  comparator's sandbox could not delete a direct-compiler output on `/mnt/c`.
  Preparing real Lake traces resolved this in the final attempt.
- `comparator-local-exporter-SfoubkK0`: clean compilation/audit passed, then
  deliberately interrupted after the user's priority change, before exporter
  extraction/build or comparator execution. Its shell trap printed exit 0
  during termination; **that footer is not acceptance**. See its cancellation note.

No workflow src/state, target repository, historical report/hash, or residual
power directory was changed. Source-to-DH/Float64 binding obligations remain
those in `README.md`; this step only packages the already proved supply core.
