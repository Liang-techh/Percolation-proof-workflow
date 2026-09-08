---
kind: review_result
review_id: review-GH-MIXED-BODY6-PATH-REASSIGNED-20260908T143002Z
task_id: GH-MIXED-BODY6-PATH-REASSIGNED
source_agent: codex-body6-reassigned-path-lane
created_at: 2026-09-08T14:30:02Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing_for_new_sidecar
admission_label: pending
registry_mutation: false
proposed_integration_target: metadata_only
requested_action: review_contract_preservation_and_focus_check_new_sidecar_without_repeating_passed_main_dependency
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHREASSIGNED20260908.lean
artifact_sha256: 2343ca9a6ad775643e344d2e78d66f4dd7960fa0c10a910fdb9864da1fa402ec
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_PATHREASSIGNED20260908.review.md
companion_sha256: d8d0e5670beb16fb3f3023fdbec71cb3573f29f46bd552cbf0f279809fb35543
---

# Reassigned BODY6 path lane: bounded review result

Independent finding: the PATHDOMAINPROJECTION repair does not change its
contract. Replacing only the current three-line proof intermediate with the
historical one-line transitivity expression, in memory, exactly recovers the
historical source hash. The full comparison and hashes are in the companion.
All binders, five hypotheses, interval and conclusions are preserved.
The unchanged budget cap+B<=bar pays the shift G=F+B once.

The new typed sidecar packages those five hypotheses in TransferInputs and
adapts them directly to the repaired theorem. Its pullback-domain interface
states that whole-path membership in project^-1(Q) is equivalent to projected
membership in Q. It also derives that membership from a specified full-state
D with both DomainProjection and WholePathMembership supplied.

An exact counterexample distinguishes this from membership in an arbitrary
specified D: Q=univ, project=id and path(t)=t satisfy projected membership,
but fail membership in D(t)=(-infinity,0] at t=1. The sidecar reuses the
existing domain counterexample proof. Choosing a pullback does not establish
the actual domain's velocity, lift or other full-state constraints.

The existing 20260908T082220 focused receipt reports successful main
PATHDOMAINPROJECTION compilation and baseline axioms, with the matching
current source hash. No main Lean compilation or passed dependency proof
was repeated. The new sidecar has no compilation/axiom receipt and remains
OPEN_UNCOMPILED/pending.

Actual path inclusion, coordinate binding, DH/source identity, source cap,
integrated growth, ODE/continuation/coverage and admission are not completed
by this review. No regression, inbox integrator, registry/state mutation or
external source write ran. Existing leaves and receipts remain unchanged.
Checks were bounded static inspection, in-memory historical reconstruction,
placeholder scanning and pair/envelope hash validation only.
