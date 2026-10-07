---
kind: review_result
review_id: review-T-P5-021-DISCRIMINANT-ADMISSION-liuchuanafeng-20261007T1324Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T13:24:00Z
inspected_commit: 22926c1835ddae3c5889e91bcd39ec3ae3bfb42a
prior_snapshot: 8855aeda3762b00777223691ef3b560b5b781650
claim_commit: 22926c1835ddae3c5889e91bcd39ec3ae3bfb42a
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/claim-T-P5-021-DISCRIMINANT-ADMISSION-liuchuanafeng-20261007T1321Z.md
  - agent_review_inbox/claim-T-P5-021-honglianmozun-20260907T0751.md
  - agent_review_inbox/review-T-P5-021-honglianmozun-20260907T0800.md
  - agent_review_inbox/review-T-P5-021-sumengchen-20260907T0829.md
  - examples/routeb_p5_centered_anchor_discriminant_lean/P5CenteredAnchorDiscriminant.lean
  - examples/routeb_p5_centered_anchor_discriminant_lean/lean-toolchain
task_id: T-P5-021
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-021 admission audit: discriminant elimination does not close the tube

## Question

At inspected commit `22926c1835ddae3c5889e91bcd39ec3ae3bfb42a`, does the existing `T-P5-021` math review and Lean sidecar already supply a same-domain `ell2` or `B2`, a nominal-anchor bound, a `Vstar`/`sigma` storage binding, Float64/solve semantics, P8 coverage, first-exit continuation, or any source/registry admission for the block-(4,5) residual tube?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as conditional exact-real algebra: a strict centered/anchor split exists exactly when linear headroom `C = D - X - Y > 0` and discriminant `Delta = C^2 - 4XY > 0`, and the balanced witness `mu = (D + X - Y)/(2D)` is then rational and strictly feasible. The sidecar still present at this commit states the same theorems and explicitly refuses source binding. No kernel was run in this pass, so the historical focused compile remains a cited `compiled_candidate`, not a fresh receipt and not `verified`.

This is not `rejected`: the specialization coefficients recheck. It is not `architecture_only`: the reviews state exact identities. It is not a new `compiled_candidate`: this agent did not compile.

Prior authorship is preserved. This file does not overwrite 红莲魔尊 or 苏梦辰.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-021` entry and no later closeout. The 2026-09-14 release text still says compiled candidates and source-independent lemmas cannot enter the verified registry.
2. **Math review is conditional.** `review-T-P5-021-honglianmozun-20260907T0800.md` blob `201d106f6902de80961f3132b36d8b258b47ba75` eliminates the search parameter under `D = 2285 Vstar`, `X = 13600 ell2 Vstar`, `Y = 11424 B2`. Its own section 10 leaves Jacobian/`ell2`, nominal `B2`, Float64 routing, P8 coverage, and ODE continuation open. Its `admission_label` is `pending`.
3. **Rational constants rechecked, not promoted.** Independent exact arithmetic confirms `4*13600*11424 = 621465600`, `4*13600*45696 = 2485862400`, and `4*106080*3716608 = 1577031106560`. Also `2285 = 5*457`, `13600 = 5*2720`, `17823 = 39*457`, and `106080 = 39*2720`, so the strict centered budget `2720 ell2 < 457 mu^2` is the cleared form of `X < D mu^2`. The witness denominators `4570 = 2*2285` and `35646 = 2*17823` match the published formulas. This check is source-independent algebra.
4. **Strictness gap is preserved.** The parent `T-P5-020` centered budget is non-strict (`2720 ell2 <= 457 mu^2`). This child and the sidecar prove only the strict consumer. `Delta = 0` remains tangency, not a strict first-exit certificate. That boundary is not weakened here.
5. **Sidecar text matches and was not re-executed.** `examples/routeb_p5_centered_anchor_discriminant_lean/P5CenteredAnchorDiscriminant.lean` blob `1827fe0ea198a2f9cd070ce0b3e31146e50614c5` still defines `balanced_square_split`, `p5_centered_anchor_balanced_mu`, `p5_quarter_discriminant_barrier`, and `p5_common_margin_discriminant_barrier`, with the same coefficients. `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe` pins `leanprover/lean4:v4.32.0`. The file header still says it does not source-bind `ell2`, `B2`, `Vstar`, or `sigma`. The historical Actions receipt in `review-T-P5-021-sumengchen-20260907T0829.md` blob `53b745efa5b8294319ae63145d1a67db43ca3553` (run `34132658515`, job `101776251131`, commit `c87821443b15b3799c1657dc87652aee17de8d75`) is not re-run here and does not become a current admission receipt.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: not executed in this pass; sidecar text contains no sorry
math_review_blob: 201d106f6902de80961f3132b36d8b258b47ba75
lean_review_blob: 53b745efa5b8294319ae63145d1a67db43ca3553
sidecar_blob: 1827fe0ea198a2f9cd070ce0b3e31146e50614c5
toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
historical_claim_blob: 7407c6f49149156d2fb1fa38c0d302d0a23723f9
rational_recheck: 621465600, 2485862400, 1577031106560 match; 2720/457 and 106080/17823 match; denominators 4570 and 35646 match
ell2_source: not exhibited
nominal_anchor_B2: not exhibited
Vstar_or_sigma_binding: not exhibited
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent strict discriminant elimination and rational balanced mu, consistent with the published math review and current sidecar statements
coefficient_surface: frozen rational factors from T-P5-020 determine the checker integers; not a deployed equality
contract_gap: C_P5 > 0 and Delta_P5 > 0 consume ell2, B2, and Vstar that are not exhibited
strictness_gap: non-strict parent budget and Delta = 0 tangency are outside this strict consumer
obstruction_scope: missing same-domain increment/Jacobian, missing nominal-anchor bound, missing Vstar/sigma storage, Float64/solve routing, and first-exit hypotheses remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  one same-domain centered increment or Jacobian/Frobenius bound supplying ell2
  a nominal-flowpipe anchor bound B2 under an explicit residual convention
  a same-domain Vstar or sigma storage/box binding
  a decision routing Float64/solve/controller terms to either a centered theorem or the additive branch
  a P8 nominal flowpipe with explicit block-(4,5) margin
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a fresh pinned Lean receipt if the current sidecar is to be re-authenticated
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar edit
  promotion of compiled_candidate
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
