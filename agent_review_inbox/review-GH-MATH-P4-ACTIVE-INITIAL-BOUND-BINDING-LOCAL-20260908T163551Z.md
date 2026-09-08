---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING-LOCAL-20260908T163551Z
task_id: GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING
source_agent: codex-initial-bound-source-lane
created_at: 2026-09-08T16:35:51Z
integration_status: pending
admission_label: pending
status: SCALAR_PROVENANCE_LOCATED_FUNCTION_BOUND_MISSING
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
generated_constants: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT-LOCAL-20260908T162738Z.md
predecessor_sha256: 961d1d4ebc47f8f7c6a7a6c28a6050fe7748cf7fc2f30bb74193d25c081a6b49
requested_action: provide an actual function-indexed initial bound for the selected storage on the block-only initial set
---

# Initial scalar: exact data path, no actual target-bound witness

Only this new review is written. No constants or bounds are generated,
no producer/checker/Julia/Lean/regression is executed, and no source, state or
registry is modified. Candidate Vfull_DH/Vshift_DH definitions are consumed
from the preceding definition/binding reviews, without reselecting the target.

External directory E:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## 1. Scalar provenance is identifiable

Freshly read `routeB_compact_energy_storage_to_block_audit.py:44-51` computes

```text
initial_quad_upper = max(POTENTIAL_HESSIAN_BLOCK_UPPER/2, MASS_UPPER/2)
                     + EPS*MASS_UPPER/2
initial_energy_upper = initial_quad_upper*INITIAL_RADIUS^2.
```

It exports the latter as initial_storage_upper. The source describes local
targeted-gain storage with a mass cross term and block-only initial data.
`routeB_compact_block_energy_barrier_audit.py:54` reads this field into V0;
it later uses V0 in V_TUBE and compares that tube against V_BAR=1.
No numerical evaluation is repeated here. The scalar's CSV continuity is
not an inequality indexed by either Vfull_DH or Vshift_DH.

The exporter performs arithmetic on declared bounds; it does not evaluate
a selected V over X0 or bind those bounds to its complete value-level
definition, normalization and parameter instance. Thus even the source-side
functional initial envelope is an outstanding premise, not just transfer
from an already admitted source bound.

## 2. X0 and state map are clear as a contract, not a filled instance

The existing STORAGEIDENTITY Lean sidecar specifies State=Fin 12 -> Real,
first six coordinates q, last six v. blockOnlyInitial retains zero-based
indices (3,4,9,10), corresponding to (q4,q5,v4,v5), sets every other coordinate
to zero and uses the recorded combined block-ball radius.

This agrees with the producer's stated scope. It is NOT the full initial
twelve-dimensional ball, nor four independent intervals replacing the ball.
For an actual binding, map this State to the selected candidate's q,v and
c/s coordinates and fix initial time if any time-dependent candidate is used.
The symbolic source Vfull_DH is six-coordinate storage even when evaluated
on a four-free-coordinate initial set.

The sidecar's RouteBInitialTransfer contains sameStorage, initialInDomain
and exportedInitial fields. Its comment explicitly says no current candidate
constructor is supplied. A bounded search of examples/*.lean found definitions
and consumers, not an actual Vfull_DH/Vshift_DH InitialBoundBinding instance.

## 3. The hidden value-anchor obligation in the Hessian-style bound

For a potential/controller part P, an upper Hessian bound on the segment
from the origin controls

```text
P(q)-P(0)-dP(0)[q],
```

not P(q) by itself. The producer's quadratic-only initial expression therefore
requires an explicit value/linear anchor, or a separately justified bound
including those omitted contributions. Derivative/Hessian data do not choose
the additive normalization. This is a logical obligation, not a recomputed
constant or a claim that every possible initial proof must use Taylor bounds.

To use the displayed formula for one actual storage also requires the same
regularized mass bound, same restricted potential/gain expression, and the
cross-term envelope on X0. The targeted gain modification can vanish in some
coordinates on X0 without proving whole storage equality. The mass cross term
does not vanish just because remote initial coordinates are zero.

For raw Vfull_DH, no source-bound origin/linear anchor was attached to this
scalar producer. For Vshift_DH, its additional existing symbolic shift must
be included in an initial bound or offset comparison. No shift is evaluated
here, and neither candidate is declared to satisfy the unchanged scalar.

## 4. Minimum exact binding and threshold obligations

Choose one candidate V and actual configuration. The smallest sufficient
initial witness is simply

```text
forall x in X0, V(embed(x)) <= recorded_initial_upper.
```

A direct proof needs no identity with targeted storage. To reuse a source
storage U's initial bound instead, prove BOTH its genuine function-indexed
initial bound and `V(embed(x))<=U(x)+delta` on X0. The resulting upper bound
is the source upper plus delta. Neither premise is supplied by matching CSV
fields or matching origin values alone. No delta is invented.

For Vshift_DH=Vfull_DH+b, a full-storage initial upper transfers with +b.
The fixed active threshold remains 1 unless the consumer threshold is
explicitly changed and rebound. To retain the current scalar unchanged,
one needs an appropriate comparison or a new direct proof; the constant-shift
identity by itself does not retain it.

Initial inclusion requires the selected target bound to lie below the
selected threshold. Future first-exit closure additionally needs the actual
same-storage growth budget and domain argument; the numeric V_TUBE comparison
does not prove these functional premises. This task evaluates none of those
scalar gates and does not claim initial inclusion or a future barrier.

## 5. Minimal obstruction and evidence status

The data path and intended X0 are located. Missing are (a) the actual target
storage/configuration selection, (b) its value/linear normalization and
source envelope on that X0, or a valid source-bound comparison, and (c) the
matching threshold budget. Therefore no exact binding to Vfull_DH or
Vshift_DH is available from the inspected chain. Keep pending.

Current raw SHA256, relative to E:

| Artifact | SHA256 |
|---|---|
| routeB_compact_energy_storage_to_block_audit.py | 80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9 |
| routeB_compact_energy_storage_to_block_audit.csv | 8d37219ea1b6189ec84e2eec16aa4fe29e2ee4bd263b946a639fafb7692b2bf1 |
| routeB_compact_block_energy_barrier_audit.py | 62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927 |
| routeB_compact_block_energy_barrier_audit.csv | b10f0118c3dd3e6708084421baf38624977e6b18cd77dbb93e11f5a7f183f875 |

Hashes were freshly computed and identify bytes only; no historical run,
source semantics, interval soundness or compiled proof was authenticated.
