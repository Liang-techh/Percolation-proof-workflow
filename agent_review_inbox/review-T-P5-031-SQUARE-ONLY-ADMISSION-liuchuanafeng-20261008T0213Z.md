---
kind: review_result
review_id: review-T-P5-031-SQUARE-ONLY-ADMISSION-liuchuanafeng-20261008T0213Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-08T02:13:00Z
inspected_commit: 1ebafdac627f37c0e90a277c6f8722c4139f650f
claim_commit: f9449d8397b2404b1394903765b300b5440680dc
claim_id: claim-T-P5-031-SQUARE-ONLY-ADMISSION-liuchuanafeng-20261008T0211Z
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/claim-T-P5-031-guyuefangyuan-20260907T1222.md
  - agent_review_inbox/review-T-P5-031-guyuefangyuan-20260907T1224.md
  - agent_review_inbox/companion-T-P5-031-guyuefangyuan-20260907T1225.md
  - agent_review_inbox/claim-T-P5-031-juyangxianzun-20260907T1228.md
  - agent_review_inbox/review-T-P5-031-juyangxianzun-20260907T1251.md
  - examples/routeb_p5_physical_gain_parameter_tube_lean/P5PhysicalGainParameterTube.lean
task_id: T-P5-031
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: harvest_pending_admission_audit_do_not_promote_square_only_bridge_or_sidecar
---

# T-P5-031 admission audit: square-only gain bridge stays conditional

## Question

At the inspected tree `1ebafdac627f37c0e90a277c6f8722c4139f650f`, do the published T-P5-031 math review, companion, and `P5PhysicalGainParameterTube.lean` already supply a same-domain force-normalized physical gain table, Float64/solve/controller incremental semantics, absolute cell-center coverage, ODE continuation, or registry admission for the moving-frame parameter tube? May the rational gate `11424*(U+p)+137088*(W+q)<2285`, or the historical `compiled_candidate` label, be promoted?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The math review is an exact source-independent bridge: if nonnegative physical component gains exist, moving-frame endpoint bounds transport them to `U,W`, and any slack pair with `p*q >= U*W` yields `||Dl||^2 <= (U+p)*Vd + (W+q)*dc^2`. The integer necessity factor `4*11424*137088 = 6264373248` matches the stated diagnostic. No gain table is exhibited. The Lean sidecar states the same interface and is already labeled `compiled_candidate` by 巨阳仙尊; this pass did not recompile it and does not inherit that label as a new receipt.

This is not `rejected`: the square identity `(p*Vd - q*dc^2)^2 + 4*dc^2*(p*q*Vd - C^2) >= 0` is a valid division-free cross-term absorption under the stated nonnegativity hypotheses, and the sidecar header refuses source and registry closure. It is not `architecture_only`: both artifacts state exact real inequalities. It is not a fresh `compiled_candidate`: no kernel was run in this pass.

Prior authorship is preserved. This file does not overwrite 古月方源 or 巨阳仙尊.

## Evidence

1. **Queue leaves the child open.** `agent_review_inbox/task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` records the harvested T-P5-031 reduction from physical incremental gains to a square-only bridge, and the 2026-09-14 release still says a source-independent lemma or compiled candidate cannot enter the verified registry.
2. **Math review is conditional.** `review-T-P5-031-guyuefangyuan-20260907T1224.md` blob `188c5340e2d89931dea6c392f9b8cbaf7868ff75` states the contract `|Dl_a| <= sum k[a,*]*|d state|`, the endpoint bounds `A4=21912800/75672601`, `A5=15007200/75672601`, the assignment `mu=U+p`, `nu=W+q`, and the gate `11424*(U+p)+137088*(W+q)<2285`. Section 9 leaves the gain table, extra mechanical coordinates, Float64 semantics, center trajectory, and ODE first-exit explicit. Its `admission_label` is `pending`.
3. **Companion does not close the parent.** `companion-T-P5-031-guyuefangyuan-20260907T1225.md` blob `dceb946242705d1d6255b7489580674167875637` repeats the same checker-facing inequalities and keeps `admission_label: pending`.
4. **Sidecar matches the interface, not the source.** `examples/routeb_p5_physical_gain_parameter_tube_lean/P5PhysicalGainParameterTube.lean` blob `d0dddc11fea89b991980d200605fc65c7fb03adb` defines `moving_frame_a4_endpoint_bound`, `moving_frame_a5_endpoint_bound`, `four_term_square`, `component_physical_gain_transport`, `product_slack_cross_bound`, `physical_gain_to_mu_nu_envelope`, `parameter_tube_gain_gate`, `slack_feasibility_necessity`, and `exact_feasibility_factor`. A text scan finds no `sorry`. The header says it does not supply the gain table, bind Float64 execution, prove P8 coverage or ODE continuation, or perform final integration. The file contains `#print axioms` lines; they were not executed.
5. **Historical Lean review is not re-certified here.** `review-T-P5-031-juyangxianzun-20260907T1251.md` blob `5240a16a8961ceaa1844751588124b6056abe9aa` reports CI run `34152839072` / job `101838555450`, `AXIOM_AUDIT=PASS`, and `admission_label: compiled_candidate`, while keeping `SOURCE_PHYSICAL_GAIN_TABLE=OPEN` and `REGISTRY_MUTATION=false`. This audit does not re-run that workflow and does not treat the cited log as a new kernel receipt.
6. **Integer factor checked arithmetically, not in Lean.** `4*11424*137088 = 6264373248` agrees with both reviews and `exact_feasibility_factor`. This is a local integer check, not a kernel proof.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: text scan only; sidecar blob contains no sorry; not a kernel scan
math_review_blob: 188c5340e2d89931dea6c392f9b8cbaf7868ff75
companion_blob: dceb946242705d1d6255b7489580674167875637
lean_review_blob: 5240a16a8961ceaa1844751588124b6056abe9aa
lean_claim_blob: e082607437e8e911d1f84ad1e858e27a421040ea
sidecar_blob: d0dddc11fea89b991980d200605fc65c7fb03adb
task_queue_blob: b905132efb6e8a9b356a3023adb6d14905e6d686
tube_gate: 11424*(U+p)+137088*(W+q)<2285 stated as a hypothesis
feasibility_factor: 6264373248 = 4*11424*137088, arithmetic check only
physical_gain_table: not exhibited
float64_incremental_semantics: not exhibited
cell_center_inclusion: not exhibited
ode_continuation: not exhibited
sidecar_matches_source_gain: false
```

## Obstruction

```text
identity_surface: moving-frame offsets fold into G_a*|dc|; cross term absorbed by p*q >= U*W without division
coefficient_surface: A4/A5/h4/h5 and 11424/137088/2285 are algebraic constants, not source witnesses
contract_gap: k[a,q4], k[a,q5], k[a,v4], k[a,v5], k[a,w], k[a,c] are hypotheses; no deployed table is exhibited
extra_coordinate_gap: other mechanical coordinates that affect Dl are not silently eliminated
sidecar_gap: P5PhysicalGainParameterTube.lean proves the interface; it does not instantiate U, W, p, q from source
coverage_gap: pairwise diameters do not place the absolute cell center in a source box
calculus_gap: first-exit and ODE continuation are named and not proved
strictness_gap: a fixed absolute residual floor is not an incremental gain and cannot certify a vanishing dc^2 tube
obstruction_scope: missing physical gain table, Float64/solve/controller difference semantics, center trajectory, and flowpipe remain failure boundaries
missing_for_parent_close:
  one same-domain force-normalized incremental gain table satisfying the component contract
  a decision routing Float64/solve/controller jumps into that table or an additive branch
  an independently certified cell-center trajectory and absolute source-domain inclusion
  a first-exit / ODE existence-continuation theorem on the actual pair
  a fresh pinned Lean receipt if the historical compiled_candidate is to be re-certified
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar edit
  promotion of the square-only bridge or the historical compiled_candidate
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
