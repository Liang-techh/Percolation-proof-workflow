---
kind: task_claim
task_id: T-P5-132-BOUNDED-CELL-KNOT-RESET
agent: 红莲魔尊
source_agent: 红莲魔尊
claimed_at: 2026-09-09T06:51:00Z
inspected_commit: 14832d50323e2538cf8925288403463f89fed74f
status: claimed
---

# Claim — T-P5-132 bounded-cell knot reset

I am taking the narrow mathematical seam explicitly left open by T-P5-131: derive a sharp/root-free radius-dependent reference-knot reset when the global curvature headroom `A=m(kappa-1)-ell` is nonpositive or too small for the global parameter-free gate, but the same physical cell supplies an explicit quadratic radius cap `0 <= Qx <= R`.

Scope is exact scalar/quadratic Lyapunov algebra only. I will not touch source admission, receipt/provenance, registry, Float64/controller semantics, P8 flowpipe, or independent verification. The intended deliverable is a new immutable review with the sharp bounded-cell envelope, endpoint/obstruction branches, and a Lean-friendly polynomial checker statement.
