---
kind: review_result
review_id: review-T-P3-central-FD-hull-c2c3-dh-evaluator-codex-20260907T2324
task_id: T-P3-central-FD-hull
source_agent: Codex
created_at: 2026-09-07T23:24:51-06:00
inspected_paths:
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_SOURCE_BINDING.lean
  - examples/routeb_p3_central_fd_hull/NEW_CENTRAL_FD_HULL_C2C3_DH_EVALUATOR_CONJUNCT.lean
integration_status: pending
admission_label: pending
---

# T-P3-central-FD-hull — C2/C3 to DH evaluator value-level conjunct

## Result

The companion proves the minimal value-level identity

```text
sourceFunction x = dhEvaluator x
```

on the existing domain, assuming the exact-real evaluator equation

```text
dhEvaluator x = sourceM x + sourceC x + sourceG x.
```

At the same covered point, the endpoint-uniform consumer also supplies the
positive common margin.  The selected box is not changed: it is the existing
`boxOf x`, with its listed-box and region facts supplied by the existing
coverage premise.

## Boundary

This result does not prove derivative-level identity between the C2/C3 fields
and derivatives of `dhEvaluator`.  It does not prove the coverage premise, the
Float64/libm-to-exact-real evaluator equation, central-FD error bounds,
rounded-source implementation, flowpipe containment, residual absorption,
continuous-domain coverage, admission, or registry promotion.

The result is therefore an inspectable conditional conjunct only.  It remains
`integration_status: pending` and `admission_label: pending`.
