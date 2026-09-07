# Agent review integration log

This log records durable integrations from `agent_review_inbox/`. The original
review files and their SHA-256 markers remain in that directory.

## 2026-09-06 / Route-B checkpoint revision 348

Integrated as pending metadata only:

| task | target | classification | admission effect |
|---|---|---|---|
| T-P3-001 | `P3.strict_true_dh_bounds` | `compiled_candidate` | none |
| T-P4-001 | `P4.residual_schur_pmi` | `pending` | none |
| T-WF-001 | `P0.reproducibility_baseline` / workflow audit | `documentation_only` | none |
| T-P8-001 | `P8.independent_reachability` | `blocked_current_contract_conditional_adapter` | none |
| T-P3-002 | `P3.strict_true_dh_bounds` | `pending_runtime_blocked` | none |
| T-P4-002 | `P4.residual_schur_pmi` | `pending` | none |
| T-P8-002 | `P8.independent_reachability` | `architecture_decision_pending_contract_change` | none |
| T-M4-001 | `M4.block45_full_certificate` | `frontier_serialization_observed` | none |
| T-P0-001 | `P0.reproducibility_baseline` | `reproducibility_baseline_blocked` | none |
| T-DAG-002 | `M4.block45_full_certificate` | `child_dag_refinement_proposal` | none |
| T-P3-003 | `P3.strict_true_dh_bounds` | `pending_source_manifest_binding` | none |
| T-P4-003 | `P4.residual_schur_pmi` | `conditional_typed_normalization` | none |
| T-P8-003 | `P8.independent_reachability` | `explicit_time_contract_recommended` | none |
| T-P4-004 | `P4.residual_schur_pmi` | `conditional_typed_normalization_sidecar` | none |
| T-P5-001 | `P5.sparse_disjunctive_sos` | `energy_syzygy_reuse_audit` | none |
| T-P8-004 | `P8.independent_reachability` | `explicit_time_typed_sidecar` | none |
| T-P3-004 | `P3.strict_true_dh_bounds` | `pending_source_semantic_adapter` | none |
| T-FLT-DERIV-CALC | external reuse catalog | `flt_derivation_calculus_scan` | none |
| T-FLT-TOPOLOGY-QUOTIENT-CLM | external reuse catalog | `flt_topology_quotient_scan` | none |
| T-P3-005 | `P3.strict_true_dh_bounds` | `pending_semantic_binding_child` | none |
| T-P5-002 | `P5.sparse_disjunctive_sos` | `pending_energy_child` | none |
| T-P3-006 | `P3.strict_true_dh_bounds` | `pending_semantic_binding_sidecar` | none |
| T-P5-003 | `P5.sparse_disjunctive_sos` | `pending_christoffel_power_sidecar` | none |
| T-FLT-SPECTRAL-LINEAR | external reuse catalog | `flt_spectral_linear_scan` | none |
| T-FLT-INFRA-REGISTRY | external reuse catalog | `flt_registry_graph_scan` | none |
| T-FLT-TRANSPORT-ADAPTER | external reuse catalog | `flt_transport_adapter_scan` | none |
| T-FLT-SPECTRAL-SIDECAR | external reuse catalog | `flt_spectral_sidecar` | none |
| T-FLT-SPECTRAL-PREDICATE | external reuse catalog | `flt_spectral_predicate_sidecar` | none |

The authoritative `artifacts/routeb_6dof/state.json` was updated through
`StateStore` from revision 328 to revision 348. Twenty-three Route-B
`agent_review_integrated` events, twenty-three node provenance references, and
nine event-only external-catalog integrations were added. Node statuses remain
open and the verified registry remains empty.

No review was promoted to `VERIFIED`; P3 source semantics, P4 true-DH residual
binding, P8 contract/flowpipe coverage, and M4 admission remain open.

P0 remains blocked by current snapshot drift and missing fresh receipts.  The
child-DAG proposal is retained as a projection only; it does not migrate the
64-node authoritative graph or change theorem statements.

The P3 review leaves source semantics pending, P4 remains a conditional typed
adapter, and P8 recommends freezing an explicit-time 13-state contract. None
of these results closes a physical parent or adds a verified registry entry.

P3 and P4 were later revised under the same filenames by agents.  The inbox
integrator retained both prior hashes and recorded the new hashes as explicit
revisions; no review evidence was silently overwritten.

P4-004 confirms a focused exact-real typed normalization sidecar, while P5-001
finds reusable energy/power bridges but no dedicated source-authenticated
Newton–Euler syzygy. Both remain below physical parent admission.

P8-004 supplies a focused explicit-time 13-state interface sidecar with the
`c` parameter external to the state vector. It remains conditional and does
not establish source binding, flowpipe coverage, or terminal transfer.

P3-004 confirms the smallest source-semantic adapter remains premise-driven:
hash equality is provenance only, while Julia Float64 semantics and Lean exact
semantics still require a separate machine-checkable binding receipt.

The two Anthropic FLT scans are retained as advisory, provenance-bearing
catalog events only. They do not create Route-B nodes, alter theorem
dependencies, or qualify any theorem for registry promotion.

P3-005 narrows the semantic-binding frontier to a premise-driven composition
of the canonical source manifest, exact snapshot, abstract true-DH semantics,
and interval enclosure. P5-002 identifies the exact Christoffel power identity
as the smallest standalone energy child; both remain pending and below parent
closure.

P3-006 implemented that interface as a new sidecar, but its focused compile is
blocked by the local missing Mathlib environment (`unknown module prefix
'Mathlib'`). P5-003 implemented the isolated Christoffel-power sidecar and its
focused compile passed with only the standard Lean base axioms; this remains a
pending reusable child and does not promote the physical P5 parent.

The spectral scan identifies an eigenspace/range bridge as the highest-value
current-pin candidate and keeps representation-specific exact-sequence results
below direct reuse until independently recompiled. The infrastructure scan
confirms that challenge/solution comparison, permitted-axiom gates,
route/stage/landmark metadata, and extract-graph-render-selfcheck are
architecture or contract inputs only; none is proof evidence by itself.

The spectral sidecar compiles with its focused harness, but it is an abstract
self-contained bridge rather than a direct proof of the upstream FLT
declaration. It remains advisory/pending and is not a Route-B spectral closure
or verified-registry entry.

An independent admission review further found that the sidecar's concrete
statements are tautological range identities and contain no eigenspace
predicate. Its compile result is retained as a negative/architecture-only
finding. A corrective predicate-bearing sidecar is queued; the original is not
treated as spectral theorem reuse.

The corrective predicate-bearing sidecar now contains an actual
`T v = μ • v` eigenspace condition and a range-to-eigenspace theorem. Two
independent reviews agree that it remains an abstract local adapter rather than
direct upstream reuse; focused Lean compilation is blocked by missing or
incompatible Mathlib object files, so no kernel evidence or registry promotion
is claimed.

Su Mengchen's reconciliation review records that those two reviews inspected
successive sidecar versions rather than identical source bodies: the earlier
review covers the generic `eigenspaceSet` form, while the current version uses
the concrete `Fin 2 → ℚ` canonical eigenspace. Their differing source hashes
are preserved as provenance, and the current predicate sidecar remains pending
until the pinned Mathlib environment is repaired and the exact source is
recompiled.
