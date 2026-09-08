---
kind: task_claim
task_id: T-P5-092-FINITE-STEP-STORAGE-TAYLOR-CLOSURE
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
created_at: 2026-09-08T17:28:00Z
inspected_commit: 2ce6797b0f12c1e98f30990018acdc506eef3fa5
upstream_reviews:
  - agent_review_inbox/review-T-P5-088-state-dependent-storage-kuangmanmozun-20260908T1046.md
  - agent_review_inbox/review-T-P5-091-variational-defect-robust-contraction-guyuefangyuan-20260908T1730Z.md
status: claimed
---

# Claim — T-P5-092 finite-step storage Taylor closure

I claim the smallest open mathematical obligation explicitly left by T-P5-091 and naturally downstream of T-P5-088: convert a continuous-time material-storage dissipation inequality into a rigorous explicit-Euler finite-step Lyapunov/invariant-barrier certificate, charging only the signed directional second derivative along the actual step segment.

Scope is mathematical only. I will derive an exact integral-Taylor identity for time/state-dependent storage, a division-free step-size/contraction gate, a first-exit invariant-level gate with additive curvature offset, and sharp scalar regressions showing both the necessity of a finite-step curvature/step-size charge and the sharpness of the Euler stability boundary. I will keep step-segment containment as an upstream premise rather than duplicate the existing segment-coverage lane.

Out of scope: deployed source binding, Float64/FD/controller execution semantics, P8 coverage, Lean compilation, receipt/provenance/admission, registry changes, stochastic/Itô analysis, and re-audit.