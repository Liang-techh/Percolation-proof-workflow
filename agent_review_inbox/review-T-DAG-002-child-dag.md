---
kind: review_result
task_id: T-DAG-002
source_agent: Codex
created_at: 2026-09-06T21:30:00-06:00
integration_status: pending
---

# T-DAG-002 — explicit child-DAG refinement

## Scope and evidence

This is a read-only design result.  It inspected the current M4 cone report
(`review-T-M4-001-cone.md`) and the existing Route-B state projection.  The
reported checkpoint is revision `331`, with 64 nodes and all current nodes
open.  The explicit cone currently encodes

`P0 → P1 → P2 → P3 → P4 → P5 → P6 → P8 → M4`,

which is a conservative prerequisite chain, not a faithful representation of
the independent source, algebra, coverage, and terminal-transfer obligations.
This report proposes a child projection; it does not migrate or mutate that
state graph.

## Proposed child DAG

The names below are stable names, not new state IDs.  A child is *admission-
eligible* only when its listed dependencies are admitted at the same evidence
level and its own receipt is fresh.

| child node | dependencies | independent work / admission boundary |
|---|---|---|
| `P3.source_manifest_binding` | `P0.reproducibility_baseline`, `P2.spectral_partition` | Bind canonical Julia source commit, coordinate order, DH convention, and source hashes.  Does not prove numerical bounds.  Admission requires manifest/hash agreement, not sampling. |
| `P3.ieee_trace_entry_M44` | `P3.source_manifest_binding` | Replay one fixed cell and one mass entry with operation-level Float64/rounding witness, then reify the exact spelling.  Admission is only a single-entry semantic bridge; no global interval claim. |
| `P3.mass_box_soundness` | `P3.source_manifest_binding`, `P3.ieee_trace_entry_M44` | Prove the interval/Taylor enclosure for the declared mass block on the fixed cell.  Requires a certified evaluator and coverage of that cell; it cannot be admitted from equal bits or a point sample. |
| `P3.cg_inverse_bounds` | `P3.source_manifest_binding` | Independently bind and enclose `C`, `G`, and the inverse/solve residual under the same coordinate and arithmetic contract.  It must not inherit mass soundness merely because both use the same CSV. |
| `P3.coverage_partition` | `P2.spectral_partition`, `P3.mass_box_soundness`, `P3.cg_inverse_bounds` | Prove disjoint cell coverage, boundary ownership, and interval enclosure on every cell.  A finite list of payload rows is insufficient without a completeness certificate. |
| `P4.residual_normalization` | `P3.source_manifest_binding` | Establish the typed map between force residual `l = I f - M0 a` and any acceleration-side residual used by the PMI.  Admission requires explicit mass/anti-mass hypotheses and dimensional consistency; no silent reuse of `l` as `d`. |
| `P4.abstract_schur_absorption` | `P4.residual_normalization` | Kernel-check the rational Schur/Young/PMI inequality for the declared symbols.  This is reusable abstract algebra only; it does not bind the witness to true DH. |
| `P4.true_dh_residual_cell` | `P3.coverage_partition`, `P4.residual_normalization`, `P4.abstract_schur_absorption` | Bind actual DH residual coefficients and prove the PMI envelope on one named cell.  Requires source trace, exact payload hash, and checker receipt. |
| `P4.true_dh_residual_coverage` | `P4.true_dh_residual_cell`, `P3.coverage_partition` | Aggregate the cell certificates with no gaps/overlaps and preserve sign conventions at boundaries.  This is the P4 global coverage gate. |
| `P5.energy_syzygy` | `P4.residual_normalization` | Reuse the exact Newton–Euler energy identity/zero residual syzygy.  Admission is limited to the exact declared model and does not imply sparse SOS feasibility. |
| `P5.sparse_sos_cell` | `P4.true_dh_residual_cell`, `P5.energy_syzygy` | Prove the sparse/disjunctive SOS certificate on one cell with exact Gram identity and multiplier side conditions.  Solver `OPTIMAL` is not evidence. |
| `P5.sparse_sos_coverage` | `P5.sparse_sos_cell`, `P4.true_dh_residual_coverage` | Close all selected cells and the disjunction/partition logic.  Admission requires exact Gram/identity receipts and complete cell coverage. |
| `P6.gram_reification` | `P5.sparse_sos_cell` | Reify every rational Gram entry and polynomial identity in pinned Lean/checker artifacts.  A decimal-to-rational conversion alone is not enough. |
| `P6.global_interval_checker` | `P3.coverage_partition`, `P4.true_dh_residual_coverage`, `P5.sparse_sos_coverage`, `P6.gram_reification` | Run the pinned interval/checker aggregation and retain hashes, versions, and negative attempts.  This produces external evidence, not registry `VERIFIED`, until the Lean adapter and comparator also pass. |
| `P8.state_contract_binding` | `P0.reproducibility_baseline` | Choose and freeze either the 14-state ramp contract or an explicit-time 13-state contract.  The current 13-state `du[13]=0` cannot be silently lifted to `w'=c`. |
| `P8.rhs_interval_containment` | `P8.state_contract_binding`, `P3.coverage_partition` | Bind the selected true-DH RHS to interval outward bounds on the reachable domain.  Conditional interface scaffolds do not satisfy this node. |
| `P8.flowpipe_local_step` | `P8.rhs_interval_containment`, `P6.global_interval_checker` | Prove a local Picard/flowpipe enclosure with step-size, Lipschitz, and invariant hypotheses.  Endpoint payloads or trajectory plots do not close it. |
| `P8.flowpipe_global_coverage` | `P8.flowpipe_local_step`, `P3.coverage_partition` | Compose local steps through the full finite horizon, including exits and domain boundaries.  Requires a continuation/first-exit argument. |
| `P8.terminal_transfer` | `P8.flowpipe_global_coverage`, `P5.sparse_sos_coverage` | Transfer the certified terminal reachable set into the block-(4,5) certificate hypotheses, with explicit coordinate/order and sign adapters. |
| `M4.block45_assembly` | `P4.true_dh_residual_coverage`, `P5.sparse_sos_coverage`, `P6.global_interval_checker`, `P8.terminal_transfer` | Assemble the finite-horizon theorem and all typed adapters.  It is not eligible while any child is merely compiled, pending, or externally `evidence_complete`. |
| `M4.comparator_and_kernel` | `M4.block45_assembly` | Require exact statement comparator, pinned Lean kernel build, zero `sorry`/`admit`, no nonstandard axiom, and CI receipt.  Only this terminal child can authorize M4 admission. |

## Parallel frontier after projection

After the shared `P3.source_manifest_binding` and `P8.state_contract_binding`
contracts are available, the following branches can proceed independently
subject to their local prerequisites:

1. `P3.ieee_trace_entry_M44 → P3.mass_box_soundness → P3.coverage_partition`;
2. `P4.residual_normalization → P4.abstract_schur_absorption`;
3. `P5.energy_syzygy` (the already audited exact identity branch);
4. `P8.rhs_interval_containment` (after the state-contract choice).

Once a named P4 cell exists, `P4.true_dh_residual_cell` and
`P5.sparse_sos_cell` can run concurrently with `P3` work on disjoint cells,
provided all artifacts carry the same source-manifest hash.  `P6` is a
consumer/reification branch, while P8 local flowpipe work can run in parallel
with P4/P5 after RHS containment is independently bound.  `M4` remains a
join, not a scheduler shortcut.

## Admission boundaries

- `compiled_candidate`, decimal/IEEE reification, solver success, and
  `evidence_complete` remain external or conditional evidence.
- Abstract algebra children may be `VERIFIED` only for their exact abstract
  statements; they do not close their physical parent.
- Source-binding children require canonical source identity, coordinate
  convention, arithmetic semantics, and fresh receipts.  Equal Float64 bits
  are not a Julia/DH semantic proof.
- Coverage children require a completeness certificate, not a finite sample or
  finite payload count.
- P8 requires a selected 13- or 14-state theorem contract, actual RHS
  containment, and global flowpipe/terminal-transfer proofs.
- `verified registry` promotion is separate from every child completion and is
  permitted only through the existing strict receipt/comparator gate.
- Until all M4 children and `M4.comparator_and_kernel` pass, the global
  `formal_certificate_allowed` flag must remain false.

## Migration risks and mitigations

| risk | consequence | mitigation |
|---|---|---|
| Replacing existing parent nodes instead of adding a projection | Loss of historical attempts or broken IDs/dependents | Keep current nodes immutable; add child records with explicit `derived_from` and migration version. |
| Treating the present chain as proof order | Artificial serialization or unsafe parallel admission | Use child-level edges for scheduling only; preserve parent gates and require all join edges at M4. |
| Mixing force and acceleration residuals | Dimensionally invalid PMI transfer | Keep `P4.residual_normalization` as a mandatory typed adapter with separate receipts. |
| Reusing a payload across source revisions | Stale or misbound true-DH evidence | Include source manifest hash, payload hash, coordinate order, and arithmetic/runtime version in every receipt. |
| Zero-tail or implicit 13→14 lift | False reachability contract (`du[13]=0` versus `w'=c`) | Freeze `P8.state_contract_binding` before any flowpipe admission; require explicit-time theorem if 13-state source remains. |
| Marking abstract Lean leaves as physical theorem closure | Registry pollution and false M4 progress | Store theorem scope and admission level separately; never infer physical binding from kernel success alone. |
| Adding children with incomplete reverse edges | Incorrect frontier and premature parent closure | Recompute dependents, cycle-check, and compare the projected graph against the manifest before migration. |
| Broad migration during active agents | Merge conflicts and lost unprocessed reviews | Perform an append-only migration after inbox review; do not rewrite queue/state in this task. |

## Recommended migration order (future task, not performed here)

1. Freeze a versioned child-DAG manifest and retain the current 64-node graph.
2. Add child nodes as `open` with `derived_from` links; do not close existing
   parents or modify the registry.
3. Attach existing receipts only as provenance, preserving their weaker
   admission states.
4. Run cycle/dependent consistency checks and a focused frontier snapshot.
5. Let agents claim disjoint child nodes; merge only review files first.
6. Promote physical parents only through the existing strict gate and only
   after the M4 join and comparator/kernel child succeed.

No state, registry, queue, external source, or full regression was modified
by this report.
