---
kind: review_result
review_id: review-T-P4-ACTIVE-ENERGY-ORIGIN-LOCAL-20260908T161455Z
task_id: T-P4-ACTIVE-ENERGY-ORIGIN
source_agent: codex-active-energy-origin-takeover
created_at: 2026-09-08T16:14:55Z
integration_status: pending
admission_label: pending
status: ACTUAL_TARGET_STORAGE_IDENTITY_AND_NORMALIZATION_MISSING
proof_status: source_identity_audit_only
source_binding_proven: false
actual_origin_membership_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
generated_constants: false
state_mutation: false
registry_mutation: false
requested_action: identify the actual target storage and its value-level normalization before origin or barrier transfer
---

# Active-energy origin: minimal source-identity obstruction

This takes over the unfinished source/API direction, not the existing generic
normalization mathematics. Only this new review is written. No constants,
origin values, bounds or execution evidence are generated. No producer,
Julia, Lean, solver or regression runs; no state or registry writes.

## Current source findings

External source directory E is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.
The following source excerpts were freshly read, not executed:

| Actual object | Source evidence | Missing identity |
|---|---|---|
| Saved V | routeB_export_traj.jl:66-77 reconstructs a polynomial in q4,q5,v4,v5,t from the saved certificate CSV using Float64 parsing | No equality to a six-coordinate physical storage or fixed time normalization |
| Targeted storage derivative | routeB_compact_targeted_nonlinear_strictification_audit.jl:19-35 changes controller gains, includes the mass cross term and differentiates the storage terms | A derivative expression does not select the additive storage constant or identify the active target V |
| Targeted initial bound | routeB_compact_energy_storage_to_block_audit.py uses local targeted-gain envelopes and a block-only initial ball | Its scalar output is not an InitialBoundBinding for a different full-DH storage |
| Active barrier | routeB_compact_block_energy_barrier_audit.py:18,49-54,92-103 reads that initial scalar, sets V_BAR=1 and labels the domain full physical energy | No value-level function V or identity/comparison with the exported storage is supplied |
| Physical source potential | dhport_lib.jl:63-71 sums mass times midpoint height | Its raw additive normalization is not the audited shifted/normalized potential by definition |
| Audited potential | routeB_compact_energy_power_rewrite_audit.jl:102-119 defines Ugrav, a separate positive shift and derivative identities | Power identity leaves the additive normalization open; it is not target-storage selection |

No newer concrete sourcePotential-to-auditedGravity or actual-target storage
instance was found in the bounded examples/*.lean symbol search. Located
SameStorageIdentity/RouteBInitialTransfer uses remain generic definitions and
consumers. This is a scoped absence finding, not an all-files nonexistence claim.

## Best available exact-source lead, without promoting it

The existing review
`review-T-P4-ACTIVE-ENERGY-ORIGIN-source-normalization-codex-20260908T0840.md`
contains a concrete ideal-real DH height/potential derivation, with the claim
that source and audited potentials differ by one additive constant. This
turn consumes it as an uncompiled mathematical candidate; it neither recomputes
nor adopts its numerical constants/bounds as new evidence.

The relevant target is the anchored identity

```text
sourcePotential(q)-sourcePotential(0)
  = auditedGravity(q)-auditedGravity(0).
```

`NEW_BODY6_SLICE_CANDIDATEDOMAIN20260907.lean:155-158` defines sourcePotential
from sourceContract origins and midpoint COMs. Its ExactRealMCGSourceBinding
still requires supplied extensional equalities. The above anchored equality
was not located as a concrete proved instance in the inspected Lean files.
Even if verified, it would bind ONLY the potential part: mass, gain branch,
cross term, linear compensation, time/state map and additive target offset
would still have to match.

This lead is more specific than a derivative identity, but it is not an actual
candidate V identity or a verified Float64 source-refinement theorem.

## Origin normalization: cheapest sufficient witness

The inspected ACTIVEENERGYORIGIN sidecar explicitly defines

```text
E_norm(q,v)=K(q,v)+U(q)-U(0)+controller(q)
E_offset(q,v)=E_norm(q,v)+beta.
```

Its controller expression has no constant term. Its origin equations are
conditional algebra about these definitions. The actual-target consumer
`bound_active_origin_attempt` requires
`hV : V(0,0)=normalizedEnergy(...,0,0)`; it does not construct hV from source.
The weaker direct witness `V(0,0)<=1` is sufficient for origin membership and
need not wait for a global storage theorem. Neither witness is supplied for
the unspecified external active V.

If the source-selected V is E_norm+beta, origin membership at the fixed
threshold is equivalent to beta<=1. This condition is symbolic; no beta is
invented or inferred from a derivative. The existing raw/shifted origin
calculations are deliberately not rerun. Normalizing an alternative expression
does not authorize silently replacing the actual active storage.

For downstream BODY6 use, actual domain inclusion and R(0) source binding are
additional premises; origin membership is not full M/C/G, coverage or flowpipe.

## Additive target storage and valid transfer

If two selected storage functions differ by a proved constant on the relevant
domain, `V_target=V_source+beta`, the same physical sublevel is

```text
V_source<=bar  iff  V_target<=bar+beta.
```

Therefore a source barrier at the fixed threshold does not transfer to the
same target threshold without the required offset condition or budget change.
For an initial upper bound, the target upper bound must similarly include beta.
Derivative equality alone does not identify beta. Equality only along a flow
also does not identify constants across distinct trajectories/initial states.

More importantly, the targeted-gain cross-term storage and original full-DH
storage are not shown to differ ONLY by an additive constant. The general
difference includes the gain quadratic, mass/cross term, potential anchoring,
linear compensation and any time/state map. On the block-only initial set,
some gain terms may vanish, but that is not a whole-domain identity and does
not erase the cross term or transfer a future barrier.

The existing STORAGEIDENTITY sidecar permits a pointwise identity on a domain
containing the initial set/path, or a separately proved comparison with a
budget adjustment. It supplies no concrete RouteBInitialTransfer instance.
No numeric scalar from the targeted producer can replace that missing premise.

## Minimal obstruction and next evidence

The first missing artifact is an unambiguous value-level definition of the
active target V, including source/configuration, state/time coordinates,
mass regularizer, gain branch, potential normalization, linear compensation,
cross term and additive offset. A label such as full physical energy does
not provide this object.

Once V is fixed, choose the smallest intended claim:

- **Origin only:** prove V(0,0)<=1 (or its exact normalized/offset identity),
  plus the downstream domain/source premises actually consumed.
- **Initial bound:** bind the bound to that V and that block-only initial set;
  if borrowing another storage's bound, prove the domain-local comparison.
- **Barrier/target storage:** additionally bind the path derivative budget,
  domain, target threshold and all nonconstant/constant storage differences.

No exact source identity currently supplies this package in the inspected
chain. Status remains pending; no candidate has been promoted. This is a
missing-binding obstruction, not a new numerical impossibility result.

## Fresh SHA256 bindings

External filenames below are relative to E; workspace filenames are explicit.

| Input | SHA256 |
|---|---|
| dhport_lib.jl | aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936 |
| routeB_compact_block_energy_barrier_audit.py | 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927 |
| routeB_compact_energy_storage_to_block_audit.py | 80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9 |
| routeB_compact_targeted_nonlinear_strictification_audit.jl | 41dd63be6fab08b3398913490cb90d5f3571cce2e3ea833c52e9d1b97674f5b1 |
| routeB_compact_energy_power_rewrite_audit.jl | 7a75dbb4cc4297e6d66e1a0d50077d24ce129c5b6e71406e68694c61cd8ae6bf |
| routeB_export_traj.jl | 35ebe806a46273068af1af937c0c0152378d6889024ec5586bf3c7aabd30eccf |
| examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTIVEENERGYORIGIN20260907.lean | c8b1dabcd19491495ee5ff39bff4337851c2224d6f938848988b279246a4f883 |
| examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_STORAGEIDENTITY20260907.lean | 486f16cebdcf6a9c9a370f2519fda1be9c8c577858bace0d9611274606ac4a40 |
| agent_review_inbox/review-T-P4-ACTIVE-ENERGY-ORIGIN-source-normalization-codex-20260908T0840.md | bc1855c6bb33145e85e4fcde1237592ba3dfefeb66844b57cbd20f8b966e4a93 |

Current hashes authenticate inspected bytes only, not theorem validity,
historical execution or registry status. No prior compile receipt was rechecked;
the status of compiled artifacts is not asserted in this review.
