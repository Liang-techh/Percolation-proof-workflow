---
kind: review_result
review_id: review-T-P5-025-ORTHANT-CONSUMER-ADMISSION-liuchuanafeng-20261007T2312Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T23:12:00Z
inspected_commit: 3df1b4611c28dc2d80a2f215d819379049d83788
prior_snapshot: 9f4d0e33eefd0e960814d63954fa4db9b53a42ea
claim_commit: 3df1b4611c28dc2d80a2f215d819379049d83788
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/claim-T-P5-025-ORTHANT-CONSUMER-ADMISSION-liuchuanafeng-20261007T2310Z.md
  - agent_review_inbox/claim-T-P5-025-liuguanyi-20260907T1004.md
  - agent_review_inbox/claim-T-P5-025-sumengchen-20260908T0620.md
  - agent_review_inbox/companion-T-P5-025-liuguanyi-20260907T1022.md
  - agent_review_inbox/review-T-P5-025-liuguanyi-20260907T1020.md
task_id: T-P5-025
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
proposed_integration_target: documentation
requested_action: preserve_the_orthant_interface_as_pending_and_do_not_collapse_K_path_or_close_P5_P8_M4
---

# T-P5-025 admission audit: orthant consumer does not close the residual tube

## Question

At inspected commit `3df1b4611c28dc2d80a2f215d819379049d83788`, does the existing `T-P5-025` math review already supply a concrete `K_path`, a source Jacobian, a certified `T-P5-023` cell/path premise, anchor-bias closure, Float64/solve semantics, P8 coverage, ODE continuation, a Lean receipt, or any source/registry admission for the block-(4,5) residual tube?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as a source-independent consumer: it keeps the nonnegative component matrix `K` visible, reduces the centered coupling envelope to at most 32 distinct sign-pair quadratic forms, and exhibits one exact one-axis certificate that is strictly sharper than the Frobenius fallback. No Lean sidecar or `review_result` from the 2026-09-08 formalization claim is present at this commit, so there is no `compiled_candidate` to cite or promote.

This is not `rejected`: the one-axis leading minors and the factor `72/49` recheck by exact rational arithmetic, and the unbridged premises are preserved. It is not `architecture_only`: the review states an exact rational inequality and a finite PSD certificate shape. It is not a new `compiled_candidate`: this agent did not compile, and no checker file exists in the inspected tree.

Prior authorship is preserved. This file does not overwrite 柳冠一 or 苏梦辰.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` at prior snapshot `9f4d0e33eefd0e960814d63954fa4db9b53a42ea` still places `T-P5-024/025` under an independent consumer harvest. It requires `K_path` to remain a typed component matrix and forbids closing P5/P8/M4 from a scalar `ell2_path` or a checker that lacks a path. The 2026-09-14 release text still says compiled candidates and source-independent lemmas cannot enter the verified registry.
2. **Math review is an interface theorem, not a witness.** `review-T-P5-025-liuguanyi-20260907T1020.md` blob `e1dc50c93f3e0f5ee2a0c7fa1d33d0164934c338` proves that a component envelope `|r_a| <= sum_k K[a,k] |z_k|` plus semidefiniteness of `mu P - sym(L^T D_tau K D_sigma)` for every sign pair implies `|(Lz)^T r| <= mu Q(z)`. Sections 6, 7, and 9 leave the actual `K_path`, the `T-P5-023` cell chain, distal coordinates, anchor bias `b`, P8 coverage, and ODE continuation open. Its `admission_label` is `pending`.
3. **Formalization claim has no receipt.** `claim-T-P5-025-sumengchen-20260908T0620.md` blob `a3e0469cb55336bd83028f7991de801813e6617f` only claims a finite-orthant Lean checker. A tree listing of `agent_review_inbox` and path search at the prior snapshot finds no `review-T-P5-025` by 苏梦辰 and no orthant sidecar. A claim is not a compile receipt.
4. **Exact arithmetic rechecks, but only the toy anisotropic layer.** Independent rational evaluation of the published leading principal minors of `(49/30)P \pm A` reproduces
   - minus: `9/40`, `3407999/16000000`, `1255633011647/1440000000000000`, `1321698458648580481847/1555200000000000000000000`;
   - plus: `89/40`, `101167997/48000000`, `9139258405266941/4320000000000000`, `3223330686008501679625847/1555200000000000000000000`.
   All eight values are positive. The comparison `(12/5)/(49/30) = 72/49` also rechecks. These identities use the single-entry envelope `K[1,1]=kappa` and do not instantiate a deployed `K_path`.
5. **Scalar fallback remains strictly weaker on that example and still conditional.** The review's Frobenius route asks `mu >= (12/5) kappa`, while the direct certificate asks `mu >= (49/30) kappa`. Neither discharges a missing state coordinate, a nonzero anchor residual, or a path premise.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed; no sidecar at inspected commit
placeholder_scan: not applicable; no Lean file inspected
math_review_blob: e1dc50c93f3e0f5ee2a0c7fa1d33d0164934c338
lean_claim_blob: a3e0469cb55336bd83028f7991de801813e6617f
lean_review_blob: absent
sidecar_blob: absent
one_axis_minors: eight leading principal minors rechecked positive
anisotropy_gap: (12/5)/(49/30)=72/49, exact recheck only
sign_pair_bound: at most 32 distinct matrices, stated only; not enumerated for a physical K
concrete_K_path: not exhibited
source_jacobian: not exhibited
cell_path_premise: not exhibited
anchor_bias: not discharged
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent orthant reduction from a nonnegative component envelope to mu*Q, consistent with the published math review
coefficient_surface: one-axis toy K permits mu >= (49/30) kappa rather than (12/5) kappa; no physical K is instantiated
contract_gap: the theorem consumes a certified K and 32 sign-pair PSD witnesses that are not exhibited
connectivity_gap: T-P5-023 cell/path transport remains an upstream premise; this consumer does not supply a connecting chain
calculus_gap: local exact-real/Float64 residual increment or Jacobian bounds remain outside the review
distal_gap: a coordinate that moves the residual while z=0 still has no finite 2x4 K
strictness_gap: the 72/49 factor only separates the toy envelope from the Frobenius fallback; it is not a physical remainder
obstruction_scope: missing source/path premises and anchor bias remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  a certified nonnegative K_path on the same first-exit domain, already in the consumed force coordinates
  exact rational PSD witnesses for the relevant sign pairs, or a valid fallback to the T-P5-024 scalar checker
  a certified connecting cell/segment chain feeding that K_path
  cell-local exact-real Jacobian/increment bounds, including Float64/solve/controller terms
  a separate anchor-bias ledger for nonzero b
  a P8 nominal flowpipe with explicit block-(4,5) margin
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a pinned Lean receipt if the claimed checker is later submitted
forbidden_this_pass:
  registry edit
  state edit
  formal proof edit
  recompile
  sidecar creation
  promotion of the interface theorem
```

## Admission

`admission_label: pending`. Integration status remains pending. `formal_certificate_allowed: false`. `registry_promoted: false`.
