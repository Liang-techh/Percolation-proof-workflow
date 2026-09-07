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
