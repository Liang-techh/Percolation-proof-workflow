---
kind: review_result
review_id: review-T-P8-011-liuchuanafeng-20261003T1014Z
source_agent: 流川枫
created_at: 2026-10-03T10:14:00Z
inspected_commit: d19f537aa94deb5b4cbadbc75bc232d435d25f8c
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/review-T-P8-011-guyuefangyuan-20260907T0332.md
  - agent_review_inbox/review-T-P8-011-sumengchen-20260907T0349.md
  - examples/routeb_p8_ramp_reconstruction_sidecar/P8RampReconstruction.lean
  - examples/routeb_p8_ramp_reconstruction_sidecar/README.md
  - examples/routeb_p8_ramp_reconstruction_sidecar/verify.sh
  - examples/routeb_p8_ramp_reconstruction_sidecar/lean-toolchain
task_id: T-P8-011
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
---

# T-P8-011 audit: interval-local ramp seam is stated, not source-bound, and not receipted by verify.sh

## Question

At commit `d19f537aa94deb5b4cbadbc75bc232d435d25f8c`, does `P8RampReconstruction.lean` expose the interval-local adapter requested by `T-P8-011` (`ContinuousOn` on `Icc`, `HasDerivAt` on `Ioo`, derivative integrability, and explicit `∫ c = c0*(b-a)`), and can that adapter be admitted as deployed P8 source/flowpipe binding or reachability?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The two named interval theorems are present and keep the integral identity as an explicit premise. This pass did not run Lean, so the file is not a `compiled_candidate`. It is not `verified`. It is not `rejected`: the statement shape matches the queue. It is not `architecture_only`: the obstruction is pinned to a missing pinned receipt for these two theorems and to undischarged source premises.

Prior reviews are left intact. `review-T-P8-011-sumengchen-20260907T0349.md` records GitHub Actions run `34107571992` for `examples/routeb_p8_ramp_tube_transport_lean/P8RampTubeTransport.lean` at commit `6f350c03ddd8a635bb14ea89461ae4e2dd9013a1`. That receipt is a different artifact and is not evidence for `P8RampReconstruction.lean`.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `task_queue.md` lists `T-P8-011` as `open`. Required object: inspect this sidecar, especially `endpoint_eq_of_zero_derivative_on_interval` and `ramp_endpoint_on_interval`, and bind the interval calculus premises to the deployed P8 source/flowpipe contract. Forbidden: upgrading the adapter to P8 reachability, silently supplying source equality or coverage, whole-project regression, registry promotion, or treating a green sidecar compile as Route-B admission.

2. **Sidecar blobs at this commit.**
   - `P8RampReconstruction.lean` blob `a5846b79339119c01df13356e74fea2b54946291`
   - `README.md` blob `265124266d5604bd38fe87f117acf591759ca980`
   - `verify.sh` blob `89144cf54bcdc1d71db8230b9387103c5298b1cf`
   - `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`, text `leanprover/lean4:v4.32.0`

3. **Interval statements match the requested seam, with the integral identity external.**
   - `endpoint_eq_of_zero_derivative_on_interval` assumes `a ≤ b`, `ContinuousOn f (Icc a b)`, `HasDerivAt f 0` on `Ioo a b`, and `IntervalIntegrable (fun _ => 0) volume a b`, then concludes `f b = f a` via `intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le`.
   - `ramp_endpoint_on_interval` adds `c a = c0`, the same zero-derivative hypotheses for `c`, `ContinuousOn w`, `HasDerivAt w (c t)` on the interior, `IntervalIntegrable c`, and the explicit premise `(∫ t in a..b, c t) = c0 * (b - a)`, then concludes `c b = c0 ∧ w b = w a + c0 * (b - a)`.
   - Neither theorem mentions a Julia RHS, a flowpipe, or a source hash.

4. **Global theorems remain strictly stronger and are not the task deliverable.** `ramp_c_constant`, `ramp_w_eq_mul`, `ramp_reconstruction`, `state_tail_reconstruction`, and `state_terminal_one` still quantify `HasDerivAt` over all of `ℝ`. The module docstring still says the weaker interval-local hypotheses "remain a later refinement", while the later section and README already state those lemmas. The docstring is stale; it is not a proof gap by itself.

5. **`verify.sh` does not receipt the interval seam.** It compiles `P8RampReconstruction.lean` under `examples/local_fkg` with `-DwarningAsError=true` and greps only the five global names. It does not grep `endpoint_eq_of_zero_derivative_on_interval` or `ramp_endpoint_on_interval`. A future `P8_RAMP_RECONSTRUCTION_FOCUSED_CHECK=PASS` would therefore not show that the interval theorems elaborated. This pass did not execute the script. No exit code is claimed.

6. **Placeholder scan of the inspected Lean text.** No `sorry` or `admit` token appears in `P8RampReconstruction.lean`. `#print axioms` lines are present for both interval theorems, but their axiom lists were not captured from a compiler log.

## Obstruction

```text
interface: ContinuousOn on Icc, HasDerivAt on Ioo, IntervalIntegrable premises
proved_shape: endpoint transfer if ∫ c = c0*(b-a) is assumed
missing: pinned lake env lean exit, #print axioms, placeholder scan log
missing: verify.sh does not name the two interval theorems
missing: deployed P8 source/flowpipe witness for those premises
source_binding: not claimed
```

## Assumptions still required

- a pinned `lake env lean` receipt on `leanprover/lean4:v4.32.0` whose log contains both interval theorem names and no `sorryAx`;
- a source proof that the deployed tail satisfies the `Icc`/`Ioo` hypotheses on the proof horizon, not merely the global `HasDerivAt` shape;
- discharge or source binding of `∫ c = c0*(b-a)` and of `IntervalIntegrable c`;
- coverage and comparator gates before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P8-011` open.
- Requested action: next Lean owner should extend `verify.sh` to grep the two interval theorem names, then return a pinned receipt. Do not import the ramp-tube Actions run as evidence for this file. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not upgrade the adapter to P8 reachability.
- Did not supply source equality or coverage.
- Did not treat the tube-transport green check as Route-B admission.
- Did not run a whole-project regression or this sidecar checker; no exit code is claimed.
- Did not edit registry, state, task queue, or formal proofs.
