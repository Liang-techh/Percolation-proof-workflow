# GH-LEAN-FLT-QUOTIENT-CLM-COMPARATOR-HANDOFF

Status: OPEN_UNCOMPILED / external_catalog_pending. This packet has not run
Lean/Lake locally or remotely. Execute only in the next separately authorized
GitHub Lean job. Do not mutate source candidates, registry/state or shared adapters.

## Immutable inputs

Candidate repository checkout inspected before inventory:
`8fd0f132c2e4cf4ac99438aa8dc295a7f6592b1b`.
Both existing input files are tracked there. Overlay them at package root:

| Filename | Git blob | SHA-256 of inspected bytes |
|---|---|---|
| NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean | eeaf00791c7786e7e2ad8779e8d61f27a7574025 | 777d4ae6cd3fa60fb0f988f5b1e263e2cb07536f7ed83113f99aa102615e9e97 |
| NEW_QUOTIENT_CLM_API_Probe20260908.lean | d3968f99dcc65d7bbd802dc719f591eb5a99c5ae | 159ddb493ca734675fc6f211e021ca05addb3cb442e6dab5ef71e7c6bd8c936b |

Source repository: https://github.com/anthropics/fermats-last-theorem
at `aa2d8b34692b16c70f699536de0d8e75b9a3e9ef`, path
`Definitions/Def_Mathlib_Topology_Algebra_Module_Quotient.lean`.
Git blob `eab66288efedd1e634203abb927805413a716aa7`; 2014 bytes;
raw Git blob SHA-256 `a8c1204b32f3b539ef31d59190ae195cc802bfa453e18e53eaea565898ebb4e2`.
This SHA was computed from git cat-file's byte stream, not newline-normalized text.

Source Lean pin recorded in intake: v4.33.1; source Mathlib
`db584cd6d46c92f209a44c0f1c829460d327499d`.
Target Lean: `leanprover/lean4:v4.33.1`; target Mathlib:
`0df444a360eaa60ab8c11dca51a86af692955474`.
Never substitute target pin for upstream provenance. No upstream build is implied.

Preserve Apache-2.0 LICENSE/NOTICE/ATTRIBUTION.md from the intake. The source is
Imperial College London FLT staging `FLT/Mathlib/Topology/Algebra/Module/Quotient.lean`,
copyright 2025 Salvatore Mercuri; authors Salvatore Mercuri, Kevin Buzzard,
Pietro Monticone. Preserve the candidate's adaptation notice. No number theory
or P2M project is required for the target build.

## Complete static import inventory, not an elaborator receipt

`NEW_COMPARATOR_HANDOFF_Closure20260908.json` contains 2877 reachable source
modules, each encoded as `root|module|sha256`, plus the full Mathlib dependency
lock and digest of the reconstructed edge graph. Root labels are overlay,
mathlib, lean, and package:<name>. Paths are module dots replaced with slashes
plus .lean. Lean root is the installed v4.33.1 source root containing Init.lean.
Package roots are the locked Mathlib .lake/packages/<name> directories.

The read-only PowerShell 7 script `NEW_COMPARATOR_HANDOFF_Inventory20260908.ps1`
recursively walks header imports, including public/private/meta imports and
implicit Init unless prelude. With -Compact it emits the saved index format;
without it it emits full edges. It never invokes Lean/Lake or writes files.
The full JSON graph digest is over UTF-8 of its compact serialized output.

Local static run: missing=[], ambiguous=[], unparsed=[]; all eight dependency
checkout HEADs matched the embedded locked revisions. This is the full closure
according to this header scanner, not a claim of Lean-parser equivalence.
The scanner strips comments lexically and stops at the first non-header line;
runner MUST reconcile it against the compiler's actual import resolution and
record any additions/overrides. Embedded JS imports are deliberately excluded.
Files with unusual header syntax require manual classification, not silent omission.

Raw working-tree hashes may differ across EOL checkout policies. Reconcile by
Git blob identity plus documented byte normalization, then bind actual compiled
bytes; unexplained mismatch is rejection, not automatic normalization approval.

## Overlay layout and executable entry points

```text
isolated-quotient-clm/
  lean-toolchain                    # v4.33.1
  lakefile.toml                     # exact git requirement on target Mathlib SHA
  lake-manifest.json                # resolved, pinned dependencies
  NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
  NEW_QUOTIENT_CLM_API_Probe20260908.lean
  provenance/{LICENSE,NOTICE,ATTRIBUTION.md,source.lean,source-manifest.json}
  packet/NEW_COMPARATOR_HANDOFF_*
  out/                              # new OLean only
  logs/
```

Use a fresh isolated package, not the local path-based historical lakefile.
Pin actions to immutable SHAs; obtain Mathlib cache/build artifacts only for
the exact lock. Audit existing cache identity; never import stale local OLean.
Create out/logs in that isolated directory; add out to LEAN_PATH while retaining
Lake's dependency paths and record the final search order.

Inventory entry (PowerShell 7; output capture is the runner's responsibility):

```powershell
pwsh -NoProfile -File packet/NEW_COMPARATOR_HANDOFF_Inventory20260908.ps1 -CandidateDirectory . -MathlibDirectory .lake/packages/mathlib -LeanSourceDirectory <pinned-Lean-source-root> -Compact
```

The angle-bracket argument must be resolved from the pinned toolchain install,
not passed literally. Full edge inventory uses the same command without -Compact.
Then run only the two target modules:

```text
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_REPAIR_20260908.olean NEW_QUOTIENT_CLM_API_REPAIR_20260908.lean
lake env lean -DwarningAsError=true -o out/NEW_QUOTIENT_CLM_API_Probe20260908.olean NEW_QUOTIENT_CLM_API_Probe20260908.lean
```

The second command must resolve the first command's newly generated OLean.
If the fresh package stores transitive dependencies at a different root from
Mathlib's .lake/packages, reproduce the locked source layout or adapt only the
isolated inventory root mapping and record that change. Do not omit packages.

## Type/API checks and comparator seam

Map upstream Submodule.Quotient.continuousLinearEquiv to
FLTQuotientCLMAPIRepair.quotientContinuousLinearEquiv; map upstream
Submodule.quotientPiContinuousLinearEquiv to the analogous renamed definition.
The probe's explicit type wrappers and #check @ outputs check target typing;
they are NOT a cross-pin source comparator or concrete quotient-domain witness.

First definition: Ring R, G/H AddCommGroup/Module/TopologicalSpace, e continuous
linear equivalence, exact mapped-submodule equality. Second: CommRing R,
dependent component modules/topologies/topological additive groups, Fintype and
DecidableEq index, component submodules. Preserve every binder and conclusion.
No closedness, norm/isometry, positivity, dynamics or coverage follows.

Potential API failures: availability of convert tactic via the two imports,
quotientPi_aux.invFun unfolding, continuous_finsetSum typed arguments and
dependent Pi topology inference. Only propose a new separately named repair
after logging the exact failure; do not edit the old candidate or widen premises.

Comparator execution is a separate stage: select an approved comparator and
record its version/hash, two input statement identities, both pins, command,
exit and full log hashes. No compatible comparator is selected or executed by
this packet. If none is available, return COMPARATOR_MISSING after compile;
do not manufacture an acceptance line or conflate type wrappers with comparison.
If using a workflow requiring `Your solution is okay!`, require the actual exact
standalone output and exit 0, in addition to source/type binding.

## Receipt and failure disposition

Fill NEW_COMPARATOR_HANDOFF_ReceiptTemplate20260908.json with actual evidence,
never optimistic defaults. Include source/import/overlay hashes, runner/workflow
identity, Lean executable version, locks, every command/cwd/search path, OLean,
full axioms/sorry scan logs and comparator status. Recompute receipt digest only
after evidence is fixed, specifying canonicalization/self-hash exclusion rules.

| Failure | Classification / response |
|---|---|
| Toolchain/cache/import unavailable | ENVIRONMENT_BLOCKED; no mathematical refutation |
| Unexpected module root or unresolved static edge | IMPORT_CLOSURE_UNRESOLVED; stop admission |
| Pin/source/compiled byte mismatch | SOURCE_BINDING_REJECTED until explained/rebound |
| Definition/typeclass/tactic elaboration error | API_REPAIR_REQUIRED; preserve exact log |
| Timeout/heartbeat/OOM | RESOURCE_INCOMPLETE; not theorem failure |
| sorryAx or unapproved extra axiom | AXIOM_REJECTED; no compiled acceptance |
| Comparator missing/not run | COMPARATOR_MISSING; external catalog pending |
| Comparator statement mismatch | STATEMENT_REJECTED |
| All compile/audit checks pass, application absent | COMPILED_CANDIDATE_EXTERNAL_PENDING only |

Never update state/registry from this packet. Compilation, comparator, source
provenance and application admission remain separate statuses.
