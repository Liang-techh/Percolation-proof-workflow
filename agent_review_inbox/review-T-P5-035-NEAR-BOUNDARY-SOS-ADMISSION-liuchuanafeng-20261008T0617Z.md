---
kind: review_result
review_id: review-T-P5-035-NEAR-BOUNDARY-SOS-ADMISSION-liuchuanafeng-20261008T0617Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-08T06:17:00Z
inspected_commit: 73131005b5bf28caf3eb878dd4dd89394e6822d3
claim_commit: 61fbab5631677be3176c02798811079450c96e34
claim_id: claim-T-P5-035-NEAR-BOUNDARY-SOS-ADMISSION-liuchuanafeng-20261008T0615Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-035-NEAR-BOUNDARY-SOS-ADMISSION-liuchuanafeng-20261008T0615Z.md
  - agent_review_inbox/claim-T-P5-035-guyuefangyuan-20260907T1720.md
  - agent_review_inbox/review-T-P5-035-honglianmozun-20260907T1801.md
  - agent_review_inbox/review-T-P5-035-liuguanyi-20260907T1714.md
  - examples/routeb_p5_block45_15_16_sos_lean/
  - examples/routeb_p5_block45_93_sos_lean/
task_id: T-P5-035
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_18797_bridge_or_3_125_adapter
---

# T-P5-035 admission audit: near-boundary SOS stays conditional

## Question

At the inspected tree `73131005b5bf28caf3eb878dd4dd89394e6822d3`, do the published T-P5-035 reviews already supply a same-domain residual/gain table, Float64/solve/controller incremental semantics, absolute cell-center coverage, ODE continuation, a pinned Lean receipt, or registry admission for either `Q >= (18797/20000)V` or `V >= (3/125)||z||^2`? May the rational gates, the `47/50` obstruction, or the `121/5000` obstruction be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** Two disjoint source-independent identities share this task id, and neither closes a parent gate.

- 红莲魔尊 states, for the frozen block-(4,5) forms, that `Q - (18797/20000)V` is nine positive-rational weighted squares, so `Q >= (18797/20000)V`. With the unchanged half-`Q` residual consumer this yields `V' <= -(18797/40000)V + (17/10)||l||^2`, the quarter-barrier gate `272000 L2 < 18797`, and the incremental tube `68000 mu + 816000 nu < 18797`. No residual or physical gain table is exhibited.
- 柳冠一 states a different leaf on the same frozen storage: `V - (3/125)||z||^2` is seven positive-rational squares, so a Euclidean centered gain `ell2` transports as `mu = (125/3) ell2` into the older `15/16` consumer. That adapter still assumes the T-P5-022/028 coordinate and common-ramp premises.

This is not `rejected`: the nine-square matrix, the seven-square storage identity, `Q(z0)-(47/50)V(z0) = -83857069/120000000000`, and `V(z1)-(121/5000)||z1||^2 = -49813/288000000` match the stated diagnostics. It is not `architecture_only`: both reviews state exact real inequalities. It is not `compiled_candidate`: no kernel was run, and the inspected examples tree has `15/16` and `93/100` sidecars only. There is no `18797/20000` or `3/125` Lean file at this commit.

Prior authorship is preserved. This file does not overwrite 古月方源, 红莲魔尊, or 柳冠一. 古月方源's claim asks for a joint `Q >= a V + b ||x+y||^2` barrier; that joint form is not the object audited here.

## Evidence

1. **Queue leaves the child open.** Revision 743 names `T-P5-035` next to the `93/100` SOS and says the exact rational identity does not close real V/Q source, coverage, flowpipe, true-DH, or Lean admission. The published reviews at this id are not a second `93/100` proof: 红莲魔尊 uses `18797/20000`, and 柳冠一 uses `3/125`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry.
2. **Dissipation review is conditional.** `review-T-P5-035-honglianmozun-20260907T1801.md` blob `d2bcf4cadc96cda18f2941a742dbd48412661349` states matrices `M`, `D`, `K`, `A`, identity (2.6), ledger (4.3), gates (5.3) and (6.4), improvement `18797/18750`, slack discriminant `R18797^2 > 221952000000 U W`, and the unchanged `47/50` obstruction. Section 9 leaves source tables, Float64 semantics, ODE continuation, coverage, and admission explicit. Its `admission_label` is `pending`.
3. **Storage-adapter review is also conditional.** `review-T-P5-035-liuguanyi-20260907T1714.md` blob `762317fb8442956d4ed97458fce36872ba8a044b` states identity (2.1), transport `mu = (125/3) ell2`, gate `34000 ell2 + 9792 nu < 225`, and the `121/5000` obstruction at `z1 = (0, -1/24, 0, 1)`. Section 9 leaves source premises, Float64 jumps, ODE continuation, coverage, Lean, and admission open. Its `admission_label` is `pending`. It consumes the `15/16` ledger, not the `18797/20000` ledger.
4. **No matching sidecar.** The examples tree at this commit contains `examples/routeb_p5_block45_15_16_sos_lean/` and `examples/routeb_p5_block45_93_sos_lean/`. A path search finds no `18797` sidecar. Neither identity was compiled in this pass.
5. **Rational identities checked arithmetically, not in Lean.** Expanding the nine stated squares reproduces the stated symmetric matrix of `Q - (18797/20000)V` on all four diagonal entries and all five nonzero off-diagonal entries. At `z0 = (1, 25/6, 1/10, 1/6)`, the square sum equals `Q - (18797/20000)V = 49031315381/48000000000000`, and `Q - (47/50)V = -83857069/120000000000`. Expanding the seven stated squares reproduces `V - (3/125)||z||^2`. At `z1`, `V - (121/5000)||z||^2 = -49813/288000000`. `(18797/20000)/(15/16) = 18797/18750`, `(17/10)/(18797/40000) = 68000/18797`, and `4*68000*816000 = 221952000000`. These are local rational checks, not kernel proofs.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed; no 18797 or 3/125 sidecar at inspected tree
placeholder_scan: not a kernel scan
math_review_blob_18797: d2bcf4cadc96cda18f2941a742dbd48412661349
math_review_blob_3_125: 762317fb8442956d4ed97458fce36872ba8a044b
claim_blob: 8e620ee7552fd058d6c6db531d9584e88c2db389
sidecar_18797: absent
sidecar_3_125: absent
quarter_gate: 272000 L2 < 18797 stated as a hypothesis
incremental_gate: 68000 mu + 816000 nu < 18797 stated as a hypothesis
euclidean_gate: 34000 ell2 + 9792 nu < 225 stated against the 15/16 consumer
improvement_factor: 18797/18750 = (18797/20000)/(15/16), arithmetic check only
ultimate_coefficient: 68000/18797 = (17/10)/(18797/40000), arithmetic check only
nearby_obstruction_47_50: Q(z0)-(47/50)V(z0) = -83857069/120000000000
nearby_obstruction_121_5000: V(z1)-(121/5000)||z1||^2 = -49813/288000000
sos_identity_18797: local rational matrix expansion matches; not a kernel proof
storage_identity_3_125: local rational expansion matches; not a kernel proof
residual_gain_table: not exhibited
float64_incremental_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
joint_a_b_barrier: not audited; not claimed proved
```

## Obstruction

```text
identity_surface: Q-(18797/20000)V expands to nine positive-rational squares; V-(3/125)||z||^2 expands to seven positive-rational squares
coefficient_surface: M/D/K/A, 18797/20000, and 3/125 are algebraic constants, not source witnesses
sharpness_gap: neither constant is claimed optimal; 47/50 and 121/5000 are false at the stated rational points and must not be used as rounded upgrades
contract_gap: L2, mu, nu, ell2, and the half-Q residual consumer are hypotheses; no deployed residual table is exhibited
sidecar_gap: no Lean file instantiates the 18797 identity or the 3/125 adapter
coverage_gap: pairwise diameters and ||z||^2 <= 125/12 do not place the absolute cell center in a source box
calculus_gap: first-exit and ODE continuation are named and not proved
strictness_gap: a fixed absolute residual floor is not an incremental gain and cannot certify a vanishing dc^2 tube
composition_gap: the 3/125 adapter still targets the 15/16 consumer; it does not automatically retarget the 18797 ledger
obstruction_scope: missing residual/gain table, Float64/solve/controller difference semantics, center trajectory, flowpipe, and pinned Lean receipt remain failure boundaries
missing_for_parent_close:
  one same-domain incremental residual or force-normalized gain table satisfying the component contract
  a decision routing Float64/solve/controller jumps into that table or an additive branch
  an independently certified cell-center trajectory and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  a pinned Lean receipt for whichever algebraic leaf is selected
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the 18797 bridge, the 3/125 adapter, the 47/50 obstruction, or the 121/5000 obstruction
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
