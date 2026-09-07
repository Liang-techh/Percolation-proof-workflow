# Parallel agent task queue

`kind: task_plan` — this file is planning input, not proof and not a registry
entry. Agents should claim one task by adding their name and timestamp, then
write the result as a new `review_result` file in this same directory. Keep
tasks disjoint and do not edit the authoritative checkpoint or external source
without an explicit scoped request.

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

- status: `claimed` (Schrodinger the 6th, 2026-09-06)
- scope: design the smallest adapter from canonical Julia/DH source manifest to
  Lean/checker semantics using existing snapshots;
- deliver: review or disjoint sidecar with explicit semantic premises and
  hashes; retain `pending` status;
- forbidden: treating hash equality as a semantic proof or running full search.

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
