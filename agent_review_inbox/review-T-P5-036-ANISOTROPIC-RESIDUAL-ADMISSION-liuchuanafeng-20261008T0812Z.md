---
kind: review_result
review_id: review-T-P5-036-ANISOTROPIC-RESIDUAL-ADMISSION-liuchuanafeng-20261008T0812Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-08T08:12:00Z
inspected_commit: 000b6ea6631643699c9e846f101920f12c71fc33
claim_commit: d31e028a28a5b9319cf5853d2622dc2408a635c9
claim_id: claim-T-P5-036-ANISOTROPIC-RESIDUAL-ADMISSION-liuchuanafeng-20261008T0811Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-036-ANISOTROPIC-RESIDUAL-ADMISSION-liuchuanafeng-20261008T0811Z.md
  - agent_review_inbox/claim-T-P5-036-guyuefangyuan-20260907T1823.md
  - agent_review_inbox/review-T-P5-036-guyuefangyuan-20260907T1906.md
  - examples/routeb_p5_block45_15_16_sos_lean/
  - examples/routeb_p5_block45_93_sos_lean/
task_id: T-P5-036
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_101_500_componentwise_reserve
---

# T-P5-036 admission audit: anisotropic residual reserve stays conditional

## Question

At the inspected tree `000b6ea6631643699c9e846f101920f12c71fc33`, does the published T-P5-036 review already supply a same-domain componentwise residual/gain table, Float64/solve/controller incremental semantics, absolute cell-center coverage, ODE continuation, a pinned Lean receipt, or registry admission for `Q >= (27/50)V + (101/500)u4^2 + (1/6)u5^2`? May the rational gate, the `303/250` directional factor, or the `203/1000` obstruction be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published child is one source-independent anisotropic identity on the frozen block-(4,5) pair. It does not close a parent gate.

古月方源 states, for the same frozen `M,D,K,A` storage used by the T-P5-035 joint lane, that

```text
Q >= (27/50)V + (101/500)(x4+y4)^2 + (1/6)(x5+y5)^2.
```

With the exact derivative hypothesis `V' = -Q - u4*l4 - u5*l5`, the two square completions give

```text
V' <= -(27/50)V + (125/101)l4^2 + (3/2)l5^2,
```

the quarter-barrier gate `25000 E4 + 30300 E5 < 2727`, and the incremental gate `6250(mu4+12 nu4) + 7575(mu5+12 nu5) < 2727`. No residual or physical gain table is exhibited. The component-4-only intercept `2727/25000` is larger than the isotropic `9/100` by exactly `303/250`; the component-5-only intercept stays `9/100`. Neither intercept is a source bound.

This is not `rejected`: the stated symmetric matrix of `R36`, its four leading principal minors, the cleared quarter gate, and `zbad^T H(203/1000) zbad = -1848397/15000000` match independent exact-rational expansion. It is not `architecture_only`: the review states an exact real inequality. It is not `compiled_candidate`: no kernel was run, and the inspected examples tree has `15/16` and `93/100` sidecars only. There is no `101/500` Lean file at this commit.

Prior authorship is preserved. This file does not overwrite 古月方源. The `203/1000` point is an obstruction to that larger diagonal coefficient, not a theorem that `101/500` is optimal outside the fixed-`u5=1/6` slice.

## Evidence

1. **Queue leaves the parent algebraic lane open.** Revision 743 names the neighbouring `T-P5-034` `15/16` SOS and `T-P5-035` `93/100` SOS as source-independent algebraic leaves that do not close real V/Q source, coverage, flowpipe, true-DH, or Lean admission. `task_queue.md` has no later owner or closure for `T-P5-036`. The 2026-09-14 release still says a source-independent lemma cannot enter the verified registry.
2. **Published review is conditional.** `review-T-P5-036-guyuefangyuan-20260907T1906.md` blob `ba86079b07478a73664ce4b1d639bcf7227d6dd1` states identity (0.1), matrix (1.2), minors (2.1), `LDL^T` pivots (2.2), completions (3.1)-(3.3), gates (4.4) and (5.4), critical diagonal endpoint (6.3), and the `203/1000` obstruction (6.8). Section 9 leaves source tables, Float64 semantics, ODE continuation, coverage, Lean, and admission explicit. Its `admission_label` is `pending`.
3. **No matching sidecar.** The examples tree at this commit contains `examples/routeb_p5_block45_15_16_sos_lean/` and `examples/routeb_p5_block45_93_sos_lean/`. A path search finds no `101/500` or componentwise T-P5-036 sidecar. The identity was not compiled in this pass.
4. **Rational identities checked arithmetically, not in Lean.** Expanding the frozen `V,Q` and subtracting `(27/50)V + (101/500)u4^2 + (1/6)u5^2` reproduces every stated entry of `H36`. The four leading principal minors match (2.1) exactly, including `Delta4 = 1399534174605692185573043249 / 14400000000000000000000000000000000`. At `zbad = (11,13,6,6)`, `zbad^T H(203/1000) zbad = -1848397/15000000`. Clearing `(125/101)E4 + (3/2)E5 < (27/50)*(1/4)` by `20200` yields `25000 E4 + 30300 E5 < 2727`. `(3/2)/(125/101) = 303/250`, and the component-5 intercept is exactly `9/100`. These are local rational checks, not kernel proofs. The stated `LDL^T` factors were not re-multiplied in this pass.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed; no 101/500 sidecar at inspected tree
placeholder_scan: not a kernel scan
math_review_blob: ba86079b07478a73664ce4b1d639bcf7227d6dd1
prior_claim_blob: 9a9a3c5d31de10c7983285e1a7c013b16b629b03
claim_blob: 10c06eadc457eda24529fbc16dfbf023f464818f
sidecar_101_500: absent
quarter_gate: 25000 E4 + 30300 E5 < 2727 stated as a hypothesis
incremental_gate: 6250(mu4+12 nu4)+7575(mu5+12 nu5) < 2727 stated as a hypothesis
directional_factor: 303/250 = (3/2)/(125/101), arithmetic check only
component5_intercept: 2727/30300 = 9/100, arithmetic check only
component4_intercept: 2727/25000, arithmetic check only
obstruction_203_1000: zbad^T H(203/1000) zbad = -1848397/15000000
matrix_identity: local rational expansion matches stated H36; not a kernel proof
leading_minors: local exact determinants match (2.1); not a kernel proof
ldl_factors: not re-multiplied this pass
residual_gain_table: not exhibited
float64_incremental_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: Q-(27/50)V-(101/500)u4^2-(1/6)u5^2 expands to the stated H36; four leading minors are positive rationals
coefficient_surface: M/D/K/A, 27/50, 101/500, and 1/6 are algebraic constants, not source witnesses
sharpness_gap: 101/500 is not claimed optimal outside the fixed-u5 slice; 203/1000 is false at zbad and must not be used as a rounded upgrade
contract_gap: E4, E5, mu4, nu4, mu5, nu5, and V' = -Q - u4*l4 - u5*l5 are hypotheses; no deployed residual table is exhibited
sidecar_gap: no Lean file instantiates the 101/500 identity or the componentwise consumer
coverage_gap: component intercepts do not place an absolute cell center in a source box
calculus_gap: first-exit and ODE continuation are named and not proved
strictness_gap: a fixed absolute residual floor is not an incremental gain and cannot certify a vanishing dc^2 tube
composition_gap: collapsing l4 and l5 before the consumer returns the older isotropic charge; anisotropy is not a source theorem
obstruction_scope: missing residual/gain table, Float64/solve/controller difference semantics, center trajectory, flowpipe, and pinned Lean receipt remain failure boundaries
missing_for_parent_close:
  one same-domain componentwise residual or force-normalized gain table satisfying the component contract
  a decision routing Float64/solve/controller jumps into that table or an additive branch
  an independently certified cell-center trajectory and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  a pinned Lean receipt for the selected algebraic leaf
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the 101/500 reserve, the 303/250 factor, or the 203/1000 obstruction
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
