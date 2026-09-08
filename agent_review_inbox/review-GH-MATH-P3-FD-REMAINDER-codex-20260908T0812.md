---
kind: review_result
review_id: review-GH-MATH-P3-FD-REMAINDER-codex-20260908T0812
task_id: GH-MATH-P3-FD-REMAINDER
source_agent: Codex
created_at: 2026-09-08T08:12:20-06:00
inspected_paths:
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER_REVIEW.md
integration_status: pending
admission_label: pending
---

# GH-MATH-P3-FD-REMAINDER — minimal central-FD remainder interface

## Result

The reusable interface fixes one exact-real source function, one central step
and direction, one listed box, and both shifted-region memberships.  It
separately requires explicit C3 regularity, the central remainder estimate

```text
|FD_h f(x) - f'(x)| ≤ h² M₃ / 6
```

and a residual-budget inequality.  At a covered point, these premises bind the
central-FD evaluator to the exact-real DH first derivative with the requested
budgeted error bound.

## Counterexample and frontier

For `f(x)=x^3`, `x=0`, and `h=1`, the central difference is `1` while
`f'(0)=0`; a zero remainder bound is therefore false.  Pointwise derivative
hulls do not prove the segment-level C3 estimate, step/direction semantics,
shifted-region membership, or residual absorption budget.

Concrete DH/Float64 correctness, continuous coverage, flowpipe containment,
residual absorption beyond the local budget, admission, and registry promotion
remain open.  This review remains `integration_status: pending` and
`admission_label: pending`.
