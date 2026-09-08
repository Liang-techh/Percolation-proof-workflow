---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY-OBSTRUCTION-20260908T182014Z
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-IDENTITY-OBSTRUCTION-20260908
source_agent: Godel the 6th
created_at: 2026-09-08T18:20:14Z
immutable: true
status: pending
integration_status: pending
admission_label: pending
result: CONDITIONAL_EXACT_FINITE_SAMESTORAGE_OBSTRUCTION
proof_status: exact_rational_algebra_with_external_source_slice_premise
receipt_kind: identity_obstruction_only
is_initial_bound_receipt: false
is_runtime_execution_receipt: false
source_binding_proven: false
initial_bound_binding_proven: false
runtime_execution_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
runtime_evaluation_observation: null
same_run_initial_upper_binding: null
state_mutation: false
registry_mutation: false
threshold_mutation: false
certificate_path: C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_certificate_V.csv
certificate_sha256: cab4a5182981bccbde18ace2d26ece5c0d7b7d3c3cf4a5a7e02e7fcda9b80601
candidate_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_identity_obstruction.py
candidate_sha256: a9101a8f05f48c3efae97f6cf74a9f43b09f926a833be6fb44f73e7a04fc5b62
result_path: examples/routeb_active_v_function_envelope/NEW_CONVENTION_identity_obstruction.json
result_sha256: 43827e8e52c0bafd33d4bb9982c92a68ffbb0e6ae5ab30f2442b0078579c5bb6
predecessor_review: agent_review_inbox/review-GH-ACTIVE-V-IDENTITY-OBSTRUCTION-20260908T181807Z.md
predecessor_sha256: ee47d032ac010ff5cbcadf39e680db9db83b236336951afadf15c9103857d1c4
requested_action: preserve pending and refuse only the contradicted sameStorage edge under the stated interpretation and source premise; do not infer an initial-bound failure or runtime theorem
---

# Immutable identity-obstruction envelope

New append-only review for the requested task ID. Existing artifacts and
reviews are untouched. Hashes above were freshly read and matched; this turn
did not rerun the checker, raw envelope, Julia, Lean/Lake or any producer.
The predecessor records the actual Python-only checks and their limitations.

## Exact slice and finite functional

Use the same block-only X0:
q4^2+q5^2+v4^2+v5^2<=9/400, all remote q/v coordinates zero.
Restrict further to t=0, q4=s, q5=v4=v5=0. Set

```text
points  = (-3/20, -3/40, 0, 3/40, 3/20)
weights = (1, -4, 6, -4, 1)
Lambda(P) = sum_i weights_i * P(points_i)
Lambda(s^k), k=0..4 = (0,0,0,0,243/320000).
```

Every point lies in X0. For the pinned 46-row certificate, exact restriction
and coefficient aggregation give:

| Interpretation | q4^4 coefficient | Nonzero Lambda(P) |
|---|---|---|
| Literal decimal tokens as rationals | 7549816188904203/125000000000000000 | 1834605333903721329/40000000000000000000000 |
| Python binary64 coefficients decoded to rationals | 8704345440016565/144115188075855872 | 423031188384805059/9223372036854775808000 |

This is an exact coefficient/moment calculation, not a sampled approximation
to a universal claim. Lambda vanishes on every degree-at-most-three polynomial.
If a comparison function restricts to degree at most two, equality at all five
points would force equal Lambda values, contradicting the table. Therefore an
exact sameStorage identity on X0 is impossible under those premises.

## Conditional source premise and narrow consumer conclusion

The separately inspected ideal Vfull/Vshift/cross conventions, including their
constant-centered versions, restrict to degree at most two on this slice:
velocities eliminate kinetic/cross terms, q2=q3=q5=0 fixes U, and the remaining
controller contribution is quadratic. The checker does NOT independently prove
Julia source semantics or this source-to-function premise.

The second interpretation is Python decoding only, NOT an observation or proof
of Julia parsing, multiplication/reduction order, or rounded evalV_fast values.
Both interpretations leave actual runtime/source refinement pending.

Consumer may use the obstruction only against the exact identity edge for
the pinned functions and map. It does not reject a separate comparison
inequality, the certificate polynomial's own initial upper bound, or all
possible storage conventions. In particular, distinct functions may share
an upper bound. Neither P(0)<=0 nor P(0)<=initial_storage_upper is established
by this envelope. The same-run link to that scalar remains null.

No successful admission, VERIFIED status, physical trajectory theorem or
runtime execution receipt is represented here; registry_eligible=false.
