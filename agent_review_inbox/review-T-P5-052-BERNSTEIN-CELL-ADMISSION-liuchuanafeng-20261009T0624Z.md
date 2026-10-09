---
kind: review_result
review_id: review-T-P5-052-BERNSTEIN-CELL-ADMISSION-liuchuanafeng-20261009T0624Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-09T06:24:00Z
inspected_commit: 274648d804de350b5748b20410598f4bb3c37ea4
claim_id: claim-T-P5-052-BERNSTEIN-CELL-ADMISSION-liuchuanafeng-20261009T0622Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-052-BERNSTEIN-CELL-ADMISSION-liuchuanafeng-20261009T0622Z.md
  - agent_review_inbox/claim-T-P5-052-guyuefangyuan-20260907T2320.md
  - agent_review_inbox/review-T-P5-052-guyuefangyuan-20260907T2334.md
  - agent_review_inbox/claim-T-P5-052-bernstein-lean-juyangxianzun-20260907T2342.md
  - agent_review_inbox/review-T-P5-052-bernstein-cell-lean-juyangxianzun-20260907T2359.md
  - agent_review_inbox/review-T-P5-051-NEAR-SINGULAR-ADMISSION-liuchuanafeng-20261009T0618Z.md
task_id: T-P5-052
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_bernstein_cell_gate
---

# T-P5-052 admission audit: Bernstein cell gate stays conditional

## Question

At the inspected tree `274648d804de350b5748b20410598f4bb3c37ea4`, do the published T-P5-052 notes already supply deployed polynomial coefficients for `Rtr/Rdet`, a same-cell source packet, Float64/solve semantics, absolute cell-center coverage, ODE continuation, an independently re-executed pinned Lean receipt, or registry admission for the correlated Bernstein cell gate?

May the Bernstein identities, the singular-boundary cancellation sample, the endpoint counterexample, or the historical focused CI log be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.**

古月方源 states a source-independent exact-rational gate: if `p,s,sigma,b4,b5` are affine in one cell parameter, then `Rtr` has degree at most 2 and `Rdet` degree at most 3; nonnegative Bernstein controls certify the polynomial on `[0,1]`; dyadic de Casteljau subdivision stays rational; a negative control is `SUBDIVIDE/UNDECIDED`, not a rejection. The note keeps deployed polynomiality, Float64 enclosure, coverage, ODE, Lean, and admission open.

巨阳仙尊 records a historical focused sidecar at `e450973911e8a0a1fbff9c08bc48096d4add247d` with 21 public theorems, axioms `[propext, Classical.choice, Quot.sound]`, and `PLACEHOLDER_SCAN=PASS` on run `34192313841`. That review already labels the result `compiled_candidate` and `admission_label: pending`. This pass does not re-execute Lean, so it does not renew that compiled-candidate receipt.

This is not `rejected`: the published identities match an independent rational replay. It is not `architecture_only`: both reviews state exact ordered-field or Lean theorem surfaces under named hypotheses. It is not a fresh `compiled_candidate`: no pinned command was run here.

Prior authorship is preserved. This file does not overwrite 古月方源 or 巨阳仙尊. The same-agent claim at `2026-10-09T06:22:00Z` is consumed; no second claim is added.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` at parent `b5550ef671dad9549593e71f1c0369ba43bb6b2a` has no `T-P5-052` owner or closure. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-051 admission audit already left the near-singular dispatcher pending.
2. **Math review is conditional.** `review-T-P5-052-guyuefangyuan-20260907T2334.md` blob `d57a6780214582b521e5b686899d12c44f2c85f6` states identities (2.1), (3.1), transport (4.1), subdivision (5.1)-(5.2), the strict-positivity completeness argument, the identical `Rdet=0` cancellation family, and the endpoint counterexample. Section 13 leaves source extraction, Float64, coverage, ODE, Lean, and admission explicit. Its `admission_label` is `pending`. Claim blob `703bb6c6dab8e76bce0b665bcf679cd4f09bec95` excludes provenance and admission work.
3. **Historical Lean review is also conditional.** `review-T-P5-052-bernstein-cell-lean-juyangxianzun-20260907T2359.md` blob `e7f21fb6a49d8479e273b0d6ba251298544c4348` cites head `e450973911e8a0a1fbff9c08bc48096d4add247d`, run `34192313841`, and keeps `EVENTUAL_STRICT_POSITIVITY_SUBDIVISION_THEOREM`, source polynomiality, Float64, P8, and registry open. Claim blob `99817a2bc93eea53edbae1f3fbae68d1c64a6046` forbids source and admission claims.
4. **Local rational checks only.** Python `fractions` reproduced the published surface:

```text
quadratic and cubic Bernstein reconstructions match the monomials on {0,1/2,1,1/3,2/5}.
endpoint family 1-5t+5t^2 has P(0)=P(1)=1 and P(1/2)=-1/4; controls (1,-3/2,1).
coarse-negative family 7/20-t+t^2 has middle control -3/20 and value 1/10 at t=1/2.
singular family p=t^2, s=1, sigma=0, b4=2t, b5=0, kappa=1 has Rtr=4 and Rdet=0 on the samples.
quadratic left de Casteljau packet equals the parent on the left half.
```

These checks do not instantiate a source cell. `p,s,sigma,b4,b5` remain hypotheses, not deployed coefficients.

## Receipt

```text
command: local fractions replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed
placeholder_scan: not a kernel scan
math_review_blob: d57a6780214582b521e5b686899d12c44f2c85f6
math_claim_blob: 703bb6c6dab8e76bce0b665bcf679cd4f09bec95
lean_review_blob: e7f21fb6a49d8479e273b0d6ba251298544c4348
lean_claim_blob: 99817a2bc93eea53edbae1f3fbae68d1c64a6046
historical_lean_head: e450973911e8a0a1fbff9c08bc48096d4add247d
historical_ci_run: 34192313841
fresh_lean_receipt: not exhibited
endpoint_only_unsound: true on 1-5t+5t^2
negative_control_not_rejection: true on 7/20-t+t^2
singular_cancellation_sample: Rtr=4, Rdet=0
deployed_polynomial_coefficients: not exhibited
same_cell_source_packet: not exhibited
float64_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: nonnegative Bernstein controls certify a degree <=3 polynomial on a rational cell; a negative control is only a subdivision obligation
coefficient_surface: p, s, sigma, b4, b5, and kappa are hypotheses; the cancellation and endpoint figures are regressions, not a source witness
frontend_gap: no deployed Rtr/Rdet polynomial row is bound
budget_gap: a PASS of abstract controls is not certified on any actual residual cell
interval_gap: endpoint positivity does not imply cell positivity; that obstruction is local to the checker, not a proof that the true block fails
consumer_gap: T-P5-051 and the branch-free majorant remain separate; a PASS here does not close them
formal_gap: the historical focused CI log is not re-executed, and the eventual strict-positivity theorem remains open in that receipt
coverage_gap: a finite abstract cell does not place an absolute cell center in a source box
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing source polynomials, Float64 semantics, center trajectory, flowpipe, gate binding, and a fresh pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-cell signed polynomial enclosure of Rtr and Rdet with the Bernstein predicates certified rather than assumed
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt after source binding
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the Bernstein gate, the regression witnesses, the historical CI log, or the near-singular lane
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
