---
kind: review_result
review_id: review-T-P5-013-FINITE-HORIZON-ADMISSION-liuchuanafeng-20261007T0114Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T01:14:00Z
inspected_commit: e2193684909605ea58fd68b721a496da4ffb9c11
claim_commit: 81c79dfe187a358eb883ea58a5803bc835e6ec51
prior_head: e2193684909605ea58fd68b721a496da4ffb9c11
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/agent_roster.md
  - agent_review_inbox/claim-T-P5-013-FINITE-HORIZON-ADMISSION-liuchuanafeng-20261007T0112Z.md
  - agent_review_inbox/claim-T-P5-013-honglianmozun-20260907T0351.md
  - agent_review_inbox/claim-T-P5-013-sumengchen-20260907T0411.md
  - agent_review_inbox/review-T-P5-013-honglianmozun-20260907T0358.md
  - agent_review_inbox/review-T-P5-013-sumengchen-20260907T0428.md
  - examples/routeb_p5_finite_horizon_budget_lean/README.md
  - examples/routeb_p5_finite_horizon_budget_lean/P5FiniteHorizonBudget.lean
task_id: T-P5-013
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-013 admission audit: pointwise barrier algebra holds, source and first-exit still open

## Question

At inspected commit `e2193684909605ea58fd68b721a496da4ffb9c11`, does the existing `T-P5-013` math review, or the pointwise Lean sidecar still present at this commit, already supply a first-exit calculus theorem, same-domain caps for `S_F`/`Hbar`/`Rbar`/`W_min`, P8 ramp-graph coverage, or any source/registry admission?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published source-independent interface is internally consistent: after splitting the damping margin into cubic and remainder parts, a one-sided ramp cap and a division-free dual-work budget give `Zdot <= Hbar + BR` inside the cubic barrier, and strict headroom `Z(0)+T*B < Zstar` is the right finite-horizon contract. The same review correctly blocks upgrading `A <= K*Z` into asymptotic decay. None of that closes source coefficients, the calculus first-exit layer, P8 coverage, or registry.

The historical Lean review may remain a `compiled_candidate` for the pointwise sidecar only. This pass did not recompile it and does not promote that candidate. It does not reclassify the neighboring `T-P5-012` storage-shift identity or the `T-P5-014` weighted-dual adapter as a `T-P5-013` receipt. Prior authorship is preserved. This file does not overwrite 红莲魔尊 or 苏梦辰.

This is not `verified`: no kernel run in this pass and no source packet. It is not `rejected`: the finite-horizon ledger and the `A <= K Z` obstruction both remain. It is not `architecture_only`: the math review states exact scalar identities and a scalar counterexample, and the sidecar names seven theorems. It is not a new `compiled_candidate`: this agent did not run `verify.sh`.

## Evidence inspected (read-only)

1. **Queue does not close this leaf.** `task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` does not contain `T-P5-013` and does not mark it verified. Roster text still lists 流川枫 as unavailable for new dispatch; this audit does not rewrite that roster.
2. **Math review stays conditional.** `review-T-P5-013-honglianmozun-20260907T0358.md` blob `7f021931cfc9f5bc6210231870c049cfdef3fcaf` derives the mixed ledger, the sharp dual charge `Rbar/(4 g_R)`, the first-exit argument under an external regularity premise, the rational `T=1` 50/50 criterion, and the obstruction that `A <= K Z` does not imply `Zdot <= -alpha Z + B`. Its own label is `pending`. It explicitly leaves `S_F`, `W_min`, `Hbar`, `Rbar`, and P8 graph coverage open.
3. **Sidecar is pointwise only.** At HEAD `e2193684909605ea58fd68b721a496da4ffb9c11`, README blob `1ac3d3210de2a13febcedc2e96a8d9d05f38fab9` and Lean blob `ff07414325a9e5ce7dac9583ebe97f69fd45c8d2` attribute the file to `T-P5-013` and stop before the calculus/ODE first-exit argument. Present declarations are `abs_le_of_sq_le_sq_nonneg`, `cubic_absorption_from_energy_barrier`, `dual_work_budget`, `mixed_energy_rate`, `linear_growth_stays_below_barrier`, `t1_fifty_fifty_headroom_from_rational`, and `upper_storage_coercivity_counterexample`. `linear_growth_stays_below_barrier` takes `Zt <= Z0 + t*B` as a hypothesis. `mixed_energy_rate` takes `hRamp <= Hbar` and the cubic/dual premises as hypotheses. No `S_F`, `Hbar`, `Rbar`, or `W_min` is instantiated.
4. **Historical Lean label is not this pass.** `review-T-P5-013-sumengchen-20260907T0428.md` blob `e97a1e48bbcb347ac8d016bc33a08c96326b4918` reports a focused CI pass on commit `590a3f53212710bc00f7e13714b7184b83e92425` and labels that sidecar `compiled_candidate`. This audit does not replay that run and does not treat it as source or parent closure.
5. **Historical claims preserved.** `claim-T-P5-013-honglianmozun-20260907T0351.md` blob `81fb9052a430829bd5bda63771209842abc919e9` and `claim-T-P5-013-sumengchen-20260907T0411.md` blob `0a4508384720594a70ea6404900badc6298cd442` remain the original claims. This audit does not replace them.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: not run by this agent
math_review_blob: 7f021931cfc9f5bc6210231870c049cfdef3fcaf
lean_review_blob: e97a1e48bbcb347ac8d016bc33a08c96326b4918
historical_math_claim_blob: 81fb9052a430829bd5bda63771209842abc919e9
historical_lean_claim_blob: 0a4508384720594a70ea6404900badc6298cd442
sidecar_blob: ff07414325a9e5ce7dac9583ebe97f69fd45c8d2
readme_blob: 1ac3d3210de2a13febcedc2e96a8d9d05f38fab9
first_exit_calculus: not formalized in the sidecar
S_F_Hbar_Rbar_W_min: not exhibited
P8_ramp_graph_coverage: not exhibited
```

## Obstruction

```text
identity_surface: source-independent, algebraically consistent with the published math review and the pointwise sidecar
missing_calculus: finite_horizon_sublevel / first-exit integral is still an external premise of linear_growth_stays_below_barrier
asymptotic_upgrade: blocked by upper_storage_coercivity_counterexample; A <= K*Z is the wrong direction
missing_for_parent_close:
  one calculus/trajectory theorem producing Z(t) <= Z(0)+t*B on the actual horizon
  same-domain rational or sound-interval caps for S_F, Hbar, Rbar, and W_min / Z0
  the disjoint T-P5-014 weighted-dual source adapter, not reused here as a receipt
  P8 coverage along w=c*t; energy confinement does not repair the |w|<=1/100 box obstruction
  a fresh pinned Lean receipt if the first-exit child is formalized
blobs:
  math_review: review-T-P5-013-honglianmozun-20260907T0358.md
  lean_review: review-T-P5-013-sumengchen-20260907T0428.md
  claim: 81c79dfe187a358eb883ea58a5803bc835e6ec51
flags: formal_certificate_allowed=false, registry_eligible=false
```

## Assumptions still required

- a later Lean owner may formalize the first-exit lemma, but that is a new receipt obligation, not implied by `linear_growth_stays_below_barrier`;
- the 50/50 split in equation (27) is a sufficient rational choice, not an optimal allocation and not a source binding of `g0`;
- the scalar witness `A=0`, `Z=1` rules out reading asymptotic decay off `A <= K Z`, but does not identify the physical dissipation;
- historical CI on `590a3f53` is not re-authenticated here;
- coverage, Float64 enclosure, and comparator admission stay outside this leaf.

## Integration target and requested action

- Target: documentation / inbox provenance only. Leave `T-P5-013` open until the first-exit calculus and same-domain `S_F`/`Hbar`/`Rbar`/`W_min` caps are supplied, and until any new Lean package has its own receipt.
- Requested action: harvest this as a pending admission audit. Do not treat the pointwise sidecar or the historical `compiled_candidate` label as verified closure of this leaf, and do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not compile, repair, or invent an exit code or axiom list.
- Did not add a Lean sidecar or alter the 2026-09-07 identity statements.
- Did not claim concrete `S_F`, `Hbar`, `Rbar`, `W_min`, source equality, coverage, or P5/P8/M4 closure.
- Did not overwrite prior reviews or claims.
- Did not edit registry, state, task queue, or formal proofs.
