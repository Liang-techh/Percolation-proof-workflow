# Parallel agent task queue

`kind: task_plan` — this file is planning input, not proof and not a registry
entry. Agents should claim one task by adding their name and timestamp, then
write the result as a new `review_result` file in this same directory. Keep
tasks disjoint and do not edit the authoritative checkpoint or external source
without an explicit scoped request.

## Current roundtable assignments

These assignments use the user-provided periodic worker pool. They are
independent bounded tasks; a worker must inspect this queue and the board before
claiming, then leave the authoritative result in a new inbox review.

| worker label | task | boundary |
|---|---|---|
| 封不觉 | `T-P3-007` | one concrete mass/DH entry bridge |
| 柳冠一 | `T-P4-005` | one-channel residual source binding |
| 占月方源 | `T-P8-005` | terminal-transfer interface |
| 星宿仙尊 | `T-M4-002` | block-(4,5) dependency cone |
| 苏梦辰 | `T-P0-002` | fresh receipt/provenance re-audit |
| 红莲魔尊 | `T-P7-001` | fallback tail obligation audit |
| 奥尼洛 | `T-DAG-003` | shared-lemma/DAG projection |
| 狂弓魔尊 | `T-REPAIR-001` | Lean/checker repair-loop audit |

Assignment does not imply proof progress or ownership of a theorem. A result
may be `pending`, `rejected`, or `architecture_only`; only the normal
verification and registry gates can change admission state.

## Queue: Route-B current bottlenecks

### T-P3-001 — single-entry true-DH source bridge

- status: `reviewed` (Codex, 2026-09-06T00:00:00-06:00; result: `review-T-P3-001-p3-audit.md`)
- scope: one fixed rational q-box and one `M[i,j]` entry;
- inspect: `docs/routeb-p3-next-concrete-child.md`,
  `examples/routeb_p3_mass_entry_bridge_lean/`;
- deliver: exact source/interval contract, source hashes, and focused Lean or
  checker result; distinguish conditional Float64 trace premises from proved
  Julia/DH equality;
- forbidden: more sampling, full branch-and-bound, registry promotion.

### T-P4-001 — residual source binding

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: one P4 residual/Schur channel and its exported decimal or rational
  witness;
- inspect: `examples/routeb_p4_next_child/`,
  `examples/routeb_p4_decimal_source_binding_audit/`, and the C2
  force/acceleration audit;
- deliver: exact algebraic child or a precise source-binding obstruction with
  receipt fields and exit code;
- forbidden: treating decimal reification or solver output as true-DH proof.

### T-P8-001 — 13-state/14-state reachability contract

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: bind the deployed RHS to either the existing 14-state ramp parent or a
  formally defined explicit-time 13-state parent;
- inspect: `docs/routeb-p8-flowpipe-binding-next.md`,
  `docs/routeb-p8-next-concrete-child.md`, and
  `examples/routeb_p8_contract_adapter/`;
- deliver: contract compatibility result and smallest next theorem;
- forbidden: claiming flowpipe coverage from endpoint payloads or a conditional
  adapter.

### T-WF-001 — registry/admission boundary audit

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as documentation-only)
- claimed_by: `Codex`
- claimed_at: `2026-09-06T20:20:00-06:00`
- scope: read-only audit of any proposed `review_result` against
  `model.py`, `registry.py`, `comparator.py`, and the current Route-B state;
- deliver: whether integration is documentation-only, DAG metadata, pending,
  rejected, or eligible for an existing explicit gate;
- forbidden: changing status or registry directly.

## Queue: next smallest leaves

### T-P3-002 — fixed-point IEEE trace witness

- status: `open`
- scope: one fixed q-box and one `M[i,j]`, preferably at a deterministic
  source point such as `q=0`;
- deliver: a replayable Float64 operation/rounding witness or a precise reason
  it cannot be produced with the current runtime; write only a review result;
- forbidden: infer global interval soundness from one point or from equal bits.

### T-P4-002 — one-channel true-DH residual envelope

- status: `open`
- scope: consume the exact Schur leaf for one channel and identify the smallest
  executable source-binding witness for `d`, `p`, and the actual residual;
- deliver: checker/Lean boundary, normalization map, and receipt contract;
- forbidden: using the decimal audit as DH equality or closing P4 globally.

### T-P8-002 — explicit-time 13-state parent option

- status: `open`
- scope: compare a new explicit-time 13-state parent with the existing
  14-state ramp parent, including initial-domain and terminal statement changes;
- deliver: a decision memo and minimal theorem signature, with no source edits;
- forbidden: silently changing the target theorem or claiming flowpipe coverage.

### T-M4-001 — dependency-cone closure audit

- status: `reviewed_pending` (Codex, 2026-09-06; result integrated as pending)
- scope: use the current checkpoint and DAG projection to list the exact M4
  prerequisite cone and identify which leaves can be proven independently;
- deliver: review result with deterministic node IDs, levels, and next frontier;
- forbidden: status promotion, deletion of failed history, or broad regression.

### T-P0-001 — reproducibility baseline re-audit

- status: `reviewed_pending` (integrated at Route-B revision 333; result:
  `review-T-P0-001-repro.md`)
- scope: existing P0 attempts, receipts, source hashes, and the smallest
  reproducibility checker only;
- deliver: whether P0 can enter `evidence_complete`, with missing gates and
  exact evidence paths;
- forbidden: broad reruns, status promotion, or registry mutation.

### T-P0-002 — fresh receipt/provenance re-audit

- status: `reviewed_pending` (integrated at Route-B revision 350; current
  snapshot has no stable fresh receipt/output-hash binding)
- scope: compare the historical P0 receipt against the current canonical
  `state.json` revision, Git/source snapshot, receipt path and output hashes;
  keep workflow-node completion separate from fresh provenance verification;
- deliver: exact current revision and hash evidence, a deterministic receipt
  alias/index proposal, and all unresolved freshness blockers;
- forbidden: deriving a receipt hash from a Git blob hash, reusing an old
  receipt as current evidence, status promotion, or registry mutation.

### T-DAG-002 — explicit child-DAG refinement

- status: `reviewed_pending` (integrated at Route-B revision 333; result:
  `review-T-DAG-002-child-dag.md`)
- scope: propose disjoint P3/P4/P5/P6/P8/M4 source-binding, algebra,
  coverage, and terminal-transfer child nodes;
- deliver: deterministic node names/dependencies, admission boundaries, and
  migration risks;
- forbidden: mutating the authoritative checkpoint or silently changing the
  theorem statement.

## Queue: next parallel leaves

### T-P3-003 — canonical source-manifest binding

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P3-003-source-manifest.md`)
- scope: reconcile the authoritative Julia/DH source, coordinate order,
  arithmetic convention, and current delivery manifest without running a full
  interval search;
- deliver: one review result with exact paths, hashes, and the smallest
  admissible source-binding contract;
- forbidden: treating equal payload bits or point samples as global bounds.

### T-P4-003 — force/acceleration residual normalization

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P4-003-residual-normalization.md`)
- scope: formalize the typed map between `l = I f - M0 a` and the PMI-side
  residual `d`, preferably as a focused algebra/Lean sidecar;
- deliver: review result plus focused compile/check evidence if available;
- forbidden: closing true-DH binding, coverage, or the P4 parent.

### T-P8-003 — freeze the state contract

- status: `reviewed_pending` (integrated at Route-B revision 334; result:
  `review-T-P8-003-contract.md`)
- scope: decide whether the deployed 13-state RHS requires an explicit-time
  theorem or a separately justified 14-state ramp source;
- deliver: minimal theorem signature and admission blockers;
- forbidden: silently changing the target theorem or claiming a flowpipe.

### T-P5-001 — energy-syzygy admission audit

- status: `reviewed_pending` (integrated at Route-B revision 337; result:
  `review-T-P5-001-energy-syzygy.md`)
- scope: isolate the exact Newton–Euler energy identity from sparse SOS and
  true-DH source obligations, and identify the smallest reusable child;
- deliver: review result with statement, dependencies, and evidence boundary;
- forbidden: promoting solver output or an abstract identity to physical M4.

### T-P4-004 — typed normalization Lean sidecar

- status: `reviewed_pending` (integrated at Route-B revision 337; result:
  `review-T-P4-004-normalization-sidecar.md`)
- scope: keep force residual `l` and PMI residual `d` as distinct typed
  objects, connected only through an explicit interface premise;
- deliver: focused Lean sidecar or review result, with no true-DH/coverage
  admission;
- forbidden: closing the P4 parent or mutating the authoritative checkpoint.

### T-P8-004 — explicit-time contract sidecar

- status: `reviewed_pending` (integrated at Route-B revision 338; result:
  `review-T-P8-004-explicit-time-sidecar.md`)
- scope: formalize the smallest 13-state explicit-time interface with external
  parameter `c`, initial projection, and terminal-transfer assumptions;
- deliver: focused Lean sidecar or review result; no broad regression;
- forbidden: silently changing the current theorem target or claiming a flowpipe.

### T-P3-004 — source-semantic adapter design

- status: `reviewed_pending` (integrated at Route-B revision 339; result:
  `review-T-P3-004-semantic-adapter.md`)
- scope: design the smallest adapter from canonical Julia/DH source manifest to
  Lean/checker semantics using existing snapshots;
- deliver: review or disjoint sidecar with explicit semantic premises and
  hashes; retain `pending` status;
- forbidden: treating hash equality as a semantic proof or running full search.

### T-FLT-DERIV-CALC — Anthropic FLT derivation/calculus scan

- status: `reviewed_pending` (catalog review integrated as event-only metadata)
- scope: audit generic derivation, calculus, continuity, integral, and limit
  infrastructure from the pinned Anthropic FLT source; identify only candidates
  whose assumptions can be restated for the current adapter/PDE lanes;
- deliver: exact source path, declaration, commit, license/provenance, reuse
  class, and a focused target-side compile proposal;
- forbidden: importing FLT-specific arithmetic or treating a scan as a proof,
  Route-B node closure, or registry promotion.

### T-FLT-TOPOLOGY-QUOTIENT-CLM — quotient/topology transport scan

- status: `reviewed_pending` (catalog review integrated as event-only metadata)
- scope: audit quotient, subsingleton, connectedness, continuity,
  `ContinuousLinearMap`, and transport infrastructure for small adapter-side
  reuse;
- deliver: exact source path/declaration, hypotheses, reuse class, and the
  smallest target-side sidecar that could be compiled without whole-repo build;
- forbidden: copying the upstream tree, weakening assumptions, or promoting
  architecture-only evidence to a verified theorem.

### T-P3-005 — minimal semantic-binding child theorem

- status: `reviewed_pending` (integrated at Route-B revision 341; result:
  `review-T-P3-005-semantic-binding-child.md`)
- scope: isolate the smallest typed child interface that connects the
  canonical Julia/DH source to Lean/checker semantics, with explicit semantic
  premises and independent provenance hashes;
- deliver: exact statement, dependency boundary, focused-check proposal, and
  unresolved true-DH/coverage blockers;
- forbidden: equating hashes with semantics, changing the authoritative source,
  or closing P3/P0/M4.

### T-P5-002 — minimal Newton–Euler energy child

- status: `reviewed_pending` (integrated at Route-B revision 341; result:
  `review-T-P5-002-energy-child.md`)
- scope: isolate a standalone energy/power identity or syzygy child theorem
  from the current 6-DOF dynamics implementation;
- deliver: typed statement, exact dependencies, evidence level, and a focused
  compile/check route that does not require a full regression;
- forbidden: promoting sparse SOS output, assuming true-DH binding, or claiming
  flowpipe/terminal transfer.

### T-P3-006 — source-binding interface sidecar

- status: `reviewed_pending` (integrated at Route-B revision 342; Lean blocked:
  `review-T-P3-006-semantic-binding-sidecar.md`)
- scope: encode the P3-005 premise boundary in a small adapter-side contract;
  keep source hashes, exact snapshot semantics, and interval enclosure as
  separate fields;
- deliver: isolated sidecar/README plus focused compile or a precise blocked
  report;
- forbidden: concrete Float64-to-exact equality, global DH identification,
  registry promotion, or edits to the authoritative checkpoint.

### T-P5-003 — Christoffel power identity sidecar

- status: `reviewed_pending` (integrated at Route-B revision 342; focused Lean
  compile passed, no registry promotion:
  `review-T-P5-003-christoffel-power-sidecar.md`)
- scope: isolate and compile the exact Christoffel power identity already
  identified by P5-002, with minimal imports and explicit #print axioms;
- deliver: isolated Lean sidecar/README and focused compile evidence;
- forbidden: importing sparse SOS or flowpipe claims, assuming source binding,
  or closing the P5/M4 parent theorem.

### T-FLT-SPECTRAL-LINEAR — spectral and linear algebra scan

- status: `reviewed_pending` (integrated at Route-B revision 343;
  event-only catalog review)
- scope: inspect only non-number-theory spectral, eigenspace, finite-dimensional
  linear algebra, quotient, and exact-sequence declarations in the pinned FLT
  repository;
- deliver: three-level reuse classification, exact declaration/path, imports,
  hypotheses, source commit/license, and the smallest current-pin sidecar
  proposal;
- forbidden: importing arithmetic endgames or claiming Route-B spectral/PDE
  closure from a source scan.

### T-FLT-TRANSPORT-ADAPTER — transport and adapter scan

- status: `reviewed_pending` (integrated at Route-B revision 344;
  event-only catalog review)
- scope: inspect generic continuous-map, linear-equivalence, pairing transport,
  representation, and coordinate-change adapters outside pure number theory;
- deliver: exact statement shape, assumptions, reuse class, attribution, and
  target-side adaptation risks;
- forbidden: whole-repository build, source copying, or registry promotion.

### T-FLT-INFRA-REGISTRY — registry/graph/obstruction scan

- status: `reviewed_pending` (integrated at Route-B revision 343;
  event-only catalog review)
- scope: inspect comparator, challenge/solution split, dependency graph,
  documentation extraction, attribution, and obstruction-tracking patterns;
- deliver: architecture-only findings and concrete integration points for the
  local DAG/frontier/registry, preserving fail-closed authority boundaries;
- forbidden: treating HTML badges, graph nodes, or comparator fixtures as
  proof evidence.

### T-FLT-SPECTRAL-SIDECAR — highest-value spectral candidate

- status: `reviewed_pending` (integrated at Route-B revision 346; independent
  admission review classifies it as architecture-only)
- scope: test the smallest non-number-theory eigenspace/range bridge identified
  by the spectral scan, using a new isolated sidecar and the current local
  Lean/Mathlib pin if available;
- deliver: exact theorem boundary, imports, compile output, #print axioms,
  provenance, and explicit reason if the upstream wrapper is too specialized;
- forbidden: whole FLT build, arithmetic theorem reuse, registry promotion, or
  inferring Route-B spectral closure from a failed/blocked compile.

### T-FLT-SPECTRAL-PREDICATE — genuine eigenspace predicate sidecar

- status: `reviewed_pending` (integrated at Route-B revision 348; current
  version has a real eigenspace predicate, but Mathlib `.olean` verification
  is blocked; prior reviews cover successive sidecar versions)
- scope: replace the tautological range helper with a proposition containing an
  actual eigenspace predicate, explicit operator/eigenvalue assumptions, and a
  range-to-eigenspace equality or a clearly stated obstruction;
- deliver: isolated Lean sidecar, #print axioms, exact distinction between a
  self-contained abstraction and direct upstream reuse;
- forbidden: tautological range identities, arithmetic FLT reuse, registry
  promotion, or declaring the original spectral sidecar verified.

## Handoff format

Use a filename such as `review-<task-id>-<agent>-<timestamp>.md` and begin it
with:

```yaml
kind: review_result
task_id: T-P3-001
source_agent: <agent-id>
created_at: <ISO-8601>
integration_status: pending
```

Then record the inspected paths/commit, exact evidence and hashes, proposed
integration, and unresolved blockers. The original result remains immutable
after integration; corrections should be a new result file.
