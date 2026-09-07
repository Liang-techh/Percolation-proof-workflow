---
kind: review_result
review_id: review-T-M4-007-sumengchen-20260907T0018
task_id: T-M4-007
parent_task_id: T-M4-006
source_agent: 苏梦辰
claimed_at: 2026-09-07T00:10:00-06:00
created_at: 2026-09-07T00:18:00-06:00
integration_status: pending
admission_label: compiled_candidate
proposed_integration_target: theorem
requested_action: independent_verify_by_封不觉_then_harvest_by_梁智炜
---

# T-M4-007 — pure arithmetic budget-transfer Lean sidecar

## Scope

This formalizes only the source-independent arithmetic child released by
`T-M4-006`.  The ramp integral, physical `rhoBar`, P7 source binding, P8
flowpipe/existence/coverage, terminal `L/g` source premises, M4 admission, and
registry mutation remain outside this sidecar.

Mathematical source:

- `agent_review_inbox/review-T-M4-006-daai-xianzun-20260906T2346.md`
  - blob `19aa5c8f0694a96c08326724766e326c4a01cf4f`.

## Lean artifact

Created portable sidecar:

- `examples/routeb_m4_tail_budget_transfer_lean/M4TailBudgetTransfer.lean`
  - blob `88737af4367e435e5d5e0752af04b3b601488352`;
- `examples/routeb_m4_tail_budget_transfer_lean/verify.sh`
  - blob `16da37d85e96c777ed420904959f9ea66fad0e24`;
- `examples/routeb_m4_tail_budget_transfer_lean/README.md`
  - blob `e8248f8c4d6fa1343084ffe31dac8985a019fa80`;
- `examples/routeb_m4_tail_budget_transfer_lean/lean-toolchain`
  - blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe`;
  - pin `leanprover/lean4:v4.32.0`, matching `examples/local_fkg`.

The verifier contains `CI_PORTABLE=1`, resolves `lake` from `PATH`, checks the
repository-pinned Lake root/toolchain, and uses no user-specific absolute path.

## Formalized theorem statements

The sidecar defines the exact constants

```text
oldGate   = 4483/2000
newGate   = 1401/625
tailScale = 160000.
```

It proves:

```lean
theorem tail_budget_transfer
    (Dbase rhoBar Dtail : ℝ)
    (hDtail : Dtail ≤ rhoBar / tailScale)
    (hbudget : Dbase + rhoBar / tailScale ≤ newGate) :
    Dbase + Dtail ≤ newGate
```

```lean
theorem old_gate_plus_rho16_exact :
    oldGate + 16 / tailScale = newGate
```

```lean
theorem old_gate_plus_tail_of_rho_le_16
    (Dbase Dtail rhoBar : ℝ)
    (hbase : Dbase ≤ oldGate)
    (hrho : rhoBar ≤ 16)
    (hDtail : Dtail ≤ rhoBar / tailScale) :
    Dbase + Dtail ≤ newGate
```

and the reusable slack form

```lean
theorem tail_budget_from_slack
    (Dbase Dtail rhoBar Delta : ℝ)
    (hDtail : Dtail ≤ rhoBar / tailScale)
    (hrhoSlack : rhoBar / tailScale ≤ Delta)
    (hbaseSlack : Dbase + Delta ≤ newGate) :
    Dbase + Dtail ≤ newGate.
```

The mathematical review proposed an additional `0 ≤ rhoBar` premise for the
old-gate corollary.  Lean confirms it is not needed for this pure monotonic
arithmetic implication: division is by the fixed positive `160000`, so
`rhoBar ≤ 16` already gives the required scaled inequality.  Physical source
lanes may still naturally prove `rhoBar ≥ 0`, but it is not a logical
requirement of this arithmetic theorem.

## GitHub-hosted compile / axiom evidence

The first shared-workflow attempt at head
`8116ca7a4d1a38f3e5e8d5d7df80c92d5b7ec420` failed before reaching this
sidecar because an unrelated earlier-sorted portable sidecar
`examples/anthropic_flt_quotient_transport_sidecar/verify.sh` exited on a bad
relative Lake-root path.  This was a CI harness obstruction, not a theorem
compile result.

To prevent one independent sidecar from hiding all later focused results, I
made a narrow CI-harness repair in
`.github/workflows/lean-agent-sidecars.yml`: each `CI_PORTABLE=1` script now
runs inside a non-fail-fast per-script branch, records `SIDECAR_RESULT=PASS/FAIL`,
continues through the full list, and only fails the aggregate step after all
focused results have been reported.  The workflow semantics remain fail-closed:
any failing sidecar still makes the job fail.  Repair commit / tested head:

```text
a59fc2add8304114809a6131c8b8deb06885cf17
```

GitHub Actions evidence for that head:

```text
workflow: Lean agent sidecars
run_id:   34090011147
job_id:   101641401296
runner:   ubuntu-24.04
job conclusion: failure (because other independent sidecars still fail)
```

Crucially, the job now records the focused T-M4-007 result before the aggregate
failure:

```text
Running examples/routeb_m4_tail_budget_transfer_lean/verify.sh
LEAN_TOOLCHAIN=leanprover/lean4:v4.32.0
'RouteBM4TailBudgetTransfer.tail_budget_transfer' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBM4TailBudgetTransfer.old_gate_plus_rho16_exact' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBM4TailBudgetTransfer.old_gate_plus_tail_of_rho_le_16' depends on axioms:
  [propext, Classical.choice, Quot.sound]
'RouteBM4TailBudgetTransfer.tail_budget_from_slack' depends on axioms:
  [propext, Classical.choice, Quot.sound]
AXIOM_AUDIT=PASS
M4_TAIL_BUDGET_TRANSFER_FOCUSED_CHECK=PASS
PHYSICAL_RHOBAR_BINDING=OPEN
P8_FLOWPIPE_COVERAGE=OPEN
REGISTRY_MUTATION=false
SIDECAR_RESULT=PASS path=examples/routeb_m4_tail_budget_transfer_lean/verify.sh
```

Thus the T-M4-007 focused kernel compile and axiom audit pass under the pinned
GitHub-hosted Lean 4.32.0 environment.  No `sorryAx` appears in this theorem set.
The overall workflow is intentionally **not** reported as green because two
other independent portable sidecars fail elsewhere in the same aggregate job.

## Other CI blockers exposed, not taken over

The improved harness also exposed two disjoint failures owned by other lanes:

1. `examples/anthropic_flt_quotient_transport_sidecar/verify.sh`:
   `cd: ../local_fkg: No such file or directory`;
2. `examples/routeb_p5_weighted_dual_residual_lean/WeightedDualResidual.lean`:
   an unused `hκ1` warning promoted to error and an invalid projection from a
   disjunction, with resulting `sorryAx` in the zero-kappa branch.

I did not modify those other agents' theorem files.  They should be repaired by
their assigned formalization owners using the now-visible focused logs.

## Remaining formalization boundary

This sidecar does **not** formalize `ramp_tail_integral_bound`; that theorem
requires the exact interval-integral/measurability/integrability interface and
was explicitly separated by `T-M4-006`.  It also does not prove a same-domain
physical upper bound `rhoBar ≤ 16`.

Therefore this result is only a `compiled_candidate` arithmetic child.  It is
**待封不觉独立验证 / 待梁智炜最终整合**.  No authoritative M4 gate, registry
entry, source-binding status, or overall conclusion was changed.
