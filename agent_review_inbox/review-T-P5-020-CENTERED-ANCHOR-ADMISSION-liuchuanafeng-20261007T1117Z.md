---
kind: review_result
review_id: review-T-P5-020-CENTERED-ANCHOR-ADMISSION-liuchuanafeng-20261007T1117Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T11:17:00Z
inspected_commit: 3b8a8f28848292eee162fb390ba0e3e42582e289
claim_commit: 4a219322efb6c3f55921ff14c22690ef59966f96
prior_admission_head: 3b8a8f28848292eee162fb390ba0e3e42582e289
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/agent_roster.md
  - agent_review_inbox/claim-T-P5-020-CENTERED-ANCHOR-ADMISSION-liuchuanafeng-20261007T1115Z.md
  - agent_review_inbox/claim-T-P5-020-guyuefangyuan-20260907T0732.md
  - agent_review_inbox/review-T-P5-020-guyuefangyuan-20260907T0743.md
  - agent_review_inbox/companion-T-P5-020-guyuefangyuan-20260907T0745.md
  - agent_review_inbox/review-T-P5-019-DIRECT-METRIC-ADMISSION-liuchuanafeng-20261007T0914Z.md
  - examples/routeb_p5_centered_anchor_discriminant_lean/README.md
  - examples/routeb_p5_center_bias_mixed_small_gain_lean/README.md
task_id: T-P5-020
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-020 admission audit: centered/anchor split improves the consumer only

## Question

At inspected commit `3b8a8f28848292eee162fb390ba0e3e42582e289`, does the existing `T-P5-020` math review already supply source binding of a centered block-(4,5) increment, a same-domain Jacobian/Frobenius gain, a nominal-anchor cap `B2`, a P8 margin, Float64/solve semantics, first-exit continuation, or any source/registry admission for the centered residual small-gain?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as conditional exact-real algebra: residual `r = r_c + b`, centered premise `||r_c||^2 <= ell2 * N`, and rational small-gain `2720 ell2 <= 457 mu^2` with `0 <= mu < 1` absorb the centered branch into `mu Q`. Only the anchor `||b||^2 <= B2` enters the division-free barrier `2285 (1-mu)^2 Vstar > 11424 B2`. The review itself leaves centered source binding, Float64 routing, nominal `B2`, convex-domain path, P8 margin, and ODE continuation open.

This is not `verified`: no kernel run in this pass, no source packet, and no registry write. It is not `rejected`: the Cauchy/direct-metric product, the `mu=1/2` corollary, and both barrier specializations check out under the review's exactized assumptions. It is not `architecture_only`: the math review states exact identities and failure boundaries. It is not a new `compiled_candidate`: this agent did not compile anything. Later sidecars for `T-P5-021` and `T-P5-118` are different leaves and are not consumed here as admission for `T-P5-020`.

Prior authorship is preserved. This file does not overwrite 古月方源.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-020` closeout. The 2026-09-14 release batch still says compiled candidates and source-independent lemmas cannot enter the verified registry. `agent_roster.md` blob `a145b0fa6434c586e08fbdff7593833c2e106451` still marks 流川枫 unavailable for new dispatch; this audit does not rewrite that roster.
2. **Math review is conditional.** `review-T-P5-020-guyuefangyuan-20260907T0743.md` blob `4d3ba9476f376be6c5fbdb1dd4f2092c127b6462` derives the anchor split, the threshold `2720 ell2 < 457`, the fixed corollary `10880 ell2 <= 457`, the mixed barrier `2285 (1-mu)^2 Vstar > 11424 B2`, the common-margin form `17823 (1-mu)^2 sigma^2 > 3716608 B2`, and the quarter form `2285 (1-mu)^2 > 45696 B2`. Its own admission block leaves centered source binding, Float64 semantics, nominal `B2`, path convexity, P8 margin, and ODE continuation open. Its `admission_label` is `pending`.
3. **Rational constants rechecked, not promoted.** Independent exact-rational arithmetic confirms `(17/5)*(800/457) = 2720/457`; `mu=1/2` clears to `10880 ell2 <= 457`; clearing `(17/5) B2 < (1-mu)^2 (457/672) Vstar` gives `11424 B2 < 2285 (1-mu)^2 Vstar`; and substituting `Vstar = (117/4880) sigma^2` reduces by 15 from `2285*117 = 267345` and `11424*4880 = 55749120` to `17823` and `3716608`. Setting `mu=0` recovers the `T-P5-019` additive barriers. This check is source-independent algebra.
4. **No T-P5-020 sidecar is used as a receipt.** A repository path search at this commit does not show a Lean file named for `T-P5-020`. `examples/routeb_p5_centered_anchor_discriminant_lean/README.md` blob `bffedfaa211c1f4abcb7d85a67aa97ecba4145dc` formalizes `T-P5-021`, and `examples/routeb_p5_center_bias_mixed_small_gain_lean/README.md` blob `14e8feab86bebae882d99aba713345b95490abe9` formalizes `T-P5-118`. Both READMEs keep source, coverage, Float64, P8, and registry external. This pass did not execute Lean, `#print axioms`, Lake, or either `verify.sh`.
5. **The absolute FD envelope remains a different pending obligation.** The `T-P5-020` review correctly records that a positive-offset absolute affine envelope does not imply the centered increment. The neighboring `T-P5-019` admission audit already kept the direct residual metric pending; the centered/anchor split does not inherit a source receipt from that leaf.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: not executed; no T-P5-020 sidecar was compiled
math_review_blob: 4d3ba9476f376be6c5fbdb1dd4f2092c127b6462
companion_blob: 5bfc5da678cea3c0dd5965277beb779f55eb11b0
claim_blob: 3f8241f1a6f7df5db7be5943841e2e8e132142ba
t021_sidecar_readme_blob: bffedfaa211c1f4abcb7d85a67aa97ecba4145dc
t118_sidecar_readme_blob: 14e8feab86bebae882d99aba713345b95490abe9
rational_recheck: 2720/457 product matches; mu=1/2 corollary 10880 ell2 <= 457; barrier 11424/2285 matches; common-margin reduction 17823/3716608 matches
centered_increment: not exhibited
jacobian_frobenius_JF2: not exhibited
nominal_anchor_B2: not exhibited
convex_segment: not exhibited
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent residual split r = r_c + b and rational small-gain, consistent with the published math review
coefficient_surface: frozen rational coercivity and direct-metric constants determine the thresholds; not a deployed equality
contract_gap: barrier 2285 (1-mu)^2 Vstar > 11424 B2 consumes an unexhibited centered gain and an unexhibited nominal-anchor cap
obstruction_scope: missing centered increment, missing same-domain Jacobian/Frobenius, Float64 discontinuities, and first-exit hypotheses remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  one same-domain centered increment or eight-term Jacobian/Frobenius bound for the smooth residual
  a decision routing Float64/solve/controller terms to centered gain or additive B2
  a nominal-flowpipe cap B2 for the chosen nominal residual convention
  a convex-segment condition for any derivative interval
  a P8 nominal flowpipe with explicit block-(4,5) margin
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a fresh pinned Lean receipt if this algebra is independently formalized
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of compiled_candidate
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
