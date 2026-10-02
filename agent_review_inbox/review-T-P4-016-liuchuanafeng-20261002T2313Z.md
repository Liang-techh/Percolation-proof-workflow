---
kind: review_result
review_id: review-T-P4-016-liuchuanafeng-20261002T2313Z
source_agent: 流川枫
created_at: 2026-10-02T23:13:00Z
inspected_commit: 3bc8aaa5829b53526d50d050accbfdabb600427c
inspected_paths:
  - agent_review_inbox/task_queue.md
  - scripts/check_routeb_physical_rational_tail.py
  - src/percolation_workflow/routeb_nominal_distal_contract.py
  - agent_review_inbox/review-T-P4-016-kuangmanmozun-20260907T0344.md
task_id: T-P4-016
integration_status: pending
admission_label: pending
source_binding_proven: false
formal_certificate_allowed: false
registry_promoted: false
checker_executed: false
---

# T-P4-016 audit: tail seam is a candidate identity, not a 3x3 PMI proof

## Question

At commit `3bc8aaa5829b53526d50d050accbfdabb600427c`, does the in-repo nominal-distal tail contract already prove the square-root-free 3x3 PMI from the full off-diagonal `M0_BB`, with an exact polynomial identity, circle/domain multipliers, and a receipt that separates candidate Gram data from kernel verification?

## Decision

**No admission upgrade. Keep `admission_label: pending`.** The queue still marks `T-P4-016` open. The checker and `audit_routeb_physical_rational_tail` are fail-closed intake for an exact-rational candidate. Their dataclass defaults `formal_certificate_allowed=False` and `registry_eligible=False`. The module docstring says the checker validates artifact shape and provenance and does not prove the polynomial inequalities or source semantics.

This pass did not execute the checker. The default inputs live outside this repository (`../6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq`). No exit code, artifact hash, or source hash is claimed. This is not `compiled_candidate`, not `verified`, and not `rejected`: the in-repo interface matches the declared tail leaf and can check one Schur-complement identity when both tail and `M0` texts are supplied. It is not `architecture_only`: the missing objects are the external payload execution, a kernel positivity proof of the 3x3 PMI, circle/domain multipliers, and source binding of `M0_BB`.

`review-T-P4-016-kuangmanmozun-20260907T0344.md` answers a different bookkeeping question (aggregate execution-remainder Schur budget and double-spending). It is preserved and not overwritten. It is not a receipt for the square-root-free 3x3 tail PMI.

## Evidence inspected (read-only)

1. **Queue contract is still open.** Required deliverable: exact polynomial identity, circle/domain multipliers or a Lean proof, and a receipt distinguishing candidate Gram data from kernel verification. Forbidden: two independent component gains, floating PSD, sampled positivity, or any claim of global coverage / residual / flowpipe closure. Source named by the queue: `routeB_physical_rational_tail_pmi_scalar.csv`, its metadata, complete `M0_BB` bridge metadata, and the local tail contract.

2. **Checker blob.** `scripts/check_routeb_physical_rational_tail.py` blob `7e1cdf011e1ee51da12f291123fd2b5002ebbadd`. It reads three external CSVs, plus `routeB_physical_rational_tail_cs_polynomial.csv`, `routeB_Mq_M0.csv`, and `dhport_lib.jl`, hashes their bytes, and calls the audit. Exit `0` is returned only when status is `EXACT_RATIONAL_TAIL_CANDIDATE`; otherwise exit `2`. That status name is a candidate label, not a kernel receipt.

3. **Audit contract.** `routeb_nominal_distal_contract.py` blob `b6ea54e0968d4297e1494c6989e1f12452cff6ee`. `audit_routeb_physical_rational_tail`:
   - string-matches `EXPECTED_BRIDGE`, including `full_MBB_12` / `full_MBB_21` equal to `153080849893419/50000000000000000000000000000000`, `evidence_level=algebraic_subcertificate`, and `EXPECTED_TAIL_META` (`pmi_dimension=3`, `schur_scalar_dimension=1`, `scalar_terms=27`, degree `6`, `delta_sq=1/160000`, `energy_accounting=tail_only_no_double_count`, `evidence_level=algebraic_sos_input_candidate`);
   - parses the scalar CSV as one 1x1 exact rational polynomial and rejects a term count other than 27, total degree other than 6, or support outside `e5..e10` (`c3,s3,c4,s4,c5,s5`);
   - if both tail-polynomial and `M0` texts are present, parses `M0` with `Fraction` on decimal CSV tokens, checks 6x6 symmetry, computes `rho` from `r_hat=(0,1,-6377/6250,0)` on remote indices `(0,1,2,5)`, and compares the scalar polynomial to

```text
(1/160000) * rho * det(M0_BB)
  - M0_BB[1,1] * t1^2
  + 2 * M0_BB[0,1] * t1 * t2
  - M0_BB[0,0] * t2^2
```

     with `M0_BB` taken from 0-based indices `(3,4)`. A mismatch appends `tail_scalar_schur_identity_mismatch`.

   Matching the metadata strings and this identity does not prove the 3x3 PMI, does not apply circle or box multipliers, and does not run a PSD/LDL test. The separate Gram audit constants in the same file are not invoked by this function. `energy_accounting=tail_only_no_double_count` is an expected CSV token, not a proved no-double-count theorem. Decimal `Fraction` parsing of `M0` is not a source equality for the physical `M0_BB`.

4. **No execution in this pass.**

```text
command: not run
exit_code: not claimed
external_payload_sha256: not observed
source_sha256: not observed
lean_receipt: absent
placeholder_scan: not applicable (no Lean file in this leaf)
```

## Obstruction

```text
interface: exact rational tail candidate plus optional Schur-complement identity
checker: scripts/check_routeb_physical_rational_tail.py
audit: audit_routeb_physical_rational_tail
blobs: 7e1cdf011e1ee51da12f291123fd2b5002ebbadd; b6ea54e0968d4297e1494c6989e1f12452cff6ee
next_route: execute the checker and keep EXACT_RATIONAL_TAIL_CANDIDATE below admission;
            then a separate kernel leaf must prove the 3x3 PMI from the off-diagonal M0_BB
            with circle/domain multipliers, without two independent component gains
missing: in-repo payload execution, source-bound M0_BB, circle/domain multipliers,
         pinned Lean/kernel positivity receipt
flags: formal_certificate_allowed=false, registry_eligible=false
source_binding: not claimed
```

## Assumptions still required

- run the checker on the named external CSVs and record artifact/source hashes, scalar term count, degree, and whether `tail_scalar_schur_identity_mismatch` is absent;
- treat a passed identity as candidate algebra only; do not infer 3x3 positivity from the scalar Schur polynomial or from metadata `pmi_dimension=3`;
- do not replace the full off-diagonal `M0_BB` by two independent component gains;
- a pinned Lean receipt for the identity and for any later Gram/LDL positivity, separate from floating or sampled checks;
- source equality, domain coverage, residual, and flowpipe gates before any parent promotion.

## Integration target and requested action

- Target: documentation / DAG metadata only. Leave `T-P4-016` open.
- Requested action: next owner may execute the existing checker and return the printed JSON plus exit code. Do not treat `EXACT_RATIONAL_TAIL_CANDIDATE` as verified. Do not edit registry, `state.json`, or formal certificates.

## Forbidden-boundary compliance

- Did not use two independent component gains.
- Did not treat floating PSD, sampled positivity, or metadata `algebraic_sos_input_candidate` as a proof.
- Did not claim global coverage, residual closure, or flowpipe closure.
- Did not invent an exit code, artifact hash, or Lean axiom list.
- Did not edit registry, state, task queue, or formal proofs.
