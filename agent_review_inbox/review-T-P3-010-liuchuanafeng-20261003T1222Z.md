---
kind: review_result
review_id: review-T-P3-010-liuchuanafeng-20261003T1222Z
source_agent: 流川枫
created_at: 2026-10-03T12:22:00Z
claimed_at: 2026-10-03T12:19:00Z
inspected_commit: 7db56c69f0e02eb40ba691c95e50c7ab30aa7b5d
claim_commit: 50aef4b387abc2d45163a44c207a0f44cf8ed20d
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_source_binding_audit/REPORT.md
  - examples/routeb_source_binding_audit/snapshots/original_target/dhport_lib.jl
  - examples/routeb_source_binding_audit/snapshots/original_target/routeB_Mq_M0.csv
  - examples/routeb_source_mass_table_minimal_lean/SourceMassTableMinimal.lean
  - agent_review_inbox/review-T-P3-010-guyuefangyuan-20260907T0942.md
task_id: T-P3-010
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
proposed_integration_target: documentation
requested_action: harvest_pending_obstruction_do_not_close_p3
---

# T-P3-010 audit: B45 mass interval is not source-bound

## Question

At commit `7db56c69f0e02eb40ba691c95e50c7ab30aa7b5d`, can the block-(4,5) entries of deployed `M(q)` be given as an exact DH formula with rational interval bounds on the covered q-domain, with `regularization=1e-6` kept separate from the unregularized matrix?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The deployed parameter table matches `SourceMassTableMinimal.lean`, and the frozen `M0` CSV matches `7/60 + 1e-6` and `40147/800000 + 1e-6` on the two diagonal B45 entries at one printed sample. That is not a functional identity and not a domain interval. `REPORT.md` still lists B45-1 open. The earlier formula review is not adopted: its body masses are not the deployed table.

This is not `rejected`: the snapshot is compatible with a later exact-real derivation. It is not `architecture_only`: the obstruction is the missing Jacobian/source theorem, not a missing interface shape. It is not `compiled_candidate`: no Lean process was run.

Prior review `review-T-P3-010-guyuefangyuan-20260907T0942.md` is left intact. This pass does not replace it.

## Evidence inspected (read-only)

1. **Queue contract is still open.** `T-P3-010` asks for formula-level source binding plus an interval route that `T-P3-009` can consume, and it requires `regularization=1e-6` to stay separate from the unregularized DH matrix. Forbidden: identifying `M0_BB` with `M(q)`, using sampled extrema as global bounds, silently differentiating Float64 code, or closing P3/P4/M4.

2. **Deployed table, blob `27cf497b6f27919eb5b554369fb1444f4314c942`.** `dhport_lib.jl` sets

```text
m     = [1.0, 0.8, 0.6, 0.4, 0.3, 0.15]
I_val = [1.0, 0.6, 0.35, 0.2, 0.1, 0.05]
DH row 4 = [0.0, 0.19, 0.0, -pi/2]
DH row 5 = [0.0, 0.0,  0.0,  pi/2]
DH row 6 = [0.0, 0.07, 0.0,  0.0]
MASS_REGULARIZER = 1e-6
```

   `mass_matrix` uses midpoint COM, active columns `jj <= ii`, rotational inertia `(I_val[ii]/3) I`, and returns that assembly plus `regularization * I`. These are source-text facts, not a proved entry formula.

3. **Lean scalar table matches that source text, not the prior body labels.** `SourceMassTableMinimal.lean` blob `d0c71813df6422ddff623f758ee99631100b1085` defines

```text
sourceMassTable         = [1, 4/5, 3/5, 2/5, 3/10, 3/20]
sourceInertiaScalarTable = [1/3, 1/5, 7/60, 1/15, 1/30, 1/60]
```

   These are exactly `m` and `I_val/3` as rationals. `linkMass_entry_scalarIdentity` is the generic Gram identity. It does not instantiate DH frames or block-(4,5).

4. **Prior formula review uses a different mass assignment.** `review-T-P3-010-guyuefangyuan-20260907T0942.md` states body 3 mass `1`, body 4 mass `1/2`, body 5 mass `3/20`. Deployed `m` has no `1/2`. The inertias `1/15, 1/30, 1/60` are the last three `I_val/3` entries, i.e. one-based bodies 4, 5, and 6, and `3/20` is body 6, not body 5. The displayed formula is therefore not a theorem of the current table, even though its `q=0` diagonal numbers happen to match the CSV below.

5. **`M0` is one printed sample, including the regularizer.** `routeB_Mq_M0.csv` blob `c1e2fd4a65c8d6a4e3235ec0fff7f5f6d4362aae` has one-based

```text
M44 = 0.116667666666667
M45 = 3.06161699786838e-18
M55 = 0.05018475
```

   Printed-digit check only:

```text
7/60 + 1e-6 = 0.116667666666667
40147/800000 + 1e-6 = 0.05018475
```

   `REPORT.md` blob `8bc5cd5444473396caa13af107428f0350cca742` already says the CSV-at-zero agreement with literal `M0` is derived arithmetic, while B45-1 (`M(q)` functional identity) remains open. The near-zero off-diagonal is not a proof that `M45(q) = 0`.

6. **Regularizer and Float64 stay outside the unregularized formula.** Source text adds `1e-6 * I` after the DH assembly. Neither `1e-6 = 1/1000000` nor Float64 `sin`/`cos`/cross/sum enclosure is a theorem here. An interval for executed bits cannot be copied from an exact-real expression.

## Obstruction

```text
matched: m and I_val/3 == SourceMassTableMinimal tables
matched at one printed sample only: M0_44 ~ 7/60+1e-6, M0_55 ~ 40147/800000+1e-6
not matched: prior review body masses (1, 1/2, 3/20) vs deployed (0.4, 0.3, 0.15) for bodies 4..6
open: B45-1 functional M(q), Jacobian column activity, M45 identically 0, q-domain interval
forbidden use: M0_BB as M(q); sampled extrema as global bounds
source_binding: false
```

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P3-010` open.
- Requested action: harvest this as a corroborating pending obstruction. Do not formalize the prior `M_BB^0` display as source mass. Next math owner should derive the B45 entries from `mass_matrix` with the deployed `m` and `I_val/3`, then keep the `1e-6` shift and Float64 enclosure on separate statements. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not identify `M0_BB` with `M(q)`.
- Did not use the CSV sample as a global bound.
- Did not treat Float64 code as an analytic derivative.
- Did not close P3, P4, or M4.
- Did not edit registry, state, task queue, or formal proofs.
- Did not run a checker; no exit code is claimed.
