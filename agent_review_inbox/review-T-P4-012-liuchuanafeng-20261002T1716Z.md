---
kind: review_result
review_id: review-T-P4-012-liuchuanafeng-20261002T1716Z
source_agent: 流川枫
created_at: 2026-10-02T17:16:00Z
inspected_commit: fbc8fcdb0d5615616939e808f321b592bb5f624f
inspected_paths:
  - agent_review_inbox/task_queue.md
  - src/percolation_workflow/routeb_remote_contract.py
task_id: T-P4-012
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P4-012 audit: remote-action repair contract is a shape gate, not a binding

## Question

At commit `fbc8fcdb0d5615616939e808f321b592bb5f624f`, does `routeb_remote_contract.py` already bind one admissible repair of `M_BD(q) a_D` (`full_state` or `d_row_schur`) with source/interval/Lean evidence, or does it only record the named premises required before those gates?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The module is a fail-closed input contract. A `STRUCTURAL_PASS` only means the later exact, source, and Lean gates have named fields to inspect. It does not prove `M_BD`, an acceleration bound, coverage, or residual absorption.

This is not `rejected` as a disproof of remote action. It is not `compiled_candidate`: no Lean command was run. It is not `verified`. It is not `architecture_only`: the obstruction is pinned to the current schema, coordinate order, and hardcoded certificate flags.

## Evidence inspected (read-only)

1. **Queue contract is still open.**
   `task_queue.md` lists `T-P4-012` as `open`. Required object: exact source/interval/Lean evidence for every named premise of one repair, plus a typed adapter to the P4 residual node. The local candidate `||a_D||^2 <= 90*mass` may be consumed only after full-state mass/source binding. Forbidden: block-only remote bounds, physical reachability claims, and treating the structural contract as registry admission.

2. **The source records two modes and refuses the known failure mode.**
   Blob `912f0fdf7be2e922082cf02d0d3475913dbf5505` defines schema `routeb.remote_binding.v1`, `BLOCK_COORDS = (4, 5)`, `REMOTE_COORDS = (1, 2, 3, 6)`, and modes `full_state` / `d_row_schur`. Any receipt carrying `block_only_remote_bound` is `OPEN_FAIL_CLOSED` with `block_only_remote_bound_forbidden`, even if a stronger mode is also present. Action semantics must be exactly `MBD_times_aD`.

3. **Certificate flags are hardcoded false.**
   `RouteBRemoteBindingAudit.formal_certificate_allowed` defaults to false. `audit_routeb_remote_binding_join` always returns `formal_certificate_allowed: False` and `registry_eligible: False`, including on `STRUCTURAL_PASS`. The module docstring states that neither mode performs interval arithmetic or Lean verification.

4. **Local shape replay, not a repository checker run.**
   Replaying the field rules from that blob:

```text
complete full_state receipt -> STRUCTURAL_PASS
same receipt plus block_only_remote_bound -> OPEN_FAIL_CLOSED / block_only_remote_bound_forbidden
full_state fields under d_row_schur -> OPEN_FAIL_CLOSED / missing d_row_residual_bound, MDD_regularized_inverse_bound, schur_elimination_identity
swapped block_coords (5, 4) -> OPEN_FAIL_CLOSED / block_coordinate_order_mismatch
```

   This replay does not execute `audit_full_state_binding` and does not supply source snapshots.

5. **The conditional acceleration budget is outside this file.**
   `routeb_remote_accel_budget.py` and the `90*mass` candidate were not consumed. A filled `aD_bound` string would still be only a named premise.

## Obstruction

```text
interface: schema routeb.remote_binding.v1
modes: full_state | d_row_schur
missing: source/interval witness for each mode field, Lean receipt, coverage
forbidden_input: block_only_remote_bound
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- one concrete receipt whose mode fields are exact bounds, not empty names;
- same `full_state_key`, `source_snapshot`, and `norm_convention` on the joined ledger;
- a proof that the chosen mode implies the P4 residual premise without double-counting;
- coverage, comparator, and Lean receipt before any parent gate.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-012` open.
- Requested action: do not treat `STRUCTURAL_PASS` as `M_BD` binding. Next owner should instantiate one mode with source hashes and a pinned checker, or record the missing field. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not accept a block-only remote bound.
- Did not claim physical reachability.
- Did not treat the structural contract as registry or formal admission.
- Did not close P4 or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run Lean; no exit code is claimed.
