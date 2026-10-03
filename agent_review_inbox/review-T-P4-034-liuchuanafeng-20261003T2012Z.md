---
kind: review_result
review_id: review-T-P4-034-liuchuanafeng-20261003T2012Z
source_agent: 流川枫
created_at: 2026-10-03T20:12:00Z
claimed_at: 2026-10-03T20:10:00Z
inspected_commit: c28d6de60c30b0faaffb7df662a87d506caa24e3
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P4-034-liuchuanafeng-20261003T1414Z.md
  - agent_review_inbox/review-T-P4-034-honglianmozun-20260908T0558.md
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/SHA256SUMS.csv
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_export_traj.jl
task_id: T-P4-034
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_obstruction_do_not_close_o2
---

# T-P4-034 audit: O2 evaluator enclosure is not closed

## Question

At commit `c28d6de60c30b0faaffb7df662a87d506caa24e3`, do the signed-rectangle energy sidecar, the 2026-09-07 coordinator scalar seams, and the frozen Julia source/export/analytic probe close any of the O2 leaves (libm/trigonometric rounding, finite operation-DAG rounding, FD-shift, regularizer conversion, solve-conditioning) for deployed `dhport_lib.jl`?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** None of those artifacts is a per-certified-box outward enclosure of deployed Float64 `M`, central-FD `C/G`, `tau`, or the linear solve. O2 remains open. This review does not close residual absorption or flowpipe coverage.

This is not `rejected`: the decomposition requested by the queue is still the right obligation. It is not `verified` or `compiled_candidate`: no Lean, MPFR, or directed-rounding process was run. It is not `architecture_only`: the blocker is missing enclosure evidence on the frozen evaluator, not a missing interface name.

Prior files are left intact: `claim-T-P4-034-liuchuanafeng-20261003T1414Z.md` and `review-T-P4-034-honglianmozun-20260908T0558.md`.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P4-034` requires every certified box to be covered, with source hash, operation order, rounding mode, and unresolved primitive lemmas. Forbidden: closing O2 from interval candidates, sampled maxima, solver `OPTIMAL`, or a stale source hash. O2 does not itself prove residual absorption or flowpipe closure.

2. **Frozen evaluator is nearest Float64, blob `27cf497b6f27919eb5b554369fb1444f4314c942`, sha256 `aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936`.** `dhport_lib.jl` sets `MASS_REGULARIZER = 1e-6`, `CG_FINITE_DIFF_STEP = 1e-5`, and `DYNAMICS_SEMANTICS` to DH-chain `M` plus central finite differences. `fk_frames` uses Julia `cos`/`sin` on `Float64` arguments that include `DH` twist literals `-pi/2` and `pi/2`. `mass_matrix` adds `Float64(regularization)*I`. `arm_MCG` forms `dM` and `Gq` by `(f(q+h e_k)-f(q-h e_k))/(2h)`. `exact_ddq` forms `tau = -Kp.*q - (Kd+b_fr).*dq + G0v + (gw_coef.*I_val).*w` and returns `Mq \ (tau - Cdq - Gq)`. There is no rounding-mode flag, no per-box certificate, and no libm error bound.

3. **Coordinator scalar seams remain seams.** Recomputed from binary64 literals, without treating them as enclosure receipts:
   - `Float64(1e-5)` is the dyadic `5902958103587057/590295810358705651712`, which exceeds exact `1/100000` by `1509/1844674407370955161600000`. Endpoint propagation and the `2h` division error are not enclosed.
   - `Float64(1e-6)` is `4722366482869645/4722366482869645213696`, not exact `1/1000000`. Adding it on the diagonal is not a proved conversion from the exact regularizer.
   - `Float64(pi)` is `884279719003555/281474976710656`, and `333/106 < pi < 355/113` still holds, but that is only a scalar offset. Per-angle `sin`/`cos` libm error is absent.

4. **Energy sidecar does not supply the rectangle.** `review-T-P4-034-honglianmozun-20260908T0558.md` is an exact-real consumer: four corners of a signed residual rectangle bound `N_H`, and a nonzero absolute bias blocks homogeneous decay. It states that it does not bind `dhport_lib.jl`, the `1e-5` shift, or solve conditioning, and that acceleration error is not force error without a same-box mass bridge. No numerical `L4,U4,L5,U5` is exported in that review.

5. **The frozen triple is not an enclosure export.** `SHA256SUMS.csv` lists the source snapshot, the analytic Fourier probe, and mass/potential CSVs. `REPORT.md` (blob `8bc5cd5444473396caa13af107428f0350cca742`) classifies DH formulas as source text only and leaves full `M(q)` reconstruction, FD gradient binding, and the PMI-versus-`tau` mismatch open. `routeB_export_traj.jl` (blob `2bfdf5a31e942475a08dfe56cc273fe99c047d9e`) writes `evidence_level = empirical`, `coverage_kind = trajectory_monte_carlo_only`, and `global_box_coverage = false`. Sampled trajectories and `solver` backslash success are not box coverage.

## Obstruction

```text
source_blob: dhport_lib.jl 27cf497b6f27919eb5b554369fb1444f4314c942
source_sha256: aebe6db09b2d943448c5d701631109dba8f5eeb070cc66593e5dbaca26485936
libm_trig: Float64 sin/cos, no per-angle error leaf
fd_step: Float64(1e-5) = 5902958103587057/590295810358705651712
fd_gap_vs_1e-5: 1509/1844674407370955161600000
regularizer: Float64(1e-6) = 4722366482869645/4722366482869645213696
solve: backslash, no conditioning enclosure
energy_sidecar: source-independent; no residual rectangle
export: global_box_coverage = false
source_binding: false
```

Open leaves, unchanged: per-box libm `sin`/`cos` error, finite-DAG outward rounding of `M`/`C`/`G`/`tau`, FD-shift including the `2h` division, regularizer conversion, and solve-conditioning, each with operation order and rounding mode. A later owner must pin one certified box and one primitive, not a sampled maximum.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-034` open.
- Requested action: harvest this as a pending obstruction. Do not treat the energy consumer, the scalar `pi`/`h` notes, or the Monte Carlo exporter as O2 closure. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not declare O2 closed from interval candidates, sampled maxima, solver status, or a stale hash. The inspected hash is the current snapshot blob.
- Did not claim residual absorption or flowpipe closure.
- Did not run a whole-project regression or a checker; no exit code is claimed.
- Did not edit registry, state, task queue, or formal proofs.
