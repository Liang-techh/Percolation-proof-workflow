---
kind: review_result
review_id: review-GH-LEAN-body6-tail-minors-liuchuanafeng-20260907T2304
task_id: GH-LEAN-body6-tail-minors
agent: 流川枫
source_agent: 流川枫
created_at: 2026-09-07T23:04:00-06:00
inspected_commit: 9d06f39d02e22b2124800ac6752a504a407f92fb
inspected_paths:
  - agent_review_inbox/task_queue.md
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_TAILMINORS20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_TAILPSD20260907.lean
  - examples/routeb_b45_source_comparator_lean/NEW_BODY6_SLICE_MASSTAIL_Core20260907.lean
  - examples/routeb_b45_source_comparator_lean/COMPILATION_STATUS.md
lean_blob_sha: 8c8f454c8e484bbcc000bd92d3e0072c26039fca
tailpsd_blob_sha: 6b38f3382fd78ef019d21135985f1e1b5776b5f1
masstail_core_blob_sha: 6ab3237ad70206ecd4e98751a4b94bb23c76ac60
related_tasks:
  - GH-LEAN-body6-tail-minors
  - T-P4-STORAGE-IDENTITY-TRANSFER
  - T-P4-COMPILED-LEDGER-BINDING
integration_status: pending
admission_label: pending
proposed_integration_target: P4.body6_slice_tail_principal_minors_sidecar
requested_action: keep the sidecar as an UNCOMPILED tail-subblock interface; require explicit zero off-diagonals before using det2 = product of diagonals; do not infer full-body PSD, eigenvalues, Fourier, coverage, source identity, or registry admission; do not write StateStore or verified registry
---

# GH-LEAN-body6-tail-minors — theorem-boundary audit

## 0. Result

`NEW_BODY6_SLICE_TAILMINORS20260907.lean` is an **UNCOMPILED 2×2 tail principal-minor adapter**. It connects `explicitTail` / `sourceTail` to `StrictPrincipalMinors`, `PrincipalMinorCriterion`, and the imported `TailPSD` predicate.

This lane did **not** run Lean/Lake/`#print axioms`. The file header and parent sidecars are themselves marked UNCOMPILED. Absence of `sorry`/`admit` in the inspected text is not a kernel receipt.

`admission_label` is therefore `pending` (uncompiled candidate interface).
Nothing here is registry evidence.

Official compile/repair ownership in `task_queue.md` remains `巨阳仙尊`.
This file is an independent inspect-only share.

## 1. Exact public surface

Namespace: `NEW_BODY6_SLICE_TAILMINORS20260907`.
Imports: `NEW_BODY6_SLICE_TAILPSD20260907` (and, transitively, mass-tail core/source and VGRAM source).

| name | role | what it does *not* do |
|---|---|---|
| `det2` | scalar `B00*B11 - B01*B10`; not `Matrix.det` | interpret a general 6×6 minor or an eigenvalue |
| `StrictPrincipalMinors` | `0 < B00`, `0 < B11`, `0 < det2 B` | claim Sylvester for a non-symmetric or non-diagonal block |
| `PrincipalMinorCriterion` | nonstrict version of the same three inequalities | close PSD for a matrix with nonzero cross terms |
| `tail_principal_formulas_attempt` | expands `explicitTail` diagonals and writes `det2 = product of those diagonals` | hold unless the off-diagonals are the zeros baked into `explicitTail` |
| `tail_principal_positive_attempt` | `0 < kappa`, `0 ≤ m`, `0 ≤ h^2` ⇒ strict minors | drop the sign hypotheses or treat `h^2 ≥ 0` as optional prose |
| `strict_to_nonnegative_attempt` | strict minors ⇒ nonstrict criterion | add new analytic content |
| `diagonal_minor_criterion_to_psd_attempt` | **requires** `B 0 1 = 0` and `B 1 0 = 0` plus nonstrict minors ⇒ `TailPSD` | apply to a general 2×2 or to the rest of BODY6 |
| `tail_minor_psd_interface_attempt` | packages the three predicates on `explicitTail` | invent a kernel compile or a source inhabitant |
| `source_tail_minors_attempt` | after `source_tail_eq_attempt`, transports the same package to `sourceTail q` | construct `CenterOffsetTarget` / `SourceWeightsTarget` or bind Julia/DH |

`TailPSD` (imported) is only symmetry plus `0 ≤ quadratic B x` on `Fin 2`. It is not an eigenvalue statement and not a full-mass-matrix statement.

## 2. Quantifier / premise boundary (the admission risk)

The determinant identity in `tail_principal_formulas_attempt` is **class-restricted**: `explicitTail` is defined in the mass-tail core as the diagonal table

`![![kappa + m * h^2 * sin^2 z, 0], ![0, kappa + m * h^2]]`.

So `det2 = B00*B11` is true because `B01 = B10 = 0`, not because a general principal-minor criterion was proved. The sidecar says this in comments and again by passing `rfl, rfl` into `diagonal_minor_criterion_to_psd_attempt`.

An integrator that reads `TailPSD (explicitTail …)` and writes “BODY6 PSD / eigenvalue closed” without

1. the three sign premises `0 < kappa`, `0 ≤ m`, `0 ≤ h^2` (or `offset^2` on the source path),
2. the explicit zero cross terms,
3. hashed inhabitants of `CenterOffsetTarget` and `SourceWeightsTarget` on the `sourceTail` path,

is a protocol error.

`source_tail_minors_attempt` still indexes body `5` and ordered joints `3,4` only through the imported `sourceTail` definition. That is a column restriction, not coverage of the other BODY6 blocks.

Pointwise real parameters carry no domain, flowpipe, or Fourier quantifier.

## 3. Compile / axiom status this slot

- Pinned toolchain: **not executed**.
- Exit code: **not obtained**.
- `#print axioms`: **not present and not run** in this sidecar.
- Placeholder scan (text only): no `sorry`, `admit`, or `axiom` command in `NEW_BODY6_SLICE_TAILMINORS20260907.lean`.
- Parent `COMPILATION_STATUS.md` records an incomplete pinned attempt on a *different* candidate (`SourceBodyMassExtensionalProbe.lean`) and must not be reused as a compile receipt for this file.
- Blobs inspected at commit `9d06f39d02e22b2124800ac6752a504a407f92fb`:
  - tail-minors `8c8f454c8e484bbcc000bd92d3e0072c26039fca`
  - tail-PSD `6b38f3382fd78ef019d21135985f1e1b5776b5f1`
  - mass-tail core `6ab3237ad70206ecd4e98751a4b94bb23c76ac60`

A later `:40` Lean slot may compile this file under the pinned toolchain.
That compile would still be `compiled_candidate`, not verified registry admission.

## 4. Forbidden promotions (explicit)

This review does **not** claim:

- full-body PSD, spectrum, or characteristic-polynomial control;
- a general (nonsymmetric / nonzero-cross-term) principal-minor criterion;
- source identity, true-DH, Float64 reification, or concrete cell payloads;
- Fourier / coverage / flowpipe / P8 statements;
- P4/M4 closure or comparator PASS;
- any StateStore or verified-registry write.

## 5. Suggested next leaf (not executed)

If the `巨阳仙尊` `:40` slot is assigned: produce an immutable compile receipt with the theorem names above, pinned toolchain, exit code, `#print axioms` for each listed theorem, and a placeholder scan of the import cone. Keep the zero-cross-term hypotheses and the source-weight/center premises as unproved inhabitants in that receipt.
