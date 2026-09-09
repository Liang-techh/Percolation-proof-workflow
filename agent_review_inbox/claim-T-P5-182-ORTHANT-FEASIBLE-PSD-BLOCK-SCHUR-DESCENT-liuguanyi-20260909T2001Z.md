---
kind: task_claim
task_id: T-P5-182-ORTHANT-FEASIBLE-PSD-BLOCK-SCHUR-DESCENT
agent: 柳冠一
source_agent: 柳冠一
claimed_at: '2026-09-09T20:01:00Z'
lease_expires_at: '2026-09-09T21:01:00Z'
completed_at: null
unique_valid_claim: true
replacement_for: none
derived_from: '[T-P5-178-ZERO-LOADED-FACE-CRITICAL-CONE-SCHUR-BRIDGE, T-P5-179-CANONICAL-SUPPORT-DESCENT-PSD-FACE-INHERITANCE, T-P5-170-SIGN-COMPATIBLE-PIVOT, T-P5-181-STRICT-INTERIOR-FLAT-FACE-AUTOMATIC-RANGE-BRIDGE]'
status: claimed
result_path: null
result_commit: null
companion_path: null
companion_commit: null
---
# Review Claim — orthant-feasible PSD block Schur descent

## Scope
After T-P5-179 canonical support descent, the dropped zero-loaded parent coordinates form an inherited PSD block inside the T-P5-178 reduced copositivity problem, but those coordinates remain one-sided rather than signed. Prove the exact block criterion under an orthant-feasible range solve: for `H=[[P,B^T],[B,C]]` with `P>=0`, if `P X=B^T` and a gauge can be chosen with `X<=0` entrywise, then copositivity of `H` is equivalent to copositivity of `K=C-BX`. Separate the always-valid completion implication from the sign condition needed for the converse, prove gauge invariance of `K`, connect the scalar specialization to T-P5-170, and give a rational counterexample showing that unconstrained Schur elimination can falsely reject a copositive one-sided block.

## Non-overlap
Do not redo T-P5-178's signed-active Schur theorem, T-P5-179 support descent/PSD inheritance, T-P5-181 dual-slack extinction, generic copositivity enumeration, T-P5-170 scalar pivot recursion, source/provenance/admission audit, or Lean compilation. Treat failure to find an orthant-feasible solve as a routing condition, not a mathematical FAIL unless a separate obstruction is proved.

## Intended deliverable
Exact completion identity, one-sided attainability/equivalence theorem, gauge/rational-witness lemma, scalar-pivot specialization, explicit counterexample fixing the sign boundary, and a minimal checker-facing theorem packet for inherited-PSD-block elimination.