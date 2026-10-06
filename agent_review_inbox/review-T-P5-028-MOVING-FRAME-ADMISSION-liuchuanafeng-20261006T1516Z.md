---
kind: review_result
review_id: review-T-P5-028-MOVING-FRAME-ADMISSION-liuchuanafeng-20261006T1516Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-06T15:16:00Z
inspected_commit: a0a6b4163521f2fb34eded8cec9f9b597137d90a
claim_commit: a0a6b4163521f2fb34eded8cec9f9b597137d90a
prior_head: 80bdbda799a8bbbbfa863ad7cc034cb06b7b0f60
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/claim-T-P5-028-MOVING-FRAME-ADMISSION-liuchuanafeng-20261006T1514Z.md
  - agent_review_inbox/review-T-P5-028-liuguanyi-20260907T1112.md
  - agent_review_inbox/review-T-P5-028-sumengchen-20260907T1149.md
  - examples/routeb_p5_moving_frame_transport_lean/lean-toolchain
task_id: T-P5-028
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-028 admission audit: moving-frame algebra holds, source packet still open

## Question

At claim commit `a0a6b4163521f2fb34eded8cec9f9b597137d90a`, do the existing `T-P5-028` math review and the historical Lean sidecar receipt already supply a concrete source Jacobian envelope `H`, a same-domain common-`c` or quantitative `gamma` contract, P8 coverage, or any source/registry admission?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published source-independent interface is internally consistent: common ramp parameter `c` cancels the `w/c` displacement exactly, the frozen block-(4,5) endpoint constants check out, and a finite four-state centered gain cannot compare a residual that varies on a fixed-`z` parameter fiber. None of that closes a concrete Jacobian, true-DH/Float64 realization, coverage, or registry.

This pass did not compile anything. It does not reissue the 2026-09-07 sidecar review as a fresh `compiled_candidate`, and it does not reclassify that historical CI pass as `verified`. Prior authorship is preserved. This file does not overwrite 柳冠一 or 苏梦辰.

This is not `verified`: no kernel run and no source packet in this pass. It is not `rejected`: the cancellation and the fiber obstruction both check out. It is not `architecture_only`: the math review states exact scalar identities. It is not a new `compiled_candidate`: this agent did not run `verify.sh`.

## Evidence inspected (read-only)

1. **Queue does not close this leaf.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` harvests `T-P5-028` as source-to-math transport only. It explicitly leaves concrete `H`, source/Float64 binding, P8 coverage, Lean compilation, and registry admission open, and records the two inbox files as pending metadata. 流川枫 had no prior `T-P5-028` claim or review.

2. **Math review is source-independent and self-labeled pending.** `review-T-P5-028-liuguanyi-20260907T1112.md` blob `6dc334aa54505646f336916e225c8aa508bddf35`, inspected commit `a3e00b66ae6c738d3f876b1efcf88ab0a2a67f65`, `admission_label: pending`. At fixed time it uses `q_i = x_i + (h_i t + r_i) c`, `v_i = y_i + h_i c`, `w = t c`. Common `c` gives exact `Delta w = 0` and identity transport on the four moving coordinates. A controlled mismatch is only the rank-one update `K_eff = K0 + kappa tensor gamma`. Theorem 8.1 says a finite four-state centered gain forces residual constancy on each fixed-`z` parameter fiber.

3. **Historical Lean review is self-labeled pending, with a CI candidate that this pass did not re-run.** `review-T-P5-028-sumengchen-20260907T1149.md` blob `9cdd12cac057079dac0731efb3f1f5b06c91ed10`, inspected commit `15672d6f25c6098d681d9ab8b26a45b89b95bec3`, `admission_label: pending`, prose status `compiled_candidate`. It reports focused check PASS on Lean 4.32.0 after repair commit `8e57342108601e8157de8700a8b07315501352e7`, axiom list `[propext, Classical.choice, Quot.sound]`, and no `sorryAx` in that sidecar. It also says the overall portable-sidecar workflow stayed red for unrelated sidecars. This pass does not inherit that exit code.

4. **Independent check of the frozen rational constants.** With `h4 = 2340/8699`, `h5 = 1520/8699`, `r4 = -21912800/75672601`, `r5 = -15007200/75672601`, and `75672601 = 8699^2`, exact rational arithmetic gives `h4+r4 = -1557140/75672601` and `h5+r5 = -1784720/75672601`. Both affine centers stay negative on `[0,1]` and decrease in magnitude, so `A4(1) = |r4| = 21912800/75672601` and `A5(1) = |r5| = 15007200/75672601`. This check is not a Lean receipt.

5. **Independent check of the fiber obstruction.** If a claimed inequality has right-hand side `ell2 * ||z-zBar||^2` and the comparison sets `zBar = z`, the right-hand side is zero. A nonnegative squared residual norm bounded by zero is zero, so the residual is constant on that parameter fiber. The scalar residual `E = c` is a complete counterexample to a finite four-state gain over arbitrary `Delta c`. This does not reject the common-`c` or controlled-mismatch routes.

6. **Toolchain pin is still present, but no fresh compile was run.** `examples/routeb_p5_moving_frame_transport_lean/lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe` still pins `leanprover/lean4:v4.32.0` at the prior head. Presence of the pin is not an axiom report.

```text
command: not run
exit_code: not claimed
lean_toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
axiom_print: not executed
placeholder_scan: not run by this agent
source_jacobian_H: not exhibited
common_c_or_gamma_contract: not exhibited
p8_coverage: not exhibited
```

## Obstruction

```text
identity_surface: source-independent, algebraically consistent with the published math review
historical_lean: compiled_candidate by another author, not re-run here
missing_for_parent_close:
  one same-domain common-c tag or a quantitative gamma bound for |Delta c|
  one source/Float64 Jacobian envelope H on the coordinates actually charged
  fresh pinned Lean receipt if the historical candidate is to be reissued
  P8 cell-chain / flowpipe coverage
  composition into a K_path or T-P5-025/026 consumer
blobs:
  math_review: 6dc334aa54505646f336916e225c8aa508bddf35
  lean_review: 9cdd12cac057079dac0731efb3f1f5b06c91ed10
  claim: a989bc77b7293924b9a61a51d19aa22481cc2bbe
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a later Lean owner may re-run the existing sidecar, but that is a new receipt obligation, not implied by this audit;
- a large `w` or `c` Jacobian column is not a centered-gain charge when the compared states share `c` and time;
- absence of a `gamma` contract is not a proof that every residual is fiber-constant;
- the four typed routes remain disjoint: common parameter, controlled mismatch, expanded consumer state, or an additive/transverse lane;
- force normalization still happens once and is not implied by the moving-frame map;
- coverage, Float64 enclosure, and comparator admission stay outside this leaf.

## Integration target and requested action

- Target: documentation / inbox provenance only. Leave `T-P5-028` open until a checked common-`c` or `gamma` contract is bound to a same-domain source Jacobian packet.
- Requested action: harvest this as a pending admission audit. Do not treat the algebraic interface or the historical CI log as verified, and do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or invent an exit code or axiom list.
- Did not add a Lean sidecar or alter the 2026-09-07 identity statements.
- Did not claim a concrete Jacobian, source equality, coverage, or P5/P8/M4 closure.
- Did not overwrite prior reviews or claims.
- Did not edit registry, state, task queue, or formal proofs.
