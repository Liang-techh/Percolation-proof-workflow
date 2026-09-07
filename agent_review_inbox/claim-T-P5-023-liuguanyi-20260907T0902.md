---
kind: task_claim
task_id: T-P5-023
source_agent: 柳冠一
agent: 柳冠一
claimed_at: 2026-09-07T09:02:00-06:00
inspected_commit: 8e2773065a77559fb9e0671f529580a5400ddc4e
status: claimed
---

# T-P5-023 — piecewise-cell transport from local Jacobian bounds to the centered P5 gain

I am claiming a new, disjoint interface-math child continuing `T-P5-022`.

Scope: remove the global-convex-segment requirement from the source-to-centered-gain adapter.  Derive a path/cellwise transport theorem that composes local residual increment/Jacobian bounds across a certified finite chain of source cells, with exact coordinate and force normalization, and identify the precise obstruction when only endpoint coverage is known.

This task does not re-audit provenance, receipts, admission, existing Lean sidecars, or any task already claimed by another Agent.  It will not claim source/Float64 semantics, P8 flowpipe coverage, P5/P8/M4 closure, or registry admission.
