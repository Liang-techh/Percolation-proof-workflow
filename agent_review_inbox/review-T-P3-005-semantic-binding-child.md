---
kind: review_result
task_id: T-P3-005
source_agent: Codex
integration_status: pending
---

# T-P3-005 semantic-binding child review for Route-B P3

## Scope

Read-only bounded review only. I inspected the Route-B true-DH side in
`6dof_sos_optimized`, the export-side dynamics semantics manifest, the current
source-binding snapshot/report material, and the existing Lean/checker adapter
for P3. I did not run a full repo search, did not change StateStore/registry,
and did not modify any existing file.

## What is canonical source versus provenance

The canonical Julia/DH source for the P3 bottleneck is the Route-B dense DH
port:

- `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\dhport_lib.jl`

The source-side semantics are stated explicitly in:

- `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\DYNAMICS_SEMANTICS.md`
- `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\routeB_dense_Mq\routeB_export_manifest.toml`

That manifest is useful provenance, not a proof. It records:

- `mass_regularizer = 1.0e-6`
- `coriolis_gravity_fd_step = 1.0e-5`
- `dynamics_semantics = "DH-chain M with explicit mass regularizer; C/G central finite differences"`

The current source-binding audit material in `examples/routeb_source_binding_audit`
and the earlier P3 reviews agree on the same provenance bundle and the same
14-state order `q1..q6, v1..v6, w, c`. That alignment is necessary, but it
does not by itself establish semantic equivalence between source and checker.

## Existing source snapshots and checker adapter

The existing exact snapshot bundle is in:

- `C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_source_binding_audit\snapshots\current_exact\reference.json`
- `C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_source_binding_audit\snapshots\current_exact\ReferenceMass.lean`
- `C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_source_binding_audit\snapshots\current_exact\PotentialSlice.lean`
- `C:\Users\z5242\Desktop\重构版\工作流\examples\routeb_source_binding_audit\snapshots\current_exact\ChristoffelPower.lean`

The Lean/checker adapter currently lives in:

- `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\artifacts\task_FLT_p3_source_binding_20260908\FLT_P3_SourceBinding.lean`
- `C:\Users\z5242\Desktop\重构版\6dof_sos_optimized\6dof_sos_optimized\artifacts\task_FLT_p3_source_binding_20260908\AxiomAudit.lean`

That adapter is intentionally abstract. It proves a generic centered-finite-difference
bridge and a generic “exact trueDH derivative lies in an inflated interval”
statement, but it does not define the six-joint DH program, IEEE-754 execution,
or a concrete Route-B source-binding theorem.

## Minimal child theorem/interface

The smallest child theorem I can defend for P3 is not “hash equality implies
semantic equality”. It should be a premise-driven interface that keeps
provenance and semantics separate:

`RouteBTrueDHSourceBindingChild`

Inputs:

- `source_root : Path` for the canonical `routeB_dense_Mq` source tree
- `manifest : routeB-export-manifest.toml`-style metadata
- `snapshot : reference.json`-style exact snapshot metadata
- `source_hashes : list of relative path + lowercase SHA-256 entries`
- `lean_adapter : FLTP3SourceBinding`-style theorem package
- `trueDH : E → ι → ℝ`
- `DtrueDH : E → ι → E →L[ℝ] ℝ`
- `A : ι → E →L[ℝ] ℝ`
- `sourceExact : ι → ℝ`
- `sourceRun : ι → ℝ`
- `payload : RationalIntervalFamily ι`
- `x v : E`
- `h : ℝ`

Outputs:

- a checked interval claim of the form
  `|DtrueDH x i v - payload.center i| ≤ payload.radius i + roundingRadius i + derivativeRadius i * ‖v‖`
- a separate provenance verdict saying only that the declared source files match
  their hashes under `source_root`

Necessary assumptions:

- the state order is exactly `q1..q6, v1..v6, w, c`
- the manifest semantics string is exactly the DH-chain / regularizer / central-FD contract
- the exact snapshot and manifest agree on the same `mass_regularizer` and `fd_step`
- the Lean adapter only speaks about exact-real semantics and interval enclosure
- `sourceExact i = centralFD trueDH x v h i`
- `sourceRun` is a runtime or exported value with a separate rounding bound
- the source-hash layer is evidence-only and does not imply semantic equivalence

What this child theorem should not claim:

- it should not claim that a SHA-256 match proves the DH equations are identical
- it should not claim `Float64` execution equals exact rational reconstruction
- it should not upgrade empirical export artifacts into a global Route-B proof
- it should not resolve the full P3 physical/global interval domain on its own

## Why this is the right semantic boundary for P3

The current Route-B evidence stack already separates three layers:

1. canonical source provenance, via hashes and manifest fields;
2. exact snapshot reconstruction, via `reference.json` and the Lean sidecars;
3. semantic enclosure, via the abstract `FLTP3SourceBinding` theorem package.

The missing piece is a child theorem that composes those layers without collapsing
them into one another. In particular, the theorem should bind a concrete
`trueDH` semantics to a checker-side interval claim, while leaving the source
hashes as provenance only.

That is the smallest credible semantic-binding interface for the current P3
bottleneck.

## Unmet physical and global boundaries

The current evidence still does not satisfy:

- a global P3 interval/domain proof over the full routeB box;
- a proof that the deployed Julia/DH execution was replayed under the same
  runtime/IEEE-754 semantics;
- a proof that the full physical DH identification is globally correct;
- a proof that the exact snapshot is the same thing as the live execution;
- a proof that the source hashes alone entail semantic equality.

These remain open even if the provenance bundle is perfect.

## Lightweight focused checks that fit the current environment

The following checks are small enough to run locally without broad search or
state changes:

1. Recompute the SHA-256 of only the canonical source and the two manifest files
   above, then compare them to the recorded hashes in the current exact snapshot
   and audit files.
2. Check that the source-path set is minimal and relative, and that it stays
   inside the declared `routeB_dense_Mq` root.
3. Compare the declared `mass_regularizer`, `fd_step`, and `dynamics_semantics`
   strings across the manifest, the audit report, and the exact snapshot.
4. Verify that the Lean adapter still only depends on the abstract
   `HasFDerivWithinAt`/centered-FD bridge and does not silently introduce a
   concrete DH execution claim.
5. Sanity-check the exact snapshot fields `Lean_compiled=false`,
   `physical_DH_identification_proved=false`, and `Float64_binding_proved=false`
   so the review stays fail-closed.

## Conclusion

The review result is still `pending`, but the minimal child theorem/interface is
clear: provenance must remain a separate input from semantic enclosure, and the
first admissible theorem for P3 should only bind concrete true-DH semantics to a
checker-side interval claim under explicit assumptions.
