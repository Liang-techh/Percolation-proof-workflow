---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT-20260908T171354Z
task_id: GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT
source_agent: codex-active-binding-minimal-contract
created_at: 2026-09-08T17:13:54Z
integration_status: pending
admission_label: pending
status: CONCRETE_SAME_CONFIGURATION_INSTANCE_MISSING
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
requested_action: instantiate the target identity and raw initial bound with one configuration and the unchanged consumer threshold
---

# Minimal consumable active-V binding contract

Fresh read-only checks confirm the active consumer still reads V0 from
initial_storage_upper and uses V_BAR=1. The candidate assignments still use
Vfull_DH=Kfull_DH+Ugrav_DH+Uctrl_DH with +g0 dot q, and Vshift_DH adds its
declared gravity/controller shift. The existing RouteBInitialTransfer only
consumes supplied sameStorage/exportedInitial/domain evidence; it does not
construct an external-candidate instance.

The current result remains missing binding, not missing candidate syntax.
This review does not repeat origin identities, compare new domains or derive
new Hessian/envelope bounds.

## Contract for the actual consumer

Fix a single configuration K and ONE candidate value function W_K, either
the existing raw Vfull_DH or existing Vshift_DH. Let embed_K map the recorded
block-only state (q4,q5,v4,v5, other q/v zero) to the same physical q/v and
trigonometric lift, with the recorded joint ordering and initial time.

The smallest direct initial contract consists of:

```text
value:    forall x in X0, V_active(x)=W_K(embed_K(x))
initial:  forall x in X0, W_K(embed_K(x))<=u_recorded
scalar:   u_recorded equals the exact parsed initial_storage_upper token
gate:     u_recorded < bar_active
threshold:bar_active equals the current consumer threshold.
```

No field is filled by this review. The gate is not evaluated. This contract
would supply initial inclusion only, not a trajectory/barrier theorem.
For later barrier use, extend value binding to the actual path domain and
provide the same-storage growth, cap and domain-containment witnesses.

Configuration K must identify the mass expression and its single regularizer,
gain branch, source analytic or runtime semantics, potential value convention,
linear compensation vector WITH its source sign, cross-term inclusion or
absence, additive shift, state/time units and relevant source dependencies.
Do not combine these from different candidate configurations under one name.
In particular, replacing +g0 by -g0 requires a proved equality for that K
(e.g. the requisite g0 zero identity), not an origin value calculation.

## Existing-source transfer alternative

If reusing the targeted-storage producer, supply an actual source function U,
its function-indexed initial bound U<=u on X0, and a verified comparison
W_K(embed_K(x))<=U(x)+delta on the same X0. The resulting target upper is
u+delta. To preserve the current consumer's unchanged scalar, additionally
prove u+delta<=u_recorded. Otherwise the existing consumer is not justified
without a separately authorized bound/threshold update. No delta is proposed.

Raw anchors and declared shifts are part of W_K. A bound on a centered
function cannot occupy the raw initial field without the anchor transfer.
The already present cross-term allowance is not automatically missing or
available slack; its source meaning and any reuse require the same K/X0 bound.
CSV equality, derivative flags and equal candidate origin values supply none
of the function-indexed fields above.

## Shortest obstruction

Neither the actual V_active=W_K instance nor a raw same-K initial theorem is
supplied in the inspected chain. Therefore initial_storage_upper cannot yet
be consumed as an initial bound for Vfull_DH or Vshift_DH at the current
threshold. Retain pending; no actual target is selected or redefined here.

## Inspection boundary

Read the existing assignments in external directory
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`:
routeB_compact_dh_full_energy_supply_split_audit.jl,
routeB_compact_dh_storage_shift_audit.jl, and
routeB_compact_block_energy_barrier_audit.py; also the workspace
NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean transfer fields.

Consume the previous initial-binding review
`review-GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING-LOCAL-20260908T170434Z.md`,
whose SHA256 was freshly checked as
`458a131a25e63ce7ddab16e939372a65cc3e61ca7781b1d4b99a826839a1bdaa`.
No existing proof/producer was run, and no historical compile status asserted.
Only this new review is written; no state, registry, old artifact or other
agent file changes. No constants or VERIFIED/source-admission claims.
