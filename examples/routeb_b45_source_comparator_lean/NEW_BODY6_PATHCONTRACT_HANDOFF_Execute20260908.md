# BODY6 SixthColumnPathContract execution packet

OPEN_UNCOMPILED / pending. No local or remote Lean/Lake execution occurred.
Only new handoff files and an inbox review are supplied; old candidate/probe,
state/registry/shared adapters remain unchanged. Next GitHub job only, subject
to its execution authorization; no workflow is launched by this packet.

## Pins and source identity

Use repository commit b4f4f35093c375615dfe024cb40bf51ee70a07b1 as the source
snapshot. Candidate and probe are tracked at that commit:

```text
NEW_PATHCONTRACT_REASSIGNED_20260908.lean
git blob: 2df69ad00eb64c96e125a0d0fa874ecfaaf72b6a
sha256: ff5e2dfbcf0375d96cce232c739e0098381ce5b1828f7142dae23ac3e86a68fc
NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean
git blob: ac66feeb5b78ea82654edcd264d091b67e8471c8
sha256: 78cd395e47fc5edc7e781ba1574562ddcb8fa41135c0c3e8613cdcbfd7e98206
```

Target Lean=leanprover/lean4:v4.32.0, target Mathlib=
81a5d257c8e410db227a6665ed08f64fea08e997. These pins were read from current
examples/local_fkg toolchain/manifest; not confirmed by executing Lean.
Do not mix with the unrelated FLT lane's 4.33.1/0df444... environment.
The project source pin is not a physical DH runtime or CSV provenance witness.

## Import manifest and overlay

NEW_BODY6_PATHCONTRACT_HANDOFF_Inputs20260908.json records all 16 statically
resolved project modules, original paths, SHA256, direct imports and a topological
compile order. No ambiguous/unresolved project modules were found. It stops at
Mathlib; the full pinned Mathlib/Lean/dependency closure must be resolved and
recorded by the runner, not treated as 16 modules total.

The scan used anchored project import lines, not a Lean parser. Reconcile with
actual imports; no unknown override or same-name stale OLean is permitted.
The candidate imports canonical targets, not the AXIS/STEP6 source witness chain.
Thus compiling these 16 modules will NOT prove the sixth-column sourceIdentity
instance from those other candidates.

```text
isolated-body6-pathcontract/
  lean-toolchain             # v4.32.0
  lakefile.toml              # exact git Mathlib requirement, not local path dependency
  lake-manifest.json         # resolved and retained by runner
  <16 project modules>.lean  # original bytes, flat names from manifest
  packet/NEW_BODY6_PATHCONTRACT_HANDOFF_*
  provenance/source-manifest.json
  out/                      # fresh project OLean
  logs/
```

Do not copy local_fkg's unrelated PercolationContinuity path dependency.
In the isolated job, prepare exact-pin Mathlib cache/build, lock actions to
immutable SHAs, create out/logs and add out to LEAN_PATH while preserving the
Lake dependency paths. Record the resolved search order and actual source bytes.
EOL changes require explicit Git-blob/byte reconciliation, not silent acceptance.

Compile each module in project_compile_order using the same command form:

```text
lake env lean -DwarningAsError=true -o out/<Module>.olean <Module>.lean
```

The final two commands are exactly:

```text
lake env lean -DwarningAsError=true -o out/NEW_PATHCONTRACT_REASSIGNED_20260908.olean NEW_PATHCONTRACT_REASSIGNED_20260908.lean
lake env lean -DwarningAsError=true -o out/NEW_PATHCONTRACT_REASSIGNED_Probe20260908.olean NEW_PATHCONTRACT_REASSIGNED_Probe20260908.lean
```

This is an execution plan, not a claim these commands ran. Source directories
alone do not satisfy imported OLean dependencies. Do not run whole-workspace
builds or change old files to make the probe pass.

## Probe/type/API boundaries

Probe checks the structure/fields, (5:Fin6).val and explicit Fin constructors,
then consumes the original cap theorem under an explicit contract hypothesis h.
It prints the two original theorem definitions and axioms plus wrapper axioms.
Check implicit X/Physical arguments, sourceIdentity q inference and the Eq rewrite.
Fin numeral 5 is body6/column6 only after the source indexing convention is bound;
Fin typing does not validate external one-based raw CSV indices.

The contract's projection/inclusion/physicalIdentity/sourceIdentity/canonicalCap
all share embed,qOf,domain,Omega,path,rows,physicalRow,cap. None is constructed by
the probe. There is no physical inhabitant, trajectory, source receipt or new cap
constant. Canonical rational-valued rows are not reversible raw body/coefficient
labels; raw provenance requires a separate list/index/coefficient binding.

## Mandatory receipt fields and failure classes

Record separately:

1. execution: repository/checkout/overlay hashes, workflow/actions/run/job/attempt,
   runner/time, actual Lean --version, Mathlib revision and every resolved lock.
2. imports: 16 project source/OLean hashes, full actual Mathlib/Lean dependency
   resolution, cache identity, source overrides and static-vs-compiler reconciliation.
3. compile: each command/cwd/search path/exit, full stdout/stderr URL/hash, fresh
   OLean hashes; do not accept a later probe if an earlier dependency failed.
4. audits: exact original theorem and wrapper types; #print axioms outputs;
   sorry/admit/sorryAx and unapproved explicit axiom findings in the relevant
   closure. Text scan alone cannot discharge the axiom gate.
5. comparator: approved tool/version/hash, statement/source pairs, exact command,
   pin/method, exit/log/output hashes. If unavailable, mark MISSING, not accepted;
   type wrappers are not a comparator. A protocol acceptance line must be actual
   output, never supplied by this template.
6. source/application: hashes and accepted witnesses for all five concrete
   fields; q projection, physical row implementation, fixed Omega/domain/path,
   authoritative raw rows and cap evidence. Missing instances stay missing even
   when the generic seam compiles.

Classify environment/import absence as BLOCKED, API elaboration as REPAIR_REQUIRED,
resource exhaustion as INCOMPLETE, source/hash/type mismatch as REJECTED, sorryAx
or unapproved axioms as AXIOM_REJECTED, absent comparator as COMPARATOR_MISSING.
No mathematical impossibility follows from infrastructure failure. Successful
generic compile permits compiled_candidate/pending only, never VERIFIED or
physical admission. No registry/state mutation is authorized.
