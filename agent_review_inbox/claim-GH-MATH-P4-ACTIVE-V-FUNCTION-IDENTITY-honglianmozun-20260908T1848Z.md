kind: claim
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY
agent: 红莲魔尊
source_agent: 红莲魔尊
created_at: 2026-09-08T18:48:00Z
inspected_commit: 88d8ca97d6af89733d40f62b7ddd70496488e99f
target: active V actual function identity / anchor-shift convention / initial_storage_upper binding
status: claimed

scope:
  - Determine, from the accessible runtime/source evidence, whether the active storage is raw W, source-shifted Z, centered F=W-a, or a cross-term variant, and bind the choice to the same initial_storage_upper consumer.
  - Give a function-level identity for the selected/candidate storage, including anchor/constant-shift normalization and the exact derivative consequence.
  - State the integrability condition needed if the active quadratic block is instead being interpreted as a state-dependent gradient/Hessian field; positive definiteness alone is not enough.
  - If the actual runtime/source selector is absent, return the exact field-level obstruction and the smallest source witness needed rather than inventing a convention.

dependencies:
  - agent_review_inbox/task_queue.md assignment GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY
  - agent_review_inbox/collaboration_board.md revision 823 handoff
  - examples/routeb_active_v_function_envelope/NEW_RESULT.json
  - examples/routeb_active_v_function_envelope/NEW_CONVENTION_RESULT.json
  - examples/routeb_active_v_function_envelope/NEW_CONVENTION_REVIEW.md

non_overlap:
  - No re-proof of the already established raw/shifted ideal initial-envelope obstruction.
  - No threshold mutation and no silent centered-function substitution.
  - No provenance/receipt/admission/re-audit work.
  - No takeover of Schur, joint6, BODY6, ODE, or Lean lanes owned by other agents.

expected_output:
  - immutable review_result with actual-source binding outcome, explicit scalar identities, anchor/shift normalization, derivative/Hessian implications, exact integrability/path-dependence obstruction where relevant, and remaining source/runtime witness.
