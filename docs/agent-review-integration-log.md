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

## 2026-09-07 / Route-B checkpoint revisions 349–350

The focused P3 mass-entry compile receipt was persisted at revision 349 as a
conditional graph artifact. It is explicitly source-unbound and did not enter
the verified registry. Su Mengchen's `T-P0-002` review was then integrated at
revision 350 as pending metadata:

| task | target | classification | admission effect |
|---|---|---|---|
| T-P0-002 | `P0.reproducibility_baseline` | `pending_fresh_receipt_reaudit` | none |

The review establishes that the historical receipt is evidence only for its
old snapshot. The current canonical state has moved, and no deterministic
fresh receipt/output-hash binding was found; a Git blob hash is not substituted
for a receipt output hash. The proposed next step is a stable receipt alias or
index followed by an independent hash check. Node statuses remain open, the
verified registry remains empty, and `formal_certificate_allowed` remains
false.

## 2026-09-07 / Route-B checkpoint revision 351

The `T-DAG-003` shared-lemma audit was integrated as architecture-only pending
metadata. It proposes shared nodes for source manifest, true-DH semantic
binding, and pure domain partition completeness, while keeping P3/P4/P5/P8
physical joins explicit. It also identifies that the current dry-run proposal
schema cannot represent multiple shared nodes in one layer without a versioned
schema change. No authoritative graph migration, theorem-statement change,
registry promotion, or admission change was performed.

| task | target | classification | admission effect |
|---|---|---|---|
| T-DAG-003 | `M4.block45_full_certificate` | `pending_shared_lemma_projection` | none |

The authoritative state remains 64 open nodes with an empty verified registry;
the shared projection is retained only as a proposal until its schema,
snapshot binding, acyclicity, and fail-closed migration checks are implemented.

## 2026-09-07 / Route-B checkpoint revision 352

The `T-P7-001` review was integrated as pending triage metadata. The assigned
worker correctly refused to guess a mathematical target from the short label.
The coordinator then bound the task to the external seven-term rational tail
checker and produced `examples/routeb_p7_tail_bound_lean/`, where the two strict
scalar inequalities were proved in Lean with exact rationals. This closes only
the arithmetic child; it does not establish the polynomial's equality to the
deployed true-DH/Float64 source, full residual absorption, flowpipe coverage,
terminal transfer, or M4 admission.

| task | target | classification | admission effect |
|---|---|---|---|
| T-P7-001 | `P7.strict_tail_fallback` | `pending_tail_obligation_audit` + exact arithmetic child | none |

The registry remains empty and `formal_certificate_allowed` remains false.

## 2026-09-07 / Route-B checkpoint revision 353

The coordinator recorded the focused P7 exact-rational child after the external
tail checker passed. The persisted receipt binds the Lean source, verifier,
toolchain, OLean and compile log hashes, and records the seven-term factorization
and both strict scalar inequalities. This is a reusable arithmetic leaf only;
it is not a physical source binding or a global Route-B certificate.

| child | parent | result | admission effect |
|---|---|---|---|
| `RouteBP7Tail.eta01_lt_target`, `eta02_lt_target` | `P7.strict_tail_fallback` | `COMPILED_CANDIDATE` / exact rational arithmetic | none |

State revision 353 retains the child as a conditional graph artifact. P7
source equality, residual absorption, P8 flowpipe, terminal transfer, and M4
kernel/comparator gates remain open; the verified registry is empty.

## 2026-09-07 / Route-B checkpoint revisions 354–355

The `T-P5-004` result was integrated at revision 354. It identifies the exact
scalar input needed for a retained-dissipation closure and warns that a mere
constant residual bound cannot imply global strict decay. The inbox parser was
also repaired to accept this worker's legacy header shape while recording a
format warning, so the mathematical body is now harvestable without weakening
the gates.

At revision 355, the new Lean child
`examples/routeb_p5_residual_power_lean/` was persisted as a conditional graph
artifact. Its five lemmas compile under the pinned Lean toolchain with only
standard axioms. The child remains below physical source binding: `δ`, `ε`,
units conversion, domain coverage, and residual semantics must still be proved
from the deployed Route-B model.

| task/child | target | result | admission effect |
|---|---|---|---|
| T-P5-004 / `RouteBP5ResidualPower.*` | `P5.sparse_disjunctive_sos` | `COMPILED_CANDIDATE` / exact scalar closure | none |

The verified registry remains empty and `formal_certificate_allowed` remains
false.

## 2026-09-07 / Route-B checkpoint revision 356

The `T-P4-005` review was integrated as pending mathematical metadata. It
identified the exact necessary-and-sufficient scalar condition for the PMI
quadratic channel, `r² ≤ p*d*y²`, and showed that the deployed block budget
admits the rational choice `c = 1/4`. It also records the obstruction that a
nonzero additive bias cannot satisfy universal PSD at `y = 0`. No
force/acceleration source binding, coverage, registry promotion, or parent
closure was performed.

## 2026-09-07 / Route-B checkpoint revision 357

`T-P8-006` was integrated as pending mathematical metadata. The review closes
the abstract ramp reconstruction on an interval: `c'=0` and `w'=c` with
`w(0)=0` imply `c(t)=c0` and `w(t)=c0*t`, hence `w(1)=c0` when `1` lies in
the interval. It also narrows the deployed-source boundary to first-12
mechanical binding plus an adapter-supplied ramp tail. A Lean interval child,
ODE existence, flowpipe coverage, and terminal admission are still open.

## 2026-09-07 / Route-B checkpoint revision 358

The focused P4 sharp child `examples/routeb_p4_sharp_residual_lean/` was
recorded as a conditional compiled candidate. Its Schur equivalence,
three-term residual envelope, and quarter-budget inequality compile under the
pinned Lean toolchain with only standard axioms. The child materially weakens
the algebraic bottleneck, but source residual units, true-DH semantic binding,
global cell coverage, and the P4/M4 join remain open. The verified registry
remains empty and `formal_certificate_allowed` remains `false`.
