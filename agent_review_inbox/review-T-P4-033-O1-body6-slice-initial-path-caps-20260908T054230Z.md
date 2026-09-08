---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-initial-path-caps-20260908T054230Z
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T05:42:30Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing
admission_label: pending
proposed_integration_target: metadata_only
requested_action: review_initial_growth_full_cap_and_shift_budget_seams_then_obtain_independent_Lean_receipt
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.lean
artifact_sha256: 5cad04f2e8b0af13c8d8a099455812fe1f6d17a66a0d567be5b85963252d224f
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_INITIALPATHCAPS20260907.review.md
companion_sha256: 77c3163be8a009388d995208a01603fe5988665ff505f05eff67d98e0965e3c0
---

# BODY6 lane: initial cap, integrated growth and full-path cap

This review belongs to the existing `T-P4-033-O1-body6-slice` lane as a
bounded advisory companion. It creates no state node, closes no source/body
theorem and requests no registry promotion. No collector/integration command
or processed marker was issued by this submission.

## Four separate mathematical statements

- `InitialSetCap X0 F a`: every x in the specified initial set satisfies
  F(0,x)<=a.
- `InitialPathCap F path a`: F(0,path(0))<=a. This follows from the previous
  statement only when path(0) is proved to belong to that same X0.
- `FullPathCap F path cap`: F(t,path(t))<=cap throughout [0,1].
- `IntegratedGrowth F path b`: F(t,path(t))<=F(0,path(0))+b(t) throughout
  [0,1]. This is an explicit dynamic/integrated premise, not inferred from
  a derivative identity or a scalar CSV.

`growth_supplies_full_cap_attempt` combines InitialPathCap at a, the
integrated growth premise and a uniform b(t)<=beta to produce FullPathCap
at a+beta. No source/path identity is omitted in the types. The subsequent
consumer composes that result with PATHDOMAINPROJECTION's same-domain
projection, whole-path membership and shifted-value identity.

## Shift budget

`ShiftBudget cap B bar` is the distinct arithmetic statement cap+B<=bar.
The composed barrier requires `(a+beta)+B<=bar`; a source initial bound
alone proves neither beta nor this inequality.

With ActualShift's B=4079979/400000>1, no nonnegative unshifted cap satisfies
cap+B<=1. If the full source cap includes an initial point of energy zero,
its cap must be nonnegative, giving an exact logical budget obstruction.
This is not a failure theorem for the controller. An already-shifted cap
is instead consumed without adding B again by the prior companion.

## Exact hump counterexample

Define F(t,x)=8*t*(1-t) on Unit-valued states and use the constant path.
InitialSetCap with a=0 holds for all initial states; F is nonnegative on
[0,1] and equals zero at t=1. Yet F(1/2)=2, so FullPathCap with cap=1 fails.

The exact proof attempt shows why initial bounds, nonnegativity and terminal
zero cannot replace integrated growth or a full-path upper cap. It is an
abstract smooth logical example, not a concrete DH solution or a claim
against a fully instantiated compiled storage theorem.

## Existing evidence and limits

ActualStorage's successful receipts cover conditional initial upper
theorems, domain nonnegativity and synthesis terminal equality. ActualShift
provides a conditional pointwise block/shifted-energy comparison. They do
not supply a current same-source actual-path upper tube. The barrier CSV
records a scalar margin but still has descriptor_flowpipe_closed=False,
fd_remainder_semantics_closed=False and formal_certificate_allowed=False.
Calling those records a compiled full-path ledger would overstate them.

The source and companion hashes are in the envelope. No Lean/Lake or wide
regression ran. The new leaf imports the also-uncompiled PATHDOMAINPROJECTION
leaf and has no independent compiler/axiom receipt. Keep OPEN_UNCOMPILED and
integration pending until those receipts and concrete initial/path/growth/
source/shift-budget instantiations are supplied. Registry/state are unchanged.
