---
kind: review_result
review_id: T-DAG-003-CHOUPIZHU-20260906T2148
task_id: T-DAG-003
source_agent: 臭屁猪
created_at: 2026-09-06T21:48:00-06:00
integration_status: pending
admission_label: architecture_only
---

# T-DAG-003 — shared-lemma / DAG projection audit

## Exact question

Can the current Route-B child-DAG be refactored into genuinely shared prerequisite lemmas/contracts so that P3, P4, P5 and P8 can proceed in parallel without weakening any physical/source/coverage gate?

## Inspected commit / paths

Inspected repository head after claim and the immediately preceding roundtable harvest:

- head observed before this result: `0ea5119474bf55cd0c6571cfb0c3447eb4f625e8`
- claim commit: `7ec9e9e5b18139e4fccc2488d79bbfd21523415e`

Files inspected:

- `agent_review_inbox/README.md`
- `agent_review_inbox/task_queue.md`
- `agent_review_inbox/collaboration_board.md`
- `agent_review_inbox/review-T-M4-001-cone.md`
- `agent_review_inbox/review-T-DAG-002-child-dag.md`
- `agent_review_inbox/review-T-P0-002-sumengchen-20260906T2136.md`
- `agent_review_inbox/review-T-P3-005-semantic-binding-child.md`
- `agent_review_inbox/review-T-P4-003-residual-normalization.md`
- `agent_review_inbox/review-T-P5-003-christoffel-power-sidecar.md`
- `agent_review_inbox/review-T-P8-004-explicit-time-sidecar.md`
- `scripts/dry_run_theorem_dag_migration.py`
- `src/percolation_workflow/dry_run_migrator.py`
- `artifacts/routeb_6dof/state.json` (blob identity only; connector did not expose the large JSON body)

## Evidence synthesis

### 1. The authoritative parent graph is still structurally over-serialized

`T-M4-001` recorded the explicit parent cone as the chain

`P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 -> P8 -> M4`.

That report explicitly says this is graph-theoretic serialization, not a mathematical requirement. `T-DAG-002` already proposed child-level refinement, but several proposed children still carry branch-local names for prerequisites that are actually shared by multiple physical branches.

### 2. Source provenance and physical semantics should be shared, not owned by P3

`T-P3-005` cleanly separates:

1. source provenance/hash/manifest facts;
2. exact snapshot reconstruction;
3. semantic enclosure / true-DH interpretation.

Those facts are consumed not only by P3 mass bounds, but also by P4 true-DH residual binding and P8 RHS containment. Therefore a P3-namespaced node such as `P3.source_manifest_binding` should not be the conceptual owner of the common contract.

Recommended shared nodes:

- `S.source_manifest_contract`
- `S.true_dh_semantic_binding`

The first records canonical source root, coordinate order, arithmetic/runtime parameters and hashes as provenance only. The second is the typed semantic bridge that makes a concrete true-DH source interpretation available to downstream physical claims. Neither node may claim that hash equality proves semantic equality.

### 3. Partition completeness is a shared geometric lemma and should be split from quantity-specific interval soundness

`T-DAG-002` placed `P3.coverage_partition` after both mass and C/G interval children. That creates an unnecessary dependency when P4 and P8 merely need the geometric fact that the declared cells cover the target domain with explicit boundary ownership.

Recommended split:

- `S.domain_partition_complete`: pure partition/coverage lemma, depending on the frozen P2 partition contract and no P3 mass/C/G enclosure theorem.
- `P3.mass_box_soundness` and `P3.cg_inverse_bounds`: quantity-specific interval facts over cells, each depending on `S.true_dh_semantic_binding` and the cell contract.
- `P4.true_dh_residual_cell`: depends on `S.true_dh_semantic_binding`, `S.domain_partition_complete` (or a named cell extracted from it), and `P4.residual_normalization`.
- `P8.rhs_interval_containment`: depends on `S.true_dh_semantic_binding`, `S.domain_partition_complete`, and `P8.state_contract_binding`.

This allows P3, P4 and P8 physical binding work to advance on disjoint quantities/cells without waiting for a P3-global coverage join.

### 4. The abstract P5 Christoffel identity should not depend on P4 residual normalization

`T-DAG-002` proposed `P5.energy_syzygy -> P4.residual_normalization`. But `T-P5-003` compiled the Christoffel power identity in an isolated Mathlib-only sidecar and explicitly imports no P4 source binding, SOS, reachability or terminal-transfer theorem.

Therefore the abstract algebraic node should be independent:

- `P5.christoffel_power_identity` has no physical P4 dependency.
- A later physical/SOS node may depend jointly on `P5.christoffel_power_identity`, `P4.true_dh_residual_cell`, and the relevant source/coverage contracts.

This removes a false scheduling edge while preserving the physical join where it actually belongs.

### 5. P8 contract work is independently available, but terminal transfer must remain a separate join

`T-P8-004` already isolates the 13-state explicit-time contract, projection from the 14-state parent, and terminal-transfer predicate. This supports keeping `P8.state_contract_binding` independent of P3/P4/P5 physical evidence. However `P8.terminal_transfer` must remain downstream of global flowpipe coverage and the certificate-side assumptions it transfers into.

### 6. Fresh receipt/provenance is a workflow gate, not a substitute for any shared mathematical lemma

`T-P0-002` reports current state revision `364` and finds no stable fresh receipt/output-hash binding for that current snapshot. The shared-DAG projection must therefore remain proposal-only. P0 freshness can gate migration/install receipts, but it must not be treated as proof of source semantics, domain coverage, residual absorption, or reachability.

## Proposed projection

The smallest useful projection is:

```text
P0.reproducibility_baseline
P2.spectral_partition
        |
        +--> S.source_manifest_contract --> S.true_dh_semantic_binding
        |
        +--> S.domain_partition_complete

P4.residual_normalization          (abstract, independent)
P5.christoffel_power_identity      (abstract, independent)
P8.state_contract_binding          (contract, independent)

S.true_dh_semantic_binding + S.domain_partition_complete
        +--> P3.mass/C/G cell bounds --> P3.quantity_coverage
        +--> P4.true_dh_residual_cell + P4.residual_normalization
        |        --> P4.true_dh_residual_coverage
        +--> P8.rhs_interval_containment + P8.state_contract_binding
                 --> P8.flowpipe_local_step --> P8.flowpipe_global_coverage

P5.christoffel_power_identity + P4.true_dh_residual_cell
        --> P5.sparse_sos_cell --> P5.sparse_sos_coverage

P8.flowpipe_global_coverage + P5.sparse_sos_coverage
        --> P8.terminal_transfer

P4.true_dh_residual_coverage
+ P5.sparse_sos_coverage
+ P6.global_interval_checker
+ P8.terminal_transfer
        --> M4.block45_assembly --> M4.comparator_and_kernel
```

Important: `S.domain_partition_complete` proves only domain/cell completeness and boundary ownership. It does **not** prove that any particular mass, residual, SOS or RHS enclosure is valid on those cells.

## Shared-node admission boundaries

| proposed node | strongest admissible claim | forbidden inference |
|---|---|---|
| `S.source_manifest_contract` | provenance/contract metadata with exact hashes and parameters | hash equality => semantic equality |
| `S.true_dh_semantic_binding` | typed physical/source semantic bridge under explicit runtime/exact-real premises | one-point/Float64 match => global interval soundness |
| `S.domain_partition_complete` | complete cell cover + boundary ownership | partition completeness => quantity enclosure |
| `P4.residual_normalization` | abstract typed force/acceleration conversion under explicit hypotheses | force residual => PMI `d` without bridge |
| `P5.christoffel_power_identity` | exact abstract algebraic identity for its stated model | abstract identity => physical/SOS closure |
| `P8.state_contract_binding` | selected 13-state explicit-time or justified 14-state contract | contract scaffold => flowpipe coverage |

## Dry-run migrator compatibility

The existing `dry_run_migrator.py` is fail-closed and useful, but its schema currently requires exactly seven proposed nodes with exactly one `entry_contract_layer` for each `L0` through `L6`. A shared-node projection like the one above naturally has multiple independent nodes in the same logical layer and cross-branch shared prerequisites.

Therefore this projection should **not** be forced into the existing `routeb-entry-dag-proposed-patch-v1` format. The next architecture task should either:

1. introduce a new proposal schema for shared nodes/cross-branch edges, while retaining snapshot revision/hash/root binding, unique IDs/names, open-only insertion, registry fail-closed checks, dependency resolution, cycle checking and state-read-only validation; or
2. generalize `complete_layers` from exactly-one-per-L0-L6 to an explicitly declared allowed layer multiset, with a compatibility mode for the old schema.

No migration or schema edit is performed in this review.

## Commands / checker evidence

This run used connector-side repository reads and commit enumeration only. No local Lean/Python runtime was available through the GitHub connector and no broad regression was appropriate for this architecture task.

Observed executable/checker actions:

- GitHub file reads: success
- GitHub directory/content enumeration: success
- GitHub commit enumeration: success
- state JSON body parse: not available through connector (large file body was not exposed); current blob identity was available
- Lean compile: not run; not required for this graph-only result
- `dry_run_theorem_dag_migration.py`: not run because no compatible proposal file was created and the current schema would reject this multi-node-per-layer shared projection by construction

## Source identities / hashes

Git blob SHA values observed during this audit:

- `agent_review_inbox/README.md`: `b10966fd088425d2b7d9b612807bb65b4146e0c7`
- `agent_review_inbox/task_queue.md`: `114a33cb7f4d8d2e7f617b9ae06dd8704d8181ee`
- `agent_review_inbox/review-T-DAG-002-child-dag.md`: `d9dd5ab4a551624330f95bfe0586b9dedb6e8820`
- `agent_review_inbox/review-T-M4-001-cone.md`: `5bf3c8e8d7a0c95c1557dfb5379ce9d2fb92c2e0`
- `agent_review_inbox/review-T-P0-002-sumengchen-20260906T2136.md`: `fe72a778f653ee3b26f7d14ce0ba89569d0e8896`
- `agent_review_inbox/review-T-P3-005-semantic-binding-child.md`: `9448715135e881db37c76f2c5863e3b416afab3e`
- `agent_review_inbox/review-T-P4-003-residual-normalization.md`: `758471955a37f3d068b158a5d0f95fe6967603ea`
- `agent_review_inbox/review-T-P5-003-christoffel-power-sidecar.md`: `34807629f3ffc7e35b559c1b17dd15c7bb310069`
- `agent_review_inbox/review-T-P8-004-explicit-time-sidecar.md`: `fba853c9378c992742e7777dbf557ebef7aaaec2`
- `src/percolation_workflow/dry_run_migrator.py`: `50ec752f2756294a4b23682aa6bee4ccee7dacab`
- `artifacts/routeb_6dof/state.json` Git blob SHA: `aa7b47fea9619deaf7537dc499f1ef524134f85f`

Git blob SHAs are repository object identities, not receipt SHA-256 values and not proof evidence by themselves.

## Proposed integration

- Integrate this result as DAG/design metadata only.
- Do not mutate current state, registry, parent status, theorem statements or existing reviews.
- For the next DAG migration proposal, factor out `S.source_manifest_contract`, `S.true_dh_semantic_binding` and `S.domain_partition_complete` before attaching branch-local physical children.
- Remove the scheduling-only edge from abstract `P4.residual_normalization` to abstract `P5.christoffel_power_identity`; keep their physical descendants joined later.
- Extend or version the dry-run proposal schema before attempting installation, preserving all current fail-closed snapshot/cycle/registry invariants.

## Admission decision

`architecture_only`.

This review improves the dependency model and identifies two false serializations, but it supplies no new physical, coverage, Lean/kernel, receipt or registry evidence. It cannot promote P3/P4/P5/P8/M4.

## Unresolved blockers

1. Current revision-364 fresh receipt/output-hash binding remains pending per `T-P0-002`.
2. No installed shared-node proposal/schema exists yet.
3. `S.true_dh_semantic_binding` remains a real physical/source obligation, not solved by this graph projection.
4. Domain partition completeness must be proved independently from quantity-specific interval enclosure.
5. P4 physical residual-to-PMI binding, global coverage, P8 RHS/flowpipe coverage, terminal transfer and M4 comparator/kernel gates remain open.

## Response / handoff

臭屁猪 claimed the :46 shared-lemma/DAG slot and produced a proposal-only projection. The main actionable result is to stop using P3-namespaced provenance/coverage nodes as shared prerequisites: split common source semantics and pure domain partition completeness into explicit shared nodes. A second concrete correction is that the already compiled abstract Christoffel power identity should not be scheduled behind P4 residual normalization; only the later physical/SOS child needs that join. Before any migration, update/version the dry-run schema so it can represent multiple shared nodes in the same layer without weakening its snapshot, acyclicity and registry fail-closed checks.
