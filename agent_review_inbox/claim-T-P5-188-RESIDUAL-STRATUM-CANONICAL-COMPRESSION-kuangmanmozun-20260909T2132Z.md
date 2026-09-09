---
kind: task_claim
task_id: T-P5-188-RESIDUAL-STRATUM-CANONICAL-COMPRESSION
agent: 狂蛮魔尊
source_agent: 狂蛮魔尊
claimed_at: '2026-09-09T21:32:00Z'
lease_expires_at: '2026-09-09T22:32:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE, T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — residual-stratum canonical compression

## Scope
Close one narrow mathematical seam left after T-P5-187: for a fixed external direction, use uniqueness of the KKT residual to identify the exact full minimizer set on the canonical zero-residual coordinates, prove that every solution of the reduced linear system gives the same full residual because PSD kills the lifted kernel, and thereby collapse overlapping active-face representatives to one residual-stratum affine feasibility problem.

## Non-overlap
Do not redo T-P5-185/186 active-fan construction, T-P5-187 residual uniqueness, generic provenance/source binding, admission, receipt, Lean compilation, or global external-cone coverage. Do not claim that the zero-residual set equals the support of every minimizer.

## Intended deliverable
Exact theorem characterizing all orthant minimizers by one principal linear system on the zero-residual stratum; PSD cross-kernel lemma; counterexample showing PSD is essential; formalizable statements and checker routing.