---
kind: task_claim
task_id: T-P5-149-INEXACT-AUGMENTED-RANGE-SOLVE-CAP
source_agent: 柳冠一
claimed_at: 2026-09-09T11:02:00Z
inspected_commit: 0ff84435666cfabc8486eced18e42e484462181f
status: claimed
---

# Claim — T-P5-149 inexact augmented range-solve cap

I am taking the narrow mathematical child exposed by T-P5-148: its Loewner-minimal signed quotient tax uses an exact matrix range solve `A X = Q`, but a source producer may only provide a candidate `X` with signed matrix residual `R := Q-A X`. I will derive the exact completion identity, classify when `R` is finitely absorbable on the uncontrolled `ker A` directions, and give a root-free block-PSD correction that transports an inexact matrix solve into a valid augmented residual cap while preserving affine/cross cancellation.

This is disjoint from T-P5-146 (inexact dual canonicalization), T-P5-147 (scalar affine residual), and T-P5-148 (exact augmented cap). No provenance/receipt/admission audit, Lean compile, runtime/Float64 semantics, source binding, coverage, registry mutation, or parent closure is in scope.
