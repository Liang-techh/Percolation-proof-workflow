---
kind: review_result
review_id: review-T-P4-034-liuchuanafeng-20261003T1418Z
source_agent: 流川枫
created_at: 2026-10-03T14:18:00Z
claimed_at: 2026-10-03T14:14:00Z
inspected_commit: e1c8a39cbfd8090ed05c521ee15784259e3ba9c1
claim_commit: 27a7f17928079154c911937668a32b29c5c49565
claim_path: agent_review_inbox/claim-T-P4-034-liuchuanafeng-20261003T1414Z.md
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - examples/routeb_p4_o2_signed_rectangle_energy_lean/README.md
  - agent_review_inbox/review-T-P4-034-o2-signed-rectangle-energy-lean-juyangxianzun-20260908T0636.md
  - agent_review_inbox/review-T-P4-O2-BB-triple-julia-obstruction-codex-20260907.md
task_id: T-P4-034
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_o2_split_do_not_close_evaluator
---

# T-P4-034 audit: O2 evaluator enclosure is still open

## Question

At commit `e1c8a39cbfd8090ed05c521ee15784259e3ba9c1`, does any already recorded artifact close the deployed Float64 enclosure of `dhport_lib.jl` `M`, central-FD `C/G`, `tau`, and the linear solve, or does it only supply a source-independent consumer and scalar seams?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The signed-rectangle sidecar is an exact-real consumer that starts after a certified force/residual error box exists. The 2026-09-07 coordinator findings close only scalar bookkeeping. The Julia parent/child/sibling exporter has a runtime obstruction, not an O2 receipt. O2, residual absorption, and flowpipe stay open.

This is not `rejected`: the consumer contract is consistent with the queue boundary. It is not `compiled_candidate`: this pass did not run Lean. It is not `architecture_only`: the missing objects are named executable leaves. It is not `verified`.

Prior reviews by 红莲魔尊, 巨阳仙尊, and Codex are left intact. This pass does not replace them.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P4-034` requires a per-certified-box enclosure of deployed Float64 `M`, central-FD `C/G`, `tau`, and the linear solve, split into libm/trigonometric rounding, finite operation-DAG rounding, FD-shift, regularizer conversion, and solve-conditioning. Forbidden: closing O2 from interval candidates, sampled maxima, solver `OPTIMAL`, or a stale source hash. O2 does not itself prove residual absorption or flowpipe closure.

2. **Coordinator findings do not discharge those leaves.** The queue records four narrower facts, all still short of O2:
   - deployed `1e-5` is the dyadic `5902958103587057/590295810358705651712`, strictly above `1/100000` by `1509/1844674407370955161600000`; endpoint propagation and the `2h` division error remain open;
   - deployed `pi` and `pi/2` sit in `333/106 < pi < 355/113`; this is a scalar offset seam, not a per-angle `sin`/`cos` libm bound;
   - the order-12 rational Taylor leaves for `sin(1/100000)` and `cos(1/100000)` are advisory and do not bind deployed libm or arbitrary DH-angle boxes;
   - the external P3 DH trig-chain is a 12-row exact-real interval contract conditional on the local q-box. It closes phase/center bookkeeping only. Float64 argument formation, libm sin/cos, finite-DAG propagation, and per-box composition remain open.

3. **Sidecar is explicitly post-enclosure.** `examples/routeb_p4_o2_signed_rectangle_energy_lean/README.md` blob `5575bc54cb4d0f6e56ff9e5f1156e770d047fb7c` says the consumer starts after the numerical lane has produced a certified signed enclosure of the final evaluator error in the same force/residual coordinates. It proves SOS identities, four-corner transport, a retained-dissipation charge, and a first-exit reserve. It declares distinct `AccelerationError2` and `ForceResidualError2` wrappers and no coercion between them. It does not prove deployed Float64/libm/central-FD/regularizer/solve semantics, residual export, source/hash/orientation binding, or coverage.

4. **Earlier Lean receipt stays candidate and is not re-run.** `review-T-P4-034-o2-signed-rectangle-energy-lean-juyangxianzun-20260908T0636.md` reports a focused `compiled_candidate` on Lean 4.32.0 for fifteen theorems, axioms `[propext, Classical.choice, Quot.sound]`, and an explicit list of still-open source bindings. That receipt is not a new exit code for this commit, and it does not supply the missing evaluator box.

5. **No fresh Julia enclosure exists in the inspected obstruction.** `review-T-P4-O2-BB-triple-julia-obstruction-codex-20260907.md` records `JULIA_FOUND=False` and no parse, include, stdout, or exit code for the opt-in O2 triple exporter. `PENDING` was not upgraded to `READY`. This pass also did not run Julia.

## Obstruction

```text
O2 needs: per-box Float64 enclosure of M, central-FD C/G, tau, and the solve
still open: libm sin/cos, argument formation, finite DAG rounding,
            FD-shift / 2h division, regularizer conversion, solve conditioning
not a substitute: dyadic 1e-5 gap, pi enclosure, Taylor(sin/cos of 1/100000),
                  12-row phase/center contract, signed-rectangle consumer
coordinate gap: AccelerationError2 is not ForceResidualError2
runtime: Julia triple exporter has no receipt on the inspected obstruction
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-034` open.
- Requested action: harvest this as a corroborating pending split. Do not treat the signed-rectangle sidecar or the scalar seams as O2 closure. Next executable owner needs one certified box with source hash, operation order, rounding mode, and the unresolved primitive lemmas still named. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not declare O2 closed from interval candidates, samples, solver status, or a stale hash.
- Did not claim residual absorption or flowpipe closure.
- Did not run Lean or Julia; no new exit code is claimed.
- Did not edit registry, state, task queue, or formal proofs.
