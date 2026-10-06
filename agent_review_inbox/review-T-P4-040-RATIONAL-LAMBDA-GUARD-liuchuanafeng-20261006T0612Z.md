---
kind: review_result
review_id: review-T-P4-040-RATIONAL-LAMBDA-GUARD-liuchuanafeng-20261006T0612Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-06T06:12:00Z
inspected_commit: 020950103717db7b1f8dbebcdf7df9cc8834bede
claim_commit: 020950103717db7b1f8dbebcdf7df9cc8834bede
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md
  - agent_review_inbox/review-T-P4-040-juyangxianzun-20260907T1653.md
  - agent_review_inbox/review-T-P4-040-divfree-liuguanyi-20260907T1816.md
  - examples/routeb_p4_rational_lambda_guard_lean/
task_id: T-P4-040
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P4-040 admission audit: interval guard is algebraic, certificate surface still open

## Question

At commit `020950103717db7b1f8dbebcdf7df9cc8834bede`, do the existing `T-P4-040` math review, Lean sidecar receipt, and later division-free sibling already supply a concrete common rational interval, source-bound row coefficients, or any source/coverage/registry admission for a P4 cell?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The chord identity, the completed-square identity, the convex endpoint gate, and the three published counterexamples are algebraically consistent as a source-independent interface. They do not close a finite-row endpoint packet, a concrete cell interval, true-DH/Float64 realization, coverage, or registry.

This pass did not compile anything. It does not reissue the 2026-09-07 Lean review as a fresh `compiled_candidate`, and it does not reclassify that historical receipt as `verified`. The historical file `review-T-P4-040-juyangxianzun-20260907T1653.md` remains a prior author's candidate receipt; this audit does not overwrite it and does not treat its Actions log as re-executed evidence.

This is not `verified`: no kernel run and no source packet in this pass. It is not `rejected`: the identities and the three counterexamples check out. It is not `architecture_only`: the math review states exact scalar theorems. It is not a new `compiled_candidate`: this agent did not run `verify.sh`.

Prior authorship is preserved. This file does not overwrite 狂蛮魔尊, 巨阳仙尊, or 柳冠一.

Label collision is recorded, not resolved. Revision 742 later reused `T-P4-040` for the division-free core. That sibling remains a separate pending interface. This audit does not merge the two children and does not treat either as a parent close.

## Evidence inspected (read-only)

1. **Queue does not close this leaf.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` records `T-P4-040` twice: first as the rational common-lambda guard still needing an independent pinned receipt, then as the division-free compression of `T-P4-039`. Both notes keep the family pending and forbid source/P8 assumptions and registry promotion.

2. **Math review is source-independent and self-labeled pending.** `review-T-P4-040-rational-lambda-guard-kuangmanmozun-20260907T1642.md` blob `44a33293c7ab6aefe25b31c3440881b3dbaf0aa9` supplies the endpoint identity, symmetric rounding checks, and one-sided coefficient envelope. It explicitly denies DH source binding, coverage, Float64 containment, and registry change.

3. **Independent exact-rational checks.** For `q(s)=2 s^2-5 s+1`, `a=1/2`, `b=3/2`, `t=2/5`, both sides of the chord identity equal `-47/25`. For `A=3`, `G=7`, `P=2`, `theta=4/3`, both sides of `(2 A theta-G)^2-(G^2-4 A P)=4 A q` equal `-24`. Concave counterexample `q(s)=-s^2+4 s-3` has endpoint values `0,0` and midpoint `1`. Midpoint-only counterexample `q(s)=s^2-4 s+3` has `q(2)=-1` but `q(1/2)=q(7/2)=5/4`. Envelope sign failure at `s=-1`, `G=2`, `G_low=1` gives `-G s=2 > 1=-G_low s`. These checks are exact rational arithmetic only; they are not a Lean receipt.

4. **Division-free sibling does not add a witness.** `review-T-P4-040-divfree-liuguanyi-20260907T1816.md` blob `96cd80d9edf0ffdc4375dff1b94eed1150da739d`, `admission_label: pending`, states four ordered-ring lemmas and an exact `Rat -> Real` seam. It does not exhibit row coefficients or a shared theta for an actual cell, and it already records the label collision.

5. **Historical Lean surface is present but not re-run.** Directory `examples/routeb_p4_rational_lambda_guard_lean/` still contains `P4RationalLambdaGuard.lean` blob `20af999c248e2d26589b37a2ff9b68601ddac65a`, `verify.sh` blob `dc65ba2476cae91d7c921e16c79082b083cbf9c9`, `README.md` blob `4d644014006d4f75b3628e99994734719874f3fb`, and `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`. The prior Lean review cites head `b759403c69510a0e551212402efbc7c5b726e75e`, Actions run `34167818945`, and axiom list `[propext, Classical.choice, Quot.sound]`. This pass did not re-execute that job. The current Lean blob differs from the cited run head, so the old Actions log is not a receipt for the current blob.

```text
command: not run
exit_code: not claimed
lean_toolchain: not pinned by this agent
axiom_print: not executed
placeholder_scan: not run by this agent
source_binding: not present
common_rational_interval_for_a_P4_cell: not exhibited
```

## Obstruction

```text
identity_surface: source-independent, algebraically consistent, historically compiled by another author
label_collision: rational-interval guard and division-free core share T-P4-040; neither closes the parent
missing_for_parent_close:
  one common rational 0<a<=b with endpoint checks on every actual row
  exact (P,G,A) or (P_up,G_low,A_up) extracted from those same rows
  interval membership of the implemented s=lambda-1, not endpoint PASS alone
  fresh pinned Lean receipt if the historical candidate is to be reissued against the current blob
  true-DH / Float64 realized-lambda containment
  P8 domain/trajectory coverage
blobs:
  math_review: 44a33293c7ab6aefe25b31c3440881b3dbaf0aa9
  lean_review: 7d8ec5c4df3bf2de401eba817628d23376b5027c
  divfree_review: 96cd80d9edf0ffdc4375dff1b94eed1150da739d
  sidecar_lean: 20af999c248e2d26589b37a2ff9b68601ddac65a
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a later Lean owner may re-run the existing sidecar, but that is a new receipt obligation, not implied by this audit;
- an untrusted proposer of `a,b` or envelopes is not a witness until every row endpoint check is bound to the same cell;
- endpoint PASS without `P>=0` or a convex upper envelope is not a PASS;
- a negative midpoint value is not a rounding-radius certificate;
- the `G_low` envelope direction requires `s>=0`;
- the division-free core still needs a supplied shared theta and does not construct one;
- coverage, Float64 enclosure, and comparator admission stay outside this leaf.

## Integration target and requested action

- Target: documentation / inbox provenance only. Leave `T-P4-040` open until a checked common rational interval and a fresh source-bound consumer exist.
- Requested action: harvest this as a pending admission audit. Do not treat the algebraic interface or the historical Actions log as verified, do not collapse the two `T-P4-040` children, and do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or invent an exit code or axiom list.
- Did not add a Lean sidecar or alter the 2026-09-07 identity statements.
- Did not claim a concrete cell interval, source equality, coverage, or P4/M4 closure.
- Did not overwrite prior reviews or claims.
- Did not edit registry, state, task queue, or formal proofs.
