---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-aligned-path-cap-consumer-20260908T112016Z
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T11:20:16Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing
admission_label: pending
proposed_integration_target: metadata_only
requested_action: review_bounded_aligned_path_cap_composition_and_obtain_independent_Lean_receipt
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.lean
artifact_sha256: f698d8c56c83005df0e0a907452ae7a6f083eb3736e6df60db4d0190084367dd
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ALIGNEDPATHCAPCONSUMER20260908.review.md
companion_sha256: 78b3df7ce36089f9d0c63b0ff297cb04a2681509b581a99775243b944c1c5639
---

# BODY6 bounded consumer: INITIALPATHCAPS + ACTUALSTORAGEALIGN

This submission is one 74-line mathematical composition under the existing
BODY6 task. It creates no task/state node, closes no parent theorem and
requests metadata review only. No collector command or registry/state
mutation was performed.

## Consumer and premises

The fixed Model contains H, Ma, Me, U, Uzero and p. Source is the existing
ActualStorage f=1,h=0 specialization; target is encoded kinetic+W+B on the
same mechanical state (q,v), with B=4079979/400000.

`ConsumerPremises` explicitly requires:

1. ACTUALSTORAGEALIGN.Alignment on configuration domain Q.
2. InitialSetCap for the same source on X0 at upper a.
3. path(0) in that X0.
4. IntegratedGrowth for the same source/path with increment b(t).
5. Uniform increment bound b(t)<=beta on [0,1].
6. Full-state domain D(t) projects into Q.
7. The whole path lies in D(t), not merely its initial point.
8. The exact shifted budget a+beta+B<=bar.

`consume_aligned_path_cap_attempt` gets the shifted value identity from
ACTUALSTORAGEALIGN and passes it to INITIALPATHCAPS. Its only conclusion is
the full target cap bar along the given path. The intermediate source cap
is a+beta; B is charged once. No premise is inferred from the desired cap
or from a matching scalar V0.

## Exact counterexample

For the normalized encoded potential Uzero=U(0) and constant origin path
(q,v)=(0,0), source is identically zero for arbitrary H,p,M. It therefore
has a full source cap zero. The shifted target is identically
B=4079979/400000>1, so a target cap one fails. The new counterexample lemma
uses the existing exact origin identities to show that even a full source
cap does not pay a missing shift budget. This is not an asserted DH solution
or a controller-failure theorem; the required budget 0+B<=1 is simply false.

## Limits and validation

No actual candidate or ConsumerPremises instance is supplied. There is no
proof of gap/coefficient feasibility, growth, path inclusion, kinematics,
ODE/continuation, physical source semantics, circle invariance, full-system
Schur claims or registry eligibility. An already shifted cap must use the
appropriate prior consumer without another B.

The new source imports OPEN_UNCOMPILED INITIALPATHCAPS and ACTUALSTORAGEALIGN;
PATHDOMAINPROJECTION is a pending transitive dependency. Old compiled
ActualStorage/ActualShift receipts do not cover this new composition.
Only targeted signature/hash/static checks were performed. No Lean/Lake
or broad regression ran. Independent elaboration and axiom/dependency
receipts remain missing. Keep OPEN_UNCOMPILED and integration pending.
