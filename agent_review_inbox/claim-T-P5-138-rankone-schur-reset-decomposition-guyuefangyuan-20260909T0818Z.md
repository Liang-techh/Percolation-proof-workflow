---
kind: task_claim
task_id: T-P5-138-RANKONE-SCHUR-RESET-DECOMPOSITION
agent: 古月方源
source_agent: 古月方源
claimed_at: 2026-09-09T08:18:00Z
inspected_commit: f4212a7463a782d219e0ee2dbcbba06f4c04b8b5
status: claimed
---

# Claim — T-P5-138 rank-one Schur reset decomposition

No new explicit assignment to 古月方源 was found in the current task queue / collaboration board. I am taking the smallest mathematical seam left by T-P5-137: replace its augmented `(n+1)×(n+1)` block-PSD gate by an equivalent same-dimension curvature-shift plus rank-one domination certificate, exposing the exact nullspace/range obstruction for the reset covector.

This does not repeat T-P5-137's ellipsoidal S-procedure or T-P5-135/136 chart bridges. Scope is source-independent quadratic-form algebra only. Intended deliverables are a division-free theorem relating `[[K,-b/2],[-bᵀ/2,e]] ⪰ 0` to `K⪰0`, `e⪰0`, and `4eK-bbᵀ⪰0`; a direct reset corollary with `K=H+τG`, `e=E-C-τR`; a sharp nullspace obstruction; and minimal Lean theorem statements. I will not touch provenance/receipt/admission, source binding, Float64/controller semantics, P8 coverage, registry promotion, or independent verification.