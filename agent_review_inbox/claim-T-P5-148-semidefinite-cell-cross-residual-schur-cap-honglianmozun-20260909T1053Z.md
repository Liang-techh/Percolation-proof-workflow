---
kind: task_claim
task_id: T-P5-148-SEMIDEFINITE-CELL-CROSS-RESIDUAL-SCHUR-CAP
source_agent: 红莲魔尊
claimed_at: 2026-09-09T10:53:00Z
inspected_commit: 0e95cf6dd3994c16ccfcce834e197b5f522bc294
status: claimed
---

# Claim — T-P5-148 semidefinite-cell cross residual Schur cap

I am taking the narrow mathematical child explicitly left open by T-P5-147: keep the physical-cell nullspace block `A >= 0`, but allow the cross solve `A L = H_NM` to have a matrix residual. The goal is to classify when that residual is finitely absorbable on the cylindrical nullspace, derive an inverse-free/root-free matrix PSD cap, and state the exact quotient curvature/linear/constant correction without duplicating T-P5-146 dual canonicalization or T-P5-147's scalar affine-residual proof.

No source admission, provenance/receipt audit, Lean compile, runtime semantics, coverage, registry mutation, or parent closure is in scope.