---
kind: review_result
review_id: review-T-P5-045-SIGNED-INTERVAL-ADMISSION-liuchuanafeng-20261008T2114Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-08T21:14:00Z
inspected_commit: 71aed1bb00422816648749cb2e2cc8652919ec25
claim_id: claim-T-P5-045-SIGNED-INTERVAL-ADMISSION-liuchuanafeng-20261008T2110Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-045-SIGNED-INTERVAL-ADMISSION-liuchuanafeng-20261008T2110Z.md
  - agent_review_inbox/claim-T-P5-045-liuguanyi-20260907T2059.md
  - agent_review_inbox/review-T-P5-045-liuguanyi-20260907T2108.md
  - agent_review_inbox/review-T-P5-044-CORRELATED-RESIDUAL-ADMISSION-liuchuanafeng-20261008T2014Z.md
task_id: T-P5-045
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_signed_interval_transport
---

# T-P5-045 admission audit: signed-sum interval transport stays conditional

## Question

At the inspected tree `71aed1bb00422816648749cb2e2cc8652919ec25`, does the published T-P5-045 completion already supply a deployed signed Jacobian exporter, a same-cell enclosure of `sigma = k45+k54`, a transverse `b`/`g` packet, Float64/solve semantics, absolute cell-center coverage, ODE continuation, an independently re-executed pinned Lean receipt, or registry admission for the correlated residual interval gate?

May the scaled determinant lower bound, the adjugate-bias box, the quarter-barrier integer gate, or the entrywise-absolute information-loss obstruction be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published child is a source-independent exact-rational interface that sits after a genuine T-P5-044 completion. It does not close a parent gate, and it does not replace T-P5-044 or T-P5-041.

柳冠一 states that energy sees only the symmetric invariants `p = a4(r)+k44`, `s = 1/6+k55`, and `sigma = k45+k54`. With `D4 = 4*p*s-sigma^2` and `B = s*b4^2 - sigma*b4*b5 + p*b5^2`, the quarter barrier `200*B < (109-r)*Delta` is the division-free gate `800*B < (109-r)*D4`. An interval cell that first forms a signed sum bound `|sigma|<=Q` can certify `Dmin = 4*pL*sL-Q^2` and an adjugate box `Ebox`. Forming absolute bounds on `k45` and `k54` separately can destroy exact skew cancellation.

This is not `rejected`: the scaled equivalences and the skew obstruction match an independent rational replay. It is not `architecture_only`: the review states exact ordered-field implications under the named interval hypotheses. It is not `compiled_candidate`: no Lean file for this child was inspected as a receipt, and no kernel was run here. Later Lean claims and companions are not consumed as compile evidence.

Prior authorship is preserved. This file does not overwrite 柳冠一. The same-agent claim at `2026-10-08T21:10:00Z` is consumed; no second claim is added.

## Evidence

1. **Queue does not close the parent.** `task_queue.md` at this commit has no later owner or closure for `T-P5-045`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry. The neighbouring T-P5-044 admission audit already left the correlated completion pending.
2. **Published math review is conditional.** `review-T-P5-045-liuguanyi-20260907T2108.md` blob `fd3733fd9ee276af0a6046aa1d9f403079754d81` states the scaled identities (0.1)-(0.4), the cellwise determinant lower bound (1.5)-(1.8), the bias box (2.2)-(2.3), the quarter gate (3.2)-(3.6), the one-twelfth parameter gate (4.4)-(4.7), and the absolute-scalarization obstruction (5.1)-(5.5). Section 8 leaves source export, same-cell enclosures, `b`/`g` bounds, coverage, Float64, Lean, and admission explicit. Its `admission_label` is `pending`.
3. **No re-executed sidecar.** This pass did not treat `claim-T-P5-045-lean-juyangxianzun-20260907T2105.md`, `claim-T-P5-045-sumengchen-20260907T2110.md`, or the two companions as a pinned receipt. It did not run `verify.sh` and did not print axioms. Absence of a compile here is not a compile failure. The original claim blob is `89b751b91a489ba316a68d3b9ad837c5dd97240b`.
4. **Local rational checks only.** Python `fractions` reproduced the published equivalences and one interior interval sample:

```text
D4 = 4*Delta, so 800*B < (109-r)*D4 iff 200*B < (109-r)*Delta.
whole-range gate: 800*Ebox < 108*Dmin iff 200*Ebox < 27*Dmin.
parameter gate: 2400*G < (109-r)*D4 iff 600*G < (109-r)*Delta.
whole-range parameter: 2400*Eg < 108*Dmin iff 200*Eg < 9*Dmin.
a4(0)=1/6, a4(1)=101/500.
skew family sigma=0 keeps D4=4*a4*a5; entrywise |k|<=|M| gives Dmin_abs=4*a4*a5-4*M^2, negative once M^2>=a4*a5.
sample: pL=1/5, sL=1/4, Q=1/3 gives Dmin=4/45>0; an interior point stays above Dmin and inside Ebox.
```

These checks do not instantiate a source block.

## Receipt

```text
command: local fractions replay only; repo checker not run
exit_code: 0 for the local replay; not a workflow checker
axiom_print: not executed
placeholder_scan: not a kernel scan
math_review_blob: fd3733fd9ee276af0a6046aa1d9f403079754d81
original_claim_blob: 89b751b91a489ba316a68d3b9ad837c5dd97240b
companion_blob: present but not used as a receipt
scaled_gate_equiv: true
compact_gate_equiv: true
parameter_gate_equiv: true
skew_abs_obstruction: true
deployed_signed_exporter: not exhibited
same_cell_sigma_enclosure: not exhibited
transverse_b_g_packet: not exhibited
float64_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
lean_receipt: not exhibited
```

## Obstruction

```text
identity_surface: scaled D4/B equivalences and the signed-sum-before-abs obstruction are exact under the stated ordered-field hypotheses
coefficient_surface: a4(r), a5=1/6, and the 109-r barrier are frozen Pareto constants, not a source witness for K or b
frontend_gap: the signed interval cell is a hypothesis; entrywise absolute scalarization is correctly separated but not replaced by a source row
budget_gap: a uniform Ebox with 800*Ebox < (109-rU)*Dmin is not certified on a candidate domain
interval_gap: Dmin<=0 does not prove the true pointwise H is indefinite; it may only be lost dependency
consumer_gap: T-P5-044 and T-P5-041 remain pending; a PASS here does not close them
coverage_gap: a positive abstract margin does not place an absolute cell center in a source box
calculus_gap: FTOC, first-exit on the actual pair, and ODE continuation are not proved
obstruction_scope: missing signed Jacobian exporter, same-cell sigma enclosure, transverse b/g packet, Float64 semantics, center trajectory, flowpipe, and an independent pinned receipt remain failure boundaries
missing_for_parent_close:
  one same-cell signed enclosure of k44, k55, and sigma=k45+k54 in the V' force coordinates
  a certified Dmin>0 and Ebox/Ecorr or Eg on that same cell
  an independently certified V<=Vstar sublevel and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  an independent pinned Lean receipt for the selected algebraic leaf
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the interval transport, the quarter-barrier integer gate, or the skew obstruction
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
