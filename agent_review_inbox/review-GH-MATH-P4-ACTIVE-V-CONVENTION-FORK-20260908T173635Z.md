---
kind: review_result
review_id: review-GH-MATH-P4-ACTIVE-V-CONVENTION-FORK-20260908T173635Z
created_at: 2026-09-08T17:36:35Z
task_id: GH-MATH-P4-ACTIVE-V-FUNCTION-ENVELOPE
source_agent: codex-active-v-convention-fork
integration_status: pending
admission_label: pending
status: RAW_SHIFTED_INCOMPATIBLE_CENTERED_INITIAL_CANDIDATE_BINDING_OPEN
proof_status: conditional_ideal_function_paper_proof_and_rational_checks
source_binding_proven: false
initial_bound_binding_proven: false
registry_eligible: false
formal_certificate_allowed: false
lean_compile_status: not_run
julia_execution: false
prior_envelope_rerun: false
state_mutation: false
registry_mutation: false
threshold_mutation: false
requested_action: determine actual active convention and bind its value function; do not reuse raw or shifted initial bounds contradicted by the fixed ideal envelope
---

# Convention fork outcome

Fixed the predecessor's analytic K and block-only X0. Consumed, without
rerunning its arithmetic, NEW_RESULT.json SHA256
71743ce600e1caaf8bd4f8a4a1e55d7c6972b3644c03374ba4b0323f5dbb88f5.
Rechecked its seven source hashes and four additional convention sources.
No H_acc lane, source producer, Julia or local Lean/Lake was used.

Raw W has the previously established uniform lower
L=32462895903/6400000000>1>u, where
u=492033745203/25600000000000 is the unchanged initial_storage_upper.

1. Source Vshift is Z=W+c, c=205029/40000>0; its controller square shift is
   zero for this analytic g0. Hence Z>=65267535903/6400000000>1, not a rescue.
2. Switching the linear compensation sign makes no change for this fixed
   analytic zero g0. This is not a statement about FD/runtime compensation.
3. On X0 the targeted gain increment vanishes, and the remaining cross term
   is bounded in absolute value by delta=8419917/6400000000000. Thus the raw
   cross variant T>=32462887483083/6400000000000>1>u. No targeted dynamics or
   damping was imported into K, and no favorable cross-term sign was assumed.
4. An EXPLICIT distinct centered function F=W-a, a=2029689/400000, has the
   all-X0 identity F=kinetic+B*(cos(q5)-1)+(3/10)q4^2+(1/4)q5^2. With the
   predecessor's same regularized mass operator bound, F<=27/4000<u.
   Likewise T-a<=43208419917/6400000000000<u. This is direct function-value
   algebra and a uniform inequality, not a Hessian/CSV/origin-only shortcut.

Centering consistently on BOTH sides preserves the raw incompatibility:
W<=1 iff F<=-1629689/400000; Z<=1 iff F<=-3679979/400000.
Keeping numerical threshold 1 but replacing W by F selects a different
sublevel. No such selection or threshold edit has been made here.

## Minimum remaining witness

If the actual consumer already intends F (or explicitly T-a), supply its
same-K value-function identity on X0, independently checked source/operator
premises, and the resulting function-indexed initial bound with the unchanged
u and threshold. If the active V is raw W or Z, the uniform inequalities rule
out that initial binding in this fixed ideal configuration.

Full barrier consumption additionally requires same-storage path-domain value
binding, growth, coercivity/caps, p_B comparison and strict gate. Constant
shifts preserve derivatives but not those other inequalities; a cross term
also changes derivatives. No initial-only result is a barrier theorem.

## New artifacts and focused validation

All artifact paths below are relative to the workspace:

- examples/routeb_active_v_function_envelope/NEW_CONVENTION_check.py
  SHA256 3d8181ca125ed3925f85467cd7de793de3044c329c078ab3810eaf8f441b4337
- examples/routeb_active_v_function_envelope/NEW_CONVENTION_RESULT.json
  SHA256 4feae94228e22edb9910eb000cbdfae8685a5295c5b0d02fd4459f2db44b11d5
- examples/routeb_active_v_function_envelope/NEW_CONVENTION_REVIEW.md
  SHA256 853e510e2724561f698180bbe729bde15c6f1cebdd3a3d1657eb9a2877af34ce

`python -B .../NEW_CONVENTION_check.py` exited 0 for convention arithmetic
assertions only. A focused read-only check confirmed saved/live result equality
and rejection of an in-memory corrupted predecessor hash. No full regression
or prior polynomial-envelope rerun occurred. All runtime evidence is null and
admission flags false. Only these NEW_CONVENTION_* files and this inbox review
were written; old artifacts, shared scripts, state, registry and thresholds
were not modified by this task.
