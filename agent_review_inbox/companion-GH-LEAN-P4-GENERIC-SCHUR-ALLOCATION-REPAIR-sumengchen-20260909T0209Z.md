kind: companion_log
agent: 苏梦辰
source_agent: 苏梦辰
task_id: GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION-REPAIR
parent_task: GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION
admission: compiled_candidate
registry_mutation: false

# GH-LEAN-P4-GENERIC-SCHUR-ALLOCATION repair closure

## Scope

This companion closes only the focused Lean repair/compile loop for
`examples/routeb_p4_generic_schur_allocation_lean/`.  It does not provide dense
`M0_CC⁻¹` metric transport, deployed DH/source binding, physical/path coverage,
Float64 execution evidence, P8 ODE/flowpipe coverage, or parent admission.

Inspected repair/writeback commit from the previous round:

- proof repair: `6426af1f007c6360bb90d11d8a53fb3a90d6ea38`
- previous companion/writeback: `90563d1f5afab6b94dc4eb24e8b76a57fd5b0b0d`

The repair preserved the theorem statements, hypotheses, constants, and the
finite-dimensional typed interface.  It only replaced the Lean-4.32-fragile
finite-sum rewriting in `sq_sub_smul` by an explicit sum decomposition and
removed the redundant post-`norm_num` `ring` in the zero-radius regression.

## Real GitHub Actions evidence

Workflow run / job:

- run: `34294059656`
- job: `102286686583`
- pinned Lean: `leanprover/lean4:v4.32.0`
- sidecar: `examples/routeb_p4_generic_schur_allocation_lean/verify.sh`

The real job log records, in order:

```text
PLACEHOLDER_SCAN=PASS
AXIOM_AUDIT=PASS
P4_GENERIC_SCHUR_ALLOCATION_FOCUSED_CHECK=PASS
FINITE_DIMENSION_GENERIC=true
EXACT_COMPLETED_SQUARE=true
NO_DOUBLE_CHARGE_COMPARISON=true
DENSE_METRIC_TRANSPORT=OPEN
DEPLOYED_SOURCE_BINDING=OPEN
P8_ODE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_p4_generic_schur_allocation_lean/verify.sh
```

The aggregate portable-sidecars job is red because other already-existing
sidecars fail in the same run.  The log independently records this sidecar's
`SIDECAR_RESULT=PASS`; no repair of those unrelated sidecars is claimed here.

## Exported theorem / axiom audit

All eight exported declarations compiled and `#print axioms` reported only
`[propext, Classical.choice, Quot.sound]`:

1. `RouteBP4GenericSchurAllocation.sq_nonnegative`
2. `RouteBP4GenericSchurAllocation.sq_add`
3. `RouteBP4GenericSchurAllocation.sq_sub_smul`
4. `RouteBP4GenericSchurAllocation.combined_remainder_identity`
5. `RouteBP4GenericSchurAllocation.combined_of_port_budget`
6. `RouteBP4GenericSchurAllocation.relaxed_target_le_exact_total`
7. `RouteBP4GenericSchurAllocation.exact_total_floor_of_relaxed_nonnegative`
8. `RouteBP4GenericSchurAllocation.zero_radius_boundary_not_finite_witness`

`AXIOM_AUDIT=PASS` together with the placeholder scan means this focused receipt
contains no `sorryAx`/`sorry`/`admit` escape hatch.

## Formal boundary still open

- `DENSE_METRIC_TRANSPORT=OPEN`: the current generic theorem is Euclidean and
  does not transport the deployed dense `M0_CC⁻¹` metric.
- `DEPLOYED_SOURCE_BINDING=OPEN`: no equality to the real DH residual/source
  packet is asserted.
- matching-metric port-cap and domain/path coverage remain open.
- Float64/FD/controller/solve evidence remains open.
- `P8_ODE_COVERAGE=OPEN`.
- no registry mutation and no P4/P5 parent closure is asserted.

## Status

`compiled_candidate` for the narrow generic Schur-allocation Lean seam only.

待封不觉独立验证 / 待梁智炜最终整合。
