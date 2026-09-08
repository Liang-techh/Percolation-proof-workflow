---
kind: review_result
review_id: review-T-P3-central-FD-hull-c2c3-central-fd-remainder-codex-20260908T0519
task_id: T-P3-central-FD-hull
source_agent: Codex
created_at: 2026-09-08T05:19:08-06:00
inspected_paths:
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER_REVIEW.md
integration_status: pending
admission_label: pending
---

# T-P3-central-FD-hull — bounded central-FD remainder interface

## Result

The bounded contract fixes the same exact source function, same central-FD
evaluator, same step/direction semantics, same listed box, and same shifted
region.  It separately requires explicit C3 regularity and the remainder estimate

```text
|FD_h f(x) - f'(x)| ≤ h² M₃ / 6
```

and a residual budget inequality.  With the existing same-box derivative
binding, this yields a central-FD error bound to the concrete exact-real DH
first derivative at each covered point.

## Obstruction and frontier

For `f(x)=x^3`, `x=0`, `h=1`, the central difference is `1` while `f'(0)=0`,
so a zero remainder claim is false.  Existing pointwise hull fields do not
prove the segment-level C3 theorem, common step/direction semantics,
shifted-box membership, or residual budget.

Derivative-level source/Float64 correctness, coverage, flowpipe containment,
residual absorption beyond the local budget, admission, and registry promotion
remain open.  This review is `integration_status: pending` and
`admission_label: pending`.
