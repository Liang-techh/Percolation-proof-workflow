---
kind: review_result
review_id: review-GH-MIXED-ADJUGATE-REASSIGNED-codex-20260908T0830
task_id: GH-MIXED-ADJUGATE-REASSIGNED
source_agent: Codex
created_at: 2026-09-08T08:30:49-06:00
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_AdjugateAcceleration.lean
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.signed_projected_adjugate_acceleration_interface
---

# GH-MIXED-ADJUGATE-REASSIGNED — signed projected-adjugate boundary

## Exact theorem boundary

`projected_identity` is the minimal signed-cancellation theorem.  From the
same two descriptor rows it derives

```text
det(M) * (ell1*u1 + ell2*u2) =
  ell1*(c*f1-b*f2) + ell2*(a*f2-b*f1).
```

`projected_accel_bound` then needs exactly a positive determinant lower bound,
the signed projected-numerator enclosure, and the order gate
`R ≤ delta*upper`.  The observable projection is not inferred from its name:
`same_cell_observable_cap` requires an explicit same-cell
`observable_binding`.

## Signed-cancellation obstruction

The exact family `M(t)=[[1,t],[t,1+t²]]`, `f(t)=(t,1+t²)`, `u=(0,1)`, and
`ell=(1,0)` has determinant `1` and projected numerator `0`.  Replacing the
signed numerator by independent absolute boxes loses this cancellation and can
create a strictly positive fallback bound despite the exact projected value
being zero.

Independently, descriptor rows and determinant bounds do not constrain an
unbound observable field: with `M=I`, `f=(1,0)`, `u=(1,0)`, `ell=(1,0)`, and
`delta=R=upper=1`, choosing the observable value `2` satisfies the row and
packet data but violates `|observable|≤upper`.  The explicit observable
binding is therefore non-optional.

## P3 cross-lane status

The P3 central-FD lane already has its minimal C3/step/shifted-region/residual
contract in a separate pending review.  It remains conditional and is not
recreated here.

No DH/source binding, Float64 correctness, coverage, flowpipe containment,
residual absorption, admission, registry promotion, or Lean compilation claim
is made.  This result remains `integration_status: pending`,
`admission_label: pending`, and `final_integration: false`.
