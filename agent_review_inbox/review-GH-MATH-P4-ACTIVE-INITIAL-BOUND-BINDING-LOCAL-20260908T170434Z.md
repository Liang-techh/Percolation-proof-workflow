---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING-LOCAL-20260908T170434Z
task_id: GH-MATH-P4-ACTIVE-INITIAL-BOUND-BINDING
source_agent: codex-minimal-initial-binding-audit
created_at: 2026-09-08T17:04:34Z
integration_status: pending
admission_label: pending
status: VALUE_LEVEL_UNIFORM_INITIAL_BOUND_MISSING
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
full_regression: false
state_mutation: false
registry_mutation: false
requested_action: supply a same-function raw initial bound including its anchor and matching threshold
---

# Minimal obstruction

The current initial_storage_upper is not yet a function-level uniform bound
for either raw Vfull_DH or Vshift_DH on the same block-only X0.

Freshly reread producer lines49-51 still form a quadratic-only bound from
declared Hessian/mass parameters plus an explicit cross-term allowance.
The barrier still reads that scalar unchanged and uses V_BAR=1. The existing
typed RouteBInitialTransfer still requires exportedInitial and sameStorage;
no actual candidate constructor is supplied there.

Consume the established expression difference on X0:
`T-W=-2*g_B^T*q_B+eps*q_B^T*M_BB(q)*v_B`, with W=Vfull_DH.
The joint-ball envelope review already gives a conditional uniform transfer;
no arithmetic or bound is regenerated here. Importantly, the scalar already
contains a cross-term allowance. Its absence is NOT the obstruction.

The shortest missing witness is

```text
forall x in the recorded block-only X0,
  selected_raw_storage(same_state_map(x), same_configuration)
    <= initial_storage_upper.
```

This requires the same regularized mass and potential/gain parameters,
the correct g sign or a proved g_B=0, and the raw value anchor. A valid bound
for W-U(0) does not provide this statement for W. Vshift_DH requires its
additional existing offset as well. Neither Hessian data nor origin equality
supplies a uniform value bound. No new offset is proposed.

Either prove that statement directly, or provide an already valid source
initial bound and an X0 comparison with every anchor/linear/cross contribution
accounted for. Any adjusted upper must match the selected threshold; keeping
the old scalar and threshold requires its own proof. Initial binding alone
would still not establish the subsequent flow/barrier theorem.

## Evidence and scope

Consumed envelope review:
`review-GH-MATH-P4-ACTIVE-ENERGY-NORMALIZATION-20260908T170235Z.md`, SHA256
`01fa475ea8904a0667ebcf480a5ed91796e14a117409cdb07e04d6d9e7e01336`.

External source root:
`C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`.
Current producer SHA256:
`80795ef4fcbe0da4fb6d491f040e69196323fc09b01cf5739cb197343ef766b9`.
Current barrier consumer SHA256:
`62972f8b2049be3351616e25837db722731744f8e3b219d2ddf90fd817026927`.
Both refer respectively to routeB_compact_energy_storage_to_block_audit.py
and routeB_compact_block_energy_barrier_audit.py. Hashes were recomputed.

Only this new review is written. No constants, origin calculation, symbolic
sidecar, Lean/Julia execution or regression; no state/registry/old-file edits.
No VERIFIED or source admission claim. Status remains pending.
