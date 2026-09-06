# Acceptance scope and remaining work

The original goal remains a reusable research workflow driven by Codex agents. Passing an upstream
submission and reconstructing one theorem are evidence toward that goal, not replacements for it.

## Evidence obtained

- Percolation at commit `795efb86f191735c5481675763537cfb4ff37e55` passes the upstream
  Linux comparator script, including nanoda and Lean default kernel acceptance. Original logs and
  the stage receipt are in `artifacts/percolation/`.
- The compiled declaration graph and elaborated types are persisted. Source theorem dependencies
  are projected through definitions and generated helpers, with 3480 target-reachable theorem nodes.
- Harris replay uses independent child proof agents and a parent agent. The direct `aesop` baseline
  failed, proof repair occurred, and the parent proof term was audited for actual child references.
  Use `scripts/audit_harris_run.py` for the current staged acceptance result.
- The portable CI script passed in a fresh local Linux snapshot: 35 Python tests, the Harris build,
  and the local-FKG 3581-job full build plus upstream comparator, nanoda and Lean default kernel.
  The comparator emitted the exact `Your solution is okay!` acceptance line. Logs and receipt are in
  `artifacts/ci/ci-s40djv1a-receipt.json` and `artifacts/ci/ci-s40djv1a.log`. That snapshot was created
  just before the source comparator was switched to `LocalFKGSolutionAgent`; its `LocalFKGSolution`
  coordinator draft has the same theorem statement and proof body as the agent file (only harmless
  formatting differs), while the agent-named artifact was also independently verified by the live
  controller. This is not a hosted GitHub Actions execution.
- A post-change fresh local Linux CI refresh also passed end to end after disk recovery. Its receipt
  is `/home/z5242/.local/share/percolation-workflow/ci-9wokc4o7/ci-receipt.json`, reporting
  `status: passed` and `exit_code: 0`. The run executed 52 Python tests, the 3245-job Harris
  build/comparator, and the 3581-job local-FKG build/comparator, with both nanoda and Lean's
  default kernel accepting the submitted solutions. This remains local Linux execution, not hosted
  GitHub Actions.
- Durable host-agent requests preserve terminal payloads and actual compiler diagnostics;
  compilation alone never promotes a candidate to the verified registry. A real Lean error
  feeds the next request in a regression test, with a synthetic host response explicitly used
  as the test fixture, not evidence of a live autonomous proof run.
- Compiler workers now persist results outside the coordinator checkpoint. `collect-compile`
  resumes a matching result without starting another compiler and reloads current state before
  committing. The real Lean subprocess regression checks checkpoint reload, duplicate launch
  rejection, preservation of intervening events, missing/mismatched receipts and idempotent
  collection. The standalone `scripts/test_compile_process_recovery.py` experiment additionally
  observed a coordinator's `os._exit(73)` while its compiler worker was live, then recovered
  success and error receipts with one compilation each. The reviewed report is
  `artifacts/compile_recovery/20260905T054245Z-905822ff/report.json`. Host responses are synthetic;
  this is not yet a crash-recovery experiment for the complete live proof controller.
- `check-sketch` now compares the elaborated reduction type against the ordered child-to-parent
  implication in Lean and rejects transitive axioms outside the standard three. Children are
  explicit assumptions of the reduction, not sorry-backed proof dependencies. A successful
  check opens proposed children for agent dispatch. Once all children are registry-verified,
  the accepted reduction audit can now close the parent automatically; the final root comparator
  remains mandatory. Zero or one universe parameter is supported by consistent renaming;
  multiple independent universe parameters are rejected pending an explicit mapping.
- The real Harris sketch replay passed on Lean 4.32.0: 3241-job child/parent builds and an
  elaborated implication/axiom audit are persisted in `artifacts/harris_sketch/state.json`.
  The conditional proof is adapted from the earlier completed Harris proof; this is explicitly
  not a fresh mathematical discovery.
- `next-actions` derives host work from durable request/node phases, including dispatch,
  observation, compiler receipt collection and final verification. It neither fabricates host
  tool results nor executes agent calls on its own. Real bridge tests exercise these transitions.
- Frontier verification now accepts a trusted node-to-project map for isolated immutable lemma
  bundles; the assembled project is checked separately with its own root-bound comparator after
  full build. The local-FKG run exercised that routing and completed a live kernel/comparator
  acceptance of the assembled parent project.
- The next target is fixed in `examples/local_fkg/LocalFKGChallenge.lean`: local increasing-event
  Harris-FKG without finite/countable vertex or interior-parameter assumptions. Its contract
  records forbidden original proof modules and the two planned mathematical obligations.
  The new Challenge elaborated successfully in the pinned upstream Lean 4.32.0 environment,
  with only its expected placeholder warning. Evidence is in `artifacts/local_fkg/state.json`.
  A real decomposition agent is bound to a persisted request; the separate local dependency
  cache has completed.
- The reconstruction contract is now enforced during sketch, per-node and final verification:
  Lean checks transitive imported module names and traverses declaration types/proof values,
  including opaque, generated and definition wrappers. Real Lean regression fixtures reject
  both a forbidden transitive import and a hidden forbidden proof reference. This adds provenance
  enforcement, not a substitute for the comparator/kernel checks or a sandbox for arbitrary code.
  The current 95-test suite passed (plus 12 subtests), including audit-idempotence/tamper, agent-lease, closability,
  parent-link, graph-artifact, manifest-intake, and automatic lease-reclaim coverage.
  The independent local FKG Challenge also built successfully (3561 jobs, expected target sorry
  warning only). The subsequent live agent-proposed reduction passed the coordinator's
  3566-job build, elaborated implication, axiom and forbidden-dependency checks, recorded in
  `artifacts/local_fkg/state.json`. Its two children were separately bound to live proof agents,
  and the raw decomposition-agent terminal payload is preserved in
  `artifacts/local_fkg/decomposition-agent-result.json`.
- Per-lemma content-addressed bundle staging now freezes only explicitly selected sources,
  checks toolchain/dependency revisions, retains old versions and rejects modified bundles.
  Its regression test passed. The parameterized `scripts/verify_leaf_linux.py` derives comparator
  modules and source sets from each theorem's verification manifest; the manifest-driven controller
  can stage every DAG node, and the target-specific wrapper connected both live coordinator-compiled
  leaves and the parent to the pinned Linux comparator and registry. A real Linux smoke build passed
  with the new host-independent `.lake/pinned-dependency` bundle path.
- The local-event marginal agent returned a candidate after two logged Lean failures and a
  third successful compile. The coordinator's independent compile and frozen Linux verification
  also passed. Live agent-owned compiler logs are ingested idempotently with explicit
  evidence labels; they cannot end a live request or promote a theorem on their own.
- The complete local-FKG run is closed in `artifacts/local_fkg/state.json`: three current registry
  entries, two child agents in parallel, finite-child repair history, marginal-child repair history,
  parent agent assembly, per-node Linux comparator checks, and controller final events. The final
  controller build covered 3574 jobs; final provenance and comparator passed with nanoda and Lean's
  default kernel, with an unchanged source snapshot.
- State persistence now has a cross-platform advisory writer lock and optimistic revision check;
  a stale coordinator cannot overwrite a newer callback/controller update. Unknown state schema
  versions are rejected. The callback cycle uses version-1 request/attempt/event correlation and
  rejects event-id payload reuse.
- `FilesystemHostAdapter` now provides a provider-neutral durable boundary for real host integrations:
  it emits dispatch envelopes from `next_actions`, atomically writes unmodified callback envelopes,
  rejects correlation mismatches, and never replaces an existing event file. The generic
  `persist-callback` CLI now exposes that boundary to an external Codex/provider adapter. The
  coordinator's `host-cycle` consumes that inbox and can start a validated candidate compile.
- `run-codex-agent` is now the concrete local Codex CLI adapter. It binds a fresh agent lease before
  invoking `codex exec --json --output-schema --output-last-message`, journals per-request/per-attempt
  raw JSONL and stderr sidecars as bytes arrive with SHA-256 metadata, rejects non-terminal or path-invalid results,
  renews the lease during long-running execution, and writes only a version-1 callback to the coordinator inbox. The real run in
  `artifacts/codex_live_smoke_20260905_v6/` reached structured callback ingestion and a collected
  Lean compile; earlier schema failures in the same smoke series were preserved as repair evidence.
- `run-codex-agents` now provides the multi-agent batch supervisor. It serially binds the dispatches,
  runs isolated Codex CLI processes in parallel, serializes lease renewals, and preserves independent
  callback/run artifacts. The real two-request run in
  `artifacts/codex_batch_smoke_20260905_v2/` reached two structured callbacks and two collected Lean
  compiles; the earlier `artifacts/codex_batch_smoke_20260905/` timeout is retained as authentic
  environment-repair evidence.
- A batch with no explicit `--project` can now resolve the single Lean project from the state-bound
  manifest, after checking the manifest digest and required `lakefile.toml`/`lean-toolchain` files.
  Explicit request-to-project maps remain mandatory for isolated multi-project bundles.
- Candidate artifact discovery now supports a strict `source:"AUTO"` result: the adapter compares
  pre/post Lean-file hashes and accepts exactly one changed source, or a multi-file bundle with
  one unique conventional `Candidate.lean`/`Solution.lean` entrypoint. Explicit `sources` lists
  are persisted through callback, coordinator compile job, receipt and repair retry; local import
  dependencies are topologically ordered before compilation; no-change, cyclic and ambiguous
  bundles remain rejected.
- The Prove2Me Stage-1/Stage-2 boundary now has a deterministic local planner in
  `src/percolation_workflow/upload_plan.py` and `scripts/plan_upload.py`. It joins declarations by
  containment (including wrapped commands and anonymous instances), preserves exact byte-offset
  proof cuts, joins private declarations by user-name suffix, adds instance roots, drops spanless
  generated companions only after reachability, and classifies definition material, theorem nodes,
  and inline helpers. The public SumSquares fixture produced an auditable plan artifact at
  `artifacts/percolation/prove2me-upload-plan.json`, including a Definitions → Theorems → Solutions
  leaves-first action order; it does not claim upload or proof verification.
- `scripts/generate_platform_tree.py` now materializes that plan into the `Definitions/`, `Theorems/`,
  and `Solutions/` layout using exact declaration/proof/reference spans, scoped import rewrites,
  private-helper retention, and top-level `solution` hoisting. The public SumSquares tree was
  compiled in the pinned Lake environment; its receipt is
  `artifacts/percolation/generated-platform/compile-receipt.json`. Active section/namespace
  `variable`/`include`/`omit` binders are now hoisted into extracted solutions and compiled in a
  real Lean fixture; notation and local-attribute hoisting remain deliberate Lean build gates.
- `scripts/build_platform_tree.py` now makes the compile phase reproducible and auditable: it runs
  Definitions → theorem stubs → Solutions against a caller-supplied pinned Lake project, records
  each command/output/source hash, topologically orders generated imports within those phases, and
  optionally gates on `compare_elaborated_types`. It rejects platform imports absent from the current
  manifest and records before/after source hashes, rejecting source drift during compilation. A
  clean output-directory refresh caught the old alphabetical-order/stale-`.olean` failure and then
  passed with the corrected order. The public fixture has a passed five-module receipt; generated
  stubs retain only the expected `sorry` warning.
- `scripts/extract_elaborated_types.py` now runs a temporary Lean meta probe for explicitly named
  declarations, recording `pp.all` types and transitive axiom sets. The public fixture's original
  and staged target rows were compared by the build gate with zero missing, unexpected, or type
  mismatches; the staged stub axiom set still contains the expected `sorryAx`, so this is a type
  equivalence gate, not a claim that an Open theorem stub is proved.
- `UploadLedger` now persists the ordered Phase-7 action list before each transport call and after its
  response, rejects changed action payloads, carries published theorem IDs into solution verification,
  and retries pending/in-flight operations with the same operation key. The transport is intentionally
  provider-neutral at the ledger boundary. `Prove2MeTransport` now implements the documented HTTP
  submit/poll endpoints, multipart solution upload, API-key token exchange, mutation idempotency keys,
  and a durable remote-id journal; the fresh loopback `scripts/test_prove2me_transport.py` integration
  run passed all five ordered mutations, polling, auth/idempotency checks, multipart solutions, and
  ledger restart without contacting Prove2Me. No live remote mutation is claimed without explicit
  credentials.
- Compiler recovery now covers the no-receipt worker-death case: a durable `started.json` marker is
  checked for process liveness, and a dead worker is recorded as `compile_error` with its request
  reopened through the normal repair scheduler. The existing receipt path remains idempotent and
  does not restart a live or unobserved worker.
- The Harris sketch frontier was exercised through the real host path: two open children were
  dispatched in parallel, bound to two independent Codex agents, returned terminal results, entered
  the atomic callback inbox, and were automatically compiled by `host-cycle`. A portable Harris
  verification manifest then staged both leaves and the assembled root in content-addressed bundles;
  all three nodes are now verified, all three registry entries are `current`, and the final root
  build/comparator passed with both nanoda and Lean's default kernel.
  The durable run is recorded at `artifacts/harris_manifest_intake/state.json` with manifest
  identity `1671b397de53beaa797a13a749a74e141e6d65f9f48c213535bcabbe3beb4d96`.
- The Harris run also exercised a repair boundary: an invalid dependency overlay was rejected before
  comparator execution, its diagnostic was retained, bundle staging was corrected, and the
  independent verifier resumed from durable state without fabricating a proof result.
- The cross-process host recovery harness now passes in `scripts/test_host_recovery.py`: a child
  exits with code 73 after durably binding an agent, the parent observes `reclaim_expired_agent`
  after lease expiry, and `host-cycle` automatically records `agent_timeout`, reopens the node,
  and prepares a fresh request.
  The Codex adapter now also persists `started.json`/`finished.json` markers, and `host-cycle` can
  reclaim a bound process proven dead before lease expiry. A fresh live Codex interruption is now
  exercised by `scripts/test_codex_interruption.py`: the exact marked Codex PID was terminated,
  its errored callback was consumed without state corruption, and one repair request was prepared.
  The report is under `artifacts/codex_interruption/`; it is recovery evidence only and makes no
  proof claim.
- Compiler launch intent is now durable before `Popen`, and Windows liveness uses the process exit
  code rather than `os.kill(pid, 0)`. The fresh `scripts/test_coordinator_crash_recovery.py`
  experiment killed a real coordinator with exit code 73 before worker spawn; `host-cycle`
  reclaimed the checking attempt as exit code 125, prepared one repair request, and left both
  worker markers and the registry empty. Its report is under
  `artifacts/coordinator_crash_recovery/`; this is recovery evidence only and makes no proof claim.
- The manifest-driven verifier is now exposed as the generic `verify-manifest` CLI command. A real
  WSL run on the Harris state selected the manifest's three nodes, staged the immutable bundles,
  and completed the root build/comparator with exit code 0; the former fixed-digest
  `run_final_local_fkg.py` is now only a compatibility alias.
- Frontier scheduling now records Prove2Me-style `closability`: a candidate leaf is ranked by the
  number of open ancestors that would close in its verified cascade. Decomposition records retain
  a proposal id, ordered child list, import kind/ordinal, visibility, and accepted reduction
  evidence while remaining backward-compatible with existing checkpoints.
- State validation now enforces root identity and any explicit `parent_id`/dependency agreement,
  preventing a malformed parent-child relation from reaching the scheduler.
- Graph imports now leave versioned state records containing the source digest, root set, selected
  theorem nodes, and projected type/value edge provenance. Replaying the same graph is idempotent;
  a changed graph digest is recorded as a new artifact revision.
- An optional manifest `research` section now initializes a durable, exact-name DAG through the
  generic `init-manifest` CLI. The Harris intake fixture was exercised successfully: it created a
  3-node state with the two child leaves as the initial frontier, without invoking a target-specific
  bootstrap script.
- Version-1 host callbacks now accept an ordered decomposition payload in addition to a proof
  candidate. `host-cycle` validates the child objects, persists the proposal atomically through the
  normal decomposition path, and re-consuming the same event is idempotent; this is covered by a
  durable-inbox regression test.
- The generic CLI now exposes `propose-decomposition` and returns nonzero status for rejected
  sketch/compile/frontier gates. The Harris intake state was driven through the CLI proposal and
  the real pinned WSL sketch checker, which returned `sketch_checked` before reopening its two-child
  frontier.

## Still required for full acceptance

1. The local-FKG target supplied a fresh end-to-end live demonstration of intake, decomposition,
    agent dispatch, compiler feedback, registry lookup and parent closure. A reusable manifest-driven
    controller, host-cycle entry point, and lease-aware local Codex CLI batch supervisor now exist.
    Remaining work is automatic artifact association beyond an explicitly bound project/bundle,
    plus removal of the remaining
    target-specific wrappers. Generic manifest intake now exists; the Harris
    `intake-manifest.json` is a reference fixture. Earlier Harris dispatch was coordinated in this
    conversation; its completed run now uses the manifest-driven verifier for leaf selection and root
    closure.
2. Record complete raw agent attempts as they happen. Some Harris failure records were imported as
   explicitly labelled agent-report excerpts after completion, not streamed through the repair API.
3. Harden stale-artifact invalidation and broaden crash-window coverage. JSON checkpoints, writer
   lock, revision/CAS checks, attempt guards, and the host-agent lease reclaim path are covered by
   a fresh cross-process harness. Compiler receipt recovery, no-receipt dead-worker recovery,
   pre-spawn coordinator-crash recovery, and fresh source-drift invalidation are covered by
   dedicated experiments. The source-drift report is under
   `artifacts/stale_artifact_invalidation/`; it detects a changed `Solution.lean`, removes the
   stale registry entry, preserves its receipt, and reopens the frontier node. These fixtures
   contain placeholders and make no proof claim. The live Codex host-process interruption is
   covered separately by `artifacts/codex_interruption/`.
   All state mutations still require one coordinator (parallel proof/compile workers do not write
    research state); cross-process CAS/locking now rejects stale writers. A deliberately parallel
    independent-leaf verification exposed and retained a real stale-revision diagnostic; the leaves
    were then verified sequentially. Compiler/process ownership remains coordinator-scoped and still
    needs broader crash-window coverage beyond the exercised pre-spawn case.
4. The local-FKG live decomposition passed the sketch gate and the complete leaf-to-parent gates.
   Its real Lean regression covers valid implication, a parent-placeholder dependency, explicit
   sorry, and a wrong target type. Expand universe handling when required by an actual target;
   reduction-audit closure is automatic after each child set closes; final root comparator
   verification remains mandatory.
5. Extend CI to the complete live workflow as it is implemented. Pinned executable CI now runs the
   Python suite, loopback Prove2Me transport integration, fresh stale-artifact invalidation,
   host/worker/coordinator recovery harnesses, Harris replay, and local-FKG comparator path. A local passing run exists; public PR/Actions
   provenance is recorded in
   `docs/public-percolation-provenance.md`. The observed green upstream job was zeta23, not
   percolation; no hosted CI pass for this new repository is claimed. The post-change local Linux
   refresh now passes after disk recovery; the fresh receipt and full log are
   `artifacts/ci/ci-jnt1du04-receipt.json` and `artifacts/ci/ci-jnt1du04.log`. It does not remove
   the remaining need for hosted CI provenance and a CI job that exercises the complete live
   workflow.
6. The local-FKG target is fresh and nontrivial, with dependency-driven parent selection. A
   generic manifest-driven Linux verifier/controller, versioned host-cycle protocol and filesystem
   HostAdapter and a concrete multi-agent, lease-aware Codex CLI bridge now exist; remaining work is
   automatic candidate/artifact association beyond explicit bundle metadata and the
   manifest-derived project, plus eliminating the historical target-specific
   scripts. The Stage-1/Stage-2 upload planner, skeleton generation, exact import rewriting,
   type-diff gate, provider-neutral ordered action plan, and durable provider-neutral upload ledger
   are now available; the concrete authenticated transport and crash-resumable remote-id journal are
   implemented and unit-tested. An authenticated end-to-end upload against the live service remains
   pending because no credentialed mutation has been authorized in this workspace. A
   failure of `aesop` alone is not evidence that no single agent could prove a target. Graph artifact
   provenance is now persisted, including constructor expansion, participating instance roots, and
   type/value edges. Exact upload-project parity still needs Stage-2 position facts, skeleton
   subtraction, span-containment classification, and the ordered uploader.

PDE expansion remains deferred until the percolation-oriented workflow passes these requirements.
