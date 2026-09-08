---
kind: review_result
review_id: review-T-P4-032-descriptor-P-upper-codex-20260908T052243
task_id: T-P4-032
agent: Codex-P4-math-lane
source_agent: Codex-P4-math-lane
created_at: 2026-09-08T05:22:43-06:00
inspected_commit: 943bd5b1713c88ba10a2965d3ce809449eac67fb
inspected_paths:
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DHAnalyticAUpper.lean
  - examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_ExactCellLambdaConsumer.lean
  - examples/routeb_p4_sharp_residual_lean/compile_receipt.json
  - examples/routeb_p4_sharp_residual_lean/SharpResidualBridge.lean
  - agent_review_inbox/receipt-T-P4-033-O0-same-key-baseline-bias-search-obstruction-20260907.json
integration_status: pending
admission_label: pending
proof_status: OPEN_UNCOMPILED
final_integration: false
proposed_integration_target: P4.same_cell_full_descriptor_P_upper
requested_action: retain the full-descriptor-to-port-cap interface as pending mathematical evidence; obtain a same-source RHS envelope and validated relative port bound before instantiation; do not promote registry status
---

# Existing relative-port evidence and the missing absolute P_upper

Bounded search result: no consumable same-source absolute P_upper or storage D_lower was established from the inspected receipts/documents. A concrete rational relative-port candidate exists in a separate BI ledger, but it is not an absolute squared-force cap and was not spliced into line 9. This round formalizes the missing full-descriptor/RHS route to P_upper without inventing H_i, K_i or P_i values.

## What the existing evidence actually supports

External paths below are under `C:/Users/z5242/Desktop/重构版/6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/`.

1. `routeB_compact_bi_combined_schur_ledger.csv` records eta=5.6 with rational `rho2_upward=234721/5000000`. Its producer reads a separate analytic_cs partition, checks 5,120 rows and RESOLVED labels, requests seven-decimal ceiling rationalization, and then uses Fraction arithmetic. The documented interpretation is `||port||²≤rhoSq*A_up`, not `||port||²≤rhoSq`. The recorded input is still rigorous-numerical candidate evidence; source, arithmetic enclosure and domain proofs are not reconstructed here. No BI coefficient replaces the Python line-9 coefficient.
2. The M0 left-output ledger has a different weighted-residual metric and different coefficients. Its numbers cannot substitute for the raw Euclidean port coefficient merely because eta agrees.
3. `examples/routeb_p4_sharp_residual_lean/compile_receipt.json` reports a compiled scalar/one-channel algebraic bridge. Its recorded source hash matches the currently inspected SharpResidualBridge file, but it explicitly has `physical_source_binding=false`, `source_residual_units_bound=false`, `global_coverage=false` and `registry_promoted=false`. Its abstract residual envelope is not a concrete DH P_upper. No compilation was rerun or independently certified this round.
4. The O0 receipt has an exact-Fourier center/radius/source/norm key and explicitly records the absence of a consumable same-key baseline/affine-bias receipt. Its K/Br/Cf tuple and rejected mass lower bound are not b_base or D_lower for this compact-DH source lane.
5. `routeB_compact_pmi_accel_envelope_interface.csv` explicitly says `A_bar not certified here`. It supplies a proposed generator, not a value or proof for the acceleration metric cap needed by DHAnalyticAUpper.

This is a bounded evidence assessment. It does not claim that no uninspected/future source-specific certificate could close the interface.

## New exact descriptor route

Let a and rhs be the FULL six-component acceleration and force vectors on one source cell, with the same mass/controller/disturbance/C/G semantics. Let mu>0 be a proved coercivity constant for that mass, not the scalar normalization nu. Required equations are

`M*a=rhs`, `mu*||a||²≤a'*(M*a)`, `||rhs||²≤H_i`.

The exact identity

`sum_j(mu*a_j-rhs_j)² = mu²||a||² - 2mu*(a' rhs) + ||rhs||²`

and coercivity imply **`mu²||a||²≤||rhs||²≤H_i`**. No inverse norm or square-root operation is needed. `full_descriptor_energy_bound` formalizes this step; it is not a proof that the intended physical mass satisfies its coercivity premise.

For the producer metric, bind a4/a5 to components 3/4 of that SAME full vector. Since both diagonal metric coefficients are at most `Bmax=1402217/12000000`,

`A_up≤Bmax*||a||²`.

Choose a rational K_i only after proving the exact scalar certificate

**`Bmax*H_i≤mu²*K_i`.**

`descriptor_metric_cap` then gives `A_up≤K_i`. The premise can be checked with exact rationals when mu and H_i are exact; this round chooses no numerical H_i/K_i.

Finally, a same-cell relative port bound and rational allocation

`||port||²≤rhoSq_i*A_up`, `rhoSq_i≥0`, `rhoSq_i*K_i≤P_i`

give **`||port||²≤P_i`**. `same_cell_P_upper` has exactly the function/quantifier shape needed for `SameSourceCharges.P_upper`; rhoSq_i is the uninflated squared-gain coefficient, not rho or a lambda-inflated charge.

## Connection to the existing A/target lane

The same proved K_i also feeds `DHAnalyticAUpper`: with same-cell p45≤28/5 and w²≤3, one may take A_i≥926/25+K_i/4. Thus one independently proved RHS/acceleration bound can support both the A_upper and P_upper envelopes, provided all source identities hold.

The full `RationalCharges`/common-lambda consumer still needs `t+D_i≤b_base` on each cell and a proved cover. Neither mass coercivity nor a port norm coefficient is a storage lower bound. `NormalizedTargetGuard` still requires the source/P4 equality or one-sided normalization conditions and a requested target T satisfying `0<T≤nu*t`.

This interface uses the FULL six-row descriptor. Four remote rows plus an independent a_B do not imply a bounded physical acceleration or the missing RHS envelope. Any nonzero residual/FD defect must appear in rhs or in the port decomposition with its own correct bound; it is not silently removed.

## Minimal obstruction

Even full descriptor equality and positive mass coercivity are insufficient without a force/domain bound. For arbitrary mu>0 and cap C≥0, the scalar assignment

`a=C+1`, `rhs=mu*(C+1)`, `M=mu`

satisfies `M*a=rhs` and `mu*a²=a*rhs`, yet `a²=(C+1)²>C`. Taking scalar port=a yields the corresponding cap failure even with a valid unit relative bound. `missing_rhs_cap_obstruction` encodes the descriptor/energy equalities and unbounded-square conclusion exactly.

This is a scalar mathematical countermodel, not a claim that an unrestricted ray belongs to the true DH physical domain. The missing fact is a proved same-source restriction on rhs/acceleration; no empirical maximum substitutes for it.

## Checks and hashes

The new proof attempt is `examples/routeb_p5_feasible_cone_spn_proof_attempt/NEW_P4_032_DescriptorPUpper.lean`. Read-only source/receipt inspection and manual algebra review only. PowerShell text/hash inspection returned exit code 0, with 0 proof placeholders and 0 trailing-whitespace lines in the new 113-line file. No Lean/Lake, producer, solver, sampling, CI query, regression or registry action was run. Import/elaboration/axiom verification remains open.

| Artifact | SHA-256 |
|---|---|
| `NEW_P4_032_DescriptorPUpper.lean` | `ab3960ffc6556475ef0543398eb1f9ec35a4b34f0098507b2b01ccae7f032368` |
| sharp-residual compile receipt | `c722093c9e69ec61a740160ce6d40b1dce200312a0eb50ed35e55d516867e5ec` |
| O0 same-key baseline/bias obstruction receipt | `275cae3c305f446a30c12c3c63fc0dd868e4445e5bfa2088a359e242bc7a70f3` |
| BI combined-Schur CSV | `b064b224467b0c3054ecc7b5926582f7f370ea1c88c4bea9821a3a36bed9bff0` |
| BI combined-Schur producer | `e106d9a43ddc7b58ade6974cc617d3d097952cf822dce4bbb06f4068791715f9` |
| acceleration-envelope interface CSV | `77d094802bab20bf0f1b88d21a040c023c7ca43a28fc145666da485f39b378c3` |

Disposition: **pending/open**. A relative coefficient has been located and bounded in scope; the new exact interface isolates the missing real-DH RHS/absolute-acceleration inequality. No concrete P_upper/D_lower is admitted.
