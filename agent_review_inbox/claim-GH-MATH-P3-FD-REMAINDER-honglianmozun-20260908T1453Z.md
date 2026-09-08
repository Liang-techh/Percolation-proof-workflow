kind: claim
task_id: GH-MATH-P3-FD-REMAINDER
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-08T14:53:00Z
inspected_commit: 141e4005b5d31421c416fcd0399010224b5c0ebf
target: NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean
status: claimed

scope:
  - Prove the minimal mathematics contract for a centered finite-difference derivative remainder from a uniform C3 bound on the full shifted stencil region.
  - Make the positive-step and shifted-region hypotheses explicit, including a uniform-cell / variable-step version.
  - Derive the exact linear residual-budget handoff from componentwise central-FD remainder bounds.
  - Preserve the x^3 sharpness/counterexample showing that pointwise C2 data at the center is insufficient.

dependencies:
  - agent_review_inbox/task_queue.md assignment GH-MATH-P3-FD-REMAINDER
  - target theorem scaffold NEW_CENTRAL_FD_HULL_C2C3_CENTRAL_FD_REMAINDER.lean if/when source owner exposes its canonical path

non_overlap:
  - No evaluator implementation/source binding claim.
  - No Float64/libm/rounding claim.
  - No provenance, receipt, admission, audit, or duplicate validation work.
  - No takeover of other agents' active Lean/source lanes.

expected_output:
  - immutable review_result with assumptions, derivation, exact constants, division-free forms, candidate theorem statements, residual-budget bridge, precise failure boundaries, and remaining source-binding obligation.
