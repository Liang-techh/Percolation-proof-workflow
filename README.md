# Percolation proof workflow

Research prototype for the public `anthropics/formal-math` + Prove2Me style:

`target -> decomposition DAG -> open frontier -> attempts -> Lean check/repair -> registry -> comparator`

The implementation is an incomplete research prototype. The registry entry point is
`verification.verify_and_register`: it runs Lean and a coordinator-supplied pinned comparator,
checks source stability and closed dependencies, and records the evidence. There is no boolean-only
promotion API. The coordinator and its executable/config selection remain trusted; Python is not an
isolation boundary against proof agents. A successful build alone does not establish statement equivalence or absence of axioms.
The public percolation replay remains an audit/reference fixture; executable target runs are recorded
separately under `artifacts/` and are not promoted merely because source files compile.

## Layout

- `src/percolation_workflow/`: persistent state model and orchestration primitives
- `tests/`: deterministic DAG/frontier/registry tests
- `upstream/`: read-only reference checkouts of the public repositories

The Anthropic FLT intake is available as a read-only catalog pipeline. It
records the pinned commit, Lean/Mathlib versions, per-candidate source hashes,
classification (1 = direct reuse, 2 = light adaptation, 3 = architecture
only), and attribution without touching the theorem registry:

```powershell
python -m percolation_workflow.cli scan-flt `
  --target-root artifacts/anthropic_fermats_last_theorem `
  --snapshot-output output/anthropic_flt_snapshot.json

python -m percolation_workflow.cli project-flt-reuse `
  --catalog output/anthropic_flt_snapshot.json `
  --source-root artifacts/anthropic_fermats_last_theorem `
  --reuse-output output/anthropic_flt_advisory_projection.json
```

The projection is hash-bound and supports a read-only Git `HEAD:path` source
backend for no-checkout clones. It is explicitly advisory-only: it cannot
promote a theorem, close a Route-B node, or set `formal_certificate_allowed`.

Each target can provide a portable `verification-manifest.json` describing the exact
challenge/solution modules and frozen source set for every theorem. The Linux leaf
verifier consumes that manifest and the pinned dependency checkout. A host adapter can
write raw agent responses as callback envelopes and run one durable coordinator cycle:

```powershell
python -m percolation_workflow.cli host-cycle artifacts/local_fkg/state.json `
  --callback-dir artifacts/local_fkg/callbacks
```

An external Codex/provider adapter can validate and atomically enqueue one raw v1 result without
touching workflow state directly:

```powershell
python -m percolation_workflow.cli persist-callback artifacts/<target>/state.json `
  --result-file artifacts/<target>/provider-result.json `
  --callback-dir artifacts/<target>/callback-inbox
```

Version-1 callback envelopes carry `request_id`, `attempt_id`, `event_id`, `agent_id`,
and `payload`; a completed candidate may additionally provide validated `candidate.project`
and `candidate.source` paths. A completed decomposition agent may instead provide
`decomposition.sketch` and an ordered `decomposition.children` array; the coordinator writes
those child obligations into the DAG before sketch checking. The cycle ingests callbacks, starts the coordinator compiler,
collects published receipts, prepares the next dispatch batch, and prints `next_actions`; it
never fabricates an agent result or promotes a theorem without the Lean/comparator gates.

The generic controller is also available directly through the CLI; the bundle root defaults to
`verification.bundle_root` in the manifest:

```powershell
python -m percolation_workflow.cli verify-manifest artifacts/local_fkg/state.json `
  --manifest examples/local_fkg/verification-manifest.json `
  --dependency-project <pinned-dependency-checkout> `
  --comparator-tools <upstream-verifier-tools>
```

When a checked reduction proposal has all of its children in the verified registry, the controller
re-runs the reduction audit and closes the parent through a recorded reduction receipt. The root
still goes through the final full-project comparator and both kernel gates.

For a new target, an optional `research` section in the same manifest can initialize the durable
state and DAG without a target-specific bootstrap script:

```powershell
python -m percolation_workflow.cli init-manifest artifacts/<target>/state.json `
  --manifest examples/<target>/verification-manifest.json
```

Non-Lean research projects can be admitted through the fail-closed external
intake.  The Route-B adapter maps P0--P9 into the same persistent DAG, keeps
artifact hashes and checker receipts in the state, and uses
`evidence_complete` only for an explicitly scoped engineering/audit gate run
by its approved checker. That status can unlock an operational dependency,
but is never accepted by the Lean theorem registry. A successful diagnostic
for an unresolved mathematical statement remains `open`; its receipt is kept
and `next-actions` requests `decompose_external_obligation` instead of treating
`UNKNOWN` or partial coverage as a proof:

```powershell
python -m percolation_workflow.cli init-routeb-external `
  artifacts/routeb_6dof/state.json `
  --target-root C:\path\to\6dof_sos_optimized\6dof_sos_optimized

python -m percolation_workflow.cli run-external-gate `
  artifacts/routeb_6dof/state.json `
  --node-name P0.reproducibility_baseline
```

`run-external-gate` records the exact command, stdout/stderr, exit code and
before/after source snapshot.  A zero exit code with source drift or missing
artifacts remains open and is surfaced as repair work by `next-actions`.
Arbitrary override commands cannot close a stage. Stale closed ancestors block
dispatch; timeout partial output and manifest-reading failures remain in the
attempt history.
External numerical/SOS evidence therefore cannot silently become a
kernel-verified theorem.

When an adapter learns that an earlier intake tracked an incomplete artifact
scope, refresh it explicitly; source-content changes, expanded scopes and
inappropriate legacy mathematical closures reopen affected nodes and their
consumers. Receipts are retained in `previous_external_receipts`; refresh is
refused while an attempt is active:

```powershell
python -m percolation_workflow.cli refresh-routeb-external `
  artifacts/routeb_6dof/state.json
```

Route-B's current source-provenance correction is documented in
`artifacts/routeb_provenance_correction_20260905/REPORT.md`. Historical source
hashes were restored, not relabelled to make current checkers green. Re-run the
read-only audit into a **new** output directory:

```powershell
python scripts/audit_routeb_provenance.py --target-root C:\path\to\6dof_sos_optimized `
  --out artifacts/routeb-provenance-new-run --run-checker
```

`docs/routeb-block45-proof-sketch.md` separates the proposed mathematical DAG
from stage sequencing. `examples/routeb_supply_core` contains the isolated exact
quadratic supply proof; its compilation is not a complete physical certificate.

The current true-DH P4 frontier is intentionally split into small, independently
admissible obligations. From the workflow root, refresh the source-semantics
receipts with:

```powershell
$env:PYTHONPATH = 'src'
python scripts/record_routeb_controller_damping_audit.py
python scripts/record_routeb_true_dh_source_formula_audit.py
python scripts/record_routeb_evaluator_enclosure_decomposition.py
python scripts/record_routeb_exact_real_coefficient_identity_draft.py
python scripts/record_routeb_regularizer_semantics_draft.py
python scripts/check_routeb_o1_interface.py
python scripts/record_routeb_o1_interface_check.py
python scripts/record_routeb_child_reviews.py
python scripts/record_routeb_force_scale_contract.py
python scripts/record_routeb_fd_step_semantics.py
python scripts/record_routeb_dh_offset_semantics.py
python scripts/record_routeb_trig_shift_leaf.py
```

These recorders preserve the deployment authority (`robot_final/dhport_lib.jl`),
the exact port sign `R_port = -M_BD M_DD⁻¹ DeltaM_DB`, and the distinction between
the conditional exact-real O1 identity and the larger Float64 O2 enclosure. They
never promote a node or set `formal_certificate_allowed`; the O1 interface draft
is uncompiled until a pinned Lean agent supplies zero-sorry, axiom, comparator, and
source-binding receipts. `scripts/refresh_anthropic_advisory_overlay.py` refreshes
the non-authoritative FLT adapter sidecar against the current state hash without
adding authoritative DAG dependencies.

`record_routeb_child_reviews.py` is the fail-closed harvest step for completed
O0/O1/O2 static agent reports. It verifies report/source hashes, records the
mathematical decomposition and unresolved obligations on the corresponding DAG
nodes, and explicitly refuses registry or certificate admission. The O1
structural checker is likewise only an interface gate; it does not claim a Lean
compile.

`record_routeb_force_scale_contract.py` keeps the block projection honest by
scanning the selected deployed/lifted sources for requested force-scale terms
and recording an obstruction when they are absent. It does not infer a missing
coefficient from a nearby nominal coupling.

`record_routeb_fd_step_semantics.py` records the exact binary64 value of the
deployed `1e-5` finite-difference step and its outward interval relative to
the exact model `1/100000`; it does not claim that the complete `C/G` evaluator
has been enclosed.

`record_routeb_dh_offset_semantics.py` records the binary64 `π` and `π/2`
representations against explicit rational enclosures. It remains separate from
the stronger per-angle `sin`/`cos` libm enclosure required by O2.

`record_routeb_trig_shift_leaf.py` imports the existing exact rational Taylor
leaf for `sin(1/100000)` and `cos(1/100000)`. It preserves the leaf as an
advisory artifact until its relationship to deployed Float64/libm evaluation
is proven.

The O1 API audit also emits
`artifacts/task_routeb_o1_lean_api_audit_20260907/RouteBO1PortIdentity.lean`.
It is a no-`sorry`/no-`admit` compilation target for the remote Lean agent, not
a compile receipt or registry entry.

After an agent returns a decomposition, the same generic state can accept it with
`propose-decomposition`; the child JSON array preserves order and each child sketch:

```powershell
python -m percolation_workflow.cli propose-decomposition artifacts/<target>/state.json `
  --parent-id <node-id> --agent-id <agent-id> --sketch "..." `
  --children-file artifacts/<target>/children.json
```

`FilesystemHostAdapter` is the provider-neutral hand-off boundary: it atomically persists
dispatch envelopes and callback inbox files without replacing an existing event. A Codex
CLI adapter is now available for one dispatch at a time; it binds a fresh host agent, runs
`codex exec --json --output-last-message` in the assigned project, saves raw JSONL plus hashes,
and emits the v1 callback. Its stdout/stderr sidecars are journaled line-by-line while the process
runs, so an interrupted attempt retains the prefix emitted before the interruption. The coordinator remains the only component allowed to reduce
callbacks into workflow state:

```powershell
python -m percolation_workflow.cli run-codex-agent artifacts/<target>/state.json `
  --dispatch-file artifacts/<target>/dispatch/<request-id>.json `
  --callback-dir artifacts/<target>/callback-inbox `
  --project examples/<target> --output-dir artifacts/<target>/codex-runs
```

The adapter rejects a successful CLI process that does not return a strict structured
candidate/decomposition, and rejects candidate paths outside the assigned project. A candidate
may name an entrypoint plus a `sources` list for a multi-file Lean proof bundle. It can also
resolve `source:"AUTO"` from before/after hashes when there is one changed conventional
`Candidate.lean`/`Solution.lean` entrypoint; the callback and coordinator compile receipt retain
every changed source, topologically orders local imports, and compiles support modules before
the entrypoint. It renews the single
request's lease while Codex is running. The batch supervisor binds each request before
starting isolated CLI processes, renews leases while they run, and writes one callback per request:

```powershell
python -m percolation_workflow.cli run-codex-agents `
  --dispatch-dir artifacts/<target>/dispatch `
  --callback-dir artifacts/<target>/callback-inbox `
  --project examples/<target> --output-dir artifacts/<target>/codex-runs `
  --max-workers 2
```

For the Prove2Me full-project path, the Stage-1 declaration graph and Stage-2 sketch facts can be
joined into an auditable upload plan. The planner uses declaration containment, exact byte-offset
proof cuts, private user-name joins, instance roots, and spanless-companion filtering; it performs
no upload and its output is planning evidence only:

```powershell
python scripts/plan_upload.py upstream/prove2me_workspace/examples/upload_full_project/expected/decl_graph.jsonl `
  --sketch <sketch-info-files> --module <MODULE=SKETCH_JSONL> `
  --source-root <source-project-root> `
  --root SumSquares.six_sumSq --force-node SumSquares.sumSq_succ `
  --output artifacts/percolation/prove2me-upload-plan.json
```

The resulting leaves-first actions can be handed to `UploadLedger`, which records an immutable
action identity before calling a provider transport and records the response afterward. The concrete
`Prove2MeTransport` implements the documented `/submit-definition`, `/submit-problem`, and `/verify`
queues, polls terminal jobs, refreshes an API-key token when configured, and persists remote ids before
polling. Bind payloads and solution files separately, then run it with credentials supplied only by
the environment:

```powershell
python scripts/upload_prove2me.py `
  --plan artifacts/percolation/prove2me-upload-plan.json `
  --actions artifacts/percolation/prove2me-upload-bindings.json `
  --ledger artifacts/percolation/upload-ledger.json `
  --operation-store artifacts/percolation/prove2me-operations.json
```

The bindings file is keyed by the plan action, for example:
`{"theorem:P.t":{"payload":{"theorem_name":"P.t","theorem_title":"…","formal_statement":"… := by sorry","natural_language_statement":"…","preamble":"import Mathlib"}},"solution:P.t":{"solution_path":"Solutions/Sol_P_t.lean"}}`.
All plan keys must be bound; the script refuses to alter plan identity or dependency edges.

The transport sends an `Idempotency-Key` for every mutation and refuses to guess after a connection
failure that returned no provider id. No network mutation occurs unless an access token or API key is
explicitly provided through `PROVE2ME_ACCESS_TOKEN` or `PROVE2ME_API_KEY`.

The protocol boundary has a loopback integration harness that drives the real HTTP transport and
ledger through definitions, theorem publication, leaves-first solution verification, polling, and a
fresh ledger/operation-store reload. It never contacts Prove2Me:

```powershell
python scripts/test_prove2me_transport.py
```

The same plan can be materialized into the platform layout with exact Stage-2 spans:

```powershell
python scripts/generate_platform_tree.py <plan.json> <decl_graph.jsonl> `
  --sketch <MODULE=sketch.jsonl> --source-root <source-project> `
  --output-root <platform-root> --import <IMPORTED=PLATFORM_IMPORT>
```

Use `CONTEXT::IMPORTED=...` when two source modules import the same module but need different
platform replacements. The generated Definitions, theorem stubs, and top-level `solution` files
must be compiled before any upload; `artifacts/percolation/generated-platform/` is a compiled
public SumSquares fixture with its receipt.

When an extracted solution came from an active `section` or `namespace`, the generator hoists
the active `variable`, `include`, and `omit` commands into the solution preamble. The generated
source is still compiled as the authoritative check for notation and local-attribute context.

Use `scripts/build_platform_tree.py` as the release gate against a pinned Lake project; it compiles
Definitions before theorem stubs before Solutions and can fail on an elaborated-type diff when the
source/staged JSONL rows are supplied:

```powershell
python scripts/build_platform_tree.py <platform-root> `
  --lake-project <pinned-lake-project> `
  --original-types <source-types.jsonl> --staged-types <staged-types.jsonl>
```

Within those phases, the gate also topologically orders generated modules by their platform
imports, so an old `.olean` cannot hide a wrong alphabetical order. A clean five-module refresh is
part of the checked artifact evidence.

Those rows can be emitted by `scripts/extract_elaborated_types.py`, which runs a temporary Lean
meta probe over explicitly named declarations and records their `pp.all` types and axiom sets.
The public fixture has both [original-types.jsonl](<C:/Users/z5242/Desktop/重构版/工作流/artifacts/percolation/original-types.jsonl>)
and [staged-types.jsonl](<C:/Users/z5242/Desktop/重构版/工作流/artifacts/percolation/staged-types.jsonl>).

When a coordinator compile fails after an environment or staging repair, the checkpointed request
can be retried without deleting the failed attempt:

```powershell
python -m percolation_workflow.cli retry-compile-agent artifacts/harris_sketch/state.json `
  --request-id <request-id> --project examples/harris_replay `
  --source examples/harris_replay/HarrisReplay/Positive.lean
```

The same `host-cycle` also labels a new dispatch as `repair` (or
`repair_parent_assembly`) after a failed Lean attempt, carrying the exact prior diagnostic as
`repair_context`. If a compiler worker has durably started but exits before publishing its receipt,
the coordinator records a synthetic-free `compile_error` recovery event and schedules the ordinary
repair frontier again; a missing start marker or a live worker remains `awaiting_receipt`.

## Run

```powershell
python -m unittest discover -s tests -v
python -m percolation_workflow.cli status .workflow/state.json
```

The Lean runner accepts a project directory and a command (default: `lake build`). Remote Prove2Me
submission is available only through the explicit upload script above and is never inferred from a
local plan.

The durable host boundary has a cross-process recovery harness. It abruptly exits a child after a
request is bound, waits for the persisted lease to expire, reclaims the timed-out attempt, and
prepares a fresh frontier request:

```powershell
python scripts/test_host_recovery.py --output artifacts/host_recovery/latest.json
```

This validates persistence and ownership recovery only. The installed Codex CLI adapter additionally
has a real isolated smoke run under `artifacts/codex_live_smoke_20260905_v6/`; that run returned a
provider thread id, a `turn.completed` event, a structured callback, and a coordinator-collected
Lean compile. It is intentionally a small theorem smoke, not evidence that the complete percolation
target is solved through this new CLI wrapper.

Registry freshness is exercised separately on a fresh Lean fixture. The script registers a node,
mutates `Solution.lean`, detects the source-digest mismatch, removes the stale registry entry,
preserves its receipt in node history, and reopens the node on the frontier:

```powershell
python scripts/test_stale_artifact_invalidation.py
```

The generated report is stored under `artifacts/stale_artifact_invalidation/`. The fixture contains
the expected `sorry` placeholders, so this is freshness/invalidation evidence rather than a proof
claim.

## Percolation replay evidence

`artifacts/percolation/decl_graph.jsonl` is extracted from the compiled `Solution` environment using
the Prove2Me declaration extractor adapted in `scripts/extract_percolation_graph.lean`.
`scripts/merge_percolation_graph.py` merges target-reachable dependencies through definitions and
generated helpers while preserving existing research IDs and attempts. This reconstructs dependencies
of an existing proof; autonomous discovery of this decomposition remains an acceptance requirement.
The state also records a versioned graph artifact with the input digest, roots, selected theorem nodes,
and projected type/value edge provenance, so the DAG's source plan remains auditable after reload.

`scripts/extract_percolation_types.lean` collects printed elaborated types and transitive axiom sets.
`scripts/attach_percolation_types.py` attaches that evidence without replacing trusted Challenge text
or promoting nodes. Printed types still require elaboration in context before proof reuse.
