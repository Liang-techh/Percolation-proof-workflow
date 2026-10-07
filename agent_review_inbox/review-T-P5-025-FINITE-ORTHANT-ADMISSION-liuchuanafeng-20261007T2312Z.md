---
kind: review_result
review_id: review-T-P5-025-FINITE-ORTHANT-ADMISSION-liuchuanafeng-20261007T2312Z
source_agent: 流川枫
agent: 流川枫
created_at: 2026-10-07T23:12:00Z
inspected_commit: 9f4d0e33eefd0e960814d63954fa4db9b53a42ea
prior_snapshot: 9f4d0e33eefd0e960814d63954fa4db9b53a42ea
claim_commit: 6b1e5bc1734e80514e67842ddedb7ac0d6ee06d0
inspected_paths:
  - agent_review_inbox/task_queue.md
  - agent_review_inbox/README.md
  - agent_review_inbox/claim-T-P5-025-FINITE-ORTHANT-ADMISSION-liuchuanafeng-20261007T2310Z.md
  - agent_review_inbox/claim-T-P5-025-liuguanyi-20260907T1004.md
  - agent_review_inbox/claim-T-P5-025-sumengchen-20260908T0620.md
  - agent_review_inbox/review-T-P5-025-liuguanyi-20260907T1020.md
  - examples/routeb_p5_finite_orthant_kpath_lean/FiniteOrthantKPath.lean
  - examples/routeb_p5_finite_orthant_kpath_lean/README.md
  - examples/routeb_p5_finite_orthant_kpath_lean/lean-toolchain
task_id: T-P5-025
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P5-025 admission audit: finite-orthant consumer does not supply a path or source witness

## Question

At inspected commit `9f4d0e33eefd0e960814d63954fa4db9b53a42ea`, does the existing `T-P5-025` math review and Lean sidecar already supply a deployed nonnegative `K_path`, a certified connecting path, source/Float64 residual binding, anchor-bias closure, P8 coverage, ODE continuation, or any source/registry admission for the block-(4,5) residual tube? May the finite orthant checker, or the stated `72/49` toy improvement over `ell2_path`, be promoted beyond a conditional interface?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The published interface is internally consistent as a source-independent consumer: it keeps a typed `2 x 4` gain table, derives `|Lz|^T K |z|` without a Frobenius collapse, and reduces the centered power bound to a finite family of directional quadratic inequalities. The sidecar still present at this commit states that seam and explicitly refuses a concrete `K_path`. No kernel was run in this pass, so the sidecar is not a fresh `compiled_candidate` and is not `verified`.

This is not `rejected`: the sign-count reduction `64 -> 32` and the factor `(12/5)/(49/30) = 72/49` recheck as text, and the source boundary is preserved. It is not `architecture_only`: the math review states an exact rational small-gain theorem under explicit premises. It is not a new `compiled_candidate`: this agent did not compile, and no 苏梦辰 `review_result` receipt for this sidecar was found in the inbox at the inspected commit. Queue text already forbids closing P5/P8/M4 from a scalar `ell2_path` or a checker that lacks a path; this audit does not lift that limit.

Prior authorship is preserved. This file does not overwrite 柳冠一 or 苏梦辰.

## Evidence

1. **Queue does not close the leaf.** `agent_review_inbox/task_queue.md` at snapshot `9f4d0e33eefd0e960814d63954fa4db9b53a42ea` says P5-025 continues the finite orthant sign reduction and must keep `K_path` as a typed component matrix. A scalar `ell2_path` or a checker without a path must not close P5/P8/M4. The 2026-09-14 release text still says compiled candidates and source-independent lemmas cannot enter the verified registry.
2. **Math review is a consumer theorem, not a witness.** `review-T-P5-025-liuguanyi-20260907T1020.md` blob `e1dc50c93f3e0f5ee2a0c7fa1d33d0164934c338` assumes a nonnegative table `K` with `|r_a| <= sum_k K[a,k] |z_k|` and `mu P - B_{sigma,tau}` positive semidefinite on at most 32 distinct sign pairs, then concludes `|(Lz)^T r| <= mu Q(z)`. Its one-axis example states `mu >= (49/30) kappa` against the scalar fallback `mu >= (12/5) kappa`, hence a factor `72/49`. Sections 7 and 9 leave the `T-P5-023` cell chain, distal coordinates, anchor bias `b`, P8 coverage, and ODE continuation open. Its `admission_label` is `pending`.
3. **Sidecar text matches the algebraic seam and was not executed.** `examples/routeb_p5_finite_orthant_kpath_lean/FiniteOrthantKPath.lean` blob `cea5129ea17983bc31c08002199ee11aaf3ed516` defines `Gain24`, `ForceResidual45`, `qDissipation`, and the theorems `component_envelope_power_bound`, `exists_boolSign_mul_eq_abs`, `orthant_support_eq_direct_support_of_signs`, `exists_orthant_support_eq_direct_support`, `orthant_quadratic_small_gain`, `orthant_support_global_reversal`, and `nonnegative_gain_is_explicit_interface`. `OrthantSmallGainCertificate` is a hypothesis over six `Bool` selectors, not a discharged PSD witness. A text scan of this blob finds no `sorry`. `lean-toolchain` blob `94b9f495baff80fd9cb44aad8f4762cb3b2066fe` pins `leanprover/lean4:v4.32.0`. The README blob `4dcc3630ca963d6531d87eb9ea96665a7d4d187d` says status is `compiled_candidate` only after a real focused CI pass, and that even then admission remains open. No such pass is cited here.
4. **The sharper toy constant is not in the sidecar.** The Lean file does not define `block45_one_axis_direct_certificate`, the matrix `A` of `x4(x4+y4)`, the leading-minor list, or the factor `72/49`. Those remain prose in the math review.
5. **The certificate does not instantiate `K_path`.** `orthant_quadratic_small_gain` consumes channel bounds and `OrthantSmallGainCertificate K mu`. It does not define a path table, a force tag, a cell chain, or the raw scales `1/5` and `1/10`. `Gain24.Nonnegative` is an explicit interface and is not used by the power theorem.

## Receipt

```text
command: not run
exit_code: not claimed
axiom_print: not executed in this pass
placeholder_scan: text scan only; sidecar blob contains no sorry; not a kernel scan
math_review_blob: e1dc50c93f3e0f5ee2a0c7fa1d33d0164934c338
math_claim_blob: 6fa5714e8968909137d21a43d51e543521e7ab98
lean_claim_blob: a3e0469cb55336bd83028f7991de801813e6617f
lean_review_blob: not found in inbox at inspected commit
sidecar_blob: cea5129ea17983bc31c08002199ee11aaf3ed516
sidecar_readme_blob: 4dcc3630ca963d6531d87eb9ea96665a7d4d187d
toolchain_blob: 94b9f495baff80fd9cb44aad8f4762cb3b2066fe
orthant_count: 2^4 * 2^2 = 64 stated; global reversal leaves at most 32 distinct forms
toy_factor: (12/5)/(49/30) = 72/49 stated in math review only; not re-proved in a kernel
ell2_fallback: 144*ell2 <= 25*mu^2 remains the T-P5-024 scalar route, not discharged here
K_path: not exhibited
connecting_cell_chain: not exhibited
force_coordinate_tag: not exhibited
anchor_bias: not exhibited
P8_margin: not exhibited
float64_solve_semantics: not exhibited
ode_continuation: not exhibited
```

## Obstruction

```text
identity_surface: source-independent finite-orthant consumer |residualPower| <= mu * qDissipation under channel envelopes and OrthantSmallGainCertificate, consistent with the published math review and current sidecar statements
coefficient_surface: toy one-axis improvement 72/49 over the Frobenius fallback is stated in prose; the sidecar does not discharge it
contract_gap: orthant_quadratic_small_gain consumes K, channel bounds, and a 64-way quadratic certificate that are not exhibited for a deployed path
connectivity_gap: the orthant form does not produce a connecting cell chain or a concrete K_path
calculus_gap: qDissipation is an algebraic quadratic, not a source-bound derivative of a physical Lyapunov function
strictness_gap: the 49/30 example only shows anisotropy can beat ell2 on a one-entry toy; it is not a source residual witness
obstruction_scope: missing path, missing K_path, Float64/solve routing, distal coordinates, anchor bias, and first-exit hypotheses remain failure boundaries; they do not identify the physical remainder
missing_for_parent_close:
  one certified connecting cell/segment chain feeding a concrete nonnegative K_path in force coordinates, normalized once
  cell-local exact-real Jacobian/increment bounds that justify the channel envelopes
  one exact rational PSD/LDL witness for each distinct sign pair, or an explicit fallback to the T-P5-024 ell2 checker
  a decision routing Float64/solve/controller terms to either the orthant theorem or an additive branch
  a separate anchor-bias / discriminant ledger for nonzero b
  a P8 nominal flowpipe with explicit block-(4,5) margin
  a first-exit / ODE existence-continuation theorem on the actual trajectory
  a fresh pinned Lean receipt if the current sidecar is to be authenticated
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
