---
kind: review_result
task_id: T-WF-001
source_agent: Codex
created_at: 2026-09-06T20:20:00-06:00
integration_status: pending
---

# Workflow admission-boundary audit

## Scope and read-only evidence

Inspected at the current worktree HEAD (`5038601 Add hourly agent review task queue`):

- `src/percolation_workflow/model.py`
- `src/percolation_workflow/registry.py`
- `src/percolation_workflow/comparator.py`
- `artifacts/routeb_6dof/state.json`
- P3/P4/P8 reports and concrete-child documents under `examples/` and `docs/`

Commands used:

```powershell
$j=Get-Content artifacts/routeb_6dof/state.json -Raw | ConvertFrom-Json
$nodes=@($j.nodes.PSObject.Properties | ForEach-Object { $_.Value })
$nodes | Group-Object status
Get-FileHash artifacts/routeb_6dof/state.json -Algorithm SHA256
Get-FileHash src/percolation_workflow/model.py,src/percolation_workflow/registry.py,src/percolation_workflow/comparator.py -Algorithm SHA256
rg -n "PENDING|OPEN|VERIFIED|registry|admission|coverage|binding|sorry|admit|axiom" docs/routeb-p3-next-concrete-child.md docs/routeb-p8-flowpipe-binding-next.md docs/routeb-p8-next-concrete-child.md examples/routeb_p3_mass_entry_bridge_lean/REPORT.md examples/routeb_p4_next_child/REPORT.md examples/routeb_p4_decimal_source_binding_audit/REPORT.md examples/routeb_p8_rhs_receipt_lean/REPORT.md
```

Observed hashes:

| artifact | SHA-256 |
|---|---|
| `artifacts/routeb_6dof/state.json` | `97fbba67d0facfb349bd41d9fc34c7229a440a263f19c4c211b97ef7ad7a4b7d` |
| `src/percolation_workflow/model.py` | `6ecf517191e0a619aab912ae4bd7612f261416cb1c8f226cb5efeb29a53ebc0` |
| `src/percolation_workflow/registry.py` | `d2e89be8848153adb2fb0a041029b67b657416552d96e3119e5955210d8139ce` |
| `src/percolation_workflow/comparator.py` | `b3e33aa73e9a606761e851156f5d0cdfb7e547b4feBDC5d1a23598d20cc4aedb` |

The model/state query returned `revision=328`, 64 nodes with status `open`, an empty registry, and no global-closure receipt. `formal_certificate_allowed` is not a top-level field in this schema; the external Route-B admission flag is recorded in the external evidence and reports as false. This schema distinction must not be interpreted as permission to admit.

## Boundary findings

### P3 mass-entry bridge — pending, conditional only

`MassEntryBridge` is a compiled candidate with a conditional source/interval premise. Its report explicitly leaves canonical Julia/DH binding, IEEE operation semantics, all-entry coverage, and downstream P4/P8/M4 obligations open. `model.py` only allows a theorem node with `NodeStatus.VERIFIED` to close a normal dependency; external-research nodes additionally require the explicit external evidence path and freshness. No P3 node or registry entry was changed.

### P4 sidecars — scoped theorem evidence, not Route-B admission

`P4RationalSchurAbsorption` reports a kernel-checked exact rational algebraic child with standard Lean axioms only. This can support a narrowly scoped Lean child theorem, but it does not establish that the rational witness is the deployed true-DH residual, nor global partition coverage, Gram/source reification, or M4 closure. The decimal audit independently labels true-DH equality `PENDING`. Therefore it is not eligible to promote `P4.residual_schur_pmi` or the verified registry.

### P8 sidecars — conditional interface and an explicit incompatibility

The P8 receipt interface and contract adapter compile, but their reports keep Julia `full_rhs!` binding open. The concrete audit identifies the deployed source as 13-state with `du[13]=0`, while the existing 14-state parent requires `w'=c` and `c'=0`; the natural lift fails for a legal `c=1` state. Endpoint payloads, a one-step Picard decomposition, or a conditional adapter cannot close flowpipe coverage or terminal transfer. No P8 admission is eligible.

## Admission decision

**Integration status: documentation-only / pending.** No proposed recent sidecar crosses an existing admission gate. There is no observed core-code path that automatically maps a compiled candidate, local Lean success, decimal reification, or conditional receipt into `VERIFIED` or the registry:

- `status_is_closed` is strict for normal theorem edges.
- `registry.audit_registry` requires a verified node, matching statement/manifest identity, source evidence, and current artifact evidence.
- `validate_candidate_receipt` in `comparator.py` returns `pending` for missing coordinator bindings and keeps comparator acceptance and registry promotion separate.
- `run_comparator` requires exit code zero plus the exact standalone acceptance line; it does not itself register a theorem.

## Proposed integration

1. Keep this result as an immutable review record; do not alter `state.json`, registry, or node status.
2. Attach this audit to the workflow's advisory graph/provenance only after an explicit coordinator integration step; preserve `integration_status=pending` until then.
3. If adding metadata later, record each sidecar as `compiled_candidate` or `pending` with its source hashes, Lean receipt, scope, and unresolved source-binding/coverage obligations. Never use `completed_axiom` or a generic `completed` projection as `VERIFIED`.
4. Keep the next mathematical frontier at P3 source semantics, P4 true-DH residual binding, and P8 contract repair/flowpipe coverage; do not spend the admission budget on repeated regression runs.

## Unresolved blockers

- P3: Float64-to-exact/interval semantic bridge for canonical DH evaluation, plus all-box/all-entry coverage.
- P4: binding the rational residual/Schur witness to deployed true-DH force/acceleration semantics and full partition coverage.
- P8: choose and formally bind a coherent 14-state ramp RHS or a new explicit-time 13-state parent; then prove outward RHS containment, solution existence, continuation, and `[0,1]` coverage.
- M4: residual absorption, true-DH flowpipe, terminal transfer, comparator, and full pinned Lean/CI remain open.
- External state reports 64 open nodes and an empty verified registry; no admission flag should be inferred from this review.

## Integrity statement

This review performed no writes to core source, `artifacts/routeb_6dof/state.json`, or the verified registry. The only intended outputs are this review file and the queue claim metadata.
