---
kind: review_result
task_id: T-P4-002
source_agent: Codex
created_at: 2026-09-06T22:00:00-06:00
integration_status: pending
---

# T-P4-002: one-channel true-DH residual envelope

## Scope and inspected evidence

This is a read-only audit. No queue, authoritative Route-B state, registry, or
external source was modified.

Inspected:

- `examples/routeb_p4_next_child/P4RationalSchurAbsorption.lean`
- `examples/routeb_p4_next_child/REPORT.md`
- `examples/routeb_p4_decimal_source_binding_audit/audit_report.json`
- `examples/routeb_physical_schur_binding_lean/PhysicalSchurBinding.lean`
- `docs/routeb-c2-d-normalization-audit.md`
- external `routeB_dense_Mq/dhport_lib.jl`,
  `routeB_descriptor_residual_interface.jl`,
  `routeB_Mq_M0.csv`

The focused checks were rerun:

```text
decimal_spelling_equality = PASS
float64_value_equality = PASS
true_dh_mass_equality = PENDING
FOCUSED_CHECK = PASS
AXIOM_AUDIT = PASS
formal_certificate_allowed = false
```

The pinned Lean leaf uses the exact spelling
`d = 116667666666667 / 10^15`, with `p=3/5`, `ell=1/100`, and proves the
Schur/Young algebra. Its result is an exact algebraic consumer, not a source
binding theorem.

## Smallest executable source-binding witness

The smallest useful witness is one fixed source point and one residual channel:

```text
channel       = 4
q             = (0,0,0,0,0,0)
dq            = (0,0,0,0,0,0)
w             = 0
mass_regularizer = 1e-6
fd_step       = 1e-5
M0[4,4]       = 0.116667666666667
exact decimal = 116667666666667 / 10^15
rhs           = tau - C*dq - G = 0                 (after the source's G0 cancellation)
a             = M(q) \\ rhs = 0                    (Float64 execution witness)
f4            = 0                                   (nominal source expression)
l4            = I4*f4 - M0[4,4]*a4 = 0             (force-side residual)
```

This point is preferable to an arbitrary sample because the source explicitly
defines `tau` with `G0`, while the deployed descriptor computes `G(q)` at the
same zero configuration. It tests the index/sign/normalization path with no
nonzero residual to estimate and no long computation. The witness must be
emitted by a pinned Julia run as a structured receipt, not inferred from the
CSV alone.

## Required receipt contract

The minimal executable receipt should contain:

```json
{
  "schema": "routeb-p4-one-channel-source-binding/v1",
  "source": {
    "dhport_lib_sha256": "aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936",
    "csv_sha256": "28d98ad71d1d6c2cbe830872cad9077f2f7b4e2d932794217eb68868fd2e2b40",
    "mass_regularizer": 1e-6,
    "fd_step": 1e-5,
    "julia_version": "<pinned runtime>"
  },
  "point": {"q": [0,0,0,0,0,0], "dq": [0,0,0,0,0,0], "w": 0},
  "channel": 4,
  "values": {"m00_float64": "<bits>", "rhs4": "<bits>", "a4": "<bits>", "f4": "<bits>", "l4": "<bits>"},
  "identities": {
    "M0_decimal_reification": "PASS",
    "descriptor_residual_inf": "<numeric bound>",
    "force_normalization": "l4 = I4*f4 - M0[4,4]*a4"
  },
  "status": "PENDING"
}
```

The `<bits>` fields must be the actual IEEE-754 bit patterns from the same
execution. A receipt with only decimal text, or with values copied from the
exported CSV, is insufficient.

## Normalization and theorem boundary

The deployed source defines `a` as acceleration and `l4` as a generalized-force
residual. Therefore the correct next conditional theorem is an instantiation
of the existing adapter with an explicit force envelope:

```text
residual = l4(q,dq,w)
residual^2 <= beta^2 * y^2
```

The exact Schur leaf may consume this premise, but the receipt must separately
bind the source definition of `l4`, the channel/index map, and the envelope
itself. If an acceleration-side `D(e)` is desired, an additional mass/ inverse-
mass bridge is required; `l4` cannot be silently renamed to `e_A`.

## Classification

| Item | Classification | Current status |
|---|---|---|
| Exact Schur/Young consumer | directly reusable | `VERIFIED` as abstract Lean algebra; standard axioms only |
| Decimal-to-rational and Float64 spelling audit | light adaptation | `COMPILED_CANDIDATE`/audit evidence only |
| Zero-point channel-4 source receipt | smallest next witness | `PENDING`; needs pinned Julia execution trace and semantic bridge |
| Pointwise/global true-DH residual envelope | not established | `PENDING` |
| P4 global coverage and M4 closure | outside this task | `OPEN` |

No item above closes P4, changes the verified registry, or permits
`formal_certificate_allowed=true`.

## Next smallest child

Generate the pinned receipt at the single zero point, then add a second
nonzero deterministic point only if the zero-point trace passes. The subsequent
theorem must prove a fixed-cell interval enclosure for `l4` (force-side), with
the same mass regularizer and finite-difference semantics. Do not infer a
cell-wide envelope or global coverage from this point witness.
