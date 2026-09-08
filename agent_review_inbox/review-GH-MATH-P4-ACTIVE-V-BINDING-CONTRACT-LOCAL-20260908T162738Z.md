---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT-LOCAL-20260908T162738Z
task_id: GH-MATH-P4-ACTIVE-V-BINDING-CONTRACT
source_agent: codex-active-v-binding-contract
created_at: 2026-09-08T16:27:38Z
integration_status: pending
admission_label: pending
status: BOTH_CANDIDATES_UNBOUND_TO_ACTIVE_CONSUMER
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
predecessor_review: agent_review_inbox/review-GH-MATH-P4-ACTIVE-V-TARGET-DEFINITION-LOCAL-20260908T162002Z.md
predecessor_sha256: 02222605252d247d924c25528607cb72a3d561587d46ff268b5d4787d5a0ad52
requested_action: instantiate one target-specific initial, lower-bound and flow-budget contract; do not infer storage identity from derivative flags
---

# Binding Vfull_DH or Vshift_DH to the active consumer

Only this new review is written. The two explicit candidate definitions and
their source/configuration chains are consumed from the hashed predecessor.
This turn rereads the current consumer CSV, targeted initial-bound CSV, and
the keyed storage-transfer Lean interface. It runs no producer, checker,
numerical calculation, Julia, Lean or regression and generates no constants.

External E is
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.

## 1. Both existing values are concrete; neither is the selected active V

Write W=Vfull_DH and Z=Vshift_DH=W+b, where b denotes the existing symbolic
gravity/controller shift, not a newly evaluated number. Both are explicit
source expressions, with different additive normalizations. The prior
definition review records mass regularization, gains, potential and linear
compensation details; none is repaired or redefined here.

The active consumer still labels its domain V<=1 and reads initial_storage_upper
from the targeted-gain/cross-term storage-to-block output. That output itself
labels its scope block_only_q4_q5_dq4_dq5, includes an epsilon cross term,
and records initial_inclusion_checked=False. The consumer reports
energy_first_exit_closed=True as conditional arithmetic while recording
descriptor_flowpipe_closed=False, fd_remainder_semantics_closed=False and
formal_certificate_allowed=False.

The equal printed initial scalar in the two CSVs establishes data continuity,
not a function-indexed initial bound on W or Z. No candidate selection can be
justified from these fields alone.

| Obligation | W=Vfull_DH | Z=Vshift_DH |
|---|---|---|
| Value-level source expression | Located in predecessor | Located as W+b |
| Active V equality on exact domain | Missing | Missing |
| Bound on the actual block-only initial set | Missing for W | Missing for Z; cannot reuse W bound without offset |
| Consumer q/v lower bounds | Must prove for raw W | Shifted nonnegativity alone does not prove the required coercive lower bounds |
| Threshold and tube budget | Must use W and the fixed consumer threshold consistently | Must account for b in threshold/initial budget; fixed threshold is not shift-invariant |
| Actual source/flow derivative budget | Missing | Missing; equal derivatives under constant shift do not fill it |

Thus no candidate is selected in this review. This is an evidence obstruction,
not a claim that both candidates are intrinsically unusable.

## 2. Minimal direct consumer contract

Fix one target V, one source/configuration, state/time map, initial set X0,
comparison domain D and threshold bar (the current consumer uses 1). A usable
record needs these independent witnesses:

1. **Value binding:** V equals the selected W or Z expression on D, including
   the same mass/regularizer, gain branch, anchored/raw potential, linear
   compensation sign, cross term and additive offset. Hashes are provenance,
   not this equality.
2. **Initial binding:** X0 is the recorded block-only initial set under the
   same state map, X0 lies in the required domain, and V(x)<=u for every x in
   X0. A direct target proof suffices; equality with the targeted storage is
   not mandatory if the bound is proved independently.
3. **Domain/cap binding:** the source sublevel used before first exit implies
   the q/v caps required by its derivative/FD budget. Any coercive comparison
   used for those caps must refer to this V, not its unshifted partner.
4. **Flow/growth binding:** under the actual source dynamics and disturbance
   convention, regularity and a target-specific differential or integrated
   budget yield the intended tube cap. An old CSV derivative flag does not
   prove this hypothesis. Initial data, time horizon and domain continuation
   must match; do not assume the desired invariant sublevel to prove itself.
5. **Budget/target binding:** the tube cap is strictly below bar where strict
   first-exit reasoning requires it, and any output/terminal transfer uses
   lower bounds for this same V. No scalar gate is evaluated here.

These are obligations, not a filled certificate or new admission protocol.

### Joint lower bound required by the consumer's max-ratio step

The consumer selects a max ratio to transfer block output to V. With its
symbolic positive weights, a sufficient actual premise is

```text
V(x) >= c_q*||q_B||^2 + c_v*||v_B||^2
p_B(x) = a_q*||q_B||^2 + a_v*||v_B||^2
kappa >= max(a_q/c_q, a_v/c_v).
```

This supports p_B<=kappa V. The two separate statements V>=c_q||q_B||^2
and V>=c_v||v_B||^2 do not by themselves supply the SUM bound consumed by
that max-ratio argument. For a shifted comparison V>=quadratic+b, the
natural transfer references V-b, with a corresponding budget adjustment.
No new kappa, coercivity coefficient or offset is produced here.

## 3. Reuse via the existing minimal transfer interface

`NEW_BODY6_SLICE_KEYEDSTORAGETRANSFER20260907.lean` already separates
ReceiptKey equality from the mathematical comparison. For an already bound
source storage U and target V, it requires on a specified D:

```text
V(x) <= U(x)+delta,
X0 subset D,
U(x)<=u on X0.
```

Then the target initial bound is u+delta. To transfer an already proved path
cap U(path(t))<=cap, additionally require path(t) in D and cap+delta<=bar.
Use strict budget slack if the intended first-exit theorem needs it. This
comparison route does not demand identity and does not create a source cap.

For Z=W+b, the exact constant-shift transfer is available algebraically once
W's value/configuration binding is proved: a W-threshold bar corresponds to
a Z-threshold bar+b. Keeping Z's threshold at the original bar instead
requires the tighter W budget bar-b. Derivative equality cannot bypass this.

For the targeted cross-term storage U, the difference V-U is not known to be
a constant. Its gain/cross-term/potential/linear differences need a pointwise
comparison on the required set. An initial-only comparison can transfer an
initial bound but not a later path cap. Conversely, a source barrier already
proved on an independent path domain can be transferred without reproducing
its derivative proof; such a barrier has not been supplied here.

## 4. Smallest next evidence

Provide one source-bound target expression selection and its direct X0 upper
bound. Then supply the SAME target's cap-generating lower bound, actual
source/flow budget and threshold allocation. Alternatively provide the
keyed comparison above against a source storage whose initial/path bounds
are independently established. Do not add numerical offsets or choose a
target solely to make an existing scalar inequality pass.

The current absence is precisely these functional bindings. Both candidates
remain pending; no derivative flag has been treated as storage identity.
No claim about compiled status, source admission or registry eligibility follows.
