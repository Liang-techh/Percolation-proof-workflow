---
kind: review_result
review_id: review-T-P5-008-liuchuanafeng-20261003T0718Z
source_agent: 流川枫
created_at: 2026-10-03T07:18:00Z
claimed_at: 2026-10-03T07:15:00Z
inspected_commit: 660592eec782755fc8e5a75934b935440a3f105e
claim_commit: 169a6d31b3a08df6f3c221eda52a6b2d6a665601
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_dh_power_binding/DHPowerBinding.lean
  - examples/routeb_dh_power_binding/FDForceBudget.lean
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - agent_review_inbox/review-T-P5-008-honglianmozun-20260906T2348.md
task_id: T-P5-008
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_split_do_not_close_p5
---

# T-P5-008 audit: deployed split is conditional; offsets are not equilibrium bias

## Question

At commit `660592eec782755fc8e5a75934b935440a3f105e`, which parts of the deployed force error are state-relative, which are exact storage corrections, and which can still be additive bias at the designated equilibrium, once `MASS_REGULARIZER=1e-6`, `CG_FINITE_DIFF_STEP=1e-5`, and `tau - Cdq - Gq` are accounted for?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The five-term `forceError` ledger is source-independent algebra. Two storage cancellations are valid only under extra premises that this snapshot does not discharge. The positive channel offsets in `FDForceBudget.offset` are enclosure slack, not a proof of nonzero equilibrium bias, and they are not a `rho|v|` bound. P5 and M4 stay open.

This is not `rejected`: the deployed text is compatible with the charged split. It is not `architecture_only`: the obstruction is pinned to open B45 bindings and to the unproved controller/solve equilibrium contract. It is not `compiled_candidate`: no Lean process was run.

Prior review `review-T-P5-008-honglianmozun-20260906T2348.md` is left intact. This pass does not replace it.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P5-008` asks for an exact energy-ledger split or a rigorous obstruction, with units and domain assumptions, and specifically names `MASS_REGULARIZER=1e-6`, `CG_FINITE_DIFF_STEP=1e-5`, and the `tau-Cdq-Gq` construction. Forbidden: turning positive-offset envelopes into `rho|v|`, using samples as global estimates, or closing P5/M4.

2. **Abstract ledger, not source binding.** `DHPowerBinding.lean` blob `5e440147a2428262d1beea31ccb56c27d2818b07` defines

```text
forceError = (Ma-Mi)a + (tauI-tauA) + (cA-cI) + (gA-gI) + solveResidual
solveResidual = Mi a - (tauI - cI - gI)
```

   `implemented_force_identity` and `implemented_energy_identity` are ring rearrangements. The file states that analytic and numeric quantities are real inputs and that concrete source binding is separate. `implemented_energy_bound_of_component_enclosures` consumes a componentwise absolute enclosure; it does not classify bias versus relative error.

3. **Deployed knobs match the task text, as source text only.** `dhport_lib.jl` blob `27cf497b6f27919eb5b554369fb1444f4314c942` sets `MASS_REGULARIZER = 1e-6` and `CG_FINITE_DIFF_STEP = 1e-5`. `mass_matrix` returns the DH assembly plus `regularization * I`. `arm_MCG` builds `Cdq` by the Christoffel contraction of central differences of that mass, and `Gq` by central differences of `potential`, both with step `h`. `exact_ddq` sets

```text
tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w
a   = Mq \ (tau - Cdq - Gq)
```

   with `G0v` from `arm_MCG` at the zero state. `gw_coef .* I_val` simplifies in source text to `[1.0, 0.5, 0.3, 0.2, 0.1, 0.05]`, not to a proved match with `RouteBSupplyCore.disturbance`.

4. **Mass regularizer is a storage candidate, not a proved cancellation.** If a source theorem gives `Mi = Ma + eps I` with `eps = 1e-6`, then `(Ma-Mi)a = -eps a`. Along a trajectory with `v' = a`, the power `-eps <v,a>` cancels the derivative of `eps/2 ||v||^2`. Constant `eps I` also drops out of every central difference of `M`, so it does not create a new `C` term. Neither `Mi = Ma + eps I` nor `v' = a` is a theorem of `DHPowerBinding.lean`. `REPORT.md` blob `8bc5cd5444473396caa13af107428f0350cca742` still lists B45-1 open. A force-level bound of `eps|a|` by `|v|` is not claimed and is not available from this interface.

5. **Gravity FD scaling is not a deployed fact.** The frozen 17-row cosine object can support `G_FD = (sin h / h) G_exact` only after every frequency coordinate is in `{-1,0,1}` and `h` is the step actually used. `REPORT.md` item B45-2 leaves `U_DH = EvalFourier(...)` open, and `PotentialSlice` disclaims physical identification. Deployed `potential` is `sum_i m_i * 9.81 * pcom_z`, not that frozen object. The model step `1/100000` is also not identified with the Float64 literal `1e-5`. So the storage shift `U -> sigma U` stays conditional. It must not be harvested as true-DH cancellation.

6. **`C` mismatch is cubic only after the Christoffel binding.** If `cA` and `cI` are the same Christoffel contraction of two tensors, the generic power identity gives

```text
<v, C(T)v - C(T^h)v> = 1/2 sum_{i,j,k} (T-T^h)_kij v_i v_j v_k.
```

   That power is zero at `v = 0` and is a relative/cubic candidate, not an additive bias. `REPORT.md` item B45-4 still does not bind source `Cdq` to that tensor. The frozen mass CSV having frequencies of size 2 blocks a single gravity-style `sigma` for mass derivatives; that observation remains advisory.

7. **Zero-state construction cancels gravity feedforward in exact arithmetic, not in Float64.** At `q = 0`, `dq = 0`, `w = 0`, source text gives `Cdq = 0` and `tau = G0v`, while `Gq` is the same `arm_MCG` gravity call, so `tau - Cdq - Gq = 0` before the solve. An exact real backslash then returns `a = 0`, and `solveResidual` is zero. This is a construction identity, not a checked Float64 theorem: `1e-5`, `cos`/`sin`, and `\` are not enclosed here. It also does not show that `G_FD(0) = 0`; it shows that the controller adds back the same `G0v` it subtracts.

8. **Envelope offsets are not bias and not `rho|v|`.** `FDForceBudget.lean` blob `4e3a3ae56b5ec2708d0deeec2de786d0a0218e36` has nonzero `offset` on channels 2--5 and zero offset on channels 1 and 6. `fd_only_supply_bound` is conditional on `|e i| <= slope i * cap + offset i`. The file says the Fourier/DH derivation, storage lower bound, and cap invariant are not axiomatized. Those positive offsets must not be read as equilibrium force bias and must not be rewritten as `rho|v|`.

## Classification

| term | classification at this commit | equilibrium from source text |
|---|---|---|
| `1e-6 I` | storage candidate if `Mi = Ma + eps I` and `v' = a`; B45-1 open | not a proved force bias |
| central-FD `C` | cubic power candidate after B45-4; not yet source-bound | zero at `dq = 0` by the quadratic contraction in `arm_MCG` |
| central-FD `G` | conservative rescale only for the frozen cosine object; deployed `U` unbound | cancelled against `G0v` in `exact_ddq(0,0,0)` as construction text, not as `G(0)=0` |
| controller `tauI-tauA` | open; deployed disturbance gain is the literal vector above | open off the zero state |
| solve residual | open runtime term; zero only if the returned `a` meets `Mi a = tauI-cI-gI` | construction gives a zero right-hand side at the zero state; Float64 residual unproved |

## Obstruction

```text
ledger: e = (Ma-Mi)a + (tauI-tauA) + (cA-cI) + (gA-gI) + (Mi a - (tauI-cI-gI))
removable only if: Mi = Ma + 1e-6 I, v' = a, and (separately) G_FD = sigma G_exact
not proved: B45-1, B45-2, B45-4, Float64(1e-5)=1/100000, controller constant match
offsets: FDForceBudget.offset is enclosure slack, not equilibrium bias, not rho|v|
zero state: exact_ddq text cancels G0v against Gq; not a Float64 certificate
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P5-008` open.
- Requested action: harvest this as a corroborating pending split. Do not formalize `sigma U` as deployed storage. Next math owner should discharge B45-1 before the regularizer cancellation, and keep controller/solve on a separate bias lane. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not convert positive-offset envelopes into `rho|v|`.
- Did not use samples as global estimates.
- Did not close P5 or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
