---
kind: review_result
review_id: review-T-P4-037-SIGN-ROBUST-TRANSPORT-liuchuanafeng-20261006T0614Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-06T06:14:00Z
inspected_commit: b9825fc2e2672ace646411ff98000a445562c002
claim_commit: b9825fc2e2672ace646411ff98000a445562c002
prior_head: 020950103717db7b1f8dbebcdf7df9cc8834bede
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/claim-T-P4-037-liuguanyi-20260907T1510.md
  - agent_review_inbox/review-T-P4-037-liuguanyi-20260907T1520.md
  - agent_review_inbox/companion-T-P4-037-liuguanyi-20260907T1523.md
task_id: T-P4-037
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P4-037 admission audit: sign-difference and Young envelope hold, certificate surface still open

## Question

At commit `b9825fc2e2672ace646411ff98000a445562c002`, does the existing `T-P4-037` math review already supply a concrete combined cross block, a same-key `R_port`/`R_gain` witness, a Lean receipt, coverage, or any source/registry admission for a P4 cell?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The sign-difference identity, the one-dimensional counterexample that blocks boolean reuse, and the rational Young envelope are algebraically consistent as a source-independent interface. They do not close a concrete combined block, source equality, Float64 realization, coverage, or registry.

This pass did not compile anything. It does not invent a Lean sidecar and does not reclassify 柳冠一's review as `verified` or `compiled_candidate`.

This is not `verified`: no kernel run and no source packet in this pass. It is not `rejected`: the scalar checks below match the stated identities. It is not `architecture_only`: the math review states exact scalar/matrix theorems and a concrete counterexample. It is not a new `compiled_candidate`: this agent did not run Lean or a checker.

Prior authorship is preserved. This file does not overwrite 柳冠一.

## Evidence inspected (read-only)

1. **Queue does not close this leaf.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` does not record a closeout for `T-P4-037`. Inbox contains only the 2026-09-07 claim, review, and companion by 柳冠一. No `T-P4-037` Lean sidecar or source packet was found in the inspected paths.

2. **Math review is source-independent and self-labeled pending.** `review-T-P4-037-liuguanyi-20260907T1520.md` blob `b20647c59b15674f0d39ccf4dd4ade3c7d9a8cf9`, inspected commit `ce3e6e614de2ea6f5276b9bb4803fba6c411e51a`, `admission_label: pending`. It states `Q_minus - Q_plus = -2 X`, the transport `M_minus = M_plus + 2 X`, and an explicit denial of source, interval, solver, Lean, coverage, and admission.

3. **Independent check of the blocking counterexample.** With `H=1`, `C0=1`, `Cp=-1`, `D=0`, the historical plus block gives `Q_plus=0` and `D-Q_plus=0`, while the physical minus block gives `Q_minus=4` and `D-Q_minus=-4`. The sign difference is `4`, matching `-2 X` with `X=2 C0 Cp=-2`. A final plus-sign PSD status is therefore not a typed source for the corrected sign.

4. **Independent check of the rational Young envelope.** For `theta=2`, `s=+1`, `C0=3`, `Cp=s theta C0=6`, `H=1`, both sides of `Q_s = (1+theta) A0 + (1+1/theta) Ap` equal `81`, so the stated sharpness case is attained. The division-free form `theta Q_s = theta(1+theta) A0 + (1+theta) Ap` equals `162` on both sides. This is exact rational arithmetic only; it is not a Lean receipt and does not bind a P4 matrix.

```text
command: not run
exit_code: not claimed
lean_toolchain: not pinned by this agent
axiom_print: not executed
placeholder_scan: not run by this agent
source_binding: not present
concrete_combined_cross_block: not exhibited
```

## Obstruction

```text
identity_surface: source-independent, algebraically consistent on the published scalar checks
missing_for_parent_close:
  a concrete combined cross block in a current P4/S-lemma artifact
  same-key decision of whether Cp is historical R_gain or already physical R_port
  retained witness class A (M_plus and X), B (A0 and Ap), or C (boolean only)
  interference enclosure Delta on the same cell, if lane A/repair is used
  fresh pinned Lean receipt for the recommended evaluation-level leaves
  true-DH / Float64 realization and P8 coverage
blobs:
  math_review: b20647c59b15674f0d39ccf4dd4ade3c7d9a8cf9
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a second sign flip must not be applied after a typed adapter has already switched to `R_port`;
- `X>=0` free reuse and the `2 Delta` additive repair are not available from a boolean PSD status alone;
- equality in the Young envelope for one scalar theta does not license shrinking both coefficients from `A0,Ap` alone;
- cellwise `Delta` or `theta` may be consumed only on the same certified cell;
- coverage, Float64 enclosure, and comparator admission stay outside this leaf.

## Integration target and requested action

- Target: documentation / inbox provenance only. Leave `T-P4-037` open until a checked combined-block witness and a fresh source-bound consumer exist.
- Requested action: harvest this as a pending admission audit. Do not treat the algebraic interface as verified, and do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or invent an exit code or axiom list.
- Did not add a Lean sidecar or alter the 2026-09-07 identity statement.
- Did not claim a concrete cross block, source equality, coverage, or P4/M4 closure.
- Did not overwrite prior reviews or claims.
- Did not edit registry, state, task queue, or formal proofs.
