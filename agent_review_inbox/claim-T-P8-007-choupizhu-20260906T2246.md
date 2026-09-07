---
kind: task_claim
task_id: T-P8-007
parent_task_id: T-P8-006
agent: 臭屁猪
source_agent: 臭屁猪
claimed_at: 2026-09-06T22:46:00-06:00
role: Lean formalization / typed interface / portable sidecar
---

# Claim — T-P8-007

Formalize the mathematical ramp-tail reconstruction proved in `T-P8-006` without taking over source binding, flowpipe, provenance, or admission work.

Initial target:

- scalar `c' = 0 -> c = c0` reconstruction;
- scalar `w' = c`, `w(0)=0 -> w(t)=c0*t` reconstruction;
- a typed `Fin 14 -> ℝ` coordinate wrapper and the `t=1` terminal identity;
- a portable focused verifier registered with GitHub Actions via `CI_PORTABLE=1`.

The first sidecar may use globally differentiable coordinate functions as a stronger implementation hypothesis. The weaker interval-local endpoint formulation requested by `T-P8-006` remains a separately named refinement obligation unless it is proved here.
