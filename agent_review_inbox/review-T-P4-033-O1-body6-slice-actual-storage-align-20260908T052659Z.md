---
kind: review_result
review_id: review-T-P4-033-O1-body6-slice-actual-storage-align-20260908T052659Z
task_id: T-P4-033-O1-body6-slice
source_agent: codex-body6-math-lane
created_at: 2026-09-08T05:26:59Z
integration_status: pending
status: OPEN_UNCOMPILED
compile_status: OPEN_UNCOMPILED
lean_receipt_status: missing
admission_label: pending
proposed_integration_target: metadata_only
requested_action: review_exact_alignment_and_obtain_independent_Lean_receipt_before_any_theorem_admission
artifact_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean
artifact_sha256: f8da2e44f9afc4c80fc14e81a1c59626d5af98071300a009aecd33463d3bef56
companion_path: examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.review.md
companion_sha256: 025a1e0d810a9f483f945bb96caf43a2e0d6e11ba7bcf1521666de1022e7efe2
---

# BODY6 lane: ActualStorage / ActualShift alignment review result

This review uses the existing BODY6 task identifier
`T-P4-033-O1-body6-slice`, which is present in the collector's TASK_TARGETS.
It is an advisory storage/domain companion within that lane, not a new
canonical body-source theorem, a proof of global h_body_6, or a new task/node
created in state. This submission does not request registry promotion.

## Artifacts

- [Open Lean sidecar](../examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.lean)
- [Independent mathematical review](../examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_ACTUALSTORAGEALIGN20260907.review.md)

Their exact byte hashes are recorded in the envelope. No integration command
was run, no processed marker was created, and no registry/state was modified
by this submission.

## Alignment premises and exact conclusion

The sidecar explicitly specializes ActualStorage to f=1,h=0 and fixed
p,H,Uzero, retaining the same q/v coordinates. This yields

```text
S(q,v) = kinetic(Mactual(q),v) + R(q),
R(q) = U(q)-Uzero-kinetic(H,q)+(7/75)*q4^2+sum p_i*q_i^2.
```

For a stated configuration domain Q, `Alignment` requires:

1. Mactual(q)=Mencoded(q) for every q in Q.
2. R(q)=RouteBPotentialSlice.W(q) for every q in Q.

A sufficient decomposition of the second field separately binds normalized
potential and quadratic compensation:

```text
U(q)-Uzero = encodedPotential(q)-encodedPotential(0),
sum p_i*q_i^2+(7/75)*q4^2 = kinetic(H,q)+proportionalEnergy(q).
```

These fields imply S=E on Q, where E is the ActualShift unshifted
kinetic+encoded-W expression. The ActualShift comparison quantity is E+B,
with exact B=4079979/400000. Hence the shifted identity is S+B=E+B;
the sidecar never asserts S=E+B. No current candidate Alignment instance,
physical mass identity or coefficient selection is supplied.

## Path inclusion and cap transfer

`aligned_path_cap_transfer_attempt` requires the *same* q(t),v(t),
q(t) in Q for every t in [0,1], an actual source bound S(q(t),v(t))<=cap,
and cap+B<=bar. It then concludes Eshift(q(t),v(t))<=bar.

Path-domain inclusion is an input, not inferred from the intended barrier.
For a larger state domain D(t), the caller must separately prove path
membership and its projection into Q. Initial membership alone is not
enough. If the source cap already bounds S+B, equality transfers that cap
directly; the shift must not be charged twice. No ODE, first-exit,
continuation, circle invariance or source-to-Float64 statement is proved.

## Exact counterexample preventing fixed-threshold promotion

At q=v=0, choose U to be the encoded potential and Uzero=U(0).
For arbitrary H,p,M, the specialized ActualStorage S equals zero, while
the encoded W is zero and Eshift equals B=4079979/400000>1.

`actual_origin_fixed_bar_counterexample_attempt` therefore states exactly
S(0,0)<=1 and not Eshift(0,0)<=1. This is an algebraic counterexample using
the actual definitions to omitting the shift at threshold 1. It is not a
simulated trajectory, controller-failure claim or full BODY6 Schur result.

## Compilation and admission boundary

The old ActualStorage and ActualShift sources have historical successful
receipts, inspected in COMPILEDLEDGERBINDING. Those receipts do not compile
this new sidecar or instantiate its source/domain hypotheses. The sidecar
directly imports those modules and therefore requires a compatible pinned
dependency environment for any future check.

No Lean/Lake invocation or broad regression was run. Static review and
hashing are the only new validation. `OPEN_UNCOMPILED` remains the correct
status; elaboration, theorem dependency/axiom reports and an independent
Lean receipt are pending. Neither proof-attempt text nor imported receipts
authorize theorem/registry admission or closure of the BODY6 parent task.
