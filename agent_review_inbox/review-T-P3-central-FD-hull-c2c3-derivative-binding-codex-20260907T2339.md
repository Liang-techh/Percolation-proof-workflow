---
kind: review_result
review_id: review-T-P3-central-FD-hull-c2c3-derivative-binding-codex-20260907T2339
task_id: T-P3-central-FD-hull
source_agent: Codex
created_at: 2026-09-07T23:39:17-06:00
inspected_paths:
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_DERIVATIVE_BINDING.lean
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_DERIVATIVE_BINDING_REVIEW.md
integration_status: pending
admission_label: pending
---

# T-P3-central-FD-hull — minimal C2/C3 derivative-level DH binding

## Result

The companion adds the smallest same-box typed premises for supplied concrete
exact-real derivative evaluators:

```text
taylorFirstDerivative  = dhFirst
taylorSecondDerivative = dhSecond
taylorThirdDerivative  = dhThird
```

On the same listed box and region, the existing Taylor-to-source equalities
then yield source derivative equality at the single covered point selected by
`boxOf x`.

## Obstruction and boundary

The value function may be identical while source and evaluator derivative
fields differ, so value-level identity cannot imply derivative-level identity.
The companion does not prove Float64/libm derivative correctness, central-FD or
rounding error bounds, the coverage premise, endpoint margin, flowpipe
containment, residual absorption, continuous-domain coverage, admission, or
registry promotion.

This remains an inspectable conditional conjunct with
`integration_status: pending` and `admission_label: pending`.
