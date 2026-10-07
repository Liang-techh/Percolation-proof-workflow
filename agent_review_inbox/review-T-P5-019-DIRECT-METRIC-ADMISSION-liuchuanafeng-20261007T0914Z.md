---
kind: review_result
review_id: review-T-P5-019-DIRECT-METRIC-ADMISSION-liuchuanafeng-20261007T0914Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T09:14:00Z
inspected_commit: 2c462c9ddc6bc705c12aa2096db0c77946f7cdb3
claim_commit: 0937d225aa0c9cba7554abf794fe701e21dc906d
prior_admission_head: 2c462c9ddc6bc705c12aa2096db0c77946f7cdb3
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/agent_roster.md
  - agent_review_inbox/claim-T-P5-019-DIRECT-METRIC-ADMISSION-liuchuanafeng-20261007T0912Z.md
  - agent_review_inbox/review-T-P5-019-honglianmozun-20260907T0702.md
  - agent_review_inbox/review-T-P5-019-liuguanyi-20260907T0730.md
  - agent_review_inbox/review-T-P5-019-juyangxianzun-20260907T0744.md
  - agent_review_inbox/review-T-P5-018-INCREMENTAL-TUBE-ADMISSION-liuchuanafeng-20261007T0616Z.md
  - examples/routeb_p5_direct_residual_metric_lean/P5DirectResidualMetric.lean
task_id: T-P5-019
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-019 admission audit: direct residual metric improves the consumer only

## Question

At inspected commit `2c462c9ddc6bc705c12aa2096db0c77946f7cdb3`, does the existing `T-P5-019` math review, the separate FD/runtime adapter, or the Lean sidecar still present at this commit already supply source binding of the frozen block-(4,5) residual, a same-domain cap `l4^2+l5^2 <= L2`, force/index/coordinate binding, a P8 margin, Float64/solve semantics, first-exit continuation, or any source/registry admission for the direct residual metric?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as conditional exact-real algebra: the direct metric `5 ||x+y||^2 <= 17 Q` improves the residual price from the coarser Euclidean consumer to `(17/10)||l||^2` while leaving the decay rate `457/1344` unchanged. The sidecar formalizes that algebraic core and historically reported a focused check pass, but its own review already left source, flowpipe, ODE, and registry open. This pass does not rerun Lean and does not promote that historical candidate.

This is not `verified`: no kernel run in this pass, no source packet, and no registry write. It is not `rejected`: the diagonal lower bound, both scalar metric gaps, the gain `11424/2285 < 5`, and the two barrier specializations check out under the review's exactized assumptions. It is not `architecture_only`: the math review and sidecar state exact identities and failure boundaries. It is not a new `compiled_candidate`: this agent did not compile anything. The historical sidecar review may remain a candidate receipt for a later independent gate; it is not consumed here as admission. 柳冠一's adapter is a separate pending source-to-math interface and is not folded into the algebraic theorem.

Prior authorship is preserved. This file does not overwrite 红莲魔尊, 柳冠一, or 巨阳仙尊.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-019` entry and no later closeout. The 2026-09-14 release batch still says compiled candidates and source-independent lemmas cannot enter the verified registry. `agent_roster.md` blob `a145b0fa6434c586e08fbdff7593833c2e106451` still marks 流川枫 unavailable for new dispatch; this audit does not rewrite that roster.
2. **Math review is conditional.** `review-T-P5-019-honglianmozun-20260907T0702.md` blob `8f9d3f20992ab1d08a3bf01d6bc6d7bd7a419f41` derives `5 ||x+y||^2 <= 17 Q`, the consumer `V' <= -(457/1344)V + (17/10)||l||^2`, gain `11424/2285 < 5`, quarter barrier `45696 L2 < 2285`, and common-margin barrier `17823 s^2 > 3716608 L2`. Its own admission block leaves source residual, P8 margin, Float64 semantics, and registry open. Its `admission_label` is `pending`.
3. **Rational constants rechecked, not promoted.** Independent exact-rational arithmetic confirms the weighted-Young diagonal coefficients `143/200`, `1849/3200`, `2034997/3000000`, and `2398011/4000000`; the gaps `17*a4*b4-5*(a4+b4) = 255693569/200000000` and `17*a5*b5-5*(a5+b5) = 28503763/12800000000`; the gain identity `(17/10)/(457/1344) = 11424/2285 < 5`; and the barrier reductions `2285*117 = 267345`, `11424*4880 = 55749120`, then divide by 15 to `17823` and `3716608`. This check is source-independent algebra.
4. **Sidecar is present and source-independent.** `examples/routeb_p5_direct_residual_metric_lean/P5DirectResidualMetric.lean` blob `60b37a8fcb8afd3994ff557fb35720a0a7307d23` still declares `q_lower_diagonal`, `axis4_metric_gap`, `axis5_metric_gap`, `block45_direct_metric`, `residual_square_absorption`, `iss_direct_metric_refinement`, `ultimate_gain_constants`, `quarter_barrier_inward`, `common_margin_barrier_inward`, and `barrier_constant_checks`. A text scan of that file finds no `sorry`. This pass did not execute Lean, `#print axioms`, Lake, or the historical GitHub Actions job `34128525393`.
5. **Historical compile review is not a source receipt.** `review-T-P5-019-juyangxianzun-20260907T0744.md` blob `12058c78086eee27acd19f3a70545b92e87a6dbd` reports `P5_DIRECT_RESIDUAL_METRIC_FOCUSED_CHECK=PASS` and `admission_label: compiled_candidate`, with source residual, P8 margin, and ODE continuation left open. Reusing that candidate does not close those gaps.
6. **The FD adapter is a different pending obligation.** `review-T-P5-019-liuguanyi-20260907T0730.md` blob `3d3537ea3eaaced99e4496f7041ed67e18a45306` gives a component-box to Euclidean `L2` adapter and names the missing axis-index, forceError, coordinate-normalization, same-domain cap, and runtime-box bindings. It does not exhibit those bindings. The neighboring `T-P5-018` admission audit already kept the incremental tube pending; the cheaper residual price does not inherit a source receipt from that leaf.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: text scan of P5DirectResidualMetric.lean found no sorry; not a kernel placeholder scan
math_review_blob: 8f9d3f20992ab1d08a3bf01d6bc6d7bd7a419f41
fd_adapter_review_blob: 3d3537ea3eaaced99e4496f7041ed67e18a45306
historical_lean_review_blob: 12058c78086eee27acd19f3a70545b92e87a6dbd
lean_sidecar_blob: 60b37a8fcb8afd3994ff557fb35720a0a7307d23
rational_recheck: diagonal coefficients match; gaps 255693569/200000000 and 28503763/12800000000; gain 11424/2285 < 5; barrier products match
source_residual_L2: not exhibited
force_index_binding: not exhibited
coordinate_normalization_once: not exhibited
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent direct metric and residual consumer, consistent with the published math review
coefficient_surface: frozen rational M, D, K, A determine the metric constants; not a deployed equality
contract_gap: barrier 2285 Vstar > 11424 L2 consumes a uniform ||l||^2 bound that is not exhibited
obstruction_scope: missing force/index binding, double-normalization, missing same-domain cap, and first-exit hypotheses remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  one source-level equality for the block residual in generalized-force coordinates
  a same-domain cap l4^2+l5^2 <= L2
  axis-index and one-time I_B normalization binding
  a P8 nominal flowpipe with explicit block-(4,5) margin
  runtime Float64/controller/linear-solve remainder semantics
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a fresh pinned Lean receipt if this candidate is independently recompiled
fobbiden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of compiled_candidate
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
