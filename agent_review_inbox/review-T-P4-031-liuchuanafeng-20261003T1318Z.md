---
kind: review_result
review_id: review-T-P4-031-liuchuanafeng-20261003T1318Z
source_agent: 流川枫
created_at: 2026-10-03T13:18:00Z
claimed_at: 2026-10-03T13:18:00Z
inspected_commit: badff6c883b20424accc1f44d51bd7be990e5c7d
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_pmi_certificate.jl
  - examples/routeb_source_binding_audit/REPORT.md
  - docs/routeb-source-fork-canonical-audit.md
task_id: T-P4-031
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_obstruction_do_not_close_p4
---

# T-P4-031 audit: deployed damping sum is pinned; lifted vector is not in this commit

## Question

At commit `badff6c883b20424accc1f44d51bd7be990e5c7d`, which damping vector is the source of truth for the deployed controller, and does the queue-cited lifted model `(Kd+Bfr)=(1.8,1.4,0.95,0.5,0.65,0.8)` match it?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The frozen deployed snapshot has an exact componentwise sum `(Kd+b_fr)=(1.3,1.1,0.95,0.8,0.65,0.5)`, and `exact_ddq` multiplies that sum by `dq`. The named lifted file is absent from this commit, so that second vector is not a source fact here and must not be copied into the deployed controller. Source binding of any lifted descriptor remains open.

This is not `rejected`: the deployed text is internally consistent. It is not `verified` or `compiled_candidate`: no checker or Lean process was run, and the lifted model was not regenerated. It is not `architecture_only`: the obstruction is a missing file plus an unproven descriptor identity, not a missing interface name.

The 2026-09-07 claim `claim-T-P4-031-liuchuanafeng-20260907T1400.md` is left intact. This file does not replace it.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P4-031` asks for a source-of-truth decision between deployed `(Kd+b_fr)=(1.3,1.1,0.95,0.8,0.65,0.5)` and lifted `(Kd+Bfr)=(1.8,1.4,0.95,0.5,0.65,0.8)`, plus the affected descriptor equations. Forbidden: silently copying one vector into the other, calling pointwise agreement a source proof, or changing the controller while preserving old receipts.

2. **Deployed snapshot, blob `27cf497b6f27919eb5b554369fb1444f4314c942`.** `dhport_lib.jl` sets

```text
Kd   = [0.8, 0.7, 0.6, 0.5, 0.4, 0.3]
b_fr = [0.5, 0.4, 0.35, 0.3, 0.25, 0.2]
Kd + b_fr = [1.3, 1.1, 0.95, 0.8, 0.65, 0.5]
```

   `exact_ddq` uses

```text
tau = -Kp .* q - (Kd + b_fr) .* dq + G0v + (gw_coef .* I_val) .* w
```

   This is a source-text fact for the frozen snapshot, not a theorem that every historical certificate used this vector.

3. **PMI `c` is the same sum divided by `I_val`, not a second damping law.** `routeB_pmi_certificate.jl` blob `207b6b361eeb465aee8933cff8b9f41a1b17a89f` sets

```text
c = (b_fr + Kd) ./ I_val
  = [1.3, 1.1, 0.95, 0.8, 0.65, 0.5] ./ [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
```

   On the block-(4,5) slots this is `c4 = 0.8/0.2 = 4` and `c5 = 0.65/0.1 = 6.5`. The block model then uses `-c[ja]*dqa` and `-c[jb]*dqb`. That normalization must stay explicit. It is not evidence that the raw sum equals `(1.8,1.4,0.95,0.5,0.65,0.8)`.

4. **Named lifted file is not in this commit.** `routeB_fourier_lifted_descriptor_model.jl` is not present at the repository root, under `examples/routeb_source_binding_audit/snapshots/`, or under `examples/routeb_b45_fourier_normal_form/`. `REPORT.md` blob `8bc5cd5444473396caa13af107428f0350cca742` does not record that vector. The fork audit blob `fde103ddbd337e44d0c295e47d8eb02ffd884e62` likewise does not instantiate it. The queue citation is therefore planning text, not a blob fact at `badff6c883b20424accc1f44d51bd7be990e5c7d`.

5. **If the queue vector is treated only as an unverified citation, it still disagrees.** Componentwise, the only shared entry is index 3 (`0.95`). Indexes 4 and 5 are not a swap of the deployed pair `(0.8,0.65)`, and indexes 1, 2, and 6 differ. No pointwise agreement is available to misuse as a proof.

## Obstruction

```text
source_of_truth_for_deployed_tau: frozen dhport_lib.jl (Kd+b_fr) on dq
deployed_sum: (1.3, 1.1, 0.95, 0.8, 0.65, 0.5)
pmi_c: that sum divided by I_val; block slots 4 and 6.5
lifted_file: routeB_fourier_lifted_descriptor_model.jl absent at this commit
queue_cited_lifted_sum: not a blob fact; not copied
open: descriptor/nominal equations that would consume the lifted vector
open: proof that any historical certificate used this snapshot
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-031` open.
- Requested action: harvest this as a pending obstruction. Keep the deployed snapshot sum as the controller anchor. Do not copy the queue-cited lifted vector into `dhport_lib.jl` or into the PMI `c` formula. Next owner should either pin the lifted file with a hash or mark that surrogate rejected, then rewrite only the descriptor equations that actually consume it. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not copy either damping vector into the other.
- Did not treat numeric agreement as source proof; the lifted vector was not even present.
- Did not change the controller or preserve/rewrite certificate receipts.
- Did not close P4 or the lifted descriptor.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
