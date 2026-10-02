---
kind: review_result
review_id: review-T-P5-009-liuchuanafeng-20261002T1418Z
source_agent: 流川枫
created_at: 2026-10-02T14:18:00Z
inspected_commit: 1bd8ecf7c3d23bc4e5f520211937305bb8881350
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P5-005-kuangmanmozun-20260906T2307.md
  - examples/routeb_dh_power_binding/FDForceBudget.lean
task_id: T-P5-009
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P5-009 interface audit: slope-plus-offset FD envelope is not a relative bound

## Question

At commit `1bd8ecf7c3d23bc4e5f520211937305bb8881350`, can the current `FDForceBudget.envelope` interface be turned into a velocity-relative residual bound without an extra equilibrium/state contract, and can that interface be admitted as true-DH source binding or P5/M4 closure?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The current typed interface cannot imply a relative bound. Channels 1--4 have a strictly positive additive offset, and no theorem relates `cap` to `|v|`. That is an interface obstruction, not a deployed-trajectory counterexample and not a compiled certificate.

This is not `rejected` as a physical claim about the deployed FD error. It is not `compiled_candidate`: no Lean command was run in this pass. It is not `verified`. It is not `architecture_only`: the obstruction is pinned to the existing envelope definition and theorem premises.

## Evidence inspected (read-only)

1. **Queue contract is still open and narrow.**
   `task_queue.md` lists `T-P5-009` as `open`. Required object: a minimal typed adapter stating the extra equilibrium/state contract needed to turn a slope-plus-offset FD envelope into a relative bound, or a proof that the current interface cannot. Forbidden: a hidden change of cap, coordinate order, or unit, and closing P5/M4.

2. **The envelope is inhomogeneous.**
   `FDForceBudget.lean` git blob `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36` defines

```text
envelope cap i = slope i * cap + offset i
```

   with exact offsets

```text
offset 0 = 0
offset 1 = 68343 / 800000000000000
offset 2 = 21909 / 1000000000000000
offset 3 = 6867 / 8000000000000000
offset 4 = 6867 / 4000000000000000
offset 5 = 0
```

   So `offset 1`, `offset 2`, `offset 3`, and `offset 4` are strictly positive. Index order is `Fin 6`, unchanged from `T-P5-005`.

3. **Existing theorems do not add a relative premise.**
   `fd_only_supply_bound` assumes only `0 <= cap` and `|e i| <= envelope cap i`. `implemented_energy_fd_plus_runtime` assumes `|efd i| <= envelope cap i` and `|runtime i| <= zeta i`, then charges `(envelope cap i + zeta i)^2 / (2 * damping i)`. Neither statement contains `|e i| <= rho i * |v i|`, nor `cap <= C * |v|`, nor `offset = 0`.

4. **Unconditional relative inference fails on the stated interface.**
   Take `cap = 0`, `v = 0`, and channel `i = 1`. The envelope premise allows

```text
efd 1 = offset 1 / 2 = 68343 / 1600000000000000 > 0
```

   while `rho * |v 1| = 0` for every finite `rho`. The same witness works for channels 2, 3, and 4. Zero-offset channels 0 and 5 are not rescued: a positive `slope i * cap` is still not relative to `v i` unless a separate contract forces `cap` to vanish with that velocity.

5. **Prior review already recorded the offsets; this pass only consumes that fact.**
   `review-T-P5-005-kuangmanmozun-20260906T2307.md` blob `65a1e212244e615568a07169889591ed2cb68c4f` states the same positive-offset obstruction. This audit does not redo the weighted Young closure. It records the missing adapter that `T-P5-009` asked for.

## Minimal extra contract

The current interface becomes a componentwise relative bound only after an additional hypothesis of one of these two shapes. Neither is present in `FDForceBudget.lean`.

```text
(A) vanishing offset and cap controlled by the same velocity:
    offset i = 0
    0 <= cap <= C i * |v i|
    0 <= slope i * C i < damping i
    ==> |efd i| <= (slope i * C i) * |v i|

(B) bias split, no change of the stored envelope:
    efd = e_rel + e_bias
    |e_rel i| <= rho i * |v i|,   0 <= rho i < damping i
    e_bias charged by an absolute/Young budget, not folded into rho
```

Contract (A) is unavailable while any `offset i > 0`. Contract (B) is the strongest statement still valid: keep the slope-plus-offset envelope as an absolute FD budget, and do not rewrite it as `rho|v|`.

## Obstruction

```text
interface: |efd i| <= slope i * cap + offset i
offset_positive: i in {1,2,3,4}
missing: cap <= C i * |v i|, or offset i = 0, or an explicit e_rel/e_bias split
witness: cap = 0, v = 0, efd 1 = offset 1 / 2
units: envelope remains a force residual; cap is not a velocity
source_binding: deployed FD/libm/domain equality not claimed
```

## Assumptions still required

- a source-bound proof that the additive offsets are absent on the deployed equilibrium, or an explicit bias ledger;
- a same-domain relation between `cap` and velocity or state;
- damping comparison `rho i < damping i` after that relation exists;
- coverage, comparator, and Lean receipt before any parent gate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P5-009` open.
- Requested action: do not convert `polynomialBudget` or `fd_only_supply_bound` into a relative residual theorem. Next owner should either formalize the channel-1 zero-velocity witness as a source-independent obstruction lemma, or supply contract (A)/(B) with a real source hash. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not change cap, coordinate order, or units.
- Did not treat the abstract envelope as true-DH source binding.
- Did not close P5 or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
