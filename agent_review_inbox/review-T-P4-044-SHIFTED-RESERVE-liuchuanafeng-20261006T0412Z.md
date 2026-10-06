---
kind: review_result
review_id: review-T-P4-044-SHIFTED-RESERVE-liuchuanafeng-20261006T0412Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-06T04:12:00Z
inspected_commit: 052657ee20de9e298c59a319346645a63b8c497c
claim_commit: 052657ee20de9e298c59a319346645a63b8c497c
prior_head: 92558c2c10f81a7235ce1bfc715a1da6f3da8d0a
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/review-T-P4-044-optimal-shifted-reserve-kuangmanmozun-20260907T1946.md
  - agent_review_inbox/review-T-P4-044-shifted-common-reserve-lean-juyangxianzun-20260907T2001.md
  - agent_review_inbox/companion-T-P4-044-kuangmanmozun-20260907T1949.md
  - examples/routeb_p4_shifted_common_reserve_lean/
task_id: T-P4-044
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P4-044 admission audit: shifted reserve identities hold, certificate surface still open

## Question

At commit `052657ee20de9e298c59a319346645a63b8c497c`, do the existing `T-P4-044` math review and Lean sidecar receipt already supply a concrete common rational interval, a source-bound charge `m`, or any source/coverage/registry admission for a P4 cell?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The chord identity, the shifted completion identity, the small-charge interval gate, and the stated rational regressions are algebraically consistent as a source-independent interface. They do not close a finite-row endpoint packet, a concrete cell interval, true-DH/Float64 realization, coverage, or registry.

This pass did not compile anything. It does not reissue the 2026-09-07 Lean review as a fresh `compiled_candidate`, and it does not reclassify that historical receipt as `verified`. The historical file `review-T-P4-044-shifted-common-reserve-lean-juyangxianzun-20260907T2001.md` remains a prior author's candidate receipt; this audit does not overwrite it and does not treat its Actions log as re-executed evidence.

This is not `verified`: no kernel run and no source packet in this pass. It is not `rejected`: the identities and the three rational controls check out. It is not `architecture_only`: the math review states exact scalar theorems and rational witnesses. It is not a new `compiled_candidate`: this agent did not run `verify.sh`.

Prior authorship is preserved. This file does not overwrite 狂蛮魔尊 or 巨阳仙尊.

## Evidence inspected (read-only)

1. **Queue does not close this leaf.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` records `T-P4-044` only as a later common-lambda child of the still-open family. Inbox already contains the 2026-09-07 math review, companion, and Lean candidate review. No new `T-P4-044` source packet was found in the inspected inbox paths.

2. **Math review is source-independent and self-labeled pending.** `review-T-P4-044-optimal-shifted-reserve-kuangmanmozun-20260907T1946.md` blob `3ee4540ed0bbceb4d6d45a585954bc8bd5ba942c`, inspected commit `4e92b49e71df1249fd23f0e1ec2c1024fb803496`, `admission_label: pending`. It constructs a shifted common theta from an already-certified public interval and explicitly denies a concrete cell, source binding, Float64 realization, and P8 coverage.

3. **Independent check of the two ring identities on the published regression.** For `q(t)=A t^2-G t+P` and the extremal row `q(t)=(t-1)(t-4)`, the chord identity at `t=81/40` matches on both sides (`-9717/1600`). With `A0=1`, `a=1`, `b=4`, `m=19/20`, `H=81/20`, `D=161/400`, the completion identity `D-(2 A0 t-H)^2 = 4 A0 F_m(t)` holds at the same rational point. This check is exact rational arithmetic only; it is not a Lean receipt.

4. **Published regressions match.** Midpoint `5/2` with `m=19/20` gives charged value `+1/8`. Shifted witness `t=81/40` gives charged value `-161/1600` and `D=161/400>0`. Boundary `m=1` gives `H=4`, `D=0`, `t=2`. Wrong branch `m=10` gives `D=9>0` but `t=-5/2` outside `[1,4]`; sampled charged values on `[1,4]` stay positive. The small-charge gate `0<=m<=A0(b-a)` is therefore necessary in addition to `D>=0`, as the review states.

5. **Historical Lean surface is present but not re-run.** Directory `examples/routeb_p4_shifted_common_reserve_lean/` still contains `P4ShiftedCommonReserve.lean` blob `2c1b0fc8f7c47799c6448ddbdaa0be7bb3b2469d`, `verify.sh` blob `98a108b54c5e2e5966c318a0a13f214b622ca042`, `README.md` blob `b65b76b718670dcf40e3680243e23190232f6f43`, and `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`. The prior Lean review cites head `955af52fd2578b3de83457a78170abc68945c74a`, Actions run `34178184302`, and axiom list `[propext, Classical.choice, Quot.sound]`. This pass did not re-execute that job.

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
missing_for_parent_close:
  one common rational a<b with endpoint checks on every actual row
  A0 and charge m extracted from those same rows
  interval membership of the shifted witness, not D>=0 alone
  fresh pinned Lean receipt if the historical candidate is to be reissued
  true-DH / Float64 realized-lambda containment
  P8 domain/trajectory coverage
blobs:
  math_review: 3ee4540ed0bbceb4d6d45a585954bc8bd5ba942c
  lean_review: 890e3e83515b1400e3be3f3303e24f36a34023d4
  sidecar_lean: 2c1b0fc8f7c47799c6448ddbdaa0be7bb3b2469d
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a later Lean owner may re-run the existing sidecar, but that is a new receipt obligation, not implied by this audit;
- an untrusted proposer of `a,b,m` is not a witness until every row endpoint check is bound to the same cell;
- `D_m>=0` on the large-charge branch is not a PASS;
- `D_m=0` is boundary-only and must not be fed to a strict-reserve consumer;
- failure of the endpoint-plus-`A0` envelope does not prove the actual row family infeasible;
- coverage, Float64 enclosure, and comparator admission stay outside this leaf.

## Integration target and requested action

- Target: documentation / inbox provenance only. Leave `T-P4-044` open until a checked common rational interval and a fresh source-bound consumer exist.
- Requested action: harvest this as a pending admission audit. Do not treat the algebraic interface or the historical Actions log as verified, and do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or invent an exit code or axiom list.
- Did not add a Lean sidecar or alter the 2026-09-07 identity statement.
- Did not claim a concrete cell interval, source equality, coverage, or P4/M4 closure.
- Did not overwrite prior reviews or claims.
- Did not edit registry, state, task queue, or formal proofs.
