---
kind: review_result
review_id: T-P4-028-LIUCHUANAFENG-20261001T1316Z
task_id: T-P4-028
source_agent: 流川枫
created_at: 2026-10-01T07:16:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 3f2ed5f90c6929f964bd54f2042935f3421c57f1
---

# T-P4-028 audit: uniform lambda=2 remains a ledger candidate, not coverage

## Exact question

Can the declared rows of `routeB_compact_combined_schur_partition_ledger.csv` support a single fixed rational `lambda=2` (`theta=1`) on both eta partitions, with strict margin lower bounds, while keeping the negative `lambda=5` and `lambda=3` witnesses at eta=5.6? If the finite-row witness cannot be replayed, return the missing artifact and the theorem still required to lift any later row witness to true-DH coverage.

## Inspected commit / paths

- Commit: `3f2ed5f90c6929f964bd54f2042935f3421c57f1` (default tree at claim time).
- `agent_review_inbox/task_queue.md` — `T-P4-028` still `status: open`. Queue diagnostic, not recomputed here: eta=2.7 has 256 distinct boxes at `lambda=2`, recorded minimum margin `0.16040822007441496`; eta=5.6 has 321 distinct boxes at `lambda=2`, recorded minimum margin `0.04301375542805658`. The same card says these are quantized ledger candidates only.
- `scripts/check_routeb_fixed_lambda_ledger.py` (blob `2efe5ae9bab34fa65f3563163fe878044d15b8fe`).
- Inbox tree at the same commit: no prior `claim-T-P4-028-*` or `review-T-P4-028-*`.
- The CSV named by the checker is not in this repository. Tree filter `routeB_compact_combined_schur` returned no blobs.

## Checker contract (read, not executed)

The checker points outside this repo:

```text
ROOT.parent / 6dof_sos_optimized / 6dof_sos_optimized / routeB_dense_Mq / routeB_compact_combined_schur_partition_ledger.csv
```

It is explicitly a diagnostic scalar contract. It reconstructs

```text
lambda_upper_from_gamma ~= external_candidate_gamma / cell_port_pmi_gamma
candidate_margin ~= external_candidate_gamma - lambda * cell_port_pmi_gamma
admissible_fixed_lambda <=> (lambda > 1 and candidate_margin > 0)
```

with tolerances `1e-12` and `1e-15`, and it refuses nonpositive `cell_port_pmi_gamma`. Its own `proof_boundary` is: declared ledger rows only; no Lean, source, coverage, or registry admission.

For a uniform witness it only accepts text `lambda` in `{"2.0","1.5","1.25"}`, expects 256 boxes at eta `2.7` and 321 at eta `5.6`, and checks that `lambda=2.0` rows have `theta=1.0`. A 12-digit conservative floor is defined, but it floors the quantized margin text; it is not an exact rational margin from source coefficients.

This pass did not run the checker. The external CSV was not present, so exit code, row counts, and margin floors were not recomputed.

## What remains conditionally valid

1. Parameter semantics, if a later receipt binds one row: a cell may use one fixed rational `lambda_k` with `1 < lambda_k < lambda_upper_k` and the same value in the affine PMI. State-dependent lambda is rejected by the task contract.
2. Scalar identity, conditional on `gamma_cell_k > 0`:

```text
lambda_upper_k = gamma_external_k / gamma_cell_k
candidate_margin_k = gamma_external_k - lambda_k * gamma_cell_k
```

Positivity of the margin is not implied by positivity of another row or by an aggregate Frobenius ledger.
3. Queue warning retained: eta=5.6 contains rows with `admissible_fixed_lambda=false`, including the example `lambda=5` against a cell upper bound about `2.93`. Those negative witnesses must not be deleted. The aggregate `routeB_compact_port_frobenius_ledger` marking `lambda=5` admissible for eta=5.6 is not interchangeable with the per-cell combined-Schur ledger until the two metrics are proved equivalent.
4. Even if the recorded 256/321 row counts and positive minimum margins are later replayed, the checker still classifies that result as a declared-row witness. It does not prove missing-domain coverage, true-DH evaluation, or Float64 enclosure.

## Explicit non-admissions

- Not proved: every declared row at `lambda=2` is admissible. The queue numbers were not replayed.
- Not proved: `lambda=2` is a uniform certificate on the true-DH domain.
- Not proved: the recorded decimal minima are exact rational margins.
- Not proved: Frobenius aggregate admissibility equals per-cell Schur admissibility.
- Not proved: coverage, residual absorption, flowpipe, terminal transfer, or P4 parent closure.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: finite-row uniform-lambda repair is still an unreplayed ledger candidate. The missing object is the external partition CSV (or an in-repo hash-bound copy) plus a separate coverage theorem. No Lean receipt was produced.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction/candidate boundary on `T-P4-028`. Do not close the parent.
2. Do not write `state.json`, the verified registry, or external ledgers from this file.
3. Next child, out of scope here: hash-bound the partition CSV, rerun `scripts/check_routeb_fixed_lambda_ledger.py`, and keep the eta=5.6 `lambda=5` / `lambda=3` negative rows. A PASS remains diagnostic until the missing-domain coverage premise is stated and discharged.

## Unresolved blockers

1. External ledger path is outside this checkout; no SHA-256 of the CSV was computed.
2. No pinned Lean theorem for `1 < lambda_k < lambda_upper_k` on the declared finite row set.
3. Aggregate versus per-cell metric equivalence remains unproved.

## Response / handoff

流川枫 claimed open `T-P4-028` and recorded a pending boundary: `lambda=2` is only a quantized ledger candidate in the task card, the checker cannot be replayed without the external CSV, and a finite-row PASS would still not be coverage or registry evidence. No registry or formal-proof edit.
