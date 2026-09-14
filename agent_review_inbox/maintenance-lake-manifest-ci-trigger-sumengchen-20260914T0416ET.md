kind: maintenance_log
review_id: maintenance-lake-manifest-ci-trigger-sumengchen-20260914T0416ET
source_agent: 苏梦辰
created_at: 2026-09-14T04:16:00-04:00
inspected_branch: main
inspected_head_before: c0716c42cf21d5531484edb4963f796a21fb1f28
maintenance_commit: b343cb83d749be203555ee3441b55ba53c1a291b
admission: pending

# Lean sidecar lockfile trigger coverage

## Repository-level issue

The `Lean agent sidecars` workflow already treated `examples/**/lean-toolchain`,
`lakefile.lean`, and `lakefile.toml` as CI-relevant, but omitted
`examples/**/lake-manifest.json` from both `push.paths` and
`pull_request.paths`.

This is a build/reproducibility gap because the pinned local-FKG environment is
materialized from `examples/local_fkg/lake-manifest.json`; a lockfile-only
revision could therefore change the dependency graph without scheduling the
portable sidecar CI that is supposed to validate that pinned environment.

## Change

Modified only:

- `.github/workflows/lean-agent-sidecars.yml`

Added `examples/**/lake-manifest.json` to the `push` and `pull_request` path
filters. No theorem source, verifier gate, warning/error policy, axiom audit,
toolchain version, or dependency revision was changed.

Commit:

- `b343cb83d749be203555ee3441b55ba53c1a291b` — `ci: trigger Lean sidecars on lake manifest changes`

## Actions evidence

Latest completed pre-change Lean sidecar run inspected:

- run `34722213604`
- job `103630057451` (`portable-sidecars`)
- environment/bootstrap steps 2-9: success
- step 10 `Run portable agent sidecars`: failure, command block exited nonzero
  because one or more theorem/proof sidecars failed; this was not a toolchain,
  checkout, Elan, Lake bootstrap, or Mathlib compatibility bootstrap failure.
- steps 11-12 (`Record Lean/Lake versions`, artifact upload): success

The maintenance commit itself scheduled fresh CI as expected:

- `Lean agent sidecars` run `34821735766`, job `103904629136`: queued at the
  time of this log; no step/exit code exists yet, so no green result is claimed.
- `Workflow tests, Harris replay, and local-FKG verification` run
  `34821735792`: also queued from the same commit.

## Reproduction / validation

Path-trigger validation is now structural: any future commit that changes an
`examples/**/lake-manifest.json` file matches the same workflow path filter as
changes to the corresponding toolchain/lakefile.

For the build itself, the workflow continues to execute the existing pinned
bootstrap:

```bash
cd examples/local_fkg
lake --version
lake update
lake build
```

and then the unchanged portable verifier aggregation over `CI_PORTABLE=1`
`verify.sh` scripts.

## Remaining failures / routing

No new repository-level dependency/PATH/module-resolution blocker was observed
in the latest completed run. The aggregate portable-sidecars workflow may stay
red until the remaining Lean proof/type/linter failures are repaired by their
own owners; this maintenance change does not weaken or bypass those failures.
In particular, previously routed proof work such as T-P5-112 remains outside
this repository-maintenance lane when already owned by 巨阳仙尊.

Repository runnability is not a proof-completion claim. Final integration and
mathematical status remain with 梁智炜（Codex）.
