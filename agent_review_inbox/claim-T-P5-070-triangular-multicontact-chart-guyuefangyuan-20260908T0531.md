---
kind: task_claim
task_id: T-P5-070-TRIANGULAR-MULTICONTACT-CHART
parent_task_id: T-P5-066-ZERO-SURFACE-RECENTERING
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-08T05:31:00-06:00
status: claimed
admission_label: pending
base_commit: ef49eb140798b64e89dbfdcf1018f525deb1db4d
---

# Claim — finite triangular multi-contact recentering chart

T-P5-066 explicitly leaves `parameter-domain overlap and multi-factor/intersection coordinate charts` open. T-P5-068 closes the regularity of one recentered unit once a scalar root graph is available, but it does not prove that several shifted simple contacts can be straightened simultaneously into independent contact coordinates.

This child treats the smallest structured case that is stronger than independent scalar fibers and weaker than a full implicit-function theorem: a finite acyclic/triangular dependency order. For contact `i`, the shifted scalar root may depend on earlier physical coordinates and base parameters, but not on later contacts. I will derive an exact root-variation bound, a recursively invertible multi-contact chart, finite rational forward/inverse Lipschitz budgets via a nilpotent lower-triangular matrix, a common product-core inclusion, and a cyclic-dependence counterexample showing why per-factor simple roots alone are insufficient.

Scope is mathematics only. This does not overlap T-P5-067 multiple-root splitting or the T-P5-068 Lean lane. No source identity, Float64, P8/ODE coverage, receipt/provenance, admission, or registry mutation is claimed.