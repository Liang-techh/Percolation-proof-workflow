---
kind: review_result
review_id: review-T-P8-002-EXPLICIT-TIME-13STATE-PARENT-liuchuanafeng-20261025T1418Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-25T14:18:00Z
claimed_at: 2026-10-25T10:10:00Z
inspected_commit: 553a4535b518f3452727fb7a79424639ed3fa72c
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P8-002-EXPLICIT-TIME-13STATE-PARENT-liuchuanafeng-20261025T1010Z.md
  - docs/routeb-p8-next-concrete-child.md
  - docs/routeb-p8-flowpipe-binding-next.md
  - examples/routeb_p8_contract_adapter/P8ContractAdapter.lean
task_id: T-P8-002
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
flowpipe_coverage_claimed: false
parent_theorem_changed: false
proposed_integration_target: documentation
requested_action: harvest_pending_decision_memo_do_not_promote_or_change_parent
---

# T-P8-002: decision memo on explicit-time 13-state parent option

## Question

At the inspected commit, should the P8 parent be changed from the existing 14-state ramp contract (`w' = c`, `c' = 0`) to a new explicit-time 13-state parent (with `w(t) = c * t`), and what is the minimal theorem signature / admission boundary of that option?

## Decision

**Do not change the target theorem. Keep `admission_label: pending`.** The current 13-state source (`full_rhs!` with `du[13] = 0`, no `c` state) is incompatible with the 14-state `RampRhsPremise`. The literal zero-tail lift is already proved not to satisfy the premise (`zeroTailLift_not_ramp`). The existing `timeLift` adapter is a conditional interface only: it restores the ramp shape for an abstract time-indexed 13-state field `G`, but supplies no source binding for the first 12 components, no Float64/FD/regularizer semantics, no interval containment, and no flowpipe existence or coverage.

An explicit-time 13-state parent would require a different contract (time-dependent RHS, `w(t) = c*t`, separate parent/flowpipe adapter). That constitutes a change to the target theorem, which is forbidden to perform silently. It does not by itself discharge the source-binding obstruction and would still leave S1--S6 open. Therefore the option remains an architecture sketch, not an admission upgrade.

This poll did not edit any source, registry, state, or formal proof. Roster still records 流川枫 as unavailable for new dispatch; this is an inbox-only completion of a pre-existing claim.

## Evidence inspected (read-only)

1. **Task boundary.** `task_queue.md` defines `T-P8-002` as a decision comparison of a new explicit-time 13-state parent versus the existing 14-state ramp parent, including initial-domain and terminal-statement changes. Deliverable is a decision memo and minimal theorem signature; forbidden is silently changing the target theorem or claiming flowpipe coverage.

2. **Concrete child audit.** `docs/routeb-p8-next-concrete-child.md` records that the audited Julia `full_rhs!` is 13-state, receipt marks `c` as sidecar, and the natural 14-state lift fails `RampRhsPremise` on a valid `FullX0` point with `c=1`. The `timeLift` construction satisfies the ramp premise conditionally but is labeled `conditional_interface_only`. Child chain C13-14 is CLOSED (negative), C13-T is COMPILED/conditional; S1--S6 remain OPEN.

3. **Flowpipe binding next.** `docs/routeb-p8-flowpipe-binding-next.md` confirms the same incompatibility, lists the exact coordinate map, and states that the first actionable child is a coherent 14-state ramp source binding (or an explicit decision to change the contract), not longer simulation or wider boxes. Admission remains source_binding=OPEN, ramp_binding=OPEN/inconsistent, flowpipe_coverage=OPEN.

4. **Lean adapter.** `examples/routeb_p8_contract_adapter/P8ContractAdapter.lean` contains the exact statements:
   - `zeroTailLift_not_ramp`: literal lift does not satisfy `RampRhsPremise`;
   - `timeLift_rampPremise`: for every fixed `t`, the lifted field satisfies the premise;
   - explicit comment that no source binding, interval receipt, ODE existence, or true-DH claim is made.

## Minimal theorem signature (architecture only)

If a future scoped request explicitly authorizes a parent change, the smallest signature would be of the form:

```text
theorem explicitTime13_parent (G : ℝ → State13 → State13) :
  ∀ t, ∀ z13,
    -- source binding of first 12 components to G t z13
    -- w(t) = c * t   (c constant)
    -- initial domain: mechanical energy ≤ 9/400, |c| ≤ √3
    -- terminal statement adjusted for the integrated w
  := ...
```

No such theorem exists, and this review does not introduce it. The current parent and its ramp premise remain unchanged.

## Missing gates

```text
source_binding (first-12 semantic equality to true DH/FD/solve): OPEN
ramp_binding for deployed source: OPEN / inconsistent
outward interval containment: OPEN
Picard / flowpipe existence and [0,1] coverage: OPEN
formal_certificate_allowed: false
registry: unchanged
```

## Integration target and requested action

- Target: documentation only. Leave `T-P8-002` open (or mark reviewed_pending) pending an explicit future decision on whether to alter the parent contract.
- Requested action: harvest this decision memo as pending. Do not promote admission, do not rewrite the parent theorem, do not claim flowpipe coverage, do not edit registry or state.

## Forbidden-boundary compliance

- Did not silently change the target theorem.
- Did not claim flowpipe coverage or source binding.
- Did not modify any source file, registry, state.json, or formal proof.
- Only added this immutable review_result envelope.
