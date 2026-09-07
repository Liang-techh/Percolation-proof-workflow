---
kind: review_result
task_id: T-P4-KC-COORDINATE-ADAPTER
source_agent: codex-local
created_at: 2026-09-07
integration_status: pending
---

# Fresh general-state B-row export contract

## Execution status

`julia` is not installed/available on this worker, so no fresh Julia runtime
CSV or numerical receipt is claimed. The directly executable exporter contract
is:

[`general_state_force_binding_export.jl`](../examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl)

Current exporter SHA-256:
`5351110e81327ebc059074a2e445a33e00859320bce37b5b0220bb189f4e46a4`.

It includes the canonical deployed source by path, binds the source hash at
runtime, and writes a fresh CSV plus `FORCE_BINDING_RECEIPT.md` under
`output/general-state-export-20260907`.

## Exact state contract

The exporter uses one deterministic state list (`SEED=20260907`, 16 states:
zero state plus 15 generated states) and fixes:

```text
B = [4,5]
D = [1,2,3,6]
sourceBlockForce := rhs[B]
rhs := tau - Cdq - Gq
a := Mq \ rhs
MqBB := Mq[B,B]
MqBD := Mq[B,D]
sourceDescriptorRhs := MqBB*a[B] + MqBD*a[D]
```

For the same state, it exports `qB=(q4,q5)`, `vB=(dq4,dq5)`, `w`,
`CdqB`, `GqB`, `G0B`, `tauB`, `rhsB`, `sourceBlockForce`, `aB`, `aD`, all
four entries of `MqBB`, all eight entries of `MqBD`, `sourceDescriptorRhs`,
and componentwise residuals

```text
E1 = sourceBlockForce - expectedSourceForce(qB,vB,w,CdqB,GqB,G0B)
E2 = sourceBlockForce - sourceDescriptorRhs
```

The exporter also records `MASS_REGULARIZER`, `CG_FINITE_DIFF_STEP`, source
SHA-256, exporter SHA-256, state seed, state count, B/D order, maximum `E1`,
and maximum `E2` in its generated receipt.

## Acceptance condition for the future runtime receipt

Run from the workflow checkout with the canonical Julia installation:

```text
julia --startup-file=no examples/routeb_b45_5_descriptor_terms_adapter_lean/general_state_force_binding_export.jl
```

The receipt may report `PASS_RUNTIME_FLOAT64` only if every exported state has
finite values and

```text
max(abs(E1_4), abs(E1_5), abs(E2_4), abs(E2_5)) <= 1e-12.
```

The CSV and receipt must be hash-bound to the current deployed
`robot_final/dhport_lib.jl` (current SHA-256
`aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`) and to
the exporter SHA above. A stale `verify_descriptor_interface.py` hash or the
old 16-row CSV cannot substitute for this fresh receipt.

## What this would discharge

For each exported state it supplies an auditable numerical witness for the two
specific source premises:

```text
sourceBlockForce = expectedSourceForce q v w t
sourceBlockForce = sourceDescriptorRhs t
```

The first is checked componentwise against exported `CdqB/GqB/G0B/tauB`; the
second is checked componentwise against the actual `Mq[B,B]` and `Mq[B,D]`
blocks and the same solved `a`. This deliberately does not use nominal
`M0_BB` for the deployed descriptor row.

## Current disposition

- exporter contract: `READY_TO_RUN`;
- fresh general-state runtime receipt: `PENDING_JULIA_EXECUTION`;
- existing P2 metadata checker: `PASS` for its old artifact only;
- Float64-to-exact-real Lean bridge: `OPEN`;
- deployed `tau` equivalence: `NOT CLAIMED`;
- registry/main-state mutation: `false`.

