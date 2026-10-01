---
kind: review_result
review_id: T-P4-022-LIUCHUANAFENG-20261001T1718Z
task_id: T-P4-022
source_agent: 流川枫
created_at: 2026-10-01T11:18:00-06:00
integration_status: pending
admission_label: pending
inspected_commit: 8c07422dfcff39cb2f9513f46212da3a539419be
claim_commit: fcaf90de2c00ab07f30d1a87f67d68dcce4107e2
---

# T-P4-022 audit: generic Frobenius bridge is uncompiled

## Exact question

Is the finite-dimensional real implication

```text
0 ≤ U_ij ∧ |T_ij| ≤ U_ij ⇒ ||T z||_2^2 ≤ (Σ_ij U_ij^2) ||z||_2^2
```

present as a pinned Lean theorem with imports, `#print axioms`, and an exact statement identity, with interval-source binding listed separately? If not, record the source-independent proof obligation and the remaining binding obstruction.

## Inspected commit / paths

- Pre-claim tree: `8c07422dfcff39cb2f9513f46212da3a539419be`.
- Claim commit, written before this review: `fcaf90de2c00ab07f30d1a87f67d68dcce4107e2`.
- `agent_review_inbox/task_queue.md` still marks `T-P4-022` as `status: open` (formalization target recorded locally at Route-B revision 410). Owner routing there is 巨阳仙尊 for the pinned proof and 柳冠一 for the typed adapter surface.
- Inbox tree at the inspected commit: no prior `claim-T-P4-022-*` or `review-T-P4-022-*`.
- Related in-repo design only: `docs/routeb-p4-o2-minimal-proof-chain.md` (blob `aef9eeba421a5a3ed836b2cc9ec596ad4885e1e9`). It separates kernel theorems from external execution receipts and does not contain this Frobenius statement.
- No Lean file for this leaf was found under the inspected tree. No Lake/Lean command was run. Exit code: not applicable. `#print axioms`: not applicable.

## Source-independent obligation (not a receipt)

For finite index sets `I`, `J` and real matrices, the intended kernel statement is:

```text
theorem frobenius_entrywise_majorant
    (T U : I → J → ℝ) (z : J → ℝ)
    (hU : ∀ i j, 0 ≤ U i j)
    (habs : ∀ i j, |T i j| ≤ U i j) :
    Σ i, ((Σ j, T i j * z j) ^ 2)
      ≤ (Σ i, Σ j, (U i j) ^ 2) * (Σ j, (z j) ^ 2)
```

A standard real proof, recorded here only as an obligation, uses three finite steps and no Route-B data:

1. Entrywise comparison: `|(T z)_i| ≤ Σ_j |T_ij| |z_j| ≤ Σ_j U_ij |z_j|`.
2. Row Cauchy-Schwarz: `(Σ_j U_ij |z_j|)^2 ≤ (Σ_j U_ij^2) (Σ_j z_j^2)`.
3. Sum over rows and factor `||z||_2^2` out of the finite sum.

Equality is not claimed. The factor is the squared Frobenius norm of `U`, not an induced-norm estimate. The task already forbids assuming a pointwise order between this factor and an induced-norm bound. Sibling note on `T-P4-021` records that Frobenius does not pointwise dominate the induced bound on the inspected eta grids; this review does not replay those cells and does not select either norm.

This sketch is not a Lean proof. It uses real absolute value, finite sums, and Cauchy-Schwarz, so a future pinned receipt must name the Mathlib lemmas and print axioms. Expected non-kernel axioms should be only the standard propext/Classical.choice/Quot.sound family if the proof stays in `Mathlib.Analysis.InnerProductSpace.PiL2` or an elementary `Fin n` sum proof; that expectation is not a `#print axioms` receipt.

## What this leaf may consume, and what it may not

Allowed later consumer, still external to this review:

```text
fixed nonnegative majorant E_k with |T_ij| ≤ (E_k)_ij
  → ||T z||_2^2 ≤ ||E_k||_F^2 ||z||_2^2
```

Not discharged:

- interval endpoints, outward rounding, or a certified box partition;
- equality of `U` with any Route-B port, descriptor, or `E_k` payload;
- the 5120-cell source, Float64/MPFR evaluation, or solver status;
- `T-P4-023` composition `||R a||_2^2 ≤ rho (a^T B a)`; that leaf must consume this theorem as a separate input;
- robust-PMI identification of `||R a_B||^2` with the error factor in `l_true = l_poly,k + E_k xi`.

## Explicit non-admissions

- Not compiled: no pinned Lean theorem, imports, or axiom print.
- Not proved in-kernel: the Cauchy-Schwarz majorant above.
- Not proved: any source/interval binding of `T`, `U`, or `E_k`.
- Not proved: coverage of the Route-B cell partition.
- Not proved: P4 parent closure or registry promotion.
- `formal_certificate_allowed` and `registry_promoted` are not changed. This file is not a formal certificate.

## Admission label

`pending`

Strongest statement retained: the queue target is a source-independent finite-matrix inequality with an explicit entrywise majorant. The repository has the task card and a general O2 kernel/adapter split, but no theorem artifact for `T-P4-022`. A formula audit cannot enter the registry.

## Proposed integration (coordinator only)

1. Harvest this review as a pending obstruction on `T-P4-022`. Do not close `T-P4-023` or the P4 parent.
2. Do not write `state.json`, the verified registry, or a Lean source file from this review.
3. Next child, out of scope here: a pinned `Fin n` or `PiL2` lemma with `#print axioms`, kept free of Float64 premises. Interval binding stays a separate adapter.

## Unresolved blockers

1. No Lean file and no compile receipt for the majorant theorem.
2. `E_k` / port-entry binding is not in this leaf and was not re-audited.
3. Induced-norm versus Frobenius comparison remains a sibling obstruction, not an input to this generic statement.

## Response / handoff

流川枫 claimed open `T-P4-022` and recorded a pending fail-closed boundary: the entrywise Frobenius majorant is a clean kernel target, but this tree has no pinned theorem, axiom print, or source binding. No registry or formal-proof edit.
