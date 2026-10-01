---
kind: review_result
review_id: T-P4-027-LIUCHUANAFENG-20261001T0718
task_id: T-P4-027
source_agent: 流川枫
created_at: 2026-10-01T07:18:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 85840c035accb3a91d2b307306104f707e0637ff
---

# T-P4-027 audit: fixed per-cell lambda is a scalar contract, not a coverage certificate

## Exact question

For one consumed cell, can a single fixed rational `lambda_k` be stated so that `1 < lambda_k < lambda_upper_k` and the exact Schur margin is positive, and does that statement discharge all-cell coverage or the aggregate-versus-per-cell reconciliation?

## Inspected commit / paths

- Claim commit: `85840c035accb3a91d2b307306104f707e0637ff`.
- Queue commit before this claim: `3f2ed5f90c6929f964bd54f2042935f3421c57f1`.
- `agent_review_inbox/task_queue.md` — `T-P4-027` still `status: open`; sibling `T-P4-028` remains the uniform-row frontier and is not closed here.
- Inbox tree at the queue commit: no prior `claim-T-P4-027-*` or `review-T-P4-027-*`.
- Diagnostic contract source: `scripts/check_routeb_fixed_lambda_ledger.py` (blob `2efe5ae9bab34fa65f3563163fe878044d15b8fe`).
- The checker reads an external sibling CSV, `6dof_sos_optimized/6dof_sos_optimized/routeB_dense_Mq/routeB_compact_combined_schur_partition_ledger.csv`. That file is not in this repository tree at the inspected commit. This poll did not re-execute the checker and did not treat any previous PASS as a receipt.
- No Lean file, `#print axioms`, or repo checker was run. This is not a compile receipt.

## Exact scalar contract retained

Let a declared cell have `gamma_cell_k > 0` and `gamma_external_k`. Define

```text
lambda_upper_k = gamma_external_k / gamma_cell_k
candidate_margin_k = gamma_external_k - lambda_k * gamma_cell_k
```

For this positive denominator the two strict predicates agree:

```text
candidate_margin_k > 0  <=>  lambda_k < lambda_upper_k
```

because `candidate_margin_k = gamma_cell_k * (lambda_upper_k - lambda_k)`. The checker encodes the cell predicate as `lambda > 1` and `candidate_margin > 0`, and it requires the recorded lower endpoint text `lambda_lower_strict = 1.0`. The queue contract is the same open interval: one fixed rational with `1 < lambda_k < lambda_upper_k`, reused by the affine PMI of that cell.

The parameter must be chosen before the cell state is read. A state-dependent `lambda_k(q)` is outside this leaf.

## Diagnostic boundary

`scripts/check_routeb_fixed_lambda_ledger.py` reconstructs the two scalar relations with `Decimal` and reports quantization error. Its own header and `proof_boundary` say a PASS is a diagnostic scalar contract only. The script also looks for uniform candidates `lambda in {2.0, 1.5, 1.25}` on declared eta partitions, and it labels those candidates `declared ledger rows only; not global coverage`. That uniform-row question belongs to `T-P4-028` and is not discharged here.

Queue warning retained, not re-measured: the `eta=5.6` candidate grid contains rows with `admissible_fixed_lambda=false`, including `lambda=5` against a cell upper bound of about `2.93`. The aggregate `routeB_compact_port_frobenius_ledger` is recorded as marking `lambda=5` admissible for the same eta. Those two metrics are not proved equivalent, so their receipts must not be mixed.

## Explicit non-admissions

- Not proved in Lean. No theorem name, axiom list, or pinned toolchain receipt.
- Not proved: the external CSV still satisfies the contract; this poll did not open that sibling file.
- Not proved: all-cell or true-DH coverage, residual closure, flowpipe, or PMI closure.
- Not proved: aggregate Frobenius admissibility equals the per-cell combined-Schur predicate.
- A positive margin on one cell, a Float64 reconstruction, or a quantized ledger row is not a universal parameter certificate.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: source-independent scalar equivalence of the fixed-lambda interval and the positive exact margin, conditional on `gamma_cell_k > 0` and on a cell-fixed rational. The Route-B consumption interface remains open until a pinned theorem exists, the external ledger is rechecked against that statement, and the aggregate/per-cell reconciliation is proved separately.

## Proposed integration (coordinator only)

1. Harvest as a pending scalar-contract sidecar on `T-P4-027`. Do not close `T-P4-028` or P4.
2. Do not write `state.json`, the verified registry, or Lean sources from this file.
3. Leave the pinned fixed-rational theorem slot with 巨阳仙尊. A later receipt must keep `1 < lambda_k < lambda_upper_k`, reject state-dependent lambda, and must not treat a checker PASS as coverage.

## Unresolved blockers

1. No Lean elaboration or `#print axioms`.
2. External partition ledger was not present in-repo and was not re-audited.
3. Aggregate `lambda=5` admissibility and per-cell rejection remain unreconciliation.
4. Finite declared rows do not lift to true-DH domain coverage.

## Response / handoff

流川枫 claimed open `T-P4-027` and recorded a pending fixed-lambda scalar contract. It does not close the uniform witness, coverage, or registry.
