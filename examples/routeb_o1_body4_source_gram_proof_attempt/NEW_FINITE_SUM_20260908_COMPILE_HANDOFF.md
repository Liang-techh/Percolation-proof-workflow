# NEW pinned compile handoff — Body4 finite sum

Task: GH-LEAN-BODY4-FINITE-SUM-RECEIPT-HANDOFF.
Status: NOT_RUN; admission=pending. Commands below are for the GitHub Lean agent only.
No GitHub dispatch, local Lean/Lake execution, or successful compilation is asserted.

## Immutable inputs and dependency closure

Use paired `NEW_FINITE_SUM_20260908_COMPILE_HANDOFF.json` as the authoritative
ordered input/hash manifest. Direct candidate import is RouteBO1Body4SourceGramTargets.
All 15 repository dependencies plus the candidate, in build order:

1. FourierNormalForm — imports: Mathlib
2. FrameRecursion — imports: FourierNormalForm
3. RealDHStep — imports: FrameRecursion
4. FrameOriginAxis — imports: RealDHStep
5. FramePrefixIndex — imports: FrameOriginAxis
6. FrameSlotAccessor — imports: FramePrefixIndex
7. BodySemanticCore — imports: Mathlib
8. BodyContractCore — imports: BodySemanticCore
9. SourceContractAdapter — imports: FrameSlotAccessor, BodyContractCore
10. SourceBodyMassExtensionalProbe — imports: SourceContractAdapter
11. SourceContractIndexAdapter — imports: SourceContractAdapter
12. RouteBO1PerBodyExactSource — imports: SourceBodyMassExtensionalProbe, SourceContractIndexAdapter, Mathlib
13. BodyTraceEvaluator — imports: Mathlib
14. RouteBO1PerBodyTraceAdapter — imports: RouteBO1PerBodyExactSource, BodyTraceEvaluator
15. RouteBO1Body4SourceGramTargets — imports: RouteBO1PerBodyTraceAdapter, SourceContractIndexAdapter
16. NEW_FINITE_SUM_20260908_STEP3_TRANSLATION — imports: RouteBO1Body4SourceGramTargets

The JSON binds every path and SHA-256. Do not substitute an older run-directory olean.
Mathlib is the external root; its complete external closure is pinned by its commit and
committed lake-manifest.json plus the Lean distribution. This handoff does not falsely
claim to have enumerated or checked every Mathlib transitive file. The remote receipt
must record the actual external package revisions/lock hash and build-root provenance.

Pin: Lean `leanprover/lean4:v4.33.1`, commit
`819816b2e0a3bf405af45ae5c7af2491d8f5bee6`; Mathlib
`0df444a360eaa60ab8c11dca51a86af692955474`.
These are the historical accessor/comparator pins, not a claim that this candidate
works with them. Abort on an incompatible mathlib lean-toolchain; no automatic upgrade.
Do not use local_fkg (different pin), workflow-wide lake update, or mixed cached oleans.

## Remote execution recipe

Run only in a new isolated Linux runner. Set REPO to an absolute read-only checkout
containing ALL hash-matched manifest inputs, including the candidate that may not be
in the observed commit. Record both actual checkout HEAD and the manifest hash.
Do not edit the candidate or its dependencies to obtain a pass; report the first failure.

```bash
set -euo pipefail
: "${REPO:?absolute source checkout required}"
REPO=$(realpath "$REPO")
HANDOFF="$REPO/examples/routeb_o1_body4_source_gram_proof_attempt/NEW_FINITE_SUM_20260908_COMPILE_HANDOFF.json"
RUN=$(mktemp -d)
export REPO HANDOFF RUN
mkdir -p "$RUN/src" "$RUN/logs"
git -C "$REPO" rev-parse HEAD > "$RUN/repo-head.txt"
sha256sum "$HANDOFF" > "$RUN/handoff.sha256"
python3 - <<'PY'
import hashlib, json, os, pathlib, shutil
root = pathlib.Path(os.environ["REPO"])
run = pathlib.Path(os.environ["RUN"])
m = json.loads(pathlib.Path(os.environ["HANDOFF"]).read_text())
for item in m["repo_modules_topological"] + m["snapshots"]:
    p = root / item["path"]
    got = hashlib.sha256(p.read_bytes()).hexdigest()
    if got.lower() != item["sha256"].lower():
        raise SystemExit("INPUT_HASH_MISMATCH: " + item["path"])
for item in m["repo_modules_topological"]:
    shutil.copyfile(root / item["path"], run / "src" / (item["module"] + ".lean"))
(run / "modules.txt").write_text("".join(x["module"]+"\n" for x in m["repo_modules_topological"]))
shutil.copyfile(os.environ["HANDOFF"], run / "input-manifest.json")
PY
git clone https://github.com/leanprover-community/mathlib4.git "$RUN/mathlib"
git -C "$RUN/mathlib" checkout --detach 0df444a360eaa60ab8c11dca51a86af692955474
cd "$RUN/mathlib"
test "$(git rev-parse HEAD)" = 0df444a360eaa60ab8c11dca51a86af692955474
test "$(tr -d '\r\n' < lean-toolchain)" = leanprover/lean4:v4.33.1
# Elan must be installed by a checksum-verified runner bootstrap, not assumed from this handoff.
elan toolchain install leanprover/lean4:v4.33.1
lake env lean --version > "$RUN/logs/lean-version.log"
grep -F 819816b2e0a3bf405af45ae5c7af2491d8f5bee6 "$RUN/logs/lean-version.log"
sha256sum lean-toolchain lake-manifest.json > "$RUN/external-lock-before.sha256"
# Capture stdout/stderr and exit codes for EACH of these setup commands in the receipt.
# No lake update. If package resolution rewrites the lockfile, fail and stop.
timeout 1800 lake exe cache get > "$RUN/logs/cache.log" 2>&1
timeout 1800 lake build Mathlib > "$RUN/logs/mathlib-build.log" 2>&1
sha256sum --check "$RUN/external-lock-before.sha256"
git diff --exit-code -- lean-toolchain lake-manifest.json
lake env printenv LEAN_PATH > "$RUN/external-lean-path.txt"
lake env sh -c 'command -v lean' > "$RUN/lean-binary-path.txt"
sha256sum "$(cat "$RUN/lean-binary-path.txt")" > "$RUN/lean-binary.sha256"
```

Before compilation, scan staged repository sources (including comments) for sorry/admit,
unsafe, axiom/opaque declaration or trust-setting candidates. A textual flag is not
automatically a kernel failure: inspect and record line, context and disposition.
Never silently suppress a flag. No build should proceed with unresolved trust flags.
Retain the scan output and its hash. Do not treat scan exit=1 (no rg matches) as an error.
If rg is unavailable record that and use an equivalent explicit scanner.

The agent must create this additional audit module ONLY inside RUN/src, not in the repo:

```lean
import NEW_FINITE_SUM_20260908_STEP3_TRANSLATION
set_option autoImplicit false
namespace RouteBO1Body4FiniteSumReceiptAudit
theorem exact_endpoint :
    RouteBO1Body4SourceGramTargets.Body4Slot4TranslationTarget :=
  RouteBO1Body4FiniteSum20260908.slot4_translation_attempt
#print exact_endpoint
#print axioms exact_endpoint
#print axioms RouteBO1Body4FiniteSum20260908.step3_column
#print axioms RouteBO1Body4FiniteSum20260908.slot4_product
#print axioms RouteBO1Body4FiniteSum20260908.product_column_four_terms
#print axioms RouteBO1Body4FiniteSum20260908.source_row_four_terms
#print axioms RouteBO1Body4FiniteSum20260908.source_row_translation
#print axioms RouteBO1Body4FiniteSum20260908.spatial_translation_fields
#print axioms RouteBO1Body4FiniteSum20260908.slot4_translation_attempt
end RouteBO1Body4FiniteSumReceiptAudit
```

Name it `NEW_FINITE_SUM_RECEIPT_AUDIT.lean` and hash its bytes before compilation.
This makes source_row_translation explicit too (the candidate's own print list omits it).
The audit validates the original target type, not a merely similarly named statement.

Compile from the pinned mathlib directory. Stage sources are flat because every local
module uses a unique unqualified module name; src is the only repository olean root.
Use the freshly generated external LEAN_PATH from this same Lake environment.

```bash
EXTERNAL_LEAN_PATH=$(cat "$RUN/external-lean-path.txt")
export LEAN_PATH="$RUN/src:$EXTERNAL_LEAN_PATH"
while IFS= read -r module; do
  budget=300
  test "$module" != NEW_FINITE_SUM_20260908_STEP3_TRANSLATION || budget=120
  set +e
  lake env lean --version > "$RUN/logs/$module.version.log" 2>&1
  env LEAN_PATH="$LEAN_PATH" timeout "$budget" "$(cat "$RUN/lean-binary-path.txt")" \
    -DwarningAsError=true --root="$RUN/src" \
    -o "$RUN/src/$module.olean" "$RUN/src/$module.lean" \
    > "$RUN/logs/$module.log" 2>&1
  code=$?
  set -e
  printf '%s\n' "$code" > "$RUN/logs/$module.exit"
  test "$code" -eq 0 || exit "$code"
  test -s "$RUN/src/$module.olean"
  sha256sum "$RUN/src/$module.lean" "$RUN/src/$module.olean" > "$RUN/logs/$module.sha256"
done < "$RUN/modules.txt"
set +e
env LEAN_PATH="$LEAN_PATH" timeout 120 "$(cat "$RUN/lean-binary-path.txt")" \
  -DwarningAsError=true --root="$RUN/src" \
  -o "$RUN/src/NEW_FINITE_SUM_RECEIPT_AUDIT.olean" "$RUN/src/NEW_FINITE_SUM_RECEIPT_AUDIT.lean" \
  > "$RUN/logs/axiom-audit.log" 2>&1
audit_code=$?
set -e
printf '%s\n' "$audit_code" > "$RUN/logs/axiom-audit.exit"
test "$audit_code" -eq 0
sha256sum "$RUN/src/NEW_FINITE_SUM_RECEIPT_AUDIT.lean" \
  "$RUN/src/NEW_FINITE_SUM_RECEIPT_AUDIT.olean" "$RUN/logs/axiom-audit.log"
```

Capture setup failures with the same phase/exit-code discipline; set -e stopping a recipe
is NOT itself a complete receipt. Never mark an unattempted module as exit=0.
Keep RUN even on failure. Hash logs and surviving outputs; a partial olean is not accepted.
Do not retry unchanged timeouts indefinitely or increase budgets without reporting.

## Required receipt fields (actual run values, not defaults fabricated as success)

- task_id, run_id, start/end UTC, actual repo HEAD/dirty status, manifest/source hashes,
  actual argv/cwd/env/timeout per phase and runner OS/architecture.
- Lean requested/actual version and commit, binary SHA-256; Mathlib requested/actual SHA,
  clean status, lean-toolchain hash, lake-manifest hash before/after; all resolved external
  package revisions and actual library roots/cache provenance.
- For every ordered repo module: direct imports, source path/hash before/after, command,
  compile attempted boolean, exit_code (null if not run), wall time, log path/hash,
  olean exists/hash, and whether its inputs match this manifest. No old olean reuse.
- Audit module source/olean/log hashes and exit code; full printed endpoint statement;
  full axiom sets for each of the seven candidate declarations and exact_endpoint.
- sorry audit scope, scanner/command/output hash, each flagged line/disposition,
  sorryAx occurrence list, custom axioms list, and unresolved trust-setting findings.
  Allowed axiom set is a SUBSET of {propext, Classical.choice, Quot.sound};
  none/smaller is fine. sorryAx or any unapproved custom axiom fails.
  Exit=0 alone does not establish absence of sorryAx.
- failure_phase, failure_class, first diagnostic, blocked dependent modules;
  compile_status separate from source_binding/admission.
- Per artifact receipt hash inventory. For receipt integrity use a detached SHA-256 file
  computed after finalizing receipt bytes, not an impossible self-referential hash field.
- Successful maximal status: COMPILED_CANDIDATE_PENDING_REVIEW. admission=pending,
  registry_promoted=false, frame_handoff_closed=false, runtime_binding_proven=false.
  No comparator was run; record comparator status NOT_RUN, not a fabricated acceptance.

## Failure taxonomy

| Class | Meaning / stop rule |
|---|---|
| INPUT_HASH_MISMATCH | Any candidate/dependency/snapshot differs; stop before compile |
| ENV_PIN_MISMATCH | Toolchain, Mathlib, package lock or cache identity mismatch |
| EXTERNAL_DEPENDENCY_UNAVAILABLE | Network/cache/bootstrap/package unavailable; not theorem failure |
| IMPORT_CLOSURE_MISMATCH | Missing/ambiguous module, unexpected repo path or mixed olean root |
| SOURCE_RESTRICTION_FLAG | Unresolved sorry/admit/axiom/unsafe/trust-setting finding |
| DEPENDENCY_COMPILE_FAILED | One of the 15 imports fails; candidate remains NOT_RUN |
| CANDIDATE_COMPILE_FAILED | Imports succeed, candidate produces Lean diagnostics |
| TIMEOUT | timeout exit 124; record exact module and elapsed budget, no logical refutation |
| RESOURCE_FAILURE | OOM/signal/disk failure; retain runner evidence, no logical refutation |
| AXIOM_AUDIT_FAILED | Type/audit compile mismatch, sorryAx, unapproved axiom or missing report |
| RECEIPT_INCOMPLETE | Missing hashes/logs/exit codes/statement or external provenance |
| COMPILED_CANDIDATE_PENDING_REVIEW | All gates pass; never automatic registry or FRAME_HANDOFF closure |

Historical comparator status explicitly lacks a completed SourceBodyMassExtensionalProbe
receipt. This dependency may be the first blocker even though the finite sum is short.
Do not replace it, rewire the candidate import, or copy an unauthenticated olean to bypass it.
No GitHub workflow auto-dispatch is configured by these new documents.

