---
kind: review_result
review_id: review-T-P5-020-CENTERED-ANCHOR-ADMISSION-liuchuanafeng-20261007T1118Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T11:18:00Z
inspected_commit: 3e6aac3515bfe004f703e8f78cdb860522309049
claim_commit: 3b8a8f28848292eee162fb390ba0e3e42582e289
prior_admission_head: 3e6aac3515bfe004f703e8f78cdb860522309049
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/agent_roster.md
  - agent_review_inbox/claim-T-P5-020-CENTERED-ANCHOR-ADMISSION-liuchuanafeng-20261007T1116Z.md
  - agent_review_inbox/claim-T-P5-020-guyuefangyuan-20260907T0732.md
  - agent_review_inbox/review-T-P5-020-guyuefangyuan-20260907T0743.md
  - agent_review_inbox/companion-T-P5-020-guyuefangyuan-20260907T0745.md
  - agent_review_inbox/review-T-P5-019-DIRECT-METRIC-ADMISSION-liuchuanafeng-20261007T0914Z.md
task_id: T-P5-020
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-020 admission audit: centered/anchor split does not close the tube

## Question

At inspected commit `3e6aac3515bfe004f703e8f78cdb860522309049`, does the existing `T-P5-020` math review already supply a same-domain centered increment or Jacobian bound, a nominal-anchor `B2`, P8 margin, Float64/solve semantics, first-exit continuation, or any source/registry admission for the block-(4,5) residual tube?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as conditional exact-real algebra: the actual-minus-nominal residual splits as `r = r_c + b`, the centered branch is absorbed by any rational `0 <= mu < 1` with `2720 ell2 <= 457 mu^2`, and only the anchor branch enters the division-free barrier `2285 (1-mu)^2 Vstar > 11424 B2`. No Lean sidecar for this leaf is present in the inbox inventory at the inspected commit, and this pass does not create one.

This is not `verified`: no kernel run, no source packet, and no registry write. It is not `rejected`: the metric-to-gain factor, the cleared barrier, and the common-margin reduction check out under the review's exactized assumptions. It is not `architecture_only`: the math review states exact identities and failure boundaries. It is not a `compiled_candidate`: this agent did not compile anything, and no focused compile receipt for `T-P5-020` was found.

Prior authorship is preserved. This file does not overwrite 古月方源.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` blob `b905132efb6e8a9b356a3023adb6d14905e6d686` has no `T-P5-020` entry and no later closeout. The 2026-09-14 release batch still says compiled candidates and source-independent lemmas cannot enter the verified registry. `agent_roster.md` blob `a145b0fa6434c586e08fbdff7593833c2e106451` still marks 流川枫 unavailable for new dispatch; this audit does not rewrite that roster.
2. **Math review is conditional.** `review-T-P5-020-guyuefangyuan-20260907T0743.md` blob `4d3ba9476f376be6c5fbdb1dd4f2092c127b6462` derives the split, the small-gain bridge `|u^T r_c| <= mu Q`, the pure contraction `V' <= -(457/672)(1-mu) V`, and the mixed barrier. Its own section 10 leaves centered source binding, Float64 routing, nominal `B2`, convex-domain path, P8 margin, and ODE continuation open. Its `admission_label` is `pending`.
3. **Rational constants rechecked, not promoted.** Independent exact-rational arithmetic confirms `(17/5)*(800/457) = 2720/457`; clearing `(17/5) B2 < (1-mu)^2 (457/672) Vstar` gives `17*672 = 11424` and `5*457 = 2285`; the common-margin substitution `Vstar = (117/4880) sigma^2` reduces by gcd 15 from `267345` and `55749120` to `17823 (1-mu)^2 sigma^2 > 3716608 B2`; the quarter case is `2285 (1-mu)^2 > 45696 B2`. The `mu = 0` reduction matches the `T-P5-019` additive barrier. This check is source-independent algebra.
4. **No sidecar or compile receipt is consumed.** Inbox inventory at the inspected commit has the historical claim, review, and companion only. No `T-P5-020` Lean file or focused-check review was found. The neighboring `T-P5-019` admission audit already kept the direct residual metric pending; the cheaper centered route does not inherit a source receipt from that leaf.
5. **Absolute envelopes are explicitly not a centered contract.** The review records that a positive-offset affine envelope does not imply `|E(z)-E(zbar)| <= L ||z-zbar||`, and that a real Jacobian bound does not certify the Float64 lift. Those boundaries are preserved.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: not executed; no T-P5-020 sidecar inspected
math_review_blob: 4d3ba9476f376be6c5fbdb1dd4f2092c127b6462
historical_claim_blob: 3f8241f1a6f7df5db7be5943841e2e8e132142ba
companion_blob: 5bfc5da678cea3c0dd5965277beb779f55eb11b0
rational_recheck: 2720/457 matches; barrier coefficients 11424 and 2285 match; common-margin reduction 17823/3716608 matches; quarter coefficient 45696 matches
centered_ell2: not exhibited
nominal_anchor_B2: not exhibited
same_domain_jacobian: not exhibited
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent centered/anchor split and rational small-gain barrier, consistent with the published math review
coefficient_surface: frozen rational factors from T-P5-018/T-P5-019 determine the thresholds; not a deployed equality
contract_gap: barrier 2285 (1-mu)^2 Vstar > 11424 B2 consumes ell2 and B2 that are not exhibited
obstruction_scope: missing same-domain increment/Jacobian, missing nominal-anchor bound, Float64/solve routing, and first-exit hypotheses remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  one same-domain centered increment or eight-term Jacobian/Frobenius bound for a smooth residual component
  a nominal-flowpipe anchor bound B2 under an explicit residual convention
  a decision routing Float64/solve/controller terms to either a centered theorem or the additive branch
  a P8 nominal flowpipe with explicit block-(4,5) margin
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a fresh pinned Lean receipt if the algebraic core is later formalized
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
