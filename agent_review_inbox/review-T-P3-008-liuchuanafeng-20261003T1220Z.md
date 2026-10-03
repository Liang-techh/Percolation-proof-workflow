---
kind: review_result
review_id: review-T-P3-008-liuchuanafeng-20261003T1220Z
source_agent: 流川枫
created_at: 2026-10-03T12:20:00Z
claimed_at: 2026-10-03T12:18:00Z
inspected_commit: 911f72dadadf313d69b0c52ad214ddc5ccf69255
claim_commit: 7db56c69f0e02eb40ba691c95e50c7ab30aa7b5d
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - examples/routeb_source_binding_audit/snapshots/current_exact/ChristoffelPower.lean
  - agent_review_inbox/review-T-P3-008-guyuefangyuan-20260907T0141.md
task_id: T-P3-008
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_index_adapter_do_not_close_p3
---

# T-P3-008 audit: exact-real index adapter holds; source binding does not

## Question

At commit `911f72dadadf313d69b0c52ad214ddc5ccf69255`, does the deployed `arm_MCG` central-difference contraction equal the generic Christoffel force in `ChristoffelPower.lean`, and can that equality be used as true-DH source binding?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The snapshot formula matches `christoffelForce` after one explicit index permutation, but only as exact-real arithmetic on a real-lifted tensor. The Lean file does not state that adapter, does not mention `Cdq`, and does not discharge analytic-derivative or Float64 premises. P3, P5, and M4 stay open.

This is not `rejected`: the source text is compatible with the adapter. It is not `architecture_only`: the obstruction is a concrete missing theorem, not a missing diagram. It is not `compiled_candidate`: no Lean process was run, and the existing `#print axioms` lines were not executed.

Prior review `review-T-P3-008-guyuefangyuan-20260907T0141.md` is left intact. This pass does not replace it.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P3-008` asks for a typed equality between source `Cdq` and the generic Christoffel expression, with FD remainder and true-DH derivative semantics kept as premises, or a precise indexing obstruction. Forbidden: treating the generic identity as source binding, silently replacing central differences by analytic derivatives, or closing P3/P5/M4.

2. **Deployed contraction, blob `27cf497b6f27919eb5b554369fb1444f4314c942`.** In `arm_MCG`:

```text
dM[:, :, kk] = (mass_matrix(q + h e_kk) - mass_matrix(q - h e_kk)) / (2h)
cijk = 0.5 * (dM[ii, jj, kk] + dM[ii, kk, jj] - dM[jj, kk, ii])
Cdq[ii] = sum_{jj,kk} cijk * dq[jj] * dq[kk]
```

   Julia is 1-based. Mapping `ii,jj,kk` to 0-based `i,j,k` gives

```text
Tfd k i j := dM[i, j, k]
Cdq[i] = sum_{j,k} ((Tfd k i j + Tfd j i k - Tfd i j k) / 2) * v j * v k
```

   The opposite convention `T i j k := dM[i, j, k]` would put the difference direction in the wrong slot and is not the source formula.

3. **Generic Lean identity, blob `e8e544007588e06fbac12638c7f71976fc094db9`.** `christoffelForce` is exactly that double sum for an arbitrary real tensor `T`, with index order `T k i j`. `christoffel_power_identity` and `christoffel_power_identity_fin6` are finite-sum rearrangements. The file says the result is for an arbitrary real tensor and specializes to `Fin 6` without enumeration. It contains no `Cdq`, no `dM`, no step `h`, and no DH premise.

4. **Smallest exact-real adapter, not yet a theorem of this file.**

```text
sourceCdq(Tfd, v) = christoffelForce Tfd v
```

   holds by matching the three tensor slots, with no symmetry of `Tfd` required. It is conditional on lifting the two mass evaluations and the subsequent sums to exact reals. Nested `jj` then `kk` does not matter over exact reals; it does matter for sequential Float64 accumulation.

5. **Analytic derivative is a separate remainder.** Define `T k i j := partial_k M_ij` and `R := Tfd - T`. Linearity of `christoffelForce` in its tensor argument gives

```text
christoffelForce Tfd v = christoffelForce T v + christoffelForce R v
```

   Replacing `Tfd` by `T` is exactly the substitution the task forbids. The power form

```text
sum_i v i * christoffelForce R v i = (1/2) * sum_{k,i,j} R k i j * v k * v i * v j
```

   follows from `christoffel_power_identity` applied to `R`, again only after `R` is an exact real tensor. No Fourier coefficient bound was recomputed in this pass.

6. **Constant regularizer cancels only in exact-real central differences.** `mass_matrix` returns `M + regularization * I` with `MASS_REGULARIZER = 1e-6`. A constant multiple of `I` has exact-real central difference zero, so it does not change `Tfd` if both perturbed evaluations use the same regularization and no rounding. The source still evaluates two separately rounded Float64 matrices, so this cancellation is not a deployed bit identity.

7. **Execution gap.** Even after lifting each stored `dM` entry, the Julia loop accumulates 36 rounded `cijk * dq[jj] * dq[kk]` terms. That real lift is not definitionally `christoffelForce`. The honest adapter remains

```text
lift(Cdq_Julia) = christoffelForce(Tfd_lift, v_lift) + r_ieee
```

   with `r_ieee` unproved here. `h = Float64(1e-5)` is also not identified with the rational `1/100000`.

## Obstruction

```text
adapter: Tfd k i j = dM[i, j, k]
exact-real: Cdq = christoffelForce Tfd, no symmetry used
not in Lean: no sourceCdq theorem, no dM premise
not discharged: Tfd = partial M + R, Float64 r_ieee, h = 1/100000
regularizer: exact-real central difference of eps*I is zero; Float64 cancellation open
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-008` open.
- Requested action: harvest this as a corroborating pending index adapter. A later formalization lane may add the source-index definition and the linearity split; that still would not be source binding. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat `christoffel_power_identity` as source binding.
- Did not replace central differences by analytic derivatives.
- Did not close P3, P5, or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
