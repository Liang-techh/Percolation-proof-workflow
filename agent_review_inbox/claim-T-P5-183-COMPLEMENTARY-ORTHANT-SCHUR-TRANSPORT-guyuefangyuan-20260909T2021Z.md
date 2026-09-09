---
kind: task_claim
task_id: T-P5-183-COMPLEMENTARY-ORTHANT-SCHUR-TRANSPORT
agent: 古月方源
source_agent: 古月方源
claimed_at: '2026-09-09T20:21:00Z'
lease_expires_at: '2026-09-09T21:21:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-178-ZERO-LOADED-FACE-CRITICAL-CONE-SCHUR-BRIDGE, T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE, T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — complementary orthant Schur transport

## Scope
Strengthen T-P5-182's lossless one-sided PSD-block elimination from the special zero-residual transport `P Y=-B^T` to a boundary-active KKT/complementarity transport. For `H=[[P,B^T],[B,C]]` with `P>=0`, study rational matrices `Y>=0` and `R:=P Y+B^T>=0`. Derive the exact completion/lower-bound identity, identify the additional complementarity condition needed for a two-sided copositivity equivalence, and specialize it to one retained critical row as an LCP-style scalar Schur certificate. Give a counterexample showing that checking complementarity column-by-column is insufficient when several retained critical directions are mixed.

## Non-overlap
Do not redo T-P5-182's `R=0` monotone range solve, T-P5-178 signed-active Schur theorem, T-P5-179 true-support descent/PSD inheritance, generic copositivity enumeration, source/provenance/admission audit, or Lean compilation. Treat absence of a complementary transport as a routing condition, not as non-copositivity.

## Intended deliverable
Exact algebraic identity and one-way sufficient bound for `R>=0`; exact copositivity iff under full matrix complementarity; single-external-row LCP specialization; mixed-column obstruction/counterexample; minimal rational checker packet and suggested Lean theorem statements.
