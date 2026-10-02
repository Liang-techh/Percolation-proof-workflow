---
kind: review_result
review_id: review-T-P4-017-liuchuanafeng-20261002T1914Z
source_agent: 流川枫
created_at: 2026-10-02T19:14:00Z
inspected_commit: c3927729ed1022e8a2428eb216e6956099475f46
claim_commit: 6605e793b5557b6e8a91cb6f254e9f4e15ac9c08
inspected_paths:
  - agent_review_inbox/task_queue.md
  - scripts/check_routeb_tail_gram_reconstruction.py
  - src/percolation_workflow/routeb_nominal_distal_contract.py
task_id: T-P4-017
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
---

# T-P4-017 audit: rational Gram reconstruction is a candidate, not a kernel receipt

## Question

At commit `c3927729ed1022e8a2428eb216e6956099475f46`, does the in-repo reconstruction contract already prove `p_scaled - opt` modulo the 12 box generators and three circle identities, with exact `opt` provenance, Gram PSD, and a positive margin that can enter the verified registry?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-017` open. The checker and `audit_routeb_physical_rational_gram_reconstruction` are fail-closed intake for an exact-rational candidate. Their own contract sets `formal_certificate_allowed=false` and `registry_eligible=false`, and the function docstring says the decimal objective/scale are rationalized under an explicit cap, so the result is not a proof of the original optimization problem or a Lean theorem.

This pass did not execute the checker. The default inputs live outside this repository (`../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`). No exit code is claimed. This is not `compiled_candidate`, not `verified`, and not `rejected`: the in-repo interface matches the declared reconstruction leaf. It is not `architecture_only`: the missing objects are the external payload execution, exact solver-`opt` provenance beyond the capped rationalization, and a pinned Lean receipt.

`review-T-P4-017-kuangmanmozun-20260907T0449.md` audits canonical `kc` scale (`c=1/20` versus `1/100`). It is not a receipt for this Gram leaf and is not overwritten.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Required deliverable: exact `opt` provenance, expansion identity, all Gram PSD evidence, and a fail-closed receipt separating rational candidate from kernel proof. Forbidden: inferring target equality from positive Gram blocks alone, using a decimal `opt` without exact provenance, or claiming Route-B closure. Local progress note: `check_routeb_tail_gram_reconstruction.py` expands a rational payload and reports a positive candidate margin; solver `opt` provenance and pinned Lean receipt remain open. The note records residual term count `511` and digest `95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf` as a binding witness, not kernel evidence. This review does not recompute that digest.

2. **Checker blob.** `scripts/check_routeb_tail_gram_reconstruction.py` blob `8b80a2c72b337890a87bf11bc8aa178d19dc4667`. It reads four external CSVs plus `dhport_lib.jl`, hashes their bytes, and calls the audit. Exit `0` is returned only when status is `EXACT_RATIONAL_GRAM_RECONSTRUCTION_CANDIDATE`; otherwise exit `2`. The module docstring says the script reconstructs the identity without upgrading status.

3. **Audit contract.** `routeb_nominal_distal_contract.py` blob `b6ea54e0968d4297e1494c6989e1f12452cff6ee`. `RouteBPhysicalRationalGramReconstructionAudit` defaults `formal_certificate_allowed=False` and `registry_eligible=False`. The reconstruction function:
   - requires probe fields `status=OPTIMAL`, 12 inequalities, 3 circle equalities, and `formal_certificate_allowed=false`;
   - quantizes `scale_factor` and floors `objective_lower_bound` at denominator cap `10**12`;
   - rejects non-positive scale or lower bound;
   - expects a 27-term scalar target on active exponents `c3,s3,c4,s4,c5,s5`;
   - builds a residual and sets `scaled_margin = safe_lower - residual_l1`;
   - appends `reconstruction_nonpositive_margin` if that margin is not strictly positive;
   - returns `EXACT_RATIONAL_GRAM_RECONSTRUCTION_CANDIDATE` only when the error list is empty.

   Matching the probe string `OPTIMAL` is an input-shape check. It is not exact solver provenance and not a kernel certificate. A positive Gram block alone is not treated as target equality: the residual and margin tests are separate, and even a candidate status does not flip the certificate flags.

4. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
external_payload_sha256: not observed
source_sha256: not observed
residual_coefficients_sha256: not recomputed
lean_receipt: absent
```

## Obstruction

```text
interface: exact rational Gram reconstruction candidate
checker: scripts/check_routeb_tail_gram_reconstruction.py
audit: audit_routeb_physical_rational_gram_reconstruction
blobs: 8b80a2c72b337890a87bf11bc8aa178d19dc4667; b6ea54e0968d4297e1494c6989e1f12452cff6ee
missing: in-repo payload execution, uncapped exact opt provenance, pinned Lean receipt for residual_l1 / margin
queue_witness_not_recomputed: 511 terms, digest 95042f6ea7c9989174d6045383138099686c2383649b3358611a63f374bcf7cf
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- run the checker on the named external CSVs and record artifact/source hashes, residual term count, residual digest, derived-versus-solver gap, and margin;
- keep Lean consumers on the derived safe lower bound, never the raw `OPTIMAL` decimal;
- a pinned Lean receipt for the coefficient residual, separate from Gram-block positivity;
- source equality, domain coverage, and comparator gates before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-017` open.
- Requested action: next owner may execute the existing checker and return the printed JSON plus exit code. Do not treat `EXACT_RATIONAL_GRAM_RECONSTRUCTION_CANDIDATE` as verified. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not infer target equality from positive Gram blocks.
- Did not treat a decimal `opt` or probe status `OPTIMAL` as exact provenance.
- Did not claim Route-B closure, coverage, or source binding.
- Did not invent an exit code, residual digest, or Lean axiom list.
- Did not edit registry, state, task queue, or formal proofs.
