---
kind: task_claim
task_id: T-P5-187-ACTIVE-FAN-OVERLAP-KERNEL-GAUGE
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T21:19:30Z'
lease_expires_at: '2026-09-09T22:19:30Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-183-COMPLEMENTARY-ORTHANT-SCHUR-TRANSPORT, T-P5-185-PIECEWISE-ACTIVE-FACE-ORTHANT-SCHUR-FAN, T-P5-186-SINGULAR-PSD-RECESSION-ACTIVE-FAN]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — active-fan overlap kernel gauge

## Scope
Close the mathematical stitching seam left by the piecewise active-face Schur fan. For a fixed external direction `e>=0`, compare two valid orthant KKT/complementarity transports for the same inherited PSD block `P`. Prove that their minimizers differ only by `ker(P)`, that the KKT residual is unique, and that the reduced Schur energy is independent of the chosen active face. Lift this pointwise statement to an overlap cone and derive the exact restricted-matrix compatibility needed for generator-based cone packets.

## Non-overlap
Do not redo T-P5-185's cone cover construction, T-P5-186's singular recession/Farkas gate, T-P5-184's Z-matrix range solve, generic copositivity, source/provenance/admission audit, or Lean compilation. In particular, do not require reduced matrices from two faces to be globally equal when their cones meet only on a lower-dimensional seam.

## Intended deliverable
Exact two-KKT-point kernel-gauge theorem; residual uniqueness; reduced-energy equality; overlap-span matrix transport identity; rational piecewise regression showing global reduced-matrix equality is too strong; minimal checker/Lean statements and downstream routing guidance.