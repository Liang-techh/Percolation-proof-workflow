---
kind: review_result
review_id: review-T-P4-018-liuchuanafeng-20261005T1224Z
source_agent: 流川枫
created_at: 2026-10-05T12:24:00Z
inspected_commit: 0cdbdf8d6ed376933db5feff42919a0408a7c891
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_gram_residual_lean/GramResidual.lean
  - examples/routeb_gram_residual_lean/README.md
  - src/percolation_workflow/routeb_residual_l1_contract.py
  - scripts/record_routeb_residual_l1_frontier.py
  - agent_review_inbox/review-T-P4-018-liuguanyi-20260907T0522.md
  - agent_review_inbox/claim-T-P4-018-juyangxianzun-20260907T0532.md
task_id: T-P4-018
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
lean_executed: false
---

# T-P4-018 audit: generic residual l1 seam is present; v1 receipt is not

## Question

At commit `0cdbdf8d6ed376933db5feff42919a0408a7c891`, does the in-repo Gram residual Lean seam already satisfy `routeb.residual_l1_lean_receipt.v1` for `weighted_residual_l1_bound` and `decomposition_nonnegative_of_abs_residual`, including the 511-term coefficient digest and a pinned compile?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-018` as `new`. The Lean file states the two generic theorems and contains `#print axioms` lines, but this pass did not compile them. No receipt object was found for `audit_routeb_residual_l1_lean_receipt` to accept. Under that auditor, missing coordinator pins stay `PENDING`; this review does not invent those pins.

This is not `compiled_candidate`: there is no exit code, toolchain pin, Mathlib pin, or axiom list from a kernel run. It is not `rejected`: the source text matches the named theorem pair and does not contain `sorry` or `admit`. It is not `architecture_only`: the missing objects are a remote receipt and the T-P4-017 coefficient binding, not the absence of an interface. It is not `verified`.

`review-T-P4-018-liuguanyi-20260907T0522.md` answers a different question (acceleration-style versus generalized-force `kc` congruence). It is preserved and not overwritten. The 2026-09-07 claim by 巨阳仙尊 remains a formalization claim for that congruence sidecar, not a compile receipt for this seam.

## Evidence inspected (read-only)

1. **Queue contract.** Deliverable required: Lean compile receipt, `#print axioms`, and explicit source/hash binding for the concrete coefficient list. Receipt schema `routeb.residual_l1_lean_receipt.v1`, auditor `audit_routeb_residual_l1_lean_receipt`. Required fields include pinned source/artifact hashes, both theorem names, zero `sorry`/`admit`, exit code `0`, coefficient term count, `residual_l1`, safe rational lower bound, positive scaled margin, and `residual_coefficients_sha256` equal to the canonical 511-term digest `95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf`. Missing coordinator-owned pins remain `PENDING`. Forbidden: treating the generic seam as proof of the giant CSV identity, true-DH semantics, domain coverage, or Route-B closure.

2. **Lean seam.** `examples/routeb_gram_residual_lean/GramResidual.lean` blob `ad8c6e41943820f4d178ab47100cc3731c7c790d` (1581 bytes). Directory contains only that file and `README.md` blob `34cf92a40c59639071bb0c60401037dc786da5af`. No `lakefile`, toolchain file, or receipt JSON.

   Theorems present, with the expected fully qualified names:

   - `RouteBGramResidual.weighted_residual_l1_bound`
   - `RouteBGramResidual.decomposition_nonnegative_of_abs_residual`

   The first uses `Finset.abs_sum_le_sum_abs`, `abs_mul`, and `mul_le_mul_of_nonneg_left` under `|atom i| ≤ 1`. The second uses `abs_le` and `linarith` under `value = lower + positive + residual`, `0 ≤ positive`, `|residual| ≤ l1`, and `l1 ≤ lower`. Neither theorem mentions a coefficient list, term count, digest, CSV, or T-P4-017 reconstruction.

3. **Placeholder scan of the Lean text only.** No `sorry`, `admit`, or `axiom` declaration. Two `#print axioms` commands are present and were not executed. Axiom list: not observed.

4. **Auditor.** `src/percolation_workflow/routeb_residual_l1_contract.py` blob `f7344dc7bcaefd98c79245605fc8edbf34ff176c`. `audit_routeb_residual_l1_lean_receipt` is side-effect free. `EXPECTED_THEOREMS` matches the two names above. Allowed axioms default to `propext`, `Quot.sound`, `Classical.choice`. `formal_certificate_allowed` and `registry_eligible` are hardcoded `False` on the returned audit. Omitting coordinator-owned expected hashes, toolchain, or Mathlib commit forces `PENDING` even if a remote receipt is internally complete. An `ACCEPTED` audit is documented as still a compiled candidate, not registry admission.

   No receipt mapping was supplied to this auditor in-repo. Calling it is therefore not useful as evidence and was not done. The documented 511-term digest appears in the queue and README as a binding witness; it is not attached to a `residual_coefficients_sha256` field that the auditor compared.

5. **Frontier recorder, not a receipt.** `scripts/record_routeb_residual_l1_frontier.py` blob `5f45ba764484b8ea0572071ec3ca44b58e1dfc6d` writes DAG metadata and lists unresolved items `pinned_lean_compile_receipt`, `zero_sorry_and_allowed_axioms_receipt`, and `concrete_t_p4_017_coefficient_list_binding`. It was not executed. It must not be treated as a compile.

6. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
lean_toolchain: not pinned in this directory
mathlib_commit: not observed
axiom_print: not executed
placeholder_scan: sorry=0 admit=0 on GramResidual.lean text only
coefficient_term_count: documented 511, not receipt-bound
residual_coefficients_sha256: documented 95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf, not auditor-matched
residual_l1 / rational_lower_bound / scaled_margin: absent
```

## Obstruction

```text
interface: generic finite-sum l1 bound plus absorption lemma
lean_blob: ad8c6e41943820f4d178ab47100cc3731c7c790d
auditor: audit_routeb_residual_l1_lean_receipt
auditor_blob: f7344dc7bcaefd98c79245605fc8edbf34ff176c
schema: routeb.residual_l1_lean_receipt.v1
next_route: pinned Lean compile of both theorems, capture #print axioms,
            then a coordinator-bound receipt with the 511-term digest
missing: compile command, exit code, toolchain, Mathlib pin, axiom list,
         coefficient artifact hash, reconstruction candidate receipt
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- a Lean owner compiles the seam on a pinned toolchain and returns stdout/stderr, exit code, and `#print axioms` for both theorems;
- the receipt must name exactly the two expected theorems and report `sorry_free` / `admit_free`;
- coordinator-owned source and coefficient-artifact hashes must be supplied to the auditor; an agent must not self-authenticate them;
- `residual_coefficients_sha256` must equal the canonical 511-term digest only after the reconstruction candidate is bound, not by copying the README string;
- generic nonnegativity under `|atom i| ≤ 1` does not prove the giant CSV identity, true-DH semantics, domain coverage, or Route-B closure.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-018` open.
- Requested action: next Lean owner may return a focused compile receipt. Do not treat the generic seam or the documented digest as verified. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not treat the generic seam as proof of the giant CSV identity.
- Did not claim true-DH semantics, domain coverage, or Route-B closure.
- Did not invent an exit code, axiom list, or coefficient binding.
- Did not edit registry, state, task queue, or formal proofs.
