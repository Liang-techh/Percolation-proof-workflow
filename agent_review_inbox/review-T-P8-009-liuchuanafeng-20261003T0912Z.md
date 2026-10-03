---
kind: review_result
review_id: review-T-P8-009-liuchuanafeng-20261003T0912Z
source_agent: 流川枫
created_at: 2026-10-03T09:12:00Z
claimed_at: 2026-10-03T09:10:00Z
inspected_commit: fcfcc680be7b1b50e66db1d19aab2c8f4b8f1e72
claim_commit: 213dc68e7921037f51fc95b7ccfd6d36aa057ad5
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_p8_interval_ramp_lean/P8IntervalRamp.lean
  - examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean
  - docs/routeb-p8-flowpipe-binding-next.md
  - agent_review_inbox/review-T-P8-009-sumengchen-20260907T0118.md
task_id: T-P8-009
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_do_not_close_p8
---

# T-P8-009 audit: interval-local ramp is a calculus child, not a source transfer

## Question

At commit `fcfcc680be7b1b50e66db1d19aab2c8f4b8f1e72`, does the interval-local ramp sidecar weaken the all-`ℝ` derivative hypotheses enough for a `[0,1]` terminal transfer, and can that child be consumed by the deployed P8 contract?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The separate sidecar states a strictly weaker calculus hypothesis than the original all-`ℝ` theorems, and its terminal conclusion `z 1 wSlot = c0` does not use a derivative at `t=1`. That statement is still conditional on continuity and right derivatives that no source theorem supplies. The documented 13-state RHS writes `du[13]=0` and has no `c` state, so it does not instantiate `w'=c` except on the degenerate `c=0` subfamily. P8 and M4 stay open.

This is not `rejected`: the Lean text is a coherent conditional child. It is not `compiled_candidate` in this review: no Lean process was run, and the 2026-09-07 focused log is not re-verified. It is not `architecture_only`: the obstruction is pinned to a concrete source mismatch.

Prior review `review-T-P8-009-sumengchen-20260907T0118.md` is left intact. This pass does not replace it and does not edit the sidecar.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P8-009` asks for an interval-local/end-point theorem sufficient for `[0,1]` terminal transfer, with `w'=c`, `c'=0`, and typed tail slots. Forbidden: altering the compiled candidate, treating interval calculus as ODE existence, source binding, flowpipe coverage, first-exit closure, or registry promotion.

2. **Original sidecar still has the strong hypothesis.** `P8RampReconstruction.lean` blob `a5846b79339119c01df13356e74fea2b54946291` proves `ramp_c_constant`, `ramp_w_eq_mul`, `state_tail_reconstruction`, and `state_terminal_one` from `HasDerivAt` at every real time. Its later `ramp_endpoint_on_interval` is interval-local, but it takes `(∫ t in a..b, c t) = c0 * (b - a)` as an explicit premise. That premise is not discharged by the file. The module comment says the interval hypotheses remain a later refinement. This audit did not modify that file.

3. **Separate child matches the requested weakening, as source text only.** `P8IntervalRamp.lean` blob `0904bd9510ccc672436459caa40d827c879bba07` states

```text
ContinuousOn c (Icc 0 1)
∀ t ∈ Ico 0 1, HasDerivWithinAt c 0 (Ici t) t
⇒ ∀ t ∈ Icc 0 1, c t = c0
```

and the corresponding `w` theorem from right derivatives of `w` on `Ico 0 1`, then `state_terminal_one_interval : z 1 wSlot = c0`. Slots remain `wSlot = 12`, `cSlot = 13` on `Fin 14`. The file header disclaims source binding, ODE existence, flowpipe coverage, first-exit closure, and admission. No `#print axioms` output is attached to this commit by this review.

4. **Deployed contract does not supply those hypotheses.** `docs/routeb-p8-flowpipe-binding-next.md` blob `c3d9dbf3aa7d1e9fdf4f0583f83c47fcdde83ae0` records the parent ramp premise `F z wSlot = z cSlot` and `F z cSlot = 0`, and the probe fact `full_rhs!` is 13-state with `du[13]=0` and no `c=u[14]`. The natural lift with `F14[12]=0` fails `RampRhsPremise` at `c=1`. Only `c=0` avoids that contradiction. Therefore `w'=c` on `[0,1)` is not a theorem of the recorded source, and the interval child cannot be specialized to it.

5. **Terminal identity is not coverage.** Even if a future source proved the right-derivative premises, `z 1 wSlot = c0` is one scalar endpoint. It does not enclose the first 12 coordinates, does not create a flowpipe tube, and does not discharge `RhsReceipt.fullRhsBinding`, which the same document still marks open.

## Obstruction

```text
calculus child: Icc continuity + Ico right derivatives ⇒ w(1)=c0
not discharged: existence of such a trajectory, source equality w'=c
source fact: full_rhs! writes du[13]=0 and has no c state
countermodel shape: F14 lift with c=1 gives F14 wSlot = 0 ≠ 1
parent interval lemma: integral identity remains a premise, not a proof
source_binding: false
flowpipe_coverage: false
```

## Integration target and requested action

- Target: documentation only. Leave `T-P8-009` open.
- Requested action: harvest this as a corroborating pending boundary. Do not promote the 2026-09-07 focused PASS into registry. Next source owner must choose a real 14-state ramp RHS or an explicit-time 13-state parent before this calculus child can be instantiated. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not alter the already compiled candidate or the interval sidecar.
- Did not treat interval calculus as ODE existence or flowpipe coverage.
- Did not claim source binding or first-exit closure.
- Did not close P8 or M4, and did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no new exit code is claimed.
